from django.contrib import admin
from .models import Metric

class MetricAdmin(admin.ModelAdmin):
    list_display = ['id','date','country']

admin.site.register(Metric, MetricAdmin)
