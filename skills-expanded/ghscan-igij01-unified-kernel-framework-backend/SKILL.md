# ADR-0024: `/arch-refactor` Skill — ADR-Driven Architectural Refactor Workflow

## Status

Proposed

## Date

2026-05-06

## Context

This repo's significant architectural changes — the Profiler/Autotuner
split (ADR-0009), `TuneService` introduction (ADR-0011),
single-point execution (ADR-0012), the JIT compilation move (ADR-0014),
the backend contract redesign (ADR-0015), and most recently the
abstract `Pipeline` Protocol with paired orchestrator/debug-session
(ADR-0021/0022) — have followed a consistent rhythm:

1. The user surfaces a conceptual concern ("the autotuner's loop is
   tightly coupled to our types," "verification policy and capability
   are orthogonal").
2. A discussion clarifies *what* the split is and *where* the seams
   land, *before* any code is touched.
3. An ADR (sometimes a pair) captures the decision and its
   consequences.
4. A sized todo list breaks implementation into independently
   reviewable steps.
5. Per-step agents do the mechanical work; the human reviews each
   main-code step before continuing.
6. Tests come at the end as a single batch, after the architecture is
   in place.

This rhythm is not accidental — when steps were skipped (jumping to
code without discussion, or writing one giant ADR that mixed protocol
and storage concerns), the resulting work needed rework.  Specifically,
the ADR-0021 first draft conflated the abstract autotuner protocol
with kernel-list orchestration concerns and had to be refactored into
two paired ADRs once the discussion clarified the responsibility split.

The rhythm also depends on a small number of project-specific
conventions that are easy to forget: the container name
(`cuda130-torch`) for running Python, the test-dep installs
(`pytest-asyncio`, `cupy-cuda13x`), the project's pre-publication
stance on backwards-compat shims, the "Protocols over inheritance"
guideline from `CLAUDE.md`, and the policy of co-locating paired ADRs
when scope warrants splitting.

Today this rhythm lives only in habit and in the user's repeated
guidance.  Each new architectural refactor reinvents the wheel: the
user has to remind Claude to discuss before drafting, to size the todo
list, to use the right container, to stop after each main-code step
for review, to verify agent claims independently rather than trusting
the report.  That friction adds up, and a future contributor (or a
future Claude session) without the conversational context will
re-litigate decisions the project has already made.

The Claude Code skill system (`.claude/skills/<name>/SKILL.md`) is the
correct mechanism for codifying a workflow that is repeated, has
project-specific quirks, and should be invokable both by name and by
contextual trigger.  Existing project skills already follow this
pattern: `architecture-decision-records` codifies *how to write* an
ADR; `bug-fix-and-ship` codifies the bug-report → fix → test → ship
pipeline; `run-in-container` codifies the container-execution wrapper.
None of them cover the architectural-refactor flow.

## Decision

Create a new project-local skill at
`.claude/skills/arch-refactor/SKILL.md` that codifies the
architectural-refactor workflow described above.

### Skill identity

- **Name:** `arch-refactor`.  Short, descriptive, pairs naturally with
  the existing `architecture-decision-records` skill (which it
  invokes for the ADR-writing phase).
- **Invocation:** `/arch-refactor` (no required arguments).
- **Triggers:** Two ways to engage the skill:
  1. **Explicit user invocation** — user types `/arch-refactor` or
     mentions the skill by name.
  2. **Contextual** — the user proposes an architectural change that
     should be documented by an ADR.  Signals include: proposing to
     split a class along conceptual lines; describing a new
     abstraction, Protocol, or pluggable boundary; using language
     like "refactor", "extract", "abstract", "pluggable", "swap out",
     "modularize"; or mentioning an existing ADR that needs revision
     in step with code changes.

### Skill phases (moderately strict)

The skill enforces hard gates between phases — Claude does not advance
to the next phase without an explicit step.  Within each phase, work
is loose.

1. **Discussion (gate: user agreement on the split).**  Claude reads
   the affected modules, names the conceptual responsibilities being
   re-cut, and proposes a split.  Trade-offs are surfaced as
   options, not decisions.  Claude does not draft an ADR or write
   code in this phase.  Exit only when the user confirms the
   conceptual split.
2. **ADR drafting (gate: user approves ADR contents).**  Claude
   invokes the `architecture-decision-records` skill for mechanics
   and writes the ADR(s) reflecting the discussion.  When scope
   warrants, paired ADRs are produced and land together.  Whether
   to split into paired ADRs is a judgement call left to Claude
   based on the discussion's outcome — the criterion is "two cleanly
   separable concerns that each warrant their own scope," but the
   skill does not enforce a hard rule.  Exit only when the user
   approves the drafted ADR(s).
3. **Plan (gate: user approves the todo list).**  Claude produces a
   numbered todo list with main-code items and test items clearly
   separated.  Each main-code item is sized to a single coherent
   reviewable change.  Test items come at the end as a single
   bundle.  Exit only when the user approves the plan.
4. **Implementation (gate: per-main-code-item user review).**  For
   each main-code item, Claude spawns a sub-agent with a
   self-contained prompt, then independently verifies the agent's
   claims (greps, reads, runs import smoke checks) before reporting
   to the user.  Claude stops after each main-code item for the
   user to review the diff.  Test items are bundled into a single
   final dispatch with no per-step review.

The skill never advances a gate on its own.  If the user is silent or
ambiguous, Claude asks rather than guesses.

### Off-ramps

Two off-ramps the skill should recognize and offer:

1. **Skip the ADR phase** when the change is small, local, and
   reversible (e.g. renaming a private method, moving a helper).
   The skill should detect this during discussion and recommend
   skipping the ADR rather than ceremonially writing one for a
   trivial change.  The decision is the user's; the skill only
   surfaces the option.
2. **Abandon mid-flight** when discussion reveals the proposed split
   is wrong.  Claude should treat "this isn't right, let's
   reconsider" as legitimate and return to the discussion phase
   without sunk-cost defending the prior draft.

### Project-specific conventions encoded

The skill bakes in conventions that have surfaced repeatedly:

- **Container.**  All Python execution happens inside the
  `cuda130-torch` container via the `run-in-container` skill.
  Sub-agent prompts always include this instruction.
- **Test dependencies.**  Sub-agents that run pytest must install
  `pytest-asyncio`; sub-agents that run CUDA backend tests must
  install `cupy-cuda13x`.
- **Pre-publication code.**  No backwards-compat shims, no
  deprecation aliases — hard cuts and renames are preferred.
- **Protocols over inheritance.**  Per `CLAUDE.md`, new abstractions
  use `typing.Protocol` (often `@runtime_checkable`) rather than ABC
  hierarchies.
- **ADR location.**  All ADRs live in `docs/adr/` with sequential
  numbering.  The skill checks the next available number before
  writing.
- **Verify before trusting.**  Sub-agent reports are summaries, not
  ground truth.  After each agent run, Claude independently
  verifies the claims via `grep`/`Read`/import smoke checks.

### Sub-agent prompts

Sub-agent prompts produced by this skill are self-contained — they
read the relevant ADR(s), state the concrete task, list constraints,
specify sanity checks, and request a bounded report.  The skill's
SKILL.md includes a prompt template for the implementation phase to
keep prompts consistent across steps.

## Consequences

### Positive

- **Reproducible architectural work.**  Future refactors follow the
  same rhythm without the user having to re-teach it.
- **Quality bar preserved.**  The hard gates (discussion → ADR →
  plan → implement) prevent the failure modes seen in early drafts:
  jumping to code, oversized ADRs, missed responsibility splits.
- **Project conventions surface automatically.**  Container name,
  test deps, pre-publication stance, Protocol-over-ABC — all
  encoded so contributors don't have to remember them.
- **Composes with existing skills.**  Invokes
  `architecture-decision-records` for ADR mechanics; reuses
  `run-in-container` for sandbox execution; complements
  `bug-fix-and-ship` (bug fixes go there, refactors come here).
- **Lightweight off-ramps.**  Trivial changes don't get ceremonied;
  bad designs caught in discussion can be abandoned without sunk
  cost.

### Negative

- **Workflow rigidity.**  Hard phase gates can slow down small
  refactors that *are* worth an ADR but don't need a full plan +
  per-step review.  Mitigated by the off-ramp for trivial changes
  and by the fact that the user can always abandon the skill
  mid-flight.
- **Skill drift.**  The encoded conventions (container name, test
  deps) live in two places now — `CLAUDE.md` and the skill —
  creating a synchronization risk.  Mitigated by treating
  `CLAUDE.md` as authoritative and having the skill's SKILL.md
  cross-reference it rather than duplicate.
- **Trigger ambiguity.**  Contextual triggers ("user proposes a
  major architectural change") rely on Claude's judgement about
  what counts as "major."  Some refactors that should use the
  skill won't trigger it; some trivial renames may.  The slash
  command remains the reliable fallback.
- **Maintenance.**  When project conventions change (e.g. the
  container name changes, or backwards-compat policy tightens
  post-publication), the skill needs an update.  Acceptable cost
  for the workflow gain.

## Related Decisions

- [ADR-0011](0011-tune-service.md), [ADR-0014](0014-jit-compilation-with-constexpr-sizes.md),
  [ADR-0015](0015-backend-contract-redesign.md),
  [ADR-0021](0021-abstract-pipeline-protocol.md),
  [ADR-0022](0022-pipeline-orchestrator-and-debug-session.md) —
  representative architectural refactors that the skill is
  distilled from.
- The `architecture-decision-records` project skill — invoked by
  this skill during the ADR-drafting phase.
- The `run-in-container` project skill — invoked by sub-agents
  produced by this skill for all Python execution.
- `CLAUDE.md` — authoritative source for project conventions
  (container name, build system, design principles); cross-
  referenced rather than duplicated by the skill.

## Follow-ups (not decided here)

1. The skill's actual SKILL.md content — drafted as the
   implementation step of this ADR.
2. Whether to also create a complementary "minor-refactor" skill
   for changes that warrant the rhythm but not the ADR.  Not
   needed yet; revisit if the off-ramp proves too coarse.
3. Whether sub-agent prompts should be templated as separate files
   under `.claude/skills/arch-refactor/templates/` or inlined in
   SKILL.md.  Decided during implementation based on prompt size.
