import requests
from pprint import pprint
from zoneinfo import ZoneInfo
from datetime import datetime, timezone, timedelta
from gcp_wrappers import get_config, get_secret, update_secret
import re


def login(username, password):
    headers = {"Accept":"application/json, text/plain, */*",
           "Content-Type":"application/json;charset=UTF-8",
           "lang": "en",
           "sec-ch-ua-platform": "macOS",
           "Sec-Fetch-Site": "same-origin",
           "Sec-Fetch-Mode": "cors",
           "Sec-Fetch-Dest": "empty",
           "Referer": "https://www.foxesscloud.com/bus/device/inverterDetail?id=xyz&flowType=1&status=1&hasPV=true&hasBattery=false",
           "Accept-Language":"en-US;q=0.9,en;q=0.8,de;q=0.7,nl;q=0.6",
           "Connection": "keep-alive",
           "X-Requested-With": "XMLHttpRequest",
           "token":"",
           "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
           "contentType": "application/json"}
    data = {"user":username,"password":password}
    response = requests.post('https://www.foxesscloud.com/c/v0/user/login', data = data, headers = headers)
    #print(data)
    token = response.json()['result']['token']
    return token



def check_response(response, config):
    global token
    if response.json()['errno'] == 41808:
        print("auth required")
        update_secret(config['foxess']['secret_path_token'] ,login(get_secret(config['foxess']['secret_path_username']) , get_secret(config['foxess']['secret_path_password']) ))
        print("Updating token")
        return False
    return True

def plant_detail(config):
    token = get_secret(config['foxess']['secret_path_token']) 
    
    headers = {"Accept":"application/json, text/plain, */*",
           "Content-Type":"application/json;charset=UTF-8",
           "lang": "en",
           "sec-ch-ua-platform": "macOS",
           "Sec-Fetch-Site": "same-origin",
           "Sec-Fetch-Mode": "cors",
           "Sec-Fetch-Dest": "empty",
           "Referer": "https://www.foxesscloud.com/bus/device/inverterDetail?id=xyz&flowType=1&status=1&hasPV=true&hasBattery=false",
           "Accept-Language":"en-US;q=0.9,en;q=0.8,de;q=0.7,nl;q=0.6",
           "Connection": "keep-alive",
           "X-Requested-With": "XMLHttpRequest",
           "token":token,
           "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
           "contentType": "application/json"}
 
    response = requests.get(f"https://www.foxesscloud.com/c/v0/plant/earnings/detail?stationID={config['foxess']['stationid']}", headers = headers)
    if not check_response(response, config):
        print("rerun")
    # print(response.status_code)
    # print(response.headers)
    utc = datetime.now(timezone.utc)
    lista = []
    lista.append({"measurement": "foxess", "tags": {"unit":"Wh","timespan": "now"}, "fields": {"power":float(response.json()['result']['power']) * 1000}, "time": int(utc.timestamp())})
    for item in response.json()['result']:
        # print(response.json()['result'][item])
        if "generation" in str(response.json()['result'][item]):
            lista.append({"measurement": "foxess", "tags": {"unit":"Wh","timespan":item}, "fields": {"power":float(response.json()['result'][item]['generation']) * 1000}, "time": int(utc.timestamp())})
            #print(response.json()['result'][item]['generation'])
    #pprint(lista)
    return lista

def raw(config, dateandtime):
    token = get_secret(config['foxess']['secret_path_token']) 
    headers = {"Accept":"application/json, text/plain, */*",
           "Content-Type":"application/json;charset=UTF-8",
           "lang": "en",
           "sec-ch-ua-platform": "macOS",
           "Sec-Fetch-Site": "same-origin",
           "Sec-Fetch-Mode": "cors",
           "Sec-Fetch-Dest": "empty",
           "Referer": "https://www.foxesscloud.com/bus/device/inverterDetail?id=xyz&flowType=1&status=1&hasPV=true&hasBattery=false",
           "Accept-Language":"en-US;q=0.9,en;q=0.8,de;q=0.7,nl;q=0.6",
           "Connection": "keep-alive",
           "X-Requested-With": "XMLHttpRequest",
           "token":token,
           "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
           "contentType": "application/json"}
    data = {"stationID": config['foxess']['stationid'],\
            "variables":\
            ["pv1Volt","pv1Current","pv1Power","pvPower","pv2Volt","pv2Current","pv2Power","RCurrent","RVolt","RFreq","RPower","SCurrent","SVolt","SFreq","SPower","TCurrent","TVolt","TFreq","TPower","ambientTemperation","boostTemperation","invTemperation","generationPower","feedinPower"],\
            "timespan":"hour",\
            "beginDate":{"year":dateandtime.strftime('%Y'),"month":dateandtime.strftime('%-m'),"day":dateandtime.strftime('%-d'),"hour":dateandtime.strftime('%-H'),"minute":dateandtime.strftime('%-M'),"second":dateandtime.strftime('%-S')}\
            }
    response = requests.post('https://www.foxesscloud.com/c/v0/plant/history/raw', json = data, headers = headers)
    print(response.json())
    lista = []
    for item in response.json()['result']:
        print(item['variable'])
        print(item['unit'])
        print(item['name'])
        if 'Volt' in item['variable']:
            item['unit'] = "V"
        if 'Current' in item['variable']:
            item['unit'] = "A"
        if 'Freq' in item['variable']:
            item['unit'] = "hz"
        if 'Temperation' in item['variable']:
            item['unit'] = "°C"
        for reading in item['data']:
            print(reading)
            lista.append({"measurement": "solar", "tags": {"unit":item['unit'],"variable":item['variable']}, "fields": {"value":float(reading['value'])}, "time": int(datetime.strptime(re.sub("[A-Z]{3,4}", r'', reading['time']), '%Y-%m-%d %H:%M:%S %z').timestamp())})
    pprint(lista)
    return response


#print(plant_detail("yz").json())
#raw("yz", datetime.now(tz=ZoneInfo("Europe/Warsaw")) - timedelta(hours=1))

#raw("yz", datetime.now(tz=ZoneInfo("Europe/Warsaw")))

#fuckingdate = "2023-06-14 12:50:00 CEST+0200"

#fromiso = int(fuckingdate, '%Y-%m-%d %H:%M:%S %Z%z').timestamp())
#print(fromiso)
#datenowinwarsaw = datetime.now(tz=ZoneInfo("Europe/Warsaw")) - timedelta(hours=1)
#print(datenowinwarsaw)
#print(datenowinwarsaw - timedelta(hours=1))


#datetime_object = datetime.strptime(item[0] + item[1], '%Y%m%d%H')
#print(date.strftime("%Y%m%d %-H"))