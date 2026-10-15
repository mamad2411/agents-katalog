---
name: postgresql-deployment
description: "Despliegue y migraciones de PostgreSQL. Cubre estrategias de migración (Flyway, EF Core), backups lógicos y físicos (pg_dump, pg_basebackup), CI/CD, Docker, zero-downtime deployments, pg_upgrade para upgrades de versión mayor, y monitoreo de migraciones. Actívala al diseñar pipelines de CI/CD, configurar migraciones automáticas, o planear despliegues sin downtime."
disable-model-invocation: true
---

# PostgreSQL Deployment & Migrations

Guía de despliegue, migraciones y CI/CD para bases de datos PostgreSQL.

---

## Estrategias de migración

### Comparativa

| Herramienta | Enfoque | Ventaja |
|-------------|---------|---------|
| **Flyway** | Migration-first (SQL) | Control total del SQL, multi-engine, rollback opcional |
| **EF Core Migrations** | Code-first (C#) | Integración con .NET, auto-detecta cambios |
| **Sqitch** | Migration-first (SQL) | Sin números de versión, verify/revert/deploy |
| **pg_dump/pg_restore** | Snapshot | Backups y clonado de entornos |

### Flyway (recomendado para control SQL)

```
migrations/
├── V001__Create_Sales_Schema.sql
├── V002__Create_Orders_Table.sql
├── V003__Create_OrderItems_Table.sql
├── V004__Add_Index_Orders_Customer.sql
├── R__Refresh_Order_Summary_View.sql  -- Repeatable
└── U004__Drop_Index_Orders_Customer.sql -- Undo (opcional)
```

```sql
-- V002__Create_Orders_Table.sql
CREATE TABLE sales.orders (
    id              UUID DEFAULT uuidv7() PRIMARY KEY,
    order_number    INT GENERATED ALWAYS AS IDENTITY,
    customer_id     TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'Pending',
    total_amount    NUMERIC(18,4) NOT NULL DEFAULT 0,
    currency        TEXT NOT NULL DEFAULT 'MXN',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_orders_customer_id ON sales.orders (customer_id);
```

```bash
# Ejecutar migraciones
flyway -url="jdbc:postgresql://localhost:5432/miapp" \
       -user="app_user" -password="***" \
       migrate

# Verificar estado
flyway -url="..." info

# Reparar (después de arreglar manualmente una migración fallida)
flyway -url="..." repair
```

### EF Core Migrations para PostgreSQL

```bash
dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL

# Crear migración
dotnet ef migrations add AddOrderShippingAddress \
    -s src/App.Api -p src/App.Infrastructure

# Generar script SQL para revisión
dotnet ef migrations script -o migrate.sql --idempotent

# Aplicar
dotnet ef database update --connection "$CONNECTION_STRING"
```

---

## CI/CD Pipeline

### GitHub Actions con Flyway

```yaml
name: Database CI/CD

on:
  push:
    branches: [main]
    paths: ['migrations/**']

jobs:
  migrate-staging:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:18-alpine
        env:
          POSTGRES_DB: miapp
          POSTGRES_USER: flyway
          POSTGRES_PASSWORD: test_pass
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - name: Run Flyway migrations
        run: |
          docker run --rm --network host \
            -v $(pwd)/migrations:/flyway/sql \
            flyway/flyway \
            -url="jdbc:postgresql://localhost:5432/miapp" \
            -user=flyway -password=test_pass \
            migrate -validateMigrationNaming=true
```

### GitHub Actions con EF Core

```yaml
- name: Install EF Core tools
  run: dotnet tool install --global dotnet-ef
- name: Generate migration script
  run: dotnet ef migrations script --idempotent -o migrate.sql
- name: Upload artifact
  uses: actions/upload-artifact@v4
  with:
    name: migration-script
    path: migrate.sql
```

---

## Zero-Downtime Deployments

### Reglas de cambios sin downtime en PostgreSQL

| Cambio | ¿Seguro? | Estrategia |
|--------|----------|------------|
| Agregar tabla | ✅ | Directo |
| Agregar columna NULLABLE | ✅ | `ALTER TABLE ... ADD COLUMN` |
| Agregar columna NOT NULL con DEFAULT | ✅ (PG 11+) | `ADD COLUMN ... NOT NULL DEFAULT 'x'` — no reescribe la tabla |
| Agregar columna NOT NULL sin DEFAULT | ✅ (PG 18) | PG 18 no requiere table scan |
| Eliminar columna | ❌ | App deja de usar → migrar → eliminar |
| Renombrar columna | ❌ | Agregar nueva → migrar datos → eliminar antigua |
| Agregar índice | ✅ | `CREATE INDEX CONCURRENTLY` |
| Cambiar tipo de columna | ❌ | Agregar nueva → migrar → eliminar |
| Agregar constraint NOT NULL | ⚠️ | Primero `ADD CONSTRAINT ... NOT VALID`, luego `VALIDATE CONSTRAINT` |

### CREATE INDEX CONCURRENTLY

```sql
-- Sin CONCURRENTLY: bloquea escrituras en la tabla
CREATE INDEX idx_orders_status ON sales.orders (status);

-- ✅ CONCURRENTLY: no bloquea escrituras. Tarda más.
CREATE INDEX CONCURRENTLY idx_orders_status ON sales.orders (status);
```

### Expansión de contrato

```
Fase 1 (Expand): Agregar nueva columna (nullable). App escribe en ambas.
Fase 2 (Migrate): Backfill de datos. App lee solo la nueva.
Fase 3 (Contract): App deja de escribir la antigua. Eliminar columna antigua.
```

---

## pg_upgrade

Upgrades de versión mayor (ej: PG 17 → PG 18) con mínima downtime.

```bash
# 1. Instalar nueva versión
sudo apt install postgresql-18

# 2. Verificar compatibilidad
/usr/lib/postgresql/18/bin/pg_upgrade \
    --old-bindir /usr/lib/postgresql/17/bin \
    --new-bindir /usr/lib/postgresql/18/bin \
    --old-datadir /var/lib/postgresql/17/data \
    --new-datadir /var/lib/postgresql/18/data \
    --check

# 3. Ejecutar upgrade (--link usa hard links, instantáneo)
/usr/lib/postgresql/18/bin/pg_upgrade \
    --old-bindir /usr/lib/postgresql/17/bin \
    --new-bindir /usr/lib/postgresql/18/bin \
    --old-datadir /var/lib/postgresql/17/data \
    --new-datadir /var/lib/postgresql/18/data \
    --link --jobs=4

# PG 18+: estadísticas preservadas automáticamente durante pg_upgrade
```

---

## Backups y restore en CI

### Clonar producción para staging

```bash
# Backup de producción
pg_dump -h prod -U backup -d miapp -Fc -f prod_backup.dump

# Restore en staging (anonimizar datos PII opcional)
pg_restore -h staging -U deploy -d miapp --clean --if-exists prod_backup.dump
```

### Scripts idempotentes

```sql
-- ✅ Verificar existencia antes de crear
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'sales' AND tablename = 'orders') THEN
        CREATE TABLE sales.orders ( ... );
    END IF;
END $$;

-- Agregar columna si no existe
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'sales' AND table_name = 'orders' AND column_name = 'cancelled_at'
    ) THEN
        ALTER TABLE sales.orders ADD COLUMN cancelled_at TIMESTAMPTZ;
    END IF;
END $$;
```

---

## Docker

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:18-alpine
    environment:
      POSTGRES_DB: miapp
      POSTGRES_USER: app_user
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./init:/docker-entrypoint-initdb.d  # Scripts SQL que corren una sola vez
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app_user -d miapp"]
      interval: 5s
      timeout: 3s
      retries: 5
```

### Testcontainers con PostgreSQL

```csharp
public class DatabaseFixture : IAsyncLifetime
{
    private readonly PostgreSqlContainer _container = new PostgreSqlBuilder()
        .WithImage("postgres:18-alpine")
        .WithDatabase("miapp_test")
        .WithUsername("test_user")
        .WithPassword("test_pass")
        .Build();

    public string ConnectionString => _container.GetConnectionString();

    public async Task InitializeAsync()
    {
        await _container.StartAsync();
        // Aplicar migraciones
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseNpgsql(ConnectionString)
            .Options;
        await using var db = new AppDbContext(options);
        await db.Database.MigrateAsync();
    }

    public Task DisposeAsync() => _container.DisposeAsync();
}
```

---

## Deployment checklists

### Pre-deploy

- [ ] Script de migración generado y revisado
- [ ] `VACUUM ANALYZE` ejecutado en producción (estadísticas frescas)
- [ ] Backup tomado antes de migrar
- [ ] Rollback plan definido (o forward-only con expand/contract)
- [ ] Conexiones de app drenadas o en pausa

### Post-deploy

- [ ] Smoke test: `SELECT COUNT(*) FROM sales.orders`
- [ ] Flyway: `flyway info` muestra estado SUCCESS
- [ ] Índices creados con `CONCURRENTLY` terminaron sin errores
- [ ] Estadísticas actualizadas con `ANALYZE` después de cambios masivos
- [ ] App desplegada y funcionando contra la nueva versión del esquema

---

## Checklist de deployment

- [ ] Herramienta de migración definida (Flyway o EF Core)
- [ ] Migraciones versionadas con naming claro
- [ ] Scripts de migración generados y revisados ANTES de producción
- [ ] `CREATE INDEX CONCURRENTLY` para índices en producción
- [ ] Expansión de contrato para cambios de esquema complejos
- [ ] CI/CD incluye smoke test post-deploy
- [ ] Backups programados antes de cada deploy
- [ ] `pg_upgrade --check` antes de upgrades de versión mayor
- [ ] Docker Compose para desarrollo local
- [ ] Testcontainers para integration tests
- [ ] Rollback plan documentado
