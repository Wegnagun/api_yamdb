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
    help = 'import data from csv to base'

    def handle(self, *args, **options):
        options_list = (options['u'], options['c'], options['g'], options['m'],
                        options['r'], options['t'])
        if any(map(None.__ne__, options_list)):
            for elem in set(options_list):
                if elem is not None:
                    try:
                        file = open(f'{settings.BASE_DIR}/static/data/{elem}',
                                    'r', encoding='utf-8')
                    except IOError:
                        self.stdout.write(self.style.ERROR(
                            'Не удалось открыть файл!'))
                    else:
                        model = next(filter(lambda x: x[1] == elem, TABLES),
                                     None)
                        with file:
                            reader = csv.DictReader(file)
                            model[0].objects.bulk_create(
                                model[0](**data) for data in reader)
                        self.stdout.write(self.style.SUCCESS(
                            f'Модель {str(model[0])} обновлена!'))

        else:
            for model, data in TABLES:
                try:
                    file = open(f'{settings.BASE_DIR}/static/data/{data}', 'r',
                                encoding='utf-8')
                except IOError:
                    self.stdout.write(self.style.ERROR(
                        'Не удалось открыть файл!'))
                else:
                    with file:
                        reader = csv.DictReader(file)
                        model.objects.bulk_create(
                            model(**data) for data in reader)

    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            const='users.csv',
            nargs='?',
            type=str,
            help='Загрузить users.csv в базу'
        )
        parser.add_argument(
            '-c',
            const='category.csv',
            nargs='?',
            type=str,
            help='Загрузить category.csv в базу'
        )
        parser.add_argument(
            '-g',
            const='genre.csv',
            nargs='?',
            type=str,
            help='Загрузить genre.csv в базу'
        )
        parser.add_argument(
            '-m',
            const='comments.csv',
            nargs='?',
            type=str,
            help='Загрузить comments.csv в базу'
        )
        parser.add_argument(
            '-r',
            const='review.csv',
            nargs='?',
            type=str,
            help='Загрузить review.csv в базу'
        )
        parser.add_argument(
            '-t',
            const='titles.csv',
            nargs='?',
            type=str,
            help='Загрузить titles.csv в базу'
        )
