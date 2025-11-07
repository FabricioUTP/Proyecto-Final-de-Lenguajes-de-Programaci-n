from services.reportes_service import ReportesService
from services.cita_service import CitaService
from ui.menus import *

def generar_reportes(reportes_service: ReportesService, cita_service: CitaService):
    """Interfaz de usuario para reportes y estadísticas"""
    while True:
        mostrar_menu_reportes()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            reporte_general_citas(reportes_service)
        elif opcion == "2":
            reporte_citas_por_medico(reportes_service)
        elif opcion == "3":
            reporte_citas_por_estado(reportes_service)
        elif opcion == "4":
            reporte_citas_por_especialidad(reportes_service)
        elif opcion == "5":
            reporte_ocupacion_medicos(reportes_service, cita_service)
        elif opcion == "6":
            reporte_tendencias_mensuales(reportes_service)
        elif opcion == "7":
            estadisticas_generales(reportes_service)
        elif opcion == "8":
            reporte_completo(reportes_service)
        elif opcion == "9":
            exportar_reporte_excel(reportes_service)
        elif opcion == "10":
            break
        else:
            mostrar_mensaje_error("Opción inválida")
        
        pausar()

def reporte_general_citas(reportes_service: ReportesService):
    """Genera reporte general de citas"""
    mostrar_encabezado("reporte general de citas")
    reportes_service.generar_reporte_citas_general()

def reporte_citas_por_medico(reportes_service: ReportesService):
    """Genera reporte de citas por médico"""
    mostrar_encabezado("reporte de citas por médico")
    reportes_service.generar_reporte_citas_por_medico(mostrar_grafico=True)

def reporte_citas_por_estado(reportes_service: ReportesService):
    """Genera reporte de citas por estado"""
    mostrar_encabezado("reporte de citas por estado")
    reportes_service.generar_reporte_citas_por_estado(mostrar_grafico=True)

def reporte_citas_por_especialidad(reportes_service: ReportesService):
    """Genera reporte de citas por especialidad"""
    mostrar_encabezado("reporte de citas por especialidad")
    reportes_service.generar_reporte_citas_por_especialidad(mostrar_grafico=True)

def reporte_ocupacion_medicos(reportes_service: ReportesService, cita_service: CitaService):
    """Genera reporte de ocupación de médicos"""
    mostrar_encabezado("reporte de ocupación de médicos")
    
    # Mostrar período por defecto (último mes)
    from datetime import datetime, timedelta
    fecha_fin = datetime.now().strftime("%Y-%m-%d")
    fecha_inicio = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    print(f"📅 Período por defecto: {fecha_inicio} a {fecha_fin}")
    cambiar_periodo = input("¿Desea cambiar el período? (s/n): ").strip().lower()
    
    if cambiar_periodo == 's':
        fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ").strip()
        fecha_fin = input("Fecha fin (YYYY-MM-DD): ").strip()
    
    reportes_service.generar_reporte_ocupacion_medicos(fecha_inicio, fecha_fin)

def reporte_tendencias_mensuales(reportes_service: ReportesService):
    """Genera reporte de tendencias mensuales"""
    mostrar_encabezado("tendencias mensuales de citas")
    reportes_service.generar_reporte_tendencias_mensuales()

def estadisticas_generales(reportes_service: ReportesService):
    """Muestra estadísticas generales del sistema"""
    mostrar_encabezado("estadísticas generales del sistema")
    reportes_service.mostrar_estadisticas_generales()

def reporte_completo(reportes_service: ReportesService):
    """Genera reporte completo con todos los análisis"""
    mostrar_encabezado("reporte completo del sistema")
    reportes_service.generar_reporte_completo()

def exportar_reporte_excel(reportes_service: ReportesService):
    """Exporta reporte a Excel"""
    mostrar_encabezado("exportar reporte a excel")
    
    nombre_archivo = input("Nombre del archivo (sin extensión) [reporte_citas]: ").strip()
    if not nombre_archivo:
        nombre_archivo = "reporte_citas"
    
    if not nombre_archivo.endswith('.xlsx'):
        nombre_archivo += '.xlsx'
    
    reportes_service.exportar_reporte_excel(nombre_archivo)