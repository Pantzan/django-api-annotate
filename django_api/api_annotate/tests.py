import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient, force_authenticate
from .models import Metric

## test the django build-in authentication
class AuthenticationTest(TestCase):
    def setUp(self):
        self.client =  APIClient()
        self.username = 'test_user'
        self.password = 'test1234'
        self.user = User.objects.create(username=self.username, password=self.password)

        Metric.objects.create(
            date=datetime.datetime.now(),channel='facebook',country='GR',impressions=23,
            clicks=4,installs=5,spend=0.5,revenue=6.89
            )

        Metric.objects.create(
            date=datetime.datetime.now(),channel='twitter',country='DE',impressions=20,
            clicks=40,installs=1,spend=43.5,revenue=9.89
            )

    def test_authenticate(self):
        from rest_framework.test import APIClient

        queryset = Metric.objects.all()
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get('/api/metrices/')
        assert response.status_code == 200

# test the get request upon the api by specific get parameters
class GetFromApiTest(APITestCase):
    def setUp(self):
        self.username = 'test_user'
        self.password = 'test1234'
        self.user = User.objects.create(username=self.username, password=self.password)

        Metric.objects.create(
            date=datetime.datetime.now(),channel='facebook',country='GR',impressions=23,
            clicks=4,installs=5,spend=0.5,revenue=6.89
            )

        Metric.objects.create(
            date=datetime.datetime.now(),channel='twitter',country='DE',impressions=20,
            clicks=40,installs=1,spend=43.5,revenue=9.89
            )

    def test_get(self):
        client = APIClient()
        queryset = Metric.objects.all().order_by('id')
        client.force_authenticate(user=self.user)
        response = client.get('/api/metrices/?fields=country&annotate=max_impressions')
        client.logout()
        self.assertEqual(response.json()[0]['impressions'], 20)
