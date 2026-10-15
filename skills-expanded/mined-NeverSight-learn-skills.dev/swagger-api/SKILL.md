---
name: swagger-api
description: "Use when a project exposes a Swagger 2.0 or OpenAPI 3.x JSON document and work requires finding endpoints, inspecting request or response schemas, checking existing calls against the contract, or implementing an API integration."
---

# Swagger API

Use the live Swagger/OpenAPI JSON document as the interface source of truth. Do not scrape the rendered documentation page or maintain a copied endpoint catalog.

If the user provides only a Swagger UI URL, inspect that page's configuration or loaded resources to locate the raw JSON document first. Do not probe unrelated paths when the page already exposes the source URL.

## Lookup

Run [`scripts/swagger_api.py`](scripts/swagger_api.py) from this skill directory, or use its absolute installed path:

```bash
python3 scripts/swagger_api.py --url URL info
python3 scripts/swagger_api.py --url URL list --tag TAG
python3 scripts/swagger_api.py --url URL search KEYWORD
python3 scripts/swagger_api.py --url URL show /path --method POST
```

Set `SWAGGER_DOC_URL` in an ignored project-root `.env.local` instead of repeating `--url` when the current project has one stable document. The script loads `.env.local` and then `.env` from the current working directory; see [`README.md`](README.md) for precedence and examples. It accepts Swagger 2.0 and OpenAPI 3.x JSON.

Use `search` to locate candidates, then `show` to read the complete operation and every recursively referenced request or response schema. Report specification-declared facts separately from inferences or behavior observed only in application code or runtime traffic.

## Authentication

For a document protected by HTTP Basic authentication, supply credentials only through the process environment:

```bash
export SWAGGER_USERNAME='...'
export SWAGGER_PASSWORD='...'
```

For another HTTP authorization scheme, set the complete header value with `SWAGGER_AUTHORIZATION`. Do not combine it with the Basic variables.

Do not print, persist, or commit credentials. Basic authentication over plain HTTP is not transport-encrypted. Keep authentication protecting the documentation separate from authentication declared by or embedded in the business API.

## Integration Work

Before changing a caller, inspect its existing request wrapper, authentication source, serialization, and response handling. Reuse that path and compare it with `show` output; do not generate a second API client or assume example values are production defaults.

The bundled script only reads the API definition. Actual business requests require a separate explicit user request and the target project's existing authenticated request path.
