---
name: sql-server-deployment
description: "Despliegue de esquema y CI/CD de SQL Server (no acceso a datos): migraciones EF Core/Flyway/DbUp, SSDT/DACPAC/SqlPackage, Docker, scripts idempotentes y zero-downtime. Úsala al diseñar pipelines o planear despliegues."
disable-model-invocation: true
---

# SQL Server Deployment & Migrations

Guía de despliegue, migraciones y CI/CD para bases de datos SQL Server. La consigna: cambios de esquema repetibles, versionados y sin downtime.

---

## Estrategias de migración

### Comparativa de herramientas

| Herramienta | Enfoque | Ventaja | Cuándo |
|-------------|---------|---------|--------|
| **EF Core Migrations** | Code-first (C#) | Integración total con .NET, auto-detecta cambios | Apps .NET con EF Core |
| **Flyway** | Migration-first (SQL) | Control total del SQL, multi-engine | DevOps, control absoluto de la DB |
| **DbUp** | Migration-first (SQL) | Simple, .NET embebido, sin dependencias externas | Proyectos .NET sin EF |
| **SSDT / DACPAC** | State-based | Compara estado deseado vs actual | Entornos Microsoft puro |

### EF Core Migrations (recomendado para apps .NET)

```bash
# Crear migración
dotnet ef migrations add AddOrderShippingAddress -s src/App.Api -p src/App.Infrastructure

# Generar script SQL para revisión
dotnet ef migrations script -o migrate.sql --idempotent

# Aplicar en CI/CD
dotnet ef database update --connection "$CONNECTION_STRING"
```

```csharp
// Aplicación automática al iniciar (solo apps pequeñas/medianas)
var app = builder.Build();
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    await db.Database.MigrateAsync();
}
```

### Flyway (recomendado para control absoluto del SQL)

```
├── migrations/
│   ├── V001__Create_Sales_Schema.sql
│   ├── V002__Create_Orders_Table.sql
│   ├── V003__Add_OrderItems_Table.sql
│   ├── V004__Add_Status_Index_to_Orders.sql
│   └── ...
```

```sql
-- V001__Create_Sales_Schema.sql
CREATE SCHEMA Sales;
GO

-- V002__Create_Orders_Table.sql
CREATE TABLE Sales.Orders (
    Id              UNIQUEIDENTIFIER NOT NULL DEFAULT NEWSEQUENTIALID(),
    OrderNumber     INT NOT NULL,
    CustomerId      NVARCHAR(50) NOT NULL,
    Status          NVARCHAR(20) NOT NULL DEFAULT 'Pending',
    TotalAmount     DECIMAL(18,4) NOT NULL DEFAULT 0,
    CreatedAt       DATETIME2(3) NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_Orders PRIMARY KEY CLUSTERED (Id)
);
GO
```

```bash
# Ejecutar migraciones
flyway -url="$CONNECTION_STRING" -user="$DB_USER" -password="$DB_PASS" migrate

# Reparar migración fallida
flyway repair
```

### DbUp (simple, embebido en .NET)

```csharp
var connectionString = builder.Configuration.GetConnectionString("Default");

var upgrader = DeployChanges.To
    .SqlDatabase(connectionString)
    .WithScriptsEmbeddedInAssembly(Assembly.GetExecutingAssembly())
    .LogToConsole()
    .Build();

var result = upgrader.PerformUpgrade();
if (!result.Successful)
    throw result.Error;
```

---

## CI/CD Pipeline

### GitHub Actions con EF Core

```yaml
name: Database CI/CD

on:
  push:
    branches: [main]
    paths: ['src/Infrastructure/Migrations/**']

jobs:
  migrate:
    runs-on: ubuntu-latest
    services:
      sqlserver:
        image: mcr.microsoft.com/mssql/server:2022-latest
        env:
          ACCEPT_EULA: Y
          MSSQL_SA_PASSWORD: TestP@ss1234
        ports:
          - 1433:1433

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '10.0.x'
      - name: Install EF Core tools
        run: dotnet tool install --global dotnet-ef
      - name: Generate migration script
        run: dotnet ef migrations script --idempotent -o migrate.sql
      - name: Upload script as artifact
        uses: actions/upload-artifact@v4
        with:
          name: migration-script
          path: migrate.sql
```

### SSDT + SqlPackage (DACPAC)

```bash
# Build DACPAC desde proyecto SSDT
dotnet build src/Database/Database.sqlproj -c Release

# Generar script de deploy comparando DACPAC con servidor destino
sqlpackage /Action:Script \
    /SourceFile:Database.dacpac \
    /TargetConnectionString:"$CONNECTION_STRING" \
    /OutputPath:deploy.sql

# Ejecutar script
sqlcmd -S $SERVER -d $DATABASE -i deploy.sql
```

---

## Zero-Downtime Deployments

### Reglas para cambios de esquema sin downtime

| Cambio | ¿Seguro sin downtime? | Estrategia |
|--------|----------------------|------------|
| Agregar tabla | ✅ Sí | Crear tabla, deploy app, usar tabla |
| Agregar columna NULLABLE | ✅ Sí | `ALTER TABLE ADD Columna NVARCHAR NULL` |
| Agregar columna NOT NULL con DEFAULT | ✅ Sí (solo SQL 2012+) | `ADD Columna NOT NULL DEFAULT 'x' WITH VALUES` |
| Agregar columna NOT NULL sin DEFAULT | ⚠️ Con cuidado | Agregar nullable → backfill → hacer NOT NULL (2 migraciones) |
| Eliminar columna | ❌ Peligroso | App deja de escribir → esperar 1 deploy → eliminar columna |
| Renombrar columna | ❌ Peligroso | Agregar nueva → copiar datos → eliminar antigua (3 migraciones) |
| Agregar índice | ✅ Sí (con ONLINE = ON) | `CREATE INDEX ... WITH (ONLINE = ON)` |
| Cambiar tipo de columna | ❌ Peligroso | Agregar nueva columna → migrar datos → eliminar antigua |
| Split de tabla | ❌ | Múltiples fases con vistas o app-layer routing |

### Expansión y contracción de contrato

```
Fase 1 (Expand): Agregar nueva columna (nullable). App empieza a escribir en ambas.
Fase 2 (Migrate): Backfill de datos. App lee solo la nueva.
Fase 3 (Contract): App deja de escribir la antigua. Eliminar columna antigua.
```

---

## Scripts idempotentes

```sql
-- ✅ Idempotente: verifica existencia antes de crear
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'Sales')
    EXEC('CREATE SCHEMA Sales');

IF OBJECT_ID('Sales.Orders', 'U') IS NULL
    CREATE TABLE Sales.Orders (
        Id              UNIQUEIDENTIFIER NOT NULL DEFAULT NEWSEQUENTIALID(),
        ...
    );

-- Agregar columna si no existe
IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID('Sales.Orders') AND name = 'CancelledAt'
)
    ALTER TABLE Sales.Orders ADD CancelledAt DATETIME2(3) NULL;

-- Agregar índice si no existe
IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'IX_Orders_CustomerId_Status' AND object_id = OBJECT_ID('Sales.Orders')
)
    CREATE NONCLUSTERED INDEX IX_Orders_CustomerId_Status
    ON Sales.Orders(CustomerId, Status);
```

---

## Docker para desarrollo y CI

```yaml
# docker-compose.yml
services:
  sqlserver:
    image: mcr.microsoft.com/mssql/server:2022-latest
    environment:
      ACCEPT_EULA: "Y"
      MSSQL_SA_PASSWORD: "DevP@ssword123!"
    ports:
      - "1433:1433"
    volumes:
      - sqlserver-data:/var/opt/mssql
      - ./init-scripts:/docker-entrypoint-initdb.d

  # Para CI: usar TestContainers desde .NET
```

### Testcontainers (integration tests)

```csharp
public class DatabaseFixture : IAsyncLifetime
{
    private readonly MsSqlContainer _container = new MsSqlBuilder()
        .WithImage("mcr.microsoft.com/mssql/server:2022-latest")
        .WithPassword("TestP@ss123!")
        .Build();

    public string ConnectionString => _container.GetConnectionString();

    public async Task InitializeAsync()
    {
        await _container.StartAsync();
        // Aplicar migraciones
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseSqlServer(ConnectionString)
            .Options;
        await using var db = new AppDbContext(options);
        await db.Database.MigrateAsync();
    }

    public Task DisposeAsync() => _container.DisposeAsync();
}
```

---

## Post-deploy verification

```sql
-- Smoke test después de migrar
SELECT COUNT(*) AS OrderCount FROM Sales.Orders;
SELECT TOP 10 * FROM Sales.Orders ORDER BY CreatedAt DESC;
SELECT * FROM sys.migration_history; -- Flyway
SELECT * FROM dbo.__EFMigrationsHistory; -- EF Core
```

---

## Checklist de deployment

- [ ] Migraciones versionadas (naming claro: V001, V002 o timestamps)
- [ ] Scripts idempotentes (IF EXISTS, IF NOT EXISTS)
- [ ] Script de migración generado y revisado ANTES de aplicar en producción
- [ ] Zero-downtime strategy definida para cambios mayores
- [ ] CI/CD genera script de migración como artifact
- [ ] Rollback plan definido (o forward-only con expand/contract)
- [ ] Smoke test automático post-deploy
- [ ] Contenedor SQL Server para CI (Testcontainers) y desarrollo local (Docker)
- [ ] Backups tomados ANTES de migrar producción
- [ ] Migraciones irreversibles marcadas claramente
