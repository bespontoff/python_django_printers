from django.shortcuts import render, redirect, get_object_or_404
# from django.views.generic.detail import DetailView
# from django.views.generic.edit import UpdateView
from django.views.generic import ListView, DetailView
from django.http import Http404, HttpResponse
from .models import *
from .forms import *
import datetime
import codecs
import csv

from django.contrib.auth.models import User
import xlwt

from .filters import *

from easysnmp import snmp_get
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page

import django_tables2
from django_tables2 import SingleTableView
from django_tables2 import RequestConfig

import asyncio

"""
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def snmp_get(oid="oid", hostname="ip", community='public', version=1):

    return "000"
"""



# ***********************************************************************************************************************************************************
# Распечатано страниц (принтеры/МФУ)

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def get_data_by_oid(ip, oid):
    try:
        response = snmp_get(oid, hostname=ip, community='public', version=1)
        return response.value

    except Exception as ex:
        return ""

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
async def async_get_data_by_oid(ip, oid):
    try:
        response = snmp_get(oid, hostname=ip, community='public', version=1)
        return "" + ip + "_" +  oid + "_" + response.value

    except Exception as ex:
        return ""

# # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# async def create_massive_by_oid(dataset_printers_in_service):

#     tasks = []

#     for data_printers_in_service in dataset_printers_in_service:

#         # print("" + data_printers_in_service.ip_address)

#         # return "" + ip + "_" +  oid + "_" + response.value
#         tasks.append(asyncio.create_task(async_get_data_by_oid(data_printers_in_service.ip_address, data_printers_in_service.printers.sn_oid.oid)))
#         tasks.append(asyncio.create_task(async_get_data_by_oid(data_printers_in_service.ip_address, data_printers_in_service.printers.printed_pages_all_oid.oid)))

#     results = await asyncio.gather(*tasks)

#     return results



# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def printed_pages_on_printers_list(request):
# def printed_pages_on_printers_list(request, service_object_id):
    # Получаем все неархивные записи из Printers_in_serviceModel с учетом объекта обслуживания
    # dataset_printers_in_service = Printers_in_serviceModel.objects.filter(archived=False).filter(service_object_id=service_object_id)
    dataset_printers_in_service = Printers_in_serviceModel.objects.filter(archived=False)



    # results_data = asyncio.run(create_massive_by_oid(dataset_printers_in_service))

    # dict_async_get_data_by_oid = {}
    # for result in results_data:
    #     # return "" + ip + "_" +  oid + "_" + response.value
    #     tmp_massive = result.split("_")
    #     dict_async_get_data_by_oid[tmp_massive[0] + "_" + tmp_massive[1]] = tmp_massive[2]



    dataset = []
    for data_printers_in_service in dataset_printers_in_service:

        dataset.append(
            [
                data_printers_in_service.ip_address,
                data_printers_in_service.printers,
                data_printers_in_service.status_printer,
                data_printers_in_service.name_on_print_server,
                data_printers_in_service.location,
                get_data_by_oid(data_printers_in_service.ip_address, data_printers_in_service.printers.sn_oid.oid),
                get_data_by_oid(data_printers_in_service.ip_address, data_printers_in_service.printers.printed_pages_all_oid.oid),
                # dict_async_get_data_by_oid.get(data_printers_in_service.ip_address + "_" + data_printers_in_service.printers.sn_oid.oid),
                # dict_async_get_data_by_oid.get(data_printers_in_service.ip_address + "_" + data_printers_in_service.printers.printed_pages_all_oid.oid),
            ]
                    )

    # dataset_thead = ['ip','sn','oid_printed_pages_all','Действия над записями',]
    dataset_thead = ['IP-адрес', 'Модель принтера', 'Статус', 'Имя на Print-server', 'Локация/Кабинет', 'S/N','Распечатано страниц (всего)',]

    context={
        'title_text':'Распечатано страниц (ББ)',
        'url_return_to_the_list':'printed_pages_on_printers_list',
        'dataset':dataset,
        'dataset_thead': dataset_thead
        }


    return render(
        request,
        'printers/select_data.html',
        context,
    )


# ***********************************************************************************************************************************************************
# Index

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def index(request):
    # Получаем все записи

    title_text = "Формирование реестров о количестве распечатанных страниц (принтеры/МФУ)"
    return render(request, 'printers/index.html', {'title_text':title_text})



class Printers_in_serviceModel_ListView(ListView):
    model = Printers_in_serviceModel
    context_object_name = 'printers_in_service'
    template_name = "printers_in_servicemodel_list.html"


class Printers_in_serviceModel_DetailView(DetailView):
    model = Printers_in_serviceModel
    context_object_name = 'data'
    # template_name = "printers_in_servicemodel_detail.html"









# ***********************************************************************************************************************************************************
# StatusPrintersModel / Статусы принтеров

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def status_printers_create_view(request):
    title_text = "Статусы принтеров (добавление записи)"
    # Проверяем, что запрос на добавление записи (POST) или просто на получение формы
    if request.method == 'POST':
        # Получаем из запроса только те данные которые использует форма
        form = StatusPrintersForm(request.POST)
        # Проверяем правильность введенных данных
        if form.is_valid():
            # сохраняем в базу
            form.save()
            # переадресуем на главную страницу
            return redirect('status_printers_list')
    else:
        form =StatusPrintersForm()
    context = {
            'form': form,
            'title_text':title_text,
            'url_return_to_the_list':'status_printers_list',
        }
        # return render(request, 'printers/status_printers_create.html', context)
    return render(request, 'printers/create.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def status_printers_list_view(request):
    form = StatusPrintersForm()
    # Получаем все записи
    dataset = StatusPrintersModel.objects.all()
    title_text = "Статусы принтеров (список записей)"
    return render(request, 'printers/status_printers_listview.html', {'form': form, 'dataset': dataset, 'title_text':title_text})


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def status_printers_detail_view(request, id):
    try:
        # Получаем запись по-определенному id
        data = StatusPrintersModel.objects.get(id=id)
        title_text = "Статус принтера"
    except StatusPrintersModel.DoesNotExist:
        raise Http404('Такой записи не существует')
    return render(request, 'printers/status_printers_detailview.html', {'data': data, 'title_text': title_text})


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def status_printers_update_view(request, id):
    try:
        old_data = get_object_or_404(StatusPrintersModel, id=id)
        title_text = "Статусы принтеров (обновление записи)"
    except Exception:
        raise Http404('Такой записи не существует')

    # Если метод POST, то это обновленные данные
    # Остальные методы - возврат данных для изменения
    if request.method =='POST':
        form = StatusPrintersForm(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect(f'/printers/status_printers/{id}')
    else:
        form = StatusPrintersForm(instance = old_data)
    context ={
            'form':form,
            'title_text':title_text,
            'url_return_to_the_list':'status_printers_list',
        }
    return render(request, 'printers/update.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def status_printers_delete_view(request, id):
    try:
        data = get_object_or_404(StatusPrintersModel, id=id)
        title_text = "Статусы принтеров (удаление записи)"
    except Exception:
        raise Http404('Такой записи не существует')

    if request.method == 'POST':
        data.delete()
        return redirect('status_printers_list')
    else:
        return render(request, 'printers/delete.html', {'title_text':title_text,'url_return_to_the_list':'status_printers_list',})


# ***********************************************************************************************************************************************************
# Print_serversModel / Print-servers

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def print_servers_create_view(request):
    title_text = "Print-servers (добавление записи)"
    # Проверяем, что запрос на добавление записи (POST) или просто на получение формы
    if request.method == 'POST':
        # Получаем из запроса только те данные которые использует форма
        form = Print_serversForm(request.POST)
        # Проверяем правильность введенных данных
        if form.is_valid():
            # сохраняем в базу
            form.save()
            # переадресуем на главную страницу
            return redirect('print_servers_list')
    else:
        form =Print_serversForm()
    context = {
            'form': form,
            'title_text':title_text,
            'url_return_to_the_list':'print_servers_list',
        }
        # return render(request, 'printers/print_servers_create.html', context)
    return render(request, 'printers/create.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def print_servers_list_view(request):
    form = Print_serversForm()
    # Получаем все записи
    dataset = Print_serversModel.objects.all()
    title_text = "Print-servers (список записей)"
    return render(request, 'printers/print_servers_listview.html', {'form': form, 'dataset': dataset, 'title_text':title_text})


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def print_servers_detail_view(request, id):
    try:
        # Получаем запись по-определенному id
        data = Print_serversModel.objects.get(id=id)
        title_text = "Print-server"
    except Print_serversModel.DoesNotExist:
        raise Http404('Такой записи не существует')
    return render(request, 'printers/print_servers_detailview.html', {'data': data, 'title_text': title_text})


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def print_servers_update_view(request, id):
    try:
        old_data = get_object_or_404(Print_serversModel, id=id)
        title_text = "Print-servers (обновление записи)"
    except Exception:
        raise Http404('Такой записи не существует')

    # Если метод POST, то это обновленные данные
    # Остальные методы - возврат данных для изменения
    if request.method =='POST':
        form = Print_serversForm(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect(f'/printers/print_servers/{id}')
    else:
        form = Print_serversForm(instance = old_data)
    context ={
            'form':form,
            'title_text':title_text,
            'url_return_to_the_list':'print_servers_list',
        }
    return render(request, 'printers/update.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def print_servers_delete_view(request, id):
    try:
        data = get_object_or_404(Print_serversModel, id=id)
        title_text = "Print-servers (удаление записи)"
    except Exception:
        raise Http404('Такой записи не существует')

    if request.method == 'POST':
        data.delete()
        return redirect('print_servers_list')
    else:
        return render(request, 'printers/delete.html', {'title_text':title_text,'url_return_to_the_list':'print_servers_list',})


# ***********************************************************************************************************************************************************
# CartridgesModel

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def cartridges_create_view(request):
    title_text = "Модели картриджей (добавление записи)"
    # Проверяем, что запрос на добавление записи (POST) или просто на получение формы
    if request.method == 'POST':
        # Получаем из запроса только те данные которые использует форма
        form = CartridgesForm(request.POST)
        # Проверяем правильность введенных данных
        if form.is_valid():
            # сохраняем в базу
            form.save()
            # переадресуем на главную страницу
            return redirect('cartridges_list')
    else:
        form =CartridgesForm()
    context = {
            'form': form,
            'title_text':title_text,
            'url_return_to_the_list':'cartridges_list',
        }
    return render(request, 'printers/create.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def cartridges_list_view(request):
    form = CartridgesForm()
    # Получаем все записи
    dataset = CartridgesModel.objects.all()
    title_text = "Модели картриджей (список записей)"
    return render(request, 'printers/cartridges_listview.html', {'form': form, 'dataset': dataset, 'title_text':title_text})


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def cartridges_detail_view(request, id):
    try:
        # Получаем запись по-определенному id
        data = CartridgesModel.objects.get(id=id)
        title_text = "Модель картриджа"
    except CartridgesModel.DoesNotExist:
        raise Http404('Такой записи не существует')
    context ={
            'data': data,
            'title_text': title_text,
            'url_return_to_the_list':'cartridges_list',
        }
    return render(request, 'printers/cartridges_detailview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def cartridges_update_view(request, id):
    try:
        old_data = get_object_or_404(CartridgesModel, id=id)
        title_text = "Модели картриджей (обновление записи)"
    except Exception:
        raise Http404('Такой записи не существует')

    # Если метод POST, то это обновленные данные
    # Остальные методы - возврат данных для изменения
    if request.method =='POST':
        form = CartridgesForm(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect(f'/printers/cartridges/{id}')
    else:
        form = CartridgesForm(instance = old_data)
    context ={
            'form':form,
            'title_text':title_text,
            'url_return_to_the_list':'cartridges_list',
        }
    return render(request, 'printers/update.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def cartridges_delete_view(request, id):
    try:
        data = get_object_or_404(CartridgesModel, id=id)
        title_text = "Модели картриджей (удаление записи)"
    except Exception:
        raise Http404('Такой записи не существует')

    if request.method == 'POST':
        data.delete()
        return redirect('cartridges_list')
    else:
        return render(request, 'printers/delete.html', {'title_text':title_text,'url_return_to_the_list':'cartridges_list',})


# ***********************************************************************************************************************************************************
# PrintersModel

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def printers_create_view(request):
    title_text = "Модели принтеров (добавление записи)"
    # Проверяем, что запрос на добавление записи (POST) или просто на получение формы
    if request.method == 'POST':
        # Получаем из запроса только те данные которые использует форма
        form = PrintersForm(request.POST)
        # Проверяем правильность введенных данных
        if form.is_valid():
            # сохраняем в базу
            form.save()
            # переадресуем на главную страницу
            return redirect('printers_list')
    else:
        form =PrintersForm()
    context = {
            'form': form,
            'title_text':title_text,
            'url_return_to_the_list':'printers_list',
        }
    return render(request, 'printers/create.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def printers_list_view(request):
    form = PrintersForm()
    # Получаем все записи
    dataset = PrintersModel.objects.all()
    title_text = "Модели принтеров (список записей)"
    return render(request, 'printers/printers_listview.html', {'form': form, 'dataset': dataset, 'title_text':title_text})


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def printers_detail_view(request, id):
    try:
        # Получаем запись по-определенному id
        data = PrintersModel.objects.get(id=id)
        title_text = "Модель принтера"
    except PrintersModel.DoesNotExist:
        raise Http404('Такой записи не существует')
    context ={
            'data': data,
            'title_text': title_text,
            'url_return_to_the_list':'printers_list',
        }
    return render(request, 'printers/printers_detailview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def printers_update_view(request, id):
    try:
        old_data = get_object_or_404(PrintersModel, id=id)
        title_text = "Модели принтеров (обновление записи)"
    except Exception:
        raise Http404('Такой записи не существует')

    # Если метод POST, то это обновленные данные
    # Остальные методы - возврат данных для изменения
    if request.method =='POST':
        form = PrintersForm(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect(f'/printers/printers/{id}')
    else:
        form = PrintersForm(instance = old_data)
    context ={
            'form':form,
            'title_text':title_text,
            'url_return_to_the_list':'printers_list',
        }
    return render(request, 'printers/update.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def printers_delete_view(request, id):
    try:
        data = get_object_or_404(PrintersModel, id=id)
        title_text = "Модели принтеров (удаление записи)"
    except Exception:
        raise Http404('Такой записи не существует')

    if request.method == 'POST':
        data.delete()
        return redirect('printers_list')
    else:
        return render(request, 'printers/delete.html', {'title_text':title_text,'url_return_to_the_list':'printers_list',})


# ***********************************************************************************************************************************************************
# Type_OIDModel

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def typeOID_create_view(request):
    title_text = "Type_OID"
    # Проверяем, что запрос на добавление записи (POST) или просто на получение формы
    if request.method == 'POST':
        # Получаем из запроса только те данные которые использует форма
        form = Type_OIDForm(request.POST)
        # Проверяем правильность введенных данных
        if form.is_valid():
            # сохраняем в базу
            form.save()
            # переадресуем на главную страницу
            return redirect('typeOID_list')
    else:
        form =Type_OIDForm()
    context = {
            'form': form,
            'title_text':title_text,
            'url_return_to_the_list':'typeOID_list',
        }
    return render(request, 'printers/create.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def typeOID_list_view(request):
    form = Type_OIDForm()
    # Получаем все записи
    dataset = Type_OIDModel.objects.all()
    title_text = "Type_OID"
    return render(request, 'printers/typeOID_listview.html', {'form': form, 'dataset': dataset, 'title_text':title_text})


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def typeOID_detail_view(request, id):
    try:
        # Получаем запись по-определенному id
        data = Type_OIDModel.objects.get(id=id)
        title_text = "Type_OID"
    except Type_OIDModel.DoesNotExist:
        raise Http404('Такой записи не существует')
    context ={
            'data': data,
            'title_text': title_text,
            'url_return_to_the_list':'typeOID_list',
        }
    return render(request, 'printers/typeOID_detailview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def typeOID_update_view(request, id):
    try:
        old_data = get_object_or_404(Type_OIDModel, id=id)
        title_text = "Type_OID"
    except Exception:
        raise Http404('Такой записи не существует')

    # Если метод POST, то это обновленные данные
    # Остальные методы - возврат данных для изменения
    if request.method =='POST':
        form = Type_OIDForm(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect(f'/printers/typeOID/{id}')
    else:
        form = Type_OIDForm(instance = old_data)
    context ={
            'form':form,
            'title_text':title_text,
            'url_return_to_the_list':'typeOID_list',
        }
    return render(request, 'printers/update.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def typeOID_delete_view(request, id):
    try:
        data = get_object_or_404(Type_OIDModel, id=id)
        title_text = "Type_OID"
    except Exception:
        raise Http404('Такой записи не существует')

    if request.method == 'POST':
        data.delete()
        return redirect('typeOID_list')
    else:
        return render(request, 'printers/delete.html', {'title_text':title_text,'url_return_to_the_list':'typeOID_list',})


# ***********************************************************************************************************************************************************
# SNMP_OIDModel

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def SNMP_OID_create_view(request):
    title_text = "SNMP_OID"
    # Проверяем, что запрос на добавление записи (POST) или просто на получение формы
    if request.method == 'POST':
        # Получаем из запроса только те данные которые использует форма
        form = SNMP_OIDForm(request.POST)
        # Проверяем правильность введенных данных
        if form.is_valid():
            # сохраняем в базу
            form.save()
            # переадресуем на главную страницу
            return redirect('SNMP_OID_list')
    else:
        form =SNMP_OIDForm()
    context = {
            'form': form,
            'title_text':title_text,
            'url_return_to_the_list':'SNMP_OID_list',
        }
    return render(request, 'printers/create.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def SNMP_OID_list_view(request):
    form = SNMP_OIDForm()
    # Получаем все записи
    dataset = SNMP_OIDModel.objects.all()
    title_text = "SNMP_OID"
    return render(request, 'printers/SNMP_OID_listview.html', {'form': form, 'dataset': dataset, 'title_text':title_text})


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def SNMP_OID_detail_view(request, id):
    try:
        # Получаем запись по-определенному id
        data = SNMP_OIDModel.objects.get(id=id)
        title_text = "SNMP_OID"
    except SNMP_OIDModel.DoesNotExist:
        raise Http404('Такой записи не существует')
    context ={
            'data': data,
            'title_text': title_text,
            'url_return_to_the_list':'SNMP_OID_list',
        }
    return render(request, 'printers/SNMP_OID_detailview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def SNMP_OID_update_view(request, id):
    try:
        old_data = get_object_or_404(SNMP_OIDModel, id=id)
        title_text = "SNMP_OID"
    except Exception:
        raise Http404('Такой записи не существует')

    # Если метод POST, то это обновленные данные
    # Остальные методы - возврат данных для изменения
    if request.method =='POST':
        form = SNMP_OIDForm(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect(f'/printers/SNMP_OID/{id}')
    else:
        form = SNMP_OIDForm(instance = old_data)
    context ={
            'form':form,
            'title_text':title_text,
            'url_return_to_the_list':'SNMP_OID_list',
        }
    return render(request, 'printers/update.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def SNMP_OID_delete_view(request, id):
    try:
        data = get_object_or_404(SNMP_OIDModel, id=id)
        title_text = "SNMP_OID"
    except Exception:
        raise Http404('Такой записи не существует')

    if request.method == 'POST':
        data.delete()
        return redirect('SNMP_OID_list')
    else:
        return render(request, 'printers/delete.html', {'title_text':title_text,'url_return_to_the_list':'SNMP_OID_list',})


# ***********************************************************************************************************************************************************
# Printers_in_serviceModel

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def printers_in_service_create_view(request):
    title_text = "Принтеры/МФУ"
    # Проверяем, что запрос на добавление записи (POST) или просто на получение формы
    if request.method == 'POST':
        # Получаем из запроса только те данные которые использует форма
        form = Printers_in_serviceForm(request.POST)
        # Проверяем правильность введенных данных
        if form.is_valid():
            # сохраняем в базу
            form.save()
            # переадресуем на главную страницу
            return redirect('printers_in_service_list')
    else:
        form =Printers_in_serviceForm()
    context = {
            'form': form,
            'title_text':title_text,
            'url_return_to_the_list':'printers_in_service_list',
        }
    return render(request, 'printers/create.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# На обслуживании
def printers_in_service_list_view(request):
    form = Printers_in_serviceForm()
    # Получаем все записи
    dataset = Printers_in_serviceModel.objects.filter(archived=False)
    title_text = "Принтеры/МФУ (на обслуживании)"
    return render(request, 'printers/printers_in_service_listview.html', {'form': form, 'dataset': dataset, 'title_text':title_text})


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# @login_required
# @permission_required(perm='laptop.view_reestr_tmts_model', raise_exception=True)
def printers_in_service_list_view_filter(request):
    # form = Reestr_TMTS_Form()

    # Получаем все записи
    dataset = Printers_in_serviceModel.objects.all().select_related('service_object', 'printers', 'status_printer', 'print_server',).exclude(archived=True)

    dataset_filter = Printers_in_serviceModel_Filter(request.GET, queryset=dataset)

    count_dataset = dataset_filter.qs.count()

    title_text = "Принтеры/МФУ (на обслуживании)"

    dataset = dataset_filter.qs

    paginator = Paginator(dataset_filter.qs, 7)  #  paginate_by 5

    # page = request.GET.get('page', 1)
    page_number = request.GET.get('page')

    try:
        dataset = paginator.page(page_number)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages)


    context = {
            # 'form': form,
            # 'user_login': request.user,
            'dataset': dataset,
            'count_dataset': count_dataset,
            'title_text':title_text,
            'filter': dataset_filter,
        }
    return render(request, 'printers/printers_in_service_listview_filter.html', context)








# export_reestr_printers_in_service_xls
def printers_in_service_export_printed_pages_xls(request):
    pass



# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Переведены в архив
def printers_in_service_list_view_archived(request):
    form = Printers_in_serviceForm()
    # Получаем все записи
    # dataset = Printers_in_serviceModel.objects.all()
    dataset = Printers_in_serviceModel.objects.filter(archived=True)
    title_text = "Принтеры/МФУ (переведены в архив)"
    return render(request, 'printers/printers_in_service_listview.html', {'form': form, 'dataset': dataset, 'title_text':title_text})


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def printers_in_service_detail_view(request, id):
    try:
        # Получаем запись по-определенному id
        data = Printers_in_serviceModel.objects.get(id=id)
        title_text = "Принтер/МФУ"
    except Printers_in_serviceModel.DoesNotExist:
        raise Http404('Такой записи не существует')
    context ={
            'data': data,
            'title_text': title_text,
            'url_return_to_the_list':'printers_in_service_list',
        }
    return render(request, 'printers/printers_in_service_detailview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def printers_in_service_update_view(request, id):
    try:
        old_data = get_object_or_404(Printers_in_serviceModel, id=id)
        title_text = "Принтеры/МФУ"
    except Exception:
        raise Http404('Такой записи не существует')

    # Если метод POST, то это обновленные данные
    # Остальные методы - возврат данных для изменения
    if request.method =='POST':
        form = Printers_in_serviceForm(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect(f'/printers/printers_in_service/{id}')
    else:
        form = Printers_in_serviceForm(instance = old_data)
    context ={
            'form':form,
            'title_text':title_text,
            'url_return_to_the_list':'printers_in_service_list',
        }
    return render(request, 'printers/update.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def printers_in_service_delete_view(request, id):
    try:
        data = get_object_or_404(Printers_in_serviceModel, id=id)
        title_text = "Принтеры/МФУ"
    except Exception:
        raise Http404('Такой записи не существует')

    if request.method == 'POST':
        data.delete()
        return redirect('printers_in_service_list')
    else:
        return render(request, 'printers/delete.html', {'title_text':title_text,'url_return_to_the_list':'printers_in_service_list',})


# ***********************************************************************************************************************************************************
# Service_objectModel

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def service_object_create_view(request):
    title_text = "Объекты_обслуживания"
    # Проверяем, что запрос на добавление записи (POST) или просто на получение формы
    if request.method == 'POST':
        # Получаем из запроса только те данные которые использует форма
        form = Service_objectForm(request.POST)
        # Проверяем правильность введенных данных
        if form.is_valid():
            # сохраняем в базу
            form.save()
            # переадресуем на главную страницу
            return redirect('service_object_list')
    else:
        form = Service_objectForm()
    context = {
            'form': form,
            'title_text':title_text,
            'url_return_to_the_list':'service_object_list',
        }
    return render(request, 'printers/create.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def service_object_list_view(request):
    # Получаем все записи
    dataset = Service_objectModel.objects.all()
    title_text = "Объекты_обслуживания"

    context = {
            'dataset': dataset,
            'user_login': request.user,
            'title_text':title_text,
            'priznak':'all',
            # 'url_return_to_the_list':'reestr_tmts_list',
        }
    return render(request, 'printers/service_object_listview.html', context=context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def service_object_list_view_bb(request):
    # Получаем все записи
    dataset = Service_objectModel.objects.filter(service_object_name__icontains="ББ")
    title_text = "Объекты_обслуживания"
    context = {
            'dataset': dataset,
            'user_login': request.user,
            'title_text':title_text,
            'priznak':'bb',
            # 'url_return_to_the_list':'reestr_tmts_list',
        }
    return render(request, 'printers/service_object_listview.html', context=context)

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def service_object_list_view_bmk(request):
    # Получаем все записи
    dataset = Service_objectModel.objects.all().exclude(service_object_name__icontains="ББ")
    title_text = "Объекты_обслуживания"
    context = {
            'dataset': dataset,
            'user_login': request.user,
            'title_text':title_text,
            'priznak':'bmk',
            # 'url_return_to_the_list':'reestr_tmts_list',
        }
    return render(request, 'printers/service_object_listview.html', context=context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def service_object_detail_view(request, id):
    try:
        # Получаем запись по-определенному id
        data = Service_objectModel.objects.get(id=id)
        title_text = "Объект_обслуживания"
    except Service_objectModel.DoesNotExist:
        raise Http404('Такой записи не существует')
    context ={
            'data': data,
            'title_text': title_text,
            'url_return_to_the_list':'service_object_list',
        }
    return render(request, 'printers/service_object_detailview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def service_object_update_view(request, id):
    try:
        old_data = get_object_or_404(Service_objectModel, id=id)
        title_text = "Объекты_обслуживания"
    except Exception:
        raise Http404('Такой записи не существует')

    # Если метод POST, то это обновленные данные
    # Остальные методы - возврат данных для изменения
    if request.method =='POST':
        form = Service_objectForm(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect(f'/printers/service_object/{id}')
    else:
        form = Service_objectForm(instance = old_data)
    context ={
            'form':form,
            'title_text':title_text,
            'url_return_to_the_list':'service_object_list',
        }
    return render(request, 'printers/update.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def service_object_delete_view(request, id):
    try:
        data = get_object_or_404(Service_objectModel, id=id)
        title_text = "Объекты_обслуживания"
    except Exception:
        raise Http404('Такой записи не существует')

    if request.method == 'POST':
        data.delete()
        return redirect('service_object_list')
    else:
        return render(request, 'printers/delete.html', {'title_text':title_text,'url_return_to_the_list':'service_object_list',})


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def service_object_export_printed_pages_xls(request, id):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="printed_pages.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('printed_pages')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
                    'Объект_обслуживания',
                    'S/N',
                    'Модель принтера',
                    'Статус',
                    'Print-server',
                    'Имя на Print-server',
                    'IP-address',
                    'Локация/Кабинет',
                    'S/N (oid)',
                    'Распечатано страниц (всего)',
                    'Дата формирования',
                    'Ошибки формирования',
                ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = []
    # Получаем все неархивные записи из Printers_in_serviceModel с учетом объекта обслуживания
    dataset_printers_in_service = Printers_in_serviceModel.objects.filter(archived=False).filter(service_object_id=id)

    for data_printers_in_service in dataset_printers_in_service:
        service_object_name = data_printers_in_service.service_object.service_object_name if data_printers_in_service.service_object != None  else ''   #0
        serial_number = data_printers_in_service.serial_number                                                                                          #1
        model_name = data_printers_in_service.printers.name,                                                                                            #2
        status_printer = data_printers_in_service.status_printer.status,                                                                                #3
        print_server = data_printers_in_service.print_server.print_server if data_printers_in_service.print_server != None  else ''                     #4
        name_on_print_server = data_printers_in_service.name_on_print_server if data_printers_in_service.name_on_print_server != None  else ''          #5
        ip_address = data_printers_in_service.ip_address if data_printers_in_service.ip_address != None  else ''                                        #6
        location = data_printers_in_service.location,                                                                                                   #7

        sn_oid = get_data_by_oid(ip_address, data_printers_in_service.printers.sn_oid.oid),                                                             #8
        printed_pages_all_oid = get_data_by_oid(ip_address, data_printers_in_service.printers.printed_pages_all_oid.oid),                               #9

        # print("^"*35)
        # print(service_object_name)
        # print(print_server)
        # print(name_on_print_server)
        # print(ip_address)
        # print(sn_oid)
        # print(printed_pages_all_oid)
        # print("^"*35)

        # проверяем корректность данных
        errors = ""

        if serial_number != sn_oid[0]:
            errors += 'S/N не равны| '
        if printed_pages_all_oid[0] == 0 or printed_pages_all_oid[0] == '' or printed_pages_all_oid[0] == None or printed_pages_all_oid[0] =='\x00\x00\x00\x00':
            errors += 'printed_pages_error|'

        # если ошибок нет, записисываем данные в БД
        if errors == "":
            # Printed_pagesModel.objects.create(printers_in_service=data_printers_in_service, printed_pages=int(printed_pages_all_oid[0]))
            Printed_pagesModel.objects.create(
                printers_in_service=data_printers_in_service.id,

                service_object_name=data_printers_in_service.service_object.service_object_name,
                printers_name=data_printers_in_service.printers.name,
                serial_number=data_printers_in_service.serial_number,
                ip_address=data_printers_in_service.ip_address,
                name_on_print_server = data_printers_in_service.name_on_print_server,
                location = data_printers_in_service.location,

                printed_pages=int(printed_pages_all_oid[0]))

        rows.append(
            [


                service_object_name,       #0
                serial_number,             #1
                model_name,                #2
                status_printer,            #3
                print_server,              #4
                name_on_print_server,      #5
                ip_address,                #6
                location,                  #7
                sn_oid[0],                 #8
                printed_pages_all_oid[0],  #9
                datetime.datetime.now(),   #10
                errors,                    #11

            ]
                    )

    # print(rows)

    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def service_object_all_export_printed_pages_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="printed_pages.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('printed_pages')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
                    'Объект_обслуживания',
                    'S/N',
                    'Модель принтера',
                    'Статус',
                    'Print-server',
                    'Имя на Print-server',
                    'IP-address',
                    'Локация/Кабинет',
                    'S/N (oid)',
                    'Распечатано страниц (всего)',
                    'Дата формирования',
                    'Ошибки формирования',
                ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = []
    # Получаем все неархивные записи из Printers_in_serviceModel с учетом объекта обслуживания
    dataset_printers_in_service = Printers_in_serviceModel.objects.filter(archived=False)

    for data_printers_in_service in dataset_printers_in_service:
        service_object_name = data_printers_in_service.service_object.service_object_name if data_printers_in_service.service_object != None  else ''   #0
        serial_number = data_printers_in_service.serial_number                                                                                          #1
        model_name = data_printers_in_service.printers.name,                                                                                            #2
        status_printer = data_printers_in_service.status_printer.status,                                                                                #3
        print_server = data_printers_in_service.print_server.print_server if data_printers_in_service.print_server != None  else ''                     #4
        name_on_print_server = data_printers_in_service.name_on_print_server if data_printers_in_service.name_on_print_server != None  else ''          #5
        ip_address = data_printers_in_service.ip_address if data_printers_in_service.ip_address != None  else ''                                        #6
        location = data_printers_in_service.location,                                                                                                   #7

        sn_oid = get_data_by_oid(ip_address, data_printers_in_service.printers.sn_oid.oid),                                                             #8
        printed_pages_all_oid = get_data_by_oid(ip_address, data_printers_in_service.printers.printed_pages_all_oid.oid),                               #9

        # print("^"*35)
        # print(service_object_name)
        # print(print_server)
        # print(name_on_print_server)
        # print(ip_address)
        # print(sn_oid)
        # print(printed_pages_all_oid)
        # print("^"*35)

        # проверяем корректность данных
        errors = ""

        if serial_number != sn_oid[0]:
            errors += 'S/N не равны| '
        if printed_pages_all_oid[0] == 0 or printed_pages_all_oid[0] == '' or printed_pages_all_oid[0] == None or printed_pages_all_oid[0] =='\x00\x00\x00\x00':
            errors += 'printed_pages_error|'

        # если ошибок нет, записисываем данные в БД
        if errors == "":
            # Printed_pagesModel.objects.create(printers_in_service=data_printers_in_service, printed_pages=int(printed_pages_all_oid[0]))
            Printed_pagesModel.objects.create(
                printers_in_service=data_printers_in_service.id,

                service_object_name=data_printers_in_service.service_object.service_object_name,
                printers_name=data_printers_in_service.printers.name,
                serial_number=data_printers_in_service.serial_number,
                ip_address=data_printers_in_service.ip_address,
                name_on_print_server = data_printers_in_service.name_on_print_server,
                location = data_printers_in_service.location,

                printed_pages=int(printed_pages_all_oid[0]))

        rows.append(
            [


                service_object_name,       #0
                serial_number,             #1
                model_name,                #2
                status_printer,            #3
                print_server,              #4
                name_on_print_server,      #5
                ip_address,                #6
                location,                  #7
                sn_oid[0],                 #8
                printed_pages_all_oid[0],  #9
                datetime.datetime.now(),   #10
                errors,                    #11

            ]
                    )

    # print(rows)

    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def service_object_all_export_printed_pages_xls_bb(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="printed_pages.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('printed_pages')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
                    'Объект_обслуживания',
                    'S/N',
                    'Модель принтера',
                    'Статус',
                    'Print-server',
                    'Имя на Print-server',
                    'IP-address',
                    'Локация/Кабинет',
                    'S/N (oid)',
                    'Распечатано страниц (всего)',
                    'Дата формирования',
                    'Ошибки формирования',
                ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = []
    # Получаем все неархивные записи из Printers_in_serviceModel с учетом объекта обслуживания
    dataset_printers_in_service = Printers_in_serviceModel.objects.filter(archived=False, service_object__service_object_name="ББ")

    for data_printers_in_service in dataset_printers_in_service:
        service_object_name = data_printers_in_service.service_object.service_object_name if data_printers_in_service.service_object != None  else ''   #0
        serial_number = data_printers_in_service.serial_number                                                                                          #1
        model_name = data_printers_in_service.printers.name,                                                                                            #2
        status_printer = data_printers_in_service.status_printer.status,                                                                                #3
        print_server = data_printers_in_service.print_server.print_server if data_printers_in_service.print_server != None  else ''                     #4
        name_on_print_server = data_printers_in_service.name_on_print_server if data_printers_in_service.name_on_print_server != None  else ''          #5
        ip_address = data_printers_in_service.ip_address if data_printers_in_service.ip_address != None  else ''                                        #6
        location = data_printers_in_service.location,                                                                                                   #7

        sn_oid = get_data_by_oid(ip_address, data_printers_in_service.printers.sn_oid.oid),                                                             #8
        printed_pages_all_oid = get_data_by_oid(ip_address, data_printers_in_service.printers.printed_pages_all_oid.oid),                               #9

        # print("^"*35)
        # print(service_object_name)
        # print(print_server)
        # print(name_on_print_server)
        # print(ip_address)
        # print(sn_oid)
        # print(printed_pages_all_oid)
        # print("^"*35)

        # проверяем корректность данных
        errors = ""

        if serial_number != sn_oid[0]:
            errors += 'S/N не равны| '
        if printed_pages_all_oid[0] == 0 or printed_pages_all_oid[0] == '' or printed_pages_all_oid[0] == None or printed_pages_all_oid[0] =='\x00\x00\x00\x00':
            errors += 'printed_pages_error|'

        # если ошибок нет, записисываем данные в БД
        if errors == "":
            # Printed_pagesModel.objects.create(printers_in_service=data_printers_in_service, printed_pages=int(printed_pages_all_oid[0]))
            Printed_pagesModel.objects.create(
                printers_in_service=data_printers_in_service.id,

                service_object_name=data_printers_in_service.service_object.service_object_name,
                printers_name=data_printers_in_service.printers.name,
                serial_number=data_printers_in_service.serial_number,
                ip_address=data_printers_in_service.ip_address,
                name_on_print_server = data_printers_in_service.name_on_print_server,
                location = data_printers_in_service.location,

                printed_pages=int(printed_pages_all_oid[0]))

        rows.append(
            [


                service_object_name,       #0
                serial_number,             #1
                model_name,                #2
                status_printer,            #3
                print_server,              #4
                name_on_print_server,      #5
                ip_address,                #6
                location,                  #7
                sn_oid[0],                 #8
                printed_pages_all_oid[0],  #9
                datetime.datetime.now(),   #10
                errors,                    #11

            ]
                    )

    # print(rows)

    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def service_object_all_export_printed_pages_xls_bmk(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="printed_pages.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('printed_pages')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
                    'Объект_обслуживания',
                    'S/N',
                    'Модель принтера',
                    'Статус',
                    'Print-server',
                    'Имя на Print-server',
                    'IP-address',
                    'Локация/Кабинет',
                    'S/N (oid)',
                    'Распечатано страниц (всего)',
                    'Дата формирования',
                    'Ошибки формирования',
                ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = []
    # Получаем все неархивные записи из Printers_in_serviceModel с учетом объекта обслуживания
    dataset_printers_in_service = Printers_in_serviceModel.objects.filter(archived=False).exclude(service_object__service_object_name="ББ")

    for data_printers_in_service in dataset_printers_in_service:
        service_object_name = data_printers_in_service.service_object.service_object_name if data_printers_in_service.service_object != None  else ''   #0
        serial_number = data_printers_in_service.serial_number                                                                                          #1
        model_name = data_printers_in_service.printers.name,                                                                                            #2
        status_printer = data_printers_in_service.status_printer.status,                                                                                #3
        print_server = data_printers_in_service.print_server.print_server if data_printers_in_service.print_server != None  else ''                     #4
        name_on_print_server = data_printers_in_service.name_on_print_server if data_printers_in_service.name_on_print_server != None  else ''          #5
        ip_address = data_printers_in_service.ip_address if data_printers_in_service.ip_address != None  else ''                                        #6
        location = data_printers_in_service.location,                                                                                                   #7

        sn_oid = get_data_by_oid(ip_address, data_printers_in_service.printers.sn_oid.oid),                                                             #8
        printed_pages_all_oid = get_data_by_oid(ip_address, data_printers_in_service.printers.printed_pages_all_oid.oid),                               #9

        # print("^"*35)
        # print(service_object_name)
        # print(print_server)
        # print(name_on_print_server)
        # print(ip_address)
        # print(sn_oid)
        # print(printed_pages_all_oid)
        # print("^"*35)

        # проверяем корректность данных
        errors = ""

        if serial_number != sn_oid[0]:
            errors += 'S/N не равны| '
        if printed_pages_all_oid[0] == 0 or printed_pages_all_oid[0] == '' or printed_pages_all_oid[0] == None or printed_pages_all_oid[0] =='\x00\x00\x00\x00':
            errors += 'printed_pages_error|'

        # если ошибок нет, записисываем данные в БД
        if errors == "":
            # Printed_pagesModel.objects.create(printers_in_service=data_printers_in_service, printed_pages=int(printed_pages_all_oid[0]))
            Printed_pagesModel.objects.create(
                printers_in_service=data_printers_in_service.id,

                service_object_name=data_printers_in_service.service_object.service_object_name,
                printers_name=data_printers_in_service.printers.name,
                serial_number=data_printers_in_service.serial_number,
                ip_address=data_printers_in_service.ip_address,
                name_on_print_server = data_printers_in_service.name_on_print_server,
                location = data_printers_in_service.location,

                printed_pages=int(printed_pages_all_oid[0]))

        rows.append(
            [


                service_object_name,       #0
                serial_number,             #1
                model_name,                #2
                status_printer,            #3
                print_server,              #4
                name_on_print_server,      #5
                ip_address,                #6
                location,                  #7
                sn_oid[0],                 #8
                printed_pages_all_oid[0],  #9
                datetime.datetime.now(),   #10
                errors,                    #11

            ]
                    )

    # print(rows)

    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response




# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .forms import RegistrationForm
# from .tasks import send_welcome_email

# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Запускаем асинхронную задачу
#             send_welcome_email.delay(user.id)
#             messages.success(request, 'Регистрация успешна! Проверьте вашу почту.')
#             return redirect('home')
#     else:
#         form = RegistrationForm()
#     return render(request, 'users/register.html', {'form': form})


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def async_service_object_printed_pages_list_view(request, id):

    from .tasks import get_data_by_oid

    # Получаем все неархивные записи из Printers_in_serviceModel с учетом объекта обслуживания
    dataset_printers_in_service = Printers_in_serviceModel.objects.filter(archived=False).filter(service_object_id=id)

    for data_printers_in_service in dataset_printers_in_service:
        # Запускаем асинхронную задачу
        get_data_by_oid.delay(data_printers_in_service.ip_address,
                                        data_printers_in_service.printers.sn_oid.oid,
                                        data_printers_in_service.printers.printed_pages_all_oid.oid,
                                        data_printers_in_service.id)



    id_printers_massive = []
    for data_printers_in_service in dataset_printers_in_service:
        id_printers_massive.append(data_printers_in_service.id)

    # print(id_printers_massive)

    for id_printer in id_printers_massive:
        try:

            # data_printers_in_service = Printed_pagesModel.objects.filter(printers_in_service=data_printers_in_service.id).latest('created')
            data_printers_in_service = Printed_pagesModel.objects.filter(printers_in_service=id_printer).latest('created')

            if data_printers_in_service == None:
                continue

            print(
                    str(data_printers_in_service.id)\
                    + ' | ' + str(data_printers_in_service.printers_in_service)\
                    + ' | ' + str(data_printers_in_service.service_object_name) \
                    + ' | ' + str(data_printers_in_service.printers_name) \
                    + ' | ' + str(data_printers_in_service.serial_number) \
                    + ' | ' + str(data_printers_in_service.ip_address) \
                    + ' | ' + str(data_printers_in_service.name_on_print_server) \
                    + ' | ' + str(data_printers_in_service.location) \
                    + ' | ' + str(data_printers_in_service.created) \
                    + ' | ' + str(data_printers_in_service.printed_pages)
                )

        except Exception as ex:
            print(f"Ошибка выполнения функции async_service_object_printed_pages_list_view(request, id): {ex} ||| id_printer: {id_printer}")
            continue


    # Переходим на главную страницу, пока выполняются запросы
    # Получаем все записи
    dataset = Service_objectModel.objects.all()
    title_text = "Объекты_обслуживания"

    context = {
            'dataset': dataset,
            'user_login': request.user,
            'title_text':title_text,
            'priznak':'all',
            # 'url_return_to_the_list':'reestr_tmts_list',
        }
    return render(request, 'printers/service_object_listview.html', context=context)




# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def service_object_printed_pages_list_view(request, id):
    form = Printed_pagesForm()

    print("+"*35)
    print("Start tasks - datetime: ", datetime.datetime.now())
    print("-"*35)

    # Получаем все неархивные записи из Printers_in_serviceModel с учетом объекта обслуживания
    dataset_printers_in_service = Printers_in_serviceModel.objects.filter(archived=False).filter(service_object_id=id)


    dataset_thead = ['IP-адрес', 'Модель принтера', 'Статус', 'Имя на Print-server', 'Локация/Кабинет', 'S/N','Распечатано страниц (всего)',]

    title_text = "Распечатано страниц"

    dataset = []



    # #####
    # tasks = []

    # for data_printers_in_service in dataset_printers_in_service:

    #     # print("" + data_printers_in_service.ip_address)

    #     # return "" + ip + "_" +  oid + "_" + response.value
    #     tasks.append(asyncio.create_task(async_get_data_by_oid(data_printers_in_service.ip_address, data_printers_in_service.printers.sn_oid.oid)))
    #     tasks.append(asyncio.create_task(async_get_data_by_oid(data_printers_in_service.ip_address, data_printers_in_service.printers.printed_pages_all_oid.oid)))

    # results_data = await asyncio.gather(*tasks)

    # # results_data = asyncio.run(create_massive_by_oid(dataset_printers_in_service))

    # dict_async_get_data_by_oid = {}
    # for result in results_data:
    #     # return "" + ip + "_" +  oid + "_" + response.value
    #     tmp_massive = result.split("_")
    #     dict_async_get_data_by_oid[tmp_massive[0] + "_" + tmp_massive[1]] = tmp_massive[2]
    # #####


    for data_printers_in_service in dataset_printers_in_service:

        sn_oid = get_data_by_oid(data_printers_in_service.ip_address, data_printers_in_service.printers.sn_oid.oid),                     #8
        printed_pages_all_oid = get_data_by_oid(data_printers_in_service.ip_address, data_printers_in_service.printers.printed_pages_all_oid.oid),      #9
        # sn_oid =  dict_async_get_data_by_oid.get(data_printers_in_service.ip_address + "_" + data_printers_in_service.printers.sn_oid.oid)
        # printed_pages_all_oid = dict_async_get_data_by_oid.get(data_printers_in_service.ip_address + "_" + data_printers_in_service.printers.printed_pages_all_oid.oid)



        # проверяем корректность данных
        errors = ""

        if data_printers_in_service.serial_number != sn_oid[0]:
            errors += 'S/N не равны| '
        if printed_pages_all_oid[0] == 0 or printed_pages_all_oid[0] == '' or printed_pages_all_oid[0] == None or printed_pages_all_oid[0] =='\x00\x00\x00\x00':
            errors += 'printed_pages_error|'

        # если ошибок нет, записисываем данные в БД
        if errors == "":
            Printed_pagesModel.objects.create(
                printers_in_service=data_printers_in_service.id,

                service_object_name=data_printers_in_service.service_object.service_object_name,
                printers_name=data_printers_in_service.printers.name,
                serial_number=data_printers_in_service.serial_number,
                ip_address=data_printers_in_service.ip_address,
                name_on_print_server = data_printers_in_service.name_on_print_server,
                location = data_printers_in_service.location,

                printed_pages=int(printed_pages_all_oid[0]))

        dataset.append(
            [
                data_printers_in_service.service_object,            #0
                data_printers_in_service.serial_number,             #1
                data_printers_in_service.printers,                  #2
                data_printers_in_service.status_printer,            #3
                data_printers_in_service.print_server,              #4
                data_printers_in_service.name_on_print_server,      #5
                data_printers_in_service.ip_address,                #6
                data_printers_in_service.location,                  #7
                sn_oid[0],                                          #8
                printed_pages_all_oid[0],                           #9
                datetime.datetime.now(),                            #10
                errors,                                             #11

            ]
                    )

    print("+"*35)
    print("End_tasks - datetime: ", datetime.datetime.now())
    print("+"*35)
    for data in dataset:
        print(data)
    print("-"*35)

    name_colomns = [
                    'Объект_обслуживания',
                    'S/N',
                    'Модель принтера',
                    'Статус',
                    'Print-server',
                    'Имя на Print-server',
                    'IP-address',
                    'Локация/Кабинет',
                    'S/N (oid)',
                    'Распечатано страниц (всего)',
                    'Дата формирования',
                    'Ошибки формирования',
                    ]

    name_file='printed_pages_list'


    context = {
            'form': form,
            'title_text':title_text,
            'dataset': dataset,
            'dataset_count': len(dataset),
            # 'url_export_csv':'export_csv',
            # 'url_export_csv':'service_object_list',
            'name_colomns': name_colomns,
            'name_file': name_file,
        }

    return render(request, 'printers/service_object_printed_pages_listview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def service_object_printed_pages_all_list_view(request):
    form = Printed_pagesForm()

    # Получаем все неархивные записи из Printers_in_serviceModel с учетом объекта обслуживания
    dataset_printers_in_service = Printers_in_serviceModel.objects.filter(archived=False)


    dataset_thead = ['IP-адрес', 'Модель принтера', 'Статус', 'Имя на Print-server', 'Локация/Кабинет', 'S/N','Распечатано страниц (всего)',]

    title_text = "Распечатано страниц"

    dataset = []

    # print("+"*35)
    # print(dataset_printers_in_service)
    # print("-"*35)


    for data_printers_in_service in dataset_printers_in_service:

        sn_oid = get_data_by_oid(data_printers_in_service.ip_address, data_printers_in_service.printers.sn_oid.oid),                     #8
        printed_pages_all_oid = get_data_by_oid(data_printers_in_service.ip_address, data_printers_in_service.printers.printed_pages_all_oid.oid),      #9

        # проверяем корректность данных
        errors = ""

        if data_printers_in_service.serial_number != sn_oid[0]:
            errors += 'S/N не равны| '
        if printed_pages_all_oid[0] == 0 or printed_pages_all_oid[0] == '' or printed_pages_all_oid[0] == None or printed_pages_all_oid[0] =='\x00\x00\x00\x00':
            errors += 'printed_pages_error|'

        # если ошибок нет, записисываем данные в БД
        if errors == "":
            # Printed_pagesModel.objects.create(printers_in_service=data_printers_in_service, printed_pages=int(printed_pages_all_oid[0]))
            Printed_pagesModel.objects.create(
                printers_in_service=data_printers_in_service.id,

                service_object_name=data_printers_in_service.service_object.service_object_name,
                printers_name=data_printers_in_service.printers.name,
                serial_number=data_printers_in_service.serial_number,
                ip_address=data_printers_in_service.ip_address,
                name_on_print_server = data_printers_in_service.name_on_print_server,
                location = data_printers_in_service.location,

                printed_pages=int(printed_pages_all_oid[0]))

        dataset.append(
            [
                data_printers_in_service.service_object,            #0
                data_printers_in_service.serial_number,             #1
                data_printers_in_service.printers,                  #2
                data_printers_in_service.status_printer,            #3
                data_printers_in_service.print_server,              #4
                data_printers_in_service.name_on_print_server,      #5
                data_printers_in_service.ip_address,                #6
                data_printers_in_service.location,                  #7
                sn_oid[0],                                          #8
                printed_pages_all_oid[0],                           #9
                datetime.datetime.now(),                            #10
                errors,                                             #11

            ]
                    )

    # print("+"*35)
    # for data in dataset:
    #     print(data)
    # print("-"*35)

    name_colomns = [
                    'Объект_обслуживания',
                    'S/N',
                    'Модель принтера',
                    'Статус',
                    'Print-server',
                    'Имя на Print-server',
                    'IP-address',
                    'Локация/Кабинет',
                    'S/N (oid)',
                    'Распечатано страниц (всего)',
                    'Дата формирования',
                    'Ошибки формирования',
                    ]

    name_file='printed_pages_list'


    context = {
            'form': form,
            'title_text':title_text,
            'dataset': dataset,
            'dataset_count': len(dataset),
            # 'url_export_csv':'export_csv',
            # 'url_export_csv':'service_object_list',
            'name_colomns': name_colomns,
            'name_file': name_file,
        }

    return render(request, 'printers/service_object_printed_pages_listview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def service_object_printed_pages_bb_list_view(request):
    form = Printed_pagesForm()

    # Получаем все неархивные записи из Printers_in_serviceModel с учетом объекта обслуживания
    dataset_printers_in_service = Printers_in_serviceModel.objects.filter(archived=False, service_object__service_object_name="ББ")


    dataset_thead = ['IP-адрес', 'Модель принтера', 'Статус', 'Имя на Print-server', 'Локация/Кабинет', 'S/N','Распечатано страниц (всего)',]

    title_text = "Распечатано страниц"

    dataset = []

    # print("+"*35)
    # print(dataset_printers_in_service)
    # print("-"*35)


    for data_printers_in_service in dataset_printers_in_service:

        sn_oid = get_data_by_oid(data_printers_in_service.ip_address, data_printers_in_service.printers.sn_oid.oid),                     #8
        printed_pages_all_oid = get_data_by_oid(data_printers_in_service.ip_address, data_printers_in_service.printers.printed_pages_all_oid.oid),      #9

        # проверяем корректность данных
        errors = ""

        if data_printers_in_service.serial_number != sn_oid[0]:
            errors += 'S/N не равны| '
        if printed_pages_all_oid[0] == 0 or printed_pages_all_oid[0] == '' or printed_pages_all_oid[0] == None or printed_pages_all_oid[0] =='\x00\x00\x00\x00':
            errors += 'printed_pages_error|'

        # если ошибок нет, записисываем данные в БД
        if errors == "":
            # Printed_pagesModel.objects.create(printers_in_service=data_printers_in_service, printed_pages=int(printed_pages_all_oid[0]))
            Printed_pagesModel.objects.create(
                printers_in_service=data_printers_in_service.id,

                service_object_name=data_printers_in_service.service_object.service_object_name,
                printers_name=data_printers_in_service.printers.name,
                serial_number=data_printers_in_service.serial_number,
                ip_address=data_printers_in_service.ip_address,
                name_on_print_server = data_printers_in_service.name_on_print_server,
                location = data_printers_in_service.location,

                printed_pages=int(printed_pages_all_oid[0]))

        dataset.append(
            [
                data_printers_in_service.service_object,            #0
                data_printers_in_service.serial_number,             #1
                data_printers_in_service.printers,                  #2
                data_printers_in_service.status_printer,            #3
                data_printers_in_service.print_server,              #4
                data_printers_in_service.name_on_print_server,      #5
                data_printers_in_service.ip_address,                #6
                data_printers_in_service.location,                  #7
                sn_oid[0],                                          #8
                printed_pages_all_oid[0],                           #9
                datetime.datetime.now(),                            #10
                errors,                                             #11

            ]
                    )

    # print("+"*35)
    # for data in dataset:
    #     print(data)
    # print("-"*35)

    name_colomns = [
                    'Объект_обслуживания',
                    'S/N',
                    'Модель принтера',
                    'Статус',
                    'Print-server',
                    'Имя на Print-server',
                    'IP-address',
                    'Локация/Кабинет',
                    'S/N (oid)',
                    'Распечатано страниц (всего)',
                    'Дата формирования',
                    'Ошибки формирования',
                    ]

    name_file='printed_pages_list'


    context = {
            'form': form,
            'title_text':title_text,
            'dataset': dataset,
            'dataset_count': len(dataset),
            # 'url_export_csv':'export_csv',
            # 'url_export_csv':'service_object_list',
            'name_colomns': name_colomns,
            'name_file': name_file,
        }

    return render(request, 'printers/service_object_printed_pages_listview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def service_object_printed_pages_bmk_list_view(request):
    form = Printed_pagesForm()

    # Получаем все неархивные записи из Printers_in_serviceModel с учетом объекта обслуживания
    dataset_printers_in_service = Printers_in_serviceModel.objects.filter(archived=False).exclude(service_object__service_object_name="ББ")


    dataset_thead = ['IP-адрес', 'Модель принтера', 'Статус', 'Имя на Print-server', 'Локация/Кабинет', 'S/N','Распечатано страниц (всего)',]

    title_text = "Распечатано страниц"

    dataset = []

    # print("+"*35)
    # print(dataset_printers_in_service)
    # print("-"*35)


    for data_printers_in_service in dataset_printers_in_service:

        sn_oid = get_data_by_oid(data_printers_in_service.ip_address, data_printers_in_service.printers.sn_oid.oid),                     #8
        printed_pages_all_oid = get_data_by_oid(data_printers_in_service.ip_address, data_printers_in_service.printers.printed_pages_all_oid.oid),      #9

        # проверяем корректность данных
        errors = ""

        if data_printers_in_service.serial_number != sn_oid[0]:
            errors += 'S/N не равны| '
        if printed_pages_all_oid[0] == 0 or printed_pages_all_oid[0] == '' or printed_pages_all_oid[0] == None or printed_pages_all_oid[0] =='\x00\x00\x00\x00':
            errors += 'printed_pages_error|'

        # если ошибок нет, записисываем данные в БД
        if errors == "":
            # Printed_pagesModel.objects.create(printers_in_service=data_printers_in_service, printed_pages=int(printed_pages_all_oid[0]))
            Printed_pagesModel.objects.create(
                printers_in_service=data_printers_in_service.id,

                service_object_name=data_printers_in_service.service_object.service_object_name,
                printers_name=data_printers_in_service.printers.name,
                serial_number=data_printers_in_service.serial_number,
                ip_address=data_printers_in_service.ip_address,
                name_on_print_server = data_printers_in_service.name_on_print_server,
                location = data_printers_in_service.location,

                printed_pages=int(printed_pages_all_oid[0]))

        dataset.append(
            [
                data_printers_in_service.service_object,            #0
                data_printers_in_service.serial_number,             #1
                data_printers_in_service.printers,                  #2
                data_printers_in_service.status_printer,            #3
                data_printers_in_service.print_server,              #4
                data_printers_in_service.name_on_print_server,      #5
                data_printers_in_service.ip_address,                #6
                data_printers_in_service.location,                  #7
                sn_oid[0],                                          #8
                printed_pages_all_oid[0],                           #9
                datetime.datetime.now(),                            #10
                errors,                                             #11

            ]
                    )

    # print("+"*35)
    # for data in dataset:
    #     print(data)
    # print("-"*35)

    name_colomns = [
                    'Объект_обслуживания',
                    'S/N',
                    'Модель принтера',
                    'Статус',
                    'Print-server',
                    'Имя на Print-server',
                    'IP-address',
                    'Локация/Кабинет',
                    'S/N (oid)',
                    'Распечатано страниц (всего)',
                    'Дата формирования',
                    'Ошибки формирования',
                    ]

    name_file='printed_pages_list'


    context = {
            'form': form,
            'title_text':title_text,
            'dataset': dataset,
            'dataset_count': len(dataset),
            # 'url_export_csv':'export_csv',
            # 'url_export_csv':'service_object_list',
            'name_colomns': name_colomns,
            'name_file': name_file,
        }

    return render(request, 'printers/service_object_printed_pages_listview.html', context)



# ***********************************************************************************************************************************************************
# Printed_pagesModel

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def printed_pages_list_view(request):
    form = Printed_pagesForm()
    # Получаем все записи
    dataset = Printed_pagesModel.objects.all().order_by('-created')[:100]
    title_text = "Распечатано страниц"

    context ={
            'form':form,
            'dataset': dataset,
            'title_text':title_text,
            # 'url_return_to_the_list':'service_object_list',
        }

    return render(request, 'printers/printed_pages_listview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# export all printed_pages reestr (Printed_pagesModel)
def export_printed_pages_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="printed_pages.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('printed_pages')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    # columns = ['Объект обслуживания', 'Модель принтера', 'S/N', 'IP-address', 'Имя на Print-server', 'Дата формирования', 'Распечатано страниц', ]
    columns = ['id', 'id объекта обслуживания', 'Объект обслуживания', 'Модель принтера',
                    'S/N', 'IP-address', 'Имя на Print-server', 'Локация/Кабинет', 'Дата формирования', 'Распечатано страниц', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = []
    dataset = Printed_pagesModel.objects.all()
    for row in dataset:
        rows.append(
            [
                row.id,
                row.printers_in_service,
                row.service_object_name,
                row.printers_name,
                row.serial_number,
                row.ip_address,
                row.name_on_print_server,
                row.location,
                row.created,
                row.printed_pages,
            ]
        )




    # rows = Printed_pagesModel.objects.all().values_list('printers_in_service.service_object.service_object_name',
    #                                                     'printers_in_service.printers.name',
    #                                                     'printers_in_service.serial_number',
    #                                                     'printers_in_service.ip_address',
    #                                                     'created',
    #                                                     'printed_pages')

    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# def service_object_create_view(request):
#     title_text = "Объекты_обслуживания"
#     # Проверяем, что запрос на добавление записи (POST) или просто на получение формы
#     if request.method == 'POST':
#         # Получаем из запроса только те данные которые использует форма
#         form = Service_objectForm(request.POST)
#         # Проверяем правильность введенных данных
#         if form.is_valid():
#             # сохраняем в базу
#             form.save()
#             # переадресуем на главную страницу
#             return redirect('service_object_list')
#     else:
#         form = Service_objectForm()
#         context = {
#             'form': form,
#             'title_text':title_text,
#             'url_return_to_the_list':'service_object_list',
#         }
#         return render(request, 'printers/create.html', context)
