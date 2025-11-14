from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
from services.reportes_service import ReportesService

class ReporteView(tk.Toplevel):

    def __init__(self, master, reportes_service: ReportesService):
        super().__init__(master)
        self.reportes_service = reportes_service

        self.title("📊 Módulo de Reportes del Sistema")
        self.geometry("650x550")
        self.config(padx=20, pady=20)

        title = ttk.Label(self, text="📊 Reportes del Sistema", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        # Frame principal
        frame = ttk.LabelFrame(self, text="Seleccione un reporte", padding=15)
        frame.pack(fill="both", expand=True, pady=15)

        # Botones de reportes
        ttk.Button(
            frame, text="📄 Reporte General de Citas",
            command=self.reporte_general
        ).pack(fill="x", pady=5)

        ttk.Button(
            frame, text="👨‍⚕️ Citas por Médico",
            command=self.reporte_por_medico
        ).pack(fill="x", pady=5)

        ttk.Button(
            frame, text="📌 Citas por Estado",
            command=self.reporte_por_estado
        ).pack(fill="x", pady=5)

        ttk.Button(
            frame, text="🏥 Citas por Especialidad",
            command=self.reporte_por_especialidad
        ).pack(fill="x", pady=5)

        ttk.Button(
            frame, text="📊 Ocupación de Médicos",
            command=self.reporte_ocupacion
        ).pack(fill="x", pady=5)

        ttk.Button(
            frame, text="📈 Tendencias Mensuales",
            command=self.reporte_tendencias
        ).pack(fill="x", pady=5)

        ttk.Button(
            frame, text="🔢 Top tres de medicos mas ocupados",
            command=self.medicos_mas_ocupados
        ).pack(fill="x", pady=5)

        ttk.Button(
            frame, text="🧩 Reporte Completo",
            command=self.reporte_completo
        ).pack(fill="x", pady=5)

        btn_exportar = ttk.Button(
            frame,
            text="📤 Exportar Reporte a Excel",
            command=self.exportar_excel
        )
        btn_exportar.pack(fill="x", pady=5)

        ttk.Button(
            self, text="❌ Cerrar", command=self.destroy
        ).pack(pady=10)




    def mostrar_dataframe(self, df, titulo="Reporte"):
        ventana = tk.Toplevel(self)
        ventana.title(titulo)
        ventana.geometry("900x500")

        tree = ttk.Treeview(ventana, show="headings")
        tree.pack(fill="both", expand=True)

        # columnas
        tree["columns"] = list(df.columns)

        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # filas
        for _, fila in df.iterrows():
            tree.insert("", "end", values=list(fila))

        ttk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)
    # =======================
    #     CONTROLADORES
    # =======================

    def reporte_general(self):
        df = self.reportes_service.generar_reporte_citas_general()
        if df.empty:
            messagebox.showwarning("Sin datos", "No existen citas registradas.")
            return
        self.mostrar_dataframe(df, "Reporte General de Citas")

    def reporte_por_medico(self):
        self.reportes_service.generar_reporte_citas_por_medico(mostrar_grafico=True)

    def reporte_por_estado(self):
        self.reportes_service.generar_reporte_citas_por_estado(mostrar_grafico=True)

    def reporte_por_especialidad(self):
        self.reportes_service.generar_reporte_citas_por_especialidad(mostrar_grafico=True)

    def reporte_ocupacion(self):
        fecha_inicio = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        fecha_fin = datetime.now().strftime("%Y-%m-%d")

        self.reportes_service.calcular_porcentaje_ocupacion_todos(
            fecha_inicio,
            fecha_fin
        )

    def reporte_tendencias(self):
        self.reportes_service.generar_reporte_tendencias_mensuales()

    def estadisticas_generales(self):
        self.reportes_service.mostrar_estadisticas_generales()

    def reporte_completo(self):
        self.reportes_service.generar_reporte_completo()
    
    def medicos_mas_ocupados(self):
        self.reportes_service.reporte_medicos_mas_ocupados()

    def exportar_excel(self):
        try:
            nombre = "reporte_citas.xlsx"
            self.reportes_service.exportar_reporte_excel(nombre)
            messagebox.showinfo("Exportado", f"Archivo generado:\n{nombre}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el archivo:\n{e}")
