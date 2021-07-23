import math
from webportal.models import *
from django.shortcuts import render


def homepage(request):
    memes = Meme.objects.all().order_by("-time")
    total_pages = math.ceil(len(memes) / 15)
    if "page" in request.GET and str(request.GET["page"]).isdigit() and int(request.GET["page"]) > 0:
        _page = int(request.GET["page"])
        memes = memes[15 * (_page - 1) : 15 * _page]
    else:
        memes = memes[:15]
    return render(request, "index.html", {"memes": memes, "total_pages": total_pages})