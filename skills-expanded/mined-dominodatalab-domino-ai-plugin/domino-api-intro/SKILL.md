---
name: domino-api-intro
description: Introduction to calling Domino platform APIs. Covers authentication (API proxy, access token, PAT, service account), which base URL to use, pagination, and common errors. Use before any other Domino API, SDK, app, extension, or governance automation skill, and whenever a request needs a Domino base URL or credential.
compatibility: Domino 6.3 and Domino Cloud. Requires DOMINO_API_HOST; in a run use DOMINO_API_PROXY or the localhost:8899 access-token endpoint, outside a run a Personal Access Token.
---

# Domino platform API intro

Applies to Domino 6.3 and Domino Cloud.

## Authentication

Reference: https://docs.domino.ai/cloud/reference/api/domino-api-authentication
(same content under `/6.3/`).

| Where the code runs | Base URL | Credential |
|---|---|---|
| Inside a Domino execution (Workspace, Job, App, Launcher) and `DOMINO_API_PROXY` is set | `$DOMINO_API_PROXY` | None. Send **no** `Authorization` header; the proxy adds the starting user's token. |
| Inside a Domino execution, `DOMINO_API_PROXY` not set | `$DOMINO_API_HOST` | `Authorization: Bearer` with the short-lived token from `http://localhost:8899/access-token` |
| Outside Domino (laptop, CI, cron) | The deployment URL users open in the browser; set `DOMINO_API_HOST` to it yourself | `Authorization: Bearer` with a **Personal Access Token** (you; **Account Settings** or `POST /api/pat/v1/tokens`, value returned once: [API-ADMIN.md](../domino-python-sdk/API-ADMIN.md#personal-access-tokens)) or a **service account token** (unattended automation) |

In an App both in-run rows act as the publisher (the user the App run was started as) for every
viewer; to act as the viewer, see [HOSTS.md](./HOSTS.md#inside-an-app).

Legacy user API keys (`X-Domino-Api-Key`, `DOMINO_USER_API_KEY`, `api_key=`) are
deprecated. Never recommend them, not even as a fallback.

### Environment variables as the secret store

Other secrets a Domino execution needs (provider API keys, tokens for other systems) are
Domino environment variables, nothing else: a **user** variable (**Account > Account
Settings > User environment variables**) for a personal credential, injected into every
Workspace, Job and App that user starts and invisible to other users; a **Project** variable
(**Project > Settings > Environment variables**) for a credential the Project's executions
share. Set them in the UI or with the non-public routes below (no Public API or
python-domino route; may change in a future Domino version; on 6.3 confirm the routes in
your deployment's `/docs`). When an
agent stores a secret for the user it writes it with these routes and confirms by
**name only**: the `GET`s return values, so never echo them into a reply or a log. Never
call the wipe-all `DELETE /v4/users/environmentVariables` unless the user explicitly asks
to remove every user variable; to remove one, delete it by name.

```
GET    /v4/projects/{projectId}/environmentVariables           -> [{"name", "value"}]
POST   /v4/projects/{projectId}/environmentVariables           body {"name", "value"}: creates or overwrites that variable
DELETE /v4/projects/{projectId}/environmentVariables/{name}
GET    /v4/users/environmentVariables                          -> {"vars": [{"name", "value"}]} (your own)
PUT    /v4/users/environmentVariables                          body {"NAME": "value", ...}: merged into your variables
DELETE /v4/users/environmentVariables                          DESTRUCTIVE: removes ALL your user variables; to remove one, use the accounts DELETE below
POST   /v4/accounts/idpid/{idpId}/environmentvariables         body {"name", "value"}: one user variable (idpId: GET /api/users/v1/self)
DELETE /v4/accounts/idpid/{idpId}/environmentvariables/{name}
```

```python
requests.post(f"{base_url}/v4/projects/{project_id}/environmentVariables", headers=headers,
              json={"name": "OPENAI_API_KEY", "value": secret})            # never print secret
names = [v["name"] for v in requests.get(f"{base_url}/v4/projects/{project_id}/environmentVariables",
                                         headers=headers).json()]
```

User overrides Project, which overrides the Compute Environment. Neither reaches a
Model API: pass `environmentVariables` (`[{"key", "value"}]`) on
`POST /api/modelServing/v1/modelApis` when you create it, or set them later under the
endpoint's own **Settings** (the update route has no variables field). Code reads them by name
(`os.environ["NAME"]`) and never prints them. Outside Domino (CI, Airflow, a laptop) these
variables are not readable; the external system holds its own copy of a token created in
Domino. Docs: https://docs.domino.ai/cloud/admin/security-and-compliance/protecting-tokens-api-keys
(same under `/6.3/`).

```bash
# Inside a run (preferred)
curl -s "$DOMINO_API_PROXY/api/users/v1/self"

# Inside a run without the proxy
curl -s -H "Authorization: Bearer $(curl -s http://localhost:8899/access-token)" \
  "$DOMINO_API_HOST/api/users/v1/self"

# Outside Domino: DOMINO_API_HOST is the deployment URL, PAT a Personal Access Token or service account token
curl -s -H "Authorization: Bearer $PAT" "$DOMINO_API_HOST/api/users/v1/self"
```

Python setup block used by every example in the API skills:

```python
import os
import requests

if os.environ.get("DOMINO_API_PROXY"):          # inside a Domino execution
    base_url = os.environ["DOMINO_API_PROXY"].rstrip("/")
    headers = {}
elif os.environ.get("DOMINO_RUN_ID"):           # inside a run, proxy not injected
    base_url = os.environ["DOMINO_API_HOST"].rstrip("/")
    token = requests.get("http://localhost:8899/access-token").text.strip()
    headers = {"Authorization": f"Bearer {token}"}
else:                                           # outside Domino: PAT or service account token
    base_url = os.environ["DOMINO_API_HOST"].rstrip("/")
    headers = {"Authorization": f"Bearer {os.environ['PAT']}"}
base = base_url                                 # examples in other skills use either name
```

`DOMINO_RUN_ID`, `DOMINO_PROJECT_ID`, `DOMINO_PROJECT_OWNER`, `DOMINO_PROJECT_NAME`
and `DOMINO_API_HOST` are injected into every execution (glossary:
https://docs.domino.ai/cloud/reference/environment-variables). Inside a run
`DOMINO_API_HOST` can be an in-pod address: never build links for users from it.

## Route types

Most Domino endpoints are stable. Public API routes (`/api/...`, plus `/remotefs/v1` and
`/model-monitor`) are versioned and documented in the published specs. Non-public routes,
meaning the internal API (`/v4/...`, documented per deployment at `https://<domino-domain>/docs`)
and web UI routes, also work, but can change in a future version of Domino. Use a public route
when one exists; where none does, the skills label the call `(non-public route; may change in a
future Domino version)` at the point of use. If a non-public call fails after an upgrade, check
the route in your deployment's `/docs`. Dataset file routes: [HOSTS.md](./HOSTS.md).
Discovery: [API-SPECS.md](./API-SPECS.md).

## Reference files (this skill)

| File | Use when |
|------|----------|
| [HOSTS.md](./HOSTS.md) | Base URL for each API family, Model API invocation, governance, 404 on the in-run base |
| [LIMITS.md](./LIMITS.md) | Pagination envelopes, caps, deprecated credentials and variables |
| [ERRORS.md](./ERRORS.md) | Status codes, retries, error bodies, job status fields |
| [SDK-MAP.md](./SDK-MAP.md) | Which plugin skill covers each API surface |
| [API-SPECS.md](./API-SPECS.md) | OpenAPI files (published and per deployment) and route discovery |

## Next steps

Use the domain skills (domino-python-sdk, domino-jobs, domino-apps, domino-governance,
domino-datasets, netapp-volumes, tags-and-properties, others); they assume the rules above.
