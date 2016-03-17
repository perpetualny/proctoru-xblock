from django import template
from datetime import datetime, timedelta
from dateutil import parser
import pytz
import time
from ..models import ProctoruUser
from ..timezonemap import win_tz

register = template.Library()


@register.filter
def get_ramaining_timestamp(tm, user_id):
    try:
        user = ProctoruUser.objects.get(student=user_id)

        tzobj = pytz.timezone(win_tz[user.time_zone])

        dt = parser.parse(tm).astimezone(tzobj)
        utcmoment_unaware = datetime.utcnow()
        utcmoment = utcmoment_unaware.replace(tzinfo=pytz.utc)

        delta = dt - utcmoment
        return "{0} Days {1} Hours {2} Minutes from now".format(delta.days, delta.seconds//3600, (delta.seconds//60) % 60)
    except:
        return False


@register.filter
def get_ramaining_timestamp_status(tm, user_id):
    try:
        user = ProctoruUser.objects.get(student=user_id)

        tzobj = pytz.timezone(win_tz[user.time_zone])

        dt = parser.parse(tm).astimezone(tzobj)
        utcmoment_unaware = datetime.utcnow()
        utcmoment = utcmoment_unaware.replace(tzinfo=pytz.utc)

        delta = dt - utcmoment
        if delta.days < 0:
            return 'hidden'
        else:
            return ''
    except:
        return False


@register.filter
def get_seconds_from_minutes(minutes):
    return int(minutes) * 60


@register.filter
def filter_date_format(dt):
    return parser.parse(dt).strftime("%m/%d/%Y")


@register.filter
def format_date(tm):
    tm = parser.parse(tm)
    return tm.strftime("%I:%M %p %A %B %dth, %Y")
