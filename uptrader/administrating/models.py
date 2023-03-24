from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.core.files import File
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager

from io import BytesIO


class UserMenu(AbstractUser):
    ...


class Page(models.Model):
    url = models.CharField(max_length=2048, blank=True)
    title = models.TextField(blank=True)
    template = models.FileField(
        upload_to=settings.STATIC_ROOT/'templates',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.url


@receiver(sender=Page, signal=pre_delete)
def delete_page_signal(instance, **kwargs):
    if instance.template:
        instance.template.delete()


@receiver(sender=Page, signal=post_save)
def on_create(instance, created=False, **kwargs):
    print(instance.template)
    if created and not instance.template:
        with open(settings.BASE_DIR/'menu'/'templates'/'menu'/'index.html', 'rb') as f:
            in_mem = BytesIO(f.read())
            instance.template = File(in_mem, 'index.html')
            instance.save()

