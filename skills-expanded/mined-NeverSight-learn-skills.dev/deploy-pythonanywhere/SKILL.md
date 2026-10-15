---
name: deploy-pythonanywhere
description: Deploy a Flask/WSGI app to PythonAnywhere free tier — automates webapp creation, code upload, WSGI config, reload, E2E test via MCP. Only CLI tool install needs user's Bash console.
disable-model-invocation: true
---

# Deploy to PythonAnywhere

Automate Flask deployment to PA free tier via MCP tools. Only one step needs user's hands: install CLI tools in Bash console. Rest is agent-driven.

## Pre-flight

Gather before starting:
1. **App directory** — local path containing app.py, templates/, etc.
2. **App entry point** — the Flask `app` import (e.g. `from app import app`).
3. **External CLI tools** — any binary the app shells out to (e.g. `officecli`). Agent cannot install these.
4. **Python version** — PA system Python (3.10+); no virtualenv needed — flask/openpyxl available in site-packages.

**Gate:** Items 1-3 confirmed. If app needs CLI tools, tell user to install them in PA Bash console BEFORE agent starts.

## User steps (do these first, then hand off to agent)

User opens PA **Bash console** and runs what applies:

```bash
# 1. pip install extras (if requirements.txt has packages beyond system site-packages)
pip install --user -r /home/<username>/<app-name>/requirements.txt

# 2. CLI tools (if app shells out to any)
curl -fsSL <install-url> | bash
```

No virtualenv needed — system Python has flask/openpyxl. Only run these if app needs extra packages or CLI tools.

**Gate:** User confirms `pip install` succeeded (if needed) + CLI tool `--version` works. Then agent takes over.

## Agent steps (fully automated via MCP)

### Step 1 — Upload code

```python
upload_directory(
    local_dir_path="<local-app-dir>",
    remote_dir_path="/home/<username>/<app-name>"
)
```

Delete stale cache:
```python
delete_path("/home/<username>/<app-name>/__pycache__")
```

**Gate:** `tree("/home/<username>/<app-name>")` shows all expected files; no `__pycache__`.

### Step 2 — Create WSGI entry point

Upload WSGI file via `upload_text_file`:
```python
upload_text_file(
    dest_path="/home/<username>/<app-name>/flask_app.py",
    content="""
import os, sys
os.environ["PATH"] = os.path.expanduser("~/.local/bin") + os.pathsep + os.environ.get("PATH", "")
sys.path.insert(0, os.path.expanduser("~/<app-name>"))
from app import app as application
"""
)
```

Key rules:
- PATH line mandatory if app uses CLI in `~/.local/bin`
- `sys.path.insert` before import
- `as application` is what uWSGI expects

**Gate:** `read_file_or_directory` confirms flask_app.py exists.

### Step 3 — Create webapp

```python
create_webapp(
    domain="<username>.pythonanywhere.com",
    python_version="3.12",
    virtualenv_path="",          # empty — use system Python
    project_path="/home/<username>/<app-name>"
)
```

If webapp already exists, skip to Step 4.

**Gate:** `get_webapp_info` returns webapp with correct `source_directory`.

### Step 4 — Point WSGI to our file

```python
patch_webapp(
    domain="<username>.pythonanywhere.com",
    data={"source_directory": "/home/<username>/<app-name>"}
)
```

Note: PA's WSGI file path is set at creation. If it doesn't match flask_app.py, user must set it in Web tab manually (no API for WSGI path).

**Gate:** `get_webapp_info` shows correct `source_directory`.

### Step 5 — Reload

```python
reload_webapp(domain="<username>.pythonanywhere.com")
```

**Gate:** `curl GET https://<user>.pythonanywhere.com/` returns 200.

### Step 6 — E2E test

1. Homepage: `curl GET` → 200.
2. Upload real file:
   ```bash
   curl -s -w "\nHTTP:%{http_code} TIME:%{time_total}" \
     --max-time 300 \
     -X POST -F "file=@<source-file>" \
     "https://<user>.pythonanywhere.com/<endpoint>" \
     -o /tmp/pa_result.xlsx
   ```
3. Verify output: correct row count, correct totals vs known-good reference.

**Gate:** HTTP 200, output validates. If 400/500, read error log:
```python
read_file_or_directory("/var/log/<user>.pythonanywhere.com.error.log")
```
Diagnose + fix + reload + retest.

## Gotchas (learned the hard way)

**`TemporaryDirectory` race.** uWSGI lazy streaming + `TemporaryDirectory.__exit__` = `OSError: [Errno 39] Directory not empty`. Fix: manual `tempfile.mkdtemp()` + `shutil.rmtree(ignore_errors=True)` in `finally`, `send_file(io.BytesIO(result_bytes))` OUTSIDE try/finally.

**Stale `__pycache__`.** Python serves cached `.pyc` after source changes. Every deploy: `delete_path(__pycache__)` + `reload_webapp`. Symptom: old errors persist in error log.

**`send_file` needs file-like.** Raw `bytes` → `AttributeError`. Wrap in `io.BytesIO()`.

**Free tier sleep.** 20-40s cold start after idle. Normal.

**No virtualenv needed.** PA system Python has flask/openpyxl in site-packages. Don't create one — wastes time.

**WSGI path.** PA sets this at webapp creation and shows it in Web tab. If it doesn't match the uploaded WSGI file, user must manually update in Web tab config (no API).

## Deploy update (code change only)

When code changes but webapp already exists:
1. `upload_directory` new code
2. `delete_path(__pycache__)`
3. `reload_webapp`
4. E2E test

Skip Steps 2-4 (webapp + WSGI already configured).
