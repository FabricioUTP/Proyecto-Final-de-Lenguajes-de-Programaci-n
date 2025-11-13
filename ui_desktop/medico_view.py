import tkinter as tk
from tkinter import ttk, messagebox

class MedicoView(tk.Toplevel):
    """Ventana gráfica para gestionar médicos con Tkinter"""

    def __init__(self, parent, medico_service):
        super().__init__(parent)
        self.title("Gestión de Médicos")
        self.geometry("900x600")
        self.resizable(False, False)
        self.medico_service = medico_service

        # === Título ===
        ttk.Label(self, text="🩺 Gestión de Médicos", font=("Arial", 16, "bold")).pack(pady=10)

        # === Sección de búsqueda ===
        search_frame = ttk.LabelFrame(self, text="🔍 Buscar Médico")
        search_frame.pack(fill="x", padx=20, pady=10)

        # Combobox para elegir tipo de búsqueda
        ttk.Label(search_frame, text="Buscar por:").grid(row=0, column=0, padx=5, pady=5)
        self.tipo_busqueda = ttk.Combobox(
            search_frame,
            values=["Nombre", "Especialidad", "Gmail", "Teléfono"],
            state="readonly",
            width=20
        )
        self.tipo_busqueda.current(0)
        self.tipo_busqueda.grid(row=0, column=1, padx=5, pady=5)

        # Campo de texto para el valor
        ttk.Label(search_frame, text="Valor:").grid(row=0, column=2, padx=5, pady=5)
        self.valor_busqueda = ttk.Entry(search_frame, width=40)
        self.valor_busqueda.grid(row=0, column=3, padx=5, pady=5)

        # Botones
        ttk.Button(search_frame, text="Buscar", command=self.buscar_medico).grid(row=0, column=4, padx=10, pady=5)
        ttk.Button(search_frame, text="Mostrar Todos", command=self.cargar_medicos).grid(row=0, column=5, padx=10, pady=5)

        # === Formulario ===
        form_frame = ttk.LabelFrame(self, text="Registrar / Actualizar Médico")
        form_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(form_frame, text="Especialidad:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(form_frame, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Label(form_frame, text="Email:").grid(row=3, column=0, padx=5, pady=5)

        self.nombre = ttk.Entry(form_frame, width=35)

        # Combobox de especialidades
        especialidades = [
            "Cardiología", "Pediatría", "Dermatología", "Ginecología",
            "Neurología", "Traumatología", "Oftalmología", "Psiquiatría",
            "Oncología", "Medicina General"
        ]
        self.especialidad = ttk.Combobox(form_frame, values=especialidades, state="readonly", width=33)
        self.especialidad.current(0)

        self.telefono = ttk.Entry(form_frame, width=35)
        self.email = ttk.Entry(form_frame, width=35)

        self.nombre.grid(row=0, column=1, padx=5, pady=5)
        self.especialidad.grid(row=1, column=1, padx=5, pady=5)
        self.telefono.grid(row=2, column=1, padx=5, pady=5)
        self.email.grid(row=3, column=1, padx=5, pady=5)

        # === Botones ===
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Registrar", command=self.registrar_medico).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar_medico).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_medico).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_campos).grid(row=0, column=3, padx=5)

        # === Tabla ===
        self.tabla = ttk.Treeview(self, columns=("ID", "Nombre", "Especialidad", "Teléfono", "Email"), show="headings")
        for col in ("ID", "Nombre", "Especialidad", "Teléfono", "Email"):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=150 if col != "ID" else 60)

        self.tabla.pack(fill="both", expand=True, padx=20, pady=10)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_medico)

        self.cargar_medicos()

    # === CRUD ===
    def registrar_medico(self):
        nombre = self.nombre.get().strip()
        especialidad = self.especialidad.get().strip()
        telefono = self.telefono.get().strip()
        email = self.email.get().strip()

        if not nombre:
            messagebox.showwarning("Atención", "El nombre es obligatorio.")
            return

        try:
            medico = self.medico_service.crear_medico(nombre, especialidad, telefono, email)
            if medico:
                messagebox.showinfo("Éxito", "Médico registrado correctamente.")
                self.cargar_medicos()
                self.limpiar_campos()
            else:
                messagebox.showerror("Error", "No se pudo registrar el médico.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cargar_medicos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        medicos = self.medico_service.obtener_todos_medicos()
        for m in medicos:
            self.tabla.insert("", "end", values=(m.id, m.nombre, m.especialidad or "N/A", m.telefono or "N/A", m.email or "N/A"))

    def seleccionar_medico(self, event):
        seleccion = self.tabla.focus()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion, "values")
        if valores:
            self.id_seleccionado = int(valores[0])
            self.nombre.delete(0, tk.END)
            self.telefono.delete(0, tk.END)
            self.email.delete(0, tk.END)
            
            self.nombre.insert(0, valores[1])
            self.especialidad.set(valores[2])
            self.telefono.insert(0, valores[3])
            self.email.insert(0, valores[4])

    def actualizar_medico(self):
        if not hasattr(self, "id_seleccionado"):
            messagebox.showwarning("Atención", "Seleccione un médico de la lista.")
            return

        campos = {
            "nombre": self.nombre.get().strip(),
            "especialidad": self.especialidad.get().strip(),
            "telefono": self.telefono.get().strip(),
            "email": self.email.get().strip()
        }

        try:
            actualizado = self.medico_service.actualizar_medico(self.id_seleccionado, **campos)
            if actualizado:
                messagebox.showinfo("Éxito", "Médico actualizado correctamente.")
                self.cargar_medicos()
                self.limpiar_campos()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el médico.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_medico(self):
        if not hasattr(self, "id_seleccionado"):
            messagebox.showwarning("Atención", "Seleccione un médico de la lista.")
            return
        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este médico?"):
            try:
                if self.medico_service.eliminar_medico(self.id_seleccionado):
                    messagebox.showinfo("Éxito", "Médico eliminado.")
                    self.cargar_medicos()
                    self.limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # === Búsqueda ===
    def buscar_medico(self):
        tipo = self.tipo_busqueda.get()
        valor = self.valor_busqueda.get().strip()

        if not valor:
            messagebox.showwarning("Atención", "Ingrese un valor para buscar.")
            return

        try:
            resultados = []

            if tipo == "Nombre":
                resultados = self.medico_service.buscar_medicos_por_nombre(valor)
            elif tipo == "Especialidad":
                resultados = self.medico_service.buscar_medicos_por_especialidad(valor)
            elif tipo == "Gmail":
                medico = self.medico_service.buscar_medico_por_email(valor)
                if medico:
                    resultados = [medico]
            elif tipo == "Teléfono":
                medico = self.medico_service.buscar_medico_por_telefono(valor)
                if medico:
                    resultados = [medico]

            # Limpiar tabla antes de mostrar resultados
            for item in self.tabla.get_children():
                self.tabla.delete(item)

            # Si no hay resultados
            if not resultados:
                self.tabla.insert("", "end", values=("", "⚠️ No se encontraron médicos que coincidan con la búsqueda.", "", "", ""))
                return

            # Mostrar resultados
            for m in resultados:
                self.tabla.insert("", "end", values=(
                    m.id,
                    m.nombre,
                    m.especialidad or "N/A",
                    m.telefono or "N/A",
                    m.email or "N/A"
                ))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def limpiar_campos(self):
        self.nombre.delete(0, tk.END)
        self.especialidad.current(0)
        self.telefono.delete(0, tk.END)
        self.email.delete(0, tk.END)
        if hasattr(self, "id_seleccionado"):
            del self.id_seleccionado
