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
    
    def calcular_porcentaje_ocupacion_todos(self, fecha_inicio, fecha_fin, mostrar_grafico=True):
        print("\n" + "="*60)
        print("📊 PORCENTAJE DE OCUPACIÓN POR MÉDICO EN EL ULTIMO MES")
        print("="*60)
        print(f"📅 Fecha inicio: {fecha_inicio}")
        print(f"📅 Fecha fin:    {fecha_fin}")
        print("-"*60)

        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

        # 1️⃣ Obtener todos los médicos
        medicos = Medico.listar_todos(self.db)

        resultados = []  # para gráfico

        for medico in medicos:
            citas = Cita.obtener_por_medico(self.db, medico.id)

            # Filtrar citas por rango
            citas_en_rango = [
                c for c in citas 
                if fecha_inicio_dt <= c.fecha_hora.date() <= fecha_fin_dt
            ]

            total_citas = len(citas_en_rango)
            capacidad_maxima = 30

            porcentaje = (total_citas / capacidad_maxima) * 100 if capacidad_maxima else 0

            print(f"👨‍⚕️ Médico: {medico.nombre} ({medico.id})")
            print(f"   📝 Total de citas: {total_citas}")
            print(f"   📈 Ocupación: {porcentaje:.2f}%")
            print("-"*60)

            # Guardamos para el gráfico
            resultados.append({
                "medico": medico.nombre,
                "porcentaje": porcentaje
            })

        # 2️⃣ Mostrar gráfico si se pidió
        if mostrar_grafico and resultados:
            df = pd.DataFrame(resultados)

            plt.figure(figsize=(12, 6))
            plt.bar(df["medico"], df["porcentaje"], color="lightgreen", edgecolor="black")
            plt.title("Porcentaje de Ocupación por Médico", fontsize=16, fontweight='bold')
            plt.xlabel("Médico", fontsize=12)
            plt.ylabel("Porcentaje de Ocupación (%)", fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            plt.show()

        return resultados


    
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
        self.calcular_porcentaje_ocupacion(medico_id=1, fecha_inicio=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"), fecha_fin=datetime.now().strftime("%Y-%m-%d"))
        
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

        
        if conteo_estados:
            estados = list(conteo_estados.keys())
            cantidades = list(conteo_estados.values())

            plt.figure(figsize=(10, 5))
            plt.bar(estados, cantidades, edgecolor='black')

            plt.title("Distribución de Citas por Estado", fontsize=16, fontweight="bold")
            plt.xlabel("Estado de la Cita", fontsize=12)
            plt.ylabel("Cantidad", fontsize=12)
            plt.grid(axis='y', alpha=0.3)

            plt.tight_layout()
            plt.show()

    def reporte_medicos_mas_ocupados(self):
        """Muestra los 3 médicos con más citas programadas y genera un gráfico de barras"""

        # Obtener datos
        medicos_ocupados = self.medico_service.obtener_medicos_mas_ocupados(limite=3)

        print("\n" + "="*60)
        print("🏆 REPORTE: MÉDICOS MÁS OCUPADOS (Solo citas programadas)")
        print("="*60)

        if not medicos_ocupados:
            print("📭 No hay datos suficientes para generar el reporte.")
            return

        # Mostrar en texto
        for i, item in enumerate(medicos_ocupados, 1):
            medico = item["medico"]
            citas_pendientes = item["citas_pendientes"]
            print(f"{i}. 👨‍⚕️ {medico.nombre} — {citas_pendientes} citas programadas")

        # ======================================
        # 📊 GRÁFICO DE BARRAS — TOP 3 MÉDICOS
        # ======================================

        nombres = [item["medico"].nombre for item in medicos_ocupados]
        cantidades = [item["citas_pendientes"] for item in medicos_ocupados]

        df = pd.DataFrame({"Médico": nombres, "Citas Programadas": cantidades})

        plt.figure(figsize=(12, 6))
        plt.bar(df["Médico"], df["Citas Programadas"], color="skyblue", edgecolor="black")

        plt.title("Top 3 Médicos con Más Citas Programadas", fontsize=16, fontweight="bold")
        plt.xlabel("Médico", fontsize=12)
        plt.ylabel("Cantidad de Citas Programadas", fontsize=12)
        plt.grid(axis="y", alpha=0.3)

        # Rotar nombres si son largos
        plt.xticks(rotation=45, ha="right")

        plt.tight_layout()
        plt.show()
    
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
                resumen_medico.to_excel(writer, sheet_name='Resumen_Medicos', index=False)
                
                # Hoja de resumen por estado
                resumen_estado = df.groupby('Estado').size().reset_index()
                resumen_estado.columns = ['Estado', 'Total_Citas']
                resumen_estado.to_excel(writer, sheet_name='Resumen_Estados', index=False)
            
            print(f"✅ Reporte exportado exitosamente a: {nombre_archivo}")
            
        except Exception as e:
            print(f"❌ Error al exportar reporte: {e}")
            raise e  # 🚨 Esto permite que la UI muestre el messagebox
