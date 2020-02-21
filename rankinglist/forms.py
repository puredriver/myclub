from django import forms
from .choices import *

class MatchesHistoryForm(forms.Form):
    year = forms.ChoiceField(choices = YEAR_CHOICES,label='Jahr')