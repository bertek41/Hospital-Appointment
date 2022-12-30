import requests
import xmltodict

url = "https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?op=TCKimlikNoDogrula"

payload = """<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <TCKimlikNoDogrula xmlns="http://tckimlik.nvi.gov.tr/WS">
      <TCKimlikNo>{0}</TCKimlikNo>
      <Ad>{1}</Ad>
      <Soyad>{2}</Soyad>
      <DogumYili>{3}</DogumYili>
    </TCKimlikNoDogrula>
  </soap12:Body>
</soap12:Envelope>"""

headers = {"Content-Type": "application/soap+xml; charset=utf-8"}


def check_civil(tc, name, surname, year):
    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=payload.format(tc, name, surname, year).encode("utf-8"),
    )
    resp = xmltodict.parse(response.text)["soap:Envelope"]["soap:Body"][
        "TCKimlikNoDogrulaResponse"
    ]["TCKimlikNoDogrulaResult"]
    return resp == "true"
