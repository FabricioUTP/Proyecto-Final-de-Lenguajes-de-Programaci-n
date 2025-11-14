import tkinter as tk
from tkinter import ttk, messagebox
from ui_desktop.paciente_view import PacienteView
from ui_desktop.medico_view import MedicoView
from ui_desktop.cita_view import CitaView
from ui_desktop.reportes_view import ReporteView

class MainWindow:
    def __init__(self, root, servicios):
        self.root = root
        self.root.title("🏥 Sistema de Gestión Médica")
        self.root.geometry("800x600")
        self.servicios = servicios

        # Encabezado
        titulo = ttk.Label(root, text="Sistema de Gestión Médica", font=("Arial", 20, "bold"))
        titulo.pack(pady=20)

        # Botones principales
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=40)

        ttk.Button(btn_frame, text="👥 Pacientes", width=25, command=self.abrir_pacientes).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(btn_frame, text="🩺 Médicos", width=25, command=self.abrir_medicos).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(btn_frame, text="📅 Citas", width=25, command=self.abrir_citas).grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(btn_frame, text="📊 Reportes", width=25, command=self.abrir_reportes).grid(row=3, column=0, padx=10, pady=10)
        ttk.Button(btn_frame, text="🚪 Salir", width=25, command=self.salir).grid(row=4, column=0, padx=10, pady=10)

    def abrir_pacientes(self):
        PacienteView(self.root, self.servicios['paciente_service'])

    def abrir_medicos(self):
        MedicoView(self.root, self.servicios['medico_service'])

    def abrir_citas(self):
        CitaView(self.root, self.servicios)

    def abrir_reportes(self):
        ReporteView(self.root, self.servicios['reportes_service'])

    def salir(self):
        if messagebox.askyesno("Salir", "¿Seguro que deseas salir del sistema?"):
            self.root.destroy()
