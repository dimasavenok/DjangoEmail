from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "Create Managers group and assign view permissions"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Managers")
        perms = []
        for app_label, model_name in [
            ("mainapp", "mailing"),
            ("mainapp", "recipient"),
            ("mainapp", "message"),
            ("mainapp", "mailingattempt"),
        ]:
            codename = f"view_all_{model_name}s"
            try:
                p = Permission.objects.get(codename=codename)
                perms.append(p)
            except Permission.DoesNotExist:
                try:
                    p2 = Permission.objects.get(
                        content_type__app_label="mainapp", codename=f"view_{model_name}"
                    )
                    perms.append(p2)
                except Permission.DoesNotExist:
                    pass
        group.permissions.set(perms)
        group.save()
        self.stdout.write(self.style.SUCCESS("Managers group created/updated"))
