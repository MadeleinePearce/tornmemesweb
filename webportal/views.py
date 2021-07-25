import math
import requests

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from webportal.models import *


def check_params(r, p):
    return all(list(map(lambda x: x in r and r[x].strip() != "", p)))


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


@csrf_exempt
def loginapi(request):
    response = {"status": 500, "message": "FAILED", "result": None}
    if request.method == "POST" and check_params(request.POST, ["tornapikey"]):
        res = requests.get(
            "https://api.torn.com/user/",
            params={"selections": "profile", "key": request.POST["tornapikey"], "comment": "TornMemes"},
        )
        try:
            res = res.json()
        except:
            res = None
            response["status"] = 404
            response["message"] = "Invalid response received from TORN API"
        if res:
            if "error" in res:
                response["status"] = 404
                response["message"] = res["error"].get("error") or "Unknown Error"
            elif "name" in res and "player_id" in res:
                try:
                    player = TornPlayer.objects.get(torn_id=res["player_id"])
                except:
                    player = TornPlayer(username=res["name"], torn_id=res["player_id"])
                    player.save()
                response["status"] = 200
                response["message"] = "SUCCESS"
                response["result"] = {"apikey": player.apikey, "username": player.username, "torn_id": player.torn_id}
            else:
                response["status"] = 404
                response["message"] = "Failed to identify player"
    else:
        response["status"] = 400
        response["message"] = "Invalid parameters"

    return JsonResponse(response)


@csrf_exempt
def memereactions(request):
    response = {"status": 500, "message": "FAILED", "result": None}
    if (
        request.method == "POST"
        and check_params(request.POST, ["apikey", "meme_id", "reaction"])
        and str(request.POST["meme_id"]).isdigit()
        and request.POST["reaction"] in ["U", "D"]
    ):
        try:
            m = Meme.objects.get(pk=int(request.POST["meme_id"]))
        except:
            m = None
            response["status"] = 404
            response["message"] = "Invalid Meme ID"
        try:
            p = TornPlayer.objects.get(apikey=request.POST["apikey"])
        except:
            p = None
            response["status"] = 403
            response["message"] = "Invalid API key"
        if m and p:
            try:
                log = ReactionLog.objects.get(meme=m, tornplayer=p)
            except:
                log = None
            if log:
                if log.reaction == "U":
                    m.likes -= 1
                    m.save()
                elif log.reaction == "D":
                    m.dislikes -= 1
                    m.save()
                log.delete()
            log = ReactionLog(meme=m, tornplayer=p, reaction=request.POST["reaction"])
            if log.reaction == "U":
                m.likes += 1
                m.save()
            elif log.reaction == "D":
                m.dislikes += 1
                m.save()
            log.save()
            response["status"] = 200
            response["message"] = "SUCCESS"
            response["result"] = {"meme_id": m.id, "likes": m.likes, "dislikes": m.dislikes}
    else:
        response["status"] = 400
        response["message"] = "Invalid parameters"

    return JsonResponse(response)