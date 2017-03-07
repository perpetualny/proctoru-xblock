from django.conf import settings


PROCTORU_EXAM_AWAY_TIMEOUT = getattr(settings, 'PROCTORU_EXAM_AWAY_TIMEOUT', -59)
