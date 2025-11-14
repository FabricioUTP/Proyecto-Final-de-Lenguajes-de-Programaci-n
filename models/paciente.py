import mysql.connector
from typing import List, Optional
from models.database import Database

class Paciente:
    """Clase para representar un paciente"""
    
    def __init__(self, id: int = None, nombre: str = "", email: str = "", 
                 telefono: str = "", fecha_nacimiento: str = None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.fecha_nacimiento = fecha_nacimiento
    
    def __str__(self):
        return f"Paciente {self.id}: {self.nombre} ({self.email})"
    
    def guardar(self, db: Database) -> bool:
        """Guarda el paciente en la base de datos"""
        try:
            if self.id is None:
                query = """INSERT INTO pacientes (id,nombre, email, telefono, fecha_nacimiento) 
                           VALUES (%s,%s, %s, %s, %s)"""
                params = (self.id, self.nombre, self.email, self.telefono, self.fecha_nacimiento)
                result = db.execute_query(query, params)
                if result:
                    self.id = result
                    return True
            else:
                query = """UPDATE pacientes SET nombre=%s, email=%s, telefono=%s, 
                           fecha_nacimiento=%s WHERE id=%s"""
                params = (self.nombre, self.email, self.telefono, self.fecha_nacimiento, self.id)
                return db.execute_query(query, params) is not None
            return False
        except mysql.connector.Error as e:
            if e.errno == 1062:  # MySQL error code for duplicate entry
                print("❌ Error: Ya existe un paciente con ese email o teléfono")
            else:
                print(f"❌ Error de base de datos: {e}")
            return False
    
    @staticmethod
    def obtener_todos(db: Database) -> List['Paciente']:
        """Obtiene todos los pacientes"""
        query = "SELECT * FROM pacientes ORDER BY nombre"
        resultados = db.execute_query(query, fetch=True)
        return [Paciente(**paciente) for paciente in resultados] if resultados else []
    
    @staticmethod
    def buscar_por_id(db: Database, id: int) -> Optional['Paciente']:
        """Busca un paciente por ID"""
        query = "SELECT * FROM pacientes WHERE id = %s"
        resultado = db.execute_query(query, (id,), fetch=True)
        return Paciente(**resultado[0]) if resultado else None
    
    @staticmethod
    def eliminar(db: Database, id: int) -> bool:
        """Elimina un paciente por ID"""
        query = "DELETE FROM pacientes WHERE id = %s"
        return db.execute_query(query, (id,)) is not None