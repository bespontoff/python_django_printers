from django import template
from django.http import Http404, HttpResponse
import codecs
import csv

register = template.Library()


@register.simple_tag
def export_csv(request, name_colomns, list_rows, name_file='file'):   # def export_csv(request, name_colomns, list_rows, name_file='file'):

    response = HttpResponse(
        content_type='text/csv',
        headers ={"Content-Disposition": f'attachment; filename="{name_file}-export.csv"'},
                            )

    response.write(codecs.BOM_UTF8) #  Экспорт в UTF-8
    csv_writer = csv.writer(response, delimiter = ";")    
    
    csv_writer.writerow(name_colomns)

    for row in list_rows:
        csv_writer.writerow(row)

    return response