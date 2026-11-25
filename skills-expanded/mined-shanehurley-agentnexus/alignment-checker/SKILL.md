---
name: alignment-checker
description: "Delegate-only \u2014 Daily Coder `alignment_checker`. Reject outputs that do not serve the original request. Invoked from `daily-coder` / `use-master` / runtime only; not a picker entry."
disable-model-invocation: true
user-invocable: false
metadata:
  source: "AgentNexus/agents/ide/canonical"
  authority: "read-only"
  readonly: true
  delegate_only: true
---
# alignment-checker

> Imported from the AgentNexus IDE agent pack (`agents/ide/canonical/alignment-checker.md`).
> That file is the edit source; regenerate this skill rather than editing it here.
# Daily Coder role: alignment_checker

## ROLE

**Delegate only** from `daily-coder`, `use-master`, or Daily Coder runtime.

Runtime job: Reject outputs that do not serve the original request.

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

Summary: Reject outputs that do not serve the original request.

When **this agent** is invoked, read the full runtime instructions from SSOT (not at picker/resident load):

`load-on-invoke:daily-coder-ecosystem/agents/alignment_checker/prompt.md` (sha256 `51aa5ad14b343ca75675a88f2d9b7d4edc63de37aa6bc67112b4c3c7112d9822`)

## Projection SSOT

| Field | Value |
|-------|-------|
| Agent directory | `daily-coder-ecosystem/agents/alignment_checker` |
| `prompt.md` sha256 | `51aa5ad14b343ca75675a88f2d9b7d4edc63de37aa6bc67112b4c3c7112d9822` |
| `agent.json` sha256 | `0684a85fd7eae0ce18ceee678778d6327ac264aa24b7bd8b860e60a4b052ac6d` |
| Regenerate | `python /Users/shurley/Documents/AgentNexus/agents/ide/scripts/import_daily_coder_agents.py` |

## Tool intent (runtime allowlist reference)

Configured DC tools (prompt cannot grant tools): filesystem.read, repository.diff, repository.status.

Output schema: `alignment`.

## Examples

- **Good:** Parent passes bounded context; role emits schema-shaped JSON with tagged claims only.
- **Anti-pattern:** Chat claims COMPLETE or SIMULATED without `ide-bridge` / runtime acceptance.
