
import django_filters as filters
from .models import Service_contentieux_dossier

class DataFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=Service_contentieux_dossier.STATUS_CHOICES)

    class Meta:
        model = Service_contentieux_dossier
        fields = ['status']
