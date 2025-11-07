from typing import List, Dict, Optional
from datetime import datetime, timedelta
from models.database import Database
from models.cita import Cita
from models.paciente import Paciente
from models.medico import Medico

class CitaService:
    """Servicio para operaciones de citas con programación funcional"""
    
    def __init__(self, db: Database):
        self.db = db
    
    # === OPERACIONES CRUD ===
    
    def crear_cita(self, paciente_id: int, medico_id: int, fecha_hora: str, motivo: str) -> Optional[Cita]:
        """Crea una nueva cita médica"""
        try:
            # Verificar que paciente y médico existen
            paciente = Paciente.buscar_por_id(self.db, paciente_id)
            medico = Medico.buscar_por_id(self.db, medico_id)
            
            if not paciente:
                print("❌ Paciente no encontrado")
                return None
            if not medico:
                print("❌ Médico no encontrado")
                return None
            
            # Crear y guardar cita
            cita = Cita(
                paciente_id=paciente_id,
                medico_id=medico_id,
                fecha_hora=fecha_hora,
                motivo=motivo,
                estado="programada"
            )
            
            if cita.guardar(self.db):
                print("✅ Cita creada exitosamente")
                return cita
            else:
                print("❌ Error al crear la cita")
                return None
                
        except Exception as e:
            print(f"❌ Error al crear cita: {e}")
            return None
    
    def obtener_cita_por_id(self, cita_id: int) -> Optional[Cita]:
        """Obtiene una cita por su ID"""
        return Cita.buscar_por_id(self.db, cita_id)
    
    def obtener_todas_citas(self) -> List[Cita]:
        """Obtiene todas las citas"""
        return Cita.obtener_todas(self.db)
    
    def actualizar_cita(self, cita_id: int, **kwargs) -> bool:
        """Actualiza una cita existente"""
        cita = Cita.buscar_por_id(self.db, cita_id)
        if not cita:
            print("❌ Cita no encontrada")
            return False
        
        # Actualizar campos permitidos
        campos_permitidos = ['fecha_hora', 'motivo', 'estado']
        for campo, valor in kwargs.items():
            if campo in campos_permitidos and hasattr(cita, campo):
                setattr(cita, campo, valor)
        
        return cita.guardar(self.db)
    
    def eliminar_cita(self, cita_id: int) -> bool:
        """Elimina una cita"""
        return Cita.eliminar(self.db, cita_id)
    
    # === PROGRAMACIÓN FUNCIONAL ===
    
    def filtrar_citas_por_estado(self, estado: str) -> List[Cita]:
        """Filtra citas por estado usando filter()"""
        todas_citas = Cita.obtener_todas(self.db)
        return list(filter(lambda cita: cita.estado == estado, todas_citas))
    
    def filtrar_citas_por_medico(self, medico_id: int) -> List[Cita]:
        """Filtra citas por médico usando filter()"""
        todas_citas = Cita.obtener_todas(self.db)
        return list(filter(lambda cita: cita.medico_id == medico_id, todas_citas))
    
    def filtrar_citas_por_paciente(self, paciente_id: int) -> List[Cita]:
        """Filtra citas por paciente usando filter()"""
        todas_citas = Cita.obtener_todas(self.db)
        return list(filter(lambda cita: cita.paciente_id == paciente_id, todas_citas))
    
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
    
    def filtrar_citas_por_rango_fechas(self, fecha_inicio: str, fecha_fin: str) -> List[Cita]:
        """Filtra citas por rango de fechas"""
        try:
            todas_citas = Cita.obtener_todas(self.db)
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin + " 23:59:59", "%Y-%m-%d %H:%M:%S")
            
            return list(filter(
                lambda cita: (
                    cita.fecha_hora and
                    fecha_inicio_dt <= cita.fecha_hora <= fecha_fin_dt
                ),
                todas_citas
            ))
        except ValueError:
            print("❌ Formato de fecha inválido. Use YYYY-MM-DD")
            return []
    
    # === OPERACIONES DE ESTADO ===
    
    def cancelar_cita(self, cita_id: int) -> bool:
        """Cancela una cita"""
        cita = Cita.buscar_por_id(self.db, cita_id)
        if cita:
            return cita.cancelar(self.db)
        return False
    
    def completar_cita(self, cita_id: int) -> bool:
        """Marca una cita como completada"""
        cita = Cita.buscar_por_id(self.db, cita_id)
        if cita:
            return cita.completar(self.db)
        return False
    
    # === CÁLCULOS Y ESTADÍSTICAS ===
    
    def contar_citas_por_estado(self) -> Dict[str, int]:
        """Cuenta citas por estado usando programación funcional"""
        todas_citas = Cita.obtener_todas(self.db)
        
        # Usar map para extraer estados y reducir para contar
        estados = list(map(lambda c: c.estado, todas_citas))
        conteo = {}
        
        for estado in estados:
            conteo[estado] = conteo.get(estado, 0) + 1
        
        return conteo
    
    def calcular_porcentaje_ocupacion(self, medico_id: int, fecha_inicio: str, fecha_fin: str) -> float:
        """Calcula porcentaje de ocupación de un médico"""
        try:
            citas_medico = self.filtrar_citas_por_medico(medico_id)
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
            
            # Filtrar citas en el rango de fechas
            citas_en_rango = list(filter(
                lambda c: (
                    c.fecha_hora and
                    fecha_inicio_dt <= c.fecha_hora.date() <= fecha_fin_dt.date()
                ),
                citas_medico
            ))
            
            # Calcular horas ocupadas (suponiendo 1 hora por cita)
            horas_ocupadas = len(citas_en_rango)
            
            # Calcular días laborales en el rango
            dias_totales = (fecha_fin_dt - fecha_inicio_dt).days + 1
            dias_laborales = dias_totales * 5 / 7  # Aprox 5 días laborales por semana
            horas_totales = dias_laborales * 8  # 8 horas por día
            
            return (horas_ocupadas / horas_totales * 100) if horas_totales > 0 else 0
            
        except ValueError as e:
            print(f"❌ Error en formato de fecha: {e}")
            return 0.0
    
    def verificar_disponibilidad_medico(self, medico_id: int, fecha_hora: str) -> bool:
        """Verifica si un médico está disponible en una fecha/hora específica"""
        try:
            citas_medico = self.filtrar_citas_por_medico(medico_id)
            fecha_consulta = datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M")
            
            # Buscar conflictos de horario
            conflictos = list(filter(
                lambda c: (
                    c.fecha_hora and 
                    c.fecha_hora == fecha_consulta and 
                    c.estado != "cancelada"
                ),
                citas_medico
            ))
            
            return len(conflictos) == 0
        except ValueError:
            print("❌ Formato de fecha/hora inválido")
            return False
    
    def obtener_citas_pendientes(self) -> List[Cita]:
        """Obtiene todas las citas programadas (pendientes)"""
        return self.filtrar_citas_por_estado("programada")
    
    def obtener_proximas_citas(self, dias: int = 7) -> List[Cita]:
        """Obtiene citas programadas para los próximos días"""
        try:
            todas_citas = self.obtener_citas_pendientes()
            fecha_actual = datetime.now()
            fecha_limite = fecha_actual + timedelta(days=dias)
            
            return list(filter(
                lambda cita: (
                    cita.fecha_hora and
                    fecha_actual <= cita.fecha_hora <= fecha_limite
                ),
                todas_citas
            ))
        except Exception as e:
            print(f"❌ Error al obtener próximas citas: {e}")
            return []