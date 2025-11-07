from typing import List, Optional
from datetime import datetime
from models.database import Database
from models.paciente import Paciente
from models.medico import Medico

class Cita:
    """Clase para representar una cita médica"""
    
    def __init__(self, id: int = None, paciente_id: int = None, medico_id: int = None,
                 fecha_hora: str = None, estado: str = "programada", motivo: str = ""):
        self.id = id
        self.paciente_id = paciente_id
        self.medico_id = medico_id
        self.fecha_hora = fecha_hora
        self.estado = estado
        self.motivo = motivo
        self.paciente = None
        self.medico = None
    
    def __str__(self):
        fecha_str = self.fecha_hora.strftime("%Y-%m-%d %H:%M") if isinstance(self.fecha_hora, datetime) else str(self.fecha_hora)
        return f"Cita {self.id}: {fecha_str} - {self.estado}"
    
    def guardar(self, db: Database) -> bool:
        """Guarda la cita en la base de datos"""
        if self.id is None:
            query = """INSERT INTO citas (paciente_id, medico_id, fecha_hora, estado, motivo) 
                       VALUES (%s, %s, %s, %s, %s)"""
            params = (self.paciente_id, self.medico_id, self.fecha_hora, self.estado, self.motivo)
            result = db.execute_query(query, params)
            if result:
                self.id = result
                return True
        else:
            query = """UPDATE citas SET paciente_id=%s, medico_id=%s, fecha_hora=%s, 
                       estado=%s, motivo=%s WHERE id=%s"""
            params = (self.paciente_id, self.medico_id, self.fecha_hora, self.estado, self.motivo, self.id)
            return db.execute_query(query, params) is not None
        return False
    
    def cargar_detalles(self, db: Database):
        """Carga los detalles del paciente y médico"""
        if self.paciente_id and not self.paciente:
            self.paciente = Paciente.buscar_por_id(db, self.paciente_id)
        if self.medico_id and not self.medico:
            self.medico = Medico.buscar_por_id(db, self.medico_id)
    
    @staticmethod
    def obtener_todas(db: Database) -> List['Cita']:
        """Obtiene todas las citas con detalles de paciente y médico"""
        query = """SELECT c.*, p.nombre as paciente_nombre, m.nombre as medico_nombre, 
                          m.especialidad as medico_especialidad
                   FROM citas c
                   LEFT JOIN pacientes p ON c.paciente_id = p.id
                   LEFT JOIN medicos m ON c.medico_id = m.id
                   ORDER BY c.fecha_hora DESC"""
        resultados = db.execute_query(query, fetch=True)
        citas = []
        
        if not resultados:
            return citas
            
        for resultado in resultados:
            cita = Cita(
                id=resultado['id'],
                paciente_id=resultado['paciente_id'],
                medico_id=resultado['medico_id'],
                fecha_hora=resultado['fecha_hora'],
                estado=resultado['estado'],
                motivo=resultado['motivo']
            )
            # ✅ CORREGIDO: Manejo seguro de valores nulos
            cita.paciente = Paciente(
                id=resultado['paciente_id'],
                nombre=resultado.get('paciente_nombre', 'N/A')
            )
            cita.medico = Medico(
                id=resultado['medico_id'],
                nombre=resultado.get('medico_nombre', 'N/A'),
                especialidad=resultado.get('medico_especialidad', 'N/A')
            )
            citas.append(cita)
        return citas
    
    @staticmethod
    def buscar_por_id(db: Database, id: int) -> Optional['Cita']:
        """Busca una cita por ID"""
        query = "SELECT * FROM citas WHERE id = %s"
        resultado = db.execute_query(query, (id,), fetch=True)
        if resultado and len(resultado) > 0:
            return Cita(**resultado[0])
        return None  # ✅ CORREGIDO: Manejo seguro
    
    @staticmethod
    def eliminar(db: Database, id: int) -> bool:
        """Elimina una cita por ID"""
        query = "DELETE FROM citas WHERE id = %s"
        return db.execute_query(query, (id,)) is not None
    
    def cancelar(self, db: Database) -> bool:
        """Cancela la cita"""
        self.estado = "cancelada"
        return self.guardar(db)
    
    def completar(self, db: Database) -> bool:
        """Marca la cita como completada"""
        self.estado = "completada"
        return self.guardar(db)
    
