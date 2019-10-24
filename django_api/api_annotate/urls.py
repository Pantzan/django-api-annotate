from django.urls import path
from .views import MetricView

urlpatterns = [
    path('api/metrices/', MetricView.as_view(), name='api-metrices'),
]
