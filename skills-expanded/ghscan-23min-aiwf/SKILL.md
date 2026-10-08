---
id: ADR-0019
title: Ship the code-health rubric as an advisory ritual skill
status: accepted
---
## Context

aiwf scores its own codebase against a stack-agnostic field guide,
"Principles for a healthy codebase" — the rubric behind the periodic health
scorecards under `docs/archive/pocv3/`. The rubric is reusable by any project, but it
has no distribution vehicle: a downstream consumer who runs `aiwf init` /
`aiwf update` receives the kernel's mechanical guarantees and the ritual
skills, but not the rubric.

The question is *what vehicle* carries the rubric to consumers, and *at which
end of the lifecycle it bites*, under two standing constraints:

- aiwf writes freely only into gitignored, marker-managed locations
  (`.claude/` skills/agents/templates, `.claude/aiwf-guidance.md`,
  `.git/hooks/`) plus a single marker-wrapped import line in the consumer's
  root `CLAUDE.md`. It does **not** write tracked files (e.g. into `docs/`)
  without explicit per-invocation consent (ADR-0015 / ADR-0018).
- aiwf does not prescribe how consumers write code. The rubric is a set of
  judgment *forces*, not pass/fail rules.

aiwf already ships two kinds of payload: **guarantees** (mechanical
chokepoints — `aiwf check`, the pre-push hook, the `internal/policies/`
tests) and **rituals** (advisory skills the assistant consults —
`wf-review-code`, `wf-tdd-cycle`, `wf-rethink`). The code-health rubric is
the same genus as the existing `wf-*` engineering skills.

A rubric like this is used at two ends of the lifecycle: to **prime** ("do it
this way," while code is written) and to **score** ("did we do it this way,"
at review/wrap). Priming is primary — catching a structural problem at wrap
is far more expensive than not introducing it.

## Decision

### 1. The full rubric ships as an on-demand advisory skill

Ship the rubric as a new advisory **ritual skill**, `wf-codebase-health`, in
the `wf-rituals` plugin under `internal/skills/embedded-rituals/`. It is
embedded via `go:embed` and materialized into the consumer's
`.claude/skills/` by `aiwf init` / `aiwf update`, on the same gitignored,
marker-managed, version-pinned pipeline as the other rituals (ADR-0014).

### 2. A minimal digest primes proactively; the skill is reached on demand

The five highest-leverage forces (D1, C1, C3, B1/B2, E1) are **primed
proactively** so the structure comes out right the first time, rather than
only checked afterward:

- **Every turn** — a minimal (~10-line) digest is appended to the per-turn
  guidance fragment (`aiwf-guidance.md`), bounded by that fragment's existing
  line-budget guard so it stays terse enough to re-anchor cheaply.
- **At build/design time** — the `builder` and `planner` agents and the
  `wf-tdd-cycle` REFACTOR step carry a pointer to the full skill, to consult
  when introducing a module or boundary.

The **scoring** face stays where it was: `wf-review-code` (the per-diff gate)
and the `reviewer` agent point to the full skill for the whole-codebase pass.

### 3. Advisory, not mechanical

The skill and the digest are **advisory**. They are not a `check` rule, not a
hook, and add no kernel surface. This is the central decision:

- The principles are judgment forces; mechanizing them is impossible for a
  language-agnostic tool and would prescribe how consumers write code.
- They are consulted when relevant and can be ignored, edited, or deleted by
  the consumer — they preserve freedom by construction.
- Skill-and-digest-as-advisory is consistent with "framework correctness must
  not depend on LLM behavior": no guarantee is claimed, so no chokepoint is
  owed.

### Roads not taken

- **Inject the *full* rubric into the per-turn guidance fragment.** Rejected
  — it would blow the fragment's line budget and dilute the operating rules.
  Only the minimal 5-force digest goes there; the full rubric stays in the
  on-demand skill. (This widens the fragment's previously aiwf-only scope, set
  by ADR-0018; see Consequences.)
- **A separate dedicated every-turn fragment** for the digest. Deferred
  (YAGNI) — it needs a new embedded artifact plus its own materialize and
  `CLAUDE.md`-wiring path; a fenced section in the existing fragment delivers
  the same priming at far lower cost.
- **Opt-in materialization of a tracked rubric doc** into the consumer's
  `docs/`. Deferred (YAGNI). aiwf does not write tracked files without
  explicit consent; a consent-gated `aiwf.yaml` knob is a future option if a
  consumer wants the rubric committed for human readers.
- **A `check` rule or git hook over consumer code.** Rejected — prescribes,
  cannot be language-agnostic, and removes the freedom this design preserves.

## Consequences

- A new `wf-*` skill ships in every materialized `.claude/`: one more file in
  the embed set, auto-discovered by the `embedded-rituals` tree embed, and
  asserted by a structural test.
- The per-turn guidance fragment now carries a minimal code-health digest,
  widening its scope beyond "operating aiwf" (ADR-0018) by one fenced
  section. The fragment's line-budget guard keeps the digest terse, and a
  test pins the digest's presence.
- The rubric is stack-agnostic and ships verbatim; its closing line invites
  per-codebase editing, and the consumer's own conventions win where they
  conflict.
- aiwf now distributes a *code-style opinion*, which narrows the
  "opinion-free kernel" framing — but only in the advisory layer, which
  already carries opinions (`wf-tdd-cycle`, `wf-rethink`). The mechanical
  layer stays opinion-free.
- The embedded `SKILL.md` is the *distributable* form of a rubric that also
  has a human-readable *authoring/reference* form as a project field guide;
  the two are roles of the same content, mirroring the source-vs-render
  pattern aiwf already uses for `ROADMAP.md` and the embedded rituals. (The
  authoring doc is maintained separately from this patch, so this ADR does
  not pin its repo path.)
