import pse
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

print(datetime.now(timezone.utc).strftime("%Y%m%d %-H"))
print(ZoneInfo('Europe/Warsaw'))
print(pse.get(datetime.now()))
