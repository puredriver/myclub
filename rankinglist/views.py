from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from operator import itemgetter
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse

from .models import Rankinglist, Match, Player, Ranking, Club
from .forms import MatchesHistoryForm, SignUpForm
from .tokens import account_activation_token


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
    club = get_object_or_404(Club,pk=club_id)
    request.session['club_name'] = club.name
    request.session['club_id'] = club.id
    rankinglists = Rankinglist.objects.filter(club=club ,active=True)
    matches = Match.objects.filter(rankinglist__in=rankinglists).exclude(status=Match.GEPLANT).order_by('-playedat') # [:10] first 10
    matches_planned=Match.objects.filter(rankinglist__in=rankinglists,status=Match.GEPLANT).order_by('playedat')
    context = {        
        'rankinglists': rankinglists,
        'matches': matches,
        'matches_planned': matches_planned,
        'club': club,
    }
    return render(request, 'rankinglist/clubmain.html', context)

def playerhistory(request,club_id,player_id):
    player = get_object_or_404(User, pk=player_id)
    club = get_object_or_404(Club,pk=club_id)
    matcheswon = Match.objects.filter(playerone=player).exclude(status=Match.GEPLANT)
    matcheslost = Match.objects.filter(playertwo=player).exclude(status=Match.GEPLANT)
    context = {        
        'player': player,
        'matcheswon': matcheswon,
        'matcheslost': matcheslost,        
        'matcheswonCount': len(matcheswon),
        'matcheslostCount': len(matcheslost),     
        'club': club,   
    }
    return render(request, 'rankinglist/playerhistory.html', context)

def rankingliststats(request,club_id,rankinglist_id):
    club = get_object_or_404(Club,pk=club_id)
    rankinglist = get_object_or_404(Rankinglist, pk=rankinglist_id)
    playerList = []
    for ranking in rankinglist.rankings.all():
        countWon = Match.objects.filter(rankinglist=rankinglist,playerone=ranking.player).exclude(status=Match.GEPLANT).count()
        countLost= Match.objects.filter(rankinglist=rankinglist,playertwo=ranking.player).exclude(status=Match.GEPLANT).count()
        playerList.append((ranking.player,countWon+countLost))

    # todo count matches in rankinglist by player in playerList
    context = {        
        'rankinglist': rankinglist,
        'players': sorted(playerList,key=itemgetter(1),reverse=True),
        'club': club,
    }
    return render(request, 'rankinglist/rankingliststats.html', context)

#def matcheshistory(request):
#    if( request.method == 'POST'):
#        form = MatchesHistoryForm(request.POST)
#        if (form.is_valid()):
#            year = form.cleaned_data['year']
#            logger.debug("Year %s in matches history" %(year))
            # TODO in 2021 - load by year
#            return render(request, 'rankinglist/matcheshistory.html', {'form': form, 'matches': []})
#    else:
#        form = MatchesHistoryForm()
#    m = Match.objects.all().exclude(status=Match.GEPLANT).order_by('-playedat') # TODO in 2021 - load by year
#    return render(request, 'rankinglist/matcheshistory.html', {'form': form, 'matches': m})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.player.leistungsklasse = form.cleaned_data.get('leistungsklasse')
            user.player.club = form.cleaned_data.get('club')
            user.save()
            current_site = get_current_site(request)
            subject = 'Bestätige deine Registrierung bei mytennisclub.online'
            message = render_to_string('rankinglist/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.add_message(
                request, messages.INFO, "Die Registrierung war erfolgreich. Bitte bestätigen sie die Emailadresse in ihrem Postfach."
            )
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'rankinglist/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        # user.is_active = True
        user.player.email_confirmed = True
        user.save()
        login(request, user)
        messages.add_message(
                request, messages.INFO, "Die Emailbestätigung war erfolgreich."
            )
        return redirect('index')
    else:
        return render(request, 'rankinglist/account_activation_invalid.html')

def account_activation_sent(request):
    return render(request, 'rankinglist/account_activation_sent.html')

class UserUpdateView(LoginRequiredMixin, UpdateView):
    #form_class = UserChangeForm
    model = User    
    template_name = 'rankinglist/user_update.html'
    fields = ["first_name","last_name","email"]
    

    def get_success_url(self):
        # return reverse("users_detail", kwargs={"username": self.request.user.username})
        return reverse("index")

    #def get_object(self):
    #    return User.objects.get(pk=self.request.user.pk)
        #return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, "Profil wurde erfolgreich aktualisiert"
        )
        return super().form_valid(form)