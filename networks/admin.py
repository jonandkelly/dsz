from django.contrib import admin
from ds.networks.models import Friends, FriendsOfFriends, CampaignGroup

admin.site.register(Friends)
admin.site.register(FriendsOfFriends)
admin.site.register(CampaignGroup)
