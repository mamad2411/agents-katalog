---
name: status-reporting
description: The report format used by program-tracker and product-manager to summarize board state — gate violations first, then the human-approval gate queue with ages, shipped, in-flight, blocked, aging items, and trends, in a neutral factual tone with every claim linked to an issue. Use when producing any scheduled or ad-hoc status report.
---

# Status Reporting

You produce status reports that let a human understand the whole board in one read and know exactly where to intervene. A report is an instrument, not a narrative: neutral, factual, and every claim traceable to an issue. Used by **program-tracker** (board-wide) and **product-manager** (product scope).

## Section order (most urgent first)

Report in this fixed order so a reader can stop as soon as they've seen what needs them:

1. **Gate violations** — always first, always present (even if "none this period"). Query: issues with metadata `gate_violation=true`.
2. **Human-approval gate queue** — what is waiting on a human, and how long. Query: issues with metadata `gate=human-approval` (status `Blocked`).
3. **Shipped** — moved to `Done` since the last report.
4. **In flight** — currently being implemented (`phase=development`), in code review (`phase=code-review`), or in QA (`phase=qa`).
5. **Blocked** — ordinary blocks (status `Blocked` with `blocked_reason`, i.e. no `gate` key) — with reason and who is needed.
6. **Aging items** — anything stalled well beyond the norm for its stage.
7. **Trends** — how the numbers move vs. the last report.

## The format

```
# Status Report — <scope> — <date>

## ⚠ Gate violations (N)
- #123 — dev started with no `adr_approved` / `no_adr_needed` metadata — `gate_violation=true` — needs human resolution.
(or: None this period.)

## Human-approval gate — `gate=human-approval` (N)   ← needs a human decision
- #131 — "Billing DB choice" — waiting 3 days — approver: @owner.
- #140 — "Auth session design" — waiting 6 days — approver: @owner.  ← aging

## Shipped since <last report> (N)
- #118 — "Save default shipping address" — Done, acceptance criteria verified.

## In flight (N)
- Development (`phase=development`): #124 (referral email), #127 (…)
- Code review (`phase=code-review`): #122 (…)
- QA (`phase=qa`): #119 (…)

## Blocked (N)   ← ordinary blocks, `blocked_reason` set (not the gate)
- #129 — needs sandbox creds from platform team (@…) — blocked 2 days.

## Aging (beyond stage norm)
- #140 — at the human-approval gate 6 days.
- #109 — in code review 8 days (norm ~2).

## Trends
- Gate queue (`gate=human-approval`): 2 → 4 (+2). Median wait rising.
- Shipped this period: 3 (prev 5).
- Open blocks: 1 (prev 3).
```

## Rules

- **Gate violations lead, every time.** They are the highest-signal item on the board; a human should see them before anything else. If there are none, say so explicitly — silence is ambiguous.
- **Ages on the gate queue are the point.** For each item carrying `gate=human-approval`, report how long it has waited and who owns the decision. A rising queue or a long wait is the main thing program-tracker exists to surface.
- **Every claim links to an issue.** No "a few things are stuck" — name the issue numbers. A report that can't be drilled into can't be acted on.
- **Neutral, factual tone.** State what is, not blame or spin. "In Review 8 days" — not "the reviewer is too slow." Report the fact; let the human judge.
- **Flag aging explicitly.** Mark items past the normal dwell time for their stage so they don't hide inside healthy counts.
- **Trends over snapshots.** A single number is weak; the direction (better/worse than last report) is what prompts action. Show deltas.

## Cadence

- **Scheduled**: program-tracker posts on a regular cadence (e.g. daily or per working session) so drift is caught early — the schedule is the escalation path for stalled approvals, which agents themselves must never bypass.
- **On-demand**: produce a report whenever a human asks or when a gate violation appears — a violation is worth an out-of-band report rather than waiting for the next scheduled one.
- Keep each report self-contained; a reader should not need the previous one open, though trend deltas reference it.
