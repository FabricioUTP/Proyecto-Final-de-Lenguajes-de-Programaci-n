from services.cita_service import CitaService
from services.paciente_service import PacienteService
from services.medico_service import MedicoService
from models.cita import Cita
from ui.menus import *

def gestionar_citas(cita_service: CitaService, paciente_service: PacienteService, medico_service: MedicoService):
    """Interfaz de usuario para gestión de citas"""
    while True:
        mostrar_menu_citas()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            programar_cita(cita_service, paciente_service, medico_service)
        elif opcion == "2":
            listar_todas_citas(cita_service)
        elif opcion == "3":
            buscar_cita_por_id(cita_service)
        elif opcion == "4":
            listar_citas_pendientes(cita_service)
        elif opcion == "5":
            listar_proximas_citas(cita_service)
        elif opcion == "6":
            filtrar_citas_por_medico(cita_service)
        elif opcion == "7":
            filtrar_citas_por_paciente(cita_service)
        elif opcion == "8":
            filtrar_citas_por_fecha(cita_service)
        elif opcion == "9":
            filtrar_citas_por_estado(cita_service)
        elif opcion == "10":
            cancelar_cita(cita_service)
        elif opcion == "11":
            completar_cita(cita_service)
        elif opcion == "12":
            eliminar_cita(cita_service)
        elif opcion == "13":
            verificar_disponibilidad_medico(cita_service, medico_service)
        elif opcion == "14":
            break
        else:
            mostrar_mensaje_error("Opción inválida")
        
        pausar()

def programar_cita(cita_service: CitaService, paciente_service: PacienteService, medico_service: MedicoService):
    """Programa una nueva cita"""
    mostrar_encabezado("programar nueva cita")
    
    try:
        # Mostrar pacientes disponibles
        pacientes = paciente_service.obtener_todos_pacientes()
        if not pacientes:
            mostrar_mensaje_error("No hay pacientes registrados")
            return
        
        print("👥 Pacientes disponibles:")
        for paciente in pacientes:
            print(f"  ID: {paciente.id} | {paciente.nombre}")
        
        # Mostrar médicos disponibles
        medicos = medico_service.obtener_todos_medicos()
        if not medicos:
            mostrar_mensaje_error("No hay médicos registrados")
            return
        
        print("\n🩺 Médicos disponibles:")
        for medico in medicos:
            print(f"  ID: {medico.id} | Dr. {medico.nombre} - {medico.especialidad or 'Sin especialidad'}")
        
        # Solicitar datos
        paciente_id = int(input("\nID del paciente: "))
        medico_id = int(input("ID del médico: "))
        fecha_hora = input("Fecha y hora (YYYY-MM-DD HH:MM): ").strip()
        motivo = input("Motivo de la cita: ").strip()
        
        if not fecha_hora or not motivo:
            mostrar_mensaje_error("Fecha/hora y motivo son obligatorios")
            return
        
        # Verificar disponibilidad
        if not cita_service.verificar_disponibilidad_medico(medico_id, fecha_hora):
            mostrar_mensaje_error("El médico no está disponible en esa fecha/hora")
            return
        
        cita = cita_service.crear_cita(paciente_id, medico_id, fecha_hora, motivo)
        if cita:
            mostrar_mensaje_exito(f"Cita programada exitosamente con ID: {cita.id}")
    
    except ValueError:
        mostrar_mensaje_error("IDs deben ser números válidos")
    except Exception as e:
        mostrar_mensaje_error(f"Error al programar cita: {e}")

def listar_todas_citas(cita_service: CitaService):
    """Lista todas las citas"""
    mostrar_encabezado("lista de todas las citas")
    
    citas = cita_service.obtener_todas_citas()
    
    if not citas:
        mostrar_mensaje_info("No hay citas registradas")
        return
    
    print(f"📅 Total de citas: {len(citas)}")
    mostrar_lista_citas(citas, cita_service)

def buscar_cita_por_id(cita_service: CitaService):
    """Busca una cita por ID"""
    mostrar_encabezado("buscar cita por id")
    
    try:
        cita_id = int(input("ID de la cita: "))
        cita = cita_service.obtener_cita_por_id(cita_id)
        
        if cita:
            cita.cargar_detalles(cita_service.db)
            mostrar_detalles_cita(cita)
        else:
            mostrar_mensaje_error("Cita no encontrada")
    
    except ValueError:
        mostrar_mensaje_error("ID debe ser un número válido")

def listar_citas_pendientes(cita_service: CitaService):
    """Lista citas pendientes"""
    mostrar_encabezado("citas pendientes")
    
    citas = cita_service.obtener_citas_pendientes()
    
    if not citas:
        mostrar_mensaje_info("No hay citas pendientes")
        return
    
    print(f"⏳ Citas pendientes: {len(citas)}")
    mostrar_lista_citas(citas, cita_service)

def listar_proximas_citas(cita_service: CitaService):
    """Lista próximas citas (7 días)"""
    mostrar_encabezado("próximas citas (7 días)")
    
    citas = cita_service.obtener_proximas_citas(dias=7)
    
    if not citas:
        mostrar_mensaje_info("No hay citas programadas para los próximos 7 días")
        return
    
    print(f"🔜 Próximas citas: {len(citas)}")
    mostrar_lista_citas(citas, cita_service)

def filtrar_citas_por_medico(cita_service: CitaService):
    """Filtra citas por médico"""
    mostrar_encabezado("filtrar citas por médico")
    
    try:
        medico_id = int(input("ID del médico: "))
        citas = cita_service.filtrar_citas_por_medico(medico_id)
        
        if not citas:
            mostrar_mensaje_info("No se encontraron citas para este médico")
            return
        
        print(f"📋 Citas del médico (ID: {medico_id}): {len(citas)}")
        mostrar_lista_citas(citas, cita_service)
    
    except ValueError:
        mostrar_mensaje_error("ID debe ser un número válido")

def filtrar_citas_por_paciente(cita_service: CitaService):
    """Filtra citas por paciente"""
    mostrar_encabezado("filtrar citas por paciente")
    
    try:
        paciente_id = int(input("ID del paciente: "))
        citas = cita_service.filtrar_citas_por_paciente(paciente_id)
        
        if not citas:
            mostrar_mensaje_info("No se encontraron citas para este paciente")
            return
        
        print(f"📋 Citas del paciente (ID: {paciente_id}): {len(citas)}")
        mostrar_lista_citas(citas, cita_service)
    
    except ValueError:
        mostrar_mensaje_error("ID debe ser un número válido")

def filtrar_citas_por_fecha(cita_service: CitaService):
    """Filtra citas por fecha"""
    mostrar_encabezado("filtrar citas por fecha")
    
    fecha = input("Fecha (YYYY-MM-DD): ").strip()
    if not fecha:
        mostrar_mensaje_error("Debe ingresar una fecha")
        return
    
    citas = cita_service.filtrar_citas_por_fecha(fecha)
    
    if not citas:
        mostrar_mensaje_info(f"No hay citas programadas para {fecha}")
        return
    
    print(f"📅 Citas para {fecha}: {len(citas)}")
    mostrar_lista_citas(citas, cita_service)

def filtrar_citas_por_estado(cita_service: CitaService):
    """Filtra citas por estado"""
    mostrar_encabezado("filtrar citas por estado")
    
    print("Estados disponibles: programada, completada, cancelada")
    estado = input("Estado: ").strip().lower()
    
    if estado not in ['programada', 'completada', 'cancelada']:
        mostrar_mensaje_error("Estado inválido")
        return
    
    citas = cita_service.filtrar_citas_por_estado(estado)
    
    if not citas:
        mostrar_mensaje_info(f"No hay citas con estado '{estado}'")
        return
    
    print(f"📊 Citas {estado}: {len(citas)}")
    mostrar_lista_citas(citas, cita_service)

def cancelar_cita(cita_service: CitaService):
    """Cancela una cita"""
    mostrar_encabezado("cancelar cita")
    
    try:
        cita_id = int(input("ID de la cita a cancelar: "))
        
        if cita_service.cancelar_cita(cita_id):
            mostrar_mensaje_exito("Cita cancelada exitosamente")
        else:
            mostrar_mensaje_error("Error al cancelar cita o cita no encontrada")
    
    except ValueError:
        mostrar_mensaje_error("ID debe ser un número válido")

def completar_cita(cita_service: CitaService):
    """Marca una cita como completada"""
    mostrar_encabezado("completar cita")
    
    try:
        cita_id = int(input("ID de la cita a completar: "))
        
        if cita_service.completar_cita(cita_id):
            mostrar_mensaje_exito("Cita marcada como completada")
        else:
            mostrar_mensaje_error("Error al completar cita o cita no encontrada")
    
    except ValueError:
        mostrar_mensaje_error("ID debe ser un número válido")

def eliminar_cita(cita_service: CitaService):
    """Elimina una cita"""
    mostrar_encabezado("eliminar cita")
    
    try:
        cita_id = int(input("ID de la cita a eliminar: "))
        cita = cita_service.obtener_cita_por_id(cita_id)
        
        if not cita:
            mostrar_mensaje_error("Cita no encontrada")
            return
        
        mostrar_detalles_cita(cita)
        confirmar = input("\n⚠️  ¿Está seguro de que desea eliminar esta cita? (s/n): ").strip().lower()
        
        if confirmar == 's':
            if cita_service.eliminar_cita(cita_id):
                mostrar_mensaje_exito("Cita eliminada exitosamente")
            else:
                mostrar_mensaje_error("Error al eliminar cita")
        else:
            mostrar_mensaje_info("Eliminación cancelada")
    
    except ValueError:
        mostrar_mensaje_error("ID debe ser un número válido")

def verificar_disponibilidad_medico(cita_service: CitaService, medico_service: MedicoService):
    """Verifica disponibilidad de un médico"""
    mostrar_encabezado("verificar disponibilidad de médico")
    
    try:
        medico_id = int(input("ID del médico: "))
        fecha_hora = input("Fecha y hora a verificar (YYYY-MM-DD HH:MM): ").strip()
        
        disponible = cita_service.verificar_disponibilidad_medico(medico_id, fecha_hora)
        
        if disponible:
            mostrar_mensaje_exito("El médico está disponible en esa fecha/hora")
        else:
            mostrar_mensaje_error("El médico NO está disponible en esa fecha/hora")
    
    except ValueError:
        mostrar_mensaje_error("ID debe ser un número válido")

def mostrar_lista_citas(citas, cita_service: CitaService):
    """Muestra una lista formateada de citas"""
    print("\n" + "="*120)
    print(f"{'ID':<4} {'FECHA/HORA':<16} {'PACIENTE':<20} {'MÉDICO':<20} {'ESPECIALIDAD':<15} {'ESTADO':<12} {'MOTIVO'}")
    print("="*120)
    
    for cita in citas:
        cita.cargar_detalles(cita_service.db)
        fecha_str = cita.fecha_hora.strftime("%Y-%m-%d %H:%M") if cita.fecha_hora else 'N/A'
        paciente_nombre = cita.paciente.nombre if cita.paciente else 'N/A'
        medico_nombre = cita.medico.nombre if cita.medico else 'N/A'
        especialidad = cita.medico.especialidad if cita.medico else 'N/A'
        
        # Emoji según estado
        estado_emoji = "⏳" if cita.estado == "programada" else "✅" if cita.estado == "completada" else "❌"
        
        print(f"{cita.id:<4} {fecha_str:<16} {paciente_nombre:<20} {medico_nombre:<20} {especialidad:<15} {estado_emoji} {cita.estado:<9} {cita.motivo}")

def mostrar_detalles_cita(cita: Cita):
    """Muestra los detalles completos de una cita"""
    print("\n" + "="*60)
    print("📅 DETALLES DE LA CITA")
    print("="*60)
    print(f"ID: {cita.id}")
    print(f"Fecha y hora: {cita.fecha_hora}")
    print(f"Estado: {cita.estado}")
    print(f"Motivo: {cita.motivo}")
    
    if cita.paciente:
        print(f"\n👤 Paciente:")
        print(f"  • ID: {cita.paciente.id}")
        print(f"  • Nombre: {cita.paciente.nombre}")
        print(f"  • Email: {cita.paciente.email or 'N/A'}")
    
    if cita.medico:
        print(f"\n🩺 Médico:")
        print(f"  • ID: {cita.medico.id}")
        print(f"  • Nombre: Dr. {cita.medico.nombre}")
        print(f"  • Especialidad: {cita.medico.especialidad or 'N/A'}")
    
    print("="*60)