from django.forms import ModelForm
from .models import *

class StatusPrintersForm(ModelForm):
    class Meta:
        model = StatusPrintersModel
        fields = ('status',)


class Print_serversForm(ModelForm):
    class Meta:
        model = Print_serversModel
        fields = ('print_server',)


class CartridgesForm(ModelForm):
    class Meta:
        model = CartridgesModel
        fields = ('name',) 


class PrintersForm(ModelForm):
    class Meta:
        model = PrintersModel
        fields = ('name', 'cartridges', 'sn_oid', 'printed_pages_all_oid',)


class Type_OIDForm(ModelForm):
    class Meta:
        model = Type_OIDModel
        fields = ('type',)
     
        
class SNMP_OIDForm(ModelForm):
    class Meta:
        model = SNMP_OIDModel
        fields = ('type_OID', 'oid')


class Printers_in_serviceForm(ModelForm):
    class Meta:
        model = Printers_in_serviceModel
        fields = ('service_object', 'serial_number', 'printers', 'status_printer', 'print_server', 'name_on_print_server', \
                  'ip_address', 'location', 'archived',)


class Printers_in_service_commentsForm(ModelForm):
    class Meta:
        model = Printers_in_service_commentsModel
        fields = ('printers_in_service', 'short_description', 'comment',)


class Service_objectForm(ModelForm):
    class Meta:
        model = Service_objectModel
        fields = ('service_object_name',)


class Printed_pagesForm(ModelForm):
    class Meta:
        model = Printed_pagesModel
        fields = ('printers_in_service','printed_pages')