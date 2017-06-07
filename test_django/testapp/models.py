from django.db import models
from public_id import PublicIdField


class Post(models.Model):
    public_id = PublicIdField(auto=True)

