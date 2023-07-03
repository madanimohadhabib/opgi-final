from datetime import date, timedelta
from django.db.models import Q
from collections import defaultdict
from data.models import *
from .filters import *
from datetime import datetime

def calculer_dette(occupant):
    now = datetime.now()

    consultation_months_sum = 0

    for consultation in Consultation.objects.filter(occupant=occupant):
        consultation_months_sum += consultation.mois
        print("consultation_months_sum",consultation_months_sum)
    contrat_values = Contrat.objects.get(id=occupant)
    diff = (now.year - contrat_values.date_strt_loyer.year) * 12 + (now.month - contrat_values.date_strt_loyer.month)
    mois_diff= (diff - consultation_months_sum)
    
    print("mois_diff",mois_diff)
    montant_dette = contrat_values.total_of_month * mois_diff

    
    print("montant_dette :::::::",montant_dette)
    return montant_dette,mois_diff


def search(queryset, search_term=None):
    """
    Recherche les consultations avec le terme de recherche donné.
    """
    if search_term:
        query = Q(Q(occupant__nom_oc__icontains=search_term) | Q(occupant__prenom_oc__icontains=search_term) | Q(occupant__oc_id__icontains=search_term))
        queryset = queryset.filter(query)
    return queryset


def archive_consultations_mois(occupant):
    consultations = Consultation.objects.filter(occupant=occupant).order_by('-created_at')
    archives = []
    latest_consultation = None

    for consultation in consultations:
        if latest_consultation is None or consultation.created_at > latest_consultation.created_at:
            latest_consultation = consultation

            date_debut_loyer = latest_consultation.logement.contrat.date_strt_loyer.date()
            date_fin_archive = date.today()
            date_archive = date_debut_loyer
            fixed_amount = latest_consultation.logement.contrat.total_of_month

            while date_archive < date_fin_archive:
                num_months = (date_debut_loyer.year - date_archive.year) * 12 + (date_debut_loyer.month - date_archive.month)
                montant_dette = abs(fixed_amount * num_months)

                archive = {
                    'logement': latest_consultation.logement,
                    'occupant': latest_consultation.occupant,
                    'unite': latest_consultation.unite,
                    'montant_dette': montant_dette,
                    'mois_entiers' : date_archive,
                    'created_at': date_fin_archive,
                }
                archives.append(archive)
                date_archive = date_archive + timedelta(days=30)

    return archives


def archive_consultations_annee(occupant):
    consultations = Consultation.objects.filter(occupant=occupant).order_by('created_at')
    archives = []
    last_consultations = {}
    total_dettes = 0

    for consultation in consultations:
        occupant_id = consultation.occupant.id

        if occupant_id in last_consultations and consultation.id != last_consultations[occupant_id]:
            continue

        last_consultations[occupant_id] = consultation.id

        logement = consultation.logement
        start_date = logement.contrat.date_strt_loyer.date()
        end_date = consultation.created_at.date()
        debt_per_year = defaultdict(int)
        fixed_amount = logement.contrat.total_of_month

        for year in range(start_date.year, end_date.year + 1):
            if year == start_date.year:
                start_month = start_date.month
            else:
                start_month = 0
            if year == end_date.year:
                end_month = end_date.month
            else:
                end_month = 12
            num_months = (end_month - start_month )
            debt_per_year[year] += fixed_amount * num_months

        for year, amount in debt_per_year.items():
            archive = {
                'logement': logement,
                'occupant': consultation.occupant,
                'unite': consultation.unite,
                'montant_dette': amount,
                'year' : year,
            }
            archives.append(archive)
            total_dettes += amount

    return archives, total_dettes
