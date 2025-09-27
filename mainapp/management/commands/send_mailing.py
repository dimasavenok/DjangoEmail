from django.core.management.base import BaseCommand, CommandError
from mainapp.services import send_mailing_sync
from mainapp.models import Mailing


class Command(BaseCommand):
    help = "Send mailing by id"

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int)

    def handle(self, *args, **options):
        mailing_id = options["mailing_id"]
        try:
            send_mailing_sync(mailing_id)
            self.stdout.write(self.style.SUCCESS(f"Mailing {mailing_id} processed"))
        except Exception as e:
            raise CommandError(f"Error: {e}")
