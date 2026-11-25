---
name: sk-crud-scaffold
description: Orchestrator skill for the TimeKast Starter Kit — gold standard to scaffold a new entity end-to-end: URL convention (`/(protected)/{entity}/{nuevo,[id],[id]/editar}`), RSC page shells, `BreadcrumbSetter` wiring, human IDs, `StatusToggle` soft delete, cascading filters. Entry point for any CRUD work — composes `kb-ui` + `sk-ui` + `kb-api` + `sk-api` + `sk-db`. Invoke when creating a CRUD for a new entity.
last-verified: 2026-04-23
---

# sk-crud-scaffold — Kit CRUD Orchestrator

> Orchestrator for: [`kb-ui`](../kb-ui/SKILL.md) + [`sk-ui`](../sk-ui/SKILL.md) + [`kb-api`](../kb-api/SKILL.md) + [`sk-api`](../sk-api/SKILL.md) + [`sk-db`](../sk-db/SKILL.md)
>
> Gold standard para montar una entidad nueva end-to-end en el TimeKast Starter Kit. No redefine primitivas — compone las que shipean las skills pair. Si algo no está aquí (tokens, queries Drizzle, wrappers de acción, primitivas UI), está en la skill correspondiente.

---

## 1. Architecture overview

Un CRUD completo del kit son **4 page shells** (RSC), **1 chain de actions**, y **componentes client** que consumen las primitivas de `sk-ui`.

```
List      /(protected)/{entity}/page.tsx          → getEntities()          → <EntityTable />
Create    /(protected)/{entity}/nuevo/page.tsx    → auth + perm guard      → <NewEntityContent />
Detail    /(protected)/{entity}/[id]/page.tsx     → getEntityById()        → <EntityDetailContent />
Edit*     /(protected)/{entity}/[id]/editar/page.tsx (opcional — inline edit vía DataTab es preferible)
```

**Action chain:**

```
getEntities()           → list (withAuth resource:list o auth manual)
getEntityById(id)       → detail
getAdjacentEntities(id) → CRM prev/next navigator (CTE)
createEntity(input)     → withAuth resource:create
updateEntity(id, input) → withAuth resource:update
deleteEntity(id)        → withAuth resource:delete (soft delete)
restoreEntity(id)       → withAuth resource:update
```

**Responsabilidades:**

| Capa                                                | Responsabilidad                                                   | Skill SSOT                                           |
| --------------------------------------------------- | ----------------------------------------------------------------- | ---------------------------------------------------- |
| Schema (`@/lib/db/schema/{entity}.ts`)              | Tabla + `auditFields` + `softDeleteFields` + `humanId` + sequence | [`sk-db`](../sk-db/SKILL.md)                         |
| Validations (`@/lib/validations/admin/{entity}.ts`) | Zod schemas `create` + `update` separados                         | [`kb-api`](../kb-api/SKILL.md)                       |
| Actions (`@/lib/actions/admin/{entity}.ts`)         | `withAuth`/`withSelf` + retry humanId + `ActionResult`            | [`sk-api`](../sk-api/SKILL.md)                       |
| Page shells (RSC)                                   | Auth/perm guard + data fetch + delegate a client                  | este doc                                             |
| Client components                                   | `DataTable`, form kit, `StatusToggle`, breadcrumbs                | [`sk-ui`](../sk-ui/SKILL.md)                         |
| Tests                                               | Component (RTL) + E2E (Playwright)                                | [`sk-testing-nextjs`](../sk-testing-nextjs/SKILL.md) |

---

## 2. URL convention del kit

Rutas en español dentro del group `(protected)`. Un solo patrón aplicado consistentemente a todas las entidades.

```
/(protected)/{entity}                  → List
/(protected)/{entity}/nuevo            → Create (full page form)
/(protected)/{entity}/[id]             → Detail (tabs: Datos | Actividad | ...)
/(protected)/{entity}/[id]/editar      → Edit (opcional — preferir inline edit en DataTab)
```

**Por qué en español:**

- La UI del kit es `es-MX` (ver `project-config.md` §Project-Specific Rules). URLs consistentes con el idioma del producto.
- `nuevo` / `editar` son verbos estables — no colisionan con slugs de entidad porque las rutas `[id]` aceptan humanId (`USR-0001`), no palabras reservadas.

**Qué resuelve esta convención:**

- URLs bookmarkeables para create/edit (no modales opacos).
- Breadcrumbs predecibles (`Users > Nuevo`, `Users > USR-0001 > Editar`).
- Routing consistente cross-entidad — el mismo mental model aplica siempre.

> 🔴 Usar humanId en la URL (`/users/USR-0001`), **nunca** UUID. El detail action resuelve por humanId. Ver [`sk-ui`](../sk-ui/SKILL.md) §4 (regla display) y [`sk-db`](../sk-db/SKILL.md) (dual-ID schema).

---

## 3. Naming conventions

| Layer                    | Pattern                                                                                              | Ejemplo                                   |
| ------------------------ | ---------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| DB Schema (file)         | `src/lib/db/schema/{entities}.ts` (plural snake→kebab)                                               | `src/lib/db/schema/orders.ts`             |
| DB Table                 | `pgTable('entities', …)` (snake_case plural)                                                         | `pgTable('orders', …)`                    |
| Zod                      | `createEntitySchema` / `updateEntitySchema` + `.z.infer`                                             | `createOrderSchema` / `updateOrderSchema` |
| Validations file         | `src/lib/validations/admin/{entity}.ts`                                                              | `src/lib/validations/admin/order.ts`      |
| Actions file             | `src/lib/actions/admin/{entity}.ts`                                                                  | `src/lib/actions/admin/order.ts`          |
| Action names             | `getEntities` / `getEntityById` / `createEntity` / `updateEntity` / `deleteEntity` / `restoreEntity` | `getOrders`, `createOrder`, ...           |
| Page files               | `page.tsx` en cada segmento                                                                          | `app/(protected)/orders/nuevo/page.tsx`   |
| Client components (file) | `PascalCase`                                                                                         | `OrderTable.tsx`, `NewOrderContent.tsx`   |
| Table component          | `{Entity}Table`                                                                                      | `OrderTable`                              |
| Create content           | `New{Entity}Content`                                                                                 | `NewOrderContent`                         |
| Detail content           | `{Entity}DetailContent`                                                                              | `OrderDetailContent`                      |
| Data tab (inline edit)   | `{Entity}DataTab`                                                                                    | `OrderDataTab`                            |
| Navigator                | `{Entity}Navigator`                                                                                  | `OrderNavigator`                          |
| Loading skeleton         | `loading.tsx` en cada nivel (list + detail)                                                          | `app/(protected)/orders/loading.tsx`      |

**Reglas:**

- Paths en `kebab-case`, files de componentes en `PascalCase`.
- Actions exportan funciones con verbos claros — no `handleX`, no `doY`.
- Tipos inferidos: `type Order = typeof orders.$inferSelect` (ver [`kb-db`](../kb-db/SKILL.md)).

---

## 4. Page RSC shells

Los 4 shells siguen el mismo pattern: **`await auth()` guard → `requirePermission`/`hasPermission` → data fetch server-side → delegar a Client Component con props serializables**.

### 4.1 List — `/(protected)/{entity}/page.tsx`

```tsx
import { redirect } from 'next/navigation';
import type { Metadata } from 'next';
import { auth } from '@/lib/auth';
import { hasPermission } from '@/lib/auth/permissions';
import { getOrders } from '@/lib/actions/admin/order';
import { OrderTable } from '@/components/admin/OrderTable';

export const metadata: Metadata = {
  title: 'Órdenes | Admin',
  description: 'Gestión de órdenes del sistema',
};

export default async function OrdersPage() {
  const session = await auth();
  if (!session?.user?.id) redirect('/login');
  if (!hasPermission(session.user.role, 'orders', 'list')) redirect('/dashboard');

  const orders = await getOrders();

  return (
    <div className="container mx-auto space-y-4 py-6">
      <div>
        <h1 className="text-foreground text-2xl font-bold">Gestión de órdenes</h1>
        <p className="text-muted-foreground text-sm">Administra las órdenes del sistema</p>
      </div>
      <OrderTable
        orders={orders}
        currentUserRole={session.user.role}
        currentUserId={session.user.id}
      />
    </div>
  );
}
```

**Reglas:**

- `h1` + descripción **en el server page**, nunca dentro del client component (SEO + layout estable durante Suspense).
- Data fetch server-side, pasa como prop al client.
- Sin `'use client'`.

### 4.2 Create — `/(protected)/{entity}/nuevo/page.tsx`

Shell delgado — toda la UI en el client component (forms requieren `'use client'`).

```tsx
import { redirect } from 'next/navigation';
import type { Metadata } from 'next';
import { auth } from '@/lib/auth';
import { hasPermission } from '@/lib/auth/permissions';
import { NewOrderContent } from '@/components/admin/NewOrderContent';

export const metadata: Metadata = {
  title: 'Crear Orden | Admin',
  description: 'Crear una nueva orden',
};

export default async function CreateOrderPage() {
  const session = await auth();
  if (!session?.user?.id) redirect('/login');
  if (!hasPermission(session.user.role, 'orders', 'create')) redirect('/dashboard');

  return <NewOrderContent currentUserRole={session.user.role} />;
}
```

### 4.3 Detail — `/(protected)/{entity}/[id]/page.tsx`

```tsx
import { redirect, notFound } from 'next/navigation';
import { auth } from '@/lib/auth';
import { hasPermission } from '@/lib/auth/permissions';
import { getOrderById, getAdjacentOrders } from '@/lib/actions/admin/order';
import { BreadcrumbSetter } from '@/components/common/BreadcrumbSetter';
import { OrderDetailContent } from '@/components/admin/OrderDetailContent';
import { OrderNavigator } from '@/components/admin/OrderNavigator';

export default async function OrderDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params; // Next.js 16+ — params es Promise

  const session = await auth();
  if (!session?.user?.id) redirect('/login');
  if (!hasPermission(session.user.role, 'orders', 'read')) redirect('/dashboard');

  const order = await getOrderById(id);
  if (!order) notFound();

  const adjacent = await getAdjacentOrders(order.humanId);
  const isInactive = order.deletedAt !== null;

  return (
    <>
      <BreadcrumbSetter segment={id} label={order.humanId} />

      <div className="mx-auto max-w-4xl space-y-6 py-6">
        <header className="flex items-start justify-between">
          <div>
            <h1 className="text-foreground text-2xl font-bold">{order.humanId}</h1>
            <p className="text-muted-foreground text-sm">
              Orden creada {order.createdAt.toISOString()}
            </p>
          </div>
          <OrderNavigator
            prev={adjacent.prev}
            next={adjacent.next}
            currentIndex={adjacent.currentIndex}
            total={adjacent.total}
          />
        </header>

        <OrderDetailContent
          order={order}
          currentUserRole={session.user.role}
          isInactive={isInactive}
        />
      </div>
    </>
  );
}
```

**Reglas:**

- `notFound()` cuando la entidad no existe (renderiza `not-found.tsx` del segmento).
- `BreadcrumbSetter` SIEMPRE en páginas con `[id]` dinámico — reemplaza el UUID/humanId en el breadcrumb por el label legible.
- Tabs (inline edit + actividad + …) se delegan a `{Entity}DetailContent` client.

### 4.4 Edit — `/(protected)/{entity}/[id]/editar/page.tsx` (opcional)

> Preferir inline edit vía `{Entity}DataTab` dentro de `OrderDetailContent`. El route `/editar` solo es necesario si el flujo de edición requiere una pantalla completa separada (ej: wizard multi-step). Para el caso común (form plano), el DataTab es suficiente y mantiene el contexto del detail.

---

## 5. BreadcrumbSetter wiring

Breadcrumbs con segmentos dinámicos (UUID/humanId) se resuelven server-side y se pushean a un context. Ver [`sk-ui`](../sk-ui/SKILL.md) §5 para el detalle del componente.

**Pattern por segmento:**

| Segmento | `segment` prop      | `label` prop                                           |
| -------- | ------------------- | ------------------------------------------------------ |
| `[id]`   | `id` (humanId/UUID) | `order.humanId` o `order.name` (lo que vea el usuario) |
| `nuevo`  | `"nuevo"`           | `"Nueva Orden"`                                        |
| `editar` | `"editar"`          | `"Editar"`                                             |

**Reglas:**

- Un `<BreadcrumbSetter>` por segmento dinámico — no "uno por página".
- Renderiza `null` — es efecto puro (context push).
- SIEMPRE en páginas con `[id]` — omitirlo deja el UUID feo en el breadcrumb.
- `label` debe coincidir con lo que el usuario reconoce (humanId para entidades técnicas, `name` para entidades con nombre propio).

---

## 6. Human ID pattern

Las URLs del kit nunca exponen UUIDs. El schema define dos claves:

- `id: uuid('id').primaryKey().defaultRandom()` — interno, FKs, queries.
- `humanId: text('human_id').notNull().unique()` — URL, UI, soporte telefónico.

**Generación atómica (en `createEntity`):**

```ts
import { getNextHumanId } from '@/lib/db/helpers/human-id';
import { HUMAN_ID_PREFIXES } from '@/lib/db/schema/enums';

const humanId = await getNextHumanId(db, 'order_human_id_seq', {
  prefix: HUMAN_ID_PREFIXES.ORDER, // p.ej. 'ORD'
  includeYear: true, // → 'ORD-2026-0042'
});
```

**Retry on 23505:** la sequence puede drift tras branch restore o seed. Envolver el `insert` en un loop de 5 intentos que capture PG code `23505` + constraint `{table}_human_id_unique`. Implementación completa en [`sk-api`](../sk-api/SKILL.md) §6.

**Display rule:** UI nunca muestra UUID. Ver [`sk-ui`](../sk-ui/SKILL.md) §4 (tabla de contextos: breadcrumbs, tablas, URLs, toast, email, PDF, soporte).

**Schema requisitos:** `humanId` + sequence SQL + `HUMAN_ID_PREFIXES` constant. Detalle del schema y migration en [`sk-db`](../sk-db/SKILL.md).

---

## 7. Interaction patterns

### 7.1 StatusToggle (soft delete switch)

Reemplaza el botón "Eliminar" en tablas del kit. Toggle activo/inactivo con confirmación vía `ConfirmDialog`.

```tsx
import { StatusToggle } from '@/components/shared/StatusToggle';

<StatusToggle
  entityName={order.humanId}
  isActive={!order.deletedAt}
  onToggle={async () => {
    const result = order.deletedAt ? await restoreOrder(order.id) : await deleteOrder(order.id);
    if (result.error) toast.error(result.error);
    else toast.success(order.deletedAt ? 'Orden reactivada' : 'Orden desactivada');
  }}
  disabled={isSelf || isProtected}
  disabledReason={isSelf ? 'No puedes cambiar tu propio estado' : undefined}
/>;
```

**Reglas:** confirmación previa, `disabled` + `disabledReason` para entradas protegidas, loading state bloquea double-click. Para el wrapper genérico `ConfirmDialog` ver [`sk-ui`](../sk-ui/SKILL.md) §6.

### 7.2 Inline edit (DataTab) vs full-page edit

| Caso                                  | Preferir            |
| ------------------------------------- | ------------------- |
| Form plano (2-10 campos)              | Inline DataTab      |
| Wizard multi-step / carga de archivos | Full-page `/editar` |
| Requiere contexto del detail visible  | Inline DataTab      |
| Form largo con secciones colapsables  | Full-page `/editar` |

**Inline DataTab pattern:**

- Pre-populado con valores actuales.
- Submit → `router.refresh()` (se queda en la misma página, recarga RSC data).
- Cancel → `confirmNavigation(() => router.push('/orders'))`.
- `disabled` prop para entidades soft-deleted.

**Full-page create (`NewOrderContent`) pattern:**

- Submit → `allowNavigation(() => router.push('/orders'))` (redirect a list).
- Cancel → `confirmNavigation(() => router.push('/orders'))`.
- `useUnsavedChangesGuard` para dirty-check.

Form kit (`useForm({ schema })`, `FormField`, `SubmitButton`): ver [`sk-ui`](../sk-ui/SKILL.md) §2. Paradigma genérico (Server/Client split, Suspense + skeleton): ver [`kb-ui`](../kb-ui/SKILL.md).

### 7.3 Cascading filters

Cuando una tabla client-side tiene **2+ filtros**, cada filtro debe calcular sus opciones a partir del subconjunto filtrado por los OTROS filtros (SK.md §3.1, enforcement).

```tsx
const roleOptions = useMemo(() => {
  const subset = orders.filter((o) => matchesStatus(o) && matchesSearch(o));
  const uniqueRoles = [...new Set(subset.map((o) => o.role))];
  return ALL_ROLE_OPTIONS.filter((opt) => uniqueRoles.includes(opt.value));
}, [orders, statusFilter, search]);
```

**Reglas:** `useMemo` con deps explícitas, mantener un `ALL_*_OPTIONS` estático como master list, botón "Limpiar filtros" con `FilterX` cuando hay filtros colapsables. Implementación UI completa en [`sk-ui`](../sk-ui/SKILL.md) §3 + [`kb-ui`](../kb-ui/SKILL.md) (URL state + paginación).

---

## 8. Cómo crear CRUD nuevo — checklist

Orden recomendado. Cada paso tiene su skill pair como SSOT.

1. **Schema** (`@/lib/db/schema/{entity}.ts`)
   - [ ] Tabla con `auditFields` + `softDeleteFields` + `humanId` unique — ver [`sk-db`](../sk-db/SKILL.md)
   - [ ] Sequence SQL (`CREATE SEQUENCE {entity}_human_id_seq`)
   - [ ] Prefix en `HUMAN_ID_PREFIXES` enum
   - [ ] Re-export desde `@/lib/db/schema/index.ts`
   - [ ] `pnpm db:generate` → revisar migration → `pnpm db:migrate` (SK.md §1.1)

2. **Validations** (`@/lib/validations/admin/{entity}.ts`)
   - [ ] `createEntitySchema` + `updateEntitySchema` separados
   - [ ] Mensajes en español, campos precisos (no reutilizar `.partial()`)
   - [ ] Export `z.infer<>` types — ver [`kb-api`](../kb-api/SKILL.md)

3. **Actions** (`@/lib/actions/admin/{entity}.ts`)
   - [ ] `'use server'` al tope
   - [ ] `getEntities` / `getEntityById` / `getAdjacentEntities` — lecturas (`auth` + `requirePermission`)
   - [ ] `createEntity` con `withAuth` + retry humanId on 23505
   - [ ] `updateEntity` / `deleteEntity` / `restoreEntity` con `withAuth`
   - [ ] `ActionResult<T>` return, `ActionError` para user-facing — ver [`sk-api`](../sk-api/SKILL.md)

4. **Page shells** (`app/(protected)/{entity}/**`)
   - [ ] `page.tsx` (list) — `h1` server-side, delegate a client
   - [ ] `nuevo/page.tsx` — shell delgado
   - [ ] `[id]/page.tsx` — `BreadcrumbSetter` + `getAdjacentEntities`
   - [ ] `loading.tsx` en list y detail — layout-aware (ver [`sk-ui`](../sk-ui/SKILL.md) §4 skeletons)

5. **Client components**
   - [ ] `{Entity}Table` con `DataTable` + `TableFilterBar` + `StatusToggle`
   - [ ] `New{Entity}Content` con form kit + `useUnsavedChangesGuard`
   - [ ] `{Entity}DetailContent` con `Tabs`
   - [ ] `{Entity}DataTab` (inline edit)
   - [ ] `{Entity}Navigator` (prev/next CRM)
   - [ ] Consultar `INVENTORY.md` (componentes) **y** `HOOKS.md` (hooks / form kit / UI wrappers con import paths canónicos) ANTES de crear cada uno (SK.md §2.1)

6. **Navigation** (`@/config/navigation.ts`)
   - [ ] Añadir item con `resource` + icon + label
   - [ ] RBAC filtering automático por `resource` — nunca hardcodear items en el sidebar

7. **Test** (ver [`sk-testing-nextjs`](../sk-testing-nextjs/SKILL.md))
   - [ ] Component (RTL): render de `{Entity}Table` + interacción (filtros, StatusToggle, onRowClick)
   - [ ] E2E (Playwright): flujo create → list → detail → edit → soft delete

8. **Regen** (automático en pre-commit)
   - [ ] `pnpm generate:inventory` (si el hook no lo corre)
   - [ ] `pnpm generate:codebase`

---

## 9. Anti-patterns

| ❌                                                   | ✅                                                          |
| ---------------------------------------------------- | ----------------------------------------------------------- |
| Rutas en inglés (`/orders/new`, `/orders/[id]/edit`) | Español: `/nuevo`, `/editar`                                |
| UUID en URL (`/orders/abc-123-uuid`)                 | humanId (`/orders/ORD-2026-0042`)                           |
| `h1` dentro del client component                     | `h1` en el server page, client recibe data como props       |
| Full-page edit por defecto                           | Inline DataTab, full-page solo para wizards                 |
| Botón "Eliminar" en tabla                            | `StatusToggle` (soft delete + confirm + restore)            |
| Hardcodear opciones de filtro estáticas              | Cascading filters (SK.md §3.1)                              |
| Schema sin `humanId` / sin sequence                  | Dual-ID siempre — el kit lo exige                           |
| `createEntity` sin retry 23505                       | Loop de 5 intentos, capturar `code`/`constraint` en `cause` |
| Breadcrumb con UUID crudo                            | `<BreadcrumbSetter segment={id} label={humanId \| name} />` |
| Olvidar `loading.tsx`                                | Skeleton layout-aware en list y detail                      |
| Navigation items hardcodeados en componentes         | `@/config/navigation.ts` con RBAC por `resource`            |

---

## 10. Cuándo NO usar este orquestador

- **Entidad puramente read-only** (dashboards, reports) → no necesitas create/edit shells, solo list + detail.
- **Flujos no-CRUD** (auth, wizards de onboarding, payments) → cada uno tiene su propia forma; consultar skills específicas.
- **Entidad interna sin UI** (tabla de jobs, audit log consumido solo por otra feature) → schema + actions bastan, no agregues pages.

---

_Cross-reference: [`kb-ui`](../kb-ui/SKILL.md) | [`sk-ui`](../sk-ui/SKILL.md) | [`kb-api`](../kb-api/SKILL.md) | [`sk-api`](../sk-api/SKILL.md) | [`sk-db`](../sk-db/SKILL.md) | [`sk-features-index`](../sk-features-index/SKILL.md)_
