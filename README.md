### 📘 Proyecto del curso: Lenguajes de Programación  
# 🩺 Sistema de Gestión de Reservas de Consultas Médicas

---

## 📖 Descripción General

El **Sistema de Gestión de Reservas de Consultas Médicas** es una aplicación desarrollada en **Python** que permite registrar, administrar y consultar citas médicas de manera eficiente.  

El propósito del proyecto es demostrar la integración de **tres paradigmas de programación** —estructurada, orientada a objetos y funcional— aplicados a un problema realista, utilizando una **base de datos MySQL** para el almacenamiento de la información.

Este sistema permite registrar pacientes y médicos, asignar citas, cancelarlas, visualizar reportes y analizar estadísticas de atención mediante gráficos generados con librerías de análisis de datos.

---

## 🎯 Objetivos del Proyecto

### 🔹 Objetivo General
Desarrollar una aplicación multiparadigma en Python que permita gestionar de forma eficiente las reservas médicas, aplicando los paradigmas **estructurado**, **orientado a objetos** y **funcional**, con conexión a **MySQL** para la persistencia de datos.

### 🔹 Objetivos Específicos
- Implementar clases y objetos que representen a los actores principales del sistema: pacientes, médicos y citas.  
- Utilizar programación estructurada para el flujo principal del sistema (menús y opciones).  
- Emplear programación funcional (`map`, `filter`, `lambda`) en el procesamiento de datos y generación de reportes.  
- Establecer conexión con una base de datos MySQL para el registro y manejo de información.  
- Aplicar manejo de excepciones para evitar errores en la ejecución.  
- Generar reportes visuales utilizando librerías externas como `pandas` y `matplotlib`.

---

## 🧠 Paradigmas de Programación Aplicados

| Paradigma | Descripción | Ejemplo en el Proyecto |
|------------|--------------|------------------------|
| **Estructurado** | Control del flujo del programa mediante funciones y estructuras de decisión. | Menú principal con opciones de registro, consulta y reportes. |
| **Orientado a Objetos (POO)** | Modelado de entidades del sistema mediante clases, atributos y métodos. | Clases `Paciente`, `Medico`, `Cita` y `GestorCitas`. |
| **Funcional** | Uso de funciones puras, `map()`, `filter()`, y `lambda` para el análisis y filtrado de datos. | Filtrado de citas por fecha o especialidad y cálculo de estadísticas. |

---

| Tecnología / Librería | Uso principal                                 |
| ---------------------- | --------------------------------------------- |
| **Python 3.12+**       | Lenguaje de programación principal.           |
| **MySQL**              | Base de datos relacional para almacenamiento. |
| **mysql.connector**    | Conexión entre Python y MySQL.                |
| **pandas**             | Análisis y manipulación de datos.             |
| **matplotlib**         | Visualización gráfica de reportes.            |
| **datetime**           | Manejo de fechas y horas de las citas.        |
| **tabulate**           | Mostrar datos en formato tabular en consola.  |


