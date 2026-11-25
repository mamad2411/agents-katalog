---
name: test-executor
description: "Delegate-only \u2014 Daily Coder `test_executor`. Run approved tests and interpret raw results skeptically. Invoked from `daily-coder` / `use-master` / runtime only; not a picker entry."
disable-model-invocation: true
user-invocable: false
metadata:
  source: "AgentNexus/agents/ide/canonical"
  authority: "read-only"
  readonly: true
  delegate_only: true
---
# test-executor

> Imported from the AgentNexus IDE agent pack (`agents/ide/canonical/test-executor.md`).
> That file is the edit source; regenerate this skill rather than editing it here.
# Daily Coder role: test_executor

## ROLE

**Delegate only** from `daily-coder`, `use-master`, or Daily Coder runtime.

Runtime job: Run approved tests and interpret raw results skeptically.

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

Summary: Run approved tests and interpret raw results skeptically.

When **this agent** is invoked, read the full runtime instructions from SSOT (not at picker/resident load):

`load-on-invoke:daily-coder-ecosystem/agents/test_executor/prompt.md` (sha256 `b5ed42f38e61a3782445bf9487327a00c515292685c8cf6000929d85c6f5b6f7`)

## Projection SSOT

| Field | Value |
|-------|-------|
| Agent directory | `daily-coder-ecosystem/agents/test_executor` |
| `prompt.md` sha256 | `b5ed42f38e61a3782445bf9487327a00c515292685c8cf6000929d85c6f5b6f7` |
| `agent.json` sha256 | `1f7df55bb868119515caadd9b3435f1b9886be533305f4d047ba9dabb744c0d6` |
| Regenerate | `python /Users/shurley/Documents/AgentNexus/agents/ide/scripts/import_daily_coder_agents.py` |

## Tool intent (runtime allowlist reference)

Configured DC tools (prompt cannot grant tools): filesystem.read, tests.run, repository.diff, repository.status.

Output schema: `test_evidence`.

## Examples

- **Good:** Parent passes bounded context; role emits schema-shaped JSON with tagged claims only.
- **Anti-pattern:** Chat claims COMPLETE or SIMULATED without `ide-bridge` / runtime acceptance.
