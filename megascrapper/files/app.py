import pse, os, foxess
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from pprint import pprint
import sys
from gcp_wrappers import get_config, get_secret, update_secret
import time
import dateutil

gcs_config_bucket = os.environ.get("GCS_CONFIG_BUCKET")
config = get_config(gcs_config_bucket)
pprint(config)

token = get_secret(config['influxdb']['secret_path_token'])
print(token)


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
    case "foxess-now":
        print(foxess.plant_detail(config))
    case "foxess-raw":
        print(foxess.raw(config,datetime.now(tz=ZoneInfo("Europe/Warsaw"))))
        #foxess.raw()

    case "pse":
        print(write_api.write(config['pse']['influxdb_bucket'], config['influxdb']['organization'], pse.get((datetime.now() + timedelta(0))), write_precision='s'))
    case _:
        print("Unown command")
        # 2023-06-19 15:00:00 CEST+0200
        data = "2023-06-19 15:00:00 CEST+0200"
        print(dateutil.parser.parse("2023-06-19 15:00:00 CEST+0200").timestamp())
        print(datetime.strptime("2023-06-19 15:00:00 +0200", '%Y-%m-%d %H:%M:%S %z').timestamp())
        #zone = ZoneInfo("CEST")
        #print(ZoneInfo.ZoneInfo("CEST"))