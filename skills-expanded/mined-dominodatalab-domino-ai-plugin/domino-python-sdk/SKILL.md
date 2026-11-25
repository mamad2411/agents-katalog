---
name: domino-python-sdk
description: Programmatically interact with Domino using the python-domino SDK and the Domino REST API. Covers authentication, starting and monitoring jobs, managing projects, files, datasets, environments and Model APIs, and automation from CI/CD. Use when automating Domino workflows, integrating Domino with external systems, or building custom tooling around Domino. For multi-step pipelines inside Domino use domino-flows; for an existing Airflow or Kubeflow deployment use domino-airflow-kubeflow; for exporting a model image from CI/CD use domino-model-delivery; for the domino command-line client and the R package use domino-cli.
compatibility: Domino 6.3 and Domino Cloud. Requires DOMINO_API_HOST; in a run use DOMINO_API_PROXY or the localhost:8899 access-token endpoint, outside a run a Personal Access Token. python-domino (dominodatalab 2.2.0) needs Python 3.10 or later.
---

# Domino Python SDK and REST API

Applies to Domino 6.3 and Domino Cloud. Read
[domino-api-intro](../domino-api-intro/SKILL.md) first for auth and base URLs.

## Two surfaces

| | python-domino (`dominodatalab` on PyPI) | REST Public API |
|---|---|---|
| Covers | Projects, jobs and legacy runs, files, datasets, environments, hardware tiers, Model APIs, apps, budgets and billing tags | Everything in the published spec, including what the SDK does not wrap: NetApp volume mounts on jobs, taxonomy, governance, audit trail, service accounts, PATs |
| Use for | Quick scripts inside Domino, existing automation | New automation and anything the SDK lacks |

Other Domino skills show REST, not python-domino; the SDK wraps older routes and lags the
Public API. Method names follow python-domino 2.2.0.

## Installation

```bash
pip install "dominodatalab==2.2.0"          # Python 3.10 or later
pip install "dominodatalab[data]==2.2.0"    # adds the Domino Data API client (domino_data)
```

Docs: https://docs.domino.ai/cloud/reference/python-sdk/python-domino

## Authentication

Follow [domino-api-intro](../domino-api-intro/SKILL.md#authentication). python-domino
resolves credentials in this order (from the docs page above): `api_proxy`, `auth_token`,
`domino_token_file`, `api_key`, then the environment variables `DOMINO_API_PROXY`,
`DOMINO_TOKEN_FILE`, `DOMINO_USER_API_KEY`. Never pass `api_key=` or rely on
`DOMINO_USER_API_KEY`; both are deprecated.

Inside a Domino execution with `DOMINO_API_PROXY` set, no credential argument is needed:
the constructor reads `DOMINO_API_HOST` and `DOMINO_API_PROXY` from the environment. If
the proxy is not set, pass the short-lived access token explicitly; otherwise the client
falls back to `DOMINO_TOKEN_FILE` and then the deprecated `DOMINO_USER_API_KEY`.

```python
import os
import requests
from domino import Domino

project = f"{os.environ['DOMINO_PROJECT_OWNER']}/{os.environ['DOMINO_PROJECT_NAME']}"
if os.environ.get("DOMINO_API_PROXY"):
    domino = Domino(project)
else:
    domino = Domino(project, auth_token=requests.get("http://localhost:8899/access-token").text.strip())
```

`domino.authenticate(auth_token=...)` refreshes the token on a long-running client.

Outside Domino, pass the deployment URL and a Personal Access Token or service account
token; `auth_token` is sent as `Authorization: Bearer`:

```python
domino = Domino(
    "owner/project-name",
    host=os.environ["DOMINO_API_HOST"],          # deployment URL
    auth_token=os.environ["PAT"],                # PAT or service account token
)
```

Notes: the `project` argument (`owner/name`) is required; the constructor calls
`GET /version` and refuses incompatible Domino versions; `api_proxy` only works inside a
run (it does not work against an HTTPS endpoint).

REST calls use the shared setup block in
[domino-api-intro](../domino-api-intro/SKILL.md#authentication) (`base_url`, `headers`).

## Common operations

Supported and deprecated python-domino methods, with examples for jobs, files, datasets,
environments, Model APIs, apps and CI/CD: [SDK-EXAMPLES.md](./SDK-EXAMPLES.md).

## REST API

Route catalog with request bodies from the specs: [API-REFERENCE.md](./API-REFERENCE.md).
Per-area files:

| Guide | Description |
|-------|-------------|
| [SDK-EXAMPLES.md](./SDK-EXAMPLES.md) | python-domino method table, examples, error handling |
| [API-PROJECTS.md](./API-PROJECTS.md) | Projects, collaborators, git repositories, goals, shared datasets |
| [API-JOBS.md](./API-JOBS.md) | Start, list, inspect and poll jobs; logs, tags, goals |
| [API-DATASETS.md](./API-DATASETS.md) | Datasets, snapshots, tags, grants, mount paths |
| [API-MODELS.md](./API-MODELS.md) | Model APIs, model deployments, registered models, invoking endpoints |
| [API-MODEL-SERVING.md](./API-MODEL-SERVING.md) | Registry v1/v2 split, lifecycle, invoke vs management |
| [API-ENVIRONMENTS.md](./API-ENVIRONMENTS.md) | Environments, revisions, build status |
| [API-APPS.md](./API-APPS.md) | Apps beta catalog (v1 publish chain is in [domino-apps](../domino-apps/API-APPS.md)) |
| [API-ADMIN.md](./API-ADMIN.md) | Users, organizations, service accounts, PATs, hardware tiers, data sources, cost, audit trail |
| [API-REFERENCE.md](./API-REFERENCE.md) | Complete route index and shared conventions |

## Rules

- Verify every route against both published specs before using it
  ([API-SPECS.md](../domino-api-intro/API-SPECS.md)). `/v4/*` routes are the Domino
  Internal API: non-public routes that may change in a future Domino version; the files above label the few that remain.
- Field names are not interchangeable across routes: `POST /api/jobs/v1/jobs` takes
  `runCommand` and `hardwareTier`; python-domino `job_start` takes `command` and
  `hardware_tier_id`.
- Treat beta routes (`metadata.notices` says "Beta endpoint with known limitations") as
  subject to change.

## Related skills

- [domino-flows](../domino-flows/SKILL.md) and scheduled Jobs ([domino-jobs](../domino-jobs/SKILL.md)):
  the default for pipelines and recurring runs; no external orchestrator needed.
- [domino-airflow-kubeflow](../domino-airflow-kubeflow/SKILL.md): `domino.airflow` (`DominoOperator`,
  `DominoSparkOperator`) for an Airflow or Kubeflow deployment you already run, why their pins clash with Airflow's constraints, and the `requests`-only
  task on the Public Jobs API; Kubeflow components.
- [domino-model-delivery](../domino-model-delivery/EXPORT-API.md): what `model_version_export`,
  `model_version_export_status` and `model_version_export_logs` call, the build step the SDK does
  not wrap, and a CI/CD pipeline that exports the image.
- [domino-cli](../domino-cli/SKILL.md): the `domino` command-line client and the R package, for
  syncing project files and starting Jobs from a laptop without writing API calls.

## Documentation

- https://docs.domino.ai/cloud/reference/api/domino-api-authentication
- https://docs.domino.ai/cloud/reference/python-sdk/python-domino
- https://github.com/dominodatalab/python-domino
