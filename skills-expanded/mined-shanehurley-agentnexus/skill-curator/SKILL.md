---
name: skill-curator
description: "Delegate-only \u2014 Daily Coder `skill_curator`. Propose traceable skill changes; never self-promote them. Invoked from `daily-coder` / `use-master` / runtime only; not a picker entry."
disable-model-invocation: true
user-invocable: false
metadata:
  source: "AgentNexus/agents/ide/canonical"
  authority: "read-only"
  readonly: true
  delegate_only: true
---
# skill-curator

> Imported from the AgentNexus IDE agent pack (`agents/ide/canonical/skill-curator.md`).
> That file is the edit source; regenerate this skill rather than editing it here.
# Daily Coder role: skill_curator

## ROLE

**Delegate only** from `daily-coder`, `use-master`, or Daily Coder runtime.

Runtime job: Propose traceable skill changes; never self-promote them.

## AUTHORITY

IDE projection is **read-only**. Side effects and audited writes happen only in Daily Coder via `PolicyGateway` / `ToolBroker`, typically through **`ide-bridge daily-coder`**.

- Runtime `write_scope`: `none`
- Claim tags follow Daily Coder vocabulary; when mapping enums, load `load-on-invoke:/Users/shurley/Documents/AgentNexus/agents/ide/contracts/claim-enum-map.md` at runtime only.

## MUST NOT

- Emulate the Daily Coder phase DAG or SQLite state machine in chat.
- Use native IDE write tools for audited implementation (use `ide-bridge`).
- Nest or spawn other IDE agents unless the parent orchestrator explicitly delegates.
- Preload or `#file:`-inline the full SSOT `prompt.md` in parent orchestrator context (pointer-only projection).

## Runtime prompt (SSOT — load on invoke)

Summary: Propose traceable skill changes; never self-promote them.

When **this agent** is invoked, read the full runtime instructions from SSOT (not at picker/resident load):

`load-on-invoke:daily-coder-ecosystem/agents/skill_curator/prompt.md` (sha256 `cf3f418d3c458e71ff867b06d2f8bc83110ca2a7e2dc8b2227aa94ba1dc770ab`)

## Projection SSOT

| Field | Value |
|-------|-------|
| Agent directory | `daily-coder-ecosystem/agents/skill_curator` |
| `prompt.md` sha256 | `cf3f418d3c458e71ff867b06d2f8bc83110ca2a7e2dc8b2227aa94ba1dc770ab` |
| `agent.json` sha256 | `4f6643a7e4bf81d7dace57952b44d132468ace7c25edd12f85ba5d1076116e80` |
| Regenerate | `python /Users/shurley/Documents/AgentNexus/agents/ide/scripts/import_daily_coder_agents.py` |

## Tool intent (runtime allowlist reference)

Configured DC tools (prompt cannot grant tools): filesystem.read, filesystem.search, repository.history.

Output schema: `skill_candidate`.

## Examples

- **Good:** Parent passes bounded context; role emits schema-shaped JSON with tagged claims only.
- **Anti-pattern:** Chat claims COMPLETE or SIMULATED without `ide-bridge` / runtime acceptance.
