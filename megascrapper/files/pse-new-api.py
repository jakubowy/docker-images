import requests
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

print("HellloW")

#query_date = datetime.today()

def get_report_json(query_date):
    response = requests.get("https://api.raporty.pse.pl/api/rce-pln?$filter=doba%20eq%20'" +query_date.strftime("%Y-%m-%d") +"'")
    lista = []
    for item in response.json()['value']:
        print(item)
        start_time = datetime.strptime(item['udtczas'], '%Y-%m-%d %H:%M')
        start_time = start_time.replace(tzinfo=ZoneInfo('Europe/Warsaw'))
        start_time = start_time - timedelta(hours=0, minutes=15)
        print(start_time)
        lista.append({"measurement": "rce", "tags": {"unit":"PLN/MWh","timespan":"15min"}, "fields": {"price":float(item['rce_pln'])}, "time": int(start_time.timestamp())})
    return lista

#print(get_report_json(datetime.today()))
# curl -vs -X GET "https://api.raporty.pse.pl/api/rce-pln?\$filter=doba%20eq%20'2024-06-29'" |jq '.'


if __name__ == '__main__':
    pass

