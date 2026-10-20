---
description: "Use when: a commit, CI gate, lint, typecheck, or ReqToCode guardrail fails and the branch must be repaired and made push-ready."
name: "Repair Commit Guardrails"
argument-hint: "Paste the failure output, name the failed gate, or give the commit SHA/range to investigate"
---

Repair a failed commit guardrail in the Rotaris repository. Work from the
concrete failure supplied in `$ARGUMENTS`; if none is supplied, inspect the
latest relevant Git and CI state to identify it.

Your goal is to leave the working tree with the underlying defect fixed and
the affected push gates passing. Do not make a commit or push unless explicitly
asked.

## Operating Rules

- Preserve unrelated user changes. Inspect `git status` before editing and do
  not revert, reset, stash, or rewrite work that is not part of the failure.
- Reproduce the narrowest failed guardrail first. Treat its error output as the
  primary evidence, not a symptom to suppress.
- Identify causal history only when it helps: use `git log`, `git diff`, and
  `git blame` to find the introducing commit, changed requirement, feature, or
  contract. Do not assume the most recent commit caused the failure.
- Read the responsible implementation, its requirement, and the relevant test
  together before changing code. Classify the root cause: implementation bug,
  incorrect or stale test, broken traceability, missed generated artifact,
  lint/type error, or configuration/tooling defect.
- Fix the root cause with the smallest coherent change. Do not weaken tests,
  delete traces, add baseline exceptions, or bypass guardrails to make a failure
  disappear.
- For product changes and bug fixes, bump `pyproject.toml` as required by
  `AGENTS.md`.

## ReqToCode Signals

For any ReqToCode verifier error, ReqToCode meta-test failure, failed trace
link, missing annotation, generated `SWR` symbol error, or requirement-store
change: load the `reqtocode` skill and work its Flow C —
`docs/reference/reqtocode-playbook.md` is the runbook, including the hard rules
about what you may never do to make a failure disappear. Do not improvise a
shorter path here.

## Repair Workflow

1. Capture evidence: `git status`, current branch, failed command/output, and
   the narrowest reproduction command.
2. Trace the failure to the decision or behavior that produced it. When useful,
   identify the responsible commit and associated feature/SWR from Git history
   and requirement links.
3. Make one focused repair. Add or correct a behavioral regression test when
   the failure exposes missing coverage; follow `tests/AGENTS.md` and use
   `@verifies` with the required productive-use docstring.
4. Immediately rerun the exact narrow reproduction. Repair again only within
   that slice until it passes.
5. Run the applicable broader gate(s) in the order given by
   [AGENTS.md §Workflow](../../AGENTS.md#workflow--worktree-merge),
   using the exact invocations from [AGENTS.md §Commands](../../AGENTS.md#commands).
   Run the failed hook command or gate again last. Do not bypass hooks or omit
   their checks.

6. Review the final diff and status for unintended changes. Report only after
   every applicable validation passes, or clearly identify the concrete blocker
   and the command/output that still fails.

## Final Response

Provide a short repair report:

```markdown
## Cause

[Root cause, responsible change/feature/SWR if identified.]

## Repair

- [Changed behavior and files.]
- [Test or traceability change, if applicable.]

## Validation

- [Command]: passed
- [Command]: passed

## Remaining State

[Clean/push-ready status, or exact blocker.]
```
