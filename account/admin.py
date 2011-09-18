from django.contrib import admin
from ds.account.models import UserProfile, Preferences, SavingRelationship, CharityRelationship, Trophy

admin.site.register(UserProfile)
admin.site.register(Preferences)
admin.site.register(SavingRelationship)
admin.site.register(CharityRelationship)
admin.site.register(Trophy)
