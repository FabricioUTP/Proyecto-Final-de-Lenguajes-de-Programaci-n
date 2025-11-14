import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry  # Importamos el selector de fechas

class PacienteView(tk.Toplevel):
    """Ventana gráfica para gestionar pacientes con Tkinter"""
    def __init__(self, parent, paciente_service):
        super().__init__(parent)
        self.title("Gestión de Pacientes")
        self.geometry("850x600")
        self.resizable(False, False)
        self.paciente_service = paciente_service

        self.grab_set()
        self.focus()

        # === Título ===
        ttk.Label(self, text="👥 Gestión de Pacientes", font=("Arial", 16, "bold")).pack(pady=10)

        # === Formulario ===
        form_frame = ttk.LabelFrame(self, text="Registrar / Actualizar Paciente")
        form_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(form_frame, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Label(form_frame, text="Fecha Nacimiento:").grid(row=3, column=0, padx=5, pady=5)

        self.nombre = ttk.Entry(form_frame, width=35)
        self.email = ttk.Entry(form_frame, width=35)
        self.telefono = ttk.Entry(form_frame, width=35)
        self.fecha_nacimiento = DateEntry(form_frame, width=33, background='darkblue',
                                          foreground='white', date_pattern='yyyy-mm-dd')

        self.nombre.grid(row=0, column=1, padx=5, pady=5)
        self.email.grid(row=1, column=1, padx=5, pady=5)
        self.telefono.grid(row=2, column=1, padx=5, pady=5)
        self.fecha_nacimiento.grid(row=3, column=1, padx=5, pady=5)

        # === Botones ===
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Registrar", command=self.registrar_paciente).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar_paciente).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_paciente).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Historial de Citas", command=self.ver_historial_citas).grid(row=0, column=3, padx=5)

        # === Sección de búsqueda ===
        search_frame = ttk.LabelFrame(self, text="🔍 Buscar Paciente")
        search_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(search_frame, text="Buscar por:").grid(row=0, column=0, padx=5, pady=5)
        self.tipo_busqueda = ttk.Combobox(search_frame, values=["Nombre", "Email", "Teléfono"], state="readonly")
        self.tipo_busqueda.current(0)
        self.tipo_busqueda.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(search_frame, text="Valor:").grid(row=0, column=2, padx=5, pady=5)
        self.valor_busqueda = ttk.Entry(search_frame, width=40)
        self.valor_busqueda.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(search_frame, text="Buscar", command=self.buscar_paciente).grid(row=0, column=4, padx=5)
        ttk.Button(search_frame, text="Mostrar Todos", command=self.cargar_pacientes).grid(row=0, column=5, padx=5)

        # === Tabla de pacientes ===
        self.tabla = ttk.Treeview(self, columns=("ID", "Nombre", "Email", "Teléfono", "Fecha Nacimiento"), show="headings")
        for col in ("ID", "Nombre", "Email", "Teléfono", "Fecha Nacimiento"):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=150 if col != "ID" else 60)

        self.tabla.pack(fill="both", expand=True, padx=20, pady=10)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_paciente)

        self.cargar_pacientes()

    # === Funciones CRUD y validaciones ===
    def registrar_paciente(self):
        nombre = self.nombre.get().strip()
        email = self.email.get().strip()
        telefono = self.telefono.get().strip()
        fecha_nac = self.fecha_nacimiento.get_date().strftime("%Y-%m-%d")

        # === VALIDACIONES ===
        if not nombre:
            messagebox.showwarning("Atención", "El nombre es obligatorio.")
            return

        if not email:
            messagebox.showwarning("Atención", "El email es obligatorio.")
            return
        if not email.lower().endswith("@gmail.com"):
            messagebox.showwarning("Atención", "El email debe terminar en '@gmail.com'.")
            return

        if not telefono:
            messagebox.showwarning("Atención", "El teléfono es obligatorio.")
            return
        if not (telefono.isdigit() and len(telefono) == 9 and telefono.startswith("9")):
            messagebox.showwarning("Atención", "El teléfono debe comenzar con 9 y tener 9 dígitos.")
            return

        # === CREAR PACIENTE ===
        try:
            paciente = self.paciente_service.crear_paciente(nombre, email, telefono, fecha_nac)
            if paciente:
                messagebox.showinfo("Éxito", "Paciente registrado correctamente.")
                self.cargar_pacientes()
                self.limpiar_campos()
            else:
                messagebox.showerror("Error", "No se pudo registrar el paciente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_paciente(self):
        if not hasattr(self, "id_seleccionado"):
            messagebox.showwarning("Atención", "Seleccione un paciente de la lista.")
            return

        campos = {
            "nombre": self.nombre.get().strip(),
            "email": self.email.get().strip(),
            "telefono": self.telefono.get().strip(),
            "fecha_nacimiento": self.fecha_nacimiento.get_date().strftime("%Y-%m-%d")
        }

        # Validaciones similares al registrar
        if not campos["nombre"] or not campos["email"] or not campos["telefono"]:
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return
        if not campos["email"].lower().endswith("@gmail.com"):
            messagebox.showwarning("Atención", "El email debe terminar en '@gmail.com'.")
            return
        if not (campos["telefono"].isdigit() and len(campos["telefono"]) == 9 and campos["telefono"].startswith("9")):
            messagebox.showwarning("Atención", "El teléfono debe comenzar con 9 y tener 9 dígitos.")
            return

        try:
            actualizado = self.paciente_service.actualizar_paciente(self.id_seleccionado, **campos)
            if actualizado:
                messagebox.showinfo("Éxito", "Paciente actualizado correctamente.")
                self.cargar_pacientes()
                self.limpiar_campos()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el paciente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_paciente(self):
        if not hasattr(self, "id_seleccionado"):
            messagebox.showwarning("Atención", "Seleccione un paciente de la lista.")
            return
        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este paciente?"):
            try:
                if self.paciente_service.eliminar_paciente(self.id_seleccionado):
                    messagebox.showinfo("Éxito", "Paciente eliminado.")
                    self.cargar_pacientes()
                    self.limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def buscar_paciente(self):
        tipo = self.tipo_busqueda.get()
        valor = self.valor_busqueda.get().strip()
        if not valor:
            messagebox.showwarning("Atención", "Ingrese un valor de búsqueda.")
            return

        try:
            resultados = []
            if tipo == "Nombre":
                resultados = self.paciente_service.buscar_pacientes_por_nombre(valor)
            elif tipo == "Email":
                paciente = self.paciente_service.buscar_paciente_por_email(valor)
                if paciente:
                    resultados = [paciente]
            elif tipo == "Teléfono":
                paciente = self.paciente_service.buscar_paciente_por_telefono(valor)
                if paciente:
                    resultados = [paciente]

            # Mostrar resultados
            for item in self.tabla.get_children():
                self.tabla.delete(item)
            if not resultados:
                messagebox.showinfo("Sin resultados", "No se encontraron pacientes con ese criterio.")
                return
            for p in resultados:
                self.tabla.insert("", "end", values=(p.id, p.nombre, p.email or "N/A",
                                                     p.telefono or "N/A", p.fecha_nacimiento or "N/A"))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ver_historial_citas(self):
        if not hasattr(self, "id_seleccionado"):
            messagebox.showwarning("Atención", "Seleccione un paciente.")
            return

        try:
            historial = self.paciente_service.obtener_historial_citas_paciente(self.id_seleccionado)
            if not historial:
                messagebox.showinfo("Sin datos", "El paciente no tiene citas registradas.")
                return

            ventana = tk.Toplevel(self)
            ventana.title("Historial de Citas")
            ventana.geometry("600x400")

            tree = ttk.Treeview(ventana, columns=("Fecha", "Médico", "Especialidad", "Estado", "Motivo"), show="headings")
            for col in ("Fecha", "Médico", "Especialidad", "Estado", "Motivo"):
                tree.heading(col, text=col)
                tree.column(col, width=120)

            for c in historial:
                tree.insert("", "end", values=(c["fecha_hora"], c["medico"], c["especialidad"], c["estado"], c["motivo"]))

            tree.pack(fill="both", expand=True, padx=10, pady=10)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def seleccionar_paciente(self, event):
        seleccion = self.tabla.focus()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion, "values")
        if valores:
            self.id_seleccionado = int(valores[0])
            self.nombre.delete(0, tk.END)
            self.email.delete(0, tk.END)
            self.telefono.delete(0, tk.END)
            self.fecha_nacimiento.set_date(valores[4])  # Asignar fecha al DateEntry

            self.nombre.insert(0, valores[1])
            self.email.insert(0, valores[2])
            self.telefono.insert(0, valores[3])

    def cargar_pacientes(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        pacientes = self.paciente_service.obtener_todos_pacientes()
        for p in pacientes:
            self.tabla.insert("", "end", values=(p.id, p.nombre, p.email or "N/A",
                                                 p.telefono or "N/A", p.fecha_nacimiento or "N/A"))

    def limpiar_campos(self):
        self.nombre.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.telefono.delete(0, tk.END)
        self.fecha_nacimiento.set_date(datetime.today())
        if hasattr(self, "id_seleccionado"):
            del self.id_seleccionado
