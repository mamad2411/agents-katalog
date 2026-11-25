---
name: domino-debug-proxy
description: Diagnose and fix Domino reverse-proxy and routing problems in published web apps by checking vite.config.js, package.json, app.sh, server.js and Python entry points (app.py) for the wrong port, localhost binding, absolute base paths, a hand-built URL prefix instead of DOMINO_RUN_HOST_PATH, BrowserRouter deep links, missing build steps, or a model token compiled into the browser bundle. Use when a Domino app never reaches Running, shows connection refused, 404s on CSS or JS assets, a blank page, broken deep links, or stopped working after a restart, and when fetch gets HTML instead of JSON, Domino API calls from the app fail (401, 403, 500) or act as the publisher, streaming stalls, or uploads get 413.
compatibility: Domino 6.3 and Domino Cloud. Reads project files; the optional log check needs DOMINO_API_PROXY in a run, or the deployment URL and a Personal Access Token outside one.
---

# Debug Domino App proxy issues

Applies to Domino 6.3 and Domino Cloud.

Find the configuration mistakes that break apps behind Domino's reverse proxy, report them, and fix them with the user's agreement. The proxy authenticates each viewer, strips the App's URL prefix (`<prefix>` and `<prefix>/` both arrive as `/`), forwards to port 8888, and by default passes the viewer's token as `Authorization: Bearer` (`domino-username` is a copy that Apps with extended identity propagation do not get).

## Steps

1. Locate the app's files: `app.sh` (or the Python/R entry point Domino runs), `vite.config.js` or `vite.config.ts`, `package.json`, `server.js`, `src/main.jsx` or `main.tsx`, and `app.py`.
2. Run every check below and record each result as pass or fail.
3. Print a report in the format shown under "Report format".
4. List the recommended fixes and ask whether to apply them. Apply only what the user approves.
5. For anything you can't fix from config, give the manual investigation steps.

## Checks

| # | Check | Pass condition |
|---|---|---|
| 1 | Port and host | The process Domino starts listens on `0.0.0.0:8888` (`serve -l 8888`, `app.listen(8888, '0.0.0.0')`, `--server.port 8888 --server.address 0.0.0.0`, `app.run(host="0.0.0.0", port=8888)`, `uvicorn --host 0.0.0.0 --port 8888`). Domino rejects any other address or port |
| 2 | Base path | Vite sets `base: './'`; HTML templates reference `static/...`, never `/static/...` |
| 3 | Router | React Router uses `HashRouter` (pass). `BrowserRouter` is a warning: it needs an SPA fallback on the server (the template `server.js`, or `serve -s`) and breaks relative assets on nested routes; a build made before publishing cannot know the prefix for an absolute `base` |
| 4 | `app.sh` | Executable (`git update-index --chmod=+x app.sh`), changes to its own directory (`cd "$(dirname "$0")"`), and never installs or builds: it serves a build made once by `scripts/build-dist.sh` whose stamp matches the code ([build once](../domino-apps/FRAMEWORKS.md#build-once-and-version-builds)); packages belong in the Compute Environment |
| 5 | Prefix | Python frameworks that need a base path read `DOMINO_RUN_HOST_PATH` (Dash `requests_pathname_prefix`, Gradio `root_path`); nothing concatenates `DOMINO_PROJECT_OWNER`, `DOMINO_PROJECT_NAME` and `DOMINO_RUN_ID` into a path; nothing reads `X-Script-Name` (Domino never sends it) |
| 6 | Asset and API references | No root-absolute `fetch('/api/...')` or `/assets/...`; frontend API calls resolve with `new URL('api/', document.baseURI)`; the entry page adds a missing trailing slash |
| 7 | Secrets | No `VITE_*_TOKEN` or `VITE_*_KEY` in `.env*`, workflow files or source; model endpoint calls happen in `server.js`, Flask, FastAPI or another backend. Synchronous endpoints use HTTP Basic (token as user and password), asynchronous ones Bearer |
| 8 | Dash API | `app.run(...)`, not `app.run_server(...)` (removed in Dash 3) |
| 9 | Identity | Viewer from the token's `preferred_username` (`domino-username` only without a token); viewer calls forward the token, answer 401 without one, never retry header-less; no browser link from `DOMINO_API_HOST` or `DOMINO_USER_HOST` |

## Common issues

| Symptom | Cause | Fix |
|---|---|---|
| Never reaches Running | Bound to `localhost` or a port other than 8888 | Listen on `0.0.0.0:8888` |
| 404 on CSS and JS | `base` is `/` or missing | `base: './'` in `defineConfig`; rebuild and republish |
| Deep links or refresh return 404 | `BrowserRouter` routes reach the server | Switch to `HashRouter`, or keep `BrowserRouter` with an SPA fallback (`server.js`, `serve -s`) |
| `no build matches these sources`, stale content | No saved build of the saved code, or no new version published | Run `scripts/build-dist.sh`, save, publish; `/healthz` names the running build |
| Worked, then failed after a restart | Hand-built prefix instead of `DOMINO_RUN_HOST_PATH` | Read the prefix from `DOMINO_RUN_HOST_PATH` |
| Model call 401 | Bearer sent to a synchronous endpoint, or token missing | Basic auth with the Model Access Token as user and password; set `MODEL_API_TOKEN` in project settings and restart |
| Model call CORS error | Browser calls the endpoint directly | Route it through the backend |
| `import.meta.env.VITE_X` undefined | Variable not set when `npm run build` ran, or no `VITE_` prefix | Prefix non-secret build-time values; keep runtime values server-side |
| 404 on assets or `api/` only when the URL has no trailing slash | `<prefix>` arrives as `/`; relative URLs resolve one level up | Add the slash first thing in `<head>` ([RUNTIME.md](./RUNTIME.md#limits-and-branding)) |
| `fetch` gets HTML (`Unexpected token '<'`) or a 302; Domino API calls fail (500, 403, 401) or act as the publisher | Consent, identity mode, credential type, or a dropped viewer token | [RUNTIME.md](./RUNTIME.md) |
| Streaming stalls or drops, 413, 400 on the direct URL, favicon 404 | Proxy buffering and limits, Apps only allowed inside Domino, injected branding | [RUNTIME.md](./RUNTIME.md#limits-and-branding) |

The corrected `app.sh` for a Vite app is the `domino-app-init` template ([app.sh](../domino-app-init/assets/vite-react/app.sh)): it serves the newest build whose stamp matches the code with `node server.js` and never runs npm.

## Report format

```
Domino Proxy Debug Report
=========================

Checking: vite.config.js
PASS Port: 8888, host 0.0.0.0
PASS Base path: './'

Checking: src/main.jsx
WARN Router: BrowserRouter with base './' (deep links 404; nested routes break assets)

Checking: app.sh
PASS Working directory: cd "$(dirname "$0")"
PASS Starts a prebuilt build (no npm ci or npm run build)
FAIL Serve command missing -s flag

Summary: 1 issue, 1 warning

Recommended fixes:
1. Replace BrowserRouter with HashRouter in src/main.jsx (or keep it with an SPA fallback)
2. Update the app.sh serve command:
   - Current: npx serve dist -l 8888
   + Fixed:   npx serve -s dist -l 8888
```

## Manual investigation

If the config is correct but the app still fails:

1. Read the App logs on the App details page (instance selector; support bundle for Kubernetes and nginx logs). Over the API: `GET /api/apps/beta/apps/{appId}/versions/{versionId}/instances`, then `GET .../instances/{instanceId}/logs?logType=stderr`, on `$DOMINO_API_PROXY` with no `Authorization` header (outside a run, the deployment URL with a Personal Access Token).
2. In the browser developer tools, check whether failing requests dropped the App's URL prefix (the path before the app's own routes) or went to another host.
3. Confirm the App was republished after the last commit: a version pins a commit, and deploying an old version serves old code.
4. Test in a workspace with **App Preview**, which runs the real proxy and `DOMINO_RUN_HOST_PATH`; a local `npm run dev` cannot reproduce them.

Identity, consent, streaming, limits and branding symptoms: [RUNTIME.md](./RUNTIME.md). For general deployment guidance, framework configs and the REST routes, use the `domino-apps` skill.
