---
name: sk-notifications
description: Kit-shipped notification infrastructure for the TimeKast Starter Kit — `notify()` server dispatcher, `/api/notifications/poll` endpoint (visibility-aware polling, Vercel-friendly), `useNotifications` client hook, `NotificationBell`/`NotificationPanel`/`NotificationSettings`/`PushDevicesList` components, push subscriptions per-device, and the categories × channels config in `src/config/notifications.ts`. Use when dispatching notifications from server actions or wiring the bell, panel, and settings page in-app. For portable patterns → `kb-notifications`.
last-verified: 2026-04-26
---

# sk-notifications — Kit-Shipped Notification Infrastructure

> Pair: [`kb-notifications`](../kb-notifications/SKILL.md)

Esta skill documenta la infraestructura **concreta** de notifications que shippea el kit. Todo lo que vive en `@/lib/notifications`, `@/config/notifications`, `@/app/api/notifications/poll`, `@/lib/hooks/useNotifications`, y `@/components/notifications`.

> **Registry anchors** — helpers exportados (`notify`, `notifyMany`, `useNotifications`, `getPushDevices`, `removePushDevice`) y componentes viven indexados en [`project/reference/HOOKS.md`](../../../project/reference/HOOKS.md) + [`project/reference/INVENTORY.md`](../../../project/reference/INVENTORY.md) (autogen). Config de categorías × canales es SSOT en `src/config/notifications.ts`. Esta skill enseña el **patrón de integración** — no reproduzcas la lista actual de categorías aquí; léela del SSOT.

---

## 1. `notify()` API — server-side dispatcher

**Ubicación:** `@/lib/notifications/service.ts` (re-exportado desde `@/lib/notifications`).

```ts
import { notify, notifyMany } from '@/lib/notifications';

await notify({
  userId: 'uuid',
  title: 'Nuevo documento',
  body: 'Se subió "Contrato Q1.pdf"',
  type: 'info', // info | success | warning | error | system
  category: 'general', // single shipped category — extensible per-app
  url: '/documents/123', // optional deep link
  channels: ['in_app'], // optional override — default viene de category
  expiresAt: undefined, // optional Date — borrado oportunista al cumplirse
  metadata: undefined, // optional Record<string, unknown>
});
```

**Qué hace internamente (`service.ts`):**

1. **Resuelve canales efectivos** — modelo en capas. Por cada canal, gana lo más específico:
   - Si el caller pasa `channels: [...]` a `notify()` (override explícito) → ese set manda. Aún respeta opt-out del user (excepto `in_app`).
   - Si no hay override → por cada canal posible: la preference del user si está guardada en `notification_preferences`; sin preference guardada cae a `defaultChannels` de la categoría (estado inicial). `in_app` siempre se entrega.
   - **Resultado:** cada toggle del UI tiene efecto independiente. `defaultChannels` define ON inicial — no es un gate.
2. **Inserta el record** en tabla `notifications` con `channels: string[]` efectivos.
3. **Dispatch a canales no-in-app:**
   - `email` → `sendEmail()` + template `notificationEmail()` (si `isEmailReady()`).
   - `push` → `sendPush({ userId, title, body, url })` (si `isPushConfigured()`) — itera por todas las `pushSubscriptions` del user (multi-device).
4. **Cleanup piggyback per-user** — un solo paso aplica 3 reglas en orden:
   - Borra notifs con `createdAt < (now - retention.days)`.
   - Borra notifs con `expiresAt` seteado y vencido (`isNotNull` + `lt`).
   - Si todavía quedan más de `retention.maxPerUser`, FIFO drop de las más viejas.

**Por qué piggyback (no cron):** Vercel-friendly (sin scheduled functions extra), users inactivos no incurren queries innecesarias, eventual consistency aceptable porque `maxPerUser` cubre el peor caso. Si el user no genera notifs nuevas, las viejas persisten — el `maxPerUser` actúa como guard.

**Graceful degradation:** errores en email/push se loggean, nunca revientan el `notify()`. El user siempre recibe `in_app`.

`notifyMany({ userIds, ...rest })` — itera `notify()` por user. Cada user resuelve sus propias preferences.

---

## 2. Polling endpoint — `/api/notifications/poll`

**Ubicación:** `src/app/api/notifications/poll/route.ts` → `GET /api/notifications/poll`.

- **Runtime:** serverless default (no `runtime = 'nodejs'`). Sin `runtime = 'edge'` para mantener acceso a `db` Drizzle Node bindings.
- **Auth:** `auth()` de NextAuth — `401` si no hay session.
- **Query:** `Promise.all([items, unreadCount])` — `select` de los 6 más recientes + `count(*)` con `read = false`.
- **`dynamic = 'force-dynamic'`** para evitar caching estático.

**Response shape:**

```jsonc
{
  "items": [
    {
      "id": "uuid",
      "title": "...",
      "body": "...",
      "type": "info",
      "category": "general",
      "url": "/documents/123",
      "read": false,
      "createdAt": "2026-04-26T...",
    },
  ],
  "unreadCount": 3,
}
```

**Por qué polling y no SSE:**

| Eje                      | SSE (anti-patrón en Vercel)     | Polling 30s (este kit)               |
| ------------------------ | ------------------------------- | ------------------------------------ |
| Costo Vercel runtime     | Wall-clock 100% por user activo | ~1% — solo cuando el cliente pide    |
| Latency notif nueva      | <5s                             | hasta 30s (avg ~15s)                 |
| Multi-tab del mismo user | 1 conexión por tab              | 1 fetch/30s por tab visible          |
| Background tabs          | Conexión sigue                  | Polling pausado (`visibilitychange`) |

**Cuándo SSE sí aplica:** infra con servidores persistentes (Render/Railway/Fly.io con proceso Node always-on que no cobra wall-clock). En Vercel/serverless, polling gana por costo.

---

## 3. Push notifications (VAPID, multi-device)

**Ubicación:** `src/lib/notifications/push.ts`. Library: `web-push`.

**APIs server-side:**

- `sendPush({ userId, title, body, url?, icon? })` — envía a **todas** las subscriptions del user (multi-device). Auto-cleanup de subscriptions con `410 Gone` o `404` (endpoint expiró).
- `subscribePush(userId, { endpoint, keys: { p256dh, auth } }, userAgent?)` — upsert por `endpoint`. Si existe, actualiza `keys` (rotación) y `userId`.
- `unsubscribePush(userId, endpoint)` — borra solo si la subscription pertenece al user (ownership check).

**Server actions UI-facing** (en `@/lib/actions/notifications`):

- `getPushDevices()` → lista de pushSubscriptions del current user (`{ id, endpoint, userAgent, createdAt }[]`).
- `removePushDevice({ id })` → DELETE filtered por `userId` (ownership).

**Env vars requeridas** (de `@/lib/env`):

| Var                            | Propósito                           |
| ------------------------------ | ----------------------------------- |
| `NEXT_PUBLIC_VAPID_PUBLIC_KEY` | Public key para suscribir en client |
| `VAPID_PRIVATE_KEY`            | Private key para firmar (server)    |
| `VAPID_SUBJECT`                | `mailto:` o URL del subject         |

**Tabla:** `pushSubscriptions` (schema Drizzle) con `userId`, `endpoint` (unique), `keys: { p256dh, auth }`, `userAgent`, `createdAt`. **Una row por device** (browser × machine) — endpoint es unique per device.

**Graceful degradation:** `ensureVapidInit()` retorna `false` si `!isPushConfigured()` → todos los métodos son no-op. Si faltan VAPID vars, push se desactiva silenciosamente (in_app + email siguen funcionando).

### 3.1 Patrón per-device en UI (regla durable)

> Push subscriptions son inherentemente per-device. **Nunca confíes solo en preferences globales para el state per-device.** El user puede tener push "ON" en preferences (BD) sin tener subscription registrada en el browser actual — y viceversa.

El kit resuelve esto con `PushDevicesList` (sección 5): listas las subscriptions del user, identifica la actual matcheando `endpoint` contra `registration.pushManager.getSubscription()?.endpoint` local, y permite activar / quitar each por separado.

**El bug que esto evita:** user activa en desktop → desktop crea row en BD + global pref `push: true`. Va al mobile, `usePushSubscription` chequea `pushManager.getSubscription()` (browser local) → `false`. Si la UI solo mostrase el toggle global de la preference, el user vería "ON" sin tener sub real en mobile. La lista per-device hace el state explícito.

---

## 4. Client hook — `useNotifications()`

**Ubicación:** `src/lib/hooks/useNotifications.ts`. Consumido por `NotificationBell` y `NotificationPanel`.

```ts
const {
  notifications, // Notification[] (newest first)
  unreadCount, // number — del último poll
  markAsRead, // (id) => void — optimistic + server action
  markAllAsRead, // () => void — optimistic
  deleteNotification, // (id) => void — optimistic
  isConnected, // boolean — última request OK
  isPending, // boolean — transition in-flight
  refetchNotifications, // () => void — fetch manual
} = useNotifications({ enabled: true });
```

**Flujo:**

1. **Polling lifecycle** — `setInterval(fetchPoll, 30_000)`. `fetchPoll` hace `GET /api/notifications/poll` con `cache: 'no-store'`.
2. **Visibility-aware** — listener `visibilitychange`. Cuando la pestaña va a `hidden`, `clearInterval` (stop). Cuando vuelve a `visible`, fetch inmediato + reanuda interval (focus refetch).
3. **`inFlightRef` guard** — evita disparar requests concurrentes si `visibilitychange` se cruza con un fetch en curso.
4. **Mutations** — `markAsRead` / `markAllAsRead` / `deleteNotification` llaman server actions via `useTransition` + optimistic update. El próximo poll resincroniza.
5. **Connection state** — `isConnected` se setea `false` cuando un fetch falla (network/server). Cosmético — no error toast.

**Trade-off honesto:** notif nueva tarda hasta 30s en aparecer (avg ~15s). Para chat real-time esto NO es aceptable; usa Pusher/Ably/Convex. Para in-app dashboard es OK.

### 4.1 Pull-to-refresh integration (mobile)

La página `/notifications` (`src/app/(protected)/notifications/notifications-client.tsx`) es el ejemplo canónico de **wrapper per-screen + opt-out del shell-wide PTR**. El estado de la lista (items, filtros, paginación) vive como state cliente y se refresca llamando `fetchData(page)` — `router.refresh()` (que dispararía el shell PTR del kit) NO actualizaría esa lista. La pantalla silencia el shell con `useDisableShellPTR()` y maneja el gesto con su propio wrapper.

```tsx
import { PullToRefresh } from '@/components/pwa';
import { useDisableShellPTR } from '@/lib/pwa/shellPullToRefresh';

export function NotificationsClient() {
  useDisableShellPTR(); // silence shell while wrapper is mounted
  // ...
  return (
    <PullToRefresh onRefresh={() => fetchData(page)}>
      <div className="flex flex-col gap-4">{/* contenido ... */}</div>
    </PullToRefresh>
  );
}
```

El kit también shippea un botón "Actualizar" visible junto a las acciones (icon `RefreshCw`), por la a11y rule del componente — PTR es gesture-only y siempre debe acompañar un mecanismo accesible. Detalle del shell-wide default, los otros patrones de callback (hook polling, RSC, server tables), y el opt-out → [`sk-pull-to-refresh`](../sk-pull-to-refresh/SKILL.md).

---

## 5. UI Components

**Ubicación:** `src/components/notifications/` (ver catálogo completo en [`sk-ui`](../sk-ui/SKILL.md)).

| Componente                 | Propósito                                                                      |
| -------------------------- | ------------------------------------------------------------------------------ |
| `NotificationBell`         | Icon + badge con `unreadCount`. Abre `NotificationPanel`.                      |
| `NotificationPanel`        | Lista de notifications recientes. Acciones: mark read, delete.                 |
| `NotificationItem`         | Row individual — `type`-aware styling + `url` deep link.                       |
| `NotificationDetailDialog` | Dialog con full body + metadata.                                               |
| `NotificationSettings`     | Matriz de preferences por `category × channel` + bloque `<PushDevicesList />`. |
| `PushDevicesList`          | Lista de subscriptions per-device. Activa/quita push del current device.       |
| `PushPermissionPrompt`     | UI para pedir `Notification.requestPermission()` + `subscribePush`.            |

> **Primitives:** `@/components/ui/*` (shadcn). **No tocar** — ver `SK.md §3.3`. Componer, no forkear.

### 5.1 Component APIs (top-level)

```ts
// NotificationBell — icon + unread badge
interface NotificationBellProps {
  userRole?: string; // opcional — pass-through desde session para RBAC
  className?: string;
}
// Consume internamente useNotifications() — no requiere props de data.

// NotificationPanel — dropdown list
interface NotificationPanelProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  // Se monta como popover desde NotificationBell; raramente se usa standalone.
}

// NotificationSettings — preferences matrix + push devices list
interface NotificationSettingsProps {
  pushConfigured: boolean;
  emailConfigured: boolean;
}

// PushDevicesList — self-contained, no props
// Lee getPushDevices() + matchea current endpoint via pushManager.getSubscription().
```

**Usage mínimo (Header desktop):**

```tsx
import { NotificationBell } from '@/components/notifications/NotificationBell';

<Header>
  <NotificationBell userRole={session.user.role} />
</Header>;
```

**Settings page:**

```tsx
import { NotificationSettings } from '@/components/notifications/NotificationSettings';
import { isPushConfigured, isEmailReady } from '@/lib/env';

export default async function NotificationSettingsPage() {
  await requirePermission('notifications', 'read');
  return (
    <NotificationSettings pushConfigured={isPushConfigured()} emailConfigured={isEmailReady()} />
  );
}
```

---

## 6. Categories × Channels config

**Ubicación:** `src/config/notifications.ts` — **SSOT** de qué categorías existen y qué canales soporta cada una.

**Tipos:**

```ts
export interface NotificationCategory {
  id: string;
  label: string;
  icon: string; // Lucide icon name
  description: string;
  locked: boolean; // user no puede desactivar push/email para esta categoría
  defaultChannels: NotificationChannel[];
  badgeVariant?: 'default' | 'success' | 'error' | 'warning' | 'info';
}
```

**Categoría shipped por default:** **`general`** (unlocked, `defaultChannels: ['in_app']`). El kit ship una sola categoría a propósito — los proyectos derivados extienden.

**Por qué una sola:**

- Evita forzar canales molestos (push/email) bajo `locked: true`. El user del derivado siempre puede opt-out de push/email vía preferences.
- `in_app` siempre es entregado (forzado en `resolveChannels`) — sirve como fallback safe.
- Matrix de preferences queda simple: 1 row × 3 columnas.

**Canales:** `'in_app' | 'push' | 'email'` (`NOTIFICATION_CHANNELS` const).

### 6.1 ¿Qué hace `defaultChannels` exactamente?

`defaultChannels` define qué canales están **ON por default** para una categoría cuando el user nunca tocó esa fila en `NotificationSettings`. Una vez que el user activa o desactiva CUALQUIER toggle de esa categoría, esa preference queda guardada en `notification_preferences` y manda sobre el default — cada canal se resuelve independientemente (§1 step 1).

**No es un gate.** Si una categoría tiene `defaultChannels: ['in_app', 'email']` y el user prende el toggle de push desde `NotificationSettings`, push se entrega normalmente. El default es solo el estado inicial.

**Defaults sanos por categoría — guía:**

| Categoría ejemplo | `defaultChannels` razonable | Razonamiento                            |
| ----------------- | --------------------------- | --------------------------------------- |
| `general`         | `['in_app']`                | Bajo nivel, no merece push ni email     |
| `security`        | `['in_app', 'email']`       | Importante pero no urgente              |
| `sync_alerts`     | `['in_app', 'push']`        | Operativo, push útil; email es ruido    |
| `billing`         | `['in_app', 'email']`       | Legal/papel, email mandatorio por canal |

> **Heurística:** elegí los canales que tendrían sentido si el user nunca abre `NotificationSettings`. No es necesario incluir todos los canales — lo que falte queda OFF por default y el user lo prende si lo quiere.

**Extensión por proyecto:** agregar entry a `NOTIFICATION_CATEGORIES`:

```ts
NOTIFICATION_CATEGORIES.billing = {
  id: 'billing',
  label: 'Facturación',
  icon: 'CreditCard',
  description: 'Pagos y facturas',
  locked: false,
  defaultChannels: ['in_app', 'email'],
  // Initial-ON set. El user puede activar/desactivar push desde
  // NotificationSettings y la preference manda sobre el default.
};
```

**Retention config:** `NOTIFICATION_CONFIG.retention = { days: 30, maxPerUser: 200 }`. Aplicado por el cleanup piggyback del `notify()` (sección 1).

**Helpers:** `getCategory(id)`, `getDefaultChannels(id)`, `isCategoryLocked(id)`, `isValidChannel(ch)`, `isValidNotificationType(t)`.

---

## 7. Cómo disparar una notification nueva (checklist)

1. **Verifica la categoría existe** en `NOTIFICATION_CATEGORIES`. Si no, agrégala primero.
2. **Desde un server action** (usa `withAuth`/`withSelf` del kit — ver [`sk-api`](../sk-api/SKILL.md)):

   ```ts
   import { notify } from '@/lib/notifications';

   export const approveDocument = (input: unknown) =>
     withAuth({ resource: 'documents', action: 'update', schema }, input, async (data, userId) => {
       // ... domain logic
       await notify({
         userId: data.ownerId,
         title: 'Documento aprobado',
         body: `"${data.title}" fue aprobado.`,
         type: 'success',
         category: 'documents', // ← debe existir en config
         url: `/documents/${data.id}`,
       });
       return { ok: true };
     });
   ```

3. **NO llames** `sendPush`/`sendEmail` directo — pasa por `notify()` que resuelve preferences.
4. **NO llames** `toast()` desde server — `notify()` dispara el in_app, el client lo recibe en el siguiente poll y muestra toast opcionalmente (ver `kb-notifications` para UX).
5. **Canales opcionales:** omite `channels` para usar `defaultChannels` de la categoría. Overridea solo si tienes razón explícita.

---

## 8. Dev testing — `testNotification` server action

**Ubicación:** `@/lib/actions/notifications` → `testNotification({ channel, category, type })`.

Dispara una notification de prueba al usuario autenticado. Útil para verificar canales durante desarrollo sin esperar un evento real.

```ts
import { testNotification } from '@/lib/actions/notifications';

await testNotification({
  channel: 'in_app', // 'in_app' | 'push' | 'all'
  category: 'general',
  type: 'info', // info | success | warning | error | system
});
```

**Verificación por canal:**

| Canal    | Cómo verificar                                                                                            |
| -------- | --------------------------------------------------------------------------------------------------------- |
| `in_app` | Bell badge + panel (próximo poll, hasta 30s)                                                              |
| `push`   | Grant browser permission → activar device en `<PushDevicesList />` → `testNotification` → OS notification |
| `email`  | Real address (dominios `@test.com` / `@example.com` auto-skippeados)                                      |

---

## 9. Anti-patterns

| ❌ Anti-pattern                                                    | ✅ Correcto                                                                        |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| `toast.info(...)` directo desde server action                      | `notify({ ..., category })` — el client renderiza toast si procede                 |
| `sendPush(...)` o `sendEmail(...)` sin `notify()`                  | `notify()` resuelve canales, preferences, FIFO, retention                          |
| Crear endpoint SSE en `/api/notifications/stream` para "real-time" | Usar el polling endpoint `/poll` — SSE en Vercel cobra wall-clock (anti-patrón)    |
| Hardcodear `category: 'my-custom'` sin actualizar config           | Agregar a `NOTIFICATION_CATEGORIES` primero (SSOT)                                 |
| Skipear el preference check manual                                 | `notify()` ya aplica preferences — no lo replicar                                  |
| Leer `notifications` table directo desde un componente server      | Usa `getNotifications` action (`@/lib/actions/notifications`)                      |
| Desactivar `in_app` en una categoría                               | `in_app` es forzado por `resolveChannels` — por diseño (safe-by-default)           |
| Disparar `notify()` desde un `useEffect` client                    | Server-side only — el dispatcher requiere DB access                                |
| Mostrar toggle "push" como global sin lista per-device             | Render `<PushDevicesList />` o equivalente — push subs son inherentes per-device   |
| Cron job para cleanup de notifications                             | Piggyback en `notify()` ya cubre retention.days + expires_at + maxPerUser per-user |
| Setear `expires_at` y NO llamar `notify()` en algún momento        | El cleanup es per-user piggyback — corre solo cuando el user genera notifs nuevas  |

---

Cross-reference: [`kb-notifications`](../kb-notifications/SKILL.md) — portable patterns. [`sk-api`](../sk-api/SKILL.md) — server actions que disparan notifs. [`sk-ui`](../sk-ui/SKILL.md) — Bell/Panel/Settings/PushDevicesList components. [`sk-features-index`](../sk-features-index/SKILL.md) — feature catalog.
