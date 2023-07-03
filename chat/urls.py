
from django.urls import path, include
from .views import *

from . import views
app_name = 'chat'

urlpatterns = [
        path('Occupant/<str:pk>/',views.OccupantDetailView,name="Occupant"),
            path('post_confirmation/<str:pk>/' ,views.post_confirmation, name='post_confirmation' ),
    path('add_service_contentieux_dossier/<str:pk>/', views.add_service_contentieux_dossier, name='add_service_contentieux_dossier'),
    path('notifications/', views.notifications, name='notifications'),
    path('accepter/<str:pk>/',views.accepter,name="accepter"),
    path('occupant/<str:pk>/',views.occupant,name="occupant"),
    path('service_contentieux/',views.service_contentieux,name="service_contentieux"),
        path('search_notification/', views.search_notification, name='search_notification'),
        path('OccupantDetailView/<str:pk>/', views.OccupantDetailView, name='OccupantDetailView'),

           path('Occupant_settings/<int:pk>/', views.Occupant_settings, name='Occupant_settings'),


    path('occupant/<int:oc_id>/pdf/', generate_pdf, name='generate_pdf'),
    path('count_dashboard/',views.count_dashboard, name='count_dashboard'),
        path('search_archive/', search_archive, name='search_archive'),
    path('archive_list_by_user/<int:oc_id>/', views.archive_list_by_user, name='archive_list_by_user'),


]