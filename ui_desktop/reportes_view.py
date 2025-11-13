import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta

class ReporteView(tk.Toplevel):
    def __init__(self, parent, reportes_service, cita_service):
        super().__init__(parent)
        self.title("Reportes y Estadísticas")
        self.geometry("750x550")

        self.reportes_service = reportes_service
        self.cita_service = cita_service

        ttk.Label(self, text="📊 Módulo de Reportes y Estadísticas", font=("Arial", 16, "bold")).pack(pady=10)

        frame_botones = ttk.Frame(self)
        frame_botones.pack(pady=10)

        # Botones principales
        ttk.Button(frame_botones, text="📋 Reporte General de Citas", width=35, command=self.reporte_general_citas).grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(frame_botones, text="🧑‍⚕️ Citas por Médico", width=35, command=self.reporte_citas_por_medico).grid(row=1, column=0, padx=10, pady=5)
        ttk.Button(frame_botones, text="📅 Citas por Estado", width=35, command=self.reporte_citas_por_estado).grid(row=2, column=0, padx=10, pady=5)
        ttk.Button(frame_botones, text="💉 Citas por Especialidad", width=35, command=self.reporte_citas_por_especialidad).grid(row=3, column=0, padx=10, pady=5)
        ttk.Button(frame_botones, text="📈 Ocupación de Médicos", width=35, command=self.reporte_ocupacion_medicos).grid(row=4, column=0, padx=10, pady=5)
        ttk.Button(frame_botones, text="📆 Tendencias Mensuales", width=35, command=self.reporte_tendencias_mensuales).grid(row=5, column=0, padx=10, pady=5)
        ttk.Button(frame_botones, text="📊 Estadísticas Generales", width=35, command=self.estadisticas_generales).grid(row=6, column=0, padx=10, pady=5)
        ttk.Button(frame_botones, text="🗂️ Reporte Completo", width=35, command=self.reporte_completo).grid(row=7, column=0, padx=10, pady=5)
        ttk.Button(frame_botones, text="💾 Exportar a Excel", width=35, command=self.exportar_reporte_excel).grid(row=8, column=0, padx=10, pady=5)

        # Área de resultados
        self.resultado_text = tk.Text(self, height=12, width=85, state="disabled", wrap="word")
        self.resultado_text.pack(pady=10, padx=10)

    # Funciones de acción
    def mostrar_resultado(self, texto):
        """Muestra resultados en el cuadro de texto"""
        self.resultado_text.config(state="normal")
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.insert(tk.END, texto)
        self.resultado_text.config(state="disabled")

    def reporte_general_citas(self):
        self.mostrar_resultado("Generando reporte general de citas...\n")
        resultado = self.reportes_service.generar_reporte_citas_general()
        self.mostrar_resultado(resultado or "No hay datos disponibles.")

    def reporte_citas_por_medico(self):
        self.mostrar_resultado("Generando reporte de citas por médico...\n")
        resultado = self.reportes_service.generar_reporte_citas_por_medico(mostrar_grafico=True)
        self.mostrar_resultado(resultado or "No hay datos disponibles.")

    def reporte_citas_por_estado(self):
        self.mostrar_resultado("Generando reporte de citas por estado...\n")
        resultado = self.reportes_service.generar_reporte_citas_por_estado(mostrar_grafico=True)
        self.mostrar_resultado(resultado or "No hay datos disponibles.")

    def reporte_citas_por_especialidad(self):
        self.mostrar_resultado("Generando reporte de citas por especialidad...\n")
        resultado = self.reportes_service.generar_reporte_citas_por_especialidad(mostrar_grafico=True)
        self.mostrar_resultado(resultado or "No hay datos disponibles.")

    def reporte_ocupacion_medicos(self):
        """Permite elegir rango de fechas"""
        top = tk.Toplevel(self)
        top.title("Seleccionar período de análisis")
        top.geometry("350x200")

        ttk.Label(top, text="📆 Fecha Inicio (YYYY-MM-DD):").pack(pady=5)
        fecha_inicio = ttk.Entry(top)
        fecha_inicio.pack()

        ttk.Label(top, text="📆 Fecha Fin (YYYY-MM-DD):").pack(pady=5)
        fecha_fin = ttk.Entry(top)
        fecha_fin.pack()

        def generar():
            fi = fecha_inicio.get().strip() or (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            ff = fecha_fin.get().strip() or datetime.now().strftime("%Y-%m-%d")
            top.destroy()
            self.mostrar_resultado(f"Generando reporte de ocupación de médicos ({fi} a {ff})...\n")
            resultado = self.reportes_service.generar_reporte_ocupacion_medicos(fi, ff)
            self.mostrar_resultado(resultado or "No hay datos disponibles.")

        ttk.Button(top, text="Generar", command=generar).pack(pady=10)

    def reporte_tendencias_mensuales(self):
        self.mostrar_resultado("Generando reporte de tendencias mensuales...\n")
        resultado = self.reportes_service.generar_reporte_tendencias_mensuales()
        self.mostrar_resultado(resultado or "No hay datos disponibles.")

    def estadisticas_generales(self):
        self.mostrar_resultado("Calculando estadísticas generales...\n")
        resultado = self.reportes_service.mostrar_estadisticas_generales()
        self.mostrar_resultado(resultado or "No hay datos disponibles.")

    def reporte_completo(self):
        self.mostrar_resultado("Generando reporte completo...\n")
        resultado = self.reportes_service.generar_reporte_completo()
        self.mostrar_resultado(resultado or "No hay datos disponibles.")

    def exportar_reporte_excel(self):
        archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivo Excel", "*.xlsx")],
            title="Guardar reporte como..."
        )
        if archivo:
            self.mostrar_resultado(f"Exportando datos a {archivo}...\n")
            exito = self.reportes_service.exportar_reporte_excel(archivo)
            if exito:
                messagebox.showinfo("Éxito", f"Reporte exportado correctamente a:\n{archivo}")
            else:
                messagebox.showerror("Error", "No se pudo exportar el reporte.")
