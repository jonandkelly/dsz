from django.forms import ModelForm
from django.db.models import Q
from django.forms.extras.widgets import SelectDateWidget
from ds.goals.models import Goal
from ds.goals.models import Downsize
from ds.goals.models import Saving
from ds.charities.models import Charity

class SavingForm(ModelForm):
    class Meta:
        model = Saving
        fields = ('saving_type',)


class GoalForm(ModelForm):
    def __init__(self,user,*args,**kwargs):
        super(GoalForm,self).__init__(*args,**kwargs)
        self.fields['charity'].queryset = Charity.objects.filter(Q(charityrelationship__userprofile=user.userprofile) & Q(charityrelationship__favorite=True) | Q(charityrelationship__queued=True) | Q(charityrelationship__donated=True))
    class Meta:
        model = Goal
        fields = ('charity',)

class DownsizeForm(ModelForm):
    def __init__(self,user,*args,**kwargs):
        super(DownsizeForm,self).__init__(*args,**kwargs)
        self.fields['saving'].queryset = Saving.objects.filter(savingrelationship__userprofile=user.userprofile)
    class Meta:
        model = Downsize
        widgets = {
            'downsize_date': SelectDateWidget(),
        }
