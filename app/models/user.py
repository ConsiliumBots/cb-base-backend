from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):

    email = models.EmailField(max_length=200, blank=True, null=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        app_label = 'app'
        db_table = 'app_user'
