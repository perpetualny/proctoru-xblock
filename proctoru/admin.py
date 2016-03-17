from django.contrib import admin
from django.db import models
from .models import ProctoruUser, ProctorUAuthToken

# Register your models here.


class TokenAdmin(admin.ModelAdmin):
    list_display = ['token', 'date_created', 'enabled']

admin.site.register(ProctorUAuthToken, TokenAdmin)
