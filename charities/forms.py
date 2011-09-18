from django import forms
from django.forms import ModelForm
from ds.account.models import CharityRelationship

class CharityRelationshipForm(ModelForm):

    class Meta:
        model = CharityRelationship
        fields = ('favorite', 'queued')



