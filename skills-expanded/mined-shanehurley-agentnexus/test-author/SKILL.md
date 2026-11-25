---
name: test-author
description: "Delegate-only \u2014 Daily Coder `test_author`. Write meaningful tests mapped to acceptance criteria and verify negative controls. Invoked from `daily-coder` / `use-master` / runtime only; not a picker entry."
disable-model-invocation: true
user-invocable: false
metadata:
  source: "AgentNexus/agents/ide/canonical"
  authority: "implementation"
  readonly: true
  delegate_only: true
---
# test-author

> Imported from the AgentNexus IDE agent pack (`agents/ide/canonical/test-author.md`).
> That file is the edit source; regenerate this skill rather than editing it here.
# Daily Coder role: test_author

## ROLE

**Delegate only** from `daily-coder`, `use-master`, or Daily Coder runtime.

Runtime job: Write meaningful tests mapped to acceptance criteria and verify negative controls.

## AUTHORITY

IDE projection is **read-only**. Side effects and audited writes happen only in Daily Coder via `PolicyGateway` / `ToolBroker`, typically through **`ide-bridge daily-coder`**.

- Runtime `write_scope`: `test_author`
- Claim tags follow Daily Coder vocabulary; when mapping enums, load `load-on-invoke:/Users/shurley/Documents/AgentNexus/agents/ide/contracts/claim-enum-map.md` at runtime only.

## MUST NOT

- Emulate the Daily Coder phase DAG or SQLite state machine in chat.
- Use native IDE write tools for audited implementation (use `ide-bridge`).
- Nest or spawn other IDE agents unless the parent orchestrator explicitly delegates.
- Preload or `#file:`-inline the full SSOT `prompt.md` in parent orchestrator context (pointer-only projection).

## Runtime prompt (SSOT — load on invoke)

Summary: Write meaningful tests mapped to acceptance criteria and verify negative controls.

When **this agent** is invoked, read the full runtime instructions from SSOT (not at picker/resident load):

`load-on-invoke:daily-coder-ecosystem/agents/test_author/prompt.md` (sha256 `fa3b15905de78ae6ea823f6a4bcb22e475b83dc244a3ebe826488773db82ba70`)

## Projection SSOT

| Field | Value |
|-------|-------|
| Agent directory | `daily-coder-ecosystem/agents/test_author` |
| `prompt.md` sha256 | `fa3b15905de78ae6ea823f6a4bcb22e475b83dc244a3ebe826488773db82ba70` |
| `agent.json` sha256 | `c0d6388f1de58177c6225d6f8155c7ca11bac6d9cfcd9e9b2e67be39db03a41e` |
| Regenerate | `python /Users/shurley/Documents/AgentNexus/agents/ide/scripts/import_daily_coder_agents.py` |

## Tool intent (runtime allowlist reference)

Configured DC tools (prompt cannot grant tools): filesystem.read, filesystem.search, filesystem.write, patch.apply, tests.run, repository.diff.

Output schema: `test_authorship`.

## Examples

- **Good:** Parent passes bounded context; role emits schema-shaped JSON with tagged claims only.
- **Anti-pattern:** Chat claims COMPLETE or SIMULATED without `ide-bridge` / runtime acceptance.
