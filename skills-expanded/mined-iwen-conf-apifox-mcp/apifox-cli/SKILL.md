---
name: apifox-cli
description: Write and maintain Apifox/OpenAPI documentation through the apifox-cli Go CLI. Use when Codex needs to read source code, routes, DTOs, validation rules, or product requirements; author .apifox-docs.json, .apifox-endpoint.json, .apifox-crud.json, or .apifox-schema.json; validate and dry-run them; apply them to Apifox; inspect endpoints/schemas/tags; or audit API response and naming consistency without Swagger marker comments or MCP tool calls.
---

# Apifox CLI

Use `apifox-cli` as a command-line tool. Do not call MCP tools, do not use `list-tools`, `describe`, or `call`, and do not use Swagger marker comments as the primary Go documentation path.

The purpose of this skill is to let AI read code and requirements, write structured Apifox/OpenAPI JSON specs, validate them locally, dry-run the CLI command, and then apply them to Apifox.

## Capability Boundaries

Use the canonical command surface in new work:

- Endpoint writes: `api create`, `api update`, `api upsert`
- Schema writes: `schema create`, `schema update`
- Batch writes: `apply-docs`, `generate-crud`
- Discovery/audit: `api`, `schema`, `tag`, `folder`, `audit`, `versions`, `request`

Treat `create-endpoint`, `update-endpoint`, and `upsert-endpoint` as legacy aliases only. Do not use them in new instructions or scripts.

Current write boundaries:

- Supported writes: create/update/upsert endpoints, create/update schemas, generate CRUD endpoint docs, import OpenAPI/Postman, replace endpoint tags.
- Not supported as direct writes: delete endpoint, delete schema, create/delete folder. Those commands explain the limitation instead of mutating Apifox. Prefer tags for folder-like organization.

`api upsert` imports a generated OpenAPI operation with overwrite behavior. Treat it as replacing the documented operation, not as a field-level patch.

## Machine Contract

Every command and subcommand should answer `--help` without requiring credentials, files, or network access:

```bash
apifox-cli validate-endpoint --help
apifox-cli api upsert --help
apifox-cli apply-docs --help
```

For JSON-file inputs, pass `--file -` to read stdin:

```bash
apifox-cli docs-template | apifox-cli validate-docs --file -
```

Validation commands support machine-readable output:

```bash
apifox-cli validate-endpoint --file .apifox-endpoint.json --json
```

The validation JSON shape is:

```json
{"valid": false, "errors": ["field is required"]}
```

Invalid validation exits with code `1`. CLI usage errors exit with code `2`. Do not continue after either failure unless you have fixed the input.

Mutating commands support `--dry-run` and `--print-payload`. For `apply-docs --dry-run`, inspect the printed `operations` array before writing. Real `apply-docs` stops at the first failed operation by default; with `--json`, it prints summary counts and per-operation results. Use `--continue-on-error` only when the user explicitly wants a full failure inventory.

Write commands such as `api upsert --json`, `schema create --json`, and `generate-crud --json` return structured fields including `kind`, `action`, identity fields, `created`, `updated`, `counters`, and `import_result`. Use those fields for scripts instead of parsing human-readable success text.

Discovery and audit commands support structured `--json` output. `api`, `schema`, `tag`, `folder`, and `audit` return typed fields such as `endpoints`, `schemas`, `tags`, `valid`, `problems`, and `issues`. Simple status commands may still wrap text as `{"result": "..."}`; `request --json` returns the raw Apifox JSON result.

## Setup

Resolve the command before doing work:

```bash
apifox-cli --help
```

When the binary is not installed but this repository is checked out:

```bash
go run ./cmd/apifox-cli --help
```

Verify credentials and project connectivity:

```bash
apifox-cli config check
```

Require `APIFOX_TOKEN` and `APIFOX_PROJECT_ID`, or pass `--token` and `--project-id` before the subcommand. Keep credentials in environment variables, not JSON files.

For multi-field AI-generated inputs, write hidden JSON files such as `.apifox-docs.json`, `.apifox-endpoint.json`, `.apifox-crud.json`, `.apifox-schema.json`, or `.apifox-request.json`.

## Reusable Local Artifacts

When the target project contains `scripts/generate_apifox_docs.py`, treat it as the reusable generator for rebuilding Apifox docs from routes and DTOs. Do not hand-edit the generated `.apifox-docs.json` as the source of truth unless the generator is missing or wrong.

Local reusable outputs:

- `scripts/generate_apifox_docs.py`: regenerates specs from routes and DTOs.
- `.apifox-docs.json`: validated batch docs output. Keep it hidden and gitignored unless the user explicitly asks to commit it.

After code changes, regenerate and validate:

```bash
python3 scripts/generate_apifox_docs.py
apifox-cli validate-docs --file .apifox-docs.json
```

Before a real write, run a dry-run preview, then apply with credentials:

```bash
apifox-cli apply-docs --file .apifox-docs.json --dry-run
APIFOX_TOKEN=... APIFOX_PROJECT_ID=8555669 apifox-cli apply-docs --file .apifox-docs.json
```

For broad updates, write in batches of about 15 operations to reduce the chance of Apifox returning 403:

```bash
apifox-cli apply-docs --file .apifox-docs.json --batch-size 15 --dry-run
APIFOX_TOKEN=... APIFOX_PROJECT_ID=8555669 apifox-cli apply-docs --file .apifox-docs.json --offset 0 --limit 15
APIFOX_TOKEN=... APIFOX_PROJECT_ID=8555669 apifox-cli apply-docs --file .apifox-docs.json --offset 15 --limit 15
```

If 403 recurs, stop, keep the generated file for inspection, and report the exact CLI output instead of retrying blindly.

## Main Workflow

For Go projects, read routes, handlers, DTOs, validation code, and product requirements. Then write structured specs and send them through the CLI.

Batch endpoint docs:

```bash
apifox-cli docs-template -o .apifox-docs.json
apifox-cli validate-docs --file .apifox-docs.json
apifox-cli apply-docs --file .apifox-docs.json --dry-run
apifox-cli apply-docs --file .apifox-docs.json
```

Use `.apifox-docs.json` when documenting more than one endpoint or a resource family.

- `endpoints`: endpoint specs, each with optional `action`: `upsert`, `create`, or `update`. Prefer `upsert` for AI documentation sync.
- `crud`: CRUD resource specs passed to `generate-crud`.

Single endpoint:

```bash
apifox-cli endpoint-template --method POST -o .apifox-endpoint.json
apifox-cli validate-endpoint --file .apifox-endpoint.json
apifox-cli api upsert --file .apifox-endpoint.json --dry-run
apifox-cli api upsert --file .apifox-endpoint.json
```

Use `api create` only when the endpoint must be new. Use `api update` when the endpoint should already exist. Use `api upsert` for normal AI sync.

CRUD:

```bash
apifox-cli crud-template -o .apifox-crud.json
apifox-cli validate-crud --file .apifox-crud.json
apifox-cli generate-crud --file .apifox-crud.json --dry-run
apifox-cli generate-crud --file .apifox-crud.json
```

Schema:

```bash
apifox-cli schema template -o .apifox-schema.json
apifox-cli schema create --file .apifox-schema.json --dry-run
apifox-cli schema create --file .apifox-schema.json
apifox-cli schema update --file .apifox-schema.json --dry-run
```

Always validate before writing to Apifox, and always run `--dry-run` before the first real write.

## Discovery

Use CLI subcommands to inspect the target Apifox project:

```bash
apifox-cli api list --limit 20
apifox-cli api get --method GET --path /orders
apifox-cli schema list --limit 20
apifox-cli schema get Order
apifox-cli tag list
apifox-cli tag apis --tag 订单管理
apifox-cli folder list
apifox-cli versions
```

Use raw `/v1` only for official Apifox endpoints that are not wrapped yet:

```bash
apifox-cli request GET /versions --json
apifox-cli request POST /projects/123/export-openapi --data-file .apifox-request.json --dry-run
```

## Import And Export

Use import/export for migration, backup, or compatibility work. Do not make it the primary AI documentation workflow.

```bash
apifox-cli export-openapi --format JSON --oas-version 3.1 -o .apifox-openapi.json
apifox-cli export-openapi --scope tags --tag 订单管理 --format YAML -o .apifox-orders.yaml
apifox-cli import-openapi --file .apifox-openapi.json --endpoint-overwrite-behavior AUTO_MERGE
apifox-cli import-postman --file .postman-collection.json
```

Before mutating Apifox through import commands:

```bash
apifox-cli import-openapi --file .apifox-openapi.json --print-payload
apifox-cli import-postman --file .postman-collection.json --dry-run
```

Choose overwrite behavior deliberately: `OVERWRITE_EXISTING`, `AUTO_MERGE`, `KEEP_EXISTING`, or `CREATE_NEW`.

## API Definition Rules

When creating or updating endpoints:

- Use Chinese business names for `title`; do not use method/path strings or role prefixes.
- Keep `description` as business context and metadata, not request/response examples.
- Put JSON Schema in `response_schema` or `request_body_schema`.
- Include `description` on every schema field and parameter.
- Use real example values; do not use placeholders like `"string"`.
- Let the CLI add standard error responses unless custom `responses` are required.

Example endpoint file:

```json
{
  "title": "创建订单",
  "path": "/orders",
  "method": "POST",
  "description": "创建新订单，需要用户已登录",
  "tags": ["订单管理"],
  "request_body_schema": {
    "type": "object",
    "properties": {
      "item_id": {"type": "integer", "description": "商品ID"},
      "quantity": {"type": "integer", "description": "购买数量"}
    },
    "required": ["item_id", "quantity"]
  },
  "request_body_example": {"item_id": 1001, "quantity": 2},
  "response_schema": {
    "type": "object",
    "properties": {
      "order_id": {"type": "integer", "description": "订单ID"},
      "status": {"type": "string", "description": "订单状态"}
    },
    "required": ["order_id", "status"]
  },
  "response_example": {"order_id": 90001, "status": "pending"}
}
```

## Audit And Repair

Run audits before broad edits and after endpoint changes:

```bash
apifox-cli audit all-responses
apifox-cli audit responses --method POST --path /orders
apifox-cli audit path-naming --style kebab-case
apifox-cli audit consistency
```

If a command fails, report the exact CLI output. Gather more context with `api list/get`, `schema list/get`, `tag list`, or audits before retrying. Do not hide failures behind local assumptions.
