import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, MyOwnUser, Title, Review, Comment

TABLES = [
    (MyOwnUser, 'users.csv'),
    (Category, 'category.csv'),
    (Genre, 'genre.csv'),
    (Review, 'review.csv'),
    (Comment, 'comments.csv'),
    (Title, 'titles.csv')
]


class Command(BaseCommand):
    help = 'import data from csv to sqlite'

    def handle(self, *args, **options):
        print(options['load'])
        model = TABLES
        with open(f'{settings.BASE_DIR}/static/data/{options["load"]}.csv',
                  'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            options["load"].objects.bulk_create(
                options["load"](**data) for data in reader)

        # for model, data in TABLES.items():
        #     with open(f'{settings.BASE_DIR}/static/data/{data}',
        #               'r', encoding='utf-8') as file:
        #         reader = csv.DictReader(file)
        #         model.objects.bulk_create(model(**data) for data in reader)
        #         self.stdout.write(self.style.SUCCESS(f'{model} обновлен!'))

    def add_arguments(self, parser):
        parser.add_argument(
            '-l',
            '--load',
            choices=[
                'MyOwnUser', 'category', 'genre', 'review', 'comments', 'titles'
            ],
            type=str
        )
