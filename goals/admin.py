from django.contrib import admin
from ds.goals.models import Saving, Goal, Downsize, Allocation

admin.site.register(Saving)
admin.site.register(Goal)
admin.site.register(Downsize)
admin.site.register(Allocation)
