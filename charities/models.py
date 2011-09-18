from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from ds.settings import MEDIA_URL
from random import shuffle

class Cause(models.Model):
    cause = models.CharField("Cause", max_length=50)
    class Meta:
        ordering = ["cause"]
    def __unicode__(self):
        return self.cause

class CauseCategory(models.Model):
    cause_category = models.CharField("Category", max_length=20)
    slug = models.SlugField()
    cause_category_image = models.URLField("cause_category_image", null=True, blank=True)
    class Meta:
        ordering = ['cause_category']        
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.cause_category)
        super(CauseCategory, self).save(*args, **kwargs)
    def __unicode__(self):
        return self.cause_category

class Charity(models.Model):
    cause_categories = models.ManyToManyField(CauseCategory)
    causes = models.ManyToManyField(Cause, null=True, blank=True)
    charity_name = models.CharField("Charity Name", max_length=20)
    city = models.CharField("City", max_length=25)
    state = models.CharField("State", max_length=2)
    zip = models.CharField("Zip Code", max_length=5)
    spotlight = models.BooleanField("Spotlight", default=False)
    impact = models.CharField("Impact", max_length=50, null=True, blank=True)
    highlighted = models.CharField("Highlighted", max_length=150, null=True, blank=True)
    perks = models.CharField("Perk", max_length=50, null=True, blank=True)
    ds_verified = models.BooleanField("DS-Verified")
    website = models.URLField("Website", null=True, blank=True)
    logo = models.URLField("Logo", null=True, blank=True)
    image1 = models.URLField("Image 1", null=True, blank=True)
    points_raised = models.DecimalField("Points Raised", max_digits=20, decimal_places=2, default=0)
    num_users_donated = models.IntegerField("Users Donated", default=0)
    class Meta:
        ordering = ['charity_name']
    def __unicode__(self):
        return self.charity_name

def RandomizeSpotlightCharities():
    spotlight_charity_list = list(Charity.objects.filter(spotlight=True))
    shuffle(spotlight_charity_list)
    return spotlight_charity_list
