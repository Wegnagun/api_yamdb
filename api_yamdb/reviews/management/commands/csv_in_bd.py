import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from users.models import CustomUser
from reviews.models import Category, Genre, Title, Review, Comment

TABLES = [
    (CustomUser, 'users.csv'),
    (Category, 'category.csv'),
    (Genre, 'genre.csv'),
    (Comment, 'comments.csv'),
    (Review, 'review.csv'),
    (Title, 'titles.csv')
]


class Command(BaseCommand):
    help = 'import data from csv to sqlite'

    def handle(self, *args, **options):
        if options['load'] is None:
            for model, data in TABLES:
                try:
                    f = open(f'{settings.BASE_DIR}/static/data/{data}', 'r',
                             encoding='utf-8')
                except IOError:
                    self.stdout.write(self.style.ERROR(
                        'Не удалось открыть файл!'))
                else:
                    with f as file:
                        reader = csv.DictReader(file)
                        model.objects.bulk_create(
                            model(**data) for data in reader)
        else:
            for elem in TABLES:
                if options['load'] in elem:
                    try:
                        f = open(
                            f'{settings.BASE_DIR}/static/data/{elem[1]}',
                            'r', encoding='utf-8')
                    except IOError:
                        self.stdout.write(self.style.ERROR(
                            'Не удалось открыть файл!'))
                    else:
                        with f as file:
                            reader = csv.DictReader(file)
                            elem[0].objects.bulk_create(
                                elem[0](**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Все данные загружены'))

    def add_arguments(self, parser):
        parser.add_argument(
            '--load',
            choices=[item[1] for item in TABLES],
            type=str,
            help='Выберите файл для загрузки(пример.csv)'
        )
