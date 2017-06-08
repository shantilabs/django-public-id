from django.db import models

from public_id.fields import PublicIdField


class Post(models.Model):
    public_id = PublicIdField(auto=True)


class PostNoAuto(models.Model):
    public_id = PublicIdField()
