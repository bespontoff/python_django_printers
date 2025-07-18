import django_filters
from .models import *
# from decimal import Decimal
# from django.db.models import Q
# from django.forms import TextInput

class Printers_in_serviceModel_Filter(django_filters.FilterSet):
    serial_number = django_filters.CharFilter(lookup_expr='icontains')
    name_on_print_server = django_filters.CharFilter(lookup_expr='icontains')
    ip_address = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')


    class Meta:
        model = Printers_in_serviceModel
        fields = ['service_object', 'serial_number', 'printers', 'status_printer', 'print_server',
                'name_on_print_server', 'ip_address', 'location', ]