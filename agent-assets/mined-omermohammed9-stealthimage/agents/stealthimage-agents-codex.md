# StealthImage — Codex Governance Layer

> Codex-specific execution rules. This file extends the project governance system; it does not replace `.agents/rules/AGENTS.md`.

## Source Of Truth

- `.agents/rules/AGENTS.md` is the project agent source of truth.
- `.agents/project-context.md`, `.agents/system-map.md`, `.agents/workflow.md`, `.agents/AUDIT_REPORT.md`, and `.agents/tasks_status_matrix.md` are the canonical project governance records.
- Codex must follow this file only as an adapter layer for repository behavior, documentation impact checks, and prompt refinement.

## Mandatory Reading

Before every task, read only these governance files unless the task clearly requires more:

- `.agents/rules/AGENTS.md`
- `.agents/workflow.md`
- `.agents/project-context.md`
- `.agents/system-map.md`
- `.agents/tasks_status_matrix.md`

For implementation tasks, also read:

- `.agents/rules/code-standards.md`
- `.agents/rules/strict-resource-management.md`

For task completion or documentation-impact checks, also read:

- `.agents/AUDIT_REPORT.md`
- `.codex/project-governor.md`

If a prompt references root-level `AGENTS.md`, `workflow.md`, `project-context.md`, `system-map.md`, `tasks_status_matrix.md`, or `AUDIT_REPORT.md`, first check whether those files exist. In this checkout, the canonical files live under `.agents/` and `.agents/rules/`; use those paths unless root-level files are later added.

## Model And Prompt Routing

Codex tasks must choose the lowest sufficient available model before any implementation or execution. In this repository, use these required selections unless the Codex UI/runtime exposes a newer exact model name:

| Task Complexity | Required Codex Selection | Use For | Quota Rule |
|---|---|---|---|
| Tiny / mechanical | `GPT-5 Codex` with **low reasoning** | typos, markdown cleanup, small config/doc updates, prompt-template wording, single obvious test/docs edits | Default for docs-only work |
| Standard | `GPT-5 Codex` with **medium reasoning** | normal bug fixes, single-file logic, route/test updates, small dashboard changes, governance sync | Default for implementation work |
| Complex | `GPT-5 Codex` with **high reasoning** | 3+ entangled files, DB + route + dashboard contract changes, telemetry/GeoIP/auth architecture changes, difficult root-cause debugging | Must justify in one sentence before use |
| Critical / security-sensitive | `GPT-5 Codex` with **high reasoning** and explicit plan | crypto, HMAC/auth redesign, privacy/telemetry contract changes, destructive migration planning | Requires explicit risk note before execution |

Rules:

- Do **not** request or claim `GPT-5.5`, `GPT-6`, `Claude`, `Gemini`, or any other model unless the current Codex runtime explicitly exposes it.
- If the user recommends an unavailable model, state: `Requested model unavailable in this runtime; using GPT-5 Codex with <low|medium|high> reasoning because <reason>.`
- Before implementation, state the selected model tier and why it is sufficient.
- Escalate from low/medium to high only for concrete multi-file reasoning, security-sensitive algorithm design, or cross-contract debugging.
- Downgrade back to low reasoning for summaries, documentation cleanup, formatting, and final reports.

## Project Understanding Summary

### Architecture

StealthImage is an internal authorized cybersecurity engineering project for web-beacon research, diagnostics, telemetry, validation, testing, and observability. The current architecture is a Flask C2 server that serves image tracking routes, collects browser-exposed telemetry, stores events in SQLite and JSONL, enriches public IPs with GeoIP data, and renders a dashboard from static assets. The image bytes remain benign; the server-side route and client-side browser telemetry flow are the active system path.

### Workflow

Every session starts with governance reads, active phase/task identification, scope declaration, minimal implementation, verification, and documentation synchronization. Tasks that touch three or more files require a short implementation plan before coding. Cross-scope changes require architect coordination, and completion is blocked until documentation gates pass.

### Documentation Synchronization

Implementation changes can make `.agents/system-map.md`, `.agents/project-context.md`, `.agents/workflow.md`, `.agents/AUDIT_REPORT.md`, `.agents/tasks_status_matrix.md`, and `README.md` stale. New files, route changes, dependency changes, API changes, config changes, phase changes, telemetry changes, GeoIP changes, dashboard changes, and architecture changes require documentation impact analysis before completion.

### Project Constraints

- Preserve the web-beacon and telemetry architecture.
- Preserve `public_ip` as the server-observed request IP.
- Treat WebRTC, proxy headers, Client Hints, mDNS, VPN, and privacy data as confidence signals, not guaranteed bypasses.
- Keep runtime behavior config-driven through `config.yaml` and environment variables.
- Use `.venv`; never install globally.
- Avoid unnecessary dependencies and unrelated scans.
- Use defensive and engineering language.

### Coding Standards

- Python files require the StealthImage educational header.
- Public functions require type hints and explicit return types.
- Use module-level logging, not production `print()`.
- Keep functions focused, small, and shallow.
- Separate I/O from business logic where practical.
- Use safe YAML loading and no hardcoded secrets.

## Mandatory Files

- `.agents/rules/AGENTS.md`
- `.agents/workflow.md`
- `.agents/project-context.md`
- `.agents/system-map.md`
- `.agents/AUDIT_REPORT.md`
- `.agents/tasks_status_matrix.md`
- `.agents/rules/code-standards.md`
- `.agents/rules/strict-resource-management.md`
- `README.md`
- `config.yaml`
- `requirements.txt`
- `server/exfil_server.py`
- `server/db_repository.py`
- `server/geo_enricher.py`
- `server/offline_geo.py`
- `server/validator.py`
- `server/sse_broker.py`
- `server/static/dashboard.html`
- `tests/test_server.py`
- `.pre-commit-config.yaml`
- `pyproject.toml`

## Protected Files And Contracts

- Do not overwrite or replace `.agents/rules/AGENTS.md`.
- Do not remove or weaken defensive modules named by project governance, including `utils/detection.py` and `extractors/svg_cleaner.py` if present.
- Do not commit or expose `.env`, `.venv/`, `server/collected_data/*.db`, or runtime state artifacts.
- Do not change the PNG marker contract `b"<<<STEGO_HIDDEN_PAYLOAD>>>"` without explicit approval.
- Do not add persistence mechanisms to payload modules.

## Critical Routes

- `GET /` dashboard
- `POST /collect` JSON collection
- `GET /collect?d=...` SVG/base64 fallback
- `GET /track/<filename>` tracking entrypoint
- `GET /image/<filename>` final image serving route
- `POST /api/v1/metrics` browser telemetry endpoint
- `GET /stats`
- `GET /stats/timeline`
- `GET /events`
- `GET /victim/<session_id>`
- `DELETE /victims/<id>`
- `GET /export`
- `GET /export/maltego`
- `GET /health`
- `GET|POST /tasks/<session_id>`
- `POST /auth/login`
- `POST /auth/logout`

## Telemetry Contracts

- Required collection schema includes `session_id`, `timestamp`, and `attack_vector`.
- `public_ip` remains the server-observed request IP.
- WebRTC candidates, candidate summaries, proxy headers, Client Hint analysis, sandbox indicators, and privacy signals live in `env_vars`.
- Candidate attribution is confidence metadata; do not claim guaranteed true-IP recovery.
- Dashboard rendering must support nested telemetry sections and redacted sensitive values.

## GeoIP Contracts

- Offline MaxMind databases are optional operator-provided artifacts.
- `geoip.offline_enabled`, `geoip.city_db_path`, `geoip.country_db_path`, and `geoip.online_fallback_enabled` control behavior.
- Online fallback is bounded and cached.
- Positive and negative GeoIP cache tables must remain consistent.
- Timezone mismatch tags are diagnostic signals, not proof of evasion or bypass.

## Database Contracts

- SQLite is managed through `VictimRepository`.
- `victims.session_id` is unique and uses upsert behavior.
- `env_vars` stores JSON telemetry.
- `geo_cache`, `geo_cache_negative`, and `server_events` support enrichment and observability.
- Export routes depend on stable repository methods, especially `get_recent`, `get_all`, `get_by_session_id`, `get_stats`, `get_timeline`, and `export_maltego_csv`.

## Documentation Obligations

- Update `.agents/system-map.md` when files, dependencies, routes, config keys, contracts, or architecture change.
- Update `.agents/project-context.md` when phase status, constraints, architecture, or design decisions change.
- Update `.agents/workflow.md` when execution process, gates, or cross-module contracts change.
- Review `.agents/AUDIT_REPORT.md` after bug fixes, feature additions, route changes, dashboard changes, GeoIP changes, telemetry changes, or architecture changes.
- Review `.agents/tasks_status_matrix.md` when a phase, feature, or implementation is completed.
- Update `README.md` when user-facing behavior, setup, config, route usage, or exports change.
- Update `.codex/AGENTS.md`, `.codex/project-governor.md`, or `.prompt-template.md` when Codex execution, documentation-impact, or prompt-routing behavior changes.

## Codex Execution Rules

- Never scan unrelated files.
- Root cause before coding.
- Prefer minimal diffs.
- Do not perform unrelated refactors.
- Preserve architecture and contracts.
- Preserve telemetry, GeoIP, database, auth, route, and dashboard contracts.
- Use targeted reads and searches; avoid speculative exploration.
- Update documentation when required.
- Update or propose audit/task matrix changes when required.
- Do not mark work complete until `.codex/project-governor.md` gates pass.

## Completion Gate

Before marking any implementation task complete, Codex must state whether these files were reviewed for staleness:

- `.agents/system-map.md`
- `.agents/project-context.md`
- `.agents/workflow.md`
- `.agents/tasks_status_matrix.md`
- `.agents/AUDIT_REPORT.md`

If affected, Codex must generate the required documentation updates or an explicit update proposal.
