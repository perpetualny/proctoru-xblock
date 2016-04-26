# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import ProctoruUser, ProctorUExam


class ProctorUserAdmin(admin.ModelAdmin):
    search_fields = ('student__last_name', 'student__username', 'student__email')
    list_display = ('student', 'date_created', 'time_zone', 'country', 'city')

admin.site.register(ProctoruUser, ProctorUserAdmin)


class ProctorExamAdmin(admin.ModelAdmin):
    search_fields = ('user__last_name', 'user__username', 'user__email')
    list_display = ('block_id', 'user', 'reservation_id', 'reservation_no', 'start_date', 'actual_start_time',
            'is_completed', 'is_started')
    list_filter = ('block_id',)

admin.site.register(ProctorUExam, ProctorExamAdmin)