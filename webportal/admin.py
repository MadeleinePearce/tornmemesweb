from django.contrib import admin

from webportal.models import *


class TornPlayerAdmin(admin.ModelAdmin):
    readonly_fields = ("time",)
    list_display = ("username", "torn_id", "time")
    search_fields = ("username", "torn_id")


class MemeAdmin(admin.ModelAdmin):
    readonly_fields = ("time",)
    list_display = ("time", "tornplayer", "caption", "image_link")
    search_fields = ("tornplayer__username", "tornplayer__torn_id", "image_link", "caption")


class ReactionLogAdmin(admin.ModelAdmin):
    readonly_fields = ("time",)
    list_display = ("time", "tornplayer", "meme", "reaction")
    search_fields = ("tornplayer__torn_id", "tornplayer__username", "meme__caption")


admin.site.register(TornPlayer, TornPlayerAdmin)
admin.site.register(Meme, MemeAdmin)
admin.site.register(ReactionLog, ReactionLogAdmin)
