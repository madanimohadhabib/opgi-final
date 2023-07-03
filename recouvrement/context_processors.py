from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification_chef_service
import datetime
from .models import MontantMensuel
from django.db.models import F, Sum
from data.models import Consultation,Unite
from django.db.models import F, Sum
from django.db.models import Count
import datetime
from django.db.models.functions import TruncDate
def notification_count_recouvrement(request):
    notifications = Notification_chef_service.objects.filter(read=False).order_by('-created_at')
    count = notifications.count()
    
    return dict(notification_count_recouvrement=count)

def montant_context_processor(request):
    now = datetime.datetime.now()
    mois_actuel = now.month
    annee_actuelle = now.year

    # Get the montants queryset
    montants = MontantMensuel.objects.filter(mois=mois_actuel, annee=annee_actuelle)

    # Calculate the total_of_month_for_all_unit and total using aggregate method
    all_totals = montants.aggregate(total_of_month=Sum('total_of_month'), total=Sum('total'))

    # Calculate the percentage for each montant
    for montant in montants:
        montant.percentage = round((montant.total_of_month / montant.total) * 100, 2)

    # Create a dictionary with the desired context data
    context = {
        'montants': montants,
    }

    # Return the context dictionary
    return context


def chart_view(request):
    lib_unit = request.GET.get('lib_unit')
    mois = request.GET.get('mois')
    annee = request.GET.get('annee')

    chart_data = MontantMensuel.objects.all()

    if lib_unit:
        chart_data = chart_data.filter(unite__lib_unit=lib_unit)
    if mois:
        chart_data = chart_data.filter(mois=mois)
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
    return context

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
    return context