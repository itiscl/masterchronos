from django.contrib import admin
from .models import Employee, ActivityType, TimeSheet, TimeSheetEntry


admin.site.register(Employee)
admin.site.register(ActivityType)
admin.site.register(TimeSheet)
admin.site.register(TimeSheetEntry)
