from typing import Optional
from services.paciente_service import PacienteService
from models.paciente import Paciente
from ui.menus import *

def gestionar_pacientes(paciente_service: PacienteService):
    """Interfaz de usuario para gestión de pacientes"""
    while True:
        mostrar_menu_pacientes()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            registrar_paciente(paciente_service)
        elif opcion == "2":
            listar_pacientes(paciente_service)
        elif opcion == "3":
            buscar_paciente_por_id(paciente_service)
        elif opcion == "4":
            buscar_paciente_por_nombre(paciente_service)
        elif opcion == "5":
            buscar_paciente_por_email(paciente_service)
        elif opcion == "6":
            actualizar_paciente(paciente_service)
        elif opcion == "7":
            eliminar_paciente(paciente_service)
        elif opcion == "8":
            ver_historial_citas_paciente(paciente_service)
        elif opcion == "9":
            break
        else:
            mostrar_mensaje_error("Opción inválida")
        
        pausar()

def registrar_paciente(paciente_service: PacienteService):
    """Registra un nuevo paciente"""
    mostrar_encabezado("registrar nuevo paciente")
    
    try:
        nombre = input("Nombre completo: ").strip()
        if not nombre:
            mostrar_mensaje_error("El nombre es obligatorio")
            return
        
        email = input("Email: ").strip()
        telefono = input("Teléfono: ").strip()
        fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ").strip()
        
        paciente = paciente_service.crear_paciente(nombre, email, telefono, fecha_nacimiento)
        if paciente:
            mostrar_mensaje_exito(f"Paciente '{nombre}' registrado con ID: {paciente.id}")
    
    except Exception as e:
        mostrar_mensaje_error(f"Error al registrar paciente: {e}")

def listar_pacientes(paciente_service: PacienteService):
    """Lista todos los pacientes"""
    mostrar_encabezado("lista de pacientes")
    
    pacientes = paciente_service.obtener_todos_pacientes()
    
    if not pacientes:
        mostrar_mensaje_info("No hay pacientes registrados")
        return
    
    print(f"📋 Total de pacientes: {len(pacientes)}")
    print("\n" + "="*80)
    print(f"{'ID':<4} {'NOMBRE':<25} {'EMAIL':<25} {'TELÉFONO':<15} {'FECHA NAC.'}")
    print("="*80)
    
    for paciente in pacientes:
        fecha_nac = paciente.fecha_nacimiento if paciente.fecha_nacimiento else 'N/A'
        print(f"{paciente.id:<4} {paciente.nombre:<25} {paciente.email or 'N/A':<25} {paciente.telefono or 'N/A':<15} {fecha_nac}")

def buscar_paciente_por_id(paciente_service: PacienteService):
    """Busca un paciente por ID"""
    mostrar_encabezado("buscar paciente por id")
    
    try:
        paciente_id = int(input("ID del paciente: "))
        paciente = paciente_service.obtener_paciente_por_id(paciente_id)
        
        if paciente:
            mostrar_detalles_paciente(paciente)
        else:
            mostrar_mensaje_error("Paciente no encontrado")
    
    except ValueError:
        mostrar_mensaje_error("ID debe ser un número válido")

def buscar_paciente_por_nombre(paciente_service: PacienteService):
    """Busca pacientes por nombre"""
    mostrar_encabezado("buscar paciente por nombre")
    
    nombre = input("Nombre a buscar: ").strip()
    if not nombre:
        mostrar_mensaje_error("Debe ingresar un nombre para buscar")
        return
    
    pacientes = paciente_service.buscar_pacientes_por_nombre(nombre)
    
    if not pacientes:
        mostrar_mensaje_info("No se encontraron pacientes con ese nombre")
        return
    
    print(f"🔍 Se encontraron {len(pacientes)} pacientes:")
    for paciente in pacientes:
        print(f"  • ID: {paciente.id} | {paciente.nombre} | {paciente.email or 'Sin email'}")

def buscar_paciente_por_email(paciente_service: PacienteService):
    """Busca un paciente por email"""
    mostrar_encabezado("buscar paciente por email")
    
    email = input("Email del paciente: ").strip()
    if not email:
        mostrar_mensaje_error("Debe ingresar un email")
        return
    
    paciente = paciente_service.buscar_paciente_por_email(email)
    
    if paciente:
        mostrar_detalles_paciente(paciente)
    else:
        mostrar_mensaje_error("No se encontró ningún paciente con ese email")

def actualizar_paciente(paciente_service: PacienteService):
    """Actualiza los datos de un paciente"""
    mostrar_encabezado("actualizar paciente")
    
    try:
        paciente_id = int(input("ID del paciente a actualizar: "))
        paciente = paciente_service.obtener_paciente_por_id(paciente_id)
        
        if not paciente:
            mostrar_mensaje_error("Paciente no encontrado")
            return
        
        mostrar_detalles_paciente(paciente)
        print("\n💡 Deje en blanco los campos que no desea cambiar")
        
        nombre = input(f"Nuevo nombre [{paciente.nombre}]: ").strip()
        email = input(f"Nuevo email [{paciente.email or 'Sin email'}]: ").strip()
        telefono = input(f"Nuevo teléfono [{paciente.telefono or 'Sin teléfono'}]: ").strip()
        fecha_nacimiento = input(f"Nueva fecha nacimiento [{paciente.fecha_nacimiento or 'Sin fecha'}]: ").strip()
        
        # Preparar campos a actualizar
        campos_actualizar = {}
        if nombre: campos_actualizar['nombre'] = nombre
        if email: campos_actualizar['email'] = email
        if telefono: campos_actualizar['telefono'] = telefono
        if fecha_nacimiento: campos_actualizar['fecha_nacimiento'] = fecha_nacimiento
        
        if campos_actualizar and paciente_service.actualizar_paciente(paciente_id, **campos_actualizar):
            mostrar_mensaje_exito("Paciente actualizado exitosamente")
        else:
            mostrar_mensaje_info("No se realizaron cambios")
    
    except ValueError:
        mostrar_mensaje_error("ID debe ser un número válido")

def eliminar_paciente(paciente_service: PacienteService):
    """Elimina un paciente"""
    mostrar_encabezado("eliminar paciente")
    
    try:
        paciente_id = int(input("ID del paciente a eliminar: "))
        paciente = paciente_service.obtener_paciente_por_id(paciente_id)
        
        if not paciente:
            mostrar_mensaje_error("Paciente no encontrado")
            return
        
        mostrar_detalles_paciente(paciente)
        
        confirmar = input("\n⚠️  ¿Está seguro de que desea eliminar este paciente? (s/n): ").strip().lower()
        if confirmar == 's':
            if paciente_service.eliminar_paciente(paciente_id):
                mostrar_mensaje_exito("Paciente eliminado exitosamente")
            else:
                mostrar_mensaje_error("Error al eliminar paciente")
        else:
            mostrar_mensaje_info("Eliminación cancelada")
    
    except ValueError:
        mostrar_mensaje_error("ID debe ser un número válido")

def ver_historial_citas_paciente(paciente_service: PacienteService):
    """Muestra el historial de citas de un paciente"""
    mostrar_encabezado("historial de citas del paciente")
    
    try:
        paciente_id = int(input("ID del paciente: "))
        paciente = paciente_service.obtener_paciente_por_id(paciente_id)
        
        if not paciente:
            mostrar_mensaje_error("Paciente no encontrado")
            return
        
        historial = paciente_service.obtener_historial_citas_paciente(paciente_id)
        
        if not historial:
            mostrar_mensaje_info("El paciente no tiene citas registradas")
            return
        
        print(f"\n📋 Historial de citas de {paciente.nombre}:")
        print("="*100)
        print(f"{'FECHA/HORA':<16} {'MÉDICO':<20} {'ESPECIALIDAD':<15} {'ESTADO':<12} {'MOTIVO'}")
        print("="*100)
        
        for cita in historial:
            print(f"{cita['fecha_hora']:<16} {cita['medico']:<20} {cita['especialidad']:<15} {cita['estado']:<12} {cita['motivo']}")
    
    except ValueError:
        mostrar_mensaje_error("ID debe ser un número válido")

def mostrar_detalles_paciente(paciente: Paciente):
    """Muestra los detalles completos de un paciente"""
    print("\n" + "="*50)
    print("👤 DETALLES DEL PACIENTE")
    print("="*50)
    print(f"ID: {paciente.id}")
    print(f"Nombre: {paciente.nombre}")
    print(f"Email: {paciente.email or 'No especificado'}")
    print(f"Teléfono: {paciente.telefono or 'No especificado'}")
    print(f"Fecha de nacimiento: {paciente.fecha_nacimiento or 'No especificada'}")
    print("="*50)