from decimal import Decimal
import xml.etree.ElementTree as ET
import requests


def get_cbr_rates(date_str: str | None = None) -> dict[str, Decimal]:
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    params = {"date_req": date_str} if date_str else None
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    response.encoding = "windows-1251"

    root = ET.fromstring(response.text)
    rates = {"RUB": Decimal("1")}

    for valute in root.findall("Valute"):
        code = valute.findtext("CharCode")
        nominal = Decimal(valute.findtext("Nominal"))
        value = Decimal(valute.findtext("Value").replace(",", "."))
        if code:
            rates[code] = value / nominal

    return rates


rates = get_cbr_rates()

