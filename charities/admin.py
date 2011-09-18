from django.contrib import admin
from ds.charities.models import Charity, Cause, CauseCategory

admin.site.register(Charity)
admin.site.register(Cause)
admin.site.register(CauseCategory)
