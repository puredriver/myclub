from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .choices import *

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='Erforderlich. Zur Anzeige in der Rangliste', label='Vorname')
    last_name = forms.CharField(max_length=30, help_text='Erforderlich. Zur Anzeige in der Rangliste', label='Nachname')
    email = forms.EmailField(max_length=254, help_text='Erforderlich. Zum Empfangen von Mails')

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2' )

class MatchesHistoryForm(forms.Form):
    year = forms.ChoiceField(choices = YEAR_CHOICES,label='Jahr')

class MatchNewWizardForm1(forms.Form):
    rankinglist = forms.CharField(max_length=100,label='Rangliste')    

class MatchNewWizardForm2(forms.Form):
    playerone = forms.CharField(max_length=100,label='Spieler 1 (Sieger)')  
    playertwo = forms.CharField(max_length=100,label='Spieler 2')

class MatchNewWizardForm3(forms.Form):
    set1playerone = forms.IntegerField()  
    set1playertwo = forms.IntegerField() 