from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q
from ds.goals.models import Goal, Downsize, SavingCategory, Saving, AddNewGoalToQueue, AllocateDownsize, UpdatePoints, UpdateGoalQueueOrder, SwapGoalCharities, CreateDownsize, DeleteDownsize
from ds.goals.forms import GoalForm, DownsizeForm, SavingForm
from ds.charities.models import RandomizeSpotlightCharities
from ds.account.models import UserProfile, SavingRelationship
from django_facebook.official_sdk import GraphAPI, get_user_from_cookie
from django_facebook.api import get_facebook_graph
from ds.settings import FACEBOOK_API_KEY, FACEBOOK_APP_SECRET
import datetime
from django.utils import simplejson

def index(request):
    user = request.user
    return render_to_response('goals/index.html', {'user': user,}, context_instance=RequestContext(request))
    
def home(request):
    user = request.user
    recent_downsize_list = Downsize.objects.all()[:3]
    completed_goal_list = Goal.objects.filter(user=user, queue_order=0)
    queued_goal_list = Goal.objects.filter(user=user, queue_order__gt=1)
    if len(queued_goal_list) == 0:
        next_goal = None
    else:
        next_goal = queued_goal_list[0]
    try:
        current_goal = Goal.objects.get(user=user, queue_order=1)
    except:
        current_goal = None
        current_goal_remaining = None
        current_goal_age = None
        current_goal_progress = None
    else:
        current_goal_remaining = current_goal.savings_goal - current_goal.current_savings
        current_goal_age = (datetime.datetime.now() - current_goal.start_date).days
        current_goal_progress = current_goal.current_savings / current_goal.savings_goal
    trophy_case = user.userprofile.trophy_case.all()
    return render_to_response('goals/home.html', {'user': user, 'completed_goal_list': completed_goal_list, 'queued_goal_list': queued_goal_list, 'current_goal': current_goal, 'next_goal': next_goal, 'current_goal_remaining': current_goal_remaining, 'current_goal_age': current_goal_age, 'recent_downsize_list': recent_downsize_list, 'current_goal_progress': current_goal_progress, 'trophy_case': trophy_case,}, context_instance=RequestContext(request))
    
def dashboard(request):
    user = request.user
    recent_downsize_list = Downsize.objects.filter(allocation__goal__user=user)[:10]
    cleared_goal_list = Goal.objects.filter(user=user, queue_order=-1)
    completed_goal_list = Goal.objects.filter(user=user, queue_order=0)
    queued_goal_list = Goal.objects.filter(user=user, queue_order__gt=1)
    spotlight_charity_list = RandomizeSpotlightCharities()
    spotlight_charity = spotlight_charity_list[0]
    if len(queued_goal_list) == 0:
        next_goal = None
    else:
        next_goal = queued_goal_list[0]
    try:
        current_goal = Goal.objects.get(user=user, queue_order=1)
    except:
        current_goal = None
        current_goal_remaining = None
        current_goal_age = None
        current_goal_progress = None
    else:
        current_goal_remaining = current_goal.savings_goal - current_goal.current_savings
        current_goal_age = (datetime.datetime.now() - current_goal.start_date).days
        current_goal_progress = current_goal.current_savings / current_goal.savings_goal
    trophy_case = user.userprofile.trophy_case.all()
    return render_to_response('goals/dashboard.html', {'user': user, 'cleared_goal_list': cleared_goal_list, 'completed_goal_list': completed_goal_list, 'queued_goal_list': queued_goal_list, 'spotlight_charity': spotlight_charity, 'current_goal': current_goal, 'next_goal': next_goal, 'current_goal_remaining': current_goal_remaining, 'current_goal_age': current_goal_age, 'recent_downsize_list': recent_downsize_list, 'current_goal_progress': current_goal_progress, 'trophy_case': trophy_case}, context_instance=RequestContext(request))

def newgoal(request):
    user = request.user
    if request.method == 'POST':
        form = GoalForm(user, request.POST)
        goal = form.save(commit=False)
        goal.user = user
        goal.save()
        AddNewGoalToQueue(user, goal, goal.charity)
        return HttpResponseRedirect('../dashboard')
    else:
        form = GoalForm(user)
    return render_to_response('goals/newgoal.html', {'form': form, 'user': user}, context_instance=RequestContext(request))

def cleargoal(request, goal_id):
    user = request.user
    goal = get_object_or_404(Goal, pk=goal_id)
    goal.queue_order = -1
    goal.end_date = datetime.datetime.now()
    goal.save()
    UpdatePoints(user, goal)
    return HttpResponseRedirect('../../dashboard')
    
def newsaving(request):
    user = request.user
    if request.method == 'POST':
        form = SavingForm(request.POST)
        saving = form.save()
        try:
            saving_relationship = SavingRelationship.objects.get(userprofile=user.userprofile, saving=saving)
        except:
            SavingRelationship.objects.create(userprofile=user.userprofile, saving=saving)
        return HttpResponseRedirect('../downsize')
    else:
        form = SavingForm()
    return render_to_response('goals/newsaving.html', {'form': form, 'user': user}, context_instance=RequestContext(request))
    
def addsaving(request, saving_id, saving_slug):
    user = request.user
    saving = get_object_or_404(Saving, pk=saving_id)
    try:
        saving_relationship = SavingRelationship.objects.get(userprofile=user.userprofile, saving=saving)
    except:
        SavingRelationship.objects.create(userprofile=user.userprofile, saving=saving)
    return HttpResponseRedirect('../../../downsize/')

def movetotop(request, goal_id):
    user = request.user
    goal_top = get_object_or_404(Goal, pk=goal_id)
    goal_top_charity = goal_top.charity
    current_position = goal_top.queue_order
    adjust_queue_list = Goal.objects.filter(Q(user=user) & Q(queue_order__gt=0) & Q(queue_order__lte=current_position)).order_by('-queue_order')
    i = 1
    for goal in adjust_queue_list:
        if i < current_position:
            goal_down = adjust_queue_list[i]
            goal.charity = goal_down.charity
            goal.save()
            i += 1
    first_in_queue = Goal.objects.get(user=user, queue_order=1)
    first_in_queue.charity = goal_top_charity
    first_in_queue.save()
    return HttpResponseRedirect('../../dashboard')

def moveup(request, goal_id):
    user = request.user
    goal_up = get_object_or_404(Goal, pk=goal_id)
    current_position = goal_up.queue_order
    new_position = current_position - 1
    goal_down = Goal.objects.get(user=user, queue_order=new_position)
    SwapGoalCharities(goal_up, goal_down)
    return HttpResponseRedirect('../../dashboard')

def movedown(request, goal_id):
    user = request.user
    goal_down = get_object_or_404(Goal, pk=goal_id)
    current_position = goal_down.queue_order
    new_position = current_position + 1
    goal_up = Goal.objects.get(user=user, queue_order=new_position)
    SwapGoalCharities(goal_up, goal_down)
    return HttpResponseRedirect('../../dashboard')

def deletegoal(request, goal_id):
    user = request.user
    goal = get_object_or_404(Goal, pk=goal_id)
    adjust_queue_list = Goal.objects.filter(Q(user=user) & Q(queue_order__gt=goal.queue_order))
    UpdateGoalQueueOrder(adjust_queue_list, 1)
    goal.delete()
    return HttpResponseRedirect('../../dashboard')
    
def summary(request, goal_id):
    user = request.user
    goal = get_object_or_404(Goal, pk=goal_id)
    return render_to_response('goals/summary.html', {'user': user, 'goal': goal}, context_instance=RequestContext(request))

def savingcategory(request, savingcategory_id, saving_category):
    user = request.user
    saving_category_list = SavingCategory.objects.all()
    ds_saving_types_list = Saving.objects.filter(ds_suggested=True, saving_categories=savingcategory_id)
    ds_saving_points_list = []
    for saving in ds_saving_types_list:
        try:
            ds_saving_points_list.append(SavingRelationship.objects.get(userprofile=user.userprofile, saving=saving).saving_points)
        except:
            ds_saving_points_list.append(0)
    ds_zipped = zip(ds_saving_types_list, ds_saving_points_list)
    crowd_saving_types_list = Saving.objects.filter(ds_suggested=False, saving_categories=savingcategory_id)
    crowd_saving_points_list = []
    for saving in crowd_saving_types_list:
        try:
            crowd_saving_points_list.append(SavingRelationship.objects.get(userprofile=user.userprofile, saving=saving).saving_points)
        except:
            crowd_saving_points_list.append(0)
    crowd_zipped = zip(crowd_saving_types_list, crowd_saving_points_list)
    if request.method == 'POST':
        form = DownsizeForm(user, request.POST)
        downsize = form.save()
        CreateDownsize(downsize, user)
        return HttpResponseRedirect('../dashboard')
    else:
        form = DownsizeForm(user)
    return render_to_response('goals/downsize.html', {'form': form, 'user': user, 'ds_zipped': ds_zipped, 'crowd_zipped': crowd_zipped, 'saving_category_list': saving_category_list},context_instance=RequestContext(request))
    
def downsize(request):
    user = request.user
    saving_category_list = SavingCategory.objects.all()
    ds_saving_types_list = Saving.objects.filter(ds_suggested=True)
    ds_saving_points_list = []
    for saving in ds_saving_types_list:
        try:
            ds_saving_points_list.append(SavingRelationship.objects.get(userprofile=user.userprofile, saving=saving).saving_points)
        except:
            ds_saving_points_list.append(0)
    ds_zipped = zip(ds_saving_types_list, ds_saving_points_list)
    crowd_saving_types_list = Saving.objects.filter(ds_suggested=False)
    crowd_saving_points_list = []
    for saving in crowd_saving_types_list:
        try:
            crowd_saving_points_list.append(SavingRelationship.objects.get(userprofile=user.userprofile, saving=saving).saving_points)
        except:
            crowd_saving_points_list.append(0)
    crowd_zipped = zip(crowd_saving_types_list, crowd_saving_points_list)
    if request.method == 'POST':
        form = DownsizeForm(user, request.POST)
        downsize = form.save()
        downsize = CreateDownsize(downsize, user)
        #facebook_user = get_user_from_cookie(request.COOKIES, FACEBOOK_API_KEY, FACEBOOK_APP_SECRET)
        graph = get_facebook_graph(request=request)
        downsize_amount = str(downsize.downsize_amount)
        saving = str(downsize.saving)
        post_string = "I downsized $" + downsize_amount + " by " + saving
        graph.put_wall_post(post_string)
        return HttpResponseRedirect('../dashboard')
    else:
        form = DownsizeForm(user)
    return render_to_response('goals/downsize.html', {'form': form, 'user': user, 'ds_zipped': ds_zipped, 'crowd_zipped': crowd_zipped, 'saving_category_list': saving_category_list}, context_instance=RequestContext(request))

def editdownsize(request, downsize_id):
    user = request.user
    downsize = get_object_or_404(Downsize, pk=downsize_id)
    if request.method == 'POST':
        form = DownsizeForm(user, request.POST, instance=downsize)
        downsize = form.save()
        
        return HttpResponseRedirect('../../../dashboard')
    else:
        form = DownsizeForm(user, instance=downsize)
    return render_to_response('goals/editdownsize.html', {'form': form, 'user': user, 'downsize_id': downsize_id}, context_instance=RequestContext(request))

def deletedownsize(request, downsize_id):
    user = request.user
    downsize = get_object_or_404(Downsize, pk=downsize_id)
    DeleteDownsize(downsize)
    return HttpResponseRedirect('../../../dashboard')
