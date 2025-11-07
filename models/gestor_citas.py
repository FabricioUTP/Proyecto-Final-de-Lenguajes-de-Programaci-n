from typing import List
from datetime import datetime
from models.database import Database
from models.cita import Cita
from models.paciente import Paciente
from models.medico import Medico

class GestorCitas:
    """Clase para gestionar operaciones avanzadas de citas"""
    
    def __init__(self, db: Database):
        self.db = db
    
    # === PROGRAMACIÓN FUNCIONAL ===
    
    def filtrar_citas_por_estado(self, estado: str) -> List[Cita]:
        """Filtra citas por estado usando filter()"""
        todas_citas = Cita.obtener_todas(self.db)
        return list(filter(lambda cita: cita.estado == estado, todas_citas))
    
    def filtrar_citas_por_medico(self, medico_id: int) -> List[Cita]:
        """Filtra citas por médico usando filter()"""
        todas_citas = Cita.obtener_todas(self.db)
        return list(filter(lambda cita: cita.medico_id == medico_id, todas_citas))
    
    def filtrar_citas_por_fecha(self, fecha: str) -> List[Cita]:
        """Filtra citas por fecha específica"""
        try:
            todas_citas = Cita.obtener_todas(self.db)
            fecha_target = datetime.strptime(fecha, "%Y-%m-%d").date()
            
            return list(filter(
                lambda cita: (
                    cita.fecha_hora and 
                    isinstance(cita.fecha_hora, datetime) and
                    cita.fecha_hora.date() == fecha_target
                ),
                todas_citas
            ))
        except ValueError:
            print("❌ Formato de fecha inválido. Use YYYY-MM-DD")
            return []
    
    def obtener_citas_pendientes(self) -> List[Cita]:
        """Obtiene citas programadas (pendientes)"""
        return self.filtrar_citas_por_estado("programada")
    
    def calcular_porcentaje_ocupacion(self, medico_id: int, fecha_inicio: str, fecha_fin: str) -> float:
        """Calcula porcentaje de ocupación de un médico"""
        try:
            todas_citas = Cita.obtener_todas(self.db)
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
            
            # Filtrar citas del médico en el rango de fechas
            citas_medico = list(filter(
                lambda c: (
                    c.medico_id == medico_id and 
                    c.fecha_hora and
                    fecha_inicio_dt <= c.fecha_hora <= fecha_fin_dt
                ),
                todas_citas
            ))
            
            # Calcular horas ocupadas (suponiendo 1 hora por cita)
            horas_ocupadas = len(citas_medico)
            
            # Suponiendo 8 horas de trabajo por día, 5 días por semana
            dias_laborales = (fecha_fin_dt - fecha_inicio_dt).days + 1
            dias_laborales_efectivos = dias_laborales * 5 / 7  # Aprox días laborables
            horas_totales = dias_laborales_efectivos * 8
            
            return (horas_ocupadas / horas_totales * 100) if horas_totales > 0 else 0
            
        except ValueError as e:
            print(f"❌ Error en formato de fecha: {e}")
            return 0.0
    
    def obtener_nombres_pacientes(self) -> List[str]:
        """Obtiene nombres de pacientes usando map()"""
        pacientes = Paciente.obtener_todos(self.db)
        return list(map(lambda p: p.nombre, pacientes))
    
    def obtener_especialidades_medicos(self) -> List[str]:
        """Obtiene especialidades únicas de médicos usando map() y set()"""
        medicos = Medico.obtener_todos(self.db)
        especialidades = list(map(lambda m: m.especialidad, medicos))
        return list(set(especialidades))
    
    def contar_citas_por_estado(self) -> dict:
        """Cuenta citas por estado usando programación funcional"""
        todas_citas = Cita.obtener_todas(self.db)
        
        estados = list(map(lambda c: c.estado, todas_citas))
        conteo = {}
        
        for estado in estados:
            conteo[estado] = conteo.get(estado, 0) + 1
        
        return conteo
    
    def verificar_disponibilidad_medico(self, medico_id: int, fecha_hora: str) -> bool:
        """Verifica si un médico está disponible en una fecha/hora específica"""
        citas_medico = self.filtrar_citas_por_medico(medico_id)
        fecha_consulta = datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M")
        
        # Buscar conflictos de horario
        conflictos = list(filter(
            lambda c: (c.fecha_hora == fecha_consulta and c.estado != "cancelada"),
            citas_medico
        ))
        
        return len(conflictos) == 0