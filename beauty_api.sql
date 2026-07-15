-- beauty_api.sql
CREATE SCHEMA IF NOT EXISTS beauty_api;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS beauty_api.usuario(
 id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
 rol VARCHAR(20) NOT NULL CHECK (rol IN ('Admin','Estilista')),
 activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS beauty_api.estilista(
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 usuario_id UUID UNIQUE NOT NULL REFERENCES beauty_api.usuario(id) ON DELETE CASCADE,
 nombre VARCHAR(150) NOT NULL,
 especialidad VARCHAR(100),
 hora_entrada TIME NOT NULL,
 hora_salida TIME NOT NULL
);

CREATE TABLE IF NOT EXISTS beauty_api.cliente(
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 nombre_completo VARCHAR(150) NOT NULL,
 telefono VARCHAR(20),
 email VARCHAR(255),
 observaciones TEXT
);

CREATE TABLE IF NOT EXISTS beauty_api.servicio(
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 nombre VARCHAR(100) NOT NULL,
 descripcion TEXT,
 duracion_minutos INT NOT NULL,
 precio DECIMAL(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS beauty_api.cita(
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 cliente_id UUID NOT NULL REFERENCES beauty_api.cliente(id),
 estilista_id UUID NOT NULL REFERENCES beauty_api.estilista(id),
 servicio_id UUID NOT NULL REFERENCES beauty_api.servicio(id),
 fecha_hora TIMESTAMP NOT NULL,
 estado VARCHAR(20) NOT NULL DEFAULT 'Pendiente'
 CHECK (estado IN ('Pendiente','Confirmada','Cancelada','Completada'))
);

CREATE TABLE IF NOT EXISTS beauty_api.notificacion(
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 cita_id UUID NOT NULL REFERENCES beauty_api.cita(id) ON DELETE CASCADE,
 tipo VARCHAR(20) CHECK(tipo IN ('Recordatorio','Confirmacion','Cancelacion')),
 estado VARCHAR(20) DEFAULT 'Pendiente'
 CHECK(estado IN ('Pendiente','Enviado'))
);

CREATE TABLE IF NOT EXISTS beauty_api.historial_cita(
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 cita_id UUID NOT NULL REFERENCES beauty_api.cita(id) ON DELETE CASCADE,
 accion_realizada VARCHAR(30) CHECK(accion_realizada IN ('Modificacion','Cancelacion')),
 fecha_modificacion TIMESTAMP DEFAULT now(),
 usuario_responsable UUID NOT NULL REFERENCES beauty_api.usuario(id)
);

ALTER TABLE beauty_api.usuario ENABLE ROW LEVEL SECURITY;
ALTER TABLE beauty_api.estilista ENABLE ROW LEVEL SECURITY;
ALTER TABLE beauty_api.cliente ENABLE ROW LEVEL SECURITY;
ALTER TABLE beauty_api.servicio ENABLE ROW LEVEL SECURITY;
ALTER TABLE beauty_api.cita ENABLE ROW LEVEL SECURITY;
ALTER TABLE beauty_api.notificacion ENABLE ROW LEVEL SECURITY;
ALTER TABLE beauty_api.historial_cita ENABLE ROW LEVEL SECURITY;

CREATE POLICY usuario_select ON beauty_api.usuario
FOR SELECT TO authenticated USING(id=auth.uid());
CREATE POLICY usuario_insert ON beauty_api.usuario
FOR INSERT TO authenticated WITH CHECK(id=auth.uid());
CREATE POLICY usuario_update ON beauty_api.usuario
FOR UPDATE TO authenticated USING(id=auth.uid()) WITH CHECK(id=auth.uid());

CREATE POLICY estilista_self ON beauty_api.estilista
FOR ALL TO authenticated
USING(usuario_id=auth.uid())
WITH CHECK(usuario_id=auth.uid());

CREATE POLICY cliente_auth ON beauty_api.cliente
FOR ALL TO authenticated USING(true) WITH CHECK(true);
CREATE POLICY servicio_auth ON beauty_api.servicio
FOR ALL TO authenticated USING(true) WITH CHECK(true);
CREATE POLICY cita_auth ON beauty_api.cita
FOR ALL TO authenticated USING(true) WITH CHECK(true);
CREATE POLICY notif_auth ON beauty_api.notificacion
FOR ALL TO authenticated USING(true) WITH CHECK(true);
CREATE POLICY historial_auth ON beauty_api.historial_cita
FOR ALL TO authenticated USING(true) WITH CHECK(true);

INSERT INTO beauty_api.servicio(id,nombre,descripcion,duracion_minutos,precio) VALUES
(gen_random_uuid(),'Corte','Corte de cabello',45,15.00),
(gen_random_uuid(),'Tinte','Coloración',120,45.00),
(gen_random_uuid(),'Peinado','Peinado profesional',60,20.00);

INSERT INTO beauty_api.cliente(id,nombre_completo,telefono,email,observaciones) VALUES
(gen_random_uuid(),'María Pérez','0999999999','maria@example.com',''),
(gen_random_uuid(),'Juan López','0988888888','juan@example.com','');
