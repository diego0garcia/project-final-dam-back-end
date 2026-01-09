CREATE TABLE IF NOT EXISTS usuario(
dni VARCHAR(9) NOT NULL PRIMARY KEY,
username VARCHAR(100) NOT NULL UNIKE,
nombre VARCHAR(100) NOT NULL,
email VARCHAR(100),
tlf VARCHAR(9) NOT NULL
);

CREATE TABLE alumno(
    nia INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    tlf VARCHAR(20),
    gmail VARCHAR(100),
    curso VARCHAR(50),
    PRIMARY KEY (nia)
);

CREATE TABLE IF NOT EXISTS asignatura(
id INT PRIMARY KEY AUTO_INCREMENT,
horas INT NOT NULL,
curso VARCHAR(50) NOT NULL,
nia_alumno INT(11) NOT NULL,
CONSTRAINT fk_nia_alumno FOREIGN KEY (nia_alumno) REFERENCES alumno(nia)
);

CREATE TABLE IF NOT EXISTS horario(
id INT PRIMARY KEY AUTO_INCREMENT,
h_inicio TIME NOT NULL,
h_final TIME NOT NULL,
dia DATE NOT NULL,
id_asignatura INT NOT NULL,
dni_usuario VARCHAR(9) NOT NULL,
CONSTRAINT pk_horario_id_asignatura FOREIGN KEY (id_asignatura) REFERENCES asignatura(id) ON DELETE CASCADE,
CONSTRAINT fk_matriculado_dni_usuario FOREIGN KEY (dni_usuario) REFERENCES usuario(dni) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS matriculado(
nia_alumno INT(11) NOT NULL,
id_asignatura INT NOT NULL,
CONSTRAINT pk_matriculado PRIMARY KEY (nia_alumno, id_asignatura),
CONSTRAINT fk_matriculado_nia_alumno FOREIGN KEY (nia_alumno) REFERENCES alumno(nia) ON DELETE CASCADE,
CONSTRAINT fk_matriculado_id_asignatura FOREIGN KEY (id_asignatura) REFERENCES asignatura(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS root(
dni_usuario VARCHAR(9) NOT NULL PRIMARY KEY,
CONSTRAINT fk_root_dni_usuario FOREIGN KEY (dni_usuario) REFERENCES usuario(dni) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS expediente(
id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
nia_alumno INT(11) NOT NULL,
accion VARCHAR(500) NOT NULL,
resultado VARCHAR(500) NOT NULL,
CONSTRAINT fk_expediente_nia_alumno FOREIGN KEY (nia_alumno) REFERENCES alumno(nia) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS notificacion(
id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
nia_alumno INT NOT NULL,
dni_usuario VARCHAR(9) NOT NULL,
descripcion VARCHAR(500) NOT NULL,
hora DATETIME NOT NULL,
CONSTRAINT fk_notificacion_nia_alumno FOREIGN KEY (nia_alumno) REFERENCES alumno(nia) ON DELETE CASCADE,
CONSTRAINT fk_notificacion_dni_usuario FOREIGN KEY (dni_usuario) REFERENCES usuario(dni) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS amonestacion(
id_notificacion INT NOT NULL PRIMARY KEY,
descripcion VARCHAR(500) NOT NULL,
CONSTRAINT fk_amonestacion_id_notificacion FOREIGN KEY (id_notificacion) REFERENCES notificacion(id) ON DELETE CASCADE
);

CREATE TABLE profesorg (
    dni_usuario VARCHAR(9) PRIMARY KEY,
    dpto VARCHAR(100),
    CONSTRAINT fk_profesor_dni_usuario FOREIGN KEY (dni_usuario) REFERENCES usuario(dni) ON DELETE CASCADE
);

CREATE TABLE directiva(
    dni_usuario VARCHAR(9) PRIMARY KEY,
    cargo VARCHAR(100),
    CONSTRAINT fk_directiva_dni_usuario FOREIGN KEY (dni_usuario) REFERENCES usuario(dni) ON DELETE CASCADE
);

CREATE TABLE previ(
    id INT PRIMARY KEY NOT NULL,
    causa VARCHAR(100),
    descripcion VARCHAR(100),
    nia_alumno int,
    CONSTRAINT fk_previ_dni_nia_alumno FOREIGN KEY (nia_alumno) REFERENCES alumno(nia) ON DELETE CASCADE
);

CREATE TABLE reconocimiento(
    id_notificacion INT PRIMARY KEY NOT NULL,
    tipo VARCHAR(100),
    CONSTRAINT fk_reconocimiento_id_notificacion_tipo FOREIGN KEY (id_notificacion) REFERENCES notificacion(id) ON DELETE CASCADE
);