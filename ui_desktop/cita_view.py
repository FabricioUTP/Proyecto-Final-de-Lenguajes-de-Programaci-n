import tkinter as tk
from tkinter import ttk, messagebox

class CitaView(tk.Toplevel):
    """Ventana gráfica para gestionar citas"""

    def __init__(self, parent, servicios):
        super().__init__(parent)
        self.title("Gestión de Citas")
        self.geometry("950x650")
        self.resizable(False, False)

        # Servicios
        self.cita_service = servicios["cita_service"]
        self.paciente_service = servicios["paciente_service"]
        self.medico_service = servicios["medico_service"]

        # === FORMULARIO ===
        form_frame = ttk.LabelFrame(self, text="Registrar Cita", padding=10)
        form_frame.pack(fill="x", padx=20, pady=10)

        # Obtener pacientes y médicos
        pacientes_lista = self.paciente_service.obtener_todos_pacientes()
        medicos_lista = self.medico_service.obtener_todos_medicos()

        # Diccionarios: nombre -> id
        self.pacientes_dict = {p.nombre: p.id for p in pacientes_lista}
        self.medicos_dict = {m.nombre: m.id for m in medicos_lista}

        # Listas de nombres (para mostrar en los combobox)
        pacientes = list(self.pacientes_dict.keys())
        medicos = list(self.medicos_dict.keys())

        # Campos del formulario
        ttk.Label(form_frame, text="Paciente:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.paciente_cb = ttk.Combobox(form_frame, values=pacientes, state="readonly", width=40)
        self.paciente_cb.grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Médico:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.medico_cb = ttk.Combobox(form_frame, values=medicos, state="readonly", width=40)
        self.medico_cb.grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Fecha (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.fecha_entry = ttk.Entry(form_frame, width=42)
        self.fecha_entry.grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Motivo de la cita:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.motivo_entry = ttk.Entry(form_frame, width=42)
        self.motivo_entry.grid(row=3, column=1, pady=5)

        ttk.Button(form_frame, text="Registrar Cita", command=self.registrar_cita).grid(row=4, columnspan=2, pady=10)

        # === TABLA DE CITAS ===
        tabla_frame = ttk.LabelFrame(self, text="Citas Registradas", padding=10)
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = ("id", "paciente", "medico", "fecha", "motivo")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=12)

        self.tabla.heading("id", text="ID")
        self.tabla.heading("paciente", text="Paciente")
        self.tabla.heading("medico", text="Médico")
        self.tabla.heading("fecha", text="Fecha")
        self.tabla.heading("motivo", text="Motivo")

        self.tabla.column("id", width=60, anchor="center")
        self.tabla.column("paciente", width=180)
        self.tabla.column("medico", width=180)
        self.tabla.column("fecha", width=100, anchor="center")
        self.tabla.column("motivo", width=300)

        self.tabla.pack(fill="both", expand=True)
        self.cargar_citas()

    # === FUNCIONES ===
    def registrar_cita(self):
        try:
            paciente_nombre = self.paciente_cb.get()
            medico_nombre = self.medico_cb.get()
            fecha = self.fecha_entry.get().strip()
            motivo = self.motivo_entry.get().strip()

            if not paciente_nombre or not medico_nombre or not fecha or not motivo:
                messagebox.showwarning("Atención", "Complete todos los campos.")
                return

            # Obtener los IDs reales desde los diccionarios
            paciente_id = self.pacientes_dict.get(paciente_nombre)
            medico_id = self.medicos_dict.get(medico_nombre)

            if not paciente_id:
                messagebox.showerror("Error", "❌ Paciente no encontrado.")
                return
            if not medico_id:
                messagebox.showerror("Error", "❌ Médico no encontrado.")
                return

            # Registrar cita
            self.cita_service.crear_cita(paciente_id, medico_id, fecha, motivo)
            messagebox.showinfo("Éxito", "✅ Cita registrada correctamente.")
            self.cargar_citas()

            # Limpiar campos
            self.paciente_cb.set("")
            self.medico_cb.set("")
            self.fecha_entry.delete(0, tk.END)
            self.motivo_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cargar_citas(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        citas = self.cita_service.obtener_todas_citas()

        for c in citas:
            # Obtenemos los nombres de paciente y médico
            medico = self.medico_service.obtener_medico_por_id(c.medico_id)
            paciente = self.paciente_service.obtener_paciente_por_id(c.paciente_id)
            print(medico, paciente)  # Debugging line

            self.tabla.insert(
                "",
                "end",
                values=(
                    c.id,
                    paciente,
                    medico,
                    c.fecha_hora,
                    c.motivo
                )
            )


