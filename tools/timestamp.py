from datetime import datetime
import pytz

EUROPE_TIMEZONE = pytz.timezone("Europe/Paris")

def getTimestampNow():
    return int(datetime.now(EUROPE_TIMEZONE).timestamp())