import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

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

        self.grab_set()
        self.focus()

        # === FORMULARIO ===
        form_frame = ttk.LabelFrame(self, text="Registrar Cita", padding=10)
        form_frame.pack(fill="x", padx=20, pady=10)

        # Obtener pacientes y médicos
        pacientes_lista = self.paciente_service.obtener_todos_pacientes()
        medicos_lista = self.medico_service.obtener_todos_medicos()

        # Diccionarios: nombre -> id
        self.pacientes_dict = {p.nombre: p.id for p in pacientes_lista}
        self.medicos_dict = {m.nombre: m.id for m in medicos_lista}

        # Listas de nombres (para combobox)
        pacientes = list(self.pacientes_dict.keys())
        medicos = list(self.medicos_dict.keys())

        # Campos del formulario
        ttk.Label(form_frame, text="Paciente:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.paciente_cb = ttk.Combobox(form_frame, values=pacientes, state="readonly", width=40)
        self.paciente_cb.grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Médico:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.medico_cb = ttk.Combobox(form_frame, values=medicos, state="readonly", width=40)
        self.medico_cb.grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Fecha de la cita:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.fecha_entry = DateEntry(form_frame, width=42, date_pattern="yyyy-mm-dd", mindate=datetime.today())
        self.fecha_entry.grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Motivo de la cita:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.motivo_entry = ttk.Entry(form_frame, width=42)
        self.motivo_entry.grid(row=3, column=1, pady=5)

        ttk.Button(form_frame, text="Registrar Cita", command=self.registrar_cita).grid(row=4, columnspan=2, pady=10)

    
        # === FILTROS ===
        filtro_frame = ttk.LabelFrame(self, text="Filtrar Citas", padding=10)
        filtro_frame.pack(fill="x", padx=20, pady=10)

        # SELECT PRINCIPAL
        ttk.Label(filtro_frame, text="Filtrar por:").grid(row=0, column=0, padx=5, pady=5)
        self.filtro_tipo_cb = ttk.Combobox(
            filtro_frame, 
            values=["Estado", "Médico", "Paciente", "Fecha", "Rango"],
            state="readonly",
            width=20
        )
        self.filtro_tipo_cb.grid(row=0, column=1, padx=5, pady=5)
        self.filtro_tipo_cb.bind("<<ComboboxSelected>>", self.mostrar_filtro)

        # CAMPOS DINÁMICOS (se mostrarán según el tipo de filtro)

        # Filtro por estado
        self.estado_label = ttk.Label(filtro_frame, text="Estado:")
        self.estado_cb = ttk.Combobox(
            filtro_frame, 
            values=["programada", "completada", "cancelada"],
            state="readonly",
            width=20
        )

        # Filtro por médico
        self.medico_label = ttk.Label(filtro_frame, text="Médico:")
        self.filtro_medico_cb = ttk.Combobox(
            filtro_frame,
            values=list(self.medicos_dict.keys()),
            state="readonly",
            width=20
        )

        # Filtro por paciente
        self.paciente_label = ttk.Label(filtro_frame, text="Paciente:")
        self.filtro_paciente_cb = ttk.Combobox(
            filtro_frame,
            values=list(self.pacientes_dict.keys()),
            state="readonly",
            width=20
        )

        # Filtro por fecha única
        self.fecha_label = ttk.Label(filtro_frame, text="Fecha (YYYY-MM-DD):")
        self.filtro_fecha_entry = ttk.Entry(filtro_frame, width=22)

        # Filtro rango
        self.desde_label = ttk.Label(filtro_frame, text="Desde:")
        self.fecha_inicio_entry = ttk.Entry(filtro_frame, width=22)

        self.hasta_label = ttk.Label(filtro_frame, text="Hasta:")
        self.fecha_fin_entry = ttk.Entry(filtro_frame, width=22)

        # BOTÓN BUSCAR
        self.buscar_btn = ttk.Button(filtro_frame, text="Buscar", command=self.ejecutar_busqueda)


        ttk.Button(filtro_frame, text="Quitar Filtros", command=self.quitar_filtros).grid(row=6, column=1, pady=10)


        acciones_frame = ttk.Frame(self)
        acciones_frame.pack(fill="x", padx=20, pady=10)

        ttk.Button(
            acciones_frame,
            text="Marcar como Completada",
            command=self.marcar_completada
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            acciones_frame,
            text="Cancelar Cita",
            command=self.cancelar_cita_ui
            ).grid(row=0, column=1, padx=5)


        # === TABLA DE CITAS ===
        tabla_frame = ttk.LabelFrame(self, text="Citas Registradas", padding=10)
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = ("id", "paciente", "medico", "fecha", "motivo", "estado")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=12)

        for col, width in zip(columnas, [60, 180, 180, 100, 100, 100]):
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=width, anchor="center" if col in ["id","fecha","estado"] else "w")

        self.tabla.pack(fill="both", expand=True)

        self.cargar_citas()

    # === FUNCIONES ===
    def registrar_cita(self):
        try:
            paciente_nombre = self.paciente_cb.get()
            medico_nombre = self.medico_cb.get()
            fecha_str = self.fecha_entry.get_date().strftime("%Y-%m-%d")
            motivo = self.motivo_entry.get().strip()

            # Validaciones
            if not paciente_nombre or not medico_nombre or not fecha_str or not motivo:
                messagebox.showwarning("Atención", "Complete todos los campos.")
                return

            # Verificar paciente y médico
            paciente_id = self.pacientes_dict.get(paciente_nombre)
            medico_id = self.medicos_dict.get(medico_nombre)
            if not paciente_id:
                messagebox.showerror("Error", "❌ Paciente no encontrado.")
                return
            if not medico_id:
                messagebox.showerror("Error", "❌ Médico no encontrado.")
                return

            # Registrar cita
            self.cita_service.crear_cita(paciente_id, medico_id, fecha_str, motivo)
            messagebox.showinfo("Éxito", "✅ Cita registrada correctamente.")
            self.cargar_citas()

            # Limpiar campos
            self.paciente_cb.set("")
            self.medico_cb.set("")
            self.motivo_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cargar_citas(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        citas = self.cita_service.obtener_todas_citas()
        for c in citas:
            medico = self.medico_service.obtener_medico_por_id(c.medico_id)
            paciente = self.paciente_service.obtener_paciente_por_id(c.paciente_id)
            self.tabla.insert(
                "",
                "end",
                values=(c.id, paciente.nombre, medico.nombre, c.fecha_hora, c.motivo, c.estado)
            )

    def obtener_cita_seleccionada(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return None
        valores = self.tabla.item(seleccion[0], "values")
        return int(valores[0])

    def cancelar_cita_ui(self):
        cita_id = self.obtener_cita_seleccionada()
        if not cita_id:
            messagebox.showwarning("Atención", "Seleccione una cita.")
            return
        if messagebox.askyesno("Confirmar", "¿Estás seguro de cancelar esta cita?"):
            if self.cita_service.cancelar_cita(cita_id):
                messagebox.showinfo("Éxito", "La cita fue cancelada.")
                self.cargar_citas()
            else:
                messagebox.showerror("Error", "No se pudo cancelar la cita.")

    def marcar_completada(self):
        cita_id = self.obtener_cita_seleccionada()
        if not cita_id:
            messagebox.showwarning("Atención", "Seleccione una cita.")
            return
        if messagebox.askyesno("Confirmar", "¿Marcar la cita como completada?"):
            if self.cita_service.completar_cita(cita_id):
                messagebox.showinfo("Éxito", "La cita fue marcada como completada.")
                self.cargar_citas()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el estado.")

    def buscar_por_estado(self):
        estado = self.estado_cb.get()
        if not estado:
            messagebox.showwarning("Atención", "Seleccione un estado.")
            return

        citas = self.cita_service.filtrar_citas_por_estado(estado)
        self.mostrar_citas(citas)

    def buscar_por_medico(self):
        nombre = self.filtro_medico_cb.get()
        if not nombre:
            messagebox.showwarning("Atención", "Seleccione un médico.")
            return

        medico_id = self.medicos_dict[nombre]
        citas = self.cita_service.filtrar_citas_por_medico(medico_id)
        self.mostrar_citas(citas)

    def buscar_por_paciente(self):
        nombre = self.filtro_paciente_cb.get()
        if not nombre:
            messagebox.showwarning("Atención", "Seleccione un paciente.")
            return

        paciente_id = self.pacientes_dict[nombre]
        citas = self.cita_service.filtrar_citas_por_paciente(paciente_id)
        self.mostrar_citas(citas)
    
    def buscar_por_fecha(self):
        fecha = self.filtro_fecha_entry.get().strip()
        if not fecha:
            messagebox.showwarning("Atención", "Ingrese una fecha.")
            return

        citas = self.cita_service.filtrar_citas_por_fecha(fecha)
        self.mostrar_citas(citas)

    def buscar_por_rango(self):
        inicio = self.fecha_inicio_entry.get().strip()
        fin = self.fecha_fin_entry.get().strip()

        if not inicio or not fin:
            messagebox.showwarning("Atención", "Ingrese ambas fechas.")
            return

        citas = self.cita_service.filtrar_citas_por_rango_fechas(inicio, fin)
        self.mostrar_citas(citas)

    

    def mostrar_citas(self, citas):
        # Limpia la tabla
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for c in citas:
            medico = self.medico_service.obtener_medico_por_id(c.medico_id)
            paciente = self.paciente_service.obtener_paciente_por_id(c.paciente_id)

            self.tabla.insert(
                "",
                "end",
                values=(
                    c.id,
                    paciente,
                    medico,
                    c.fecha_hora,
                    c.motivo,
                    c.estado
                )
            )

    def obtener_cita_seleccionada(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return None

        valores = self.tabla.item(seleccion[0], "values")
        return int(valores[0])  # El primer valor es el ID


    def cancelar_cita_ui(self):
        cita_id = self.obtener_cita_seleccionada()

        if not cita_id:
            messagebox.showwarning("Atención", "Seleccione una cita.")
            return

        confirmado = messagebox.askyesno(
            "Confirmar",
            "¿Estás seguro de cancelar esta cita?"
        )

        if not confirmado:
            return

        if self.cita_service.cancelar_cita(cita_id):
            messagebox.showinfo("Éxito", "La cita fue cancelada.")
            self.cargar_citas()
        else:
            messagebox.showerror("Error", "No se pudo cancelar la cita.")

    def marcar_completada(self):
        cita_id = self.obtener_cita_seleccionada()

        if not cita_id:
            messagebox.showwarning("Atención", "Seleccione una cita.")
            return

        confirmado = messagebox.askyesno(
            "Confirmar",
            "¿Marcar la cita como completada?"
        )

        if not confirmado:
            return

        if self.cita_service.completar_cita(cita_id):
            messagebox.showinfo("Éxito", "La cita fue marcada como completada.")
            self.cargar_citas()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el estado.")

    def quitar_filtros(self):
        # Limpiar campos de filtros
        self.estado_cb.set("")
        self.filtro_medico_cb.set("")
        self.filtro_paciente_cb.set("")
        self.filtro_fecha_entry.delete(0, tk.END)
        self.fecha_inicio_entry.delete(0, tk.END)
        self.fecha_fin_entry.delete(0, tk.END)

        # Cargar todas las citas nuevamente
        self.cargar_citas()

    def mostrar_filtro(self, event=None):
        # Ocultar todos los widgets
        widgets = [
            self.estado_label, self.estado_cb,
            self.medico_label, self.filtro_medico_cb,
            self.paciente_label, self.filtro_paciente_cb,
            self.fecha_label, self.filtro_fecha_entry,
            self.desde_label, self.fecha_inicio_entry,
            self.hasta_label, self.fecha_fin_entry,
            self.buscar_btn
        ]

        for w in widgets:
            w.grid_forget()

        tipo = self.filtro_tipo_cb.get()

        if tipo == "Estado":
            self.estado_label.grid(row=1, column=0, padx=5, pady=5)
            self.estado_cb.grid(row=1, column=1, padx=5, pady=5)

        elif tipo == "Médico":
            self.medico_label.grid(row=1, column=0, padx=5, pady=5)
            self.filtro_medico_cb.grid(row=1, column=1, padx=5, pady=5)

        elif tipo == "Paciente":
            self.paciente_label.grid(row=1, column=0, padx=5, pady=5)
            self.filtro_paciente_cb.grid(row=1, column=1, padx=5, pady=5)

        elif tipo == "Fecha":
            self.fecha_label.grid(row=1, column=0, padx=5, pady=5)
            self.filtro_fecha_entry.grid(row=1, column=1, padx=5, pady=5)

        elif tipo == "Rango":
            self.desde_label.grid(row=1, column=0, padx=5, pady=5)
            self.fecha_inicio_entry.grid(row=1, column=1, padx=5, pady=5)

            self.hasta_label.grid(row=2, column=0, padx=5, pady=5)
            self.fecha_fin_entry.grid(row=2, column=1, padx=5, pady=5)

        # Botón buscar siempre visible
        self.buscar_btn.grid(row=3, column=1, padx=5, pady=10)

    def ejecutar_busqueda(self):
        tipo = self.filtro_tipo_cb.get()

        if tipo == "Estado":
            self.buscar_por_estado()

        elif tipo == "Médico":
            self.buscar_por_medico()

        elif tipo == "Paciente":
            self.buscar_por_paciente()

        elif tipo == "Fecha":
            self.buscar_por_fecha()

        elif tipo == "Rango":
            self.buscar_por_rango()
