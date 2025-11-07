from typing import List, Dict, Any
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from models.database import Database
from models.cita import Cita
from models.paciente import Paciente
from models.medico import Medico
from services.cita_service import CitaService
from services.paciente_service import PacienteService
from services.medico_service import MedicoService

class ReportesService:
    """Servicio para generar reportes y gráficos con pandas y matplotlib"""
    
    def __init__(self, db: Database):
        self.db = db
        self.cita_service = CitaService(db)
        self.paciente_service = PacienteService(db)
        self.medico_service = MedicoService(db)
    
    def generar_reporte_citas_general(self) -> pd.DataFrame:
        """Genera un reporte general de todas las citas"""
        citas = Cita.obtener_todas(self.db)
        
        if not citas:
            print("📭 No hay citas para generar reporte")
            return pd.DataFrame()
        
        # Preparar datos para el DataFrame
        datos = []
        for cita in citas:
            cita.cargar_detalles(self.db)
            datos.append({
                'ID_Cita': cita.id,
                'Fecha_Hora': cita.fecha_hora,
                'Paciente': cita.paciente.nombre if cita.paciente else 'N/A',
                'Médico': cita.medico.nombre if cita.medico else 'N/A',
                'Especialidad': cita.medico.especialidad if cita.medico else 'N/A',
                'Estado': cita.estado,
                'Motivo': cita.motivo
            })
        
        df = pd.DataFrame(datos)
        return df
    
    def generar_reporte_citas_por_medico(self, mostrar_grafico: bool = True):
        """Genera reporte de citas por médico con gráficos"""
        df = self.generar_reporte_citas_general()
        
        if df.empty:
            return
        
        # Reporte por médico
        citas_por_medico = df.groupby('Médico').size().sort_values(ascending=False)
        
        print("\n" + "="*50)
        print("📊 REPORTE DE CITAS POR MÉDICO")
        print("="*50)
        for medico, cantidad in citas_por_medico.items():
            print(f"👨‍⚕️  {medico}: {cantidad} citas")
        
        if mostrar_grafico:
            # Gráfico de barras
            plt.figure(figsize=(12, 6))
            citas_por_medico.plot(kind='bar', color='skyblue', edgecolor='black')
            plt.title('Citas por Médico', fontsize=16, fontweight='bold')
            plt.xlabel('Médico', fontsize=12)
            plt.ylabel('Número de Citas', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            plt.show()
    
    def generar_reporte_citas_por_estado(self, mostrar_grafico: bool = True):
        """Genera reporte de citas por estado con gráficos"""
        df = self.generar_reporte_citas_general()
        
        if df.empty:
            return
        
        # Reporte por estado
        citas_por_estado = df.groupby('Estado').size()
        
        print("\n" + "="*50)
        print("📊 REPORTE DE CITAS POR ESTADO")
        print("="*50)
        total_citas = len(df)
        for estado, cantidad in citas_por_estado.items():
            porcentaje = (cantidad / total_citas) * 100
            print(f"📌 {estado.capitalize()}: {cantidad} citas ({porcentaje:.1f}%)")
        
        print(f"\n📈 Total de citas: {total_citas}")
        
        if mostrar_grafico:
            # Gráfico de pie
            plt.figure(figsize=(10, 8))
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
            citas_por_estado.plot(
                kind='pie', 
                autopct='%1.1f%%', 
                colors=colors[:len(citas_por_estado)],
                startangle=90,
                shadow=True
            )
            plt.title('Distribución de Citas por Estado', fontsize=16, fontweight='bold')
            plt.ylabel('')  # Oculta el label del y-axis
            plt.tight_layout()
            plt.show()
    
    def generar_reporte_citas_por_especialidad(self, mostrar_grafico: bool = True):
        """Genera reporte de citas por especialidad médica"""
        df = self.generar_reporte_citas_general()
        
        if df.empty:
            return
        
        # Filtrar datos válidos
        df_especialidades = df[df['Especialidad'] != 'N/A']
        
        if df_especialidades.empty:
            print("📭 No hay datos de especialidades para generar reporte")
            return
        
        citas_por_especialidad = df_especialidades.groupby('Especialidad').size().sort_values(ascending=False)
        
        print("\n" + "="*50)
        print("📊 REPORTE DE CITAS POR ESPECIALIDAD")
        print("="*50)
        for especialidad, cantidad in citas_por_especialidad.items():
            print(f"🎯 {especialidad}: {cantidad} citas")
        
        if mostrar_grafico:
            plt.figure(figsize=(12, 6))
            citas_por_especialidad.plot(kind='bar', color='lightgreen', edgecolor='black')
            plt.title('Citas por Especialidad Médica', fontsize=16, fontweight='bold')
            plt.xlabel('Especialidad', fontsize=12)
            plt.ylabel('Número de Citas', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            plt.show()
    
    def generar_reporte_ocupacion_medicos(self, fecha_inicio: str = None, fecha_fin: str = None):
        """Genera reporte de ocupación de médicos"""
        if not fecha_inicio or not fecha_fin:
            # Usar el último mes por defecto
            fecha_fin = datetime.now().strftime("%Y-%m-%d")
            fecha_inicio = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        medicos = Medico.obtener_todos(self.db)
        
        if not medicos:
            print("📭 No hay médicos para generar reporte")
            return
        
        print("\n" + "="*60)
        print("📊 REPORTE DE OCUPACIÓN DE MÉDICOS")
        print(f"📅 Período: {fecha_inicio} a {fecha_fin}")
        print("="*60)
        
        datos_ocupacion = []
        for medico in medicos:
            porcentaje = self.cita_service.calcular_porcentaje_ocupacion(
                medico.id, fecha_inicio, fecha_fin
            )
            datos_ocupacion.append({
                'Médico': medico.nombre,
                'Especialidad': medico.especialidad or 'N/A',
                'Ocupación (%)': porcentaje
            })
            print(f"👨‍⚕️  {medico.nombre} ({medico.especialidad}): {porcentaje:.1f}%")
        
        # Crear DataFrame para análisis adicional
        df_ocupacion = pd.DataFrame(datos_ocupacion)
        
        if not df_ocupacion.empty:
            # Gráfico de ocupación
            plt.figure(figsize=(12, 6))
            plt.bar(df_ocupacion['Médico'], df_ocupacion['Ocupación (%)'], 
                   color=['green' if x < 70 else 'orange' if x < 90 else 'red' 
                         for x in df_ocupacion['Ocupación (%)']])
            plt.title(f'Ocupación de Médicos ({fecha_inicio} a {fecha_fin})', 
                     fontsize=16, fontweight='bold')
            plt.xlabel('Médico', fontsize=12)
            plt.ylabel('Porcentaje de Ocupación (%)', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.ylim(0, 100)
            plt.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            plt.show()
    
    def generar_reporte_tendencias_mensuales(self):
        """Genera reporte de tendencias mensuales de citas"""
        df = self.generar_reporte_citas_general()
        
        if df.empty:
            return
        
        # Extraer mes y año de las fechas
        df['Mes'] = df['Fecha_Hora'].dt.to_period('M')
        tendencias_mensuales = df.groupby('Mes').size()
        
        print("\n" + "="*50)
        print("📊 TENDENCIAS MENSUALES DE CITAS")
        print("="*50)
        
        for mes, cantidad in tendencias_mensuales.items():
            print(f"📅 {mes}: {cantidad} citas")
        
        # Gráfico de tendencias
        plt.figure(figsize=(12, 6))
        tendencias_mensuales.plot(kind='line', marker='o', color='purple', linewidth=2)
        plt.title('Tendencias Mensuales de Citas', fontsize=16, fontweight='bold')
        plt.xlabel('Mes', fontsize=12)
        plt.ylabel('Número de Citas', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def generar_reporte_completo(self):
        """Genera un reporte completo con todos los análisis"""
        print("🚀 GENERANDO REPORTE COMPLETO...")
        
        # 1. Reporte general
        self.generar_reporte_citas_por_estado(mostrar_grafico=True)
        
        # 2. Reporte por médico
        self.generar_reporte_citas_por_medico(mostrar_grafico=True)
        
        # 3. Reporte por especialidad
        self.generar_reporte_citas_por_especialidad(mostrar_grafico=True)
        
        # 4. Reporte de ocupación
        self.generar_reporte_ocupacion_medicos()
        
        # 5. Estadísticas adicionales
        self.mostrar_estadisticas_generales()
    
    def mostrar_estadisticas_generales(self):
        """Muestra estadísticas generales del sistema"""
        total_pacientes = self.paciente_service.contar_total_pacientes()
        total_medicos = self.medico_service.contar_total_medicos()
        total_citas = len(Cita.obtener_todas(self.db))
        conteo_estados = self.cita_service.contar_citas_por_estado()
        
        print("\n" + "="*50)
        print("📈 ESTADÍSTICAS GENERALES DEL SISTEMA")
        print("="*50)
        print(f"👥 Total de pacientes: {total_pacientes}")
        print(f"🩺 Total de médicos: {total_medicos}")
        print(f"📅 Total de citas: {total_citas}")
        print(f"🎯 Especialidades disponibles: {len(self.medico_service.obtener_especialidades_disponibles())}")
        
        if conteo_estados:
            print("\n📊 Distribución de citas:")
            for estado, cantidad in conteo_estados.items():
                print(f"   • {estado.capitalize()}: {cantidad}")
        
        # Médicos más ocupados
        medicos_ocupados = self.medico_service.obtener_medicos_mas_ocupados(limite=3)
        if medicos_ocupados:
            print(f"\n🏆 Top 3 médicos más ocupados:")
            for i, item in enumerate(medicos_ocupados, 1):
                print(f"   {i}. {item['medico'].nombre}: {item['citas_pendientes']} citas pendientes")
    
    def exportar_reporte_excel(self, nombre_archivo: str = "reporte_citas.xlsx"):
        """Exporta el reporte completo a Excel"""
        try:
            df = self.generar_reporte_citas_general()
            
            if df.empty:
                print("📭 No hay datos para exportar")
                return
            
            with pd.ExcelWriter(nombre_archivo, engine='openpyxl') as writer:
                # Hoja principal
                df.to_excel(writer, sheet_name='Citas_Completas', index=False)
                
                # Hoja de resumen por médico
                resumen_medico = df.groupby('Médico').size().reset_index()
                resumen_medico.columns = ['Médico', 'Total_Citas']
                resumen_medico.to_excel(writer, sheet_name='Resumen_Médicos', index=False)
                
                # Hoja de resumen por estado
                resumen_estado = df.groupby('Estado').size().reset_index()
                resumen_estado.columns = ['Estado', 'Total_Citas']
                resumen_estado.to_excel(writer, sheet_name='Resumen_Estados', index=False)
            
            print(f"✅ Reporte exportado exitosamente a: {nombre_archivo}")
            
        except Exception as e:
            print(f"❌ Error al exportar reporte: {e}")