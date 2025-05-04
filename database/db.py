import sqlite3

def initialize_db():
    conn = sqlite3.connect('pgc_predicciones.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NO EXISTS 
                   ''')