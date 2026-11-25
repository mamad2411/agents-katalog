# Reviewer Dispatch Template

For iteration reviews (`agents/iteration-reviewer.md`) and the final gate
(`agents/final-reviewer.md`). The role file carries the review protocol —
this dispatch only supplies the inputs, scope, and output contract.

```
Agent (general-purpose):
  description: "Review: [short task name]"
  model: [Iteration reviews: OMIT to inherit the session model; set the
         gate model only when the diff is large, subtle, or
         security-sensitive. Final gate: the gate model — set explicitly
         only when it differs from the session model. Per SKILL.md Roles
         and Models]
  prompt: |
    Read <SKILL_DIR>/agents/[iteration-reviewer.md | final-reviewer.md]
    and adopt that role completely before doing anything else — including
    the coding-standards file it points to, in that same directory.

    Review one task's uncommitted implementation in [repo path].
    There are NO commits to inspect — the diff file below is the complete
    change. Do not run git log; do not expect a branch history.

    ## Inputs

    - Requirements: [SCRATCH]/tasks/task-[N]-brief.md — verify the diff
      against this
    - Implementer's report: [SCRATCH]/tasks/task-[N]-report.md — treat as
      UNVERIFIED claims; verify against the diff. A stated rationale never
      downgrades a finding.
    - Diff: [SCRATCH]/tasks/task-[N]-diff.txt — stat summary and full diff
      with context, covering ONLY this task's changes (earlier approved
      tasks are baked into the diff's base and are not under review). This
      is your view of the change; read files outside it only to check a
      concrete named risk (call sites of a changed signature, etc.), and
      name what you checked.

    [Final review only — replace the three inputs above with: the whole-run
    diff [SCRATCH]/final-diff.txt, ALL task briefs and reports in
    [SCRATCH]/tasks/, and the Minor findings accumulated in the ledger —
    triage which must be fixed before merge: [LIST].]

    ## Scope

    Review ONLY changes in the diff. Tests were run by the implementer — the
    report carries the evidence; do not re-run suites. Missing/unconvincing
    test evidence is itself a finding. Never run PHPStan, PHPCS or PHPMD:
    where the project ships their configs, those rulesets are binding on
    the diff and you enforce them by reading it against them, exactly as
    you enforce every other coding standard.

    Read-only on this checkout: no edits, no git state changes.

    ## Verdicts (both required)

    1. **Spec compliance:** ✅ | ❌ — missing, extra, or misunderstood
       requirements vs the brief, with file:line. ⚠️ for anything you cannot
       verify from the diff alone.
    2. **Code quality:** Approved | Needs fixes — findings as
       🔴 Critical / 🟡 Important / 💬 Minor, each with file:line, what's
       wrong, why it matters.

    Begin your reply directly with the spec verdict. No preamble, no process
    narration.
```

**Controller rules when filling this in:**
- Never tell the reviewer what not to flag or pre-rate a finding's severity.
- Copy binding constraints into the brief, not the dispatch — one source.
- ⚠️ items are yours to resolve: you hold context the reviewer lacks. A
  confirmed gap = failed spec review → fix dispatch → re-review.
- A finding that contradicts what the brief explicitly mandates goes to the
  user — present both, ask which governs.
