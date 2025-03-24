
import sqlite3
import sys
import pathlib

try:
    script_dir = pathlib.Path(sys.argv[0]).parent
    db_file = script_dir / 'db.sqlite3'

    # sqlite_connection = sqlite3.connect('db.sqlite3')
    sqlite_connection = sqlite3.connect(db_file)
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")   

    sqlite_insert_query_update = """UPDATE printers_printers_in_servicemodel
                            SET service_object_id = 1;"""
    
    
    
            
    count = cursor.execute(sqlite_insert_query_update)
    sqlite_connection.commit()
    print("Запись успешно вставлена ​​в таблицу", cursor.rowcount)        

    cursor.close()      
    
except sqlite3.Error as error:
    print("Ошибка при работе с SQLite", error)
finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")