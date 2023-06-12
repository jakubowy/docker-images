import requests, csv
from zoneinfo import ZoneInfo


def get(datetime):
    date = datetime
    lista = []
    print(date.strftime("%Y%m%d %-H"))
    response = requests.get("https://www.pse.pl/getcsv/-/export/csv/PL_CENY_RYN_EN/data/" + date.strftime("%Y%m%d"))
    cr = csv.reader(response.content.decode('utf-8').splitlines(), delimiter=';')
    for item in cr:
        if item[0].isnumeric():
            print("Time in zulu")
            item[1] = str(int(item[1])-1)
#            datetime_object = datetime.strptime(item[0] + item[1], '%Y%m%d%H')
            datetime_object = datetime.strptime(item[0] + item[1], '%Y%m%d%H') #.strftime('%m/%d/%y')
            datetime_object = datetime_object.replace(tzinfo=ZoneInfo('Europe/Warsaw'))
            print(int(datetime_object.timestamp()) * 1000)
            print(float(item[2].replace(',','.')))
            lista.append({"timestamp": int(datetime_object.timestamp()) * 1000, "value": float(item[2].replace(',','.')), "unit": "PLN", "name": "electricity-price-hourly"})
    return lista

if __name__ == '__main__':
    pass
