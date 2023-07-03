from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from user_agents import parse
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only
from django import template
from accounts.decorators import unauthenticated_user, allowed_users, admin_only
from django.views.decorators.cache import cache_control
from datetime import datetime, timedelta
from django.utils import timezone

register = template.Library()

@register.filter(name='in_group')
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


# Create your views here.
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if Group.objects.filter(user=user, name='service_contentieux').exists():
                return redirect('home')
                
            elif Group.objects.filter(user=user, name='service_recouvrement').exists():
                return redirect('home')
            
            elif Group.objects.filter(user=user, name='admin').exists():
                return redirect('admin:index')  # Redirect to the admin panel's index page
            
            else:
                return HttpResponse("Cannot sanitize form data")

        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'registration/login.html')

def abcd(request):
	            return HttpResponse("Cannot sanitize form data")


#@login_required(login_url='login')
#@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutUser(request):
	logout(request)
	return redirect('accounts:login')



@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def profile(request):
    last_login = request.user.last_login
    user = request.user

    user_agent = request.META.get('HTTP_USER_AGENT')
    user = request.user
    maintenant = timezone.now()

    # Calculate the duration since the last access
    duration = maintenant - last_login

    # Format the duration in a human-readable format
    days = duration.days
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Parse the user agent string to extract device information
    user_agent_info = parse(user_agent)
    device_name = user_agent_info.device.family if user_agent_info.device.family else 'Unknown Device'
    browser_name = user_agent_info.browser.family if user_agent_info.browser.family else 'Unknown Browser'

    return render(request, 'registration/profile.html', {
        'last_login': last_login,
        'device_name': device_name,
        'browser_name': browser_name,
        'duration_days': days,
        'duration_hours': hours,
        'duration_minutes': minutes,
        'duration_seconds': seconds,
        'is_logged_in': user.is_authenticated,
    })
