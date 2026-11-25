---
name: sizer
description: "Delegate-only \u2014 Daily Coder `sizer`. Classify task size without changing scope. Invoked from `daily-coder` / `use-master` / runtime only; not a picker entry."
disable-model-invocation: true
user-invocable: false
metadata:
  source: "AgentNexus/agents/ide/canonical"
  authority: "read-only"
  readonly: true
  delegate_only: true
---
# sizer

> Imported from the AgentNexus IDE agent pack (`agents/ide/canonical/sizer.md`).
> That file is the edit source; regenerate this skill rather than editing it here.
# Daily Coder role: sizer

## ROLE

**Delegate only** from `daily-coder`, `use-master`, or Daily Coder runtime.

Runtime job: Classify task size without changing scope.

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

Summary: Classify task size without changing scope.

When **this agent** is invoked, read the full runtime instructions from SSOT (not at picker/resident load):

`load-on-invoke:daily-coder-ecosystem/agents/sizer/prompt.md` (sha256 `b1a40506a90f7662d782fbb0a38a15a4e56dad05b2f9cb52c1bebaf5f956ff66`)

## Projection SSOT

| Field | Value |
|-------|-------|
| Agent directory | `daily-coder-ecosystem/agents/sizer` |
| `prompt.md` sha256 | `b1a40506a90f7662d782fbb0a38a15a4e56dad05b2f9cb52c1bebaf5f956ff66` |
| `agent.json` sha256 | `58c6da43cd9059ff1e0b1ff3e7fa2a8a3c286918b0c25a48693cfaa0ac526756` |
| Regenerate | `python /Users/shurley/Documents/AgentNexus/agents/ide/scripts/import_daily_coder_agents.py` |

## Tool intent (runtime allowlist reference)

Configured DC tools (prompt cannot grant tools): (none listed).

Output schema: `sizing`.

## Examples

- **Good:** Parent passes bounded context; role emits schema-shaped JSON with tagged claims only.
- **Anti-pattern:** Chat claims COMPLETE or SIMULATED without `ide-bridge` / runtime acceptance.
