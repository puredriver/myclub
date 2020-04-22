from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from operator import itemgetter
from django.contrib.auth.models import User

from .models import Rankinglist, Match, Player, Ranking, Club
from .forms import MatchesHistoryForm

import logging
logger = logging.getLogger('rankinglist')

# Create your views here.

def index(request):
    clubs = Club.objects.all()
    context = {        
        'clubs': clubs,
    }
    # logger.debug('in index')
    return render(request, 'rankinglist/index.html', context)

def clubmain(request,club_id):
    print(slug)
    rankinglists = Rankinglist.objects.filter(active=True)
    matches = Match.objects.all().exclude(status=Match.GEPLANT).order_by('-playedat')[:10] # first 10
    matches_planned=Match.objects.filter(status=Match.GEPLANT).order_by('playedat')
    context = {        
        'rankinglists': rankinglists,
        'matches': matches,
        'matches_planned': matches_planned,
    }
    return render(request, 'rankinglist/clubmain.html', context)

def playerhistory(request,player_id):
    player = get_object_or_404(User, pk=player_id)
    matcheswon = Match.objects.filter(playerone=player).exclude(status=Match.GEPLANT)
    matcheslost = Match.objects.filter(playertwo=player).exclude(status=Match.GEPLANT)
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
        countWon = Match.objects.filter(rankinglist=rankinglist,playerone=ranking.player).exclude(status=Match.GEPLANT).count()
        countLost= Match.objects.filter(rankinglist=rankinglist,playertwo=ranking.player).exclude(status=Match.GEPLANT).count()
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
        if (form.is_valid()):
            year = form.cleaned_data['year']
            logger.debug("Year %s in matches history" %(year))
            # TODO in 2021 - load by year
            return render(request, 'rankinglist/matcheshistory.html', {'form': form, 'matches': []})
    else:
        form = MatchesHistoryForm()
    m = Match.objects.all().exclude(status=Match.GEPLANT).order_by('-playedat') # TODO in 2021 - load by year
    return render(request, 'rankinglist/matcheshistory.html', {'form': form, 'matches': m})

 