---
name: setup-ph-build
description: Detect the harness, map the five effort tiers onto models it can actually reach, and write the fan-out policy that every ph-build skill reads.
disable-model-invocation: true
---

# Setup ph-build

Write the **fan-out policy** — one file holding the entire cost picture for this
plugin: which model each effort tier resolves to, how many agents each skill may
spawn, and the total budget for each playbook.

One file, one read. Nobody should have to open nine skills to answer "what will
this cost me."

## Where it goes

The policy is machine-level, not per-repo — run this once per machine, not once
per project. Only the path is harness-specific:

| Harness | Path | Wiring |
| --- | --- | --- |
| Claude Code | `~/.claude/ph-build-policy.md` | append `@~/.claude/ph-build-policy.md` to `~/.claude/CLAUDE.md` |
| Codex | `~/.codex/ph-build-policy.md` | reference it from `~/.codex/AGENTS.md` |
| Other | that harness's user config directory | whatever that harness uses to include standing context |

If the harness has no mechanism for always-loaded context, write the file anyway
and tell the user it must be referenced manually. Skills fall back to their own
documented defaults when no policy is present, so a missing file degrades to
cheap-and-safe rather than to broken.

## Process

### 1. Identify the harness

Determine which agent harness is running. Do not guess from the model name —
check what the environment actually exposes.

### 2. Enumerate reachable models

List the model identifiers this harness can dispatch subagents to. Enumerate;
do not assume. Model lineups change, and a policy naming a slug the harness
cannot resolve fails at spawn time, mid-task.

### 3. Propose a tier mapping, then ask

**Detect and propose. Never infer silently.** You can enumerate model names, but
"which of these is my judgment tier" is a cost-and-quality judgment only the
user can make, and it changes every time a model ships.

Present the proposed mapping with `AskUserQuestion` and let the user correct it.

| Tier | What runs here | Pick a model that is |
| --- | --- | --- |
| `scan` | File searches, deterministic lookups, reading a slice of a corpus — a step above `rg` | Cheapest and fastest |
| `scoped` | Building against a fully settled spec: `problem`, `shape`, `approach`, `verification` all closed | Solid mid-tier; deep reasoning is wasted when the thinking is already done |
| `judgment` | Code review, architecture, hard calls, synthesis | Strongest analytical |
| `divergent` | Creative and architectural exploration, in limited bursts | Strongest creative, distinct from `judgment` |
| `panel` | Multi-model adversarial review — the most expensive rung | Three *different* models, for genuine diversity |

The ladder is strictly ordered: `scan` < `scoped` < `judgment` < `divergent` <
`panel`. No ties.

`panel` is not one model. Cross-family diversity is the entire mechanism — three
reviewers on one model is three correlated opinions. Where the harness offers
fewer than three families, say so in the file so skills can report the
limitation rather than pretending to a diversity they do not have.

Two aliases are always valid in any slot: `inherit-parent` and `auto` both mean
"run on the parent session's model" (omit `model` on the `Agent` call).

### 4. Confirm the caps

Show the per-skill caps and playbook budgets below. These ship with defaults
that work; the user may raise or lower any of them. Caps are **hard ceilings**,
not targets.

### 5. Write the file and wire it up

Write the whole file — this is an idempotent overwrite, not an append. Then add
the include line to the harness's standing-context file if it is not there
already.

## File format

```markdown
# ph-build fan-out policy

## Tiers

scan: <model>
scoped: <model>
judgment: <model>
divergent: <model>
panel: <model>, <model>, <model>

## Skill caps

architect: divergent, 3 runners
arena: divergent, 3 candidates + 1 judge
interrogate: panel, 3 reviewers
swarm: scoped, 6 workers
how: scan, 3 explorers + 1 explainer
why: scan, 4 investigators + 1 synthesizer
maintain-verification-skill: scan, 5 readers
show-me-your-work: scan, 1 reviewer (conditional)

## Playbook budgets

investigation: 8
refactoring: 8
bug-fix: 10
perf-issue: 10
feature: 14

## Role tiers

feature: judgment
refactoring: judgment
bug-fix: judgment
perf-issue: judgment
hillclimb: divergent
```

## Why the budgets exist

Per-skill caps do not bound nesting. `architect` internally runs `how`, `why`,
and `arena`; cap each of those at three and `architect` still costs around nine.
The playbook budget is the ceiling on the whole composition, and it is the only
number that answers what a unit of work actually costs.

Neither replaces the one-way-door gate in `dispatch`. Caps bound the worst case;
the gate makes the common case cheap. Both are needed — the failure this plugin
exists to prevent was a fully specified task priced as though nothing were
known.
