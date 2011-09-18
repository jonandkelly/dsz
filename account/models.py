from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from ds.charities.models import Charity
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

USER = 100
SUPER_USER = 200

class Trophy(models.Model):
    award = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True, blank=True)
    image = models.URLField("Trophy", null=True, blank=True)
    def __unicode__(self):
        return self.award

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    ds_points = models.IntegerField(verbose_name="DS Points", default=0)
    baller_status = models.CharField(max_length=10, verbose_name="Baller Status", default='User')
    trophy_case = models.ManyToManyField(Trophy, verbose_name="Trophy Case", default=None)
    charities = models.ManyToManyField(Charity, through='CharityRelationship', verbose_name="Favorite Charities", default=None)
    #facebook additions from Django-facebook
    about_me = models.TextField(blank=True, null=True)
    facebook_id = models.IntegerField(blank=True, null=True)
    facebook_name = models.CharField(max_length=255, blank=True, null=True)
    facebook_profile_url = models.TextField(blank=True, null=True)
    website_url = models.TextField(blank=True, null=True)
    blog_url = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='profile_images')
    date_of_birth = models.DateField(blank=True, null=True)
    raw_data = models.TextField(blank=True, null=True)
    def __unicode__(self):
        return self.user.username
        
    def post_facebook_registration(self, request):
        '''
        Behaviour after registering with facebook
        '''
        from django_facebook.utils import next_redirect
        default_url = reverse('facebook_connect')
        response = next_redirect(request, default=default_url, next_key='register_next')
        response.set_cookie('fresh_registration', self.user_id)
        return response
    
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        UserProfile.objects.create(user=kwargs.get('instance'))

post_save.connect(ensure_profile_exists, sender=User)

class SavingRelationship(models.Model):
    userprofile = models.ForeignKey(UserProfile)
    saving = models.ForeignKey('goals.Saving')
    saving_points = models.IntegerField(verbose_name="Saving Points", default=0)
    def __unicode__(self):
        return self.saving.saving_type
    class Meta:
        ordering = ['saving']

class CharityRelationship(models.Model):
    userprofile = models.ForeignKey(UserProfile)
    charity = models.ForeignKey(Charity)
    charity_points = models.IntegerField(verbose_name="Charity Points", default=0)
    favorite = models.BooleanField()
    queued = models.BooleanField()
    donated = models.BooleanField()
    def __unicode__(self):
        return self.charity.charity_name
    class Meta:
        ordering = ['charity']

class Preferences(models.Model):
    user = models.OneToOneField(User)
    CHECKIN_FREQUENCY_CHOICES = (
        (u'daily', u'Daily'),
        (u'weekly', u'Weekly'),
    )
    checkin_frequency = models.CharField(max_length=6, choices=CHECKIN_FREQUENCY_CHOICES, verbose_name="Check In Frequency", default='daily')
    facebook = models.BooleanField(default=True)
    twitter = models.BooleanField(default=True)
    downsize = models.BooleanField(default=True)
    new_goal = models.BooleanField(verbose_name="New Goal", default=True)
    goal_achieved = models.BooleanField(verbose_name="Goal Achieved", default=True)
    saving_summary = models.BooleanField(verbose_name="Monthly Savings Summary", default=True)
    on_spot_downsize = models.BooleanField(verbose_name="On-the-Spot Downsizes", default=True)
    PRIVACY_WHO_CHOICES = (
        (u'friends', u'Friends'),
        (u'friendsfriends', u'Friends of Friends'),
        (u'alldownsize', u'All of Downsize'),
    )
    privacy_who = models.CharField(max_length=14, choices=PRIVACY_WHO_CHOICES, default='alldownsize')
    full_profile = models.BooleanField(verbose_name="Full Profile", default=True)
    commitments = models.BooleanField(default=True)
    goals = models.BooleanField(default=True)
    badges = models.BooleanField(default=True)
    total_points = models.BooleanField(verbose_name="Total DS Points", default=True)
    def __unicode_(self):
        return self.user.username


def ensure_preferences_exists(sender, **kwargs):
    if kwargs.get('created', False):
        preferences = Preferences.objects.create(user=kwargs.get('instance'))

post_save.connect(ensure_preferences_exists, sender=User)
