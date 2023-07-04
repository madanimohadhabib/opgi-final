from django.contrib.auth.models import User,Group


def nombre_utilisateurs(request):
    nombre_utilisateurs = User.objects.count()
    nombre_groups = Group.objects.count()
    
    context = {
        'nombre_utilisateurs':nombre_utilisateurs,
        'nombre_groups':nombre_groups,
    }
    
    
    return context