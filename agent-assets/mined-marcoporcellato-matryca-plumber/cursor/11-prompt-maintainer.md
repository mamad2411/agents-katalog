---
description: Checklist when touching prompt builders, agent fragments, or MCP tool docstrings
alwaysApply: false
---

# Prompt maintainer checklist (Matryca Plumber)

Load on demand when editing Tier-1 prompts, `docs/openspec/agent/` fragments, or MCP tool contracts.

**Rule routing:** Complements [`06-auto-changelog.mdc`](06-auto-changelog.mdc), [`07-env-example.mdc`](07-env-example.mdc), [`AGENTS.md`](../AGENTS.md).

## Trigger → Azione

| Hai modificato | Devi eseguire |
|----------------|---------------|
| `docs/openspec/agent/*.md` | `make build-system-prompt && make check-system-prompt` |
| `src/agent/**/prompts.py`, `src/graph/**/prompts.py` (builder Tier-1A) | `uv run pytest tests/test_daemon_prompts.py --update-prompt-hashes` → `git add tests/prompt_hash_snapshots.json` |
| `src/agent/**/prompts.py` (builder Tier-1B writer) | Come sopra + verifica che nessuna stringa contenga `English only` |
| `mcp_server.py` (docstrings tool) | Aggiorna `docs/openspec/agent/mcp-tools.md` (+ `tool-reference.md` se serve) → `make build-system-prompt`; alla release MCP sync anche `llms.txt` §2 |
| `tests/prompt_hash_snapshots.json` | Il commit message deve contenere `prompt(<builder>): <motivo>` |

## Non fare

- Non editare `SYSTEM_PROMPT.md` direttamente — è generato (`<!-- GENERATED — do not edit -->`).
- Non aggiungere frammenti `docs/openspec/agent/*.md` senza riga in `_assembly_order.txt` — `make check-system-prompt` fallisce.
- Non aggiungere stringhe system inline in `llm_client.py` — usa un builder di dominio che importa solo `src/agent/prompts/core.py`.
- Non impostare `alwaysApply: true` su nuove rule senza approvazione esplicita.
