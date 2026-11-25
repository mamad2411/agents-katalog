---
name: tracker-hub-apps-builder
description: Construir apps JSX interactivas embebibles dentro de Tracker Hub (renderizadas en /apps/:id/render, opcionalmente expuestas como /kiosk/:slug via views). Cubre componente JSX único + window.__TrackerUI + reglas anti-leak para is_public_safe + endpoints REST y MCP tools (tracker_create_app, tracker_update_app, tracker_set_app_public_safe). Usá este skill SIEMPRE que el usuario quiera crear una UI custom, formulario interactivo, dashboard con interacción, panel embebido, o cualquier app que se pueda mostrar dentro de tracker-hub aunque no mencione "app". También aplicalo si te piden mostrar datos con drilldowns, formularios para humanos, o salida de agente que necesita interacción (no solo lectura).
---

# Tracker Hub Apps Builder

> **Para qué sirve este skill**: construir apps JSX interactivas que se embeben dentro de Tracker Hub.
> El agente que lo lee es responsable de escribir un componente JSX único (`<App />`), respetar las
> reglas anti-leak si el app va a ser público, y elegir entre `tracker_create_app` directo o delegar
> al agente **App Builder** (`0ddf85f84efb9a3a`).

---

## TL;DR — flujo recomendado

1. Discovery — `tracker_list_apps`, `tracker_search` por nombre/tag para no duplicar.
2. Diseñar — qué datos lee, qué interacciones soporta, si va a ser público.
3. Componente JSX — UN solo `<App />` + `ReactDOM.render(<App />, document.getElementById('app-root'))`.
4. Crear — `tracker_create_app { name, jsx, description, is_public_safe? }`.
5. Verificar — abrir `/apps/:id/render` en el browser y probar interacciones.
6. Exponer (opcional) — embeber en una view (`tracker-hub-views-builder` skill).

---

## Modelo conceptual

- Un **app** es JSX que se renderiza dentro de un iframe en `/apps/:id/render`.
- React + Tailwind están disponibles globalmente. NO importar.
- API a tracker-hub via `window.__TrackerUI.*` (HTTP envuelto con auth de la sesión).
- Datos persistidos en `app_data` (key-value JSON por app). Útil para state que sobrevive recargas.
- Output del agente (cuando un agente alimenta el app) via `tracker_set_app_public_safe` + reads del app.

---

## Plantilla mínima

```jsx
function App() {
  const { useState, useEffect } = React;
  const [data, setData] = useState(null);

  useEffect(() => {
    window.__TrackerUI.api.get('/stats').then(setData);
  }, []);

  if (!data) return <div className="p-4">Cargando...</div>;

  return (
    <div className="p-4 space-y-2">
      <h1 className="text-xl font-bold">Stats</h1>
      <div>Total items: {data.total_items}</div>
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById('app-root'));
```

Reglas clave:
- UN solo componente `<App />` exportado.
- `ReactDOM.render(<App />, document.getElementById('app-root'))` al final.
- React/Tailwind global — NO `import`.
- Usar `window.__TrackerUI.*` para llamadas al backend.
- **NO usar `localStorage`** — usa `app_data` via API si necesitás persistencia.

Detalle completo: [`references/jsx-template.md`](./references/jsx-template.md).

---

## API `window.__TrackerUI`

| Método | Uso |
|--------|-----|
| `__TrackerUI.api.get(path)` | GET a `/api/<path>` con auth |
| `__TrackerUI.api.post(path, body)` | POST con body JSON |
| `__TrackerUI.api.put(path, body)` | PUT |
| `__TrackerUI.api.delete(path)` | DELETE |
| `__TrackerUI.user` | Info del usuario actual (id, role, etc.) |
| `__TrackerUI.appId` | ID del app actual |
| `__TrackerUI.refresh()` | Forzar re-render |

Detalle: [`references/tracker-ui-api.md`](./references/tracker-ui-api.md).

---

## MCP tools disponibles

| Tool | Para |
|------|------|
| `tracker_create_app` | Crear app `{name, jsx, description, is_public_safe?}` |
| `tracker_update_app` | Update parcial |
| `tracker_get_app` | Leer app config + JSX |
| `tracker_list_apps` | Listar (filtros: tag, mine) |
| `tracker_delete_app` | Eliminar |
| `tracker_set_app_public_safe` | Toggle `is_public_safe` (gate para BlockApp en kiosk views) |
| `tracker_get_app_outputs` | Leer outputs persistidos (de agentes que escriben al app) |
| `tracker_consume_outputs` | Marcar outputs como consumidos |
| `tracker_run_agent` `agent_id=0ddf85f84efb9a3a` | Delegar al agente App Builder |

---

## Modo público (`is_public_safe`)

Por default, un app requiere auth para `/apps/:id/render`. Para embeber en una view `kiosk` (`is_public:true`), el app debe tener `is_public_safe:true`.

```
tracker_set_app_public_safe app_id=<id> is_public_safe=true
```

**Antes de activar, revisá [`references/public-mode.md`](./references/public-mode.md)** — hay reglas anti-leak críticas (no usar IDs ni datos sensibles en el JSX, no hacer fetches que dependan de auth, etc.).

---

## Cuándo App vs View

| Caso | Elegir |
|------|--------|
| Componer bloques pre-hechos (KPIs, listas, quick actions) sin escribir código | **View** |
| UI custom con interacciones específicas (formularios, drag-drop, drill-downs) | **App** |
| Página pública (kiosko, link compartido) | **View en mode kiosk + apps embebidas con `is_public_safe`** |
| Dashboard mixto: agente actualiza un app + view la muestra junto a otros bloques | **Ambos** — patrón común |

---

## Receta: app que muestra outputs de un agente

```jsx
function App() {
  const { useState, useEffect } = React;
  const [outputs, setOutputs] = useState([]);

  useEffect(() => {
    const load = async () => {
      const data = await window.__TrackerUI.api.get(`/apps/${window.__TrackerUI.appId}/outputs?limit=10`);
      setOutputs(data);
    };
    load();
    const t = setInterval(load, 30000); // refresh cada 30s
    return () => clearInterval(t);
  }, []);

  return (
    <div className="p-4 space-y-3">
      <h1 className="text-2xl font-bold">Reporte del agente</h1>
      {outputs.length === 0 && <div className="text-gray-500">Sin reportes todavía</div>}
      {outputs.map(o => (
        <div key={o.id} className="border rounded p-3">
          <div className="text-sm text-gray-500">{o.created_at}</div>
          <div className="prose" dangerouslySetInnerHTML={{ __html: o.content_html }} />
        </div>
      ))}
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById('app-root'));
```

Más recetas: [`references/recipes.md`](./references/recipes.md).

---

## Errores frecuentes

| Síntoma | Causa | Fix |
|---------|-------|-----|
| App muestra blanco | JSX rompe en runtime | Abrir devtools, ver error en consola |
| `__TrackerUI is not defined` | El bundle no se cargó | Verificar que JSX termine con `ReactDOM.render(...)` |
| App no aparece en kiosk view | `is_public_safe:false` | `tracker_set_app_public_safe` |
| Fetch falla con 401 | Auth no propagada | Usar `__TrackerUI.api` (no `fetch` directo) |
| Tailwind class no funciona | Color/safelist | Tailwind tiene safelist en `tailwind.config.js`; usar colores ya listados |
| App rompe al hacer `import` | React/Tailwind son globals | Quitar imports |

---

## Convenciones

- Tags semánticos: `["app","<dominio>","<categoria>"]`.
- Nombre: descriptivo en español, ej. `"Panel Soporte v2"`.
- JSX < 500 líneas. Si crece, split en varios apps embebidos en una view.
- Persistencia: `app_data` (no localStorage).
- Refresh: poll cada 30s para apps que muestran data en vivo.
- Mobile-first: probar en width ~400px.

---

## App Builder agent (delegación)

Si la app es compleja, delegar al agente **App Builder** (`0ddf85f84efb9a3a`):

```
tracker_run_agent
  agent_id=0ddf85f84efb9a3a
  input="Crear un app que muestre {descripción}"
```

El agente App Builder iterará sobre el JSX y dejará el app listo. Verificá el resultado.

---

## Referencias cruzadas

- [`references/jsx-template.md`](./references/jsx-template.md) — plantilla mínima + reglas
- [`references/tracker-ui-api.md`](./references/tracker-ui-api.md) — `window.__TrackerUI` reference
- [`references/public-mode.md`](./references/public-mode.md) — anti-leak para `is_public_safe`
- [`references/recipes.md`](./references/recipes.md) — recetas end-to-end

Skills hermanos:
- `tracker-hub-agent-bootstrap` — agente que alimenta el app
- `tracker-hub-views-builder` — view donde embeber el app
