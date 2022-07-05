from django.db import models

# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    # question = models.ForeignKey(Question, on_delete=models.CASCADE)
    music_name = models.CharField(max_length=200)
    image_id = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)
    def __str__(self):
        return self.music_name
