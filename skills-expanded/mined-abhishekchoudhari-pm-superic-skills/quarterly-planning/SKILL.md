---
name: quarterly-planning
description: "Run an adaptive quarterly planning session that calibrates to the user's level. Use when someone asks to do quarterly planning, Q-planning, build a QBR, set quarterly goals, align on roadmap for the quarter, run a planning cycle, or prepare a board-ready quarterly review. Detects whether the user is an IC/team PM (team-level OKRs + roadmap alignment), a VP/CPO (P&L + strategic resourcing + cross-functional alignment), or preparing a QBR for CEO/board (financial narrative + strategic priorities + decisions needed). Always ask for level first if not provided. Commands: /quarterly-planning, /plan-quarter, /qbr"
---

# Quarterly Planning — Adaptive by Level

This skill runs a complete quarterly planning session. The output, depth, and
framing adapt entirely to the user's seniority and audience. Same rigour.
Different altitude.

Read the full file before producing anything.

---

## Step 1 — Detect Level

**Before doing any planning work, ask:**

> "Before we start — are you planning as an IC/team PM, as a VP or CPO, or
> are you building a QBR for your CEO or board?"

If the user has already stated their level, skip the question and proceed.

Map their answer to one of three modes:

| Answer | Mode |
|---|---|
| IC, PM, team lead, team-level planning | **MODE A — Team** |
| VP, CPO, Head of Product, director-level | **MODE B — VP/CPO** |
| QBR, board, CEO review, investor update | **MODE C — QBR** |

---

## MODE A — Team-Level Planning (IC / PM)

**Context:** The user is a PM or team lead planning for their squad or product
area. Output is internal. Audience is their manager, adjacent teams, and
engineering partners.

**Gather these inputs:**

1. What product area / feature domain are you responsible for?
2. What did last quarter deliver? Key wins and misses.
3. What are the company or org-level OKRs this quarter?
4. What are your biggest constraints (engineering capacity, dependencies,
   data gaps)?
5. What are the 2–3 biggest bets you want to make this quarter?

**Produce this output:**

### A1 — Last Quarter Snapshot (3–4 bullets max)

Format:
- Win: [metric moved] — [what drove it]
- Miss: [metric missed] — [root cause, one line]
- Learning: [what changes this quarter as a result]

### A2 — This Quarter's OKRs

Structure:
```
Objective: [one crisp outcome sentence]
  KR1: [metric] from [baseline] → [target] by [date]
  KR2: [metric] from [baseline] → [target] by [date]
  KR3: [metric] from [baseline] → [target] by [date]
```

Maximum 2 objectives. Maximum 3 KRs each. If the user gives you more, push
back and force prioritisation.

Use placeholder baselines (e.g. "[insert current value]") wherever the user
hasn't provided data — never fabricate numbers.

### A3 — Roadmap by Priority Tier

Use a simple three-tier structure:

**Must ship (P0):** Directly drives KRs. Non-negotiable this quarter.
**Should ship (P1):** High value, ships if P0 stays on track.
**Explore (P2):** Discovery only — no commitment to ship.

For each item: Name | Owner | Effort estimate | KR it drives

### A4 — Risks and Dependencies

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|

### A5 — Decisions Needed Before Planning Lock

List the 2–3 decisions that must be made by [planning lock date] for this plan
to be executable. Format as: "Decision needed: [topic]. Owner: [person].
Deadline: [date]."

---

## MODE B — VP / CPO Level Planning

**Context:** The user is operating at VP or CPO scope. Output drives
cross-functional alignment, resourcing decisions, and P&L accountability.
Audience is the leadership team and CEO.

**Gather these inputs:**

1. What are the company's top 3 strategic priorities this quarter?
2. What is your P&L ownership — what revenue / cost lines do you control?
3. What did last quarter's scorecard look like vs plan? (High level is fine.)
4. What are you doubling down on vs pulling back from this quarter?
5. What resourcing or budget decisions are you making or requesting?
6. What are your top 2–3 cross-functional dependencies (Eng, Data, Marketing,
   Finance)?

**Produce this output:**

### B1 — Strategic Context (2–3 sentences)

Why this quarter matters. What the macro or competitive environment demands.
What the business cannot afford to get wrong.

### B2 — Last Quarter P&L and Product Scorecard

| Metric | Target | Actual | Delta | Commentary |
|---|---|---|---|---|

Use "[insert]" placeholders where data isn't provided.

### B3 — This Quarter's Strategic Bets

Maximum 3 bets. For each:

**Bet name:** [short label]
**Thesis:** [one sentence — why this wins]
**Investment:** [headcount, budget, or focus time required]
**Expected outcome:** [metric move, by when]
**If this fails:** [what's the kill signal and by when do we call it]

### B4 — Portfolio Allocation

Show where product and engineering capacity is going:

| Initiative | Capacity % | Category | Strategic Fit |
|---|---|---|---|

Categories: Growth / Retention / Monetisation / Infrastructure / Compliance

### B5 — Cross-Functional Commitments

| Dependency | Team | What you need | By when | Risk if delayed |
|---|---|---|---|---|

### B6 — Decisions for Leadership Alignment

Frame these as decision-ready statements, not discussion topics:

"Recommendation: [specific action]. If approved, outcome is [X]. If not
approved, consequence is [Y]. Decision needed by [date]."

### B7 — Leading and Lagging KPIs

| Metric | Baseline | Q-Target | Owner | Review Cadence |
|---|---|---|---|---|

Separate leading indicators (weekly signal) from lagging outcomes (end of
quarter).

---

## MODE C — QBR for CEO / Board

**Context:** The user is preparing a formal Quarterly Business Review for the
CEO, board, or investor audience. Output is presentation-ready. Narrative
matters as much as numbers. Every slide must answer "so what."

**Gather these inputs:**

1. Who is the audience — CEO only, full board, investors, or mixed?
2. What is the single most important thing you want them to leave believing?
3. What was last quarter's headline story — growth, challenge, or pivot?
4. What are the 3 metrics the board tracks most closely?
5. What decisions or resources are you asking them to approve?
6. Are there any elephants in the room — misses, risks, or headcount changes
   that must be addressed proactively?

**Produce this output:**

### C1 — Executive Narrative (The Spine)

Write a 3-paragraph narrative that any board member can read in 60 seconds:

Para 1 — Last quarter in context: What we said we'd do, what happened, and
why the delta matters or doesn't.

Para 2 — Where we are now: The strategic position, what's working, what needs
to change.

Para 3 — This quarter's commitments: The 2–3 things we will deliver and what
success looks like in numbers.

This narrative is the skeleton. Every slide should be traceable to it.

### C2 — Board Scorecard

| Metric | Q-1 Actual | Q Target | Q Actual | vs Plan | Trend |
|---|---|---|---|---|---|

Green / Amber / Red rating for each. One line of commentary on any Red.

### C3 — Strategic Priority Deep Dives (max 3)

For each priority:

**Priority:** [name]
**Status:** [Green / Amber / Red]
**Progress this quarter:** [what moved, in numbers]
**What's working:** [one sentence]
**What's not:** [one sentence — own it, don't bury it]
**Next quarter plan:** [specific commitment]

### C4 — Decisions and Asks

This is the highest-value slide in the QBR. Make it surgical.

For each ask:
- **Ask:** [specific decision or resource]
- **Why now:** [urgency framing]
- **Options considered:** [2–3 alternatives, briefly]
- **Recommendation:** [your preferred option]
- **Impact if approved:** [metric or outcome]
- **Impact if deferred:** [cost of delay]

### C5 — Risk Register (Board-Visible)

| Risk | Probability | Impact | Mitigation | Owner |
|---|---|---|---|---|

Only include risks that are board-relevant — material to revenue, regulatory,
or strategic direction. Don't pad.

### C6 — Next Quarter Commitments

Three statements, each in this format:

"By end of [month], we will [specific outcome] as measured by [metric], owned
by [name]."

No more than three. If you give more, the board stops believing them.

---

## Universal Quality Rules (All Modes)

**Numbers over words.** "+40% net deposits QoQ" not "strong deposit growth."

**Own the misses.** Never bury a miss in passive voice. "We missed activation
by 8 points because onboarding latency spiked post-migration" is better than
"activation was below target."

**Decisions, not discussions.** Every planning output should end with a clear
list of what needs to be decided, by whom, and by when.

**Placeholders over fabrication.** If the user hasn't provided a metric, use
"[insert current value]" — never invent a number.

**Suggest next commands.** After completing the plan, offer:
- `/pre-mortem` — to stress test the plan before lock
- `/stakeholder-update` — to draft the communication to leadership
- `/write-prd` — to kick off execution on the top P0 initiative

---

## Examples

**MODE A trigger:**
"Help me do quarterly planning for my payments team — I'm a PM."

**MODE B trigger:**
"I need to run VP-level Q2 planning. I own the credit card P&L."

**MODE C trigger:**
"Help me build a QBR deck for our board meeting next Friday."

**Ambiguous trigger (ask):**
"Can we do quarterly planning?"
→ Respond: "Happy to — are you planning as a team PM, as a VP/CPO, or
building a QBR for your CEO or board?"
