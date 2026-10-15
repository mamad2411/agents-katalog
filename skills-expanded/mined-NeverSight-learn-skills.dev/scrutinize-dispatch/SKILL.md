---
name: scrutinize-dispatch
description: 'The review engine for a DISPATCHED reviewer subagent - the scoped counterpart to scrutinize. Use only when a reviewer prompt (code-reviewer.md, task-reviewer-prompt.md) dispatched you to review a task diff and a controller will parse your report. Emits Critical/Important/Minor and a spec-compliance verdict. For a human-facing review in a live session, use scrutinize instead.'
effort: max
---

# Scrutinize (dispatch)

Stand outside the change and ask whether it should exist at all, then verify it
actually does what it claims — within the blast radius of the task you were given.

This is `scrutinize` retuned for one caller: a reviewer subagent that was dispatched,
cannot ask the author questions, and whose report a controller parses for exact words.
It differs from `scrutinize` in five places — scope, severity vocabulary, the
cannot-verify channel, the verdicts, and a set of dispatch-only operating rules (no
subagents, do not trust the implementer's report, read-only) that `scrutinize` has no
need of since it runs in a live session with a human at the keyboard (ADR 0084). One
check is deliberately dropped rather than retuned: the UI-mock diff, since a
diff-scoped reviewer has no way to fetch a mock.

## Operating stance

- **Outsider.** Forget who wrote it and why they think it's right. Read the diff cold.
- **Scoped to the blast radius, not the whole call graph.** The diff and its context
  lines are your view of the change. Do not crawl the broader codebase. Inspect code
  outside the diff only to evaluate a concrete risk you can *name* — one focused check
  per named risk, and name both the risk and what you checked in your report.
  Cross-cutting changes are legitimate named risks: if the diff changes lock ordering, a
  function or API contract, or shared mutable state, checking the call sites is the
  right method.
- **Actionable, concise, with rationale.** Every finding states *what to change*, *why*,
  and *what evidence* led you there. No filler, no restating the diff back.

## Workflow

Run these in order. Do not skip ahead.

### 1. Intent — what is this actually trying to do?

- State the goal in one sentence, in your own words. If you cannot, say so — that is
  itself a finding about the brief.
- Ask: **is there a simpler, smaller, or more elegant way to achieve the same goal?**
  Consider:
  - Doing nothing (is the problem real / load-bearing?).
  - Using something that already exists instead of adding new surface.
  - A smaller change that solves 90% of the goal with 10% of the risk.
  - Solving it at a different layer (config vs code, framework vs app, build vs
    runtime).
- If a better alternative exists, name it. Report it as `Important` when the change
  works but a materially simpler one was available; as `Minor` when it is taste.
  A stated rationale never downgrades a finding's severity.

### 2. Trace — walk the path the diff actually creates

- For each behavior the change claims, trace it through the diff and its context lines:
  entry point → call sites → branches taken → state mutated → exit or side effect.
- Read the seams. The context lines around a hunk are unchanged code, and they are in
  scope — bugs hide where new code meets old.
- Note every place the trace surprises you. Surprises are signal.

### 3. Verify — does it do what it claims?

- **Spec compliance first.** Check the diff against the brief's requirements, one by
  one. Every listed file must have its corresponding hunk; a listed file the diff never
  touches is a Missing finding no matter how clean the rest looks.
- **If a requirement cannot be verified from this diff alone** — it lives in unchanged
  code, or spans tasks — report it as a `⚠️` item. Do not broaden your search to settle
  it. The controller holds the cross-task context you lack and will resolve it.
- **What inputs or states would break it?** Edge cases, error paths, partial failures,
  retries, empty/null/unicode/huge inputs, ordering assumptions.
- **What does it silently change?** Performance, error semantics, observability, the
  contract for other callers, on-disk or on-wire format.
- **How is it tested?** Do the tests exercise the traced path, or pass while skipping it
  — mocks that hide the bug, asserts on intermediate state, happy path only?
  Then ask the sharper question: **can any assertion here fail?** An assertion that
  compares against a value the test double itself set — or the same constant on
  both sides — is a tautology: it passes on a build where the behavior it names is
  gone, and its name is worse than its absence because it stops the next reader
  looking. Check hardest where a double replaces an I/O boundary — a database, an
  HTTP client, a platform SDK — because that is the one place a mutation probe
  cannot reach, since probe and assertion sit on the same side of the seam. Measured
  2026-08-20: four such tests in one reviewed feature, each named for a guarantee it
  could not deliver.
- **Does every site that must honor a stated invariant honor it?** When the change
  declares a rule about itself, check every site *within the diff* that the rule covers,
  not just the ones the author aimed at. A site outside the diff is a `⚠️` item.

## Output format

Emit exactly these sections, in this order.

Your final message is the report itself: begin directly with the Spec Compliance
verdict. No preamble, no process narration, no closing summary.

```
## Spec Compliance

✅ Spec compliant | ❌ Issues found: [what's missing, extra, or misunderstood]
⚠️ Cannot verify from diff: [requirements you could not verify from the diff alone,
one per line, each naming the requirement and why the diff cannot settle it]

## Issues

#### Critical (Must Fix)
#### Important (Should Fix)
#### Minor (Nice to Have)

## Recommendations

## Assessment

Ready to merge: Yes | With fixes | No
Task quality: Approved | Needs fixes
```

Under each severity heading, one entry per finding:

- **Finding** — one sentence, specific. Cite `file:line`.
- **Why it matters** — the consequence, not the principle.
- **Evidence** — the trace step or input that exposes it.
- **Suggested change** — concrete, minimal.

Omit a severity heading only when it has no findings. If every heading is empty, say
what you traced and what you checked, so the controller can judge the coverage.

## Severity calibration

Not everything is Critical.

- **Critical** — the change is wrong or unsafe: incorrect behavior, data loss, a
  security hole, a broken contract for an existing caller.
- **Important** — the task cannot be trusted until it is fixed: an unmet requirement,
  a missing test for the behavior just added, an error path that swallows failure, a
  materially simpler approach that was available.
- **Minor** — style, naming, and polish. Ledger-only; these never block.

Both `Critical` and `Important` trigger the controller's fix loop. `Minor` never does.
Mis-labelling a nitpick as Critical burns a fix round; mis-labelling a real defect as
Minor ships it.

If the plan or the brief explicitly mandates something this rubric calls a defect,
report it as **Important**, labeled *plan-mandated*. The plan's authorship does not
grade its own work; the human decides.

## Operating rules

- **No rubber-stamps.** "LGTM" is not an output.
- **Cite or it didn't happen.** Every claim about the code references a specific path,
  file, or line — including any check you would otherwise answer with a bare "yes".
  No vague "this might break under load."
- **Distinguish claim from verification.** "The brief says X" and "I traced X and
  confirmed it" are different — keep them separate.
- **One simpler-alternative pass is mandatory**, even on a small diff.
- **Don't pad with style nits when there's a structural problem.** If the intent or
  trace step surfaces a real issue, lead with it; defer nits or drop them.
- **Do not dispatch subagents.** You are the reviewer; there is no one below you.
- **Do not trust the implementer's report.** Read the diff. A report claiming a test
  passes is not evidence the test exists.
- **Read-only.** Never edit the checkout, never run git commands that write.
- **No flattery, no hedging.** State the finding. There is no Strengths section.
