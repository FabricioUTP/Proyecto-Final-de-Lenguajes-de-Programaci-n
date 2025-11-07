from typing import List, Optional, Dict
from models.database import Database
from models.paciente import Paciente
from models.cita import Cita

class PacienteService:
    """Servicio para operaciones de pacientes"""
    
    def __init__(self, db: Database):
        self.db = db
    
    # === OPERACIONES CRUD ===
    
    def crear_paciente(self, nombre: str, email: str, telefono: str, fecha_nacimiento: str) -> Optional[Paciente]:
        """Crea un nuevo paciente"""
        try:
            paciente = Paciente(
                nombre=nombre,
                email=email,
                telefono=telefono,
                fecha_nacimiento=fecha_nacimiento
            )
            
            if paciente.guardar(self.db):
                print("✅ Paciente creado exitosamente")
                return paciente
            else:
                print("❌ Error al crear paciente")
                return None
                
        except Exception as e:
            print(f"❌ Error al crear paciente: {e}")
            return None
    
    def obtener_paciente_por_id(self, paciente_id: int) -> Optional[Paciente]:
        """Obtiene un paciente por su ID"""
        return Paciente.buscar_por_id(self.db, paciente_id)
    
    def obtener_todos_pacientes(self) -> List[Paciente]:
        """Obtiene todos los pacientes"""
        return Paciente.obtener_todos(self.db)
    
    def actualizar_paciente(self, paciente_id: int, **kwargs) -> bool:
        """Actualiza un paciente existente"""
        paciente = Paciente.buscar_por_id(self.db, paciente_id)
        if not paciente:
            print("❌ Paciente no encontrado")
            return False
        
        # Actualizar campos permitidos
        campos_permitidos = ['nombre', 'email', 'telefono', 'fecha_nacimiento']
        for campo, valor in kwargs.items():
            if campo in campos_permitidos and hasattr(paciente, campo):
                setattr(paciente, campo, valor)
        
        return paciente.guardar(self.db)
    
    def eliminar_paciente(self, paciente_id: int) -> bool:
        """Elimina un paciente y sus citas (por CASCADE)"""
        return Paciente.eliminar(self.db, paciente_id)
    
    # === BÚSQUEDAS Y FILTROS ===
    
    def buscar_pacientes_por_nombre(self, nombre: str) -> List[Paciente]:
        """Busca pacientes por nombre (búsqueda parcial)"""
        todos_pacientes = Paciente.obtener_todos(self.db)
        return list(filter(
            lambda p: nombre.lower() in p.nombre.lower(),
            todos_pacientes
        ))
    
    def buscar_paciente_por_email(self, email: str) -> Optional[Paciente]:
        """Busca un paciente por email exacto"""
        todos_pacientes = Paciente.obtener_todos(self.db)
        resultados = list(filter(
            lambda p: p.email and p.email.lower() == email.lower(),
            todos_pacientes
        ))
        return resultados[0] if resultados else None
    
    def buscar_paciente_por_telefono(self, telefono: str) -> Optional[Paciente]:
        """Busca un paciente por teléfono exacto"""
        todos_pacientes = Paciente.obtener_todos(self.db)
        resultados = list(filter(
            lambda p: p.telefono and p.telefono == telefono,
            todos_pacientes
        ))
        return resultados[0] if resultados else None
    
    # === ESTADÍSTICAS E INFORMES ===
    
    def contar_total_pacientes(self) -> int:
        """Cuenta el total de pacientes"""
        return len(Paciente.obtener_todos(self.db))
    
    def obtener_pacientes_sin_citas(self) -> List[Paciente]:
        """Obtiene pacientes que no tienen citas programadas"""
        from services.cita_service import CitaService
        cita_service = CitaService(self.db)
        
        todos_pacientes = Paciente.obtener_todos(self.db)
        citas_pendientes = cita_service.obtener_citas_pendientes()
        
        # Obtener IDs de pacientes con citas pendientes
        ids_con_citas = set(map(lambda c: c.paciente_id, citas_pendientes))
        
        # Filtrar pacientes que no tienen citas pendientes
        return list(filter(
            lambda p: p.id not in ids_con_citas,
            todos_pacientes
        ))
    
    def obtener_historial_citas_paciente(self, paciente_id: int) -> List[Dict]:
        """Obtiene el historial completo de citas de un paciente"""
        from services.cita_service import CitaService
        cita_service = CitaService(self.db)
        
        citas_paciente = cita_service.filtrar_citas_por_paciente(paciente_id)
        
        # Usar map para transformar las citas en un formato más legible
        return list(map(
            lambda c: {
                'id': c.id,
                'fecha_hora': c.fecha_hora.strftime("%Y-%m-%d %H:%M") if c.fecha_hora else 'N/A',
                'medico': c.medico.nombre if c.medico else 'N/A',
                'especialidad': c.medico.especialidad if c.medico else 'N/A',
                'estado': c.estado,
                'motivo': c.motivo
            },
            citas_paciente
        ))
    
    def obtener_pacientes_recientes(self, dias: int = 30) -> List[Paciente]:
        """Obtiene pacientes registrados en los últimos días"""
        # Nota: Esta función asume que tienes un campo fecha_creacion en la tabla
        # Si no lo tienes, puedes omitir esta función
        todos_pacientes = Paciente.obtener_todos(self.db)
        return todos_pacientes  # Placeholder - implementar cuando haya fecha_creacion
    
    # === PROGRAMACIÓN FUNCIONAL ===
    
    def obtener_nombres_pacientes(self) -> List[str]:
        """Obtiene lista de nombres de pacientes usando map()"""
        pacientes = Paciente.obtener_todos(self.db)
        return list(map(lambda p: p.nombre, pacientes))
    
    def obtener_emails_pacientes(self) -> List[str]:
        """Obtiene lista de emails de pacientes usando map() y filter()"""
        pacientes = Paciente.obtener_todos(self.db)
        emails = list(map(lambda p: p.email, pacientes))
        return list(filter(lambda email: email is not None, emails))
    
    def agrupar_pacientes_por_inicial(self) -> Dict[str, List[Paciente]]:
        """Agrupa pacientes por la inicial de su nombre"""
        pacientes = Paciente.obtener_todos(self.db)
        grupos = {}
        
        for paciente in pacientes:
            inicial = paciente.nombre[0].upper() if paciente.nombre else 'Otros'
            if inicial not in grupos:
                grupos[inicial] = []
            grupos[inicial].append(paciente)
        
        return grupos