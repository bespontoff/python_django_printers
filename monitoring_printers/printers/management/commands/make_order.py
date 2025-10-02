# import json

# from django.utils import timezone
# from django.core.management.base import BaseCommand, CommandError
# from django_celery_beat.models import PeriodicTask, IntervalSchedule

# from models import *



# class Command(BaseCommand):

#     def add_arguments(self, parser):
#         parser.add_argument('any_argument', type=str)
#         parser.add_argument('anymodel_id', nargs=1, type=int)

#     def handle(self, *args, **options):
#         any_argument = options['any_argument']
#         order = Printers_in_serviceModel.objects.get(pk=options['anymodel_id'][0])

#         if any_argument == 'test_value':
#             PeriodicTask.objects.create(
#                 name='Repeat order {}'.format(options['anymodel_id']),
#                 task='repeat_order_make',
#                 interval=IntervalSchedule.objects.get(every=100, period='seconds'),
#                 args=json.dumps([options['anymodel_id'][0]]),
#                 start_time=timezone.now(),
#             )
#         else:
#             order.update(any_argument=any_argument)
#             order.refresh_from_db()

#             #'any logic'

#             print('success')





#     # def async_service_object_printed_pages_list_view_all_time(request):

#     #     from tasks import get_data_by_oid

#     #     # Получаем все неархивные записи из Printers_in_serviceModel с учетом объекта обслуживания
#     #     # dataset_printers_in_service = Printers_in_serviceModel.objects.filter(archived=False).filter(service_object_id=id)
#     #     dataset_printers_in_service = Printers_in_serviceModel.objects.filter(archived=False)

#     #     for data_printers_in_service in dataset_printers_in_service:
#     #         # Запускаем асинхронную задачу
#     #         get_data_by_oid.delay(data_printers_in_service.ip_address,
#     #                                         data_printers_in_service.printers.sn_oid.oid,
#     #                                         data_printers_in_service.printers.printed_pages_all_oid.oid,
#     #                                         data_printers_in_service.id)

#     #     dataset = Printed_pagesModel.objects.all().order_by('-created')[:500]
#     #     # dataset = Printed_pagesModel.objects.all().order_by('-created')[:100]
#     #     title_text = "Распечатано страниц"

#     #     context = {
#     #             'dataset': dataset,
#     #             'user_login': request.user,
#     #             'title_text':title_text,
#     #             'priznak':'all',
#     #             # 'url_return_to_the_list':'reestr_tmts_list',
#     #         }
#     #     # return render(request, 'printers/service_object_listview.html', context=context)
#     #     return render(request, 'printers/printed_pages_listview.html', context)