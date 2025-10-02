from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet
from .models import *
from .admin_mixins import ExportAsCSVMixin


@admin.register(StatusPrintersModel)
class StatusPrintersAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        'export_csv',
    ]

    list_display = ('id', 'status',)
    list_display_links = ('status',)
    list_filter = ['status',]
    search_fields = ('id', 'status',)
    ordering = ('status',)


@admin.register(Print_serversModel)
class Print_serversAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        'export_csv',
    ]

    list_display = ('id', 'print_server',)
    list_display_links = ('print_server',)
    list_filter = ['print_server',]
    search_fields = ('id', 'print_server',)
    ordering = ('print_server',)


@admin.register(CartridgesModel)
class CartridgesAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        'export_csv',
    ]

    list_display = ('id', 'name',)
    list_display_links = ('name',)
    list_filter = ['name',]
    search_fields = ('id', 'name',)
    ordering = ('name',)


@admin.register(PrintersModel)
class PrintersAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        'export_csv',
    ]

    model = CartridgesModel
    filter_horizontal = ('cartridges',)
    list_display = ('id', 'name', '_cartridges', 'sn_oid', 'printed_pages_all_oid',)
    list_display_links = ('name',)
    list_filter = ['name', 'cartridges', 'printed_pages_all_oid',]
    search_fields = ('id', 'name', 'cartridges__name', 'sn_oid__oid', 'printed_pages_all_oid__oid',)
    ordering = ('name',)

    def _cartridges(self, row):
        return ', '.join([x.name for x in row.cartridges.all()])

    def queryset(self, request):
        return PrintersModel.objects.select_related("Cartridges")


@admin.register(Type_OIDModel)
class Type_OIDAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        'export_csv',
    ]

    list_display = ('id', 'type',)
    list_display_links = ('type',)
    list_filter = ['type',]
    search_fields = ('id', 'type',)
    ordering = ('type',)


@admin.register(SNMP_OIDModel)
class SNMP_OIDAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        'export_csv',
    ]

    list_display = ('id', 'type_OID','oid', )
    list_display_links = ('type_OID',)
    list_filter = ['type_OID__type','oid',]
    search_fields = ('id', 'oid', 'type_OID__type',)
    ordering = ('type_OID__type', 'oid',)



# ---------------------------------------------------------------
# Printers_in_service

@admin.action(description='Архивировать записи')
def printers_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)

@admin.action(description='Вернуть записи из архива')
def printers_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)

class Printers_in_service_commentsInline(admin.TabularInline):   # добавляем в Printers_in_serviceAdmin поля из Printers_in_service_comments
    model = Printers_in_service_commentsModel
    readonly_fields = ('id', 'created', 'updated')
    extra = 1 # Это определяет, сколько еще форм, в дополнение к начальным формам, отображается в наборе форм. по умолчанию до 3
    # # fk_name = 'printers_comments'

@admin.register(Printers_in_serviceModel)
class Printers_in_serviceAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        printers_archived,
        printers_unarchived,
        'export_csv',

    ]
    inlines = [Printers_in_service_commentsInline,]   # добавляем в Printers_in_serviceAdmin поля из Printers_in_service_comments

    list_display = ('id', 'service_object', 'serial_number', 'printers', 'status_printer', 'print_server', 'name_on_print_server',
                    'ip_address', 'location', 'created', 'updated', 'archived',)
    list_display_links = ('serial_number', 'printers')
    list_filter = ['service_object', 'print_server__print_server', 'status_printer__status', 'location', 'printers__name',]
    # filters = ['service_object', 'print_server__print_server', 'status_printer__status', 'location', 'printers__name',]
    search_fields = ('serial_number', 'service_object', 'printers__name', 'status_printer__status', 'print_server__print_server', 'name_on_print_server',
                     'ip_address', 'location', 'updated',)
    ordering = ('service_object', 'status_printer__status', 'print_server__print_server', 'location', 'name_on_print_server',)

    def queryset(self, request):
        return Printers_in_serviceModel.objects.select_related('PrintersModel', 'Status_printersModel', 'Print_serversModel').prefetch_related('Printers_in_service_commentsModel')


    # # группировка полей в админке
    # fieldsets = [
    #     ('Namesection1', {"fields":('serial_number', 'printers',)}),
    #     ('Namesection2',
    #         {"fields": ('status_printer', 'print_server', 'name_on_print_server', 'ip_address', 'location',),
    #          'classes': ('wide', 'collapse',),}),  # параметр 'collapse' позволяет скрывать секцию, 'wide' - смещение полей
    #     ('Extra options', {
    #         "fields": ('archived',),
    #         'classes': ('collapse',),
    #         'description': 'Extra options. Field "archived" is for soft delete',
    #     }),
    # ]


    # '_short_comments'

    # def _cartridges(self, row):
    #     return ', '.join([x.name for x in row.cartridges.all()])

    # def _short_comments(self, obj:Printers_in_service_comments) -> str:
    #     if len(obj.printers_comments) < 55:
    #         return obj.printers_comments
    #     return obj.printers_comments[:55] + "..."



@admin.register(Printers_in_service_commentsModel)
class Printers_in_service_commentsAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        'export_csv',
    ]

    list_display = ('printers_in_service', 'short_description', '_short_comment', 'created', 'updated',)
    list_display_links = ('printers_in_service', 'short_description',)
    search_fields = ('printers_in_service__printers__name', 'short_description', 'comment', 'created', 'updated',)
    ordering = ('-created',)

    def _short_comment(self, obj:Printers_in_service_commentsModel) -> str:
        if len(obj.comment) < 15:
            return obj.comment
        return obj.comment[:15] + "..."


@admin.register(Service_objectModel)
class Service_objectAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        'export_csv',
    ]

    list_display = ('id', 'service_object_name', )
    list_display_links = ('service_object_name',)
    list_filter = ['service_object_name',]
    search_fields = ('service_object_name',)
    ordering = ('service_object_name',)


@admin.register(Printed_pagesModel)
class Printed_pagesAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        'export_csv',
    ]
    list_display = ('id', 'printers_in_service', 'service_object_name', 'printers_name',
                    'serial_number', 'ip_address', 'name_on_print_server', 'location', 'created', 'printed_pages', 'error_message', )
    list_display_links = ('printers_in_service',)
    search_fields = ('printers_in_service', 'service_object_name', 'printers_name',
                     'serial_number', 'ip_address', 'name_on_print_server', 'location', 'created', 'printed_pages', 'error_message', )
    ordering = ('created',)
