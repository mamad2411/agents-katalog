---
name: fix-it-now
description: "Use the moment a real bug is found during an audit, review, test wave, or unrelated work, and the temptation is to document it and move on. Confirmed bugs get fixed in the current pass; a deferral must be explicit and accepted by the user, never a buried TODO. Also covers half-finished features: finish them or remove them."
---

# Fix It Now

## The failure mode this fixes

An audit runs, finds six real defects, and produces a beautiful document listing them. The document gets filed. The defects stay. Three weeks later one of them detonates in front of a customer, and the worst part isn't the bug — it's that the system *knew*. "You found the bug and documented it but didn't fix it?" is the angriest sentence in code review, and it's earned.

Agents drift into bug-documentation mode because finding feels like finishing: the analysis was the hard part, the writeup is the artifact, surely fixing is "a separate task." But a confirmed bug with a known root cause is the *cheapest it will ever be to fix* — the context is loaded, the repro is fresh, the fix is usually small. Deferring it throws that context away and converts a ten-minute fix into a future debugging session.

The sibling failure: the half-kept feature. Something gets built to 80%, has known gaps, and stays in the codebase as a "mostly works" zombie — too present to ignore, too broken to trust.

## When to Use This Skill

- An audit, review, or test wave just produced confirmed findings
- You found a bug while working on something else and the instinct is "note it and stay on task"
- A report you're writing contains "known issue," "TODO," or "should be fixed later"
- A feature exists in a permanently-partial state — kept, but with gaps everyone routes around
- The user asks "did you fix it or just document it?"

**Don't use when:** the "bug" is unconfirmed (a hunch needs verification before it earns a fix), the fix requires a product decision that genuinely belongs to the user, or you're mid-critical-path and a context switch would endanger the primary task — in those cases, defer *explicitly* (see step 3), don't just skip the skill.

## Instructions

### 1. Confirm it's real, then treat the fix as part of the find

A finding's lifecycle is find → confirm → fix → verify, in one pass. The deliverable of an audit is not a list of bugs; it's a list of bugs *that no longer exist*, plus the residue that genuinely couldn't be fixed and why. Budget audits accordingly: an audit you only have time to half-fix is an audit you should scope smaller.

### 2. Fix in root-cause order, not discovery order

When a pass produces multiple findings, fix the ones that might be causing the others first. Re-test after each — some findings are shadows of the same defect, and the list often shrinks as you go.

### 3. If you must defer, defer loudly and get it accepted

A legitimate deferral (needs user decision, out of scope, blocked on external data) is a *negotiation*, not a footnote. State it directly: what the bug is, why it can't be fixed now, what it will cost to fix later, and what risk it carries until then — and get an explicit "okay, defer it" from the user. A TODO comment is not a deferral; it's a hiding place.

### 4. Apply the keep-it-or-kill-it rule to half-done features

Anything that stays in the codebase gets held to the codebase's standard. If a feature is kept, its known gaps are bugs — fix them now (this skill). If it's not worth finishing, remove it cleanly rather than leaving a zombie. "We'll finish it someday" is a decision to keep it broken; make that decision visible and let the user make it.

### 5. Verify the fix landed wired-in, not in isolation

A fix verified only in a unit harness can still be dead in the integrated path. Confirm the fix in the context where the bug actually bit — the full suite, the real pipeline, the rendered page.

## Output format

```
Findings from <pass>: <N confirmed>
Fixed now: <list — each with root cause and verification>
Deferred (explicitly accepted): <list — reason, cost-of-delay, user sign-off | none>
Keep-or-kill calls: <half-done features surfaced, with recommendation>
Net state: <what is now true that wasn't — not what is now documented>
```

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| Audit theater | a findings document as the end product, with zero diffs attached. |
| The buried TODO | deferral by comment, where no one with authority ever saw the decision. |
| "Tracked in backlog" | moving a live, confirmed, cheap-to-fix-now bug into a queue where context goes to die. |
| The zombie feature | permanently 80% done, exempted from quality standards by being perpetually "in progress." |
| Fixing without verifying wired-in | the patch is in the file; the bug is still in the product. |

## Mental Model

> A documented bug is a bug with better PR. The moment of discovery is the cheapest fix you will ever be offered — every deferral after that is buying the same fix at a markup.
