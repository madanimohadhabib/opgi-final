"""opgi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from .views import *
from . import views
from django.contrib.auth import views as auth_views
from django.urls import re_path as url
from django.views.static import serve


app_name = 'opgi'

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),

  url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
            path('' ,views.home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),

    path('admin/', admin.site.urls),
        path('service_contentieux/', include('chat.urls')),
        path('accounts/', include('accounts.urls')),
        path('recouvrement/', include('recouvrement.urls')),
    path('search/',include("search.urls")),
   

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()


