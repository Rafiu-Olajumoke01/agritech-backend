from django.db import models
from django.conf import settings

class Content(models.Model):
    CONTENT_TYPES = (
        ('article', 'Article'),
        ('tip', 'Tip'),
        ('news', 'News Update'),
        ('tutorial', 'Tutorial'),
        ('alert', 'Weather/Market Alert'),
    )

    title = models.CharField(max_length=255)
    body = models.TextField()
    type = models.CharField(max_length=20, choices=CONTENT_TYPES)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.SET_NULL,
        null=True
    )

    cover_image = models.ImageField(upload_to='content/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title
