from django import forms
from django.contrib.auth.models import User

from .models import Week, Timesheet


class DateInput(forms.DateInput):
    input_type = 'date'


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class WeekForm(forms.ModelForm):
    class Meta:
        widgets = {'week_start': DateInput(), 'week_end': DateInput()}
        model = Week
        fields = ['week_start', 'week_end']


class TimesheetForm(forms.ModelForm):
    class Meta:
        widgets = {'finish': DateTimeInput()}
        model = Timesheet
        fields = ['day', 'shift', 'client', 'address', 'start', 'finish']





