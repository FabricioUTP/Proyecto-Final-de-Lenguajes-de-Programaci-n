import mysql.connector
from config.database_config import DB_CONFIG

class Database:
    """Clase para manejar la conexión a la base de datos"""
    
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            return True
        except mysql.connector.Error as e:
            print(f"❌ Error conectando a la base de datos: {e}")
            return False
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = False):
        """Ejecuta una consulta en la base de datos"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
            else:
                self.connection.commit()
                result = cursor.lastrowid
            
            cursor.close()
            return result
        except mysql.connector.Error as e:
            print(f"❌ Error en la consulta: {e}")
            return None
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        if self.connection:
            self.connection.close()