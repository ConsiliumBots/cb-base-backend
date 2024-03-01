from django.db import models


class Post(models.Model):

    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=2000, blank=False, null=False)

    class Meta:
        app_label = 'app'
        db_table = 'app_post'
