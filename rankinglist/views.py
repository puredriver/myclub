from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from operator import itemgetter

from .models import Rankinglist, Match, Player
from .forms import MatchesHistoryForm

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

def rankingliststats(request,rankinglist_id):
    rankinglist = get_object_or_404(Rankinglist, pk=rankinglist_id)
    playerList = []
    for ranking in rankinglist.rankings.all():
        countWon = Match.objects.filter(rankinglist=rankinglist,playerone=ranking.player).count()
        countLost= Match.objects.filter(rankinglist=rankinglist,playertwo=ranking.player).count()
        playerList.append((ranking.player,countWon+countLost))

    # todo count matches in rankinglist by player in playerList
    context = {        
        'rankinglist': rankinglist,
        'players': sorted(playerList,key=itemgetter(1),reverse=True)
    }
    return render(request, 'rankinglist/rankingliststats.html', context)

def matcheshistory(request):
    if( request.method == 'POST'):
        form = MatchesHistoryForm(request.POST)
        if ( form.is_valid):
            year = form.cleaned_data['year']
            return render(request, 'rankinglist/matcheshistory.html', {'form': form, 'matches': []})
    else:
        form = MatchesHistoryForm()
    return render(request, 'rankinglist/matcheshistory.html', {'form': form, 'matches': []})
