---
name: bug-triage
description: Prioritize bugs and review findings by likelihood times severity before touching code. Use whenever you or a review, audit, or scan has found more than one bug or potential issue, when the user asks to find bugs, audit, harden, or "what should we fix first", and whenever you feel the urge to add defensive code for edge cases nobody reported. Rates each bug 1 to 10 for how often it happens and how bad it is, fixes the ones at or above the threshold (default 5), files the rest as issues without changing code, and refuses to design for rare or hypothetical future cases nobody asked about.
license: MIT
metadata:
  category: senior-five
  version: "1.2.0"
---

# Bug Triage

> *Rate each bug from 1 to 10 on how often it would happen and how bad it would be. If the two scores multiplied are below 5, just file it as an issue and leave the code alone. Do not design for rare or future cases nobody asked about.*

Finding bugs is easy; an agent can produce fifty "potential issues" in a minute. The senior skill is deciding which ones deserve code. Every fix has a cost: review time, risk of regression, more code to maintain, and attention taken from the bugs that matter. Triage makes that trade explicit and auditable.

## The rule

```
score = likelihood (1-10) x severity (1-10)

score >= threshold  ->  fix it, highest score first, with a regression test
score <  threshold  ->  file an issue, leave the code alone
```

The default threshold is **5**. Projects tune it. Read `AGENTS.md`, `CLAUDE.md`, or `CONTRIBUTING.md` for a line like `bug-triage threshold: 12`, and use the user's number if they give one.

| Project type | Typical threshold | Why |
|---|---|---|
| Safety-critical, payments, health data | 2 to 4 | Fix nearly everything real |
| Production product | 5 to 10 | The default trade-off |
| Fast-moving startup or prototype | 12 to 20 | Ship; keep a clean backlog |
| Throwaway spike | 30+ | Only fix what blocks the spike |

## Scoring scales

Score on **evidence**. Each score needs a concrete trigger and a code location. If you can't describe a realistic way to trigger the bug, likelihood is 1, so a hypothetical only crosses the default threshold when its consequence would be serious.

**Likelihood**: how often does this happen in real use?

| Score | Meaning |
|---|---|
| 1 | No realistic trigger, or needs a contrived sequence; never seen |
| 2-3 | Rare: unusual input or timing; a few users a year |
| 4-5 | Occasional: a specific but realistic path; some users a month |
| 6-7 | Common: a normal path for some users every week |
| 8-9 | Frequent: most users hit it regularly |
| 10 | Every time, on the main path |

**Severity**: how bad is it, in this product, when it happens?

| Score | Meaning |
|---|---|
| 1 | Cosmetic; nobody notices |
| 2-3 | Annoyance with an obvious workaround |
| 4-5 | Feature degraded or confusing; a workaround exists |
| 6-7 | Feature broken for affected users; no workaround; support tickets |
| 8-9 | Data loss or corruption, wrong money, security exposure, core flow down |
| 10 | Irreversible loss, breach affecting many users, legal or compliance violation |

**Calibration rules**

- Severity is the realistic consequence here, not the worst theoretical one. A crash in an internal admin script is not a 9.
- For security bugs, likelihood means *reachability and attacker motivation*, not accidental frequency. An injectable public endpoint is likely even if no honest user would ever trigger it.
- Bugs that corrupt data are rarely below severity 7, because the damage outlives the fix.
- When two bugs share a root cause, triage the root cause once.

## Don't design for the hypothetical

Below-threshold findings and "what if someday" ideas are where codebases bloat. Don't add:

- Defensive checks for inputs that trusted internal callers can't produce.
- Configuration, plugin points, or abstraction for requirements nobody stated.
- Handling for scale, platforms, or locales the product doesn't support.
- Retry, fallback, or caching layers without an observed failure.

If a hypothetical case matters, someone can file it and argue for it. That is cheaper than code everyone must maintain.

## Process

1. **Collect** every finding with its location, trigger, and consequence. Deduplicate by root cause.
2. **Score** each one with a one-line justification per score.
3. **Sort** by score, then by severity. Anything with **severity 9 or more is listed at the top of your report regardless of score**: a catastrophic failure deserves a human's eyes even when it's rare.
4. **Check what was asked.** If the user asked for fixes ("fix the bugs", "harden this"), continue. If they asked only for a review, audit, or list of bugs, or the code belongs to someone else's PR, stop here: present the triage table and let them choose what to fix.
5. **Fix** at-or-above-threshold bugs in order. Each fix gets a regression test that fails before the fix and passes after (see `test-driven-development`). Group fixes that touch the same code.
6. **File** below-threshold bugs. Search for duplicates first (`gh issue list --search "<keywords>" --state all`). Use one issue per root cause:

   ```bash
   gh issue create --title "<symptom> when <trigger>" --label bug --body "$(cat <<'EOF'
   **What happens:** ...
   **Trigger:** ...
   **Location:** path/to/file.ts:123
   **Triage:** likelihood 2 x severity 2 = 4 (threshold 5), filed, not fixed.
   **Suggested fix:** ...
   EOF
   )"
   ```

   If the user hasn't asked you to file issues in this tracker, or `gh` isn't authenticated, or there's no remote, write the issues into the report instead and offer to file them. Creating issues is visible to other people.
7. **Report.**

## Report format

```markdown
## Triage: 9 findings, threshold 5

| # | Bug | Where | L | S | Score | Decision |
|---|-----|-------|---|---|-------|----------|
| 1 | Refund applied twice on retry | billing/refund.ts:88 | 4 | 9 | 36 | Fixed + test |
| 2 | Upload stuck at 100% on slow networks | upload/index.ts:140 | 6 | 5 | 30 | Fixed + test |
| 3 | Tooltip clipped on 320px screens | ui/Tooltip.tsx:22 | 2 | 2 | 4 | Issue #142 |

**Severity 9 or more:** #1 (fixed).
**Fixed:** 2 bugs, 2 regression tests, full suite green.
**Filed:** 7 issues, linked above.
**Not acted on:** none.
```
