"""
SISTEMA DE GESTIÓN MÉDICA
==========================
Sistema completo para gestionar pacientes, médicos y citas médicas.
Implementa POO, programación estructurada y funcional.

Paradigmas aplicados:
- POO: Clases Paciente, Medico, Cita, GestorCitas
- Estructurado: Menús principales y flujo de control
- Funcional: Uso de filter(), map() para operaciones avanzadas
"""

import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import Database
from services.paciente_service import PacienteService
from services.medico_service import MedicoService
from services.cita_service import CitaService
from services.reportes_service import ReportesService
from ui.menus import mostrar_menu_principal, pausar, mostrar_mensaje_exito, mostrar_mensaje_error
from ui.paciente_ui import gestionar_pacientes
from ui.medico_ui import gestionar_medicos
from ui.cita_ui import gestionar_citas
from ui.reportes_ui import generar_reportes

def inicializar_sistema():
    """Inicializa todos los componentes del sistema"""
    print("🔧 INICIALIZANDO SISTEMA...")
    
    # Conectar a la base de datos
    try:
        db = Database()
        if not db.connection:
            mostrar_mensaje_error("No se pudo conectar a la base de datos")
            return None
        
        mostrar_mensaje_exito("Conexión a base de datos establecida")
        
        # Inicializar servicios
        paciente_service = PacienteService(db)
        medico_service = MedicoService(db)
        cita_service = CitaService(db)
        reportes_service = ReportesService(db)
        
        mostrar_mensaje_exito("Servicios inicializados correctamente")
        
        return {
            'db': db,
            'paciente_service': paciente_service,
            'medico_service': medico_service,
            'cita_service': cita_service,
            'reportes_service': reportes_service
        }
        
    except Exception as e:
        mostrar_mensaje_error(f"Error al inicializar el sistema: {e}")
        return None

def mostrar_bienvenida():
    """Muestra mensaje de bienvenida"""
    print("\n" + "="*70)
    print("🏥 BIENVENIDO AL SISTEMA DE GESTIÓN MÉDICA")
    print("="*70)
    print("Sistema completo para la gestión de:")
    print("  • 👥 Pacientes")
    print("  • 🩺 Médicos") 
    print("  • 📅 Citas médicas")
    print("  • 📊 Reportes y estadísticas")
    print("\nDesarrollado con:")
    print("  ✅ Programación Orientada a Objetos (POO)")
    print("  ✅ Programación Estructurada")
    print("  ✅ Programación Funcional")
    print("  ✅ Base de datos MySQL")
    print("="*70)

def mostrar_estadisticas_rapidas(servicios):
    """Muestra estadísticas rápidas del sistema"""
    try:
        print("\n📊 ESTADÍSTICAS RÁPIDAS:")
        print("-" * 30)
        
        # Contar pacientes
        total_pacientes = servicios['paciente_service'].contar_total_pacientes()
        print(f"👥 Pacientes registrados: {total_pacientes}")
        
        # Contar médicos
        total_medicos = servicios['medico_service'].contar_total_medicos()
        print(f"🩺 Médicos registrados: {total_medicos}")
        
        # Contar citas por estado
        conteo_citas = servicios['cita_service'].contar_citas_por_estado()
        total_citas = sum(conteo_citas.values())
        print(f"📅 Citas totales: {total_citas}")
        
        if conteo_citas:
            for estado, cantidad in conteo_citas.items():
                emoji = "⏳" if estado == "programada" else "✅" if estado == "completada" else "❌"
                print(f"{emoji} {estado.capitalize()}: {cantidad}")
        
        # Especialidades disponibles
        especialidades = servicios['medico_service'].obtener_especialidades_disponibles()
        if especialidades:
            print(f"🎯 Especialidades: {len(especialidades)}")
        
    except Exception as e:
        print(f"   ℹ️  No se pudieron cargar las estadísticas: {e}")

def ejecutar_opcion_principal(opcion, servicios):
    """Ejecuta la opción seleccionada del menú principal"""
    try:
        if opcion == "1":
            print("\n" + "="*50)
            print("👥 INGRESANDO A GESTIÓN DE PACIENTES")
            print("="*50)
            gestionar_pacientes(servicios['paciente_service'])
            
        elif opcion == "2":
            print("\n" + "="*50)
            print("🩺 INGRESANDO A GESTIÓN DE MÉDICOS")
            print("="*50)
            gestionar_medicos(servicios['medico_service'])
            
        elif opcion == "3":
            print("\n" + "="*50)
            print("📅 INGRESANDO A GESTIÓN DE CITAS")
            print("="*50)
            gestionar_citas(
                servicios['cita_service'],
                servicios['paciente_service'],
                servicios['medico_service']
            )
            
        elif opcion == "4":
            print("\n" + "="*50)
            print("📊 INGRESANDO A REPORTES Y ESTADÍSTICAS")
            print("="*50)
            generar_reportes(
                servicios['reportes_service'],
                servicios['cita_service']
            )
            
        elif opcion == "5":
            print("\n" + "="*50)
            print("👋 ¡HASTA LUEGO!")
            print("="*50)
            return False  # Indicar que se debe salir
            
        else:
            mostrar_mensaje_error("Opción inválida. Por favor, seleccione 1-5")
            
        return True  # Continuar ejecución
        
    except Exception as e:
        mostrar_mensaje_error(f"Error inesperado: {e}")
        return True

def main():
    """Función principal del sistema"""
    try:
        # Mostrar bienvenida
        mostrar_bienvenida()
        
        # Inicializar sistema
        servicios = inicializar_sistema()
        if not servicios:
            input("Presione Enter para salir...")
            return
        
        # Bucle principal
        while True:
            try:
                # Mostrar estadísticas rápidas
                mostrar_estadisticas_rapidas(servicios)
                
                # Mostrar menú principal
                mostrar_menu_principal()
                
                # Leer opción
                opcion = input("\n🎯 Seleccione una opción (1-5): ").strip()
                
                # Ejecutar opción
                if not ejecutar_opcion_principal(opcion, servicios):
                    break
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupción detectada. ¿Desea salir?")
                confirmar = input("Presione 's' para salir o cualquier otra tecla para continuar: ").strip().lower()
                if confirmar == 's':
                    break
            except Exception as e:
                mostrar_mensaje_error(f"Error en el bucle principal: {e}")
                pausar()
    
    except Exception as e:
        mostrar_mensaje_error(f"Error crítico en el sistema: {e}")
    
    finally:
        # Cerrar conexión a la base de datos
        if servicios and 'db' in servicios and servicios['db'].connection:
            servicios['db'].close()
            mostrar_mensaje_exito("Conexión a base de datos cerrada")
        
        print("\n" + "="*50)
        print("🚀 SISTEMA CERRADO CORRECTAMENTE")
        print("="*50)
        print("¡Gracias por usar el Sistema de Gestión Médica!")
        print("Desarrollado con Python 🐍 y MySQL 🗄️")
        print("="*50)

def verificar_dependencias():
    """Verifica que todas las dependencias estén disponibles"""
    try:
        # Verificar imports
        from models.database import Database
        from models.paciente import Paciente
        from models.medico import Medico
        from models.cita import Cita
        
        # Verificar servicios
        from services.paciente_service import PacienteService
        from services.medico_service import MedicoService
        from services.cita_service import CitaService
        from services.reportes_service import ReportesService
        
        # Verificar interfaces de usuario
        from ui.menus import mostrar_menu_principal
        from ui.paciente_ui import gestionar_pacientes
        from ui.medico_ui import gestionar_medicos
        from ui.cita_ui import gestionar_citas
        from ui.reportes_ui import generar_reportes
        
        print("✅ Todas las dependencias están disponibles")
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Asegúrese de que todos los archivos estén en su lugar")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    # Verificar dependencias antes de ejecutar
    print("🔍 VERIFICANDO DEPENDENCIAS...")
    if verificar_dependencias():
        main()
    else:
        print("\n❌ No se pueden verificar todas las dependencias.")
        print("💡 Revise la estructura de archivos y asegúrese de que:")
        print("   - Todos los módulos estén en sus directorios correctos")
        print("   - Los imports en los archivos sean correctos")
        print("   - Las dependencias (mysql-connector, pandas, matplotlib) estén instaladas")
        print("\n📦 Dependencias necesarias:")
        print("   pip install mysql-connector-python pandas matplotlib")
        input("\nPresione Enter para salir...")