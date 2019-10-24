This is a Django app to import data from a csv file and then provide an api point to view the stored metrices in various filters and forms.

### installation:
- pip3 install -r requirements
- python manage.py migrate
- python manage.py csvimport --path dataset.csv

### then a user should be created and be logged in to view the api.
- python manage.py createsuperuser 

## Common API use-cases:

1. Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order.

- http://127.0.0.1:8000/api/metrices/?fields=channel,country&annotate=sum_impressions,sum_clicks&end_date=01-06-2017&ordering=-clicks&fields=date

2. Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.

- http://127.0.0.1:8000/api/metrices/?fields=date&os=ios&start_date=06-2017&end_date=07-2017&annotate=count_installs&ordering=-date

3. Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order.

- http://127.0.0.1:8000/api/metrices/?fields=os&annotate=count_revenue&date=1-06-2017&ordering=-date

4. Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order. Please think carefully which is an appropriate aggregate function for CPI.

- http://127.0.0.1:8000/api/metrices/?cpi=true&fields=channel&annotate=count_spend&ordering=-cpi

##### The api can be field selected, sorted, grouped, annotated date choosed by date, start_date and end_date for any single field in the Metric table

## test
to run the tests
- python manage.py test
