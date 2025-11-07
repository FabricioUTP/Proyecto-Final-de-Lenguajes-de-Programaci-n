import mysql.connector
from typing import List, Optional
from models.database import Database

class Medico:
    """Clase para representar un médico"""
    
    def __init__(self, id: int = None, nombre: str = "", especialidad: str = "", 
                 telefono: str = "", email: str = ""):
        self.id = id
        self.nombre = nombre
        self.especialidad = especialidad
        self.telefono = telefono
        self.email = email
    
    def __str__(self):
        return f"Dr. {self.nombre} - {self.especialidad}"
    
    def guardar(self, db: Database) -> bool:
        """Guarda el médico en la base de datos con manejo de errores UNIQUE"""
        try:
            if self.id is None:
                # INSERT para nuevo médico
                query = """INSERT INTO medicos (nombre, especialidad, telefono, email) 
                           VALUES (%s, %s, %s, %s)"""
                params = (self.nombre, self.especialidad, self.telefono, self.email)
                result = db.execute_query(query, params)
                if result:
                    self.id = result
                    print("✅ Médico registrado exitosamente!")
                    return True
                return False
            else:
                # UPDATE para médico existente
                query = """UPDATE medicos SET nombre=%s, especialidad=%s, telefono=%s, 
                           email=%s WHERE id=%s"""
                params = (self.nombre, self.especialidad, self.telefono, self.email, self.id)
                result = db.execute_query(query, params)
                if result is not None:
                    print("✅ Médico actualizado exitosamente!")
                    return True
                return False
                
        except mysql.connector.Error as e:
            # Manejar errores específicos de MySQL
            if e.errno == 1062:  # Error de entrada duplicada
                # Identificar qué campo causó el error
                error_message = str(e).lower()
                if 'email' in error_message:
                    print("❌ Error: Ya existe un médico con ese email")
                elif 'telefono' in error_message:
                    print("❌ Error: Ya existe un médico con ese teléfono")
                else:
                    print("❌ Error: Datos duplicados - ya existe un médico con esa información")
            elif e.errno == 1406:  # Datos muy largos
                print("❌ Error: Los datos exceden la longitud permitida")
            else:
                print(f"❌ Error de base de datos: {e}")
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return False

    @staticmethod
    def obtener_todos(db: Database) -> List['Medico']:
        """Obtiene todos los médicos"""
        query = "SELECT * FROM medicos ORDER BY nombre"
        resultados = db.execute_query(query, fetch=True)
        return [Medico(**medico) for medico in resultados] if resultados else []
    
    @staticmethod
    def buscar_por_id(db: Database, id: int) -> Optional['Medico']:
        """Busca un médico por ID"""
        query = "SELECT * FROM medicos WHERE id = %s"
        resultado = db.execute_query(query, (id,), fetch=True)
        return Medico(**resultado[0]) if resultado else None
    
    @staticmethod
    def buscar_por_especialidad(db: Database, especialidad: str) -> List['Medico']:
        """Busca médicos por especialidad"""
        query = "SELECT * FROM medicos WHERE especialidad LIKE %s ORDER BY nombre"
        resultados = db.execute_query(query, (f"%{especialidad}%",), fetch=True)
        return [Medico(**medico) for medico in resultados] if resultados else []
    
    @staticmethod
    def eliminar(db: Database, id: int) -> bool:
        """Elimina un médico por ID"""
        query = "DELETE FROM medicos WHERE id = %s"
        return db.execute_query(query, (id,)) is not None