# Tether — AI Agent Map

> If you're an AI agent (Copilot CLI, Codex, Claude Code, Cursor, etc.) operating
> on this repo, start here.

## TL;DR

- **What**: Single-user, local-first FastAPI service for streaming chat completions
  from local model providers with function calling and persistent sessions.
- **Architecture map**: [`docs/architecture.md`](./docs/architecture.md) — start here for the layered overview, request lifecycle, and extension seams.
- **Locked decisions / phase digest**: [`docs/refactor/synthesis-2026-05.md`](./docs/refactor/synthesis-2026-05.md) — invariants, deferrals, in-flight Phase-9 work; never relitigate decisions ratified there.
- **Per-decision detail**: [`docs/adr/`](./docs/adr/) — Architecture Decision Records.

## Operating rules

1. **Pre-refactor reference code is archived**, not in `main`. The old `legacy/` and `llm_service/` directories live on the [`archive/pre-refactor`](https://github.com/Lando-00/Tether/tree/archive/pre-refactor) branch. Reference there if you need to understand pre-refactor behavior; do NOT restore them to `main`.
2. **`src/tether/`** is the canonical package; `tether_service.*` is a deprecation
   alias kept for one release cycle.
3. **Default model provider** is **GenieX**, an external OpenAI-compatible
   server (`geniex serve`) that uses the Hexagon HTP v73 NPU. Tether is only
   its HTTP client and never starts, stops, downloads for, or upgrades GenieX.
   MLC remains available for the Adreno X1 GPU via OpenCL; Ollama is available
   for local/LAN servers; `NexaProvider` is a forward-compatibility stub.
   See [`docs/runbooks/geniex-provider.md`](./docs/runbooks/geniex-provider.md).
4. **GC-disabled in MLC shutdown daemon thread** is **load-bearing**. Don't touch
   `_terminate_bounded` or `daemon_thread_call` without reading
   [`docs/runbooks/shutdown-hang-fix-summary.md`](./docs/runbooks/shutdown-hang-fix-summary.md) first.
5. **Choose Python for the provider**: use a python.org native ARM64 3.12
   stdlib venv for GenieX-only work. The installed x64 Miniconda cannot create
   ARM64 environments. The CodeLinaro MLC wheels require an x64 conda Python
   3.12 environment under Prism. In automation, invoke the selected
   environment's `python.exe` directly; activation does not persist between
   one-shot shells.
6. **No forbidden features**: autonomous reply, plugin SDK, multi-agent routing,
   scheduled jobs, voice, Canvas, push-based notification.

## Conventions enforced by tests/lint

- All settings are typed Pydantic `StrictModel` (extra=forbid, frozen).
- All tools subclass `BaseTool` and use `@tool(name=...)` from `tether.tools.registration`.
- All connectors subclass `Connector` (ABC) and tools they expose carry the
  mandatory `{connector_id}_` prefix.
- All wire-protocol events are typed Pydantic models in
  `tether.protocol.wire.events` (v2 NDJSON: `message_start`, `text_delta`,
  `tool_call`, `tool_result`, `message_stop`).

## Sub-agent prompt templates

If you're delegating work to sub-agents (impl + code-review + rubber-duck pattern), reusable prompt scaffolds live in `.github/agents/`:

- `.github/agents/implementation.agent.md` — impl-agent template
- `.github/agents/code-review.agent.md` — code-review-agent template
- `.github/agents/README.md` — usage guide

## Where things live

| You want… | Look at… |
|---|---|
| Architecture overview + diagrams | [`docs/architecture.md`](./docs/architecture.md) |
| ADRs (locked decisions) | [`docs/adr/`](./docs/adr/) |
| Operational runbooks | [`docs/runbooks/`](./docs/runbooks/) |
| Wire protocol / API specs | [`docs/specs/`](./docs/specs/) (post Phase 8 step 91) |
| Tool implementations | [`src/tether/tools/`](./src/tether/tools/) |
| Connector framework | [`src/tether/connectors/`](./src/tether/connectors/) — connector ABC/registry plus Echo support |
| WhatsApp connector | [`src/tether/connectors/whatsapp/`](./src/tether/connectors/whatsapp/) — neonize adapter and nine `whatsapp_*` tools |
| Provider implementations | [`src/tether/providers/`](./src/tether/providers/) — GenieX, MLC, Ollama, dummy, and Nexa stub |
| Orchestrators | [`src/tether/protocol/orchestration/`](./src/tether/protocol/orchestration/) — chat and research modes |
| Intent classification | [`src/tether/protocol/intent/`](./src/tether/protocol/intent/) — explicit-send confirmation classifiers |
| Runtime supervision | [`src/tether/runtime/`](./src/tether/runtime/) — watchdogs, daemon calls, and task supervision |
| Security | [`src/tether/security/`](./src/tether/security/) — outbound URL safety |
| Configuration loader | [`src/tether/config/`](./src/tether/config/) |
| HTTP entry point | [`src/tether/app/http/api.py`](./src/tether/app/http/api.py) and [`src/tether/app/__main__.py`](./src/tether/app/__main__.py) |
| One-command stack launcher | [`tether.ps1`](./tether.ps1) — see [`docs/runbooks/one-command-launch.md`](./docs/runbooks/one-command-launch.md) |

## Quick commands

```powershell
# Bring up the whole stack (GenieX + server + CLI) in one command
.\tether.ps1
.\tether.ps1 status   # health check;  stop / logs also available
.\tether.ps1 -NoCli   # services only, no CLI

# Run server only
python -m tether.app

# Run tests (default-on markers only)
python -m pytest -q

# Reload editable install after pyproject.toml changes
python -m pip install -e . --no-deps --quiet
```

## Agent skills

### Issue tracker

Issues and specifications live in GitHub Issues for `Lando-00/Tether`. Use the
authenticated `gh` CLI for tracker operations. See
`docs/agents/issue-tracker.md`.

### Triage labels

Use the canonical `needs-triage`, `needs-info`, `ready-for-agent`,
`ready-for-human`, and `wontfix` labels. See `docs/agents/triage-labels.md`.

### Domain docs

This is a single-context repository. Read `CONTEXT.md` and the relevant
decisions under `docs/adr/` before changing domain behaviour. See
`docs/agents/domain.md`.
