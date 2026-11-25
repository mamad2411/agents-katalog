---
name: airflow-plugins
description: Build Airflow 3.1+ plugins that embed FastAPI apps, custom UI pages, React components, middleware, macros, and operator links directly into the Airflow UI. Use this skill whenever the user wants to create an Airflow plugin, add a custom UI page or nav entry to Airflow, build FastAPI-backed endpoints inside Airflow, serve static assets from a plugin, embed a React app in the Airflow UI, add middleware to the Airflow API server, create custom operator extra links, or call the Airflow REST API from inside a plugin. Also trigger when the user mentions AirflowPlugin, fastapi_apps, external_views, react_apps, plugin registration, or embedding a web app in Airflow 3.1+. If someone is building anything custom inside Airflow 3.1+ that involves Python and a browser-facing interface, this skill almost certainly applies.
---

# Airflow 3 Plugins

Airflow 3 plugins let you embed FastAPI apps, React UIs, middleware, macros, operator buttons, and custom timetables directly into the Airflow process. No sidecar, no extra server.

> **CRITICAL**: Plugin components (fastapi_apps, react_apps, external_views) require **Airflow 3.1+**. **NEVER import `flask`, `flask_appbuilder`, or use `appbuilder_views` / `flask_blueprints`** — these are Airflow 2 patterns and will not work in Airflow 3. If existing code uses them, rewrite the entire registration block using FastAPI.
>
> **Security**: FastAPI plugin endpoints are **not automatically protected** by Airflow auth. If your endpoints need to be private, implement authentication explicitly using FastAPI's security utilities.
>
> **Restart required**: Changes to Python plugin files require restarting the API server. Static file changes (HTML, JS, CSS) are picked up immediately. Set `AIRFLOW__CORE__LAZY_LOAD_PLUGINS=False` during development to load plugins at startup rather than lazily.
>
> **Relative paths always**: In `external_views`, `href` must have no leading slash. In HTML and JavaScript, use relative paths for all assets and `fetch()` calls. Absolute paths break behind reverse proxies.

### Before writing any code, verify

1. Am I using `fastapi_apps` / FastAPI — not `appbuilder_views` / Flask?
2. Are all HTML/JS asset paths and `fetch()` calls relative (no leading slash)?
3. Are all synchronous SDK or SQLAlchemy calls wrapped in `asyncio.to_thread()`?
4. Do the `static/` and `assets/` directories exist before the FastAPI app mounts them?
5. If the endpoint must be private, did I add explicit FastAPI authentication?

---

## Step 1: Choose plugin components

A single plugin class can register multiple component types at once.

| Component | What it does | Field |
|-----------|-------------|-------|
| Custom API endpoints | FastAPI app mounted in Airflow process | `fastapi_apps` |
| Nav / page link | Embeds a URL as an iframe or links out | `external_views` |
| React component | Custom React app embedded in Airflow UI | `react_apps` |
| API middleware | Intercepts all Airflow API requests/responses | `fastapi_root_middlewares` |
| Jinja macros | Reusable Python functions in DAG templates | `macros` |
| Task instance button | Extra link button in task Detail view | `operator_extra_links` / `global_operator_extra_links` |
| Custom timetable | Custom scheduling logic | `timetables` |
| Event hooks | Listener callbacks for Airflow events | `listeners` |

---

## Step 2: Plugin registration skeleton

### Project file structure

Give each plugin its own subdirectory under `plugins/` — this keeps the Python file, static assets, and templates together and makes multi-plugin projects manageable:

```
plugins/
  my-plugin/
    plugin.py       # AirflowPlugin subclass — auto-discovered by Airflow
    static/
      index.html
      app.js
    assets/
      icon.svg
```

`BASE_DIR = Path(__file__).parent` in `plugin.py` resolves to `plugins/my-plugin/` — static and asset paths will be correct relative to that. Create the subdirectory and any static/assets folders before starting Airflow, or `StaticFiles` will raise on import.

```python
from pathlib import Path
from airflow.plugins_manager import AirflowPlugin
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

BASE_DIR = Path(__file__).parent

app = FastAPI(title="My Plugin")

# Both directories must exist before Airflow starts or FastAPI raises on import
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.mount("/assets", StaticFiles(directory=BASE_DIR / "assets"), name="assets")


class MyPlugin(AirflowPlugin):
    name = "my_plugin"

    fastapi_apps = [
        {
            "app": app,
            "url_prefix": "/my-plugin",   # plugin available at {AIRFLOW_HOST}/my-plugin/
            "name": "My Plugin",
        }
    ]

    external_views = [
        {
            "name": "My Plugin",
            "href": "my-plugin/ui",              # NO leading slash — breaks on Astro and reverse proxies
            "destination": "nav",                # see locations table below
            "category": "browse",                # nav bar category (nav destination only)
            "url_route": "my-plugin",            # unique route name (required for React apps)
            "icon": "/my-plugin/static/icon.svg" # DOES use a leading slash — served by FastAPI
        }
    ]
```

### External view locations

| `destination` | Where it appears |
|--------------|-----------------|
| `"nav"` | Left navigation bar (also set `category`) |
| `"dag"` | Extra tab on every Dag page |
| `"dag_run"` | Extra tab on every Dag run page |
| `"task"` | Extra tab on every task page |
| `"task_instance"` | Extra tab on every task instance page |

### Nav bar categories (`destination: "nav"`)

Set `"category"` to place the link under a specific nav group: `"browse"`, `"admin"`, or omit for top-level.

### External URLs and minimal plugins

`href` can be a relative path to an internal endpoint (`"my-plugin/ui"`) or a full external URL. A plugin with only `external_views` and no `fastapi_apps` is valid — no backend needed for a simple link or tab:

```python
from airflow.plugins_manager import AirflowPlugin

class LearnViewPlugin(AirflowPlugin):
    name = "learn_view_plugin"

    external_views = [
        {
            "name": "Learn Airflow 3",
            "href": "https://www.astronomer.io/docs/learn",
            "destination": "dag",   # adds a tab to every Dag page
            "url_route": "learn"
        }
    ]
```

The no-leading-slash rule applies to internal paths only — full `https://` URLs are fine.

---

## Step 3: Serve the UI entry point

```python
@app.get("/ui", response_class=FileResponse)
async def serve_ui():
    return FileResponse(BASE_DIR / "static" / "index.html")
```

In HTML, always use **relative paths**. Absolute paths break when Airflow is mounted at a sub-path:

```html
<!-- correct -->
<link rel="stylesheet" href="static/app.css" />
<script src="static/app.js?v=20240315"></script>

<!-- breaks behind a reverse proxy -->
<script src="/my-plugin/static/app.js"></script>
```

Same rule in JavaScript:

```javascript
fetch('api/dags')           // correct — relative to current page
fetch('/my-plugin/api/dags') // breaks on Astro and sub-path deploys
```

---

## Step 4-6: API Endpoints, Components & Deployment

> **For JWT auth, DAG/task API patterns, macros, middleware, React apps, operator links, streaming proxy, and deployment, see:**
> `references/api-patterns.md`

---

## Common pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| Nav link 404 | Leading `/` in `href` | `"my-plugin/ui"` not `"/my-plugin/ui"` |
| Nav icon missing | Missing `/` in `icon` | `icon` takes absolute path |
| Event loop freezes | Sync SDK in `async def` | Wrap with `asyncio.to_thread()` |
| 401 after 1 hour | JWT expires, no refresh | Use 5-min pre-expiry refresh |
| StaticFiles raises | Directory missing | Create `assets/` and `static/` first |
| Plugin not showing | Python file changed | `astro dev restart` |
| Endpoints public | FastAPI not auto-authenticated | Add FastAPI security explicitly |
| fetch() breaks | Absolute path | Always use relative paths |

---

## References

- [Airflow plugins docs](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/plugins.html)
- [Airflow REST API reference](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html)
- [Astronomer: Using Airflow plugins](https://www.astronomer.io/docs/learn/using-airflow-plugins)

