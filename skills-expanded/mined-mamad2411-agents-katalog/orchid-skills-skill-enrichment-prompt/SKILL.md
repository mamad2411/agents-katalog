# Skill Enrichment Prompt

Use this prompt when another agent should improve Orchid's included skill stubs.

```text
Improve the two Orchid skill stubs in this repository. Make exactly two
content edits:

1. `skills/make-specs/SKILL.md`
2. `skills/orchid/SKILL.md`

Start from those files, then research just enough local context to adapt them:
read the README, AGENTS.md if present, CLI help, tests/fixtures, and any nearby
examples of task specs or repo workflow. Do not copy this prompt into the
skills. Do not add reference files; keep each skill as one concise `SKILL.md`.
Keep descriptions specific, third-person, and trigger-oriented; keep workflows
sequential with explicit validation loops.

For `skills/make-specs/SKILL.md`, make the skill better at creating
dispatchable Orchid specs. It should keep the human in the loop before freezing
non-trivial work: clarify intent, success criteria, desired task granularity,
review expectations, and the ideal shape of the spec. It should steer ambiguous
work into discovery or a draft spec. Preserve the core spec ingredients:
stable requirement ids, design notes with scope/non-goals/risks/validation,
policy in `spec.toml`, narrow task files with concrete scopes, dependencies,
DoD, task-level validation, aligned `covers`, and a lint/fix/re-run loop.
If network access is available, a short deeper research pass can improve this
skill significantly. Useful search terms include EARS requirements, PRD vs
design doc, acceptance criteria, INVEST stories, vertical slices,
tracer-bullet development, red-green-refactor, ADR/RFC, agent handoff, and
validation gates. Distill the useful practices; do not paste research into the
skill.

For `skills/orchid/SKILL.md`, make the orchestration workflow concrete and safe
for a shared Git worktree. It should follow repo conventions for validation,
branching, commit messages, signing/signoff, and review. Cover phase
observation, serial-by-default leases, bud delegation for scoped ephemeral work,
agent-id lookup as discovery only, packet handoff, reports as claims,
touched-file attribution, validation before completion, staging only approved
pathspecs, stale-lease recovery, cleanup, and backoff for unavailable agents or
flaky resources. The critical rule: spawned agents only work or review. They
must not stage files, commit, edit task state, close leases, or own final
handoff. The coordinator owns validated staging, intentional commit, independent
auto-review against the request/spec/diff, and final cleanup.

Use normal engineering heuristics where they sharpen the workflow: red-green
loops, tracer-bullet slices, small reversible steps, explicit evidence, and
bounded retries. Keep the skills minimal and operational, not exhaustive. The
result should feel repo-specific, but still leave room for teams to customize
their own preferences.

Before finishing, inspect the diff. It should touch only the two target
`SKILL.md` files unless the repository clearly requires otherwise, and each
skill should remain short enough to read quickly.
```
