# Create your views here.

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required


@login_required
def volunteer(request):
    if request.method == 'POST':
        group = Group.objects.get(name='volunteers')
        user = User.objects.get(username=request.user)
        user.groups.add(group)
        messages.success(request, 'We have added you to the volunteers group')

    groups = list(request.user.groups.all().values_list('name', flat=True))

    return render(request, 'app/volunteer.html', {
        'user_is_volunteer': 'volunteers' in groups
    })

@login_required
def withdraw(request):
    if request.method == 'POST':
        group = Group.objects.get(name='volunteers')
        user = User.objects.get(username=request.user)
        user.groups.remove(group)
        messages.success(request, 'We have removed you from the volunteers group')

    return redirect('volunteer')
