from datetime import date, timedelta


def last_day():
    today = date.today()

    return today - timedelta(days=1)
