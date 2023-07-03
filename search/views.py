from django.shortcuts import redirect, render,get_object_or_404
from django.http import JsonResponse
from data.models import  *
from django.db.models import *
from search.filters import *
from search.utils import *
from django.contrib.auth.decorators import login_required
from accounts.decorators import unauthenticated_user, allowed_users, admin_only
from django.views.decorators.cache import cache_control
from search.models import *

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def recherche(request):
    search_term = request.GET.get('search')
    consultations = Consultation.objects.all()
    consultations = search(consultations,search_term)
    myFilter = DataFilter(request.GET, queryset=consultations)
    consultations  = myFilter.qs


    occupants = Occupant.objects.filter(consultation__in=consultations).distinct()

    latest_consultations = []
    for occupant in occupants:
        consultation = Consultation.objects.filter(occupant=occupant.id).latest('created_at')
        latest_consultations.append(consultation)


    logement = {}
    occupants = None # initialise la variable occupant
    if search_term:

     if not consultations.exists():
        occupants = Occupant.objects.filter(Q(Q(nom_oc__icontains=search_term) | Q(prenom_oc__icontains=search_term)))



        for occupant in occupants:
            contrats = Contrat.objects.filter(occupant=occupant.id)
            for contrat in contrats:
                logement[occupant.id] = Logement.objects.filter(contrat=contrat.id).first()


    context ={
        'service': 'Service Recouvrement',
        'title': "Recherche", 
        'myFilter': myFilter,
        'occupants': occupants,
        'logement': logement,
        'consultations':consultations,
        'latest_consultations':latest_consultations
        }

    return render(request, 'search/search.html', context=context)

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def occupant_detail(request, pk):
    if   Occupant.objects.filter(id=pk).exists():
        occupant = get_object_or_404(Occupant, pk = pk)
        contrats = Contrat.objects.filter(occupant=occupant)
        for contrat in contrats:
            logements= Logement.objects.filter(contrat=contrat)

        montant_dette,mois_diff = calculer_dette(pk)
        montant_dette_plus = abs(montant_dette)
        print("montant_dette_plus",montant_dette_plus)

        if montant_dette <= 0:
            status = 'En règle'
        elif montant_dette >0:
            status = 'En dette'
      

        print("montant_dette",montant_dette)
        print(status)
        if mois_diff <=0:
                mois_diffabs= abs(mois_diff)
                print("mois_diff",mois_diff)
        else :
                mois_diffabs= abs(mois_diff)
                print("mois_diff",mois_diff)
        context = {
        'service': 'Service Recouvrement',
        'title': 'Dashbord',
        'subtitle': "Occupant Detail",
        'contrats': contrats,
        'logements': logements,
        'occupant': occupant,
        'montant_dette':montant_dette,
        'status':status,
        'mois_diffabs':mois_diffabs,
        'montant_dette_plus':montant_dette_plus
        }
        return render(request, "service_recouvrement/occupant_detail.html", context=context)
    
    elif   not  Consultation.objects.filter(pk=pk).exists():
        return redirect('home')
    else : 
        consultation = get_object_or_404(Consultation, pk = pk)
        total_months = Consultation.objects.filter(occupant=consultation.occupant).aggregate(Sum('mois'))['mois__sum'] or 0

        """"
        occupant2 = Occupant.objects.get(id=consultation.occupant.id)

        print("dette:::",occupant2)
        occupant2 = Occupant.objects.get(id=consultation.occupant.id)
        montant_dettes = Dette.objects.filter(occupant=occupant2)


        for dette in montant_dettes:
              montant_dette=dette.montant_dette
             # print("Occupant: ", dette.occupant)
             # print("Montant dette: ", dette.montant_dette)

        """
        mois_entiers = int((consultation.created_at - consultation.logement.contrat.date_strt_loyer).total_seconds() / 2628000) - total_months

        montant_dette,mois_diff = calculer_dette(consultation.occupant.id)
        mois_diff_plus=abs(mois_diff)
        montant_dette_plus = abs(montant_dette)
        print("montant_dette_plus",montant_dette_plus)
        if montant_dette <= 0:
            status = 'En règle'
            
        elif montant_dette >0:
            status = 'En dette'
      

       # print("montant_dettesssss",montant_dette)
        archives = archive_consultations_mois(consultation.occupant.id)

        archivesyears,total_dettes = archive_consultations_annee(consultation.occupant.id)
        
    
    context = {
        'service': 'Service Recouvrement',
        'title': 'Dashbord',
        'subtitle': "Occupant Detail",
        'consultation': consultation,
        'archives': archives,
       'archivesyears': archivesyears,
       'total_dettes': total_dettes,
       'mois_entiers': mois_entiers,
       'total_months': total_months,
              'status': status,
       'montant_dette': montant_dette,
       'montant_dette_plus':montant_dette_plus,
       'mois_diff_plus':mois_diff_plus,

    }

    return render(request, "service_recouvrement/occupant_detail.html", context=context)


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_cites(request):
    unite_id = request.GET.get('unite_id')
    cites = Cite.objects.filter(batiment__Cite__unite_id=unite_id).distinct()

    data = {
        'cites': list(cites.values('id', 'lib_Cite')),
    }

    return JsonResponse(data)

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_batiments(request):
    Cite_id = request.GET.get('Cite_id')
    batiments = Batiment.objects.filter(Cite_id=Cite_id).distinct()
    data = {
         'batiments': list(batiments.values('id', 'lib_Batiment')),
    }
    return JsonResponse(data)