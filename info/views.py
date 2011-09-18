from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def findoutmore(request):
    user = request.user
    return render_to_response('info/findoutmore.html', {'user': user}, context_instance=RequestContext(request))

def takeatour(request):
    user = request.user
    return render_to_response('info/takeatour.html', {'user': user}, context_instance=RequestContext(request))

