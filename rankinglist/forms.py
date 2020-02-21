from django import forms
from .choices import *

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