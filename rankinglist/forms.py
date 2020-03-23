from django import forms
from .choices import *
from .models import Rankinglist
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div

class MatchesHistoryForm(forms.Form):
    year = forms.ChoiceField(choices = YEAR_CHOICES,label='Jahr')

class RankinglistSelForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(RankinglistSelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
#        self.helper.form_show_labels = False
        self.fields['rl'].label = ''
#        self.helper.layout = Layout(
#            Field('rl',css_class="form-control form-control-sm"),            
#        )
    
    rankinglists = Rankinglist.objects.filter(active=True).order_by('name')
    rl = forms.ChoiceField(label="Rangliste",choices=[(r.id, r.name) for r in rankinglists])