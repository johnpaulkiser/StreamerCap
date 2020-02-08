from django.core.management.base import BaseCommand, CommandError

from rankings.twitch_service import get_top_streams


class Command(BaseCommand):
    help = 'Updates the db with most recent twitch streams'

    # def add_arguments(self, parser):
    #     parser.add_argument('amount to fetch', nargs='+', type=int)

    def handle(self, *args, **options):
        get_top_streams()