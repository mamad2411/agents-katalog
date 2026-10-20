# API Versioning

## Summary

**One-sentence:** Picks a versioning scheme (url-path / accept-header / header-key), classifies a proposed change as breaking or additive, and emits a version-bump plan with deprecation window + sunset header.

**One-paragraph:** API versioning fails most when the team cannot tell whether a change is breaking. This methodology picks one scheme (url-path / accept-header / header-key), runs a breaking-change classifier against the diff (new required field = breaking; new optional field = additive; rename = breaking; etc.), emits the version-bump plan (major if breaking, minor if additive, patch if doc-only), and adds a Sunset header with concrete dates for any deprecation.

**Ефективно для:**

- Solo dev shipping v2 of the public API and unsure which changes are breaking.
- Adding a Sunset header so partners know when to migrate.
- Choosing between /v1/orders vs Accept: application/vnd.example.v1+json — and sticking with the choice.
- Wiring a Spectral rule that fails breaking changes without a major bump.

## Applies If (ALL must hold)

- API has external consumers.
- OpenAPI spec is available (api-openapi-spec).
- Author can ship a version bump + maintain &gt;= 1 prior version during deprecation window.

## Skip If (ANY kills it)

- Pre-public-launch API where breaking changes are free.
- Internal-only API with same-team consumer (synchronised deploys).
- Version pinning per-feature (separate methodology).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| OpenAPI spec (proposed + base) | openapi.yaml + diff | api-openapi-spec |
| Existing versioning policy | info.x-versioning block | current spec |
| Deprecation window | days | platform / partner contract |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-openapi-spec]] | Spec carries the x-versioning policy. |
| [[api-contract-first]] | CI diff gate detects breaking changes. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes by observable signals to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `api_versioning_draft` | sonnet | Bounded synthesis. |
| `api_versioning_validate` | haiku | Mechanical schema check. |
| `api_versioning_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/versioning.py` | Stdlib breaking-change classifier on a spec diff |
| `templates/spectral-rules.yaml` | Spectral ruleset enforcing one-scheme + breaking-change requires major bump |
| `templates/output-schema.json` | JSON Schema (draft-07) for the api-versioning artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in api-versioning artefact for validator round-trip |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-versioning.py` | Validate api-versioning artefact against schema | Pre-commit; CI on each artefact change |

## Related

- [[api-rest-design]]
- [[api-contract-first]]
- [[api-documentation]]
- [[api-openapi-spec]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/versioning.py`

```python
# versioning.py — FastAPI multi-version router with deprecation middleware
# Mount both routers on the FastAPI app:
#   app.include_router(v1)
#   app.include_router(v2)

from fastapi import APIRouter, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

DEPRECATED_AT = "Wed, 01 Jan 2026 00:00:00 GMT"
SUNSET_AT     = "Wed, 01 Jul 2026 00:00:00 GMT"

v1 = APIRouter(prefix="/api/v1")
v2 = APIRouter(prefix="/api/v2")


class V1DeprecationMiddleware(BaseHTTPMiddleware):
    """Inject deprecation headers on all /api/v1/* responses."""

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        if request.url.path.startswith("/api/v1/"):
            response.headers["Deprecation"] = DEPRECATED_AT
            response.headers["Sunset"] = SUNSET_AT
            response.headers["Link"] = '</api/v2>; rel="successor-version"'
        return response


# Shared service (one source of truth — both versions call this)
def _get_user_from_db(user_id: str) -> dict:
    """Fetch user. Replace with real service/repo call."""
    return {"id": user_id, "name": "Alice", "email": "alice@example.com"}


@v1.get("/users/{user_id}")
async def get_user_v1(user_id: str):
    """V1 flat response shape."""
    user = _get_user_from_db(user_id)
    return {"id": user["id"], "name": user["name"]}


@v2.get("/users/{user_id}")
async def get_user_v2(user_id: str):
    """V2 enveloped response shape with meta."""
    user = _get_user_from_db(user_id)
    return {"data": user, "meta": {"version": 2}}
```

### `templates/spectral-rules.yaml`

```yaml
# .spectral.yaml — Enforce API versioning conventions
# Run: npx @stoplight/spectral-cli lint openapi.yaml --ruleset .spectral.yaml

extends: ["spectral:oas"]

rules:
  url-version-prefix:
    description: All paths must start with /api/vN/
    severity: error
    given: "$.paths.*~"
    then:
      function: pattern
      functionOptions:
        match: "^/api/v[0-9]+/"

  deprecation-header-on-v1:
    description: V1 paths must declare Deprecation header in responses
    severity: warn
    given: "$.paths['/api/v1/{*}'].*.responses.*.headers"
    then:
      field: "Deprecation"
      function: truthy

  no-query-param-versioning:
    description: Do not use query parameters for versioning
    severity: error
    given: "$.paths.*.*.parameters[?(@.in == 'query')]"
    then:
      field: "name"
      function: pattern
      functionOptions:
        notMatch: "^(version|v|api_version)$"
```

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/api-versioning.json",
  "type": "object",
  "required": [
    "plan_id",
    "scheme",
    "current_version",
    "next_version",
    "change_kind",
    "deprecation_window_days"
  ],
  "properties": {
    "plan_id": {
      "type": "string",
      "pattern": "^VER-[A-Z0-9-]{2,40}$"
    },
    "scheme": {
      "type": "string",
      "enum": [
        "url-path",
        "accept-header",
        "header-key"
      ]
    },
    "current_version": {
      "type": "string",
      "pattern": "^v?[0-9]+(\\.[0-9]+)?(\\.[0-9]+)?$"
    },
    "next_version": {
      "type": "string",
      "pattern": "^v?[0-9]+(\\.[0-9]+)?(\\.[0-9]+)?$"
    },
    "change_kind": {
      "type": "string",
      "enum": [
        "breaking",
        "additive",
        "docs-only"
      ]
    },
    "breaking_signals": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "deprecation_window_days": {
      "type": "integer",
      "minimum": 1,
      "maximum": 730
    },
    "sunset_date": {
      "type": "string",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "plan_id": "VER-PUBLIC-V2",
  "scheme": "url-path",
  "current_version": "v1",
  "next_version": "v2",
  "change_kind": "breaking",
  "breaking_signals": [
    "Field 'amount' became required on POST /charges",
    "Status 422 added in place of 400 for semantic validation"
  ],
  "deprecation_window_days": 180,
  "sunset_date": "2026-11-23"
}
```
