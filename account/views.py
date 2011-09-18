from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from ds.account.forms import PreferencesForm

def preferences(request):
    user = request.user
    preferences = user.preferences
    if request.method == 'POST':
        form = PreferencesForm(request.POST, instance=preferences)
        form.save()
        return HttpResponseRedirect('../../goals/dashboard')
    else:
        form = PreferencesForm(instance=preferences)
    return render_to_response('account/preferences.html', {'form': form, 'user': user}, context_instance=RequestContext(request))
