
import sqlite3
import sys
import pathlib
from openpyxl import load_workbook


try:
    script_dir = pathlib.Path(sys.argv[0]).parent
    db_file = script_dir / 'db.sqlite3'

    # sqlite_connection = sqlite3.connect('db.sqlite3')
    sqlite_connection = sqlite3.connect(db_file)
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")

    # sqlite_insert_query = """INSERT INTO printers_printers_in_servicemodel
    #                       (id, serial_number, name_on_print_server, ip_address, location, created, updated, archived, print_server_id, status_printer_id, printers_id)
    #                       VALUES
    #                       (3,'CNB7DB9H2B', 'BB-CUPP_ASUTP_HP LaserJet 400MFP', '10.0.162.5','ЦУПП АСУТП', '2023-11-27 04:46:38.580962', '2023-11-27 08:05:05.793339', 0, 8, 2, 5);"""
    
    sqlite_insert_query = """INSERT INTO printers_printers_in_servicemodel
                          (serial_number, name_on_print_server, ip_address, location, created, updated, archived, print_server_id, status_printer_id, printers_id)
                          VALUES
                          (?,?,?,?,?,?,?,?,?,?);"""
    
    
    wb = load_workbook(script_dir / 'import_data.xlsx')
    sheet = wb['reestr']

    table_data = {}
    index = 1
    for cellObj in sheet['A2':'J44']:        
        tmp_row = []
        for cell in cellObj:            
            if cell.value == '':
                tmp_row.append(None)
            else:
                tmp_row.append(cell.value)

        table_data[index]=tmp_row
        index +=1

    for key, massive_data_row in table_data.items():
        print(key, massive_data_row)        
        count = cursor.execute(sqlite_insert_query, massive_data_row)
        sqlite_connection.commit()
        print("Запись успешно вставлена ​​в таблицу", cursor.rowcount)        

    cursor.close()

       
    

except sqlite3.Error as error:
    print("Ошибка при работе с SQLite", error)
finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")