def mostrar_menu_principal():
    """Muestra el menú principal del sistema"""
    print("\n" + "="*60)
    print("🏥 SISTEMA DE GESTIÓN MÉDICA")
    print("="*60)
    print("1. 👥 Gestión de Pacientes")
    print("2. 🩺 Gestión de Médicos")
    print("3. 📅 Gestión de Citas")
    print("4. 📊 Reportes y Estadísticas")
    print("5. 🚪 Salir")
    print("="*60)

def mostrar_menu_pacientes():
    """Muestra el menú de gestión de pacientes"""
    print("\n" + "="*50)
    print("👥 GESTIÓN DE PACIENTES")
    print("="*50)
    print("1. Registrar nuevo paciente")
    print("2. Listar todos los pacientes")
    print("3. Buscar paciente por ID")
    print("4. Buscar paciente por nombre")
    print("5. Buscar paciente por email")
    print("6. Actualizar paciente")
    print("7. Eliminar paciente")
    print("8. Ver historial de citas de paciente")
    print("9. Volver al menú principal")
    print("="*50)

def mostrar_menu_medicos():
    """Muestra el menú de gestión de médicos"""
    print("\n" + "="*50)
    print("🩺 GESTIÓN DE MÉDICOS")
    print("="*50)
    print("1. Registrar nuevo médico")
    print("2. Listar todos los médicos")
    print("3. Buscar médico por ID")
    print("4. Buscar médico por nombre")
    print("5. Buscar médico por especialidad")
    print("6. Actualizar médico")
    print("7. Eliminar médico")
    print("8. Ver disponibilidad de médico")
    print("9. Volver al menú principal")
    print("="*50)

def mostrar_menu_citas():
    """Muestra el menú de gestión de citas"""
    print("\n" + "="*50)
    print("📅 GESTIÓN DE CITAS")
    print("="*50)
    print("1. Programar nueva cita")
    print("2. Listar todas las citas")
    print("3. Buscar cita por ID")
    print("4. Listar citas pendientes")
    print("5. Listar próximas citas (7 días)")
    print("6. Filtrar citas por médico")
    print("7. Filtrar citas por paciente")
    print("8. Filtrar citas por fecha")
    print("9. Filtrar citas por estado")
    print("10. Cancelar cita")
    print("11. Completar cita")
    print("12. Eliminar cita")
    print("13. Verificar disponibilidad de médico")
    print("14. Volver al menú principal")
    print("="*50)

def mostrar_menu_reportes():
    """Muestra el menú de reportes y estadísticas"""
    print("\n" + "="*50)
    print("📊 REPORTES Y ESTADÍSTICAS")
    print("="*50)
    print("1. Reporte general de citas")
    print("2. Reporte de citas por médico")
    print("3. Reporte de citas por estado")
    print("4. Reporte de citas por especialidad")
    print("5. Reporte de ocupación de médicos")
    print("6. Tendencias mensuales de citas")
    print("7. Estadísticas generales del sistema")
    print("8. Reporte completo")
    print("9. Exportar reporte a Excel")
    print("10. Volver al menú principal")
    print("="*50)

def mostrar_encabezado(titulo: str):
    """Muestra un encabezado estilizado"""
    print(f"\n⭐ {titulo.upper()} ⭐")
    print("-" * (len(titulo) + 6))

def mostrar_mensaje_exito(mensaje: str):
    """Muestra un mensaje de éxito"""
    print(f"✅ {mensaje}")

def mostrar_mensaje_error(mensaje: str):
    """Muestra un mensaje de error"""
    print(f"❌ {mensaje}")

def mostrar_mensaje_info(mensaje: str):
    """Muestra un mensaje informativo"""
    print(f"ℹ️  {mensaje}")

def mostrar_mensaje_advertencia(mensaje: str):
    """Muestra un mensaje de advertencia"""
    print(f"⚠️  {mensaje}")

def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter"""
    input("\n📝 Presiona Enter para continuar...")