---
name: bug-report-standards
description: How to file a bug that a developer can act on immediately — the exact board bug template, the urgent/high/low priority rubric, reproduce-twice discipline, mandatory evidence, one-bug-per-issue, dedupe-first, and a neutral factual tone. Use whenever QA, a reviewer, or an auditor files a bug.
---

# Bug Report Standards

A bug report is a work order for a developer, not a note to yourself. The bar is: someone who has never seen the problem can reproduce it from your report alone, know how bad it is, and start fixing without asking you a single question. Reports that miss that bar bounce back and cost a full round-trip.

## Before you file

1. **Reproduce it twice.** A failure you saw once and cannot repeat is not yet a bug report — it's an observation. Reproduce it a second time from clean state, noting the exact steps that trigger it. If it won't reproduce, keep it as a comment/spike, not a bug.
2. **Minimize the repro.** Strip every step that isn't required to trigger it. Five tight steps beat twenty incidental ones.
3. **Search for duplicates first.** Search the board (open and recently closed) before filing. If it exists, add your evidence as a comment on the existing issue instead of creating a duplicate. Duplicates fragment the fix and waste triage.
4. **One bug per issue.** If you found three problems, file three issues. Bundled bugs get partially fixed and half-closed.

## The template (use verbatim)

File the issue with exactly the board bug template:

```
## Summary
## Steps to reproduce
## Expected / Actual
## Environment & evidence (logs, screenshots)
Priority: urgent | high | low
```

- **Summary** — one line: what's broken and where. "Checkout: applying a valid coupon returns 500" — not "checkout broken".
- **Steps to reproduce** — numbered, deterministic, from a known starting state. Include the exact input/data used.
- **Expected / Actual** — expected quotes the acceptance criterion or documented contract where one exists; actual states what happened, observably.
- **Environment & evidence** — see below. **Mandatory.**
- **Priority** — from the rubric below.

Also set metadata **`type=bug`**, the matching **priority** (`urgent`/`high`/`low`), the relevant **`stack`** routing (`stack=mobile-react-native`, `stack=backend-nestjs`, …), and **link the originating issue/PR** the bug was found against.

## Evidence is mandatory

No evidence, not a valid report. Attach whatever proves it:

- **Logs** — the actual error and stack trace, not "it errored".
- **Screenshots / screen recording** — for any UI bug; a recording for anything involving a sequence or timing.
- **Request/response capture** — for API bugs, the exact request (method, path, headers sans secrets, body) and the full response (status + body).
- **Environment** — app version / commit SHA, browser+version or device+OS, environment (local/staging/prod), user role, feature flags.

## Priority rubric

Assign against user/business impact, not how annoyed you are:

**`urgent`** — data loss or corruption; a security hole; a **critical flow blocked** (checkout, auth, payments) with no workaround; a crash on a common path. Ship-stopper. Blocks `Done` (Definition of Done forbids open `urgent`).
> e.g. Payment charges the card but the order isn't created. Any user can read another user's data. App crashes on cold start for all Android users.

**`high`** — a feature is broken but a **workaround exists**, or it hits a meaningful subset of users/inputs. Serious, not a full stopper. Also blocks `Done`.
> e.g. Coupon codes fail, but users can still check out at full price. Export works on desktop but not tablet. Search misses results with apostrophes.

**`low`** — cosmetic, or an edge case with negligible impact. Should be fixed, doesn't block release.
> e.g. Button 2px misaligned. Tooltip typo. Error copy slightly off on an unlikely input.

When genuinely between two levels, pick the higher and say why in the report.

## Tone — neutral and factual

State what happened and what was expected. No blame ("dev clearly didn't test"), no hedging ("might sometimes maybe"), no drama ("totally broken, disaster"). The report describes system behavior, not people. A calm, specific report gets fixed faster than an alarmed vague one.

## Anti-patterns

- Filing after seeing it once, never confirming.
- "Doesn't work" with no steps, no evidence.
- Several bugs crammed into one issue.
- A new issue for something already filed.
- Priority inflated to force attention, or deflated to avoid blocking a release.
- Missing environment (which version? which device?) so the dev can't reproduce.
- Editorializing about who's at fault.

## Final step

Post the issue with the template filled, metadata set, evidence attached, and the originating issue/PR linked. Set status to `Backlog` (or per your team's triage flow) and, for `urgent`/`high` found during QA of an in-flight issue, comment on that issue so it cannot reach `Done` with the bug open.
