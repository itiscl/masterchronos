import calendar
import datetime

from django.shortcuts import render
from django.db.models.aggregates import Sum
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Employee, TimeSheet, ActivityType
from .forms import TimeSheetEntryAddForm, TimeSheetStatusChangeForm


def employees(request):
    employee_list = Employee.objects.all()

    return render(
        request,
        'employees.html',
        context={
            'employee_list': employee_list,
        }
    )


def timesheets(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)

    if not employee:
        raise Http404()

    timesheet_list = employee.timesheet_set.all()
    
    return render(
        request,
        'timesheets.html',
        context={
            'employee': employee,
            'timesheet_list': timesheet_list
        }
    )


def timesheets_add(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)

    if not employee:
        raise Http404()

    if employee.timesheet_set.count() > 0:
        latest_time_sheet = employee.timesheet_set.latest("month")
        latest_month = latest_time_sheet.month
        number_of_days_in_month = calendar.monthrange(latest_month.year, latest_month.month)[1]
        last_day_of_month = datetime.date(latest_month.year, latest_month.month, number_of_days_in_month)
        next_month = last_day_of_month + datetime.timedelta(days=1)
    else:
        next_month = datetime.date.today()
        
    time_sheet = employee.timesheet_set.create(month=next_month)
    time_sheet.save()

    url = reverse("timesheets", args=[employee.id])
    return HttpResponseRedirect(url)


def timesheet_detail(request, timesheet_id):
    timesheet = TimeSheet.objects.get(pk=timesheet_id)

    if not timesheet:
        raise Http404()

    year = timesheet.month.year
    month = timesheet.month.month
    month_last_day = calendar.monthrange(year, month)[1]

    month_date_list = [datetime.date(year, month, number + 1) for number in range(month_last_day)]
    timesheet_entries_list_by_day = []

    for day in month_date_list:
        day_entries_list = timesheet.timesheetentry_set.filter(date=day)
        day_total = int(day_entries_list.aggregate(total=Sum("quantity"))["total"] or 0)
        dic = {"day": day, "total": day_total, "entries": day_entries_list}
        timesheet_entries_list_by_day.append(dic)

    activity_type_list = ActivityType.objects.all()

    form = TimeSheetEntryAddForm()
    form.fields["date"].widget.attrs["min"] = datetime.date(year, month, 1).isoformat()
    form.fields["date"].widget.attrs["max"] = datetime.date(year, month, month_last_day).isoformat()
    
    form_status = TimeSheetStatusChangeForm()

    return render(
        request=request,
        template_name='timesheet.html',
        context={
            'timesheet': timesheet,
            'timesheet_entries_list_by_day': timesheet_entries_list_by_day,
            'activity_type_list': activity_type_list,
            'form': form,
            'form_status': form_status
        }
    )


def timesheet_entry_add(request, timesheet_id):
    timesheet = TimeSheet.objects.get(pk=timesheet_id)

    if not timesheet:
        raise Http404()

    form = TimeSheetEntryAddForm(request.POST)
    if form.is_valid():
        form_date = form.cleaned_data["date"]
        form_activity = form.cleaned_data["activity"]
        form_quantity = form.cleaned_data["quantity"]
        entry = timesheet.timesheetentry_set.create(date=form_date, activity=form_activity, quantity=form_quantity)
        entry.save()

    url = reverse("timesheet", args=[timesheet.id])
    return HttpResponseRedirect(url)
    
def timesheet_status_change(request, timesheet_id):
    timesheet = TimeSheet.objects.get(pk=timesheet_id)
    
    if not timesheet:
        raise Http404()

    form = TimeSheetStatusChangeForm(request.POST)
    if form.is_valid():
        timesheet.status = form.cleaned_data["status"]
        timesheet.save()
    
    url = reverse("timesheet", args=[timesheet.id])
    return HttpResponseRedirect(url)    
