from django.contrib import admin
from .models import JobApplication, OurTeam, BoardMembers, Notifications

admin.site.register(OurTeam)
admin.site.register(BoardMembers)
admin.site.register(Notifications)
admin.site.register(JobApplication)