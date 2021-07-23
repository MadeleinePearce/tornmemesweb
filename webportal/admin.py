from django.contrib import admin

from webportal.models import *


class MemeAdmin(admin.ModelAdmin):
    readonly_fields = ("time",)
    list_display = ("time", "username", "image_link")
    search_fields = ("username", "torn_id", "image_link")


class ReactionLogAdmin(admin.ModelAdmin):
    readonly_fields = ("time",)
    list_display = ("time", "torn_id", "meme_id", "reaction")
    search_fields = ("tord_id",)


admin.site.register(Meme, MemeAdmin)
admin.site.register(ReactionLog, ReactionLogAdmin)
