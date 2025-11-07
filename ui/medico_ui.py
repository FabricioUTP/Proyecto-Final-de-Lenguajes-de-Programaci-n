from services.medico_service import MedicoService
from models.medico import Medico
from ui.menus import *

def gestionar_medicos(medico_service: MedicoService):
    """Interfaz de usuario para gestión de médicos"""
    while True:
        mostrar_menu_medicos()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            registrar_medico(medico_service)
        elif opcion == "2":
            listar_medicos(medico_service)
        elif opcion == "3":
            buscar_medico_por_id(medico_service)
        elif opcion == "4":
            buscar_medico_por_nombre(medico_service)
        elif opcion == "5":
            buscar_medico_por_especialidad(medico_service)
        elif opcion == "6":
            actualizar_medico(medico_service)
        elif opcion == "7":
            eliminar_medico(medico_service)
        elif opcion == "8":
            ver_disponibilidad_medico(medico_service)
        elif opcion == "9":
            break
        else:
            mostrar_mensaje_error("Opción inválida")
        
        pausar()

def registrar_medico(medico_service: MedicoService):
    """Registra un nuevo médico"""
    mostrar_encabezado("registrar nuevo médico")
    
    try:
        nombre = input("Nombre completo: ").strip()
        if not nombre:
            mostrar_mensaje_error("El nombre es obligatorio")
            return
        
        especialidad = input("Especialidad: ").strip()
        telefono = input("Teléfono: ").strip()
        email = input("Email: ").strip()
        
        medico = medico_service.crear_medico(nombre, especialidad, telefono, email)
        if medico:
            mostrar_mensaje_exito(f"Médico '{nombre}' registrado con ID: {medico.id}")
    
    except Exception as e:
        mostrar_mensaje_error(f"Error al registrar médico: {e}")

def listar_medicos(medico_service: MedicoService):
    """Lista todos los médicos"""
    mostrar_encabezado("lista de médicos")
    
    medicos = medico_service.obtener_todos_medicos()
    
    if not medicos:
        mostrar_mensaje_info("No hay médicos registrados")
        return
    
    print(f"🩺 Total de médicos: {len(medicos)}")
    print("\n" + "="*90)
    print(f"{'ID':<4} {'NOMBRE':<25} {'ESPECIALIDAD':<20} {'EMAIL':<25} {'TELÉFONO':<15}")
    print("="*90)
    
    for medico in medicos:
        print(f"{medico.id:<4} {medico.nombre:<25} {medico.especialidad or 'N/A':<20} {medico.email or 'N/A':<25} {medico.telefono or 'N/A':<15}")

def buscar_medico_por_id(medico_service: MedicoService):
    """Busca un médico por ID"""
    mostrar_encabezado("buscar médico por id")
    
    try:
        medico_id = int(input("ID del médico: "))
        medico = medico_service.obtener_medico_por_id(medico_id)
        
        if medico:
            mostrar_detalles_medico(medico)
        else:
            mostrar_mensaje_error("Médico no encontrado")
    
    except ValueError:
        mostrar_mensaje_error("ID debe ser un número válido")

def buscar_medico_por_nombre(medico_service: MedicoService):
    """Busca médicos por nombre"""
    mostrar_encabezado("buscar médico por nombre")
    
    nombre = input("Nombre a buscar: ").strip()
    if not nombre:
        mostrar_mensaje_error("Debe ingresar un nombre para buscar")
        return
    
    medicos = medico_service.buscar_medicos_por_nombre(nombre)
    
    if not medicos:
        mostrar_mensaje_info("No se encontraron médicos con ese nombre")
        return
    
    print(f"🔍 Se encontraron {len(medicos)} médicos:")
    for medico in medicos:
        print(f"  • ID: {medico.id} | Dr. {medico.nombre} | {medico.especialidad or 'Sin especialidad'}")

def buscar_medico_por_especialidad(medico_service: MedicoService):
    """Busca médicos por especialidad"""
    mostrar_encabezado("buscar médico por especialidad")
    
    # Mostrar especialidades disponibles
    especialidades = medico_service.obtener_especialidades_disponibles()
    if especialidades:
        print("Especialidades disponibles:")
        for esp in especialidades:
            print(f"  • {esp}")
        print()
    
    especialidad = input("Especialidad a buscar: ").strip()
    if not especialidad:
        mostrar_mensaje_error("Debe ingresar una especialidad")
        return
    
    medicos = medico_service.buscar_medicos_por_especialidad(especialidad)
    
    if not medicos:
        mostrar_mensaje_info("No se encontraron médicos con esa especialidad")
        return
    
    print(f"🔍 Se encontraron {len(medicos)} médicos en {especialidad}:")
    for medico in medicos:
        print(f"  • ID: {medico.id} | Dr. {medico.nombre} | Tel: {medico.telefono or 'N/A'}")

def actualizar_medico(medico_service: MedicoService):
    """Actualiza los datos de un médico"""
    mostrar_encabezado("actualizar médico")
    
    try:
        medico_id = int(input("ID del médico a actualizar: "))
        medico = medico_service.obtener_medico_por_id(medico_id)
        
        if not medico:
            mostrar_mensaje_error("Médico no encontrado")
            return
        
        mostrar_detalles_medico(medico)
        print("\n💡 Deje en blanco los campos que no desea cambiar")
        
        nombre = input(f"Nuevo nombre [{medico.nombre}]: ").strip()
        especialidad = input(f"Nueva especialidad [{medico.especialidad or 'Sin especialidad'}]: ").strip()
        telefono = input(f"Nuevo teléfono [{medico.telefono or 'Sin teléfono'}]: ").strip()
        email = input(f"Nuevo email [{medico.email or 'Sin email'}]: ").strip()
        
        # Preparar campos a actualizar
        campos_actualizar = {}
        if nombre: campos_actualizar['nombre'] = nombre
        if especialidad: campos_actualizar['especialidad'] = especialidad
        if telefono: campos_actualizar['telefono'] = telefono
        if email: campos_actualizar['email'] = email
        
        if campos_actualizar and medico_service.actualizar_medico(medico_id, **campos_actualizar):
            mostrar_mensaje_exito("Médico actualizado exitosamente")
        else:
            mostrar_mensaje_info("No se realizaron cambios")
    
    except ValueError:
        mostrar_mensaje_error("ID debe ser un número válido")

def eliminar_medico(medico_service: MedicoService):
    """Elimina un médico"""
    mostrar_encabezado("eliminar médico")
    
    try:
        medico_id = int(input("ID del médico a eliminar: "))
        medico = medico_service.obtener_medico_por_id(medico_id)
        
        if not medico:
            mostrar_mensaje_error("Médico no encontrado")
            return
        
        mostrar_detalles_medico(medico)
        
        confirmar = input("\n⚠️  ¿Está seguro de que desea eliminar este médico? (s/n): ").strip().lower()
        if confirmar == 's':
            if medico_service.eliminar_medico(medico_id):
                mostrar_mensaje_exito("Médico eliminado exitosamente")
            else:
                mostrar_mensaje_error("Error al eliminar médico")
        else:
            mostrar_mensaje_info("Eliminación cancelada")
    
    except ValueError:
        mostrar_mensaje_error("ID debe ser un número válido")

def ver_disponibilidad_medico(medico_service: MedicoService):
    """Muestra la disponibilidad de un médico"""
    mostrar_encabezado("disponibilidad del médico")
    
    try:
        medico_id = int(input("ID del médico: "))
        disponibilidad = medico_service.obtener_disponibilidad_medico(medico_id)
        
        if not disponibilidad:
            mostrar_mensaje_error("Médico no encontrado")
            return
        
        medico = disponibilidad['medico']
        print(f"\n📊 Disponibilidad del Dr. {medico.nombre} ({medico.especialidad}):")
        print("="*50)
        print(f"Total de citas: {disponibilidad['total_citas']}")
        print(f"Citas pendientes: {disponibilidad['citas_pendientes']}")
        print(f"Citas completadas: {disponibilidad['citas_completadas']}")
        print(f"Citas canceladas: {disponibilidad['citas_canceladas']}")
        
        # Mostrar médicos más ocupados
        medicos_ocupados = medico_service.obtener_medicos_mas_ocupados(limite=5)
        if medicos_ocupados:
            print(f"\n🏆 Top 5 médicos más ocupados:")
            for i, item in enumerate(medicos_ocupados, 1):
                ocupado = "🔴" if item['citas_pendientes'] > 10 else "🟡" if item['citas_pendientes'] > 5 else "🟢"
                print(f"   {ocupado} {i}. {item['medico'].nombre}: {item['citas_pendientes']} citas pendientes")
    
    except ValueError:
        mostrar_mensaje_error("ID debe ser un número válido")

def mostrar_detalles_medico(medico: Medico):
    """Muestra los detalles completos de un médico"""
    print("\n" + "="*50)
    print("🩺 DETALLES DEL MÉDICO")
    print("="*50)
    print(f"ID: {medico.id}")
    print(f"Nombre: Dr. {medico.nombre}")
    print(f"Especialidad: {medico.especialidad or 'No especificada'}")
    print(f"Email: {medico.email or 'No especificado'}")
    print(f"Teléfono: {medico.telefono or 'No especificado'}")
    print("="*50)