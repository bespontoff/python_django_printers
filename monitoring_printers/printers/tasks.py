from celery import shared_task
# from django.core.mail import send_mail
# from time import sleep
import datetime

from celery.utils.log import get_task_logger

from easysnmp import snmp_get



logger = get_task_logger(__name__)



# @shared_task
# def send_welcome_email(user_id):
#     from users.models import User  # Импортируем здесь для избежания циклических импортов

#     try:
#         user = User.objects.get(id=user_id)
#         # Имитация длительной операции
#         sleep(5)

#         send_mail(
#             'Добро пожаловать на наш сайт!',
#             f'Здравствуйте, {user.username}! Спасибо за регистрацию.',
#             'noreply@example.com',
#             [user.email],
#             fail_silently=False,
#         )
#         return f"Email успешно отправлен пользователю {user.email}"
#     except User.DoesNotExist:
#         return f"Пользователь с ID {user_id} не найден"

# @shared_task
# def add_printed_pages_data(id):
#     from printers.models import Printers_in_serviceModel  # Импортируем здесь для избежания циклических импортов
#     from printers.models import Printed_pagesModel  # Импортируем здесь для избежания циклических импортов

#     try:

#         print("+"*35)
#         print("Start tasks - datetime: ", datetime.datetime.now())
#         print("-"*35)

#         # Получаем все неархивные записи из Printers_in_serviceModel с учетом объекта обслуживания
#         dataset_printers_in_service = Printers_in_serviceModel.objects.filter(archived=False).filter(service_object_id=id)

#         dataset = []

#         for data_printers_in_service in dataset_printers_in_service:

#             sn_oid = get_data_by_oid(data_printers_in_service.ip_address, data_printers_in_service.printers.sn_oid.oid) #8
#             printed_pages_all_oid = get_data_by_oid(data_printers_in_service.ip_address, data_printers_in_service.printers.printed_pages_all_oid.oid)   #9

#             # проверяем корректность данных
#             errors = ""

#             if data_printers_in_service.serial_number != sn_oid[0]:
#                 errors += 'S/N не равны| '
#             if printed_pages_all_oid[0] == 0 or printed_pages_all_oid[0] == '' or printed_pages_all_oid[0] == None or printed_pages_all_oid[0] =='\x00\x00\x00\x00':
#                 errors += 'printed_pages_error|'

#             # если ошибок нет, записисываем данные в БД
#             if errors == "":
#                 Printed_pagesModel.objects.create(
#                     printers_in_service=data_printers_in_service.id,

#                     service_object_name=data_printers_in_service.service_object.service_object_name,
#                     printers_name=data_printers_in_service.printers.name,
#                     serial_number=data_printers_in_service.serial_number,
#                     ip_address=data_printers_in_service.ip_address,
#                     name_on_print_server = data_printers_in_service.name_on_print_server,
#                     location = data_printers_in_service.location,

#                     printed_pages=int(printed_pages_all_oid[0]))

#             dataset.append(
#                 [
#                     data_printers_in_service.service_object,            #0
#                     data_printers_in_service.serial_number,             #1
#                     data_printers_in_service.printers,                  #2
#                     data_printers_in_service.status_printer,            #3
#                     data_printers_in_service.print_server,              #4
#                     data_printers_in_service.name_on_print_server,      #5
#                     data_printers_in_service.ip_address,                #6
#                     data_printers_in_service.location,                  #7
#                     sn_oid[0],                                          #8
#                     printed_pages_all_oid[0],                           #9
#                     datetime.datetime.now(),                            #10
#                     errors,                                             #11

#                 ]
#                         )

#         print("+"*35)
#         print("End_tasks - datetime: ", datetime.datetime.now())
#         print("+"*35)
#         for data in dataset:
#             print(data)
#         print("-"*35)

#         return f"Функции add_printed_pages_data(id) успешно выполнена."
#     except Exception as ex:
#         return f"Ошибка выполнения функции add_printed_pages_data(id): {ex}"



# def get_data_by_oid(ip, oid):
#     try:
#         response = snmp_get(oid, hostname=ip, community='public', version=1)
#         return response.value
#     except Exception as ex:
#         return f"Ошибка выполнения функции get_data_by_oid(ip, oid): {ex}"



def  printed_pagesModel_objects_create(id, service_object_name, printers_name, serial_number, ip_address,
                                        name_on_print_server, location, printed_pages, error_message):

    from printers.models import Printed_pagesModel  # Импортируем здесь для избежания циклических импортов

    try:
        # записисываем данные в БД
        Printed_pagesModel.objects.create(
                    printers_in_service = id,
                    service_object_name = service_object_name,
                    printers_name = printers_name,
                    serial_number = serial_number,
                    ip_address = ip_address,
                    name_on_print_server = name_on_print_server,
                    location = location,
                    printed_pages = printed_pages,
                    error_message = error_message
                    )
    except Exception as ex:
        return f"Ошибка записи Printed_pagesModel функцией printed_pagesModel_objects_create(...): {ex}"



@shared_task
def get_data_by_oid(ip, sn_oid, printed_pages_all_oid, id_printer):
    try:
        from printers.models import Printed_pagesModel  # Импортируем здесь для избежания циклических импортов
        from printers.models import Printers_in_serviceModel  # Импортируем здесь для избежания циклических импортов

        # Получаем все неархивные записи из Printers_in_serviceModel с учетом объекта обслуживания
        data_printers_in_service = Printers_in_serviceModel.objects.filter(archived=False).filter(id=id_printer)

        try:
            # # sn_oid = get_data_by_oid(data_printers_in_service.ip_address, data_printers_in_service.printers.sn_oid.oid) #8
            response_sn_oid = snmp_get(sn_oid, hostname=ip, community='public', version=1)
            result_sn = response_sn_oid.value#[0]

            # # printed_pages_all_oid = get_data_by_oid(data_printers_in_service.ip_address, data_printers_in_service.printers.printed_pages_all_oid.oid)   #9
            response_printed_pages_all_oid = snmp_get(printed_pages_all_oid, hostname=ip, community='public', version=1)
            result_response_printed_pages_all = response_printed_pages_all_oid.value#[0]

        except Exception as ex:

            printed_pagesModel_objects_create(
                data_printers_in_service[0].id,#printers_in_service =
                data_printers_in_service[0].service_object.service_object_name,#service_object_name =
                data_printers_in_service[0].printers.name,#printers_name =
                data_printers_in_service[0].serial_number,#serial_number =
                data_printers_in_service[0].ip_address,#ip_address =
                data_printers_in_service[0].name_on_print_server,#name_on_print_server =
                data_printers_in_service[0].location,#location =
                0,#printed_pages =
                error_message = "snmp_get errors (ошибка получения данных)"
                )

            return f"Ошибка snmp_get(sn_oid, hostname=ip, community='public', version=1) функции async_get_data_by_oid(ip, sn_oid, printed_pages_all_oid, id_printer): {ex}"

        # print("result_sn: ", result_sn, "| result_response_printed_pages_all: ", result_response_printed_pages_all)

        # проверяем корректность данных
        errors = ""
        if data_printers_in_service[0].serial_number != result_sn:
            errors += f'S/N не равны (S/N oid {result_sn})| '
        if data_printers_in_service[0].ip_address != ip:
            errors += f'ip не равны (S/N oid {ip})| '
        if result_response_printed_pages_all == 0 or result_response_printed_pages_all == '' or result_response_printed_pages_all == None or result_response_printed_pages_all =='\x00\x00\x00\x00':
            errors += 'ошибка получения данных|'
            result_response_printed_pages_all=0


        printed_pagesModel_objects_create(
                data_printers_in_service[0].id,#printers_in_service =
                data_printers_in_service[0].service_object.service_object_name,#service_object_name =
                data_printers_in_service[0].printers.name,#printers_name =
                data_printers_in_service[0].serial_number,#serial_number =
                data_printers_in_service[0].ip_address,#ip_address =
                data_printers_in_service[0].name_on_print_server,#name_on_print_server =
                data_printers_in_service[0].location,#location =
                printed_pages = int(result_response_printed_pages_all), #int(printed_pages_all_oid[0]))
                error_message = errors
                )

        # return str(result_sn) + " | " + str(result_response_printed_pages_all) + " ||| " + errors + " ||| " + str(ip) + " | " + str(sn_oid)+ " | " + str(printed_pages_all_oid)+ " | " + str(id_printer) + " ||| " + str(data_printers_in_service[0])

    except Exception as ex:
        return f"Ошибка выполнения функции async_get_data_by_oid(ip, sn_oid, printed_pages_all_oid, id_printer): {ex}"


def task_service_object_printed_pages():

    # from tasks import get_data_by_oid
    from printers.models import Printers_in_serviceModel

    # Получаем все неархивные записи из Printers_in_serviceModel с учетом объекта обслуживания
    # dataset_printers_in_service = Printers_in_serviceModel.objects.filter(archived=False).filter(service_object_id=id)
    dataset_printers_in_service = Printers_in_serviceModel.objects.filter(archived=False)

    for data_printers_in_service in dataset_printers_in_service:
        # Запускаем асинхронную задачу
        get_data_by_oid.delay(data_printers_in_service.ip_address,
                                data_printers_in_service.printers.sn_oid.oid,
                                data_printers_in_service.printers.printed_pages_all_oid.oid,
                                data_printers_in_service.id)


@shared_task
def printers_task():

    task_service_object_printed_pages()

    logger.info("The \"task_service_object_printed_pages\" just run")
