---
name: rc
description: "Explains RC — its skills, agents, hooks and artifacts. Use to learn what RC offers. Do not use to run a workflow step."
disable-model-invocation: true
model: haiku
effort: low
---

# RC

An agent plugin for AI-assisted development: **skills, agents and hooks**, loaded by the host. No CLI,
no daemon, no database. Every artifact is plain markdown under a project's `.rc/`, versioned with the
code.

Three primitives, one job each. When a component sits in the wrong one, the tell is in the table:

| Primitive | Job | It's in the wrong place when |
| --- | --- | --- |
| **hooks** | deterministic rules that hold *every* time | it is written as prose in a skill and the agent skips it under pressure |
| **skills** | the disciplines the agent reaches for | it is a sequence of other skills |
| **agents** | context isolation — fan-out, adversarial review | it has a catalog entry instead of being spawned from inside a skill |

## Installation

Install through your host's plugin mechanism; skills, agents and hooks are auto-discovered. Claude
Code: `/plugin marketplace add rodolfochicone/rc-project`, then `/plugin install rc@rc-project`. GitHub
read access is required for the private repo (`gh auth login` or `GH_TOKEN`).

## The skills

Only `skills/promoted/` ships. `skills/stacks/` and `skills/misc/` stay on disk, editable and
greppable, out of the context budget — see **Buckets** below.

This skill itself carries `disable-model-invocation: true`: it is a reference for *you*, so the model
never needs to reach it mid-task, and stripping it from the listing costs the budget nothing. That is
the second lever after the buckets — a skill only ever invoked by hand pays zero context load.

**The build path**, in order. Each phase reads what the last one wrote:

| Skill | Use it to |
| --- | --- |
| `rc-spec` | interview an idea into a spec — product intent, then technical design, with ADRs |
| `rc-tickets` | break that spec into independently implementable tickets with blocking edges |
| `rc-implement` | build the tickets in dependency order, least code first, then the gate |
| `rc-tdd` | drive the test side: red → green, one vertical slice, at agreed seams |
| `rc-code-review` | review on three lenses (standards, spec, delete-list) and fix what it confirms |
| `rc-git` | ship it: branch, push, PR — confirming each outward-facing step |

**Reached when needed:**

| Skill | Use it to |
| --- | --- |
| `rc-diagnose` | root-cause any bug, failure or tracing question, then fix and verify |
| `rc-memory` | recall and record what this project taught — facts, lessons, golden paths |
| `rc-codemap` | build cheap per-directory structure maps before exploring a large repo |
| `rc-council` | stress-test a high-impact decision across advisors, preserving dissent |
| `rc-writing-for-agents` | author or trim a skill, an `AGENTS.md`, or a hook — and audit context cost |
| `rc-codebase-design` | decide where an interface goes and how much it hides — module, depth, seam |
| `rc-interface-design` | build UI with craft, avoiding generic AI aesthetics |
| `rc-typescript` · `rc-python` · `rc-sql` | type design, idiomatic Python, relational query and schema work |

Read `references/conventions.md` for the rules the skills share — `.rc` resolution, Serena
navigation, untrusted content, root-cause-over-workaround, the verification-evidence bar, and project
memory. It is held once, not pasted into each skill.

## Buckets

Every shipped description is charged against the host's skill-listing budget in **every** session —
Claude Code's `skillListingBudgetFraction` defaults to 1% of the context window. Past that budget the
host does not disable skills, it **drops descriptions**, starting with the least-invoked, and the skill
goes mute: present by name, with nothing for the model to match against. That is why the shipped set is
small and every promoted description is capped at 150 characters.

| Bucket | Ships | Holds |
| --- | --- | --- |
| `promoted/` | yes | the 17 above |
| `stacks/` | no | `rc-rust`, `rc-axum`, `rc-sqlx`, `rc-sveltekit` — load by name when working that stack |
| `misc/` | no | `rc-board`, `rc-gan`, `rc-qa-execution`, `rc-openapi`, `rc-postman`, `rc-readme`, `rc-a11y`, `rc-seo`, `rc-observability`, `rc-resilience`, `rc-video` |

`scripts/plugin-smoke.mjs` enforces the split: everything in `promoted/` is in the manifest, nothing
outside it is, and the promoted count has a ceiling that must be raised deliberately.

## Agents

Four council archetypes, dispatched by `rc-council` — not a general-purpose worker pool. The host's own
`Explore` and the model's tool access already cover recon, library lookups and bounded edits; four
leaf-worker agents that duplicated them shipped for months with zero invocations and were removed.

| Agent | Perspective |
| --- | --- |
| `pragmatic-engineer` | execution reality, maintenance burden, team velocity |
| `architect-advisor` | boundaries, coupling, long-horizon coherence |
| `security-advocate` | attack surface, blast radius, compliance |
| `devils-advocate` | hidden assumptions, edge cases, failure modes |

## Hooks

Configured in `hooks/hooks.json`, gated by `RC_HOOK_PROFILE` (`minimal|standard|strict`) and
`RC_DISABLED_HOOKS`. Every hook fails open: an environment problem never blocks a tool call.

- **Guardrails** — `git-guard` and `commit-guard` (never auto-commit or push; destructive git denied,
  recoverable-but-serious git asks), `db-guard` (database access read-only by default),
  `gateguard` (grounding before the first edit of a file).
- **Discipline** — `no-workarounds-guard` prompts before an edit introduces a type assertion, a lint
  suppression or a swallowed error. `verify-guard` stamps the project's gate when it runs and asks
  before a commit whose code changed after that stamp.
- **Memory** — `observe` appends tool observations for the `rc-memory` distill pass; `memory-load`
  surfaces the store at SessionStart.
- **Resilience** — `repair-guidance` injects corrective guidance when an `Edit` or `Task` returns a
  repairable failure, so the agent fixes the cause instead of retrying the same failing call.

A rule that must hold every time belongs here, not in prose. `rc-writing-for-agents`
(`references/hooks.md`) owns authoring one.

## Commands

Two, both thin prompt macros with no skill behind them: `/rc-commit-msg` (a Conventional Commits
message from the staged diff — it never commits) and `/rc-plano` (explore → assumptions → plan → stop
for approval). The eight others were sequences of "invoke skill A, then B, then C" — orchestration
duplicated between a command and the skills it called — and were removed with the skills they drove.

## Artifacts

```
.rc/
  tasks/
    <slug>/
      _prd.md _techspec.md _tasks.md    # spec (rc-spec) + master ticket list (rc-tickets)
      task_01.md … task_N.md            # one ticket each
      adrs/                             # architecture decision records
      notes.md                          # task-scoped scratch, deleted with the task
      code-review-NNN.md                # review + fix rounds (rc-code-review)
    _archived/<slug>/
  memory/                               # durable store (rc-memory)
    INDEX.md <slug>.md                  # facts
    lessons.json LESSONS.md             # machine-owned lesson store
    observations.jsonl                  # raw capture (observe hook)
  analysis/                             # rc-diagnose reports outside a slug
  ROADMAP.md                            # phases for unattended mode (rc-tickets, roadmap mode)
```

Archive a finished slug by moving `.rc/tasks/<slug>/` into `.rc/tasks/_archived/`.

## Configuration

No runtime config file. Model and reasoning effort live in each skill's and agent's frontmatter
(`model:` / `effort:`); hook behaviour is set by `RC_HOOK_PROFILE` and `RC_DISABLED_HOOKS`. See
`references/config-reference.md`.

## Anti-patterns

- **Executing without a spec and tickets.** The pipeline exists because unstated intent produces
  plausible-looking wrong work.
- **Promoting a skill without demoting one.** The ceiling is the point; crossing it silently is how
  48 skills happened, and how they went mute.
- **Writing an every-time rule as prose.** It becomes advisory the moment context gets tight.
- **Claiming done without fresh evidence.** `references/conventions.md` holds the bar.
