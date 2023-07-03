

from django.shortcuts import render, redirect
from accounts.decorators import unauthenticated_user, allowed_users, admin_only
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.views import LoginView

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def home(request):
    return render(request, 'index.html')


class CustomLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redirect authenticated users to a different page
            return redirect('home')  # Replace 'dashboard' with your desired URL name

        return super().get(request, *args, **kwargs)