---
name: sql-server-architecture
description: "Arquitectura y administración de SQL Server. Cubre filegroups, backup/restore, alta disponibilidad y disaster recovery (Always On, log shipping, mirroring), particionamiento de tablas, data compression, Resource Governor, y configuración de TempDB. Actívala al diseñar infraestructura de base de datos, planear HA/DR, o configurar entornos productivos."
disable-model-invocation: true
---

# SQL Server Architecture & Administration

Guía de arquitectura, alta disponibilidad y administración de SQL Server. Cubre decisiones de infraestructura para producción.

---

## Filegroups y archivos

### Diseño recomendado

```sql
-- Múltiples filegroups para separar datos, índices e históricos
ALTER DATABASE MiApp ADD FILEGROUP DataFG;
ALTER DATABASE MiApp ADD FILEGROUP IndexFG;
ALTER DATABASE MiApp ADD FILEGROUP ArchiveFG;

ALTER DATABASE MiApp ADD FILE (
    NAME = 'MiApp_Data1',
    FILENAME = 'D:\Data\MiApp_Data1.mdf',
    SIZE = 10GB,
    MAXSIZE = 100GB,
    FILEGROWTH = 1GB
) TO FILEGROUP DataFG;

ALTER DATABASE MiApp ADD FILE (
    NAME = 'MiApp_Archive1',
    FILENAME = 'E:\Archive\MiApp_Archive1.mdf',
    SIZE = 100MB,
    MAXSIZE = UNLIMITED,
    FILEGROWTH = 500MB
) TO FILEGROUP ArchiveFG;
```

### Separación de objetos por filegroup

```sql
-- Tablas activas en FG Data
CREATE TABLE Sales.Orders (...) ON DataFG;

-- Índices en FG separado (reduce contención I/O)
CREATE NONCLUSTERED INDEX IX_Orders_CreatedAt ON Sales.Orders(CreatedAt)
    ON IndexFG;

-- Datos históricos en FG Archive (discos lentos/baratos)
CREATE PARTITION FUNCTION pf_Monthly(DATE)
    AS RANGE RIGHT FOR VALUES ('2023-01-01','2024-01-01','2025-01-01');

CREATE PARTITION SCHEME ps_Monthly
    AS PARTITION pf_Monthly
    TO (ArchiveFG, ArchiveFG, ArchiveFG, DataFG); -- 2025+ en DataFG
```

---

## TempDB

TempDB es la base de datos más crítica para rendimiento. Se recrea al reiniciar.

```sql
-- Configuración recomendada: 1 archivo de datos por core (máx 8)
-- Ej: 4 cores → 4 archivos TempDB
ALTER DATABASE tempdb ADD FILE (
    NAME = 'tempdev2',
    FILENAME = 'D:\TempDB\tempdev2.ndf',
    SIZE = 1GB,
    FILEGROWTH = 500MB
);
-- Repetir para tempdev3, tempdev4...

-- Todos los archivos del mismo tamaño y auto-growth igual.
-- Nombrar: tempdev2, tempdev3...
```

⚠️ **Nunca** poner TempDB en el mismo disco que los datos o logs. Usar discos SSD/NVMe más rápidos.

---

## Backup y Restore

### Estrategia de backup

| Tipo | Contenido | Frecuencia típica | Tamaño |
|------|-----------|-------------------|--------|
| **Full** | Toda la DB | Diario (madrugada) | Grande |
| **Differential** | Cambios desde el último full | Cada 4-6 horas | Mediano |
| **Transaction Log** | Transacciones desde último log backup | Cada 15-30 min | Pequeño |

### Comandos

```sql
-- Full
BACKUP DATABASE MiApp
TO DISK = 'E:\Backups\MiApp_Full_20251115_0200.bak'
WITH CHECKSUM, COMPRESSION, INIT, STATS = 10;

-- Differential
BACKUP DATABASE MiApp
TO DISK = 'E:\Backups\MiApp_Diff_20251115_0800.bak'
WITH DIFFERENTIAL, CHECKSUM, COMPRESSION, STATS = 10;

-- Transaction Log
BACKUP LOG MiApp
TO DISK = 'E:\Backups\MiApp_Log_20251115_0830.trn'
WITH CHECKSUM, COMPRESSION, STATS = 10;

-- Restore: FULL → (NORECOVERY) → DIFF/LOG → RECOVERY
RESTORE DATABASE MiApp FROM DISK = 'MiApp_Full.bak' WITH NORECOVERY;
RESTORE DATABASE MiApp FROM DISK = 'MiApp_Diff.bak' WITH NORECOVERY;
RESTORE LOG MiApp FROM DISK = 'MiApp_Log_0830.trn' WITH RECOVERY;

-- Point-in-time recovery
RESTORE LOG MiApp FROM DISK = 'MiApp_Log_1000.trn'
WITH STOPAT = '2025-11-15T09:45:00', RECOVERY;
```

✅ Recomendado: probar restores **mensualmente** en staging. Un backup no testeado no es un backup.

---

## Alta Disponibilidad (HA) y Disaster Recovery (DR)

### Always On Availability Groups (Enterprise)

```
Primary Replica                         Secondary Replica(s)
┌──────────────────┐       ┌──────────────────────────┐
│ SQL Server Node 1 │ ───── │ SQL Server Node 2 (Sync) │
│ (Read/Write)     │       │ (Read-Only / DR)          │
└──────────────────┘       └──────────────────────────┘
        │                               │
    WSFC Cluster                   Azure / Otra región
```

- **Synchronous commit**: cero pérdida de datos, latencia mínima.
- **Asynchronous commit**: posible pérdida de datos mínima, baja latencia.
- **Readable secondary**: reportes y queries de solo lectura contra réplicas.

### Basic Availability Groups (Standard Edition)

Similar a Always On pero con límites: una sola DB por grupo, sin réplicas legibles.

### Log Shipping

Alternativa simple y soportada en todas las ediciones. Copia backups de log a un secundario y los restaura.

```
Primary: BACKUP LOG → network → Secondary: RESTORE LOG
```

### Failover Cluster Instance (FCI)

Protección a nivel instancia (no DB). Un nodo asume si otro falla. Requiere storage compartido (SAN).

### Cuándo usar cada uno

| Escenario | Solución |
|-----------|----------|
| Zero data loss, failover automático | Always On Sync |
| DR cross-region, OK con segundos de pérdida | Always On Async |
| Presupuesto limitado, RPO ~15 min | Log Shipping |
| Protección de instancia completa | FCI |
| Base de datos única, baja complejidad | Log Shipping o Basic AG |

---

## Particionamiento de tablas

```sql
-- Partición por mes para datos históricos (>100M filas)
CREATE PARTITION FUNCTION pf_OrderCreated_Monthly(DATETIME2)
    AS RANGE RIGHT FOR VALUES (
        '2024-01-01','2024-02-01', ... '2025-12-01','2026-01-01'
    );

CREATE PARTITION SCHEME ps_OrderCreated_Monthly
    AS PARTITION pf_OrderCreated_Monthly
    TO (ArchiveFG, ArchiveFG, ..., DataFG);

-- Aplicar a tabla
CREATE TABLE Sales.Orders (
    ...
) ON ps_OrderCreated_Monthly(CreatedAt);

-- Switch de partición (archivado instantáneo)
ALTER TABLE Sales.Orders SWITCH PARTITION 1 TO Archive.Orders PARTITION 1;
```

---

## Data Compression

```sql
-- Compresión de página (mejor que ROW para OLTP con valores repetidos)
ALTER TABLE Sales.Orders REBUILD PARTITION = ALL
WITH (DATA_COMPRESSION = PAGE);

-- Compresión de índice
ALTER INDEX IX_Orders_CreatedAt ON Sales.Orders REBUILD
WITH (DATA_COMPRESSION = PAGE);

-- Evaluar ahorro antes de aplicar
EXEC sp_estimate_data_compression_savings
    @schema_name = 'Sales',
    @object_name = 'Orders',
    @index_id = NULL,
    @partition_number = NULL,
    @data_compression = 'PAGE';
```

| Compresión | Ahorro típico | Overhead CPU | Cuándo |
|------------|--------------|--------------|--------|
| NONE | 0% | 0% | Tablas pequeñas |
| ROW | 20-30% | Bajo | General |
| PAGE | 40-60% | Moderado | Tablas grandes, data warehouse |
| COLUMNSTORE | 70-90% | Bajo en lecturas | Data warehouse, analítica |

---

## Resource Governor

Limitar recursos por aplicación o usuario.

```sql
-- Crear resource pool
CREATE RESOURCE POOL ReportingPool
WITH (MAX_CPU_PERCENT = 20, MAX_MEMORY_PERCENT = 30);

-- Crear workload group
CREATE WORKLOAD GROUP ReportingGroup
USING ReportingPool;

-- Clasificar conexiones (ej: por application name)
CREATE FUNCTION dbo.Classifier()
RETURNS SYSNAME WITH SCHEMABINDING
AS
BEGIN
    DECLARE @group SYSNAME = 'default';
    IF APP_NAME() LIKE '%SSRS%'
        SET @group = 'ReportingGroup';
    RETURN @group;
END;

ALTER RESOURCE GOVERNOR WITH (CLASSIFIER_FUNCTION = dbo.Classifier);
ALTER RESOURCE GOVERNOR RECONFIGURE;
```

---

## Jobs y mantenimiento programado

```sql
-- Ola Hallengren Maintenance Solution (recomendado)
-- https://ola.hallengren.com

-- Backup diario
EXEC dbo.DatabaseBackup
    @Databases = 'USER_DATABASES',
    @Directory = 'E:\Backups',
    @BackupType = 'FULL',
    @Compress = 'Y';

-- Integrity check semanal
EXEC dbo.DatabaseIntegrityCheck
    @Databases = 'USER_DATABASES';

-- Index maintenance semanal
EXEC dbo.IndexOptimize
    @Databases = 'USER_DATABASES',
    @FragmentationLow = NULL,
    @FragmentationMedium = 'INDEX_REORGANIZE',
    @FragmentationHigh = 'INDEX_REBUILD_ONLINE',
    @UpdateStatistics = 'ALL',
    @OnlyModifiedStatistics = 'Y';
```

---

## Checklist de arquitectura

- [ ] TempDB: 1 archivo por core (máx 8), mismo tamaño, discos SSD separados
- [ ] Filegroups: datos separados de logs, índices en FG opcional
- [ ] Backups: full diario + diff cada 4-6h + log cada 15-30min
- [ ] Restore testeado mensualmente en staging
- [ ] HA/DR definida según RPO (pérdida) y RTO (tiempo de recuperación)
- [ ] Query Store habilitado
- [ ] Data compression evaluada en tablas >10GB
- [ ] Particionamiento para tablas >100M filas con historial
- [ ] Resource Governor si hay aplicaciones compitiendo por recursos
- [ ] Mantenimiento automatizado (Ola Hallengren o similar)
- [ ] Alertas configuradas (severity 17-25, errores 823/824/825)
