---
name: eng-review-and-ship
description: "Execute the review-to-delivery pipeline automatically in one command: structured code review, surgical fixes for critical and warning findings, validation loop until green, atomic conventional commits, resolution of the matching remote repository, and a push executed solely behind an explicit user authorization gate. Use when completed changes need end-to-end review, remediation, verification, and delivery to their corresponding repository."
---

# Review & Ship Lifecycle

Composes `eng-code-review`, `eng-review-fix`, `eng-validate`, `eng-completion-gate`, and `eng-git-commit` into one continuous loop that ends at a verified, authorized push to the repository the working tree belongs to.

Design principles inherited from the lifecycle family:

- **Verdict before push**: the completion gate runs before any remote action, so an unverified state is structurally impossible to deliver.
- **Push requires explicit authorization**: the default outcome is a readiness report; delivery happens solely on user instruction.
- **Target resolution by inspection**: the destination remote and branch come from git metadata, never from assumption; multiple remotes always ask.
- **Convergence by repetition**: the quality gauntlet runs 3 to 5 full passes; a single green pass never ships on its own.

## 8-Stage Pipeline State Machine

```
Convergence Pass p (p = 1 .. 5, minimum 3 passes):
  eng-code-review (scope auto-detection, standard/strict profile)
           │
           ▼
[Gate: open Critical/Warning findings? yes -> Stage 2 in this pass]
           │
           ▼
Stage 2: eng-review-fix (triage Critical -> Warning)
           │
           ▼
Stage 3: eng-validate ──► failures return to Stage 2 (per-pass repair cap: 3)
           │
           ▼
[Convergence Gate: p >= 3 and pass clean -> Stage 4;
 p < 3 -> next pass; p = 5 with open findings -> halt and escalate]
           │
           ▼
Stage 4: Resolution re-review (union of findings from all passes)
           │
           ▼
Stage 5: eng-completion-gate (DONE / DONE-WITH-ACCEPTED-RISKS / BLOCKED)
           │        (BLOCKED halts here; nothing remote has happened)
           ▼
Stage 6: eng-git-commit (atomic conventional commits, hashes recorded)
           │
           ▼
Stage 7: Delivery Target Resolution + readiness report
           │        ───► [Gate: Explicit Push Authorization]
           ▼
Stage 8: Authorized push or PR + consolidated report archive
```

---

## Autonomous Execution Protocol

### Stages 1-4: Convergence Gauntlet (3-5 Passes)

Each pass runs the full review-fix-validate sequence on the current change surface. Passes 1 through 3 are mandatory; the loop converges only on a clean pass at or after pass 3 and hard-caps at pass 5.

1. **Execute `eng-code-review`** with scope auto-detection: uncommitted changes use `diff` scope, staged-only changes use `staged` scope, full audits use `repo` scope. Profile defaults to `standard`; escalate to `strict` for security-sensitive or pre-release surfaces. Archive one report per pass under `.agents/eng-code-reviews/`.
2. **Triage gate**: any Critical or Warning finding proceeds to Stage 2 automatically within the pass. A clean pass at p >= 3 converges; a clean pass at p < 3 starts the next pass, because prior fixes deserve fresh review.
3. **Execute `eng-review-fix`**: minimal convention-following fixes, each backed by a regression test where feasible.
4. **Execute `eng-validate`** after each remediation batch; per-pass repair cap at 3 rounds, then halt the pipeline and hand unresolved items back with evidence.
5. **Re-review the union of findings from all passes**: every finding ends in exactly one state: `Resolved`, `Deferred (human decision required)`, or `Not Reproducible (with evidence)`. Open findings at the 5-pass cap halt delivery before Stage 5.

### Stage 5: Completion Verdict

**Execute `eng-completion-gate`** against the checkable criteria of this skill. A BLOCKED verdict halts the pipeline before Stage 6; no commit or remote action occurs.

### Stage 6: Atomic Commit

**Execute `eng-git-commit`**: staging purity checklist, conventional message format, hook respect. Record every commit hash; hashes become delivery evidence in the final report.

### Stage 7: Delivery Target Resolution

Resolve which repository this tree ships to using tool inspection, never assumption:

1. Inventory the facts: `git remote -v`, `git branch --show-current`, and `git rev-parse --abbrev-ref --symbolic-full-name @{u}` for the upstream mapping.
2. Single remote: it becomes the default target; propose `-u <remote> <branch>` when the branch lacks an upstream.
3. Multiple remotes: present a target table (name, push URL, current tracking) and let the user choose inside the authorization gate. Cross-remote guessing stays outside the contract.
4. Divergence check: compare ahead/behind counts against the upstream. A non-fast-forward target raises a risk flag in the card instead of planning a silent overwrite.

Produce the readiness report and raise the authorization card:

```markdown
## Push Authorization Requested
- Repository: `<remote>` (<push URL>)
- Branch: `<local branch>` -> `<upstream>`
- Commits: N (<hash range>)
- Evidence: verdict <state>, validation green (runs: N), findings closed
- Risk flags: <protected branch / diverged history / none>

Reply PUSH to deliver, PR to open a pull request instead, or HOLD to stop here.
```

### Stage 8: Authorized Delivery & Archive

1. Re-verify state stability: same HEAD, clean status output, unchanged remote table. Any deviation voids the authorization and returns to Stage 7.
2. On PUSH: run exactly the confirmed command sequence. On PR: **execute `eng-git-pr`** for repositories whose contribution model routes through pull requests.
3. Hard blocks standing regardless of authorization: force push to `main`, `master`, `release`, or protected branches, and any push while the verdict is BLOCKED or missing (aligned with `eng-destructive-safety-gate`).
4. Archive the consolidated report at `.agents/review-and-ship/<timestamp>.md`: findings matrix vs final states, fixes applied, validation history, verdict, commit hashes, and the delivery result (`PUSHED` / `PR OPENED` / `HELD`).

---

## State Persistence & Resumption

Record pipeline progress in `.agents/lifecycle-state.json`:

```
{
  "feature": "<review-scope>",
  "pipelineType": "review-and-ship",
  "currentStage": 7,
  "stageName": "delivery-target-resolution",
  "pass": 3,
  "maxPasses": 5,
  "completedStages": [
    "eng-code-review",
    "eng-review-fix",
    "eng-validate",
    "eng-completion-gate",
    "eng-git-commit"
  ],
  "deliveryTarget": { "remote": "origin", "branch": "<branch>", "authorized": false },
  "lastUpdated": "YYYY-MM-DDTHH:mm:ssZ"
}
```

An interrupted run resumes from the last incomplete stage and the interrupted convergence pass. An `"authorized": true` entry still requires the Stage 8 stability re-check before execution.

---

## Checkable Completion Criteria

- [ ] Review reports archived under `.agents/eng-code-reviews/` for every pass.
- [ ] Every finding across all passes Resolved, Deferred with rationale, or disproven with evidence.
- [ ] At least 3 convergence passes completed; the loop exited only on a clean pass or a documented escalation at the 5-pass cap.
- [ ] Validation suite green within the per-pass 3-repair-round cap.
- [ ] Completion verdict recorded before any remote action; BLOCKED never reached delivery.
- [ ] Atomic conventional commits created with hashes recorded.
- [ ] Delivery target resolved via tool inspection; multi-remote choice made by the user.
- [ ] Push commands executed verbatim after explicit authorization on a stable state.
- [ ] Consolidated report saved under `.agents/review-and-ship/` with the final delivery result.
