from django.core.management.base import BaseCommand, CommandError

from rankings.mixer_service import streams_to_db
import json

class Command(BaseCommand):
    help = 'Updates the db with most recent twitch streams'

    def add_arguments(self, parser):
        parser.add_argument('amount to fetch', nargs='+', type=int)

    def handle(self, *args, **options):
        streams_to_db(options['amount to fetch'][0])