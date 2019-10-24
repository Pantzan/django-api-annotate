import csv
from django.core.management import BaseCommand
from api_annotate.models import Metric
import logging

## initiate the command object, validate file and create Metric objects for each row in the file
class Command(BaseCommand):
    help = 'Import .CSV file into a model'
    logger = logging.getLogger(__name__)

    def add_arguments(self, parser):
        import argparse
        parser.add_argument('--path', type=str,help='pass a csv file to import')

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        if self.validate_csv_file(path):
            with open(path, 'r') as csv_file:
                reader = csv.DictReader(open(path), delimiter=',', quotechar='"')
                print("---")
                print("Creating Metric objects. This might take few minutes")
                for row in reader:
                    Metric.objects.create(
                            date = row['date'],
                            channel = row['channel'],
                            country = row['country'],
                            os = row['os'],
                            impressions = row['impressions'],
                            clicks = row['clicks'],
                            installs = row['installs'],
                            spend = row['spend'],
                            revenue = row['revenue'],
                        )
            csv_file.close()

    ## validate the file for it's integrity by reading headers and check if rows have the valid delimiter
    def validate_csv_file(self, file):
        valid_headers = [f.name for f in Metric._meta.get_fields()]
        with open(file, newline = "") as csv_file:
            try:
                reader = csv.Sniffer().sniff(csv_file.read(1024), delimiters = ",")
                csv_file.seek(0)
                reader = csv.DictReader(open(file), delimiter=',', quotechar='"')
                headers = reader.fieldnames
                validate_headers = all(field in valid_headers for field in headers)

                if not validate_headers:
                    print('Headers of the file do not much with the model')
                    logger.error('Wrong csv file attempted to be imported')
                    csv_file.close()
                    return False

                return True
            except csv.Error:
                print("There was an error with the .csv file")
                logger.error('Error in .csv file during the importing')
                csv_file.close()
                return False
