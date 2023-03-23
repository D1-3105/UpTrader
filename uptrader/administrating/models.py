from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager


class UserMenu(AbstractUser):
    ...


class Page(models.Model):
    url = models.CharField(max_length=2048)
    menus = models.ManyToManyField(
        to='menu.Menu',
        through='PageToMenu',
        through_fields=['page', 'menu']
    )
    title = models.TextField(blank=True)
    template_path = models.FileField(
        upload_to=settings.BASE_DIR/'menu/templates/menu',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.url


class PageToMenu(models.Model):
    order = models.SmallIntegerField()
    menu = models.ForeignKey(to='menu.Menu', on_delete=models.CASCADE)
    page = models.ForeignKey(to='Page', on_delete=models.CASCADE)

# Create your models here.
