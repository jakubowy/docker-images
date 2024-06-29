import pse-new-api, os, foxess
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from pprint import pprint
import sys
from gcp_wrappers import get_config, get_secret, update_secret
import time
import dateutil
from dateutil.relativedelta import relativedelta
import foxesscloud.openapi as foxcloud

gcs_config_bucket = os.environ.get("GCS_CONFIG_BUCKET")
config = get_config(gcs_config_bucket)
pprint(config)

token = get_secret(config['influxdb']['secret_path_token'])


print(datetime.now(timezone.utc).strftime("%Y%m%d %-H"))
print(ZoneInfo('Europe/Warsaw'))

client = influxdb_client.InfluxDBClient(url=config['influxdb']['host'], token=token, org=config['influxdb']['organization'])

#write_api = client.write_api()
write_api = client.write_api(write_options=SYNCHRONOUS)

if len(sys.argv) > 1:
    whattorun = sys.argv[1]
else:
    whattorun = ""

match whattorun:
    case "foxesscloud-now":
        fox_vars = config['foxess']['fox_vars']
        foxcloud.api_key = get_secret(config['foxess']['secret_path_token'])
        foxcloud.device_sn = config['foxess']['device_sn']
        foxcloud.time_zone = "Europe/Warsaw"
        foxcloud.debug_setting = 2
        #pprint(foxcloud.get_vars())
        #pprint(foxcloud.get_real(fox_vars))
        fox_device = foxcloud.get_device()
        pprint(fox_device)
        lista = []
        utc = datetime.now(timezone.utc)
        for value in ["generationMonth", "generationToday", "generationTotal"]:
            print(value + str(fox_device[value]))
            match value:
                case "generationMonth":
                    timesp = "month"
                case "generationToday":
                    timesp = "today"
                case "generationTotal":
                    timesp = "cumulate"
                case _:
                    timesp = "unknown"
            lista.append({"measurement": "foxess", "tags": {"unit":"Wh","timespan":timesp}, "fields": {"power":float(fox_device[value]) * 1000}, "time": int(utc.timestamp())})
        pprint(lista)
        print(write_api.write(config['foxess']['influxdb_bucket'], config['influxdb']['organization'], lista, write_precision='s'))
        print(foxcloud.get_access_count())

    case "foxess-now":
        print(write_api.write(config['foxess']['influxdb_bucket'], config['influxdb']['organization'], foxess.plant_detail(config), write_precision='s'))
        #pprint(foxess.plant_detail(config))
    case "foxess-raw":
        print(write_api.write(config['foxess']['influxdb_bucket'], config['influxdb']['organization'], foxess.raw(config,datetime.now(tz=ZoneInfo("Europe/Warsaw")) - timedelta(hours=1)), write_precision='s'))
        print(write_api.write(config['foxess']['influxdb_bucket'], config['influxdb']['organization'], foxess.raw(config,datetime.now(tz=ZoneInfo("Europe/Warsaw"))), write_precision='s'))
        #pprint(foxess.raw(config,datetime.now(tz=ZoneInfo("Europe/Warsaw")) - timedelta(hours=1)))
        #foxess.raw()
    case "foxess-history":
        for godziny in range(config['foxess']['history_start'],config['foxess']['history_stop']):
            print(f"HISTORY MODE, PROCESSING: {godziny}")
            print(write_api.write(config['foxess']['influxdb_bucket'], config['influxdb']['organization'], foxess.raw(config,datetime.now(tz=ZoneInfo("Europe/Warsaw")) - timedelta(hours=godziny)), write_precision='s'))
            time.sleep(30)
    case "foxess-history-month":
        for months in range(config['foxess']['history_start'],config['foxess']['history_stop']):
            print(f"{config['foxess']['history_start']} --------------  {config['foxess']['history_stop']}")
            print(f"HISTORY MODE MONTHLY, PROCESSING: {months}")
            print(write_api.write(config['foxess']['influxdb_bucket'], config['influxdb']['organization'], foxess.raw_month(config,datetime.now(tz=ZoneInfo("Europe/Warsaw")) - relativedelta(months=months)), write_precision='s'))
            time.sleep(30)

    case "pse":
        print(write_api.write(config['pse']['influxdb_bucket'], config['influxdb']['organization'], pse-new-api.get_report_json((datetime.now() + timedelta(config['pse']['time_delta']))), write_precision='s'))
    case _:
        print("Unown command")
        # 2023-06-19 15:00:00 CEST+0200
        data = "2023-06-19 15:00:00 CEST+0200"
        print(dateutil.parser.parse("2023-06-19 15:00:00 CEST+0200").timestamp())
        print(datetime.strptime("2023-06-19 15:00:00 +0200", '%Y-%m-%d %H:%M:%S %z').timestamp())
        #zone = ZoneInfo("CEST")
        #print(ZoneInfo.ZoneInfo("CEST"))
