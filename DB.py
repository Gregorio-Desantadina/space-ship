import sqlite3
from config import DB_SQL_FILE

def init_db(conexion):
    # Abrir el archivo SQL
    with open(DB_SQL_FILE, 'r') as f:
        sql_script = f.read()

    # Ejecutar el script SQL en la base de datos
    cursor = conexion.cursor()
    cursor.executescript(sql_script)

    # Confirmar los cambios y cerrar la conexión
    conexion.commit()
    




