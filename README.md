# 📌 Sistema de Gestión Médica Integral

Proyecto grupal desarrollado para el curso **Lenguajes de Programación**.  
El objetivo es implementar un sistema de software en Python aplicando **programación multiparadigma** (estructurada, orientada a objetos y funcional) para gestionar información médica de manera integral.

### Integrantes del equipo
- *[Benites Ostos, Anthony Yonayquer]*
- *[Bravo Borjas, Sandro César]*
- *[Condor, Cristian Anderson Adriano]*
- *[Munives Santamaría, Fabricio Manuel]*

---

## 🎯 Objetivo del Proyecto

Desarrollar un software que permita gestionar pacientes, médicos y citas médicas, y generar reportes estadísticos, aplicando los 3 paradigmas de programación en Python:

| Paradigma | Aplicación en el proyecto |
|----------|----------------------------|
| **Estructurado** | Flujos secuenciales del menú principal y submenús. |
| **Orientado a Objetos** | Modelado de entidades: Paciente, Médico, Cita. |
| **Funcional** | Funciones puras para cálculos, filtros y estadísticas. |

---

## 🧪 Requisitos funcionales

| Código | Requisito |
|-------|-----------|
| RF-01 | Registrar pacientes |
| RF-02 | Registrar médicos |
| RF-03 | Registrar citas médicas |
| RF-04 | Listar entidades en tabla por consola |
| RF-05 | Editar / eliminar registros |
| RF-06 | Conectar a MySQL para almacenamiento persistente |
| RF-07 | Generar reportes con visualización gráfica (matplotlib) |

---

## 📂 Arquitectura del Proyecto

/Proyecto_Gestion_Medica
│
├─ main.py # Punto de entrada del sistema
│
├─ config/
│ └─ database_config.py # Conexión MySQL
│
├─ models/
│ ├─ paciente.py # Clase Paciente (POO)
│ ├─ medico.py # Clase Medico (POO)
│ └─ cita.py # Clase Cita (POO)
│
├─ services/
│ ├─ paciente_service.py # CRUD + lógica
│ ├─ medico_service.py
│ └─ cita_service.py
│
└─ ui/
├─ menu_principal.py
└─ menu_submodulos.py

---

       ┌────────────────────────┐
       │        UI (CLI)        │
       │ Menús / interacción    │
       └───────────▲────────────┘
                   │
       ┌───────────┴────────────┐
       │       SERVICES          │
       │ Validaciones / lógica   │
       └───────────▲────────────┘
                   │
       ┌───────────┴────────────┐
       │        MODELS           │
       │ Clases Paciente, etc.   │
       └───────────▲────────────┘
                   │
       ┌───────────┴────────────┐
       │     BASE DE DATOS      │
       │       MySQL            │
       └────────────────────────┘

---

## 🛠 Tecnologías Utilizadas

| Tecnología / Librería | Uso principal                                 |
| ---------------------- | --------------------------------------------- |
| **Python 3.12+**       | Lenguaje de programación principal.           |
| **MySQL**              | Base de datos relacional para almacenamiento. |
| **mysql.connector**    | Conexión entre Python y MySQL.                |
| **pandas**             | Análisis y manipulación de datos.             |
| **matplotlib**         | Visualización gráfica de reportes.            |
| **datetime**           | Manejo de fechas y horas de las citas.        |
| **tabulate**           | Mostrar datos en formato tabular en consola.  |

---

## 🧩 Justificación académica

Este proyecto aplica los 3 paradigmas del curso:

- **POO** para modelar entidades del dominio médico
- **Estructurada** para menús y flujo de interacción
- **Funcional** para filtros, estadísticas y cálculos puros

Además integra una base de datos real (MySQL) que añade persistencia, consultas y eficiencia de acceso, alineándose con el criterio de modelado completo del problema.

---

## ▶️ Ejecución

```bash
python main.py


