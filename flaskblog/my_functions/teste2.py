from datetime import datetime, timezone

utc_dt = datetime.utcnow()
print(utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None))