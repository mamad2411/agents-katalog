---
name: twingate-api
description: >
  Twingate GraphQL API, CLI tools, and automation. Load when the user wants to
  automate Twingate via the API, write scripts against the GraphQL endpoint,
  generate or manage API tokens, use the Twingate CLI tools, or build automation
  pipelines. Also trigger on 'GraphQL', 'X-API-KEY', 'Twingate API', 'api/graphql',
  'service account key', 'connector token provisioning', 'rate limiting', or any
  Twingate admin API mention. Also activate for: AWS tag-driven resource automation
  (EC2/ECS/RDS tag sync, Lambda, EventBridge/CloudWatch Events), a web UI for the
  Twingate CLI (tgcli-web, FastAPI, Docker/Kubernetes), the Twingate GitHub Action for
  CI runners, Jupyter/Python API tutorials, or generating a network health/insights
  report from a Network Events export.
---

## Role

This skill owns Twingate's GraphQL API, service account key management, CLI tooling, and API-driven automation. It covers scripting, CI/CD pipeline integration, pagination, rate limiting, token permissioning, and the programmatic path for connector and service account credential provisioning. It does not replace IaC — use it for scripting and automation, not for managing long-lived Twingate objects that need lifecycle tracking.

## Decisions & Guidelines

- **Always check `ok` before reading `entity` in a mutation response.** A mutation can return HTTP 200 with `ok: false` and `entity: null`. Reading entity fields without checking `ok` first causes null reference errors or silent data corruption. Check `error.errorCode` and `error.message` on failure.
- **Always paginate — never assume all results fit in one page.** Scripts that omit pagination silently miss records with no error. You may get 50 of 500 resources. Loop on `pageInfo.hasNextPage` until `false`, passing `pageInfo.endCursor` as the `after` argument on each request.
- **Never parse, decode, or construct IDs.** Twingate IDs are opaque base64-encoded NodeIDs. Use them only as returned by the API. Never infer numeric components from base64 decoding.
- **Issue the least-privileged token for the task.** Read for monitoring/reporting. Write for provisioning. Provision only for `connectorGenerateTokens` and service account key generation. Never issue Provision-level tokens to read-only scripts.
- **`connectorGenerateTokens` rotates credentials on an existing Connector.** Calling it again on a deployed Connector invalidates the current tokens and the Connector stops working until restarted with the new tokens. Only call this when reprovisioning credentials — never as a "refresh" operation.
- **Prefer Terraform or Pulumi over raw GraphQL for persistent configuration management.** The API is the right tool for scripting, automation, and reporting. IaC is better for long-lived Twingate objects that need lifecycle tracking and drift detection.
- **Implement 429 retry with `Retry-After` backoff from the start, not as an afterthought.** The API enforces per-minute rate limits. Scripts that ignore 429 fail mid-run on large operations. The Terraform and Pulumi providers handle this automatically — raw scripts must not ignore it.
- **Service account keys expire — build rotation logic into any pipeline that uses them.** Monitor `expiresAt` and rotate before expiry. Reactive rotation on failure disrupts pipelines.
- **There are two unrelated tools both called "the Twingate CLI" — do not conflate them.** `Twingate-Labs/tg-cli` (Deno/TypeScript; export/import, topology diagrams) and `Twingate-Labs/Twingate-CLI` (Python, installed as `tgcli`; full CRUD, multi-tenant sessions) are separate projects with different flags and no shared history. Confirm which one the user means before giving command syntax. Flag repos like `gh-twingate-solutions-general-scripts.md` as LLM-assisted reference examples, not supported products, before recommending them for production use.

## Search References First

**Grep `references/` with the user's own keywords before answering, and cite what you
find.** Filenames reveal only the topic — tool names, vendor names, and exact flag/env-var
names live in the file bodies, so a filename scan alone will miss them:

```
grep -ril "cloudwatch" references/     # -> gh-twingate-labs-tg-aws-tag-sync.md
grep -ril "graphviz" references/       # -> gh-twingate-labs-tg-cli.md
grep -ril "jupyter" references/        # -> gh-twingate-labs-twingate-api-intro-with-python.md, gh-twingate-solutions-health-report-generator.md
```

**Before writing any API code or answering questions involving any of the following,
read `references/graphql-schema-reference.md` first** — this is the authoritative type
and field reference and must be consulted for every non-trivial query or mutation:

- Exact query/mutation names, argument names, or argument types
- Field names on response objects (including nested fields and pagination structures)
- Enum values for any field (e.g., resource protocol enums, address-type enums)
- Input type structure for create/update mutations
- Whether a given field exists, is nullable, or is deprecated

For **CLI tooling** (Python `tgcli`, Deno `tg-cli`, `tgcli-web`, OpenClaw), read the
corresponding CLI reference before suggesting commands — flag names and subcommand
structure differ between tools, and two of them share almost the same name.

Do not answer schema or CLI questions from training-data memory — the schema evolves
and CLI tools have version-specific syntax. If the user asks whether tooling exists for
an automation task (AWS tag sync, health reporting, CI runner access), **search before
saying no.**

## Routing

**Co-activate, don't either/or.** The pointers below are *additive*: for a cross-cutting
prompt, load and grep the named skills' `references/` *in addition to* this one — never stop
at the first skill that matched. Grep a sibling's references with the user's own keywords
first; load it fully when the grep hits. Twingate answers are routinely split across skills,
so err toward consulting more, not fewer. Common cross-cutting clusters here: automating a
given object → also that object's skill (**connectors** / **identity** / **architect**);
persistent lifecycle management → **terraform**/**pulumi**.

- **→ twingate-terraform / twingate-pulumi**: when the user wants persistent IaC management rather than API scripting — IaC provides drift detection, audit trail, and lifecycle management that raw API scripts do not
- **→ twingate-architect**: for understanding what resources, remote networks, groups, and connectors are before writing API automation against them
- **→ twingate-connectors**: for `connectorGenerateTokens` context — token provisioning is an API operation, but the Connector deployment specifics (runtime env vars, restart behavior) live in twingate-connectors

## References

See [`references/`](./references/) for the current corpus, refreshed weekly. Two kinds
of file live there, plus one hand-maintained authoritative reference:

- **`graphql-schema-reference.md`** — the static GraphQL SDL, hand-maintained and
  authoritative. Never auto-regenerated.
- **`{slug}.md`** — summaries of `twingate.com/docs` pages (product documentation).
- **`gh-{org}-{repo}.md`** — summaries of public Twingate GitHub repos: official
  tooling, SE automation, and community integrations.

| If the user asks about… | Read first |
|---|---|
| Query/mutation signatures, field names, enum values, input types | `graphql-schema-reference.md` (authoritative) |
| API overview, authentication, getting started | `api-overview.md`, `api.md`, `getting-started-with-the-api.md` |
| Exploring the API, sample queries | `exploring-the-apis.md` |
| Python CLI docs page (`tg-cli`) | `introduction-to-the-python-cli.md` |
| JavaScript CLI docs page (`tg-cli`) | `introduction-to-tg-cli-javascript.md` |
| OpenClaw automation tool (general, Docker Compose, DigitalOcean) | `openclaw.md`, `openclaw-docker-compose.md`, `openclaw-digitalocean.md` |
| CI/CD pipeline patterns (docs page) | `example-cicd-configurations.md` |
| **GitHub Action for CI runners** — installs the Client on a runner via a Service Key so workflow steps can reach IP-restricted/private resources | `gh-twingate-github-action.md` |
| **AWS tag-driven resource automation** (`tg_resource`/`tg_groups` tags on EC2, ECS, RDS → Lambda creates/deletes Twingate resources via EventBridge/CloudWatch Events) | `gh-twingate-labs-tg-aws-tag-sync.md` |
| **Deno/TypeScript admin CLI** (`tg-cli`) — topology export to Excel/PNG (GraphViz), group/network/resource import | `gh-twingate-labs-tg-cli.md` |
| **Browser web UI for the Python CLI** (`tgcli-web`) — FastAPI app wrapping the `tgcli` library; entity browsing, export/import with diff review, health dashboards, Docker/K8s/pip install | `gh-twingate-labs-tgcli-web-py.md` |
| **Beginner Jupyter/Python tutorial** for the GraphQL API — queries, mutations, introspection, no prior GraphQL knowledge assumed | `gh-twingate-labs-twingate-api-intro-with-python.md` |
| **Python admin CLI** (`tgcli`, Typer-based) — full CRUD on remote networks/resources/connectors/groups/users/service accounts, multi-tenant sessions, Synced→Manual group migration | `gh-twingate-labs-twingate-cli.md` |
| **General operational scripts** (client deployment, Intune/Autopilot, gateway-as-DNS-server, Network Events CSV filtering, bulk group removal) — **LLM-assisted reference examples, not a supported product** | `gh-twingate-solutions-general-scripts.md` |
| **Network health/insights report generator** — Jupyter notebook that turns a Network Events export into resource/user/connector/remote-network health analysis | `gh-twingate-solutions-health-report-generator.md` |

This table is a fast path, not the whole corpus — when a question doesn't match a row,
grep `references/` before answering. **Default to checking the schema** — never write
a query or mutation from memory; field names and enum values change.
