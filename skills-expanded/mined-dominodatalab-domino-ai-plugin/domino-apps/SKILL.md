---
name: domino-apps
description: Publish, deploy, update, restart, stop or roll back a web application as a Domino App, and automate those steps over the Apps API or a CI/CD pipeline. Use whenever the user wants to publish, deploy, ship, launch, release or host an app (React/Vite, Streamlit, Dash, Flask, Shiny, Gradio, FastAPI, Rust) on Domino, make an existing app work behind Domino's reverse proxy (app.sh entry point, mandatory 0.0.0.0:8888, DOMINO_RUN_HOST_PATH, relative base, HashRouter, server-side model endpoint calls), create a new App version, deploy an older version, start or stop an App over /api/apps/v1, or set up GitHub Actions deployment to Domino. Not for scaffolding a brand-new app from scratch (domino-app-init) or for diagnosing 404s, blank pages or broken routing in an already published app (domino-debug-proxy); use it when those hand off to publishing.
compatibility: Domino 6.3 and Domino Cloud. Requires DOMINO_API_HOST; in a run use DOMINO_API_PROXY, outside a run a Personal Access Token or service account token.
---

# Domino Apps

Applies to Domino 6.3 and Domino Cloud.

A Domino App runs project code in a container behind Domino's reverse proxy. The proxy authenticates every request, strips the App's URL prefix, and forwards the viewer's token as `Authorization: Bearer` (secure identity propagation, the default).

## Rules every App must satisfy

1. **Make the App idempotent.** It restarts at any time and can run as several replicas at once: startup changes nothing (migrate and seed in a Job before publishing), each write is an upsert or carries an idempotency key under a unique constraint, so a retry stores it once, and state lives in a Dataset or database, not in memory or on the App's disk ([details](./FRAMEWORKS.md#make-the-app-idempotent)).
2. **Serve on `0.0.0.0:8888`.** An App that does not expose a server on that address and port fails to start. Port 8888 is mandatory, not a default.
3. **The entry point is a launch file** in the project (`app.sh`, or a Python or R script). It is fixed for the life of the App; create a new App to change it.
4. **Read the URL prefix from `DOMINO_RUN_HOST_PATH`** wherever a framework needs its base path (Dash `requests_pathname_prefix`, Gradio `root_path`). Never assemble it from the project owner, name and run ID; the prefix is not derived from them.
5. **Use relative URLs** for assets and API calls (Vite `base: './'`, `new URL('api/', document.baseURI)`), never root-absolute `/assets/...` or `fetch('/api/...')`. They break when the App URL lacks its trailing slash; add it ([details](./FRAMEWORKS.md#behind-dominos-app-proxy)).
6. **Keep secrets on the server.** Model endpoint tokens live in project or user environment variables and are read by backend code. Anything in a `VITE_`-prefixed variable is compiled into the browser bundle.

## Quick start

| Framework | `app.sh` runs | Details |
|---|---|---|
| Vite + React | `node server.js` serving a build made once by `scripts/build-dist.sh`; never installs or builds | [REACT-VITE-GUIDE.md](./REACT-VITE-GUIDE.md) |
| Streamlit | `streamlit run app.py --server.port 8888 --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false` | [FRAMEWORKS.md](./FRAMEWORKS.md) |
| Dash | `python app.py` with `Dash(__name__, routes_pathname_prefix='/', requests_pathname_prefix=os.environ.get('DOMINO_RUN_HOST_PATH'))` and `app.run(host='0.0.0.0', port=8888)` | [FRAMEWORKS.md](./FRAMEWORKS.md) |
| Flask | `python -m flask run --host=0.0.0.0 --port=8888` or `gunicorn -w 4 -b 0.0.0.0:8888 app:app` | [FRAMEWORKS.md](./FRAMEWORKS.md) |
| Shiny | `R -e 'shiny::runApp("./", port=8888, host="0.0.0.0")'` | [FRAMEWORKS.md](./FRAMEWORKS.md) |
| Rust (axum) | the prebuilt binary; never compiles | [domino-rust-apps](../domino-rust-apps/SKILL.md) |

Vite: `base: './'` and `HashRouter`; `BrowserRouter` breaks nested routes.

## Lifecycle

Create, publish and deploy are separate steps. Publishing records an immutable version (code commit, environment revision, mounts, identity propagation); deploying starts it. Hardware tier, autoscaling, vanity URL and iframe settings are deployment settings: changing them restarts the instance without creating a version. Develop in a workspace with **App Preview** (a real App runtime, author-only at `/preview/<draftAppId>`), then **Publish App**, then **Deploy** the version from the App details page.

Check three things before publishing. **Builds**: Vite and Rust Apps start a build made once in a Workspace or Job, named by date, with the previous build kept and the label in Version Notes ([details](./FRAMEWORKS.md#build-once-and-version-builds)). **Files**: the App runs the project's committed files, so sync first (DFS Workspace: **File Changes > Sync to Domino**; Git-based: commit and push) or the start fails with `entry script 'app.sh' not found`. **Packages**: the App uses the project's Compute Environment, not what you `pip install` in a Workspace (`streamlit: not found`, exit 127); check with `python -c "import <framework>"` and fix it as [FRAMEWORKS.md](./FRAMEWORKS.md#dependencies) shows.

## Environment variables and headers

Injected at start: `DOMINO_RUN_HOST_PATH` (URL prefix, trailing `/`), the `DOMINO_PROJECT_*` and `DOMINO_RUN_ID` identifiers, `DOMINO_STARTING_USERNAME` (who started the run, not the viewer), `DOMINO_API_HOST` and `DOMINO_API_PROXY` (in-cluster API addresses; never in browser links), plus project and user environment variables ([full list](./FRAMEWORKS.md#environment-variables)). The viewer is the token's `preferred_username` claim; read `domino-username` only when no token arrives (Apps with extended identity propagation never get it, and there a client can send its own).

## Calling Domino APIs and model endpoints from an App

- **As the publisher** (the user who started the App): `$DOMINO_API_PROXY/api/...` with no `Authorization` header; code that needs a bearer gets one per request from `$DOMINO_API_PROXY/access-token`.
- **As the viewer**: the request's bearer token on `$DOMINO_API_HOST`. Without extended identity propagation (published by a SysAdmin or CloudAdmin; viewer consent) most routes reject it, often with 500 ([details](./FRAMEWORKS.md#viewer-identity-and-domino-api-calls)). No token: return 401, since `$DOMINO_API_HOST` runs calls without `Authorization` as the publisher.
- **Model endpoints**: from backend code only, with `MODEL_API_URL` and `MODEL_API_TOKEN` from Project environment variables; HTTP Basic with the token as username and password for synchronous endpoints, a bearer for asynchronous ones ([details](./FRAMEWORKS.md#calling-a-model-endpoint-from-any-framework)).

Auth: https://docs.domino.ai/cloud/reference/api/domino-api-authentication ; legacy API keys (`X-Domino-Api-Key`) are deprecated.

## REST automation

`/api/apps/v1` for create, versions, publish (drafts), start and stop; `/api/apps/beta` only for instance reads (list instances, logs, real-time logs, views). Full chain, bodies and the logs route: [API-APPS.md](./API-APPS.md). CI/CD with GitHub Actions and a service account: [REACT-CICD.md](./REACT-CICD.md).

## Reference files

- [REACT-VITE-GUIDE.md](./REACT-VITE-GUIDE.md): Vite config, Express backend, HashRouter, App Preview
- [REACT-CICD.md](./REACT-CICD.md): GitHub Actions workflow and Public API deploy script
- [FRAMEWORKS.md](./FRAMEWORKS.md): Streamlit, Dash, Flask, Gradio, FastAPI, Shiny, dependencies, viewer identity, proxy behaviour and limits
- [API-APPS.md](./API-APPS.md): v1 vs beta routes, publish chain, logs
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md): symptoms, causes and fixes

Docs: https://docs.domino.ai/cloud/platform-capabilities/core-concepts/apps (same under `/6.3/`). Related skills: `domino-app-init` (scaffold), `domino-debug-proxy` (diagnose), `domino-api-intro` (auth, hosts), `domino-ui-bootstrap` (design system SPA), `domino-extensions` (mount an App in the Domino UI).
