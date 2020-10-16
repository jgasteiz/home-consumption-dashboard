import datetime
import datetime as datetime_
from typing import List, Optional, Tuple

import pytz
from dateutil import relativedelta
from django.utils import timezone

UTC = pytz.UTC


def parse_date(value: str) -> datetime_.date:
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime_.datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    raise Exception(f'"{value}" is not a valid date format')


def as_localtime(dt, tz=None):
    return timezone.localtime(dt, timezone=tz)


def as_utc(dt):
    return as_localtime(dt, pytz.utc)


def now():
    return as_localtime(timezone.now())


def date(dt: datetime_.datetime) -> datetime_.date:
    return as_localtime(dt).date()


def today() -> datetime_.date:
    return date(timezone.now())


def midnight(_date=None, tz=None):
    if _date is None:
        _date = today()
    naive_midnight = datetime_.datetime.combine(_date, datetime_.datetime.min.time())
    return timezone.make_aware(naive_midnight, timezone=tz)


def next_midnight(_date=None, tz=None):
    if _date is None:
        _date = today()
    return midnight(_date + datetime_.timedelta(days=1), tz=tz)


def datetime_from_date(_date, hour, tz=None):
    naive_datetime = datetime_.datetime.combine(_date, datetime_.time(hour))
    return timezone.make_aware(naive_datetime, timezone=tz)


def get_previous_and_next_dates(
    date_list: List[str], selected_date: datetime.date
) -> Tuple[Optional[str], Optional[str]]:
    """
    Return the previous and next dates of a selected date, using a list of dates as boundaries.
    """
    next_date = (selected_date + relativedelta.relativedelta(days=1)).isoformat()
    if next_date not in date_list:
        next_date = None
    previous_date = (selected_date - relativedelta.relativedelta(days=1)).isoformat()
    if previous_date not in date_list:
        previous_date = None
    return previous_date, next_date
