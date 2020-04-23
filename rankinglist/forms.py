from django import forms
from .choices import *
from .models import Rankinglist, Match, Ranking, Club
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField

class MatchesHistoryForm(forms.Form):
    year = forms.ChoiceField(choices = YEAR_CHOICES,label='Jahr')

#class RankinglistSelForm(forms.Form):
#    def __init__(self, *args, **kwargs):
#        super(RankinglistSelForm, self).__init__(*args, **kwargs)
#        self.helper = FormHelper()
#        self.helper.form_show_labels = False
        #self.fields['rl'].label = ''
#        self.helper.layout = Layout(
#            Field('rl',css_class="form-control form-control-sm"),            
#        )
    
#    rankinglists = Rankinglist.objects.filter(active=True).order_by('name')
#    rl = forms.ChoiceField(label="Rangliste",choices=[(r.id, r.name) for r in rankinglists])

class MatchAdminForm(forms.ModelForm):
    class Meta:
        model = Match
        exclude = ('update_user','updatedate','activatedate','activate_user')

    def clean(self):
        cleaned_data = self.cleaned_data

        # check whether ranking exists
        rankinglist = cleaned_data.get('rankinglist')        
        playerone = cleaned_data.get('playerone')
        playertwo = cleaned_data.get('playertwo')

        ranking_playerone = Ranking.objects.filter(rankinglist=rankinglist,player=playerone).first()
        ranking_playertwo = Ranking.objects.filter(rankinglist=rankinglist,player=playertwo).first()
        
        if ranking_playerone is None: 
            raise forms.ValidationError('Das Spiel kann nicht gespeichert werden. Spieler 1 hat noch keine Ranglistenposition')

        if ranking_playertwo is None:
            raise forms.ValidationError('Das Spiel kann nicht gespeichert werden. Spieler 2 hat noch keine Ranglistenposition')

        return cleaned_data

class SignUpForm(UserCreationForm):
    club = forms.ModelChoiceField(queryset=Club.objects.all(), empty_label=None)
    leistungsklasse = forms.IntegerField( max_value=23, min_value=1,required=False)
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ('club','first_name', 'last_name','leistungsklasse', 'username', 'email', 'password1', 'password2', )