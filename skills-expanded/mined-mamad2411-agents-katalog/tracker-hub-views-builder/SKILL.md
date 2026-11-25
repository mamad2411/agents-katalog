---
name: tracker-hub-views-builder
description: Componer dashboards y kioskos en Tracker Hub usando vistas agent-driven (rutas /v/:slug con auth, /kiosk/:slug sin auth). Combina bloques nativos (upcoming, approvals, chat, quick_actions, kpi, app) en un layout JSON validado. Usá este skill SIEMPRE que el usuario quiera crear un dashboard, kiosko, pantalla compartida (Raspberry Pi en cocina/oficina), página pública con datos de tracker-hub, vista por usuario, default view per-role, o cualquier composición de bloques aunque no diga "view". También aplicalo si te piden mostrar varias secciones juntas (próximos vencimientos + chat con agente + KPIs), o exponer una pantalla auto-refrescante.
---

# Tracker Hub Views Builder

> **Para qué sirve este skill**: construir dashboards/kioskos componiendo bloques nativos + apps
> embebidas en una vista. El agente que lo lee es responsable de diseñar un layout válido (rows →
> columns → blocks), elegir entre `dashboard` / `kiosk` / `focus`, configurar permisos coherentes
> (`is_public`, `allowed_users`, `required_role`, `default_for_users`), y validar antes de crear.

---

## TL;DR — flujo recomendado

1. Discovery — `tracker_list_views`, `tracker_list_view_block_types` (introspección).
2. Diseñar layout — rows → columns (con `span` 1-12, suma ≤ 12 por row) → blocks.
3. Validar — `tracker_validate_view_layout { layout }` antes de crear.
4. Crear — `tracker_create_view { name, slug, mode, layout, is_public, allowed_users, required_role }`.
5. Default per-user (opcional) — `tracker_set_user_default_view` para que el `/` del usuario redirija ahí.
6. Verificar — abrir `/v/<slug>` (auth) o `/kiosk/<slug>` (público).

---

## Modelo conceptual

- **View**: dashboard configurable con `name` + `slug` (único) + `mode` (`dashboard`/`kiosk`/`focus`) + `layout` (JSON).
- **Modes**:
  - `dashboard`: dentro del Layout normal (sidebar, header). Para uso autenticado.
  - `kiosk`: fullscreen, sin sidebar/header. Para pantallas compartidas (Raspberry Pi, TV).
  - `focus`: similar a dashboard pero sin distracciones.
- **Rutas**: `/v/<slug>` (con auth) y `/kiosk/<slug>` (solo si `is_public:true`).
- **Layout** = `{ rows: [{ id, columns: [{ id, span, blocks: [{ id, type, config }] }] }] }`.
- **Blocks**: tipos nativos (`upcoming`, `approvals`, `chat`, `quick_actions`, `kpi`) + `app` (embebe un app builder).

---

## Bloques nativos

| Tipo | Resumen | Config principal | Soporta `is_public` |
|------|---------|------------------|---------------------|
| `upcoming` | Lista de items con due_date próxima | `days?, workspace_id?, module_id?` | ❌ (necesita scope user) |
| `approvals` | Agent runs en `awaiting_approval` | `agent_id?` | ❌ |
| `chat` | Sesión de chat con un agente | `agent_id` (required) | parcial (sin history) |
| `quick_actions` | Botones para acciones (`create_item`, `run_agent`) | `actions: []` | ❌ |
| `kpi` | Métricas (count, sum, last) sobre items | `metric, scope` | ✅ |
| `app` | Embebe un app JSX | `app_id` (required) | ✅ (si `is_public_safe:true`) |

Detalle por bloque: [`references/block-types.md`](./references/block-types.md).

---

## Esquema del layout

```json
{
  "rows": [
    {
      "id": "row1",
      "columns": [
        {
          "id": "col1",
          "span": 8,
          "blocks": [
            {
              "id": "block-kpi-1",
              "type": "kpi",
              "config": { "metric": "count", "scope": { "status": "open" } }
            }
          ]
        },
        {
          "id": "col2",
          "span": 4,
          "blocks": [
            {
              "id": "block-upcoming",
              "type": "upcoming",
              "config": { "days": 7 }
            }
          ]
        }
      ]
    }
  ]
}
```

Reglas de validación (`tracker_validate_view_layout`):
- `block.id` único en TODA la vista (necesario para refresh granular).
- `column.span` ∈ {1, 2, 3, 4, 6, 12}; suma por fila ≤ 12.
- `row.id` y `column.id` únicos dentro de su scope.
- `block.type` debe estar registrado (`tracker_list_view_block_types`).

Detalle: [`references/layout-schema.md`](./references/layout-schema.md).

---

## MCP tools (22)

**CRUD básico**:
- `tracker_create_view`, `tracker_update_view`, `tracker_get_view`, `tracker_list_views`, `tracker_delete_view`

**Diseño**:
- `tracker_list_view_block_types` (introspección)
- `tracker_validate_view_layout` (sin persistir)
- `tracker_preview_view_data` (resuelve layout con `as_user_id`/`as_public` impersonation)
- `tracker_add_view_block`, `tracker_update_view_block`, `tracker_remove_view_block`

**Permisos**:
- `tracker_set_view_access` (atajo `is_public`/`allowed_users`/`required_role`)
- `tracker_grant_view_permission`, `tracker_revoke_view_permission`
- `tracker_set_user_default_view`

**Gestión**:
- `tracker_clone_view`, `tracker_reorder_views`, `tracker_archive_view`, `tracker_invalidate_view_cache`

**Soporte**:
- `tracker_set_app_public_safe` (para apps embebidos en kiosk)
- `tracker_list_view_users` (audit quién tiene acceso)
- `tracker_get_view_render_url`

---

## Cuándo `is_public:true`

- Vista kiosko en pantalla compartida (cocina, oficina, sala de espera).
- Status page público de un servicio.

**Cuando dudás**: empezá con `is_public:false` y `allowed_users:[...]` explícitos. Abrir más tarde es más fácil que cerrar después de filtrar datos.

Para apps embebidos en kiosk view: el `app.is_public_safe` debe ser `true` también — sino el bloque se renderiza vacío.

Detalle: [`references/permissions.md`](./references/permissions.md).

---

## Receta: vista kiosko Raspberry Pi

```js
// 1) Validar layout
const layout = {
  rows: [
    { id: 'r1', columns: [
      { id: 'c1', span: 12, blocks: [
        { id: 'b1', type: 'app', config: { app_id: '<app-public-id>' } }
      ]}
    ]}
  ]
};
await tracker_validate_view_layout({ layout: JSON.stringify(layout) });

// 2) Asegurar app público-seguro
await tracker_set_app_public_safe({ app_id: '<app-public-id>', is_public_safe: true });

// 3) Crear view kiosko
const view = await tracker_create_view({
  name: 'Familia — Pantalla Cocina',
  slug: 'familia-cocina',
  mode: 'kiosk',
  is_public: true,
  layout: JSON.stringify(layout)
});

// 4) URL para el Pi
const url = await tracker_get_view_render_url({ view_id: view.id });
// → https://hub.tuempresa.com/kiosk/familia-cocina
```

Más recetas: [`references/recipes-kiosk.md`](./references/recipes-kiosk.md).

---

## Receta: vista personal por integrante (clone)

```js
const baseView = await tracker_get_view({ slug: 'familia-base' });
for (const user of familyUsers) {
  const personal = await tracker_clone_view({
    view_id: baseView.id,
    name: `Familia — ${user.display_name}`,
    slug: `familia-${user.username}`,
  });
  // Ajustar config por usuario si querés
  // ej: tracker_update_view_block({ ..., config: { user_id: user.id } })

  // Setearla como default del usuario
  await tracker_set_user_default_view({ user_id: user.id, view_id: personal.id });
}
```

Patrón: 1 base + clones per-user + `set_user_default_view` → cada uno tiene su `/` propio.

---

## Validation antes de crear (gate)

**Siempre** correr `tracker_validate_view_layout` antes de `tracker_create_view`. Si está mal:

```
tracker_validate_view_layout { layout: "{...}" }
→ { valid: false, errors: ["row.id duplicate: r1", "column.span sum > 12 in row r2"] }
```

Sin validación previa, vas a romper la view en producción y los usuarios verán un error 500.

---

## Preview con impersonation (debug)

Para ver cómo se renderiza una view para un usuario específico antes de exponerla:

```
tracker_preview_view_data
  layout="{...}"
  as_user_id="<user-id>"
```

Solo admin/owner puede usar `as_user_id` / `as_public`. Útil para confirmar que los bloques resuelven data correctamente con el scope del usuario destino.

---

## Errores frecuentes

| Síntoma | Causa | Fix |
|---------|-------|-----|
| `slug already exists` | duplicado | Cambiar slug o `tracker_archive_view` el viejo |
| View 404 en `/kiosk/<slug>` | `is_public:false` | `tracker_set_view_access is_public=true` |
| App embebido en kiosk muestra vacío | `apps.is_public_safe:false` | `tracker_set_app_public_safe is_public_safe=true` |
| Block no aparece | `block.type` no registrado | Verificar contra `tracker_list_view_block_types` |
| Row se rompe | suma de `span` > 12 | Re-distribuir |
| Cambios no se reflejan | cache | `tracker_invalidate_view_cache` |
| User no puede acceder | sin `allowed_users` ni `required_role` que matchee | `tracker_grant_view_permission` |
| Default view ignorado | `users.default_view_id` no seteado | `tracker_set_user_default_view` |

---

## Convenciones

- **Slug**: kebab-case, descriptivo (`familia-cocina`, `equipo-soporte-overview`).
- **Tags semánticos** en `name`: incluí el dominio.
- **Block IDs** legibles: `kpi-overdue`, `app-reporte-semanal` (no `b1`, `b2`).
- **Default view por rol**: si todo un equipo necesita la misma vista, considerá `required_role` en vez de granular.
- **Cache**: si la view depende de data que cambia rápido, dejá `cache_version` bajo (default es OK).

---

## Referencias cruzadas

- [`references/layout-schema.md`](./references/layout-schema.md) — esquema JSON + validación
- [`references/block-types.md`](./references/block-types.md) — 6 bloques nativos + config
- [`references/permissions.md`](./references/permissions.md) — `is_public`, `allowed_users`, `required_role`, defaults
- [`references/recipes-kiosk.md`](./references/recipes-kiosk.md) — kiosko Raspberry, clone per-user

Skills hermanos:
- `tracker-hub-apps-builder` — para los apps que vas a embeber en bloques `type:"app"`
- `tracker-hub-agent-bootstrap` — para el agente que alimenta los bloques `chat` y `approvals`
