from datetime import datetime, timedelta

def get_seconds_until_midnight():
    now = datetime.now()
    midnight = datetime.combine(now.date() + timedelta(days=1), datetime.min.time())
    return int((midnight - now).total_seconds())