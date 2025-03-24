from django.db import models
from django.urls import reverse


class StatusPrintersModel(models.Model):
    status = models.CharField(max_length=50, verbose_name='Статус', unique=True, db_index=True)   
    
    class Meta:
        # db_table='Status_printers' # указание имени таблицы в базе данных "вручную"
        verbose_name_plural = '(1) Статусы'
        verbose_name = 'Статус'
        ordering = ['id','status',]

    def __str__(self):
        return self.status
    

class Print_serversModel(models.Model):
    print_server = models.CharField(max_length=50, verbose_name='print-server', unique=True, db_index=True)

    class Meta:
        verbose_name_plural = '(1) print-servers'
        verbose_name = 'print-server'
        ordering = ['print_server',]
    
    def __str__(self):
        return self.print_server
    
    # def get_absolute_url(self):
    #     return reverse('print-server', kwargs={'id': self.pk})


class CartridgesModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Картридж', unique=True, db_index=True)    

    class Meta:
        verbose_name_plural = '(1) Модели картриджей'
        verbose_name = 'Модель картриджа'
        ordering = ['name',]

    def __str__(self):
        return self.name


class PrintersModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Модель принтера', unique=True, db_index=True)   
    cartridges = models.ManyToManyField('CartridgesModel', blank=True, related_name='cartridges_printers', verbose_name='Модели картриджей')
    sn_oid =  models.ForeignKey('SNMP_OIDModel', blank=True, null=True, on_delete=models.PROTECT, related_name='sn_oid', verbose_name='S/N OID')
    printed_pages_all_oid =  models.ForeignKey('SNMP_OIDModel', blank=True, null=True, on_delete=models.PROTECT, 
                                               related_name='printed_pages_all_oid', verbose_name='Распечатано страниц (всего) OID')

    class Meta:
        verbose_name_plural = '(1) Модели принтеров'
        verbose_name = 'Модель принтера'        
        ordering = ['name',]        

    def __str__(self):
        return self.name
        

class Type_OIDModel(models.Model):    
    type = models.CharField(max_length=100, verbose_name='Type_OID', unique=True)

    class Meta:
        verbose_name_plural = '(1) Type_OID'
        verbose_name = 'Type_OID'
        ordering = ['type',]

    def __str__(self):
        return self.type


class SNMP_OIDModel(models.Model):    
    type_OID = models.ForeignKey('Type_OIDModel', blank=True, null=True, on_delete=models.PROTECT, related_name='type_OID', verbose_name='Type_OID')
    oid = models.CharField(max_length=100, verbose_name='OID', unique=True)

    class Meta:
        verbose_name_plural = '(1) SNMP_OID'
        verbose_name = 'SNMP_OID'
        ordering = ['type_OID', 'oid',]

    def __str__(self):
        return self.type_OID.type + ' | ' + self.oid
    


class Printers_in_serviceModel(models.Model):    
    service_object = models.ForeignKey('Service_objectModel', blank=True, null=True, on_delete=models.PROTECT, verbose_name='Объект_обслуживания')
    serial_number = models.CharField(max_length=50, verbose_name='S/N', db_index=True)
    printers = models.ForeignKey('PrintersModel', on_delete=models.PROTECT, verbose_name='Модель принтера', related_name='printers_fk')
    status_printer = models.ForeignKey('StatusPrintersModel', on_delete=models.PROTECT, verbose_name='Статус', related_name='status_printer_fk')
    print_server = models.ForeignKey('Print_serversModel', blank=True, null=True, on_delete=models.PROTECT, 
                                     verbose_name='print-server', related_name='print_server_fk')
    name_on_print_server = models.CharField(max_length=100, blank=True, null=True, verbose_name='Имя на Print-server')
    ip_address = models.GenericIPAddressField(verbose_name='IP-address', blank=True, null=True)
    location = models.CharField(max_length=100, verbose_name='Локация/Кабинет')    
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False, verbose_name='Переведен в архив')

    class Meta:
        verbose_name_plural = '(3) Принтеры (учет)'
        verbose_name = 'Принтер (учет)'
        ordering = ['status_printer', 'print_server', 'location', 'printers', 'serial_number',]        
        indexes = [
            models.Index(fields=['serial_number', 'printers']),
        ]

    def __str__(self):
        return self.printers.name + ' | ' + self.serial_number + ' | ' + str(self.ip_address) + ' | ' + self.location
    
    # def get_absolute_url(self):
    #     return reverse('printers:printer_detail',
    #                    args=[self.name])


class Printers_in_service_commentsModel(models.Model):
    printers_in_service = models.ForeignKey('Printers_in_serviceModel', blank=True, null=True, on_delete=models.PROTECT, verbose_name='Принтер (учет)')
    short_description = models.CharField(max_length=100, verbose_name='Краткое описание', default='')    
    comment = models.TextField(verbose_name='Комментарий', default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)    

    class Meta:
        verbose_name_plural = '(3) Принтеры (учет)_Комментарии'
        verbose_name = 'Принтеры (учет)_Комментарий'
        ordering = ['created']
        get_latest_by = 'updated' # поле типа DateField ИЛИ DateTimeField, которое будет взято в расчет при получении 
                           # наиболее поздне/ранней записи  (методы latest() / earliest() вызванные без параметров)
        indexes = [models.Index(fields=['created']),]
    
    def __str__(self):
        return self.short_description + ' | ' + str(self.updated)
    

class Service_objectModel(models.Model):
    service_object_name = models.CharField(max_length=100, verbose_name='Объект_обслуживания', unique=True)
    
    class Meta:
        verbose_name_plural = '(2) Объекты_обслуживания'
        verbose_name = 'Объект_обслуживания'
        ordering = ['service_object_name']        
        indexes = [models.Index(fields=['service_object_name']),]
    
    def __str__(self):
        return self.service_object_name


class Printed_pagesModel(models.Model):
    # printers_in_service = models.ForeignKey('Printers_in_serviceModel', blank=True, null=True, on_delete=models.DO_NOTHING, 
    #                                          verbose_name='Принтер (учет)')#related_name='printers_in_service_fk',
    printers_in_service = models.IntegerField(verbose_name='id принтера',)

    service_object_name = models.CharField(max_length=100, verbose_name='Объект_обслуживания',)
    printers_name = models.CharField(max_length=100, verbose_name='Модель принтера',)
    serial_number = models.CharField(max_length=50, verbose_name='S/N')
    ip_address = models.GenericIPAddressField(verbose_name='IP-address', blank=True, null=True)   
    name_on_print_server = models.CharField(max_length=100, blank=True, null=True, verbose_name='Имя на Print-server')
    location = models.CharField(max_length=100, verbose_name='Локация/Кабинет')

    created = models.DateTimeField(auto_now_add=True, db_index=True) # значение True приводит к тому, что поле становится невидимым и 
                                                                        # необязательным для заполнения на уровне Django
    printed_pages = models.IntegerField(null=True, verbose_name='Распечатано страниц', default=0)
       
    
    class Meta:
        verbose_name_plural = '(4) Распечатано страниц'
        verbose_name = 'Распечатано страниц'
        get_latest_by = 'created' # поле типа DateField ИЛИ DateTimeField, которое будет взято в расчет при получении 
                                    # наиболее поздне/ранней записи  (методы latest() / earliest() вызванные без параметров)
        # ordering = ['created']
        indexes = [models.Index(fields=['created']),]

    def __str__(self):
        return self.printers_name + ' | ' + self.serial_number + ' | ' + self.ip_address + ' | ' + self.printed_pages
        # return self.service_object_name + ' | ' + self.printers_name + ' | ' \
        #         + self.serial_number + ' | ' + self.ip_address + ' | ' + self.name_on_print_server \
        #          + ' | ' + self.created + ' | ' + self.printed_pages





"""
# правильный запрос к БД (не делаются повторные запросы, при наличии связей, запрос один на все объекты)
    # cartridges = Cartridges.objects.select_related("cartridges_printers").prefetch_related("printers").all()
    # select_related("cartridges_printers") - для ForeignKey
    # prefetch_related("cartridges_printers") - для ManyToManyField


В качестве параметров select_related принимает имена ForeignKey/OneToOne полей или related_name поля OneToOne в связанной таблице. 
Также можно передавать имена полей в связанных через отношение внешнего ключа таблицах, например:

Employee.objects.all().select_related("city", "city__country")
# или вот так
Employee.objects.all().select_related("city").select_related("city__country")
# или вот так
Employee.objects.all().select_related("city__country")


В отличие от select_related, prefetch_related загружает связанные объекты отдельным запросом для каждого поля переданного
в качестве параметра и производит связывание объектов внутри python.
Однако prefetch_related можно также использовать там, где мы используем select_related, чтобы загрузить связанные записи используя дополнительный запрос, вместо JOIN.
"""








# class Printer_сartridges(models.Model):    
#     printers = models.ForeignKey('Printers', to_field='name', null=True, on_delete=models.PROTECT, verbose_name='Модель принтера')
#     cartridge = models.ForeignKey('Cartridges', to_field='name', null=True, on_delete=models.PROTECT, verbose_name='Картридж')

#     class Meta:
#         verbose_name_plural = '(1) Принтеры_Картриджи'
#         verbose_name = 'Принтер_Картридж'
#         ordering = ['printers',]

#     def __str__(self):
#         return self.printers.name + ' | ' + self.cartridge.name