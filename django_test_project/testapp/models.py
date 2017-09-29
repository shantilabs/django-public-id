from django.db import models

from public_id.fields import PublicIdField


class Post(models.Model):
    public_id = PublicIdField(auto=True)
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)


class PostNoAuto(models.Model):
    public_id = PublicIdField()


class TableWithIdOnly(models.Model):
    public_id = PublicIdField()
