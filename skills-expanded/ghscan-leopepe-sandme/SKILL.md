---
name: review-standards
description: Use when the user runs /review-standards, or asks whether the current change — working tree, branch commits, or open PR — complies with this repository's docs/guidelines (simplicity, spec-driven development, traceability to docs/specs).
---

# Review Standards

Audit **the current change** against **every guideline in `docs/guidelines/`**. Report; do not fix.

The guidelines are the only source of authority. A finding that cannot quote a line from a
guideline file is not a finding — delete it.

## Not this skill's job

| Question | Skill that owns it |
| --- | --- |
| Does the change contradict an ADR, sit in the wrong module, or box the codebase in? | `architecture-review` |
| Is a requirement in `docs/specs/` implemented, or do two specs conflict? | `spec-review` |
| Does it miss an `NFR-` budget, block the runtime, cost startup time? | `performance-review` — it measures; this skill only checks the rule is followed |
| Does the code simply not work — wrong output, wrong format, a crash? | No review skill owns runtime correctness. List it under `Defects noticed` at the end of the report, one line each, ungraded |

Those three cite §1 and §2 below for the gate and the scope; both are canonical here. Keep them
in step.

## 1. Check the gate first

The change MUST pass the quality gate in `docs/guidelines/code/quality-gates.md` before it is
reviewed. Run all five, in order, and **read the output — exit status is not the pass criterion**:

| Order | Command | Passes when |
| --- | --- | --- |
| 1 | `cargo fmt --check` | Exits `0` with no diff |
| 2 | `cargo clippy --all-targets` | **No warning printed.** Clippy exits `0` while printing warnings — the status lies; count the warnings |
| 3 | `cargo build` | Compiles with **no warning printed** — same trap as clippy |
| 4 | `cargo test` | Every test passes **and at least one test ran** |
| 5 | `cargo doc --no-deps` | No warnings — `quality-gates.md` §2 requires this too |

`cargo test` reporting `0 passed; 0 failed` is a **vacuous pass**: nothing was verified. It does
not stop the review, but the report says `N tests ran` — never "all green" — and the empty suite
is itself a finding under `docs/guidelines/tests/testing.md`.

If any of the five fails, **stop**. Do not review. Report only the gate failure, with the command
and its output, and say the review will run once it passes. An unformatted, unlinted,
non-compiling or red change wastes the review — the findings would be noise from the failure, not
the design.

**Stopping means stopping.** The report contains the gate output, the fix, and nothing else:

- No preview of what you expect to find, however hedged.
- No "two things worth knowing before you re-run it".
- No naming a rule, file or finding-in-waiting you would have graded, even labelled ungraded.

A partial review under a red gate is the worst of both: the reader treats it as the review, and
the code moves under `cargo fmt` before it is finished. Say the gate is red, say what to run, stop.

Skip this step only when the change touches no code (documentation, specs, ADRs).

## 2. Resolve the scope

Take the first case that holds, and state which one you used in the report:

| Condition | Diff to review |
| --- | --- |
| `gh pr view --json baseRefName` succeeds | `git diff $(git merge-base origin/<baseRef> HEAD)...HEAD` plus uncommitted changes |
| Branch ≠ `main` and `main` exists | `git diff $(git merge-base main HEAD)...HEAD` plus uncommitted changes |
| Repo has commits, branch is `main` | `git diff HEAD` + `git diff --cached` + untracked files |
| Repo has no commits | every tracked and untracked file (`git status --short`) |

"Uncommitted changes" always means staged + unstaged + untracked. Untracked files are part of
the change; `git diff` does not show them — list them with `git status --short` and read them.

Review only lines the change touches, plus whatever you must read to judge them. Pre-existing
code outside the diff is out of scope; if it blocks a verdict, say so instead of reviewing it.

## 3. Load the guidelines

`find docs/guidelines -name '*.md'` and read **all** of them. Do not work from memory or from
this file's examples — the directory grows, and a skipped file is an unreviewed dimension.
Extract each rule verbatim; you will quote it.

Also read `AGENTS.md`, `docs/AGENTS.md`, and — when the change is code — the spec in
`docs/specs/` that governs it. Those give the context a rule needs to be applied correctly, but
only `docs/guidelines/` produces findings.

## 4. Grade each rule

- **Blocker** — violates a `MUST` / `MUST NOT`, or a rule stated as an absolute.
- **Advisory** — violates a `SHOULD`, or a preference.
- **Not assessable** — the rule has no measurable threshold (e.g. simplicity.md's "3 page
  scrolls", flagged `# todo` in the file itself). Say the rule is unmeasurable and describe what
  you observed. MUST NOT invent a threshold to convict or acquit against.
- **Pass** — checked, no violation. Name what you checked.
- **N/A** — the change contains nothing the rule can apply to. Say why.

Every guideline file gets a verdict row, including the ones that pass.

## 5. Report

Emit exactly these sections, in this order:

```markdown
## Standards review

**Gate:** fmt ✓ · clippy ✓ 0 warnings · build ✓ 0 warnings · test ✓ <N> tests ran · doc ✓
**Scope:** <scope case from §2> — <N files, +A/-B lines>
**Guidelines applied:** <every file read from docs/guidelines/>

### Verdicts
| Guideline | Rule | Verdict | Finding |
| --- | --- | --- | --- |
| code/simplicity.md | one purpose per unit | Blocker | F1 |
| sdd/spec-driven-development.md | §6 traceability | Pass | — |

### Findings
#### F1 — <one line> · `src/path.rs:42-58` · <guideline file>
**Rule:** "<verbatim quote from the guideline>"
**Evidence:** <what the code at that location actually does>
**Fix:** <the specific change that clears it>

### Traceability
| Changed file | Requirement ID | Verified by | Status |
| --- | --- | --- | --- |
| src/config.rs | FR-007 | tests::loads_user_config | Covered |
| src/probe.rs | — | — | Unspecified |

### Defects noticed
<behaviour bugs seen while reviewing — `path:line`, one line each, ungraded. "None" if none.>

### Result
<Blockers: N · Advisories: N> — <one sentence: mergeable, or what must change first>
```

Fill the Traceability table from the governing spec's Verification table and Implementation
tasks. A changed source file with no requirement ID is a row reading `Unspecified`, not an
omitted row — under `docs/guidelines/sdd/spec-driven-development.md` §8 that is itself a finding
unless the change qualifies for the fast path (§9).

## 6. Stop

Report only. Do not edit code, specs, or the guidelines. If the user then asks for fixes, apply
them one finding at a time, citing the finding ID. After the last fix, run the gate again (§1)
before saying the change is clean.

## Red flags

| If you catch yourself... | Do this instead |
| --- | --- |
| Writing "could be cleaner" / "consider refactoring" | Quote the rule and give the concrete edit, or drop it |
| Citing a rule you remember | Open the file, copy the line, cite `path:line` |
| Reviewing code the diff does not touch | Cut it — or state it as blocking context, not a finding |
| Skipping the Traceability table because there is no spec | Fill it with `Unspecified` rows and judge against §9 |
| Reporting zero findings with no verdict rows | Every guideline file gets a row, including passes |
| Picking a number for an unmeasurable rule | Verdict is Not assessable; describe what you saw |
| Starting to fix what you found | Report first. Fixes are a separate, requested step |
| Reviewing before running the gate | Stop. Report the gate failure; the review runs after it passes |
| Assuming the gate passes because the change "looks fine" | Run all five commands and read the output |
| Reading `exit 0` from clippy or build as a pass | Both exit `0` while printing warnings. Count the warnings, not the status |
| Writing "gate: all green" when `cargo test` ran 0 tests | Report the count. A vacuous suite verified nothing, and the gap is a finding |
| Adding "worth knowing before you re-run it" to a gate-failure report | That is the review, hedged. Report the gate and stop — §1 |
