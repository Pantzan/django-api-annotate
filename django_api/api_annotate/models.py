from __future__ import unicode_literals
from django.utils.translation import ugettext as _

from django.utils import timezone
from django.db import models

## the metric class (table) with it's fields (columns)
class Metric(models.Model):
    date = models.DateField(_('date'), default=timezone.now)
    channel = models.CharField(_('channel'), max_length=50, blank=False)
    country = models.CharField(_('country'), max_length=10, blank=False)
    os = models.CharField(_('os'), max_length=6, blank=False)
    impressions = models.PositiveIntegerField(_('impressions'), blank=False)
    clicks = models.PositiveSmallIntegerField(_('clicks'), blank=False)
    installs = models.PositiveSmallIntegerField(_('installs'), blank=False)
    spend = models.FloatField(_('installs'), blank=False)
    revenue = models.FloatField(_('revenue'))

    class Meta:
        verbose_name = "metric"
        verbose_name_plural = "metrices"

    def __str__(self):
        return "%s (%s)" %(self.id, self.date)
