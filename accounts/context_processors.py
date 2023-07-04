from django.contrib.auth.models import User


def nombre_utilisateurs(request):
    nombre_utilisateurs = User.objects.count()
    
    context = {
        'nombre_utilisateurs':nombre_utilisateurs,
    }
    
    return context