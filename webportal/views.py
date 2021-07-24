import math
from webportal.models import *
from django.shortcuts import render


def homepage(request):
    _memes = Meme.objects.all().order_by("-time")
    _total_pages = math.ceil(len(_memes) / 15)
    if "page" in request.GET and str(request.GET["page"]).isdigit() and int(request.GET["page"]) > 0:
        _page = int(request.GET["page"])
        _memes = _memes[15 * (_page - 1) : 15 * _page]
    else:
        _memes = _memes[:15]
    return render(
        request,
        "index.html",
        {
            "memes_group1": _memes[:3],
            "memes_group2": _memes[3:6],
            "memes_group3": _memes[6:9],
            "memes_group4": _memes[9:12],
            "memes_group5": _memes[12:15],
            "memes_on_page": len(_memes),
            "total_pages": _total_pages,
        },
    )
