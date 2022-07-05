from django.db import models

class Choice(models.Model):
    music_name = models.CharField(max_length=200)
    image_id = models.CharField(max_length=200)
    def __str__(self):
        return self.music_name
