from django.db import models

# Create your models here.


class Meme(models.Model):
    username = models.CharField(max_length=40)
    caption = models.CharField(max_length=80)
    torn_id = models.PositiveBigIntegerField()
    image_link = models.URLField()


class Reaction(models.Model):
    torn_id = models.PositiveBigIntegerField()

    reactions =(
        ('U', 'Upvote'),
        ('D', 'Downvote'),
        ) 

    meme = models.ForeignKey(to = Meme, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=1, choices=reactions)



    