from collections import OrderedDict
from django.db.models.query import QuerySet
from rest_framework import filters
import django_filters
from django_filters.widgets import RangeWidget
from .models import Metric
from django.db.models import Sum, Max, Min, Avg, Count

# custom filter class for our get Parameters
class RangeFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date',lookup_expr='gt',input_formats=['%Y-%m-%d','%d-%m-%Y','%m-%Y','%Y'])
    end_date = django_filters.DateFilter(field_name='date',lookup_expr='lt',input_formats=['%Y-%m-%d','%d-%m-%Y','%m-%Y','%Y'])
    date = django_filters.DateFilter(field_name='date',lookup_expr='contains',input_formats=['%Y-%m-%d','%d-%m-%Y','%m-%Y','%Y'])
    os = django_filters.CharFilter(field_name='os',lookup_expr='icontains', label="Os")
    country = django_filters.CharFilter(field_name='country',lookup_expr='icontains', label="Country")

    annotate = django_filters.CharFilter(method='fields_annotate',label='annotate')
    fields = django_filters.CharFilter(method='fields_selected',label='fields')
    cpi = django_filters.BooleanFilter(method='cpi_display', label='cpi')

    class Meta:
        model = Metric
        fields = ('start_date', 'end_date', 'date', 'os', 'country', 'annotate', 'fields', 'cpi')

    ## filter to annotate fields by it's function such as Max or Count
    def fields_annotate(self, queryset, value, *args, **kwargs):
        try:
            if args:

                fields = set(args[0].split(','))
                valid_fields = list(queryset.values()[0].keys() if queryset.count() else [])
                valid_prefixes = ['sum', 'max', 'min', 'avg', 'count']

                fields_split = [tuple(f.split("_")) for f in fields]
                fields_to_annotate = dict()

                for m,field in fields_split:
                    if m in valid_prefixes and field in valid_fields:
                        if field not in list(fields_to_annotate.values()):
                            fields_to_annotate[m] = field
                            if m == "max":
                                queryset = queryset.annotate(**{field+"_":Max(field)})
                            elif m == "min":
                                queryset = queryset.annotate(**{field+"_":Min(field)})
                            elif m == "avg":
                                queryset = queryset.annotate(**{field+"_":Avg(field)})
                            elif m == "sum":
                                queryset = queryset.annotate(**{field+"_":Sum(field)})
                            elif m == "count":
                                queryset = queryset.annotate(**{field+"_":Count(field)})
        except ValueError:
            pass
        return queryset

    # filter to select specific fields. It is also useful to make a group_by annotation
    def fields_selected(self, queryset, value, *args, **kwargs):
        try:
            if args:
                fields = set(args[0].split(','))
                valid_fields = list(queryset.values()[0].keys() if queryset.count() else [])
                fields_to_lookup = [f for f in fields if f in valid_fields]
                queryset = queryset.values(*fields_to_lookup)
        except ValueError:
            pass
        return queryset

    # filter to display to calculate and render the cpi value - cpi = spend / installs
    def cpi_display(self, queryset, value, *args, **kwargs):
        from django.db import models
        from django.db.models import Sum, F

        try:
            if args:
                value = args[0]
                if value:
                    queryset = queryset.annotate(cpi=Sum(
                                F('spend') /
                                F('installs'),
                                output_field=models.FloatField()
                            ))
        except ValueError:
            pass
        return queryset

    # as dicts are not in order, make sure that annotation filter will get executed last to perform the group_by after values
    def filter_queryset(self, queryset):
        cleaned_data = OrderedDict(sorted(self.form.cleaned_data.items(),reverse=True))
        fields = cleaned_data.get('fields', None)
        annotate = cleaned_data.get('annotate', None)
        if fields is not None and annotate is not None:
            cleaned_data.move_to_end("annotate")
        for name, value in cleaned_data.items():
            queryset = self.filters[name].filter(queryset, value)
            assert isinstance(queryset, QuerySet), \
                "Expected '%s.%s' to return a QuerySet, but got a %s instead." \
                % (type(self).__name__, name, type(queryset).__name__)
        return queryset
