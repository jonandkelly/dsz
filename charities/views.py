from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from ds.charities.models import Charity, CauseCategory, RandomizeSpotlightCharities
from ds.charities.forms import CharityRelationshipForm
from ds.goals.models import Goal, AddNewGoalToQueue

def index(request):
    user = request.user
    spotlight_charity_list = RandomizeSpotlightCharities()
    spotlight_charity = spotlight_charity_list[0]
    ds_charity_list = Charity.objects.all().order_by('-points_raised')[:10]
    category_list = CauseCategory.objects.all()
    return render_to_response('charities/index.html', {'user': user, 'spotlight_charity': spotlight_charity,  'ds_charity_list': ds_charity_list, 'category_list': category_list}, context_instance=RequestContext(request))

def listbycategory(request, category_id, category_slug):
    user = request.user
    category = get_object_or_404(CauseCategory, pk=category_id)
    charity_list = category.charity_set.all()
    queued_list = []
    if len(charity_list) > 0:
        for index, charity in enumerate(charity_list):
            queued_list.append("add")
    zipped = zip(charity_list, queued_list)
    return render_to_response('charities/listbycategory.html', {'user': user, 'category': category, 'zipped': zipped}, context_instance=RequestContext(request))

def addqueued(request, charity_id):
    user = request.user
    userprofile=user.userprofile
    charity = get_object_or_404(Charity, pk=charity_id)
    goal = Goal.objects.create(user=user, charity=charity)  
    AddNewGoalToQueue(user, goal, charity)
    return HttpResponseRedirect('../../../goals/dashboard')

def newcharity(request):
    user = request.user
    return HttpResponseRedirect('../')

