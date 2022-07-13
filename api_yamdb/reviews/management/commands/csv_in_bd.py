import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title, MyOwnUser

TABLES = {
    MyOwnUser: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    #  когда будут модели раскоментить
    # Reviews: 'reviews.csv,
    # Comments: 'comments.csv,
}


class Command(BaseCommand):
    help = 'import data from csv to sqlite'

    def handle(self, *args, **options):
        for model, data in TABLES.items():
            with open(f'{settings.BASE_DIR}/static/data/{data}',
                      'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                model.objects.bulk_create(model(**data) for data in reader)
                self.stdout.write(f'{model} обновлен!')
