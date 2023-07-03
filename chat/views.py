from django.shortcuts import render, redirect
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import  PostForm
from accounts.decorators import unauthenticated_user, allowed_users, admin_only
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from .models import Service_contentieux_dossier
# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Service_contentieux_dossier
from .forms import SearchForm
from data.models import  *
from .filters import *
from django.views.decorators.cache import cache_control
from django import template




register = template.Library()

@register.filter(name='in_group')
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()





@cache_control(no_cache=True, must_revalidate=True, no_store=True)

@login_required(login_url='login')
@allowed_users(allowed_roles=['service_contentieux'])
#@require_http_methods(["POST"])
def post_confirmation(request,pk):
      # Check if confirmation has already been successful
    if request.session.get('confirmation_success', False):
        # Redirect the user to the home page
            return redirect('chat:Occupant',pk=pk)

    if request.method == 'POST':
        # Check if the password is correct and confirmation is successful
        # If yes, set confirmation_success to True
        password = request.POST.get('password', '')
        if request.user.check_password(password):
            request.session['confirmation_success'] = True
            # Redirect the user to the home page
            return redirect('chat:Occupant',pk=pk)

    return render(request, 'service_contentieux/confirm_password.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@allowed_users(allowed_roles=['service_contentieux'])
def add_service_contentieux_dossier(request,pk):
    if request.method == 'POST':
        created_by = request.POST['created_by']
        dossier = request.POST['dossier']
        status = request.POST['status']
       
        Service_contentieux_dossier.objects.create(created_by=request.user.username, dossier=pk, status=status)
        
        return render(request, 'occupant.html')   
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@allowed_users(allowed_roles=['service_contentieux'])
def create_dossier(request,pk):
    if request.method == 'POST':
        username = request.POST.get('username')
        dossier = request.POST.get('dossier')
        status = request.POST.get('status')

        if username == request.user.username:
            try:
                Service_contentieux_dossier.objects.create(created_by=username, dossier=pk, status='active')
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
        else:
            return JsonResponse({'success': False, 'message': 'Username does not match'})
    else:
        return render(request, 'occupant.html')


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def notifications(request):
      #sercher par non read
      notifications = Notification.objects.filter(read=False).order_by('-created_at')
      return render(request, 'service_contentieux/notification/notification.html', {'notifications': notifications})

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def accepter (request, pk):
 if   Service_contentieux_dossier.objects.filter(created_by=request.user.username, dossier=pk, status='active').exists() and   Notification.objects.filter(message=pk,read =False).exists():
            return redirect('home')

 elif    Notification.objects.filter(message=pk,read =False).exists():

    if request.method == 'POST':
         if   Service_contentieux_dossier.objects.filter(created_by=request.user.username, dossier=pk, status='terminer').exists() :
                         Service_contentieux_dossier.objects.filter(created_by=request.user.username, dossier=pk).update(status ='active')
                         Notification.objects.filter( message=pk).update(read =True)
                         return redirect('chat:Occupant',pk=pk)


         elif  not Service_contentieux_dossier.objects.filter(created_by=request.user.username, dossier=pk, status='active').exists() : 
     

             Service_contentieux_dossier.objects.create(created_by=request.user.username, dossier=pk, status='active')
             Notification.objects.filter( message=pk).update(read =True)

            
             return redirect('chat:Occupant',pk=pk)

    context = {'item':pk}
    return render(request, 'service_contentieux/accepter.html', context)
 else: 
        return redirect('home')

 

@login_required(login_url='login')
@allowed_users(allowed_roles=['service_contentieux'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def OccupantDetailView (request,pk):

     if  Notification.objects.filter(message=pk).exists():

          dossiers = not Service_contentieux_dossier.objects.filter(dossier=pk,status='terminer')
          notifications = Occupant.objects.get(oc_id=pk)
          occupant = Occupant.objects.get(id=notifications.id) 
          contrats = Contrat.objects.filter(occupant=occupant)
           # dispaly touts les info de Occupant de opgi 
          context = {
                'notifications': notifications,
                'contrats':contrats,
                'dossiers':dossiers,
            }
          return render(request, 'service_contentieux/occupant.html',context)

     else:
        return redirect('home')

@login_required(login_url='login')
@allowed_users(allowed_roles=['service_contentieux'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def occupant (request, pk):
         if not request.session.get('has_occupant', False):
                 return redirect('chat:Occupant',pk=pk)
         return render(request, 'index.html')








@login_required(login_url='login')
@allowed_users(allowed_roles=['service_contentieux'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def service_contentieux(request):
    keyword = request.GET.get('keyword')
    status = request.GET.get('status')

    occupants = Occupant.objects.none()
    dossiers = Service_contentieux_dossier.objects.none()

    if keyword:
        occupants = Occupant.objects.filter(
            Q(nom_oc__icontains=keyword) |
            Q(prenom_oc__icontains=keyword) |
            Q(oc_id__icontains=keyword)
        )
        occupant_ids = [occupant.oc_id for occupant in occupants]

        if status:
            dossiers = Service_contentieux_dossier.objects.filter(
                dossier__in=occupant_ids,
                status=status,created_by=request.user.username
            )
        else:
            dossiers = Service_contentieux_dossier.objects.filter(
                dossier__in=occupant_ids,created_by=request.user.username
            )
    else:
        if status:
            dossiers = Service_contentieux_dossier.objects.filter(
                status=status,created_by=request.user.username
            )
        else:
            dossiers = Service_contentieux_dossier.objects.all()

    myFilter = DataFilter(request.GET, queryset=dossiers)
    dossiers = myFilter.qs

    occupant_names = []
    for dossier in dossiers:
        occupant_names.extend(list(Occupant.objects.filter(oc_id=dossier.dossier).values_list('nom_oc', 'prenom_oc','oc_id')))
    
    context = {
        'occupant_names': occupant_names,
        'dossiers': dossiers,
        'myFilter': myFilter,
    }

    return render(request, 'service_contentieux/service_contentieux.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['service_contentieux'])
def search_notification(request):
    search_notification = None  # Initialize to None

    if 'query' in request.GET:
        query = request.GET['query']
        if query:
             search_notification = Notification.objects.order_by('-created_at').filter(Q(message__icontains=query) | Q(prenom_oc__icontains=query) | Q(nom_oc__icontains=query),read=False)
        else :
                 return redirect('/notifications/')
        
    
    
    context = {
        'search_notification': search_notification,

    }
    return render(request, 'service_contentieux/notification/notification.html', context)

    
#  
@login_required(login_url='login')
@allowed_users(allowed_roles=['service_contentieux'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def Occupant_settings(request,pk):
        

    if Service_contentieux_dossier.objects.filter(created_by=request.user.username, dossier=pk).exists():
        if request.method == 'POST':
           Service_contentieux_dossier_archive.objects.create(created_by=request.user.username, dossier=pk)
           Service_contentieux_dossier.objects.filter(created_by=request.user.username, dossier=pk).delete()
           
           return redirect('home')

         
        context = {'item':pk}

        return render(request, 'service_contentieux/Occupant_settings.html',context)
    else :
        occupant_settings_users = Service_contentieux_dossier.objects.filter(dossier=pk)
        context = {
            'occupant_settings_users': occupant_settings_users,
            'item':pk,
        }
        return render(request, 'service_contentieux/Occupant_settings_user.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['service_contentieux'])
def generate_pdf(request, oc_id):
    occupant = get_object_or_404(Occupant, oc_id=oc_id)
    template_path = 'service_contentieux/pdf_template.html'
    context = {'occupant': occupant}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="occupant_{oc_id}.pdf"'
    # Find the template and render the context
    template = get_template(template_path)
    html = template.render(context)
    # Create the PDF document
    pisa_status = pisa.CreatePDF(html, dest=response)
    # If the document was created successfully, return it
    if pisa_status.err:
        return HttpResponse('An error occurred while creating the PDF')
    return response



def count_dashboard(request):
     
     # Filter instances of Service_contentieux_dossier by created_by
    created_by = request.user.username
    print("created_by",created_by)
    count = Service_contentieux_dossier.objects.filter(created_by=created_by).count()
    context = {
        'count': count
    }
    return render(request, 'service_contentieux/count_dashboard.html',context)

def search_archive(request):
    if request.method == 'GET':
        search_query = request.GET.get('q')  # Obtains the search query value

        if search_query:
            try:
                search_query = int(search_query)  # Try to convert the search query to an integer
                occupants = Occupant.objects.filter(
                    oc_id=search_query
                )
            except ValueError:
                occupants = Occupant.objects.filter(
                    Q(oc_id__icontains=search_query) |
                    Q(nom_oc__icontains=search_query) |
                    Q(prenom_oc__icontains=search_query)
                )

            occupant_ids = [occupant.oc_id for occupant in occupants]

            results = Service_contentieux_dossier_archive.objects.filter(dossier__in=occupant_ids)
            occupants_in_results = occupants.filter(oc_id__in=occupant_ids)

            return render(request, 'service_contentieux/search_archive.html', {'results': results,'occupants': occupants_in_results})

    return render(request, 'service_contentieux/search_archive.html')

def archive_list_by_user(request, oc_id):
    occupant = get_object_or_404(Occupant, oc_id=oc_id)
    results = Service_contentieux_dossier_archive.objects.filter(dossier=occupant.oc_id)
    return render(request, 'service_contentieux/archive_list_by_user.html', {'occupant': occupant, 'results': results})

