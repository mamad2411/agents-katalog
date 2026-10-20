---
name: gates
description: >
  Toggle Forge's workflow gates and rails — strong-but-toggleable enforcement. `forge gate
  enable|disable <gate-id>` flips `workflow.gates.<id>.enabled` in `.forge/config.yaml`; the
  installed git hooks read resolved config at run time, so disabling a rail makes them
  genuinely inert. `forge gate approve|reject <issue> <gate>` records durable human-gate
  approval events; `forge gate status`/`check` query them; `forge control <id>
  <mandatory|optional|permission>` sets tri-state DECLARED intent (writes the same `enabled`
  field — no independent runtime enforcement). Use when the user says "disable the gate",
  "turn off TDD enforcement", "the tdd intent rail is blocking me", "toggle or enable a
  gate", "loosen enforcement", or "approve a human gate". Common default-ON toggleable rails:
  `rail.tdd_intent`, `rail.kernel_tracking`, `rail.auto_shepherd` — e.g. `forge gate disable
  rail.tdd_intent`. NOT for addressing PR review feedback (review), NOT the status snapshot
  of work in flight (status).
allowed-tools: Bash, Read, Grep, Glob
terminal: true
---

Forge's gates and rails are **default-strong but toggleable**. The `gates` skill is how you flip one off (or back on), record a human-gate approval, and see enforcement state. The stored truth is one field — `workflow.gates.<id>.enabled` — and the installed hooks read the resolved config at run time, so a disabled rail is genuinely inert, not cosmetically off.

# Toggling gates and rails

## When to use

- "Disable the gate", "turn off TDD enforcement", "the tdd intent rail is blocking me".
- "Toggle / enable a gate", "loosen enforcement for this repo".
- "Approve a human gate" (record a durable approval event on an issue).

## Toggle a gate or rail (the enforcement switch)

```bash
forge gate disable <gate-id>     # set workflow.gates.<id>.enabled = false in .forge/config.yaml
forge gate enable  <gate-id>     # set it back to true
```

An unknown gate id — or disabling a **locked** gate — errors **before** anything is written, never mid-run. Because the hooks resolve config at run time, the flip takes effect immediately with no reinstall.

### Common rails (default-ON, toggleable)

| Rail | What it enforces | Turn off with |
| --- | --- | --- |
| `rail.tdd_intent` | Pre-commit TDD gate (source changed ⇒ tests changed). The `minimal` adoption profile ships it off. | `forge gate disable rail.tdd_intent` |
| `rail.kernel_tracking` | "File every issue" — nothing discussed goes missing. | `forge gate disable rail.kernel_tracking` |
| `rail.auto_shepherd` | The autonomous PR-shepherd daemon fire. | `forge gate disable rail.auto_shepherd` |

The `gate.*` and `rail.*` id namespaces are disjoint, so `forge gate enable|disable` governs both through one flat surface.

## Human-gate approval events

```bash
forge gate approve <issue-id> <gate-id>                     # record a durable gate.approved event
forge gate reject  <issue-id> <gate-id>                     # record gate.rejected
forge gate status  <issue-id>                               # list recorded events for that issue (resume-safe)
forge gate check   <issue-id> <gate-id>                     # exit 0 iff gate DISABLED or an approval exists on that issue
```

`check` is the reusable enforcement primitive a stage skill calls: it passes when the gate is disabled or an approval event has been recorded for that specific issue id (approvals are issue-scoped, so pass the same `<issue-id>` you approved against). Events are durable on the issue, so they survive a compaction or crash.

## Tri-state control (declared intent)

```bash
forge control <gate-id|rail-id> <mandatory|optional|permission>
forge control status [--json]
```

`forge control` sets the **declared intent** vocabulary and writes the **same** `enabled` field that `forge gate` writes — there is deliberately no parallel key. It is a view/intent layer: today no runtime consumer denies purely on a control flag (MCP/rules/skills are presence-only and refused). For actually turning enforcement off, use `forge gate disable`.

## The doc-update gate

```bash
forge gate doc <detect|check|init|...>     # = forge doc-gate (run `forge doc-gate --help`)
```

The doc-update gate folds under this noun as `forge gate doc`; bare `forge doc-gate` stays as a back-compat alias.

## Adjacent skills

- Addressing PR review feedback / resolving threads → `review`.
- The snapshot of where the project stands and what's in flight → `status`.
