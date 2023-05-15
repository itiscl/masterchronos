from django import forms
from .models import ActivityType, TimeSheet


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeSheetEntryAddForm(forms.Form):
    date = forms.DateField(
        label="Дата",
        widget=DateInput(
            attrs={
                "class": "form-control",
            },
        )
    )

    activity = forms.ModelChoiceField(
        queryset=ActivityType.objects.all(),
        label='Вид деятельности',
    )

    quantity = forms.IntegerField(
        label="Количество",
        min_value=1,
        max_value=24
    )
    
class TimeSheetStatusChangeForm(forms.Form):
	status = forms.ChoiceField(
	    label = "Статус",
	    choices = TimeSheet.STATUS_CHOICES
	)
