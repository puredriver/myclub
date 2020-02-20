from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Rankinglist, Match, Player

import logging
logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
    rankinglists = Rankinglist.objects.all()
    matches = Match.objects.all().order_by('-playedat')
    context = {        
        'rankinglists': rankinglists,
        'matches': matches,
    }
    logger.debug('in index')
    return render(request, 'rankinglist/index.html', context)

def playerhistory(request,player_id):
    player = get_object_or_404(Player, pk=player_id)
    matcheswon = Match.objects.filter(playerone=player)
    matcheslost = Match.objects.filter(playertwo=player)
    context = {        
        'player': player,
        'matcheswon': matcheswon,
        'matcheslost': matcheslost,        
        'matcheswonCount': len(matcheswon),
        'matcheslostCount': len(matcheslost),
    }
    return render(request, 'rankinglist/playerhistory.html', context)