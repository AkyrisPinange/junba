from datetime import datetime
from main.config import START_DATE

def days_from_begin():
    today = datetime.now()
    delta = today.date() - START_DATE.date()
    return delta.days + 1
