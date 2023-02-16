from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from MainApp.models import Snippet

class Command(BaseCommand):
    help = 'delete snippets created by user'

    def add_arguments(self, parser):
        parser.add_argument('user')

    def handle(self, *args, **options):
        chosen_user = options['user']
        user = User.objects.get(username=chosen_user)
        snippets = Snippet.objects.filter(user_id=user.id)
        snippets.delete()
