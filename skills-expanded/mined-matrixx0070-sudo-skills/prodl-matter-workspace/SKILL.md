---
name: prodl-matter-workspace
version: 1.0.0
description: Set up and maintain a single organized workspace for one launch-review matter, tracking facts, findings, conditions, and the escalation trail.
author: matrixx0070
tags: [product-legal, matter, workspace, tracking, organization, audit-trail]
capabilities: []
---

## When to use
Use this to open and run the file for one matter — a specific launch, feature, or campaign under review — so every intake fact, finding, condition, and counsel decision lives in one place. It is the connective tissue: the other product-legal skills read from and write to this workspace, and it becomes the audit trail if a decision is later questioned.

**Not for:** company-wide configuration (use `prodl-customize`), producing the actual verdict (use `prodl-launch-review`), or spotting issues (use `prodl-is-this-a-problem`).

## Method
1. **Open the matter.** Assign a name, owner, go-live date, and the `prodl-customize` profile it runs under.
2. **Seat the intake.** Drop in the `prodl-cold-start-interview` record as the fact base.
3. **Register findings.** Each finding from a feature or claims review lands here with its tier, owner, and status.
4. **Track conditions to closure.** Every go-with-conditions item is open until its owner marks it done with evidence.
5. **Log the escalation trail.** Record what went to counsel, when, and the disposition — the paper trail.
6. **Hold the verdict and its basis.** The final go/no-go plus the findings that drove it.
7. **Set the review trigger and archive.** On go-live, snapshot the state; on the trigger event, reopen.

## Example
Matter "Q3 Sleep-App Launch" opens with the intake fact sheet, then accumulates: a claims finding (unsubstantiated "2x faster", Unlawful, owner Marketing, open), a data finding (undisclosed SDK, High, owner Legal Ops, closed with updated policy), and a counsel note approving revised copy. Verdict recorded: Go-with-conditions. Two weeks post-launch a new claim is added — the matter reopens per its review trigger instead of starting cold.

## Pitfalls
- **Scattering the record.** Findings in Slack, conditions in a doc, counsel notes in email means no trail — keep one workspace.
- **Closing conditions without evidence.** "Done" needs the artifact (updated copy, study, disclosure), not a checkbox.
- **No escalation log.** If you can't show what counsel saw, you can't show the decision was informed.
- **Never archiving.** An open matter with a shipped launch rots; snapshot at go-live.

## Output format
```
Matter: <name> — owner — go-live — profile
Intake: <linked fact sheet>
Findings:
  - <issue> — tier — owner — status (open/closed) — evidence
Conditions outstanding:
Escalation log: <date — item — counsel — disposition>
Verdict + basis:
Review trigger / archive state:
```

## Reference
**FTC substantiation.** The workspace is where substantiation lives: for each objective claim, store the evidence (or its absence) on the record. "Reasonable basis before dissemination" is auditable only if the proof is filed against the claim it supports.

**Launch-risk rubric.** The matter's overall status = worst open finding. Any open Critical keeps the matter at No-go; the workspace should surface that at a glance rather than burying it in a list.

**When to escalate to counsel.** The workspace does not decide — it records. It routes every Critical, Severity-5, and regulated-category finding to the escalation log for an attorney, and holds counsel's disposition. This skill is organization and audit trail, not legal advice; the escalation trail exists precisely because an attorney, not this workspace, owns the calls on flagged items.
