from django.db import models
from django.core.exceptions import ValidationError


def reaction_validator(data):
    if data not in ["U", "D"]:
        raise ValidationError(f"'{data}' is not a valid reaction")


class Meme(models.Model):
    class Meta:
        verbose_name = "Meme"
        verbose_name_plural = "Memes"

    time = models.DateTimeField(verbose_name="Time", auto_now_add=True)
    username = models.CharField(max_length=25, verbose_name="Torn Username")
    torn_id = models.CharField(max_length=10, verbose_name="Torn ID")
    caption = models.CharField(max_length=100, verbose_name="Caption", blank=True, null=True)
    image_link = models.URLField(verbose_name="Image URL")


class ReactionLog(models.Model):
    class Meta:
        verbose_name = "Reaction Log"
        verbose_name_plural = "Reaction Logs"

    time = models.DateTimeField(verbose_name="Time", auto_now_add=True)
    torn_id = models.CharField(max_length=10, verbose_name="Torn ID")
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=1, validators=[reaction_validator])
