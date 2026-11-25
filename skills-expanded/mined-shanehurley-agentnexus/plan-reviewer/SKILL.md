---
name: plan-reviewer
description: "Delegate-only \u2014 Daily Coder `plan_reviewer`. Adversarially try to disprove plan completeness and executability. Invoked from `daily-coder` / `use-master` / runtime only; not a picker entry."
disable-model-invocation: true
user-invocable: false
metadata:
  source: "AgentNexus/agents/ide/canonical"
  authority: "read-only"
  readonly: true
  delegate_only: true
---
# plan-reviewer

> Imported from the AgentNexus IDE agent pack (`agents/ide/canonical/plan-reviewer.md`).
> That file is the edit source; regenerate this skill rather than editing it here.
# Daily Coder role: plan_reviewer

## ROLE

**Delegate only** from `daily-coder`, `use-master`, or Daily Coder runtime.

Runtime job: Adversarially try to disprove plan completeness and executability.

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

Summary: Adversarially try to disprove plan completeness and executability.

When **this agent** is invoked, read the full runtime instructions from SSOT (not at picker/resident load):

`load-on-invoke:daily-coder-ecosystem/agents/plan_reviewer/prompt.md` (sha256 `b90e1761758b41a7c718b5555d36f03be5b2b52bc41874123a89f66e010f8cc9`)

## Projection SSOT

| Field | Value |
|-------|-------|
| Agent directory | `daily-coder-ecosystem/agents/plan_reviewer` |
| `prompt.md` sha256 | `b90e1761758b41a7c718b5555d36f03be5b2b52bc41874123a89f66e010f8cc9` |
| `agent.json` sha256 | `36293df6f16cfe4017260e2dc46b7e4662aa9e665c5f9a60d50290893e2539f2` |
| Regenerate | `python /Users/shurley/Documents/AgentNexus/agents/ide/scripts/import_daily_coder_agents.py` |

## Tool intent (runtime allowlist reference)

Configured DC tools (prompt cannot grant tools): filesystem.read, filesystem.search, repository.diff.

Output schema: `review`.

## Examples

- **Good:** Parent passes bounded context; role emits schema-shaped JSON with tagged claims only.
- **Anti-pattern:** Chat claims COMPLETE or SIMULATED without `ide-bridge` / runtime acceptance.
