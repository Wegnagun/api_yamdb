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
        if options['u']:
            try:
                file = open(f'{settings.BASE_DIR}/static/data/{options["u"]}',
                            'r', encoding='utf-8')
            except IOError:
                self.stdout.write(self.style.ERROR(
                    'Не удалось открыть файл!'))
            else:
                with file:
                    reader = csv.DictReader(file)
                    CustomUser.objects.bulk_create(
                        CustomUser(**data) for data in reader)
        if options['c']:
            try:
                file = open(f'{settings.BASE_DIR}/static/data/{options["c"]}',
                            'r', encoding='utf-8')
            except IOError:
                self.stdout.write(self.style.ERROR(
                    'Не удалось открыть файл!'))
            else:
                with file:
                    reader = csv.DictReader(file)
                    Category.objects.bulk_create(
                        Category(**data) for data in reader)
        if options['g']:
            try:
                file = open(f'{settings.BASE_DIR}/static/data/{options["g"]}',
                            'r', encoding='utf-8')
            except IOError:
                self.stdout.write(self.style.ERROR(
                    'Не удалось открыть файл!'))
            else:
                with file:
                    reader = csv.DictReader(file)
                    Genre.objects.bulk_create(
                        Genre(**data) for data in reader)
        if options['m']:
            try:
                file = open(f'{settings.BASE_DIR}/static/data/{options["m"]}',
                            'r', encoding='utf-8')
            except IOError:
                self.stdout.write(self.style.ERROR(
                    'Не удалось открыть файл!'))
            else:
                with file:
                    reader = csv.DictReader(file)
                    Comment.objects.bulk_create(
                        Comment(**data) for data in reader)
        if options['r']:
            try:
                file = open(f'{settings.BASE_DIR}/static/data/{options["r"]}',
                            'r', encoding='utf-8')
            except IOError:
                self.stdout.write(self.style.ERROR(
                    'Не удалось открыть файл!'))
            else:
                with file:
                    reader = csv.DictReader(file)
                    Review.objects.bulk_create(
                        Review(**data) for data in reader)
        if options['t']:
            try:
                file = open(f'{settings.BASE_DIR}/static/data/{options["t"]}',
                            'r', encoding='utf-8')
            except IOError:
                self.stdout.write(self.style.ERROR(
                    'Не удалось открыть файл!'))
            else:
                with file:
                    reader = csv.DictReader(file)
                    Title.objects.bulk_create(
                        Title(**data) for data in reader)
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
        self.stdout.write(self.style.SUCCESS('Все данные загружены'))

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
