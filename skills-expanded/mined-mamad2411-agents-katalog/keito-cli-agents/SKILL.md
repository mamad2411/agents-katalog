# AGENTS.md

Guidance for coding agents working in `keito-cli`.

## Product Context

`keito-cli` is a Rust CLI for humans and AI agents to track billable time against the Keito platform. The product goal is an agent-native interface: deterministic commands, no prompts during normal use, structured JSON output, stable exit codes, and self-documenting help/man pages.

Primary docs to read before changing behavior:

- `docs/keito-cli-prd.md` - product requirements and target command surface.
- `docs/agent-guide.md` - expected agent usage workflow.
- `README.md` - public user-facing contract.
- `man/*.1` - generated man pages from clap definitions.

## Repo Shape

- `src/main.rs` - binary entrypoint and top-level error handling.
- `src/cli/` - clap command/flag definitions and help text.
- `src/commands/` - command handlers.
- `src/api/` - Keito REST client, models, and HTTP error mapping.
- `src/config/` - config file and credential resolution.
- `src/output/` - table and JSON rendering.
- `src/types.rs` - duration parsing, duration formatting, name/ID resolution.
- `src/bin/gen-man.rs` - man-page generation.
- `tests/` - integration and mocked API tests.

## Common Commands

Because the crate has two binaries, use `--bin keito` for local CLI runs.

```sh
cargo test --all-targets
cargo run --bin keito -- --help
cargo run --bin keito -- time start --help
cargo run --bin gen-man
man ./man/keito.1
```

Regenerate `man/*.1` after changing any clap help text, flags, subcommands, version, or command descriptions.

## Production API Contract

Validate CLI behavior against the production app repo at:

`/Users/sionsmith/development/oso/com.github.osodevops/keito`

Key production API references:

- `src/app/api/v2/time_entries/route.ts`
- `src/app/api/v2/time_entries/[id]/route.ts`
- `src/app/api/v2/projects/route.ts`
- `src/app/api/v2/tasks/route.ts`
- `src/app/api/v2/users/me/route.ts`
- `src/lib/api-v2-transformers.ts`
- `src/lib/api-v2-response.ts`
- `docs/openapi-v2.yaml`

The live API base is `https://app.keito.ai`. Do not assume `https://app.keito.io` is valid; as of 2026-05-04 it fails TLS from this environment. Unauthenticated probes that are safe and useful:

```sh
curl -i https://app.keito.ai/api/health
curl -i https://app.keito.ai/api/v2/users/me
curl -i https://app.keito.ai/api/v2/projects
```

Expected v2 auth headers:

- `Authorization: Bearer <api-key>`
- `Keito-Account-Id: <company-id>`

Current production response envelopes use entity-specific keys:

- `GET /api/v2/projects` returns `projects`, not `data`.
- `GET /api/v2/tasks` returns `tasks`, not `data`.
- `GET /api/v2/time_entries` returns `time_entries`, not `data`.

Current production time-entry fields use Harvest-style snake case:

- Create requires `project_id`, `task_id`, and `spent_date`.
- Billable is `billable`, not `is_billable`.
- Responses include nested `project` and `task` objects, not `project_name` and `task_name`.
- `source` accepts `web`, `cli`, `api`, or `agent`.
- `metadata` must be a JSON object and is limited to 4KB.

## Production Validation

The current CLI has been updated for the production v2 auth/projects/tasks/time-entry list/create/stop response shapes. A live production smoke test on 2026-05-05 verified:

- `keito auth status` and `keito auth whoami` against `https://app.keito.ai`.
- `keito projects list`, `keito projects show`, and `keito projects tasks`.
- `keito time start`, `keito time running`, duplicate-start conflict handling, `keito time stop`, `keito time stop --discard`, no-running stop handling, `keito time log`, and `keito time list`.

Remaining product gaps:

- Time entries default to `source=cli`; agent metadata flags, source selection, auto-detection, offline queue, sync, reports, clients, config commands, completions, and time edit/delete are PRD items that are not implemented in the CLI yet.

When fixing production compatibility, update both the Rust models/client and the mock tests so tests assert the real production envelope and field names.

## Implementation Guidelines

- Preserve the agent-native contract: no interactive prompts except explicit setup commands such as `auth login`.
- Every command that can be used by agents must support `--json` and deterministic exit codes.
- Keep human table output useful, but treat JSON as the stable integration surface.
- Prefer exact, explicit errors with recovery suggestions over fuzzy interactive behavior.
- Do not log or print API keys.
- Do not commit local credentials, generated config, or real production responses containing customer data.
- Leave unrelated dirty files alone. There may be user changes in sibling repos.
