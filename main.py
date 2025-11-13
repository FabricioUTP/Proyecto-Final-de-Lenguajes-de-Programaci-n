import tkinter as tk
from models.database import Database
from services.paciente_service import PacienteService
from services.medico_service import MedicoService
from services.cita_service import CitaService
from services.reportes_service import ReportesService
from ui_desktop.main_window import MainWindow

def inicializar_sistema():
    db = Database()
    return {
        'db': db,
        'paciente_service': PacienteService(db),
        'medico_service': MedicoService(db),
        'cita_service': CitaService(db),
        'reportes_service': ReportesService(db)
    }

if __name__ == "__main__":
    root = tk.Tk()
    servicios = inicializar_sistema()
    app = MainWindow(root, servicios)
    root.mainloop()
