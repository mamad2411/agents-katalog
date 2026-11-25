---
name: domino-app-init
description: Scaffold a new Domino-ready web application (Vite + React, Streamlit, Dash, Flask, Gradio or FastAPI) with the settings Domino's reverse proxy needs, the mandatory 0.0.0.0:8888 binding, DOMINO_RUN_HOST_PATH prefixes, server-side model endpoint calls, and an app.sh entry point. Use when the user wants to start, initialize, create or scaffold a new app to publish on Domino, or asks for a starter app.sh or starter app for a web framework on Domino.
compatibility: Domino 6.3 and Domino Cloud. Templates only; no API calls. Publishing the result needs a Domino project and a Compute Environment that contains the framework (and Node for Vite).
---

# Initialize a Domino App

Applies to Domino 6.3 and Domino Cloud.

Create a web application that works behind Domino's reverse proxy on the first publish.

Every App must be idempotent: it restarts at any time and can run as several replicas at once, so `app.sh` only starts the server (migrate and seed in a Job), each write is an upsert or carries an idempotency key under a unique constraint, so a retry stores it once, and state lives in a Dataset or database ([details](../domino-apps/FRAMEWORKS.md#make-the-app-idempotent)).

## Inputs

Collect these before writing files. Skip any the user has already given.

1. **Framework**: `vite-react` (default), `streamlit`, `dash`, `flask`, `gradio` or `fastapi`.
2. **Project name**: app folder name and `package.json` name (React only).
3. **Model endpoint integration**: whether the app calls a Domino endpoint. If yes, the call goes through backend code and the user sets `MODEL_API_URL` and `MODEL_API_TOKEN` as Domino Project variables, never in the repository. The URL comes from the user; the token is the user's or one you create and store ([FRAMEWORKS.md](../domino-apps/FRAMEWORKS.md#calling-a-model-endpoint-from-any-framework)).

If the target directory already contains an app, stop and ask before overwriting anything.

## Steps

1. Copy the matching template from this skill's `assets/` folder into the project:

   | Framework | Files to copy |
   |---|---|
   | `vite-react` | From `assets/vite-react/`: `vite.config.js`, `app.sh`, `server.js`, `scripts/build-dist.sh`, `scripts/stamp.sh`, `.env.example`, `.dominoignore` (run `npm create vite@9.3.4` first if there is no Vite project yet; `server.js` needs no packages) |
   | `streamlit` | `assets/streamlit/app.sh`, and `assets/streamlit/app.py.template` saved as `app.py` |
   | `dash` | `assets/dash/app.sh`, and `assets/dash/app.py.template` saved as `app.py` |
   | `flask`, `gradio`, `fastapi` | No template; write the files from the snippets below |

2. Make `app.sh` and `scripts/*.sh` executable (`chmod +x`) and commit the mode (`git update-index --chmod=+x app.sh`).
3. Keep these invariants in every generated file:
   - Bind `0.0.0.0` on port `8888`. Domino requires both; an App on any other address or port fails to start.
   - Where the framework needs its base path, read `DOMINO_RUN_HOST_PATH` (Dash `requests_pathname_prefix`, Gradio `root_path`). Never build the prefix from project owner, name and run ID.
   - Use relative URLs for assets and API calls. For Vite set `base: './'`, use `HashRouter`, and make this the first line of `<head>` in `index.html` (the App URL also answers without its trailing slash): `<script>if (!location.pathname.endsWith('/')) location.replace(location.pathname + '/' + location.search + location.hash)</script>`.
   - Identify the viewer from the `Authorization` token, not `domino-username` alone (`viewer.py` in [FRAMEWORKS.md](../domino-apps/FRAMEWORKS.md#viewer-identity-and-domino-api-calls)).
   - Secrets stay on the server: no token in a `VITE_` variable, no token in the repo.
   - Vite: `app.sh` never installs or builds; it serves a dated build `scripts/build-dist.sh` made ([why](../domino-apps/FRAMEWORKS.md#build-once-and-version-builds)).
4. Add `.env`, `.env.local`, `node_modules/`, `build/` and `dist/` to `.gitignore`; keep `.env.example`. In a DFS Project add `node_modules/` and `build/` to the `.dominoignore` at the Project root (Domino reads only that one).
5. **Check that the framework is in the Compute Environment.** The App runs in the project's environment, without what you `pip install` in a Workspace (`streamlit: not found`, exit 127). Run `python -c "import streamlit"` (or `dash`, `flask`, `gradio`, `fastapi`). Vite: the App needs `node` 18+, the build Node 20.19+ with npm ([REACT-VITE-GUIDE.md](../domino-apps/REACT-VITE-GUIDE.md#build-once-serve-the-build)). If missing: an environment with the package (best), `requirements.txt` at the project root, or `pip install` in `app.sh` for a prototype ([trade-offs](../domino-apps/FRAMEWORKS.md#dependencies)).
6. Finish with the post-initialization checklist.

## Reference snippets

### Dash: `app.py` (Dash 3 removed `run_server`)

```python
import os
from dash import Dash, html

app = Dash(__name__, routes_pathname_prefix="/",
           requests_pathname_prefix=os.environ.get("DOMINO_RUN_HOST_PATH"))
app.layout = html.Div([html.H1("Domino Dash App")])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=False)
```

### Flask: `app.py` and `app.sh`

```python
from flask import Flask, request
from viewer import viewer_name  # viewer.py from domino-apps/FRAMEWORKS.md

app = Flask(__name__)

@app.route("/")
def index():
    return f"Hello {viewer_name(request.headers) or 'viewer'}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=False)
```

```bash
#!/bin/bash
set -e
cd "$(dirname "$0")"
python app.py
```

### Gradio: `app.py` (same `app.sh` as Flask)

```python
import os
import gradio as gr

demo = gr.Interface(fn=lambda text: text, inputs="text", outputs="text")

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8888,
                root_path=os.environ.get("DOMINO_RUN_HOST_PATH", ""))
```

### FastAPI: `app.py` and `app.sh`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Domino FastAPI App"}
```

```bash
#!/bin/bash
set -e
cd "$(dirname "$0")"
uvicorn app:app --host 0.0.0.0 --port 8888
```

### Model endpoint call (any Python framework)

```python
import os, requests
token = os.environ["MODEL_API_TOKEN"]
resp = requests.post(os.environ["MODEL_API_URL"], auth=(token, token),   # synchronous endpoint
                     json={"data": {"feature1": 1.0}}, timeout=60)
```

Asynchronous endpoints take `Authorization: Bearer` instead.

## Post-initialization checklist

Tell the user to:

1. Set `MODEL_API_URL` and `MODEL_API_TOKEN` (if used) in the project's environment variables (see Inputs for where each comes from).
2. Make sure the framework is in the App's environment (step 5), not only the Workspace.
3. **Build, then sync, before publishing.** Vite: `bash scripts/build-dist.sh` (`DIST_DIR=dist` in a DFS Project) after every code change. An App runs the project's committed files, not the Workspace's working copy. DFS project: **File Changes > Sync to Domino** (or the bundled MCP server's upload tool), then check `app.sh` and `app.py` under **Code**. Git-based: `git add`, `git commit`, `git push`, then **Sync All Changes** to save a Vite build in `/mnt/artifacts`. Over the API, pin `content.dfsCommitId` to the uploaded commit ([API-APPS.md](../domino-apps/API-APPS.md)).
4. Optional: check that it starts, on another port (8888 is the IDE's): [FRAMEWORKS.md](../domino-apps/FRAMEWORKS.md#streamlit). Keep 8888 in `app.sh`.
5. Open **App Preview** in the workspace, select `app.sh`, and test: it runs the latest committed code in the real App runtime with the proxy prefix.
6. **Publish App** with the build label (Vite) in the Version Notes, then **Deploy** the version from the App details page and set sharing.

More: `domino-apps` (deploy, CI/CD, frameworks), `domino-debug-proxy` (404s, blank pages, routing), `domino-ui-bootstrap` (design system).
