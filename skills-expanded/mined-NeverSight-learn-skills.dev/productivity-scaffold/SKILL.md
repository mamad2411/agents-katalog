---
name: productivity-scaffold
description: Genera la estructura inicial de un proyecto a partir de una especificación técnica (productivity-spec). Crea árbol de directorios, archivos base (entry point, config, linters), Dockerfile, CI pipeline inicial, y todo el boilerplate según la arquitectura del dev-kit del stack elegido. Úsala después de productivity-spec o cuando el usuario pida "crear proyecto", "scaffold", "inicializar el repo", o "generar boilerplate" para un stack específico.
disable-model-invocation: true
requires-devkits: auto-detect
---

# Productivity Scaffold — Spec a Proyecto

Convierte una especificación técnica en una estructura de proyecto lista para empezar a codificar.

---

## Workflow

### Paso 1: Detectar stack objetivo

Si viene de `productivity-spec`, el stack ya está identificado. Si no, pregunta:

1. **Stack**: backend + frontend + base de datos
2. **Framework**: dentro del stack, cuál (ej: "Express" o "Fastify" para Node.js)
3. **Arquitectura**: default del dev-kit o custom (ej: "Clean Architecture" o "Vertical Slices")

Carga los dev-kits correspondientes para respetar su estructura.

### Paso 2: Generar estructura de directorios

Según el stack, genera el árbol completo:

#### .NET + SQL Server

```
Solution.sln
src/
├── MiApp.Api/
│   ├── Endpoints/
│   │   └── Orders/
│   │       ├── CreateOrder.cs
│   │       ├── GetOrderById.cs
│   │       └── ListOrders.cs
│   ├── Middleware/
│   │   ├── ExceptionHandler.cs
│   │   └── RequestIdMiddleware.cs
│   ├── Program.cs
│   ├── appsettings.json
│   └── MiApp.Api.csproj
├── MiApp.Application/
│   └── Orders/
│       ├── CreateOrder/
│       │   ├── CreateOrderCommand.cs
│       │   ├── CreateOrderHandler.cs
│       │   └── CreateOrderValidator.cs
│       └── GetOrder/
│           ├── GetOrderQuery.cs
│           └── GetOrderHandler.cs
├── MiApp.Domain/
│   └── Orders/
│       ├── Order.cs
│       ├── OrderItem.cs
│       └── OrderStatus.cs
└── MiApp.Infrastructure/
    ├── Data/
    │   ├── AppDbContext.cs
    │   └── Configurations/
    │       └── OrderConfiguration.cs
    └── Services/
        └── EmailService.cs
```

#### Node.js + PostgreSQL

```
├── package.json
├── tsconfig.json
├── vitest.config.ts
├── Dockerfile
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── index.ts
│   ├── config/
│   │   ├── env.ts
│   │   └── database.ts
│   ├── modules/
│   │   └── orders/
│   │       ├── orders.controller.ts
│   │       ├── orders.service.ts
│   │       ├── orders.repository.ts
│   │       ├── orders.schema.ts
│   │       ├── orders.routes.ts
│   │       └── orders.test.ts
│   ├── shared/
│   │   ├── middleware/
│   │   │   ├── auth.ts
│   │   │   ├── error-handler.ts
│   │   │   └── validation.ts
│   │   └── errors/
│   │       └── app-error.ts
│   └── types/
│       └── global.d.ts
└── tests/
    └── setup.ts
```

#### Python + FastAPI

```
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── miapp/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── modules/
│       │   └── orders/
│       │       ├── __init__.py
│       │       ├── router.py
│       │       ├── service.py
│       │       ├── repository.py
│       │       ├── schemas.py
│       │       └── models.py
│       └── shared/
│           ├── database.py
│           ├── exceptions.py
│           └── deps.py
└── tests/
    ├── __init__.py
    └── modules/
        └── orders/
            ├── test_router.py
            └── test_service.py
```

#### React + Ant Design

```
├── package.json
├── tsconfig.json
├── vite.config.ts
├── index.html
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── config/
│   │   └── theme.ts
│   ├── pages/
│   │   └── orders/
│   │       ├── OrdersPage.tsx
│   │       ├── OrderDetailPage.tsx
│   │       └── CreateOrderPage.tsx
│   ├── components/
│   │   └── orders/
│   │       ├── OrderTable.tsx
│   │       ├── OrderForm.tsx
│   │       └── OrderDetail.tsx
│   ├── hooks/
│   │   └── use-orders.ts
│   ├── services/
│   │   └── orders-api.ts
│   └── types/
│       └── order.ts
└── tests/
    ├── setup.ts
    └── pages/
        └── orders.test.tsx
```

### Paso 3: Generar archivos base

Para cada archivo, generar contenido mínimo funcional:

```typescript
// Ejemplo: src/modules/orders/orders.schema.ts (Node.js + Zod)
import { z } from 'zod';

export const CreateOrderSchema = z.object({
  customerId: z.string().min(1).max(50),
  amount: z.number().positive(),
  currency: z.enum(['MXN', 'USD', 'EUR']).default('MXN'),
});

export type CreateOrderInput = z.infer<typeof CreateOrderSchema>;
```

```python
# Ejemplo: src/miapp/modules/orders/schemas.py (Python + Pydantic)
from pydantic import BaseModel, Field

class OrderCreate(BaseModel):
    customer_id: str = Field(..., min_length=1, max_length=50)
    amount: float = Field(..., gt=0)
    currency: str = Field(default="MXN", pattern=r"^[A-Z]{3}$")
```

```csharp
// Ejemplo: Program.cs (.NET 10 Minimal API)
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddOpenApi();
var app = builder.Build();
if (app.Environment.IsDevelopment()) app.MapOpenApi();
app.Run();
```

### Paso 4: Generar config files

Según stack, generar:

| Archivo | Contenido |
|---------|-----------|
| `.gitignore` | Específico del stack (node_modules, __pycache__, bin/obj, .env, dist) |
| `.editorconfig` | charset, indent_style, trim_trailing_whitespace |
| `tsconfig.json` / `pyproject.toml` / `.csproj` | Config del lenguaje con strict mode |
| `eslint.config.mjs` / `ruff.toml` / `.editorconfig` | Linter config |
| `Dockerfile` | Multi-stage build según stack |
| `.github/workflows/ci.yml` | CI pipeline mínimo: lint + test + build |
| `docker-compose.yml` | Servicios: app + DB + Redis |

### Paso 5: Instalar dependencias

Si el usuario lo pide, ejecutar:

```bash
npm install          # Node.js
uv sync             # Python
dotnet restore      # .NET
```

### Paso 6: Resumen y next steps

```
✅ Proyecto generado: miapp/
📁 34 archivos creados
📦 Stack: Node.js 24 + Express 5 + PostgreSQL 18 + React 19 + Ant Design 5.29

🔜 Próximos pasos:
1. Configurar .env con DATABASE_URL, JWT_SECRET, etc.
2. Ejecutar migraciones: npx prisma migrate dev
3. Iniciar desarrollo: docker-compose up
4. Abrir http://localhost:5173
```

---

## Lo que NO debe hacer

- No generar código de negocio más allá del scaffolding. El archivo de servicio tiene estructura vacía, no lógica inventada.
- No asumir nombres de entidades o endpoints que no están en la spec. Usar placeholders `{Entidad}` si falta información.
- No instalar dependencias sin preguntar.
- No sobreescribir archivos existentes. Si el proyecto ya existe, preguntar antes de sobrescribir.
