---
name: superforge-verify
description: >
  Gate that blocks any completion claim until there is empirical runtime
  evidence — the test suite actually run, both mobile and desktop viewports
  checked, and native iOS or Android simulator runs confirmed. Grades every
  piece of evidence (reproducible / observed / derived / asserted) and forbids
  a report that rests on assertion, separates "it worked" from "it happened to
  work" by re-running cold, and names the seven ways evidence gets faked without
  anyone intending to. Use before saying a task is done, fixed, or shipped. Use
  when the user says "is it done", "did it work", "verify", "double check",
  "are you sure", "before we ship", "proof", "確認して", "検証して", "本当に動く",
  "終わった", "動作確認", "証拠", or runs /superforge-verify.
license: MIT
metadata:
  author: Takao Umehara
  version: "3.1"
compatibility: >
  Standalone.
  Requires the project's own build and test commands.
  Writes docs/verification.md.
---

# Superforge Verify — Pre-Completion Verification Gateway

NEVER claim a task is resolved, a bug is fixed, or a feature is complete without gathering empirical runtime proof of success.

---

## 0. Know which grade of evidence you are holding

"Paste the real output" is the right rule and only half a rule, because it does
not say what makes a piece of evidence good. Evidence that looks convincing
while proving nothing is this skill's own failure mode, one level up.

| Grade | What it is |
|---|---|
| **A — reproducible** | A command anyone can re-run, with its output pasted and the command line above it |
| **B — observed** | Something captured once: a screenshot at a stated viewport, a log with timestamps |
| **C — derived** | A conclusion drawn from an A or a B — and it **must name which one** |
| **D — asserted** | Someone says so |

> **A verification report may not contain a single D.**

The quiet failure to watch for is **a C written in the confident tone of an A**.
"Mobile layout verified" is a conclusion; "screenshot at 375px, attached" is
evidence. What makes each grade valid, and the "it worked" versus "it happened
to work" table (cold start is the check most often skipped and the one that
catches the most) → **`references/evidence.md`**.

### Whoever did the work cannot grade it

Grading your own evidence is a conflict of interest no instruction repairs. The
grader has already read the reasoning, already believes the claim, and reads the
output looking for the confirmation it expects — which is precisely how a C gets
written in the tone of an A.

Where Claude Code is available, run **`workflows/superforge-verify-evidence.js`**:
one agent extracts the claims, one runs each proof line and pastes raw output,
and **a separate agent grades that output having never seen the implementation**
and being asked for the reason it does *not* prove the claim. Then a reporter
writes `docs/verification.md` with the mandatory unverified section. Up to
fourteen agents; say *"use a workflow"* or run `/superforge-verify-evidence`.

Everywhere else, do it in one pass — but write the evidence down completely
before grading any of it, and grade only from what is written.

Both paths write `docs/verification.md`, and **`superforge-ship` blocks on that
file**, so the difference has to be a field rather than something a reader
infers: the first line is `Mode: single-pass (grader = implementer)` here, and
`Mode: independent grading (<n> claims, <n> agents)` from the workflow. A reader
who knows the grader wrote the code can discount accordingly; a reader who does
not, cannot.

---

## Verification Requirements Checklist

### 1. Automated Build & Test Pass
- [ ] Complete test suite passes cleanly with 0 failures.
- [ ] 0 TypeScript / Swift / Kotlin compilation errors.
- [ ] 0 Linter warnings.

### 2. Dual-Viewport Web & UX Verification (Web Apps)
- [ ] **Mobile Viewport (< 640px)**: Tap target sizing (≥ 44px), zero horizontal overflow, touch menu responsiveness.
- [ ] **Desktop Viewport (> 1024px)**: Multi-column structure, keyboard navigation (`Tab`/`Enter`), hover states.
- [ ] **Accessibility (a11y)**: run **`superforge-a11y`** and require its verdict. The gate passes only when `docs/accessibility.md` exists, has no Blockers, and has no Level A or AA criterion left `not assessed`. A green automated scan on its own does not clear this box.

### 3. Native Mobile Verification (iOS / Android Apps)
- [ ] **iOS**: Xcode build success, iOS Simulator rendering, Dynamic Type scaling, SF Symbols alignment.
- [ ] **Android**: Gradle assemble success, Android Emulator execution, Material Design 3 Dynamic Color & ripple effects.

---

## Simulated usability pass

Run the three-persona flow check — 初回・急いでいる / 慣れた常用者 /
懐疑的・慎重 — and report the point where each would abandon. Method detail is
in **`skills/superforge-roast/references/evaluation-methods.md`**.

---

## Deeper reference

**`references/evidence.md`** — the four grades and what makes each valid, the
"it worked" versus "it happened to work" table, the seven ways evidence gets
faked unintentionally (a green screenshot of the wrong build, a suite that
passed because the test was skipped, a check that cannot fail, verifying the fix
but not the bug), the extra verification owed by anything carrying someone
else's name on it, and the report template.

---

## Artifact

Write `docs/verification.md`: every check, **its grade**, the exact command run,
and its real output. Paste the output rather than describing it. A verification
report without evidence is an assertion, which is the thing this skill exists
to prevent.

**`## 確認していないこと` is a mandatory section** and may not be empty without a
stated reason. A verification claiming to have checked everything has almost
certainly not enumerated what "everything" was.

It is read by **`superforge-ship`**, which treats it as a precondition — a
missing `docs/verification.md` is a `BLOCK` there — and by
**`superforge-handoff`**, which carries its status forward so the next session
knows what has and has not been proven. Record failures as plainly as passes:
a check that failed and was left failing is exactly what the next reader needs
to see.

## Delegate when a sharper skill is installed

`verification-before-completion` (evidence discipline) · `superforge-a11y`
(the accessibility gate) · `audit`, `optimize` (technical sweep) · `run`
(launching the actual app) · **`superforge-ship`** (the separate question of
whether it may be released — undisclosed data collection, a missing deletion
path, or no rollback will stop a launch that passes every check here).

**"It works" is also not "it is safe."** This skill proves the intended path
runs. Whether a logged-in user can reach data that is not theirs is a different
question with a different method — **`superforge-secure`**, whose
`docs/security.md` is a `superforge-ship` precondition alongside this file's.

**Passing this skill is not permission to ship.** "It works" and "we are
allowed to release it" are different verdicts with different evidence. Hand the
second one to `superforge-ship`.
