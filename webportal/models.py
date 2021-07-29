import random
import datetime
from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


def reaction_validator(data):
    if data not in ["U", "D"]:
        raise ValidationError(f"'{data}' is not a valid reaction")


class TornPlayer(models.Model):
    class Meta:
        verbose_name = "Torn Player"
        verbose_name_plural = "Torn Players"

    def generate_apikey():
        return str(uuid4())

    time = models.DateTimeField(verbose_name="Time", auto_now_add=True)
    username = models.CharField(max_length=25, verbose_name="Torn Username", unique=True)
    torn_id = models.CharField(max_length=10, verbose_name="Torn ID", unique=True)
    apikey = models.CharField(max_length=50, verbose_name="TornMemes API Key", unique=True, default=generate_apikey)

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
        return f"{self.caption[:10]} [{self.time.strftime('%H:%M:%S %d/%m/%Y')}]"


class ReactionLog(models.Model):
    class Meta:
        verbose_name = "Reaction Log"
        verbose_name_plural = "Reaction Logs"

    time = models.DateTimeField(verbose_name="Time", auto_now_add=True)
    tornplayer = models.ForeignKey(TornPlayer, on_delete=models.CASCADE)
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=1, validators=[reaction_validator])


class BannerAd(models.Model):
    class Meta:
        verbose_name = "Banner Ad"
        verbose_name_plural = "Banner Ads"

    created_at = models.DateTimeField(verbose_name="Created At", auto_now_add=True)
    tornplayer = models.ForeignKey(TornPlayer, on_delete=models.CASCADE)
    image_link = models.URLField(verbose_name="Image URL")
    redirect_link = models.URLField(verbose_name="Redirect URL")
    validity = models.PositiveIntegerField(verbose_name="Validity (Days)", default=1)

    @property
    def is_valid(self):
        return timezone.now() <= self.created_at + datetime.timedelta(days=self.validity)
    
    def __str__(self):
        if not self.is_valid:
            return f"AD-{self.id} ({self.tornplayer.username}) [EXPIRED]"
        else:
            _r = (self.created_at + datetime.timedelta(days=self.validity)) - timezone.now()
            return f"AD-{self.id} ({self.tornplayer.username}) [{_r.days} days remaining]"

    @staticmethod
    def get_valid_ads(n: int = None):
        if n:
            if len(BannerAd.objects.all()) > 1:
                return random.sample(
                    [ad for ad in BannerAd.objects.all() if ad.is_valid],
                    k=n,
                )
            else:
                return []
        else:
            return [ad for ad in BannerAd.objects.all() if ad.is_valid]
