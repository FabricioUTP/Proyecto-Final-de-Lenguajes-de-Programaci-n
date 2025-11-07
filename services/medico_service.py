from typing import List, Optional, Dict
from models.database import Database
from models.medico import Medico
from models.cita import Cita

class MedicoService:
    """Servicio para operaciones de médicos"""
    
    def __init__(self, db: Database):
        self.db = db
    
    # === OPERACIONES CRUD ===
    
    def crear_medico(self, nombre: str, especialidad: str, telefono: str, email: str) -> Optional[Medico]:
        """Crea un nuevo médico"""
        try:
            medico = Medico(
                nombre=nombre,
                especialidad=especialidad,
                telefono=telefono,
                email=email
            )
            
            if medico.guardar(self.db):
                print("✅ Médico creado exitosamente")
                return medico
            else:
                print("❌ Error al crear médico")
                return None
                
        except Exception as e:
            print(f"❌ Error al crear médico: {e}")
            return None
    
    def obtener_medico_por_id(self, medico_id: int) -> Optional[Medico]:
        """Obtiene un médico por su ID"""
        return Medico.buscar_por_id(self.db, medico_id)
    
    def obtener_todos_medicos(self) -> List[Medico]:
        """Obtiene todos los médicos"""
        return Medico.obtener_todos(self.db)
    
    def actualizar_medico(self, medico_id: int, **kwargs) -> bool:
        """Actualiza un médico existente"""
        medico = Medico.buscar_por_id(self.db, medico_id)
        if not medico:
            print("❌ Médico no encontrado")
            return False
        
        # Actualizar campos permitidos
        campos_permitidos = ['nombre', 'especialidad', 'telefono', 'email']
        for campo, valor in kwargs.items():
            if campo in campos_permitidos and hasattr(medico, campo):
                setattr(medico, campo, valor)
        
        return medico.guardar(self.db)
    
    def eliminar_medico(self, medico_id: int) -> bool:
        """Elimina un médico y sus citas (por CASCADE)"""
        return Medico.eliminar(self.db, medico_id)
    
    # === BÚSQUEDAS Y FILTROS ===
    
    def buscar_medicos_por_nombre(self, nombre: str) -> List[Medico]:
        """Busca médicos por nombre (búsqueda parcial)"""
        todos_medicos = Medico.obtener_todos(self.db)
        return list(filter(
            lambda m: nombre.lower() in m.nombre.lower(),
            todos_medicos
        ))
    
    def buscar_medicos_por_especialidad(self, especialidad: str) -> List[Medico]:
        """Busca médicos por especialidad"""
        return Medico.buscar_por_especialidad(self.db, especialidad)
    
    def buscar_medico_por_email(self, email: str) -> Optional[Medico]:
        """Busca un médico por email exacto"""
        todos_medicos = Medico.obtener_todos(self.db)
        resultados = list(filter(
            lambda m: m.email and m.email.lower() == email.lower(),
            todos_medicos
        ))
        return resultados[0] if resultados else None
    
    def buscar_medico_por_telefono(self, telefono: str) -> Optional[Medico]:
        """Busca un médico por teléfono exacto"""
        todos_medicos = Medico.obtener_todos(self.db)
        resultados = list(filter(
            lambda m: m.telefono and m.telefono == telefono,
            todos_medicos
        ))
        return resultados[0] if resultados else None
    
    # === ESTADÍSTICAS E INFORMES ===
    
    def contar_total_medicos(self) -> int:
        """Cuenta el total de médicos"""
        return len(Medico.obtener_todos(self.db))
    
    def obtener_especialidades_disponibles(self) -> List[str]:
        """Obtiene lista de especialidades únicas"""
        medicos = Medico.obtener_todos(self.db)
        especialidades = list(map(lambda m: m.especialidad, medicos))
        # Usar set para eliminar duplicados y filter para quitar None
        especialidades_unicas = list(set(filter(lambda e: e is not None, especialidades)))
        return sorted(especialidades_unicas)
    
    def obtener_medicos_mas_ocupados(self, limite: int = 5) -> List[Dict]:
        """Obtiene los médicos con más citas programadas"""
        from services.cita_service import CitaService
        cita_service = CitaService(self.db)
        
        todos_medicos = Medico.obtener_todos(self.db)
        citas_pendientes = cita_service.obtener_citas_pendientes()
        
        # Contar citas por médico
        conteo_citas = {}
        for cita in citas_pendientes:
            medico_id = cita.medico_id
            conteo_citas[medico_id] = conteo_citas.get(medico_id, 0) + 1
        
        # Crear lista de médicos con su conteo de citas
        medicos_con_conteo = []
        for medico in todos_medicos:
            conteo = conteo_citas.get(medico.id, 0)
            medicos_con_conteo.append({
                'medico': medico,
                'citas_pendientes': conteo
            })
        
        # Ordenar por número de citas (descendente) y tomar los primeros
        medicos_con_conteo.sort(key=lambda x: x['citas_pendientes'], reverse=True)
        return medicos_con_conteo[:limite]
    
    def obtener_disponibilidad_medico(self, medico_id: int) -> Dict:
        """Obtiene información de disponibilidad de un médico"""
        from services.cita_service import CitaService
        cita_service = CitaService(self.db)
        
        medico = Medico.buscar_por_id(self.db, medico_id)
        if not medico:
            return {}
        
        citas_medico = cita_service.filtrar_citas_por_medico(medico_id)
        citas_pendientes = list(filter(lambda c: c.estado == "programada", citas_medico))
        citas_completadas = list(filter(lambda c: c.estado == "completada", citas_medico))
        citas_canceladas = list(filter(lambda c: c.estado == "cancelada", citas_medico))
        
        return {
            'medico': medico,
            'total_citas': len(citas_medico),
            'citas_pendientes': len(citas_pendientes),
            'citas_completadas': len(citas_completadas),
            'citas_canceladas': len(citas_canceladas)
        }
    
    # === PROGRAMACIÓN FUNCIONAL ===
    
    def obtener_nombres_medicos(self) -> List[str]:
        """Obtiene lista de nombres de médicos usando map()"""
        medicos = Medico.obtener_todos(self.db)
        return list(map(lambda m: m.nombre, medicos))
    
    def obtener_medicos_por_especialidad_grupo(self) -> Dict[str, List[Medico]]:
        """Agrupa médicos por especialidad"""
        medicos = Medico.obtener_todos(self.db)
        grupos = {}
        
        for medico in medicos:
            especialidad = medico.especialidad or 'Sin especialidad'
            if especialidad not in grupos:
                grupos[especialidad] = []
            grupos[especialidad].append(medico)
        
        return grupos
    
    def filtrar_medicos_con_contacto(self) -> List[Medico]:
        """Filtra médicos que tienen email y teléfono"""
        medicos = Medico.obtener_todos(self.db)
        return list(filter(
            lambda m: m.email is not None and m.telefono is not None,
            medicos
        ))