from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ProctoruUser(models.Model):

    student = models.ForeignKey(User)

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15} |  \(\d{3}\)[-]\d{3}[-\.]??\d{4}$ | \d{3}[-]\d{3}[-\.]??\d{4}$',
        message=_(u"Num&eacute;ro de t&eacute;l&eacute;phone doit &ecirc;tre saisi dans le format: &apos;999999999&apos;. Jusqu&apos;&agrave; 15 chiffres autoris&eacute;s."))

    phone_number = models.CharField(
        max_length=100, validators=[phone_regex], blank=True)  # validators should be a list

    time_zone = models.CharField(max_length=100)

    address = models.TextField()

    city = models.CharField(max_length=50)

    country = models.CharField(max_length=50)

    state = models.CharField(max_length=50)

    date_created = models.DateTimeField(
        auto_now=True, auto_now_add=False)


class ProctorUAuthToken(models.Model):

    token = models.CharField(max_length=200)

    date_created = models.DateTimeField(
        auto_now=True, auto_now_add=False)

    enabled = models.BooleanField(default=True)


class ProctorUExam(models.Model):

    user = models.ForeignKey(User)

    start_date = models.DateTimeField(verbose_name=_(u"heure de d&eacute;part",))

    actual_start_time = models.DateTimeField(
        verbose_name=_(u"Heure de d&eacute;but r&eacute;elle",), blank=True, null=True)

    is_completed = models.BooleanField(default=False, blank=True)

    is_started = models.BooleanField(default=False, blank=True)

    is_canceled = models.BooleanField(default=False, blank=True)

    block_id = models.CharField(max_length=200)

    end_time = models.DateTimeField(
        verbose_name=_(u"heure de fin",), blank=True, null=True)

    reservation_id = models.CharField(max_length=50)

    reservation_no = models.CharField(max_length=200)

    url = models.TextField()
