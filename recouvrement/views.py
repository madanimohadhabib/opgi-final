from django.shortcuts import render, redirect
from .models import *
from django import template
from django.contrib.auth.models import Group
from accounts.decorators import unauthenticated_user, allowed_users, admin_only
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from .models import *
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from .models import MontantMensuel
from dal import autocomplete
from data.models import *
from django.db.models.functions import TruncDate
from django.db.models import Count

import datetime

from django.db.models import F, Sum
from django.db.models import Sum
register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

@login_required(login_url='login')
@allowed_users(allowed_roles=['service_recouvrement'])

def notifications(request):
        notifications = Notification_chef_service.objects.filter(read=False).order_by('-created_at')

        return render(request, 'recouvrement/notifications.html', {'notifications': notifications})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)

@login_required(login_url='login')
@allowed_users(allowed_roles=['service_recouvrement'])

def recouvrement(request):
            notifications_alert = Notification_chef_service.objects.filter(read=True).order_by('-created_at')

            return render(request, 'recouvrement/recouvrement.html', {'notifications_alert': notifications_alert})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)

@login_required(login_url='login')
@allowed_users(allowed_roles=['service_recouvrement'])

def accepter(request, pk):
        if  not  Notification_chef_service.objects.filter(id=pk).exists():
                                            return redirect('home')

        elif    Notification_chef_service.objects.filter(id=pk,read =False).exists():
            if request.method == 'POST':
                    Notification_chef_service.objects.filter( id=pk).update(read =True)
                    return redirect('recouvrement:recouvrement')

            
            context = {'item':pk}
            return render(request, 'recouvrement/accepter.html', context)
        elif  Notification_chef_service.objects.filter(id=pk,read =True).exists():
                                    return redirect('home')

             

@cache_control(no_cache=True, must_revalidate=True, no_store=True)

@login_required(login_url='login')
@allowed_users(allowed_roles=['service_recouvrement'])
def generate_pdf(request, pk):
 if  not  Notification_chef_service.objects.filter(id=pk).exists():
                                            return redirect('home')
 elif  Notification_chef_service.objects.filter(id=pk,read =True).exists():
    unite = get_object_or_404(Notification_chef_service, id=pk)
    template_path = 'recouvrement/pdf_template.html'
    context = {'unite': unite}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="unite_{id}.pdf"'
    # Find the template and render the context
    template = get_template(template_path)
    html = template.render(context)
    # Create the PDF document
    pisa_status = pisa.CreatePDF(html, dest=response)
    # If the document was created successfully, return it
    if pisa_status.err:
        return HttpResponse('An error occurred while creating the PDF')
    return response
 




 #
 ####

 ####


 ##
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

@login_required(login_url='login')
@allowed_users(allowed_roles=['service_recouvrement'])
def montant_mensuel(request):
    now = datetime.datetime.now()
    mois_actuel = now.month
    annee_actuelle = now.year
    
    # Get the montants queryset
    montants = MontantMensuel.objects.filter(mois=mois_actuel, annee=annee_actuelle)

    # Calculate the total_of_month_for_all_unit and total using aggregate method
    all_totals = montants.aggregate(total_of_month=Sum('total_of_month'), total=Sum('total'))
     # Get all units with their corresponding years
    

    # Calculate the percentage for each montant
    for montant in montants:
        montant.percentage = round((montant.total_of_month / montant.total) * 100, 2)

    # Pass the montants queryset and all_totals dictionary to the template
    context = {
        'montants': montants,
        'all_totals': all_totals,
    }

    

    return render(request, 'recouvrement/montant_mensuel.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)

@login_required(login_url='login')
@allowed_users(allowed_roles=['service_recouvrement'])
def montant_mensuel_updates(request, unit):

 if    Unite.objects.filter(lib_unit=unit).exists():

    now = datetime.datetime.now()
    mois_actuel = now.month
    annee_actuelle = now.year
    montants = MontantMensuel.objects.filter(unite__lib_unit=unit, mois=mois_actuel, annee=annee_actuelle)
    
    # Get the list of distinct years for the given unit
    years = MontantMensuel.objects.filter(unite__lib_unit=unit).values_list('annee', flat=True).distinct()

    for montant in montants:
        montant.percentage = round((montant.total_of_month / montant.total) * 100, 2)

    context = {"montants": montants, "unit": unit, "years": years}
    return render(request, 'recouvrement/test.html', context)
 else :
                                                     return redirect('home')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)

@login_required(login_url='login')
@allowed_users(allowed_roles=['service_recouvrement'])
def montant_mensuel_updates_anne(request, unit, anne):
 
 if    Unite.objects.filter(lib_unit=unit).exists() and MontantMensuel.objects.filter(annee=anne).exists() :

    # Get the distinct months for the given year and unit
    mois = MontantMensuel.objects.filter(unite__lib_unit=unit, annee=anne).order_by('mois').values_list('mois', flat=True).distinct()

    # Get the montants for the given year, unit, and months
    montants = MontantMensuel.objects.filter(unite__lib_unit=unit, annee=anne, mois__in=mois).order_by('mois')
    total_all_months = montants.aggregate(total=Sum('total_of_month'))['total']

    for montant in montants:
        montant.percentage = round((montant.total_of_month / montant.total) * 100, 2)

    context = {
        "data_montant_mensuel": montants,
        "unit": unit,
        "anne": anne,
                "total_all_months": total_all_months,

    }
    return render(request, 'recouvrement/test_anne.html', context)
 else :
                                                     return redirect('home')

#

@cache_control(no_cache=True, must_revalidate=True, no_store=True)

@login_required(login_url='login')
@allowed_users(allowed_roles=['service_recouvrement'])
def chart_view(request):
    lib_unit = request.GET.get('lib_unit')
    mois = request.GET.get('mois')
    annee = request.GET.get('annee')

    chart_data = MontantMensuel.objects.all()

    if lib_unit:
        chart_data = chart_data.filter(unite__lib_unit=lib_unit)
    if mois:
        try:
            mois = int(mois)
            if 1 <= mois <= 12:
                chart_data = chart_data.filter(mois=mois)
        except ValueError:
            pass
    if annee:
        try:
            annee = int(annee)
            chart_data = chart_data.filter(annee=annee)
        except ValueError:
            pass
    chart_data = chart_data.values('unite__lib_unit', 'total', 'total_of_month').order_by('unite__lib_unit')

    chart_labels = [data['unite__lib_unit'] for data in chart_data]
    chart_values_total = [data['total'] for data in chart_data]
    chart_values_total_of_month = [data['total_of_month'] for data in chart_data]

    lib_unit_values = MontantMensuel.objects.values_list('unite__lib_unit', flat=True).distinct()

    context = {
        'chart_labels': chart_labels,
        'chart_values_total': chart_values_total,
        'chart_values_total_of_month': chart_values_total_of_month,
        'selected_lib_unit': lib_unit,
        'selected_mois': mois,
        'selected_annee': annee,
        'lib_unit_values': lib_unit_values,
    }

    return render(request, 'recouvrement/montantMensuel_views.html', context)


class UniteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Unite.objects.all()

        if self.q:
            qs = qs.filter(lib_unit__icontains=self.q)

        return qs


@login_required(login_url='login')
@allowed_users(allowed_roles=['service_recouvrement'])
def MontantMensuel_views(request):
            return render(request, 'recouvrement/montantMensuel_views.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['service_recouvrement'])
def display_unites(request):
    query = request.GET.get('query', '')
    unites = Unite.objects.filter(lib_unit__icontains=query)
    context = {'unites': unites, 'query': query}
    return render(request, 'recouvrement/display_unites.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['service_recouvrement'])
def montant_mensuel_chart(request, unit):
    if Unite.objects.filter(lib_unit=unit).exists():
        now = datetime.datetime.now()
        mois_actuel = now.month
        annee_actuelle = now.year
        montants = MontantMensuel.objects.filter(unite__lib_unit=unit, mois=mois_actuel, annee=annee_actuelle)

        # Get the list of distinct years for the given unit
        years = MontantMensuel.objects.filter(unite__lib_unit=unit).values_list('annee', flat=True).distinct()

        for montant in montants:
            montant.percentage = round((montant.total_of_month / montant.total) * 100, 2)

        # Prepare the data for the chart
        chart_labels = [f"{montant.mois}/{montant.annee}" for montant in montants]
        chart_data_total = [montant.total for montant in montants]
        chart_data_total_of_month = [montant.total_of_month for montant in montants]

        context = {
            "montants": montants,
            "unit": unit,
            "years": years,
            "chart_labels": chart_labels,
            "chart_data_total": chart_data_total,
            "chart_data_total_of_month": chart_data_total_of_month,
        }
        return render(request, 'recouvrement/montant_mensuel_chart.html', context)
    else:
        return redirect('home')
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['service_recouvrement'])
def montant_mensuel_chart_par_anne(request, unit, anne):
 
    if Unite.objects.filter(lib_unit=unit).exists() and MontantMensuel.objects.filter(annee=anne).exists() :

        # Get the distinct months for the given year and unit
        mois = MontantMensuel.objects.filter(unite__lib_unit=unit, annee=anne).order_by('mois').values_list('mois', flat=True).distinct()

        # Get the montants for the given year, unit, and months
        montants = MontantMensuel.objects.filter(unite__lib_unit=unit, annee=anne, mois__in=mois).order_by('mois')
        total_all_months = montants.aggregate(total=Sum('total_of_month'))['total']

        for montant in montants:
            montant.percentage = round((montant.total_of_month / montant.total) * 100, 2)
        
        # Prepare the data for the chart
        chart_labels = [f"{montant.mois}/{montant.annee}" for montant in montants]
        chart_data_total = [montant.total for montant in montants]
        chart_data_total_of_month = [montant.total_of_month for montant in montants]

        context = {
            "data_montant_mensuel": montants,
            "unit": unit,
            "anne": anne,
            "total_all_months": total_all_months,
            "chart_labels": chart_labels,
            "chart_data_total": chart_data_total,
            "chart_data_total_of_month": chart_data_total_of_month,

        }
        return render(request, 'recouvrement/montant_mensuel_chart_par_annee.html', context)
    else :
        return redirect('home')
    

@login_required(login_url='login')
@allowed_users(allowed_roles=['service_recouvrement'])
def chart_view_consultations_par_unit(request):

    consultation_data = Consultation.objects.annotate(date=TruncDate('created_at'))

   

    consultation_data = consultation_data.values('unite__lib_unit').annotate(consultation_count=Count('id')).order_by('unite__lib_unit')


    total_consultations = 0

    for data in consultation_data:

        total_consultations += data['consultation_count']

    lib_unit_values = [data['unite__lib_unit'] for data in consultation_data]

    context = {
        
        'total_consultations': total_consultations,
    }

    return render(request, 'recouvrement/consultations_views.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['service_recouvrement'])
def montant_mensuel_chart(request, unit):
    if Unite.objects.filter(lib_unit=unit).exists():
        now = datetime.datetime.now()
        mois_actuel = now.month
        annee_actuelle = now.year
        montants = MontantMensuel.objects.filter(unite__lib_unit=unit, mois=mois_actuel, annee=annee_actuelle)

        # Get the list of distinct years for the given unit
        years = MontantMensuel.objects.filter(unite__lib_unit=unit).values_list('annee', flat=True).distinct()

        for montant in montants:
            montant.percentage = round((montant.total_of_month / montant.total) * 100, 2)

        # Prepare the data for the chart
        chart_labels = [f"{montant.mois}/{montant.annee}" for montant in montants]
        chart_data_total = [montant.total for montant in montants]
        chart_data_total_of_month = [montant.total_of_month for montant in montants]

        context = {
            "montants": montants,
            "unit": unit,
            "years": years,
            "chart_labels": chart_labels,
            "chart_data_total": chart_data_total,
            "chart_data_total_of_month": chart_data_total_of_month,
        }
        return render(request, 'recouvrement/montant_mensuel_chart.html', context)
    else:
        return redirect('home')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)

@login_required(login_url='login')
@allowed_users(allowed_roles=['service_recouvrement'])
def montant_mensuel_chart_par_anne(request, unit, anne):
 
    if Unite.objects.filter(lib_unit=unit).exists() and MontantMensuel.objects.filter(annee=anne).exists() :

        # Get the distinct months for the given year and unit
        mois = MontantMensuel.objects.filter(unite__lib_unit=unit, annee=anne).order_by('mois').values_list('mois', flat=True).distinct()

        # Get the montants for the given year, unit, and months
        montants = MontantMensuel.objects.filter(unite__lib_unit=unit, annee=anne, mois__in=mois).order_by('mois')
        total_all_months = montants.aggregate(total=Sum('total_of_month'))['total']

        for montant in montants:
            montant.percentage = round((montant.total_of_month / montant.total) * 100, 2)
        
        # Prepare the data for the chart
        chart_labels = [f"{montant.mois}/{montant.annee}" for montant in montants]
        chart_data_total = [montant.total for montant in montants]
        chart_data_total_of_month = [montant.total_of_month for montant in montants]

        context = {
            "data_montant_mensuel": montants,
            "unit": unit,
            "anne": anne,
            "total_all_months": total_all_months,
            "chart_labels": chart_labels,
            "chart_data_total": chart_data_total,
            "chart_data_total_of_month": chart_data_total_of_month,

        }
        return render(request, 'recouvrement/montant_mensuel_chart_par_annee.html', context)
    else :
        return redirect('home')
    


    ###########
    #####
    ##################