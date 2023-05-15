from django.urls import path
from . import views

urlpatterns = [
    path('', views.employees, name='employees'),
    path('timesheets/<int:employee_id>', views.timesheets, name='timesheets'),
    path('timesheets/<int:employee_id>/add', views.timesheets_add, name='timesheets_add'),
    path('timesheet/<int:timesheet_id>', views.timesheet_detail, name='timesheet'),
    path('timesheet/<int:timesheet_id>/add', views.timesheet_entry_add, name='timesheet_entry_add'),
    path('timesheet/<int:timesheet_id>/status', views.timesheet_status_change, name='timesheet_status_change')
]
