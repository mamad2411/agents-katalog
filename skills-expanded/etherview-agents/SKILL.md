# Etherview Repository Instructions

## Before editing

Read [PLAN.md](PLAN.md), the owning [child plan](docs/plans/index.md), the
[development guide](docs/development.md), relevant [architecture](docs/architecture/overview.md)
sections and [accepted ADRs](docs/decisions/index.md), and the applicable
[testing rules](docs/testing.md). Accepted ADRs are mandatory even when omitted
here; update or add one when its decision changes.

The development guide owns detailed workflow and boundary routing. The current
[Makefile](Makefile) and testing guide own commands; historical plan evidence
must not revive removed targets. Operator procedures belong in the
[runbook](docs/operations.md), task status and evidence in plans.

## Workflow

- Review and preserve staged, unstaged, and untracked work. Claim one
  dependency-ready `todo` item as `in_progress` before implementation.
- Deliver implementation, regressions, acceptance checks, and concise child-plan
  evidence together. Synchronize the root plan when child status changes.
- Never share, delete, or reuse item IDs. Mark abandoned work `dropped` with a
  reason or `superseded` with its replacement; `blocked` names the blocker and
  clearing condition. Long-lived code TODOs cite a plan item.

## Required boundaries

- Target the current fresh-database schema. No compatibility adapters, startup
  backfills, or legacy readiness states unless explicitly requested.
- PostgreSQL is authoritative; Redis, NATS, and object storage are disposable
  accelerators, never the sole copy of correctness data.
- Preserve chain/block identity, canonical and orphan history, endpoint pinning,
  and lease-fenced atomic publication. Never fall back from block hash to height
  or `latest`.
- Keep `serve --roles=all` and split-role components and persistence identical;
  align builders, production manifest, readiness, shutdown, and parity tests.
- Close database snapshots before external calls. Bound hostile input and work;
  return stable typed errors without nested errors, URLs, or credentials.
- Public HTTP contracts start in `api/openapi.yaml`; production SQL starts in
  `internal/db/queries/`. Regenerate outputs, never hand-edit them. Public
  integers beyond JavaScript's safe range are strings.
- Keep secrets server-side and role-scoped, explorer traffic on the generated
  same-origin client, and wallet RPC in the injected-provider allowlist.
- Consult the relevant ADR before changing APIs, persistent contracts, security,
  external services, verifier/proxy provenance, runtime topology, or
  authentication/billing identities; preserve its boundaries.

## Verification

Run targeted regressions, then all applicable gates in [docs/testing.md](docs/testing.md):

- `make generate-check`: OpenAPI, SQL, generated-client, or embedded SPA changes.
- `make source-check`: database execution-boundary changes.
- `make docs-check`: maintained docs or executable deployment/runtime surfaces.
- `make plan-check`: plan, ADR-link, or governance changes.

Follow the testing guide's restricted-host matrix without weakening targets or
acceptance criteria. Mark work `done` only after targeted tests and applicable
gates pass and the child plan records current evidence.

Keep this file limited to repository-wide rules and document routing. Add nested
`AGENTS.md` files only for genuinely different subtree rules.
