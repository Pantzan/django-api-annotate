from rest_framework.response import Response
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .serializers import MetricSerializer
from .models import Metric
from .filters import RangeFilter

# the generic view for our metrices
class MetricView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MetricSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_class = RangeFilter
    ordering_fields = [f.name for f in Metric._meta.get_fields()]
    ordering_fields.append('cpi')

    # get the queryset and validate the get arguments
    def get_queryset(self):
        query_parameters = set(self.request.query_params)
        filter_fields = list(RangeFilter._meta.fields)
        all_fields = filter_fields
        all_fields.append('ordering')
        all_fields.append('cpi')
        all_fields.append('offset')

        queryset = Metric.objects.all()
        valid_parameters = all(elem in all_fields for elem in query_parameters)

        if valid_parameters:
            return queryset

        raise ValidationError(detail='Invalid Parameters')

    # manipulate the initialization of the serializator when only values are selected by passing the values field.
    # so the the serializer knows which fields to serialize
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        fields = None
        # is queryset dict values or obects?
        if queryset.count() and isinstance(queryset[0],dict):
            fields = list(queryset[0].keys())

        page = self.paginate_queryset(queryset)

        serializer =  MetricSerializer(page, many=True, fields=fields, context={'request': self.request})
        return Response(serializer.data)
