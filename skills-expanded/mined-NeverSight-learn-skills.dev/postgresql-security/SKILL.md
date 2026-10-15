---
name: postgresql-security
description: "Seguridad en PostgreSQL. Cubre roles (rol de login, grupo), GRANT/REVOKE, Row-Level Security (RLS), SSL/TLS, pg_hba.conf, autenticación SCRAM-SHA-256, encriptación de columnas (pgcrypto), políticas de seguridad, y hardening de instancia. Actívala al asegurar bases de datos, diseñar esquemas de permisos multi-tenant, o implementar encriptación."
disable-model-invocation: true
---

# PostgreSQL Security

Guía de seguridad para PostgreSQL. Principio: mínimo privilegio. Conexiones TLS, autenticación fuerte, permisos granulares.

---

## Roles y autenticación

PostgreSQL no distingue usuarios de grupos: todo son **ROLEs**.

```sql
-- Crear rol de login (usuario)
CREATE ROLE app_user WITH LOGIN PASSWORD 'StrongP@ssw0rd!2025'
    CONNECTION LIMIT 50
    VALID UNTIL '2026-12-31';

-- Crear rol de grupo (sin login)
CREATE ROLE sales_readers;
CREATE ROLE sales_writers;
CREATE ROLE report_viewers;

-- Asignar roles a usuarios
GRANT sales_readers TO app_user;
GRANT sales_writers TO app_user;

-- Ver membresía
SELECT r.rolname, array_agg(m.rolname) AS member_of
FROM pg_roles r
LEFT JOIN pg_auth_members am ON r.oid = am.member
LEFT JOIN pg_roles m ON am.roleid = m.oid
WHERE r.rolcanlogin
GROUP BY r.rolname;
```

### Roles predefinidos de PostgreSQL

| Rol | Privilegio |
|-----|-----------|
| `pg_read_all_data` | SELECT en todas las tablas |
| `pg_write_all_data` | INSERT, UPDATE, DELETE en todas |
| `pg_read_all_stats` | Leer pg_stat_* |
| `pg_monitor` | Monitoreo completo |
| `pg_signal_backend` | Cancelar queries de otros |

```sql
-- Otorgar rol predefinido
GRANT pg_read_all_data TO report_viewers;
```

---

## Permisos (GRANT / REVOKE)

```sql
-- A nivel schema
GRANT USAGE ON SCHEMA sales TO sales_readers;
GRANT USAGE ON SCHEMA sales TO sales_writers;

-- A nivel tabla
GRANT SELECT ON ALL TABLES IN SCHEMA sales TO sales_readers;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA sales TO sales_writers;

-- A nivel columna
GRANT SELECT (id, customer_id, total_amount) ON sales.orders TO report_viewers;
-- report_viewers NO puede ver otras columnas.

-- A nivel secuencia
GRANT USAGE ON ALL SEQUENCES IN SCHEMA sales TO sales_writers;

-- A nivel función
GRANT EXECUTE ON FUNCTION sales.create_order TO sales_writers;

-- Para tablas futuras: ALTER DEFAULT PRIVILEGES
ALTER DEFAULT PRIVILEGES IN SCHEMA sales
    GRANT SELECT ON TABLES TO sales_readers;

ALTER DEFAULT PRIVILEGES IN SCHEMA sales
    GRANT SELECT, INSERT, UPDATE ON TABLES TO sales_writers;

-- Revocar
REVOKE DELETE ON ALL TABLES IN SCHEMA sales FROM sales_writers;
```

---

## pg_hba.conf (Host-Based Authentication)

Controla quién puede conectarse, desde dónde y cómo.

```conf
# TYPE  DATABASE  USER       ADDRESS          METHOD
local   all       postgres                    peer          # Socket local
local   all       all                         scram-sha-256 # Resto de usuarios locales
host    miapp     app_user   10.0.0.0/8       scram-sha-256
host    miapp     readonly   0.0.0.0/0        scram-sha-256
host    all       replicator 10.0.0.2/32      scram-sha-256
host    all       all        0.0.0.0/0        reject        # Bloquear todo lo demás
```

Métodos de autenticación:

| Método | Seguridad | Cuándo |
|--------|-----------|--------|
| `scram-sha-256` | ✅ Alta | **Default.** Password hasheado con SCRAM. |
| `cert` | ✅ Alta | Certificados SSL cliente. |
| `md5` | ❌ Débil | Legacy. Migrar a scram-sha-256. |
| `peer` | ✅ Alta | Conexiones locales (mismo usuario del SO). |
| `trust` | ❌ Ninguna | **Nunca** en producción. Solo dev local con Docker. |

```bash
# Recargar pg_hba.conf sin reiniciar
pg_ctl reload
# o
SELECT pg_reload_conf();
```

---

## Row-Level Security (RLS)

```sql
-- Habilitar RLS en la tabla
ALTER TABLE sales.orders ENABLE ROW LEVEL SECURITY;

-- Política: cada tenant ve solo sus órdenes
CREATE POLICY tenant_isolation ON sales.orders
    FOR ALL
    TO app_user
    USING (tenant_id = current_setting('app.tenant_id'));

-- La app establece el tenant al conectarse
SET app.tenant_id = 'tenant-123';
-- PostgreSQL automáticamente agrega: WHERE tenant_id = 'tenant-123' a todas las queries.

-- Política para admins (ven todo)
CREATE POLICY admin_all_access ON sales.orders
    FOR ALL
    TO admin_role
    USING (true);

-- Política de solo lectura para reportes
CREATE POLICY reports_read_only ON sales.orders
    FOR SELECT
    TO report_role
    USING (true);

-- Bypass RLS (solo superusuarios y BYPASSRLS)
ALTER ROLE db_admin BYPASSRLS;
```

---

## SSL/TLS

```bash
# Generar certificados
openssl req -new -x509 -days 365 -nodes \
    -out server.crt -keyout server.key \
    -subj "/CN=postgres"

# Configurar en postgresql.conf
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
```

```conf
# pg_hba.conf: forzar SSL para conexiones remotas
hostssl miapp   app_user   0.0.0.0/0   scram-sha-256
hostnossl miapp app_user   0.0.0.0/0   reject        # Bloquear no-SSL
```

```csharp
// Conexión desde .NET con SSL
// "Host=server;Database=miapp;SSL Mode=Require;Trust Server Certificate=false"
```

---

## Encriptación de datos

### pgcrypto

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Hashing (para passwords, nunca desencriptar)
UPDATE users SET password_hash = crypt('user_password', gen_salt('bf'));
SELECT (password_hash = crypt('user_password', password_hash)) AS match FROM users;

-- Encriptación simétrica (datos sensibles que necesitan desencriptarse)
INSERT INTO secure_data (encrypted_pii)
VALUES (pgp_sym_encrypt('SSN-123-45-6789', 'encryption_key'));

SELECT pgp_sym_decrypt(encrypted_pii, 'encryption_key') FROM secure_data;
-- ⚠️ La clave viaja en cada query. Manejar con cuidado.
```

### Encriptación a nivel de aplicación

Para datos altamente sensibles (PII, datos de tarjetas), encriptar/desencriptar en la aplicación antes de enviar a PostgreSQL. PostgreSQL nunca ve el texto plano.

---

## Hardening

```sql
-- Eliminar base de datos pública (todos pueden conectarse)
-- PostgreSQL 15+: se revoca permiso CREATE en public por defecto.
REVOKE CREATE ON SCHEMA public FROM PUBLIC;

-- Revocar permisos globales
REVOKE ALL ON DATABASE miapp FROM PUBLIC;

-- Deshabilitar login remoto para superuser
-- En pg_hba.conf: postgres solo puede conectarse localmente

-- Auditar conexiones
ALTER SYSTEM SET log_connections = on;
ALTER SYSTEM SET log_disconnections = on;
SELECT pg_reload_conf();

-- Timeout de sesión inactiva
ALTER SYSTEM SET idle_in_transaction_session_timeout = '15min';
SELECT pg_reload_conf();

-- Limitar intentos de conexión (extension)
-- CREATE EXTENSION auth_delay;
-- auth_delay.milliseconds = 500  (retraso después de login fallido)
```

---

## Checklist de seguridad

- [ ] Autenticación `scram-sha-256` (no md5, no trust)
- [ ] `pg_hba.conf` restrictivo: bloquear conexiones externas no autorizadas
- [ ] SSL habilitado para conexiones remotas
- [ ] RLS implementado si hay multi-tenancy en la misma DB
- [ ] Permisos granulares por rol (no usar superuser para apps)
- [ ] `public` schema con permisos revocados
- [ ] `log_connections` y `log_disconnections` habilitados
- [ ] `idle_in_transaction_session_timeout` configurado
- [ ] Password policy: longitud mínima, expiración, complejidad
- [ ] Datos PII encriptados (pgcrypto o a nivel aplicación)
- [ ] `CONNECTION LIMIT` configurado para roles de aplicación
- [ ] Extensiones no necesarias removidas
