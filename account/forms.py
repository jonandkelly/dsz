from django.forms import ModelForm
from ds.account.models import Preferences

class PreferencesForm(ModelForm):

    class Meta:
        model = Preferences
        exclude = ('user',)


