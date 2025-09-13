from django.contrib import admin

from mainapp.models import Recipient, Message, Mailing, MailingAttempt

# Register your models here.

admin.site.register(Recipient)
admin.site.register(Message)
admin.site.register(Mailing)
admin.site.register(MailingAttempt)
