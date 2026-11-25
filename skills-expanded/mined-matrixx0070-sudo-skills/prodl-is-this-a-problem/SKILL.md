---
name: prodl-is-this-a-problem
version: 1.0.0
description: Give a fast, structured triage verdict on whether a product or marketing question raises a real legal concern and what to do next.
author: matrixx0070
tags: [product-legal, triage, spot-check, verdict, escalation, fast]
capabilities: []
---

## When to use
Use this when someone asks "is this okay to ship?" and needs a quick, reasoned answer — not a full review. It sorts a question into clear / caution / stop and points to the right next step. It is the front door: cheap to run, honest about its limits.

**Not for:** the final sign-off (use `prodl-launch-review`), sizing a specific risk (use `prodl-feature-risk-assessment`), or vetting claims in detail (use `prodl-marketing-claims-review`). When triage says "caution" or "stop", hand off to those.

## Method
1. **Restate the question as one testable thing.** "Can we say X?" or "Can we ship feature Y?"
2. **Find the legal hook.** Is any regime plausibly in play — claims, privacy, consumer protection, IP, sector rules? If none, likely clear.
3. **Check for the obvious tripwires.** Superlatives without proof, health/financial claims, minors' data, pre-checked consent, comparisons, "free" with strings.
4. **Assign a verdict.** Clear (no concern found) / Caution (real issue, needs deeper review) / Stop (likely unlawful as-is).
5. **State the reason in one line.** Tie the verdict to the specific hook.
6. **Route the next step.** Name the skill or the person (counsel) who takes it from here.

## Example
Question: "Can we call our supplement 'FDA-approved'?" Legal hook: FTC/FDA claim rules. Tripwire: dietary supplements are not FDA-approved. Verdict: Stop — the claim is false and creates direct enforcement exposure. Next step: drop the phrase; if a compliant alternative is wanted, route to `prodl-marketing-claims-review` and counsel.

## Pitfalls
- **Turning triage into a full review.** If it needs analysis, escalate — don't improvise a verdict.
- **False "clear".** No hook found in five minutes is not proof of safety; say "no concern found", not "safe".
- **Skipping the reason.** A verdict without its hook can't be trusted or challenged.
- **Over-escalating everything.** Triage that stops every question is noise; reserve stop/caution for real hooks.

## Output format
```
Question (testable):
Legal hook:
Tripwires found:
Verdict: Clear | Caution | Stop
Reason (one line):
Next step: <skill or counsel>
```

## Reference
**FTC substantiation.** The commonest tripwire: an objective claim with no reasonable basis on file. If the answer to "do we have proof?" is no, the verdict is at least Caution. Health, safety, and efficacy claims demand competent, reliable scientific evidence.

**Launch-risk rubric.** Verdict maps to risk: Clear = proceed; Caution = hold pending review; Stop = do not ship as-is. Any minors, health, or financial angle raises the floor to at least Caution regardless of the surface question.

**When to escalate to counsel.** Every Stop, and any Caution touching regulated categories, goes to an attorney. This skill is issue-spotting under time pressure, not legal advice; a "Clear" verdict is the absence of a spotted problem, not a legal opinion.
