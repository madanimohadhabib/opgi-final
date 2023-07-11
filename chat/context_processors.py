from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
from .models import *

def notification_count(request):
    channel_layer = get_channel_layer()
    notifications = Notification.objects.filter(read=False).order_by('-created_at')
    count = notifications.count()
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {"type": "send_notification", "count": count},
    )
    return dict(notification_count=count)



def my_view_1(request):
    now = datetime.now()

    instances = []

    # Iterate over all Contrat objects
    for contrat in Contrat.objects.all():
        # Calculate the number of months since date_strt_loyer for this Contrat
        if contrat.date_strt_loyer is not None:
            months = (now.year - contrat.date_strt_loyer.year) * 12 + (now.month - contrat.date_strt_loyer.month)
        else:
            months = 0

        # Calculate the total difference between the number of months and the mois field for all associated Consultation objects
        consultation_months_sum = 0

        px = 0
        for consultation in Consultation.objects.filter(occupant=contrat.occupant):
            consultation_months_sum += consultation.mois
        px = (months - consultation_months_sum) * contrat.total_of_month > contrat.total_of_month
        if px:
            print("px is True", (months - consultation_months_sum) * contrat.total_of_month)
            # Display the occupant name if px is True
            print("Occupant name:", contrat.occupant.nom_oc)
            print("Number of months since date_strt_loyer:", months)
            print("Total difference between months and mois for associated Consultation objects:", consultation_months_sum)
            instances.append((contrat.occupant.nom_oc, contrat.occupant.id))  # Append as a tuple

        else:
            print("px is False", (months - consultation_months_sum) * contrat.total_of_month)
            print("Number of months since date_strt_loyer:", months)
            print("Total difference between months and mois for associated Consultation objects:", consultation_months_sum)

    context = {
        'instances': instances
    }
    return context



def my_view_1_Fidele(request):
    now = datetime.now()

    instances_Fidele = []

    # Iterate over all Contrat objects
    for contrat in Contrat.objects.all():
        # Calculate the number of months since date_strt_loyer for this Contrat
        if contrat.date_strt_loyer is not None:
            months = (now.year - contrat.date_strt_loyer.year) * 12 + (now.month - contrat.date_strt_loyer.month)
        else:
            months = 0

        # Calculate the total difference between the number of months and the mois field for all associated Consultation objects
        consultation_months_sum = 0

        px = 0
        for consultation in Consultation.objects.filter(occupant=contrat.occupant):
            consultation_months_sum += consultation.mois
        px = (months - consultation_months_sum) * contrat.total_of_month < contrat.total_of_month
        if px:
            print("px is True", (months - consultation_months_sum) * contrat.total_of_month)
            # Display the occupant name if px is True
            print("Occupant name:", contrat.occupant.nom_oc)
            print("Number of months since date_strt_loyer:", months)
            print("Total difference between months and mois for associated Consultation objects:", consultation_months_sum)
            instances_Fidele.append((contrat.occupant.nom_oc, contrat.occupant.id))  # Append as a tuple

        else:
            print("px is False", (months - consultation_months_sum) * contrat.total_of_month)
            print("Number of months since date_strt_loyer:", months)
            print("Total difference between months and mois for associated Consultation objects:", consultation_months_sum)

    context = {
        'instances_Fidele': instances_Fidele
    }
    return context