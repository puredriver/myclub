from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from operator import itemgetter
from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Rankinglist, Match, Player
from .forms import MatchesHistoryForm, SignUpForm

import logging
logger = logging.getLogger('rankinglist')

# Create your views here.

def index(request):
    rankinglists = Rankinglist.objects.filter(active=True)
    matches = Match.objects.all().exclude(status=Match.GEPLANT).order_by('-playedat')[:10] # first 10
    matches_planned=Match.objects.filter(status=Match.GEPLANT).order_by('playedat')
    context = {        
        'rankinglists': rankinglists,
        'matches': matches,
        'matches_planned': matches_planned,
    }
    # logger.debug('in index')
    return render(request, 'rankinglist/index.html', context)

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
    m = Match.objects.all().order_by('-playedat') # TODO in 2021 - load by year
    return render(request, 'rankinglist/matcheshistory.html', {'form': form, 'matches': m})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'rankinglist/signup.html', {'form': form})

class MatchCreateView(CreateView):
    model = Match
    # form_class = MatchForm
    fields = ['rankinglist','playerone','playertwo','status','playedat']
    success_url = "index"

class MatchNewWizard(SessionWizardView):
    template_name = 'rankinglist/matchnewwizard.html'
    
    def done(self, form_list, **kwargs):
        logger.debug("in match new wizard")
        # do_something_with_the_form_data(form_list)
        return HttpResponseRedirect(reverse('index'))