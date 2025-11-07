-- Se crea la base de datos
CREATE DATABASE gestion_medica;

-- Se abre la base de datos
USE gestion_medica;

-- Se crea la tabla 'pacientes'
CREATE TABLE pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    telefono VARCHAR(15) UNIQUE,
    fecha_nacimiento DATE
);

-- Se crea la tabla 'medicos'
CREATE TABLE medicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100),
    telefono VARCHAR(15) UNIQUE,
    email VARCHAR(100) UNIQUE
);

-- Se crea la tabla 'citas'
CREATE TABLE citas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT,
    medico_id INT,
    fecha_hora DATETIME,
    estado ENUM('programada', 'completada', 'cancelada') DEFAULT 'programada',
    motivo TEXT,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
    FOREIGN KEY (medico_id) REFERENCES medicos(id) ON DELETE CASCADE
);

-- Se muestra la tabla completa con sus datos
SELECT * FROM pacientes;
SELECT * FROM medicos;
SELECT * FROM citas;

-- Se elimina la base de datos
DROP DATABASE gestion_medica;