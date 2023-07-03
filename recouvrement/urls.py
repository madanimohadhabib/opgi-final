from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import UniteAutocomplete

app_name = 'recouvrement'

urlpatterns = [
    # ... other URL patterns ...
    path('login/', auth_views.LoginView.as_view(), name='login'),

        path('notifications/', views.notifications, name='notifications'),
                path('recouvrement/', views.recouvrement, name='recouvrement'),
    path('accepter/<int:pk>/', views.accepter, name='accepter'),
    path('unite/<int:pk>/pdf/', views.generate_pdf, name='generate_pdf'),

####
####
   path('montant_mensuel/', views.montant_mensuel, name='montant_mensuel'),

    path('montant_mensuel_updates/<str:unit>/', views.montant_mensuel_updates, name='montant_mensuel_updates'),
    path('montant_mensuel_updates_anne/<str:unit>/<int:anne>/', views.montant_mensuel_updates_anne, name='montant_mensuel_updates_anne'),
    path('chart_view/', views.chart_view, name='chart_view'),
    path('unite-autocomplete/', UniteAutocomplete.as_view(), name='unite-autocomplete'),
    path('MontantMensuel_views/', views.MontantMensuel_views, name='MontantMensuel_views'),
   path('display_unites/', views.display_unites, name='display_unites'),

   path('montant_mensuel/<str:unit>/', views.montant_mensuel_chart, name='montant_mensuel_chart'),#### Madani
    path('montant_mensuel_chart_par_anne/<str:unit>/<int:anne>/', views.montant_mensuel_chart_par_anne, name='montant_mensuel_chart_par_anne'),#### Madani

 path('consultations_views/', views.chart_view_consultations_par_unit, name='consultations_views'),#### Madani
   path('montant_mensuel/<str:unit>/', views.montant_mensuel_chart, name='montant_mensuel_chart'),#### Madani
       path('montant_mensuel_chart_par_anne/<str:unit>/<int:anne>/', views.montant_mensuel_chart_par_anne, name='montant_mensuel_chart_par_anne'),#### Madani

]