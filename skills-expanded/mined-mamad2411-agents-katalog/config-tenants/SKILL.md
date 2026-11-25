---
name: config-tenants
description: Skill para implementar módulo de administración de Empresas/Inquilinos (Multi-tenant)
---

# Skill: config-tenants

## Propósito

Este skill genera un módulo completo de administración de **Tenants (Empresas/Inquilinos)** para aplicaciones multi-tenant. Incluye CRUD completo, gestión de logos, activación/desactivación y estadísticas.

---

## Variantes Disponibles

| Variante  | Descripción                                           |
|-----------|-------------------------------------------------------|
| **basic** | Solo CRUD de tenants                                  |
| **full**  | CRUD + logos + colores + suscripciones + estadísticas |

---

## Prerrequisitos

### Backend (Go)

- PostgreSQL con extensión UUID
- Gin framework
- sqlc para generación de código
- pgxpool para conexión a BD

### Frontend (Flutter)

- Dio para HTTP
- Provider o Bloc para estado
- file_picker para logos (variante full)

---

## Estructura de Archivos a Crear

```text
proyecto/
├── backend/
│   ├── internal/
│   │   ├── database/
│   │   │   └── queries/
│   │   │       └── tenants.sql          # Queries SQL
│   │   └── handlers/
│   │       └── tenants.go               # Handler REST
│   └── migrations/
│       └── 000001_create_tenants.up.sql # Schema
└── frontend/
    └── lib/
        └── features/
            └── tenants/
                ├── data/
                │   ├── models/
                │   │   └── tenant_model.dart
                │   └── datasources/
                │       └── tenant_datasource.dart
                ├── services/
                │   └── tenant_service.dart
                └── presentation/
                    └── widgets/
                        └── tenant_management_tab.dart
```

---

## Paso 1: Schema de Base de Datos

### Variante basic

```sql
-- Crear tabla de tenants/empresas
CREATE TABLE public.tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tenants_slug ON public.tenants(slug);
CREATE INDEX idx_tenants_active ON public.tenants(is_active);
```

### Variante full

```sql
CREATE TABLE public.tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    domain VARCHAR(255),
    logo_url TEXT,
    
    -- Colores del tema
    primary_color VARCHAR(20) DEFAULT '#1976D2',
    secondary_color VARCHAR(20) DEFAULT '#FF9800',
    tertiary_color VARCHAR(20) DEFAULT '#4CAF50',
    
    -- Estado
    is_active BOOLEAN DEFAULT true,
    
    -- Suscripción y límites
    subscription_plan VARCHAR(50) DEFAULT 'free',
    max_users INT DEFAULT 10,
    max_clients INT DEFAULT 100,
    
    -- Configuración extensible
    settings JSONB DEFAULT '{}',
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tenants_slug ON public.tenants(slug);
CREATE INDEX idx_tenants_domain ON public.tenants(domain);
CREATE INDEX idx_tenants_active ON public.tenants(is_active);

-- Trigger para updated_at
CREATE TRIGGER update_tenants_updated_at
    BEFORE UPDATE ON public.tenants
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## Paso 2: Queries SQL (sqlc)

Crear archivo `tenants.sql`:

```sql
-- name: CreateTenant :one
INSERT INTO public.tenants (
    name, slug, domain, logo_url,
    primary_color, secondary_color, tertiary_color,
    subscription_plan, max_users, max_clients, settings
)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
RETURNING *;

-- name: GetTenantByID :one
SELECT * FROM public.tenants WHERE id = $1;

-- name: GetTenantBySlug :one
SELECT * FROM public.tenants WHERE slug = $1;

-- name: ListTenants :many
SELECT * FROM public.tenants
ORDER BY name
LIMIT $1 OFFSET $2;

-- name: ListActiveTenants :many
SELECT * FROM public.tenants
WHERE is_active = true
ORDER BY name;

-- name: UpdateTenant :one
UPDATE public.tenants
SET name = $2,
    slug = $3,
    domain = $4,
    subscription_plan = $5,
    max_users = $6,
    max_clients = $7,
    updated_at = CURRENT_TIMESTAMP
WHERE id = $1
RETURNING *;

-- name: UpdateTenantLogo :one
UPDATE public.tenants
SET logo_url = $2,
    updated_at = CURRENT_TIMESTAMP
WHERE id = $1
RETURNING *;

-- name: UpdateTenantTheme :one
UPDATE public.tenants
SET primary_color = $2,
    secondary_color = $3,
    tertiary_color = $4,
    logo_url = $5,
    updated_at = CURRENT_TIMESTAMP
WHERE id = $1
RETURNING *;

-- name: UpdateTenantSettings :one
UPDATE public.tenants
SET settings = $2,
    updated_at = CURRENT_TIMESTAMP
WHERE id = $1
RETURNING *;

-- name: ActivateTenant :one
UPDATE public.tenants
SET is_active = true,
    updated_at = CURRENT_TIMESTAMP
WHERE id = $1
RETURNING *;

-- name: DeactivateTenant :one
UPDATE public.tenants
SET is_active = false,
    updated_at = CURRENT_TIMESTAMP
WHERE id = $1
RETURNING *;

-- name: CountTenants :one
SELECT COUNT(*) as total FROM public.tenants;

-- name: CountActiveTenants :one
SELECT COUNT(*) as total FROM public.tenants WHERE is_active = true;

-- name: DeleteTenant :exec
DELETE FROM public.tenants WHERE id = $1;
```

---

## Paso 3: Handler Go (Backend)

Ver template: `templates/backend/tenants_handler.go.tmpl`

### Endpoints REST

| Método | Ruta                    | Descripción                  |
|--------|-------------------------|------------------------------|
| GET    | /tenants                | Listar todos los tenants     |
| GET    | /tenants/:id            | Obtener tenant por ID        |
| POST   | /tenants                | Crear nuevo tenant           |
| PUT    | /tenants/:id            | Actualizar tenant            |
| PATCH  | /tenants/:id/activate   | Activar tenant               |
| PATCH  | /tenants/:id/deactivate | Desactivar tenant            |
| POST   | /tenants/:id/logo       | Subir logo (variante full)   |
| GET    | /tenants/stats          | Estadísticas (variante full) |

### Registro de Rutas

```go
// En main.go
tenantHandler := handlers.NewTenantHandler(db, queries, storageProvider)

tenants := v1.Group("/tenants")
{
    tenants.GET("", tenantHandler.ListTenants)
    tenants.GET("/:id", tenantHandler.GetTenant)
    tenants.POST("", tenantHandler.CreateTenant)
    tenants.PUT("/:id", tenantHandler.UpdateTenant)
    tenants.PATCH("/:id/activate", tenantHandler.ActivateTenant)
    tenants.PATCH("/:id/deactivate", tenantHandler.DeactivateTenant)
    
    // Variante full
    tenants.POST("/:id/logo", tenantHandler.UploadTenantLogo)
    tenants.GET("/stats", tenantHandler.GetTenantStats)
}
```

---

## Paso 4: DTOs (Go)

```go
// CreateTenantRequest para crear tenant
type CreateTenantRequest struct {
    Name             string `json:"name" binding:"required"`
    Slug             string `json:"slug" binding:"required"`
    Domain           string `json:"domain,omitempty"`
    PrimaryColor     string `json:"primary_color,omitempty"`
    SecondaryColor   string `json:"secondary_color,omitempty"`
    TertiaryColor    string `json:"tertiary_color,omitempty"`
    SubscriptionPlan string `json:"subscription_plan,omitempty"`
    MaxUsers         int    `json:"max_users,omitempty"`
    MaxClients       int    `json:"max_clients,omitempty"`
}

// UpdateTenantRequest para actualizar tenant
type UpdateTenantRequest struct {
    Name             string `json:"name" binding:"required"`
    Slug             string `json:"slug" binding:"required"`
    Domain           string `json:"domain,omitempty"`
    SubscriptionPlan string `json:"subscription_plan,omitempty"`
    MaxUsers         int    `json:"max_users,omitempty"`
    MaxClients       int    `json:"max_clients,omitempty"`
}

// TenantResponse respuesta de tenant
type TenantResponse struct {
    ID               string                 `json:"id"`
    Name             string                 `json:"name"`
    Slug             string                 `json:"slug"`
    Domain           *string                `json:"domain,omitempty"`
    LogoURL          *string                `json:"logo_url,omitempty"`
    PrimaryColor     *string                `json:"primary_color,omitempty"`
    SecondaryColor   *string                `json:"secondary_color,omitempty"`
    TertiaryColor    *string                `json:"tertiary_color,omitempty"`
    IsActive         bool                   `json:"is_active"`
    SubscriptionPlan *string                `json:"subscription_plan,omitempty"`
    MaxUsers         *int32                 `json:"max_users,omitempty"`
    MaxClients       *int32                 `json:"max_clients,omitempty"`
    Settings         map[string]interface{} `json:"settings,omitempty"`
    CreatedAt        string                 `json:"created_at"`
    UpdatedAt        string                 `json:"updated_at"`
}

// TenantStatsResponse estadísticas
type TenantStatsResponse struct {
    Total        int64 `json:"total"`
    Active       int64 `json:"active"`
    Inactive     int64 `json:"inactive"`
    TotalUsers   int64 `json:"total_users,omitempty"`
}
```

---

## Paso 5: Modelo Flutter

Ver template: `templates/frontend/tenant_model.dart.tmpl`

```dart
class Tenant {
  final String id;
  final String name;
  final String slug;
  final String? domain;
  final String? logoUrl;
  final String? primaryColor;
  final String? secondaryColor;
  final String? tertiaryColor;
  final bool isActive;
  final String? subscriptionPlan;
  final int? maxUsers;
  final int? maxClients;
  final Map<String, dynamic>? settings;
  final String createdAt;
  final String updatedAt;

  // constructor, fromJson, toJson, copyWith...
}
```

---

## Paso 6: DataSource Flutter

Ver template: `templates/frontend/tenant_datasource.dart.tmpl`

Interface:

- `getTeants({limit, offset})` → `List<Tenant>`
- `getTenant(id)` → `Tenant`
- `createTenant(request)` → `Tenant`
- `updateTenant(id, request)` → `Tenant`
- `activateTenant(id)` → `Tenant`
- `deactivateTenant(id)` → `Tenant`
- `uploadLogo(id, bytes, filename)` → `Tenant`

---

## Paso 7: Service Flutter

Ver template: `templates/frontend/tenant_service.dart.tmpl`

---

## Paso 8: Widget de Gestión Flutter

Ver template: `templates/frontend/tenant_management_tab.dart.tmpl`

Características:

- Tabla paginada con tenants
- Búsqueda por nombre/slug
- Indicadores de estado (activo/inactivo)
- Acciones: crear, editar, activar/desactivar
- Dialogo de formulario con selector de colores
- Preview de logo

---

## Consideraciones de Seguridad

1. **Autorización**: Solo super_admin puede gestionar tenants
2. **Validación de Slug**: Único y formato válido (solo letras, números, guiones)
3. **Límites**: Validar max_users y max_clients según plan
4. **Aislamiento**: Los usuarios normales no ven otros tenants

---

## Opciones de Configuración

| Opción                 | Default | Descripción                         |
|------------------------|---------|-------------------------------------|
| `ENABLE_DOMAINS`       | false   | Habilitar dominios personalizados   |
| `ENABLE_THEMES`        | true    | Permitir personalización de colores |
| `ENABLE_SUBSCRIPTIONS` | false   | Habilitar planes de suscripción     |
| `DEFAULT_MAX_USERS`    | 10      | Límite default de usuarios          |
| `DEFAULT_MAX_CLIENTS`  | 100     | Límite default de clientes          |

---

## Archivos de Template Incluidos

- `templates/backend/tenants_handler.go.tmpl`
- `templates/backend/tenants_queries.sql.tmpl`
- `templates/frontend/tenant_model.dart.tmpl`
- `templates/frontend/tenant_datasource.dart.tmpl`
- `templates/frontend/tenant_service.dart.tmpl`
- `templates/frontend/tenant_management_tab.dart.tmpl`
