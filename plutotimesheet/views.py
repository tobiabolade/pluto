from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import UserForm, WeekForm, TimesheetForm
from django.shortcuts import render, get_object_or_404
from .models import Week, Timesheet


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'plutotimesheet/login.html')
    else:
        form = WeekForm(request.POST or None)
        week = Week.objects.filter(user=request.user)
        if form.is_valid():
            weeks = form.save(commit=False)
            weeks.user = request.user
            week_start = form.cleaned_data['week_start']
            week_end = form.cleaned_data['week_end']
            weeks.save()
            return render(request, 'plutotimesheet/detail.html', {'weeks': weeks})
        else:
            context = {'form': form,
                       }
            return render(request, 'plutotimesheet/index.html', context)


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                if request.user.is_superuser:
                    return render(request, 'plutotimesheet/adminpage.html')
                else:
                    return render(request, 'plutotimesheet/index.html')
            else:
                return render(request, 'plutotimesheet/login.html', {'error_message': "You are blocked"})
        else:
            return render(request, 'plutotimesheet/login.html', {'error_message': "Invalid details, please try again"})
    return render(request, 'plutotimesheet/login.html')


def logout(request):
    auth_logout(request)
    form = UserForm(request.POST or None)
    context = {'form': form, }
    return render(request, 'plutotimesheet/login.html', context)


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return render(request, 'plutotimesheet/index.html')
    context = {
        'form': form,
    }
    return render(request, 'plutotimesheet/register.html', context)


def about(request):
    return render(request, 'plutotimesheet/about.html')


def timesheet(request, week_id):
    form = TimesheetForm(request.POST or None)
    week = get_object_or_404(Week, pk=week_id)
    if form.is_valid():
        timesheets = form.save(commit=False)
        day = form.cleaned_data['day']
        shift = form.cleaned_data['shift']
        client = form.cleaned_data['client']
        address = form.cleaned_data['address']
        start = form.cleaned_data['start']
        finish = form.cleaned_data['finish']
        timesheets.save()
        return render(request, 'plutotimesheet/detail.html', {'week', week})
    context = {'form': form,
               'week': week,
               }
    return render(request, 'plutotimesheet/timesheet.html', context)


def admin_check(request):
    if not request.user.is_superuser:
        return render(request, 'plutotimesheet  /login.html')
    else:
        week = Week.objects.all()
        times = Timesheet.objects.all()
        context = {'week': week,
                   'times': times,
                   }
        return render(request, 'plutotimesheet/adminpage.html', context)


def detail(request, week_id):
    if not request.user.is_authenticated:
        return render(request, 'plutotimesheet/login.html')
    else:
        user = request.user
        week = get_object_or_404(Week, pk=week_id)
        weeks = Week.objects.filter(user=request.user)
        context = {'week': week,
                   'weeks': weeks,
                   }
        return render(request, 'plutotimesheet/detail.html', context)
