from django.urls import path
from .views import *

# app_name = 'printers'

urlpatterns = [
    # path('', index, name='index'),
    path('', service_object_list_view, name='index'),

    path('test_listview/', Printers_in_serviceModel_ListView.as_view(), name='printers_in_serviceModel_listView'),
    path('test_listview/<int:pk>/', Printers_in_serviceModel_DetailView.as_view(), name='printers_in_serviceModel_detailView'),


    path('printed_pages_on_printers_list', printed_pages_on_printers_list, name='printed_pages_on_printers_list'),



    # Status_printersModel
    path('status_printers_create/', status_printers_create_view, name='status_printers_create'),
    path('status_printers_list/', status_printers_list_view, name='status_printers_list'),
    path('status_printers/<int:id>/', status_printers_detail_view, name='status_printers_detail'),
    path('status_printers_update/<int:id>/', status_printers_update_view, name='status_printers_update'),
    path('status_printers_delete/<int:id>/', status_printers_delete_view, name='status_printers_delete'),

    # Print_serversModel
    path('print_servers_create/', print_servers_create_view, name='print_servers_create'),
    path('print_servers_list/', print_servers_list_view, name='print_servers_list'),
    path('print_servers/<int:id>/', print_servers_detail_view, name='print_servers_detail'),
    path('print_servers_update/<int:id>/', print_servers_update_view, name='print_servers_update'),
    path('print_servers_delete/<int:id>/', print_servers_delete_view, name='print_servers_delete'),

    # CartridgesModel
    path('cartridges_create/', cartridges_create_view, name='cartridges_create'),
    path('cartridges_list/', cartridges_list_view, name='cartridges_list'),
    path('cartridges/<int:id>/', cartridges_detail_view, name='cartridges_detail'),
    path('cartridges_update/<int:id>/', cartridges_update_view, name='cartridges_update'),
    path('cartridges_delete/<int:id>/', cartridges_delete_view, name='cartridges_delete'),

    # PrintersModel
    path('printers_create/', printers_create_view, name='printers_create'),
    path('printers_list/', printers_list_view, name='printers_list'),
    path('printers/<int:id>/', printers_detail_view, name='printers_detail'),
    path('printers_update/<int:id>/', printers_update_view, name='printers_update'),
    path('printers_delete/<int:id>/', printers_delete_view, name='printers_delete'),

    # Type_OIDModel
    path('typeOID_create/', typeOID_create_view, name='typeOID_create'),
    path('typeOID_list/', typeOID_list_view, name='typeOID_list'),
    path('typeOID/<int:id>/', typeOID_detail_view, name='typeOID_detail'),
    path('typeOID_update/<int:id>/', typeOID_update_view, name='typeOID_update'),
    path('typeOID_delete/<int:id>/', typeOID_delete_view, name='typeOID_delete'),

    # SNMP_OIDModel
    path('SNMP_OID_create/', SNMP_OID_create_view, name='SNMP_OID_create'),
    path('SNMP_OID_list/', SNMP_OID_list_view, name='SNMP_OID_list'),
    path('SNMP_OID/<int:id>/', SNMP_OID_detail_view, name='SNMP_OID_detail'),
    path('SNMP_OID_update/<int:id>/', SNMP_OID_update_view, name='SNMP_OID_update'),
    path('SNMP_OID_delete/<int:id>/', SNMP_OID_delete_view, name='SNMP_OID_delete'),

    # Printers_in_serviceModel
    path('printers_in_service_create/', printers_in_service_create_view, name='printers_in_service_create'),
    path('printers_in_service_list/', printers_in_service_list_view, name='printers_in_service_list'),

    path('printers_in_service_list_filter/', printers_in_service_list_view_filter, name='printers_in_service_list_filter'),

    path('printers_in_service_list_archived/', printers_in_service_list_view_archived, name='printers_in_service_list_archived'),
    path('printers_in_service/<int:id>/', printers_in_service_detail_view, name='printers_in_service_detail'),
    path('printers_in_service_update/<int:id>/', printers_in_service_update_view, name='printers_in_service_update'),
    path('printers_in_service_delete/<int:id>/', printers_in_service_delete_view, name='printers_in_service_delete'),



    # path('printers_in_service_export_xls/<int:id>/', printers_in_service_export_xls, name='printers_in_service_export_xls'),



    # Service_objectModel
    path('service_object_create/', service_object_create_view, name='service_object_create'),
    path('service_object_list/', service_object_list_view, name='service_object_list'),

    path('service_object_list_view_bb/', service_object_list_view_bb, name='service_object_list_view_bb'),
    path('service_object_list_view_bmk/', service_object_list_view_bmk, name='service_object_list_view_bmk'),

    path('service_object/<int:id>/', service_object_detail_view, name='service_object_detail'),
    path('service_object_update/<int:id>/', service_object_update_view, name='service_object_update'),
    path('service_object_delete/<int:id>/', service_object_delete_view, name='service_object_delete'),
    path('service_object_export_printed_pages_xls/<int:id>/', service_object_export_printed_pages_xls, name='service_object_export_printed_pages_xls'),
    path('service_object_printed_pages_list_view/<int:id>/', service_object_printed_pages_list_view, name='service_object_printed_pages_list_view'),

    # Асинхронный метод сбора данных по принтерам по id площадки (объекта обслуживания)
    path('async_service_object_printed_pages_list_view/<int:id>/', async_service_object_printed_pages_list_view, name='async_service_object_printed_pages_list_view'),



    path('async_service_object_printed_pages_list_view_all/', async_service_object_printed_pages_list_view_all, name='async_service_object_printed_pages_list_view_all'),
    path('printed_pages_list_view_all_last/', printed_pages_list_view_all_last, name='printed_pages_list_view_all_last'),



    path('service_object_printed_pages_all_list_view/', service_object_printed_pages_all_list_view, name='service_object_printed_pages_all_list_view'),

    path('service_object_printed_pages_bb_list_view/', service_object_printed_pages_bb_list_view, name='service_object_printed_pages_bb_list_view'),
    path('service_object_printed_pages_bmk_list_view/', service_object_printed_pages_bmk_list_view, name='service_object_printed_pages_bmk_list_view'),

    path('service_object_all_export_printed_pages_xls/', service_object_all_export_printed_pages_xls, name='service_object_all_export_printed_pages_xls'),

    path('service_object_all_export_printed_pages_xls_bb/', service_object_all_export_printed_pages_xls_bb, name='service_object_all_export_printed_pages_xls_bb'),
    path('service_object_all_export_printed_pages_xls_bmk/', service_object_all_export_printed_pages_xls_bmk, name='service_object_all_export_printed_pages_xls_bmk'),


    # Printed_pagesModel
    # path('service_object_create/', service_object_create_view, name='service_object_create'),
    path('printed_pages_list/', printed_pages_list_view, name='printed_pages_list'),


    # export_csv
    # path('export_csv/', export_csv, name='export_csv'),


    # export_xls
    path('export_users_xls/', export_printed_pages_xls, name='export_users_xls'),


]