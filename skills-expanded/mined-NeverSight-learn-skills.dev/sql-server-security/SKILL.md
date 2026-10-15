---
name: sql-server-security
description: "Seguridad en SQL Server. Cubre autenticación (Windows y SQL Server), logins, usuarios, roles, permisos (GRANT/DENY/REVOKE), TDE (Transparent Data Encryption), Always Encrypted, Row-Level Security (RLS), Dynamic Data Masking, SQL Injection prevention, y hardening de instancia. Actívala al asegurar bases de datos, diseñar esquemas de permisos, o implementar encriptación."
disable-model-invocation: true
---

# SQL Server Security

Guía de seguridad para SQL Server. Principio: mínimo privilegio necesario. Todo acceso explícito, nada implícito.

---

## Autenticación

### Modos

| Modo | Descripción | Recomendación |
|------|-------------|---------------|
| **Windows Authentication** | Usa usuarios/grupos de Active Directory | ✅ Preferido. AD maneja passwords y políticas. |
| **SQL Server Authentication** | Logins SQL con password local | ⚠️ Solo si Windows Auth no es posible (apps legacy, Linux). |
| **Mixed Mode** | Ambos | Default común. Hardening: deshabilitar `sa`, usar AD. |

```sql
-- Ver modo actual
SELECT SERVERPROPERTY('IsIntegratedSecurityOnly'); -- 1 = Windows only

-- Crear login SQL (solo si es necesario)
CREATE LOGIN AppUser WITH PASSWORD = 'StrongP@ssw0rd!2025'
    CHECK_POLICY = ON,  -- Respeta políticas de AD
    CHECK_EXPIRATION = ON;
```

### Usuarios contenidos (Contained Database)

```sql
-- Habilitar contained DB (autenticación a nivel DB, sin login de servidor)
ALTER DATABASE MiApp SET CONTAINMENT = PARTIAL;

CREATE USER ApiUser WITH PASSWORD = 'StrongP@ssw0rd!2025';
-- Útil para Always On: usuario viaja con la DB entre réplicas.
```

---

## Roles

### Server-level

```sql
-- Roles fijos de servidor
ALTER SERVER ROLE sysadmin    ADD MEMBER [DOMAIN\DBA];
ALTER SERVER ROLE securityadmin ADD MEMBER [DOMAIN\SecurityAdmin];
ALTER SERVER ROLE dbcreator   ADD MEMBER [DOMAIN\AppDeployer];
ALTER SERVER ROLE processadmin ADD MEMBER [DOMAIN\Operator]; -- Kill processes
-- ❌ Nunca sysadmin para cuentas de aplicación.

-- Roles definidos por usuario (SQL 2012+)
CREATE SERVER ROLE AppManagers;
ALTER SERVER ROLE AppManagers ADD MEMBER [DOMAIN\TeamLead];
```

### Database-level

```sql
-- Roles fijos de base de datos
ALTER ROLE db_datareader  ADD MEMBER ApiUser;
ALTER ROLE db_datawriter   ADD MEMBER ApiUser;
ALTER ROLE db_ddladmin     ADD MEMBER DeveloperUser;
ALTER ROLE db_owner        ADD MEMBER DbaUser;
-- ❌ Nunca db_owner para cuentas de aplicación.

-- Roles definidos por usuario (granular)
CREATE ROLE SalesReaders;
CREATE ROLE SalesWriters;
CREATE ROLE ReportViewers;

-- Permisos al rol, no al usuario
GRANT SELECT, INSERT, UPDATE ON SCHEMA::Sales TO SalesWriters;
GRANT SELECT ON SCHEMA::Sales TO SalesReaders;
GRANT SELECT ON SCHEMA::Audit TO ReportViewers;
```

---

## Permisos (GRANT / DENY / REVOKE)

```sql
-- GRANT: otorgar permiso
GRANT SELECT ON Sales.Orders TO SalesReaders;
GRANT EXECUTE ON Sales.usp_CreateOrder TO SalesWriters;

-- DENY: denegar explícitamente (prevalece sobre GRANT)
DENY DELETE ON Sales.Orders TO SalesWriters;

-- Permisos a nivel schema (recomendado)
GRANT SELECT, INSERT, UPDATE ON SCHEMA::Sales TO SalesWriters;
GRANT SELECT ON SCHEMA::Catalog TO Public; -- Todos pueden leer catálogo

-- Ver permisos de un usuario
EXEC sp_helprotect @username = 'SalesWriters';
```

### Jerarquía: DENY > GRANT > REVOKE

---

## Transparent Data Encryption (TDE)

Encripta datos en reposo (archivos .mdf, .ldf, backups).

```sql
-- Crear master key y certificate
USE master;
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'StrongMasterKeyP@ss!';
CREATE CERTIFICATE TdeCert WITH SUBJECT = 'TDE Certificate';

-- Habilitar TDE en la DB
USE MiApp;
CREATE DATABASE ENCRYPTION KEY
WITH ALGORITHM = AES_256
ENCRYPTION BY SERVER CERTIFICATE TdeCert;

ALTER DATABASE MiApp SET ENCRYPTION ON;

-- Monitorear progreso
SELECT
    database_id,
    encryption_state,        -- 3 = Encrypted
    percent_complete,
    key_algorithm,
    key_length
FROM sys.dm_database_encryption_keys;
```

⚠️ **Backup del certificado TDE es crítico.** Si se pierde: base de datos irrecuperable.

```sql
BACKUP CERTIFICATE TdeCert TO FILE = 'E:\SecureBackup\TdeCert.cer'
WITH PRIVATE KEY (
    FILE = 'E:\SecureBackup\TdeCert.pvk',
    ENCRYPTION BY PASSWORD = 'PrivateKeyP@ss!'
);
```

---

## Always Encrypted

Encripta columnas específicas. La clave nunca está en SQL Server, solo en el cliente.

```sql
-- Column Master Key (se crea desde SSMS o PowerShell)
CREATE COLUMN MASTER KEY Cmk_CustomerPii
WITH (
    KEY_STORE_PROVIDER_NAME = 'MSSQL_CERTIFICATE_STORE',
    KEY_PATH = 'CurrentUser/My/A1B2C3D4E5F6...'
);

-- Column Encryption Key
CREATE COLUMN ENCRYPTION KEY Cek_CustomerPii
WITH VALUES (
    COLUMN_MASTER_KEY = Cmk_CustomerPii,
    ALGORITHM = 'RSA_OAEP',
    ENCRYPTED_VALUE = 0x...
);

-- Tabla con columnas encriptadas
CREATE TABLE Customers (
    Id INT NOT NULL,
    Name NVARCHAR(100) NOT NULL,
    SSN NCHAR(11)
        COLLATE Latin1_General_BIN2
        ENCRYPTED WITH (
            ENCRYPTION_TYPE = DETERMINISTIC,  -- Permite JOINs, equality
            ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256',
            COLUMN_ENCRYPTION_KEY = Cek_CustomerPii
        ) NULL,
    Salary DECIMAL(18,4)
        ENCRYPTED WITH (
            ENCRYPTION_TYPE = RANDOMIZED,     -- Más seguro, no permite equality
            ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256',
            COLUMN_ENCRYPTION_KEY = Cek_CustomerPii
        ) NULL
);
```

⚠️ Limitaciones: no LIKE, no range queries (RANDOMIZED), no `MAX`, no full-text en columnas encriptadas.

---

## Row-Level Security (RLS)

Restringe filas visibles según el usuario, dentro de SQL Server.

```sql
-- Tabla con TenantId
CREATE TABLE Sales.Orders (
    Id INT NOT NULL,
    TenantId NVARCHAR(50) NOT NULL,
    ...
);

-- Predicate function
CREATE FUNCTION Security.fn_TenantAccessPredicate(@TenantId NVARCHAR(50))
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN SELECT 1 AS AccessResult
WHERE @TenantId = SESSION_CONTEXT(N'TenantId')
   OR IS_MEMBER('db_owner') = 1;

-- Security policy
CREATE SECURITY POLICY Sales.Orders_SecurityPolicy
ADD FILTER PREDICATE Security.fn_TenantAccessPredicate(TenantId) ON Sales.Orders,
ADD BLOCK PREDICATE Security.fn_TenantAccessPredicate(TenantId) ON Sales.Orders
WITH (STATE = ON);

-- La app establece el tenant al conectarse
EXEC sp_set_session_context N'TenantId', @TenantId;
-- Ahora todas las queries filtran automáticamente por TenantId.
```

---

## Dynamic Data Masking

Oculta datos sensibles a usuarios no autorizados. No encripta, solo oculta en output.

```sql
CREATE TABLE Customers (
    Id INT NOT NULL,
    FirstName NVARCHAR(100) MASKED WITH (FUNCTION = 'partial(1,"XXX",1)'),
    LastName  NVARCHAR(100) MASKED WITH (FUNCTION = 'default()'),
    Email     NVARCHAR(200) MASKED WITH (FUNCTION = 'email()'),
    SSN       NCHAR(11)     MASKED WITH (FUNCTION = 'partial(0,"XXX-XX-",4)')
);

-- Usuarios sin UNMASK ven: FXXXt, xxxx, aXXX@XXXX.com, XXX-XX-1234
-- Usuarios con UNMASK ven los valores reales
GRANT UNMASK TO SecurityAdmin;
```

⚠️ No es encriptación. Usuarios con permisos de escritura pueden inferir valores reales con queries.

---

## SQL Injection Prevention

```sql
-- ❌ Vulnerable: concatenación de strings
SET @sql = 'SELECT * FROM Orders WHERE CustomerId = ''' + @customerId + '''';
EXEC (@sql);

-- ✅ Parametrizado siempre
CREATE PROCEDURE Sales.usp_GetOrders
    @customerId NVARCHAR(50)
AS
BEGIN
    SELECT * FROM Sales.Orders WHERE CustomerId = @customerId;
END;

-- ✅ Para SQL dinámico: sp_executesql con parámetros
DECLARE @sql NVARCHAR(MAX) = N'SELECT * FROM Sales.Orders WHERE CustomerId = @cid';
EXEC sp_executesql @sql, N'@cid NVARCHAR(50)', @cid = @customerId;
```

Reglas anti-injection:
- **Nunca** concatenar input del usuario en SQL.
- Usar **procedimientos almacenados** con parámetros o **sp_executesql**.
- En .NET: usar `SqlParameter` siempre, nunca `string.Format`.
- Validar y sanitizar input en la capa de aplicación también (defense in depth).

---

## Hardening de instancia

```sql
-- Deshabilitar xp_cmdshell (acceso a shell del SO)
EXEC sp_configure 'xp_cmdshell', 0;
RECONFIGURE;

-- Deshabilitar procedimientos de automatización OLE
EXEC sp_configure 'Ole Automation Procedures', 0;
RECONFIGURE;

-- Deshabilitar CLR si no se usa
EXEC sp_configure 'clr enabled', 0;
RECONFIGURE;

-- Renombrar o deshabilitar cuenta SA
ALTER LOGIN sa DISABLE;

-- Forzar conexiones cifradas (TLS)
-- En SQL Server Configuration Manager: Protocolos → Propiedades → Force Encryption = Yes
```

---

## Checklist de seguridad

- [ ] Windows Authentication preferido; `sa` deshabilitado
- [ ] Permisos asignados a roles, no directamente a usuarios
- [ ] Principio de mínimo privilegio: SELECT solo lo necesario, sin db_owner para apps
- [ ] TDE habilitado en producción (si se requiere encriptación en reposo)
- [ ] Always Encrypted para datos PII sensibles (SSN, salarios)
- [ ] RLS implementado si hay multi-tenancy en la misma DB
- [ ] SQL Injection prevenido: todo parametrizado, nada concatenado
- [ ] `xp_cmdshell` y `Ole Automation` deshabilitados
- [ ] TLS forzado en conexiones externas
- [ ] Backup del certificado TDE guardado en lugar seguro
- [ ] Auditoría de logins fallidos habilitada (`LOGIN FAILED` en error log)
- [ ] Dynamic Data Masking aplicado a columnas PII en entornos dev/test
