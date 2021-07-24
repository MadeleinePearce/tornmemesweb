from django.db import models
from django.core.exceptions import ValidationError


def reaction_validator(data):
    if data not in ["U", "D"]:
        raise ValidationError(f"'{data}' is not a valid reaction")


class TornPlayer(models.Model):
    class Meta:
        verbose_name = "Torn Player"
        verbose_name_plural = "Torn Players"

    time = models.DateTimeField(verbose_name="Time", auto_now_add=True)
    username = models.CharField(max_length=25, verbose_name="Torn Username", unique=True)
    torn_id = models.CharField(max_length=10, verbose_name="Torn ID", unique=True)
    apikey = models.CharField(max_length=25, verbose_name="Custom API Key", unique=True)

    def __str__(self):
        return self.username + f" [{self.torn_id}]"


class Meme(models.Model):
    class Meta:
        verbose_name = "Meme"
        verbose_name_plural = "Memes"

    time = models.DateTimeField(verbose_name="Time", auto_now_add=True)
    tornplayer = models.ForeignKey(TornPlayer, on_delete=models.CASCADE)
    caption = models.CharField(max_length=50, verbose_name="Caption", blank=True, null=True)
    image_link = models.URLField(verbose_name="Image URL")
    likes = models.PositiveIntegerField(verbose_name="Likes", default=0)
    dislikes = models.PositiveIntegerField(verbose_name="Dislikes", default=0)

    def __str__(self):
        return f"Meme ({self.caption}) [{self.time.strftime('%H:%M:%S %d/%m/%Y')}]"


class ReactionLog(models.Model):
    class Meta:
        verbose_name = "Reaction Log"
        verbose_name_plural = "Reaction Logs"

    time = models.DateTimeField(verbose_name="Time", auto_now_add=True)
    tornplayer = models.ForeignKey(TornPlayer, on_delete=models.CASCADE)
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=1, validators=[reaction_validator])
