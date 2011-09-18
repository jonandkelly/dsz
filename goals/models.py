from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from ds.charities.models import Charity
from ds.account.models import CharityRelationship, SavingRelationship, Trophy, USER, SUPER_USER
import datetime

GOAL_TARGET = 25
DOLLARS_TO_POINTS = 1
DS_TROPHY_POINTS = 25
CHARITY_TROPHY_POINTS = 100
DS_TROPHY_AWARD = "First Downsize"

class SavingCategory(models.Model):
    CATEGORY_CHOICES = (
        (u'foodbev', u'Food & Bev'),
        (u'entertain', u'Entertainment'),
        (u'shopping', u'Shopping'),
        (u'tech', u'Tech'),
        (u'home', u'Home'),
        (u'transport', u'Transport'),
        (u'gifts', u'Gifts'),
        (u'finance', u'Finance'),
        (u'other', u'Other'),
    )
    saving_category = models.CharField("Saving's Category", choices=CATEGORY_CHOICES, max_length=50)
    image = models.URLField("Image")
    def __unicode__(self):
        return self.saving_category
    class Meta:
        ordering = ['saving_category']

class Saving(models.Model):
    saving_type = models.CharField("Type of Savings", max_length=50)
    saving_categories = models.ManyToManyField(SavingCategory)
    description = models.CharField("Description", max_length=250)
    charity_pairing = models.CharField("Suggested Charity Pairing", max_length=100, null=True, blank=True)
    slug = models.SlugField()
    ds_suggested = models.BooleanField("DS Suggested", default=False)
    social = models.BooleanField("Social", default=False)
    resource1 = models.URLField("Resource",  null=True, blank=True)
    resource2 = models.URLField("Resource",  null=True, blank=True)
    resource3 = models.URLField("Resource",  null=True, blank=True)
    DIFFICULTY_CHOICES = (
        (u'easy', u'Easy'),
        (u'medium', u'Medium'),
        (u'hard', u'Hard'),
    )
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES, verbose_name="Difficulty")
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.saving_type)
        super(Saving, self).save(*args, **kwargs)
    def __unicode__(self):
        return self.saving_type
    class Meta:
        ordering = ['saving_type']

class Downsize(models.Model):
    saving = models.ForeignKey(Saving, verbose_name="Saving")
    downsize_date = models.DateField("Downsize Date", default=datetime.datetime.now)
    downsize_amount = models.DecimalField("Downsize Amount", max_digits=20, decimal_places=2)
    def __unicode__(self):
        return self.saving.saving_type      
    class Meta:
        ordering = ['-downsize_date']
    
class Goal(models.Model):
    user = models.ForeignKey(User, verbose_name="User")
    queue_order = models.IntegerField("Queue Order", default=0)
    charity = models.ForeignKey(Charity, verbose_name="Charity")
    start_date = models.DateTimeField("Start Date", null=True, blank=True)
    end_date = models.DateTimeField("End Date", null=True, blank=True)
    savings_goal = models.DecimalField("Savings Goal", max_digits=20, decimal_places=2, default=GOAL_TARGET)
    current_savings = models.DecimalField("Current Savings", max_digits=20, decimal_places=2, default=0)
    def __unicode__(self):
        return self.charity.charity_name
    class Meta:
        ordering = ['queue_order']

class Allocation(models.Model):
    allocation_amount = models.DecimalField("Allocation Amount", max_digits=20, decimal_places=2)
    goal = models.ForeignKey(Goal, verbose_name="Goal")
    downsize = models.ForeignKey(Downsize, verbose_name="Downsize")
    def __unicode__(self):
        return self.goal.charity.charity_name
        
def AddNewGoalToQueue(user, goal, charity):
    queued_goals_list = Goal.objects.filter(user=user, queue_order__gt=0)
    num_queued = len(queued_goals_list)
    goal.queue_order = num_queued + 1
    if goal.queue_order == 1:
        goal.start_date = datetime.datetime.now()
    goal.save()
    try:
        charity_relationship = CharityRelationship.objects.get(userprofile=user.userprofile, charity=goal.charity)
    except:
        CharityRelationship.objects.create(userprofile=user.userprofile, charity=charity, favorite=False, queued=True, donated=False)
    else:
        charity_relationship.queued = True
        charity_relationship.save()
        
def AllocateDownsize(user, goal, downsize, amount, num_goals_completed):
    allocation_amount = min(amount, goal.savings_goal - goal.current_savings)
    Allocation.objects.create(allocation_amount=allocation_amount, goal=goal, downsize=downsize)
    if amount < goal.savings_goal - goal.current_savings:
        goal.current_savings += amount
        amount = 0
    else:
        amount -= (goal.savings_goal - goal.current_savings)
        goal.current_savings = goal.savings_goal
        goal.queue_order = 0
        num_goals_completed += 1
    user.userprofile.save()
    goal.save()
    return (amount, num_goals_completed)

def UpdatePoints(user, goal):
    #update total points donated to charity
    goal.charity.points_raised += goal.current_savings * DOLLARS_TO_POINTS
    goal.charity.save()
    
    #update users points donated to charity
    charity_rel = CharityRelationship.objects.get(userprofile=user.userprofile, charity=goal.charity)
    prev_charity_points = charity_rel.charity_points
    charity_rel.charity_points += goal.current_savings * DOLLARS_TO_POINTS
    #award charity trophy
    if charity_rel.charity_points >= CHARITY_TROPHY_POINTS and prev_charity_points < CHARITY_TROPHY_POINTS:
        charity_trophy = Trophy.objects.get(award=goal.charity.charity_name)
        user.userprofile.trophy_case.add(charity_trophy)
    charity_rel.save()
    
    #update users points donated to saving type
    allocation_list = Allocation.objects.filter(goal=goal)
    for allocation in allocation_list:
        saving_rel = SavingRelationship.objects.get(userprofile=user.userprofile, saving=allocation.downsize.saving)
        saving_rel.saving_points += allocation.allocation_amount * DOLLARS_TO_POINTS
        saving_rel.save()
    
    #update users overall points and status
    prev_ds_points = user.userprofile.ds_points
    user.userprofile.ds_points += goal.current_savings * DOLLARS_TO_POINTS
    if user.userprofile.ds_points < USER:
        user.userprofile.baller_status = 'User'
    elif user.userprofile.ds_points < SUPER_USER:
        user.userprofile.baller_status = 'Super User'
    else:
        user.userprofile.baller_status = 'Mega User'
    #award DS trophy
    if user.userprofile.ds_points >= DS_TROPHY_POINTS and prev_ds_points < DS_TROPHY_POINTS:
        ds_trophy = Trophy.objects.get(award=DS_TROPHY_AWARD)
        user.userprofile.trophy_case.add(ds_trophy)
    user.userprofile.save()

def UpdateGoalQueueOrder(goal_list, queue_decrement):
    for goal in goal_list:
        goal.queue_order -= queue_decrement
        if goal.queue_order == 1:
            goal.start_date = datetime.datetime.now()
        goal.save()
        
def SwapGoalCharities(goal_up, goal_down):
    goal_up_charity = goal_up.charity
    goal_down_charity = goal_down.charity
    goal_down.charity = goal_up_charity
    goal_down.save()
    goal_up.charity = goal_down_charity
    goal_up.save()
    
def CreateDownsize(downsize, user):
    try:
        saving_relationship = SavingRelationship.objects.get(userprofile=user.userprofile, saving=downsize.saving)
    except:
        SavingRelationship.objects.create(userprofile=user.userprofile, saving=downsize.saving)
    num_goals_completed = 0
    amount = downsize.downsize_amount
    i = 1
    while amount > 0:
        goal = Goal.objects.get(user=user, queue_order=i)
        amount, num_goals_completed = AllocateDownsize(user, goal, downsize, amount, num_goals_completed)
        i += 1
    if num_goals_completed > 0:
        adjust_queue_list = Goal.objects.filter(user=user, queue_order__gt=0)
        UpdateGoalQueueOrder(adjust_queue_list, num_goals_completed)
    return downsize
    
def DeleteDownsize(downsize):
    allocation_list = Allocation.objects.filter(downsize=downsize)
    requeue_goal_list = []
    for allocation in allocation_list:
        goal = allocation.goal
        goal.current_savings -= allocation.allocation_amount
        goal.save()
        requeue_goal_list.append(goal)
        allocation.delete()
    downsize.delete()
