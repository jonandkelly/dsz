from django.db import models
from django.contrib.auth.models import Group, User

class Network(models.Model):
    network = models.OneToOneField(Group)
    network_name = models.CharField("Network Name", max_length=25)
    member = models.ManyToManyField(User)

