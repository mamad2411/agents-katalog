---
name: agent-runtime-governance
description: >-
  Audit runtime controls for tool permissions, approvals, memory, telemetry,
  evals, rollout, and containment. Use when reviewing tool-bearing agent
  systems. NOT for security scans, prompt-only work, or static code review.
argument-hint: "<mode> [system-or-path]"
model: opus
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Agent Runtime Governance

Design and audit the controls that keep tool-bearing agent systems predictable,
observable, and safe to operate.

**Scope:** Runtime governance for agents that use tools, memory, approvals,
subagents, evals, or external systems. NOT for generic vulnerability scanning
(`security-scanner`), normal code review (`review`), prompt-only
optimization (`prompt-engineer`), or MCP implementation details (`mcp-creator`).

## Dispatch

| `$ARGUMENTS` | Mode | Action |
|---|---|---|
| Empty | `menu` | Show governance modes and required inputs |
| `design <system>` | `design` | Define runtime policies for a new or changing agent system |
| `audit <path-or-system>` | `audit` | Review existing tool, approval, memory, telemetry, and eval controls |
| `permissions <agent-or-tools>` | `permissions` | Design allowlists, denylists, approval modes, and escalation rules |
| `memory <agent-or-system>` | `memory` | Define memory scope, retention, privacy, and invalidation policy |
| `evals <workflow>` | `evals` | Plan regression, adversarial, and runtime acceptance eval loops |
| `rollout <system>` | `rollout` | Define staged release, monitoring, rollback, and operator readiness controls |
| `incident <failure-mode>` | `incident` | Define containment and recovery controls for agent failures |
| Natural language about agent tools, permissions, memory, evals, or containment | Auto-detect the closest mode |

## Governance Surfaces

| Surface | Review Questions |
|---|---|
| Tools | Which tools can read, write, spend money, deploy, message users, or delete data? |
| Approvals | Which operations require explicit user approval or human review? |
| Memory | What can be stored, for how long, and at what scope? |
| State | What is durable, replayable, idempotent, and auditable? |
| Telemetry | Which traces, decisions, tool calls, and failures are observable? |
| Evals | Which scenarios prevent regression before rollout? |
| Containment | How does the system stop, rollback, quarantine, or degrade safely? |

## Canonical Vocabulary

Use these canonical terms exactly when producing governance reports.

| Term | Meaning |
|---|---|
| **tool consequence** | The real-world effect a tool call can have: read, write, deploy, message, spend, delete, or expose |
| **approval gate** | Explicit human or policy checkpoint before a higher-risk action |
| **runtime guard** | Hook, wrapper, allowlist, denylist, test, or platform policy that enforces a governance rule |
| **memory boundary** | Scope, retention, redaction, and invalidation policy for stored agent context |
| **containment** | Stop, rollback, quarantine, or degrade action after unsafe or failed behavior |
| **shadow mode** | Runtime mode that records proposed actions without executing them |

## Classification Gate

Classify the request before choosing a mode:

1. If it asks for app vulnerability scanning, route to `security-scanner`.
2. If it asks for code review, route to `review`.
3. If it asks for prompt wording only, route to `prompt-engineer`.
4. If it asks how to implement an MCP server, route to `mcp-creator`.
5. Otherwise, choose the closest runtime governance mode from the dispatch table.

## Workflow

1. Define the agent’s job, users, data sensitivity, and external effects.
2. Inventory tools by capability: read-only, write, destructive, financial,
   deploy, messaging, credential access, and network egress.
3. Map approval gates to consequence, reversibility, and confidence.
4. Define memory scope, retention, redaction, and invalidation rules.
5. Require telemetry for tool calls, decisions, approval outcomes, and failures.
6. Build evals around unsafe tool use, stale memory, missing approval, and
   failure containment.
7. Define rollout gates, rollback criteria, and operator evidence for changes
   that affect live users, accounts, credentials, or external systems.
8. Return a governance matrix with owners and enforcement points.

## Scaling Strategy

| Scope | Strategy |
|---|---|
| Single agent or workflow | Produce one control matrix and one eval/monitoring set |
| Multiple agents sharing tools | Group by tool consequence and shared approval gates |
| Platform-wide governance | Define baseline policy first, then exceptions by agent class |
| Live production rollout | Add staged rollout, rollback, monitoring, and owner review gates |

## Progressive Disclosure

- Start with this `SKILL.md` for routing and control surfaces.
- Read `references/control-matrix.md` for permissions, memory, telemetry, and eval controls.
- Read `references/rollout-governance.md` only when release, rollback, monitoring, or production readiness is in scope.
- Do not load security, prompt, or MCP implementation references unless routing redirects to those skills.

## Reference File Index

| File | Read When |
|---|---|
| `references/control-matrix.md` | Designing or auditing runtime control surfaces |
| `references/rollout-governance.md` | Planning staged release, rollback, monitoring, and operator readiness |

## Output Shape

```markdown
## Agent Governance Report

- System:
- Mode:
- Risk tier:

### Control Matrix
| Surface | Current | Required | Enforcement | Evidence |
|---|---|---|---|---|

### Required Changes
- ...

### Evals And Monitoring
- ...

### Rollout And Containment
- ...
```

## Critical Rules

1. Classify tools by consequence before recommending autonomy.
2. Require explicit approval for irreversible, costly, public, credential, or destructive actions.
3. Keep memory scope narrow and document retention, redaction, and invalidation.
4. Require telemetry for tool calls, approvals, denials, failures, and containment actions.
5. Add evals for unsafe tool use, missing approval, stale memory, and rollback behavior.
6. Separate policy from enforcement; name the hook, wrapper, test, or runtime gate that enforces each rule.
7. Do not replace `security-scanner`, `review`, `prompt-engineer`, or `mcp-creator`; route to them when the request is outside runtime governance.
8. Do not mark a governance change ready without rollout, rollback, and monitoring criteria.

## Validation Contract

Run from this skill directory before declaring changes complete:

```bash
python scripts/check.py
```

Completion criteria:

1. `scripts/check.py` exits 0.
2. No portable-CLI violations remain under this skill directory.
3. Smoke review covers explicit, implicit, rollout, and negative-control prompts.
