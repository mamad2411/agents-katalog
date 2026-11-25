---
name: sk-navigation
description: Kit-shipped navigation system for the TimeKast Starter Kit — `NavItem` interface, helpers (`filterNavigationByRole`, `getBottomNavItems`, `getMoreSheetItems`), `Sidebar`/`BottomNav`/`BottomNavMoreSheet` components, RBAC runtime filtering, badge integration, iOS safe-area handling. Single config lives in `src/config/navigation.ts`. Invoke when adding or modifying nav items. For portable patterns → `kb-navigation`.
last-verified: 2026-04-23
---

# sk-navigation — Kit-Shipped Navigation System

> Pair: [`kb-navigation`](../kb-navigation/SKILL.md) — portable navigation patterns (config-driven, RBAC filtering, mobile+desktop composition). This skill is the kit-shipped implementation.

Navigation en el TimeKast Starter Kit se maneja por **configuración declarativa única** en `src/config/navigation.ts`. Tres componentes (`Sidebar`, `BottomNav`, `BottomNavMoreSheet`) consumen el mismo array vía helpers. Nunca hardcodear items en componentes.

> **Registry anchors** — items canónicos viven en [`src/config/navigation.ts`](../../../src/config/navigation.ts); helpers exportados y componentes layout están indexados en [`project/reference/HOOKS.md`](../../../project/reference/HOOKS.md) + [`project/reference/INVENTORY.md`](../../../project/reference/INVENTORY.md). Esta skill enseña el **patrón** — los nombres exactos y signaturas son autogen, no los enumeres manualmente.

---

## 1. `NavItem` interface — SSOT

Definido en `src/config/navigation.ts`. Todos los campos más allá de `name`, `href`, `icon` son opcionales.

| Campo            | Tipo              | Consumido por      | Semántica                                                                                                                                                  |
| ---------------- | ----------------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`           | `string`          | Todos              | Label visible (UI en es-MX)                                                                                                                                |
| `href`           | `string`          | Todos              | Ruta Next.js                                                                                                                                               |
| `icon`           | `LucideIcon`      | Todos              | Import desde `lucide-react`                                                                                                                                |
| `children`       | `NavItem[]`       | Sidebar, Más sheet | Sub-items (solo con `collapsible: true`)                                                                                                                   |
| `collapsible`    | `boolean`         | Sidebar            | Renderiza como sección expandible con chevron                                                                                                              |
| `roles`          | `string[]`        | Todos (RBAC)       | Restringe a roles específicos. Omitir = visible para todo usuario autenticado. Usar constantes de `@/config/roles` (`ROLES.ADMIN`, etc.)                   |
| `bottomNav`      | `boolean`         | BottomNav          | Muestra como tab primario en mobile. **Máx 4 items** — el 5° slot es "Más" auto-generado                                                                   |
| `bottomNavOrder` | `number`          | BottomNav          | Orden left-to-right (menor = más a la izquierda). Solo si `bottomNav: true`                                                                                |
| `bottomNavLabel` | `string`          | BottomNav          | Label corto para tab (≤10 chars recomendado). Fallback → `name`                                                                                            |
| `bottomNavHref`  | `string`          | BottomNav          | Override del `href` en BottomNav. Útil para `collapsible` sin página propia (ej: `/settings` → `/settings/general`)                                        |
| `bottomNavOnly`  | `boolean`         | Todos              | Oculto del Sidebar; solo aparece en BottomNav + Más sheet. Útil cuando desktop ya lo expone por otro medio (ej: Perfil vía avatar menu)                    |
| `featureFlag`    | `'notifications'` | Todos              | Feature flag key. Item oculto si la feature está disabled. Actualmente soporta `'notifications'` (checkeado via `isNotificationsEnabled()` en `@/lib/env`) |

---

## 2. Config SSOT — `src/config/navigation.ts`

Un archivo, un array exportado (`navigation: NavItem[]`), tres helpers. Todo lo visible en la app sale de aquí.

```ts
import { navigation, filterNavigationByRole } from '@/config/navigation';
```

**Regla:** agregar o mover un item = editar `navigation.ts`. Nunca editar `Sidebar.tsx` o `BottomNav.tsx` para agregar un link.

---

## 3. Helper functions

Definidos en el mismo `src/config/navigation.ts`. Stateless, puros, fáciles de testear.

| Helper                                     | Signature                           | Consumido por      | Comportamiento                                                                                                                   |
| ------------------------------------------ | ----------------------------------- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| `filterNavigationByRole(items, userRole?)` | `(NavItem[], string?) => NavItem[]` | Sidebar            | Filtra por `roles`, excluye `bottomNavOnly`, remueve collapsibles sin children visibles, aplica filtering recursivo a `children` |
| `getBottomNavItems(items, userRole?)`      | `(NavItem[], string?) => NavItem[]` | BottomNav          | Filtra `bottomNav: true` por `roles`, ordena por `bottomNavOrder`, slice max 4                                                   |
| `getMoreSheetItems(items, userRole?)`      | `(NavItem[], string?) => NavItem[]` | BottomNavMoreSheet | Filtra por `roles` + `featureFlag`, preserva parent-child groups, remueve collapsibles vacíos. Incluye TODO (no solo overflow)   |

Internamente, `filterNavigationByRole` y `getMoreSheetItems` comparten lógica: roles + feature flag gating + limpieza de collapsibles vacíos.

---

## 4. Componentes shipped — `@/components/layout`

Todos son Client Components (`'use client'`) — usan `usePathname()` para active state.

| Componente           | Archivo                                        | Breakpoint | Qué hace                                                                                                                                                        |
| -------------------- | ---------------------------------------------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Sidebar`            | `src/components/layout/Sidebar.tsx`            | `≥lg`      | Fixed left rail, 240px wide. Branding top + nav scrollable middle + TimeKast logo footer. Collapsibles con chevron (estado local). Active item = `neo-inset-sm` |
| `BottomNav`          | `src/components/layout/BottomNav.tsx`          | `<lg`      | Fixed bottom tab bar. Max 4 tabs + "Más" button (LayoutGrid icon). Respeta `env(safe-area-inset-bottom)`. Active = inset elevation                              |
| `BottomNavMoreSheet` | `src/components/layout/BottomNavMoreSheet.tsx` | `<lg`      | Overflow sheet animado (framer-motion spring). Grid 3 columnas. Top-level items (flat) + grouped items (section header + children grid). Backdrop cerrable      |

**Assembly:** `DashboardShell` (`src/app/(protected)/DashboardShell.tsx`) monta los tres junto con `Header`. Todos reciben `userRole?: string` desde el server (session).

> ℹ️ **`Header` es hardcoded en `DashboardShell`** — breadcrumb + avatar menu + theme toggle + notification bell se renderizan directamente, **no consumen `navigation.ts`**. Si agregas un ítem global del shell (ej: shortcut en el header), edita `DashboardShell.tsx`/`Header.tsx`, no `navigation.ts`.

---

## 5. RBAC runtime filter

RBAC se aplica en cada render de navegación, server-side cuando el `userRole` viene de la session (`auth()`), propagado client-side como prop.

```ts
// DashboardShell (server) lee session y pasa userRole
<Sidebar userRole={session.user.role} />
<BottomNav userRole={session.user.role} />
```

**Reglas del filtro:**

- `roles` omitido o array vacío → visible para todos los autenticados
- `roles: [ROLES.ADMIN]` → solo si `userRole === 'admin'`
- Children heredan el check recursivamente
- Collapsibles que quedan sin children visibles post-filter → auto-removidos

**⚠️ No es autorización.** El filter esconde items, no bloquea rutas. La ruta debe protegerse en su propio layout/page con `requirePermission()` o el middleware de auth (ver [`sk-security`](../sk-security/SKILL.md)).

---

## 6. Badge integration — notifications

`BottomNav` y `BottomNavMoreSheet` integran el hook `useNotifications` (`@/lib/hooks/useNotifications`) para mostrar badge de unread count.

```ts
const { unreadCount } = useNotifications();
const showBadge = isNotificationsEnabled() && unreadCount > 0;
const badgeText = unreadCount > 9 ? '9+' : String(unreadCount);
```

**Dónde aparece el badge:**

| Location                                 | Cuándo                                                              |
| ---------------------------------------- | ------------------------------------------------------------------- |
| BottomNav → botón "Más"                  | Agregado de todos los unread (siempre que haya cualquiera)          |
| BottomNavMoreSheet → item Notificaciones | Específicamente en el item con `featureFlag: 'notifications'`       |
| Header bell (desktop)                    | `NotificationPanel` — tiene su propio badge (fuera de este sistema) |

Ver [`sk-notifications`](../sk-notifications/SKILL.md) para el pipeline completo de unread counts y realtime.

---

## 7. Safe-area insets (iOS notch)

`BottomNav` y `BottomNavMoreSheet` respetan `env(safe-area-inset-bottom)` para dispositivos con home indicator (iPhone X+).

```tsx
// BottomNav
style={{ paddingBottom: 'env(safe-area-inset-bottom, 0px)' }}

// BottomNavMoreSheet
style={{ paddingBottom: 'calc(1.5rem + env(safe-area-inset-bottom, 0px))' }}
```

**Requisito previo:** el `<meta name="viewport">` del root layout debe incluir `viewport-fit=cover` (shipped en `src/app/layout.tsx` del kit). Si el contenido queda tapado por la home bar, verificar este meta y que los `env()` estén presentes en los componentes.

---

## 8. Cómo agregar un nav item — checklist

1. **Abrir `src/config/navigation.ts`** (único archivo a tocar para items simples)
2. **Importar el ícono** desde `lucide-react` (ej: `import { BarChart } from 'lucide-react';`)
3. **Agregar al array `navigation`** con los campos apropiados:

   ```ts
   {
     name: 'Reportes',
     href: '/reportes',
     icon: BarChart,
     roles: [ROLES.ADMIN, ROLES.SUPER_ADMIN], // opcional
     bottomNav: true,                           // opcional — máx 4 en total
     bottomNavOrder: 2,                         // si bottomNav
     bottomNavLabel: 'Reportes',                // si ≤10 chars distinto de name
   }
   ```

4. **Si es `collapsible` con children** → `bottomNavHref` apuntando al primer child (evita 404 del parent sin página)
5. **Si es solo mobile** → `bottomNavOnly: true`
6. **Si depende de feature flag** → `featureFlag: 'notifications'` (o extender la union en el interface para nuevos flags)
7. **Verificar que la ruta exista** en `src/app/(protected)/`
8. **Guard real de la ruta:** agregar `requirePermission()` en el layout/page — el nav filter no autoriza

---

## 9. Troubleshooting

### Item no aparece en Sidebar

1. `bottomNavOnly` está en `true` → por diseño, solo aparece en mobile
2. `roles` restringe y el user no matchea
3. `featureFlag` apaga el item
4. Es un collapsible con `children: []` post-filter → auto-removido
5. Cache stale del dev server → `pnpm dev` restart

### Tab no aparece en BottomNav

1. Falta `bottomNav: true`
2. Ya hay 4 items con `bottomNav: true` → el 5° se va al Más sheet (slice en `getBottomNavItems`)
3. `roles` excluye al user
4. `bottomNavOrder` muy alto → reordenar números

### BottomNav tap va a 404

- El `href` apunta a un parent `collapsible` sin página (ej: `/settings`). Agregar `bottomNavHref: '/settings/general'`

### Label truncado en mobile

- `bottomNavLabel` > 10 chars en pantallas de 375px. Usar label más corto o abreviatura

### Badge no aparece

- `isNotificationsEnabled()` retorna `false` (revisar `NEXT_PUBLIC_NOTIFICATIONS_ENABLED`)
- `useNotifications()` no está hidratado (SSE aún no conectó)
- `unreadCount === 0` (no hay mensajes)

### Hydration mismatch en ítems theme-dependent

Síntoma: warning `Hydration failed` o flicker del ícono cuando un ítem cambia según el tema (ej: logo variant, ícono según `resolvedTheme`).

Causa: el server no conoce el tema (viene de `localStorage` / `next-themes`) → el render inicial difiere del cliente.

Fix: gate el render theme-dependent con `useMounted()`:

```tsx
const mounted = useMounted();
if (!mounted) return <PlaceholderIcon />; // o null
return <ThemeAwareIcon theme={resolvedTheme} />;
```

El `useMounted()` hook vive en `@/lib/hooks/useMounted` y retorna `false` en SSR, `true` tras el primer effect. Úsalo solo para el subárbol que depende del tema — no wrappees toda la navegación.

### Contenido tapado por home indicator iOS

- Falta `viewport-fit=cover` en `<meta name="viewport">` del root layout
- Componente custom overlay no respeta `env(safe-area-inset-bottom)`

---

## 10. Anti-patterns (NO hacer)

```
❌ Hardcodear un `<Link>` dentro de Sidebar.tsx o BottomNav.tsx
✅ Agregar al array `navigation` en src/config/navigation.ts

❌ Editar Sidebar.tsx / BottomNav.tsx para cambiar un label o ícono
✅ Editar la entry del NavItem correspondiente

❌ Skipear `roles` y "filtrar después" en el componente
✅ Declarar `roles` en el NavItem — el helper lo aplica uniforme en los 3 componentes

❌ Confiar solo en el nav filter como autorización
✅ El filter oculta la UI; la ruta se protege con requirePermission()/middleware (ver sk-security)

❌ Crear un segundo array de navegación para "admin-only items"
✅ Un único `navigation` array + roles por item

❌ Mutar `navigation` en runtime o filtrar fuera de los helpers
✅ Los 3 helpers (filterNavigationByRole, getBottomNavItems, getMoreSheetItems) son la API — usar exclusivamente

❌ Usar `bottomNavOnly` + faltar en Más sheet (item inaccesible)
✅ `bottomNavOnly` implica que aparece en BottomNav o Más sheet — verificar visualmente

❌ Meter más de 4 tabs con `bottomNav: true`
✅ El 5° se va a Más (no rompe, pero oculta intención) — revisar qué debería ser primario
```

---

## Cross-reference

Cross-reference: [`kb-navigation`](../kb-navigation/SKILL.md) — portable patterns. [`kb-security`](../kb-security/SKILL.md) / [`sk-security`](../sk-security/SKILL.md) — RBAC. [`sk-notifications`](../sk-notifications/SKILL.md) — badge counts. [`sk-ui`](../sk-ui/SKILL.md) — componentes relacionados. [`sk-features-index`](../sk-features-index/SKILL.md).
