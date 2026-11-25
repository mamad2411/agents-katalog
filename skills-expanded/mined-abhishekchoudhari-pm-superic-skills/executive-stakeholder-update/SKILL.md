---
name: executive-stakeholder-update
description: "Draft a structured stakeholder update — weekly, monthly, or milestone-based — calibrated to the user's seniority and audience. Use when someone asks to write a stakeholder update, status update, leadership update, weekly update, exec update, board update, or 'update for my CEO/manager/team'. Detects whether the user is an IC/PM writing to their manager, a VP/CPO writing to CEO or leadership team, or anyone writing a board-level update. Always asks for level and update type if not stated. Different from stakeholder-map (which maps the landscape). This skill produces the actual communication artifact. Commands: /stakeholder-update, /write-update, /exec-update"
---

# Executive Stakeholder Update — Adaptive by Level

This skill drafts the actual update artifact — the document, message, or
slide that goes to leadership. It is not about mapping stakeholders. It is
about communicating to them, clearly and at the right altitude.

Read the full file before producing anything.

---

## Step 1 — Detect Level and Update Type

**If the user hasn't specified, ask:**

> "Quick context before I draft — are you writing as an IC/PM to your manager,
> as a VP/CPO to your CEO or leadership team, or is this a board-level update?
> And is this weekly, monthly, or milestone-triggered?"

Map to a mode:

| Seniority | Audience | Update Cadence | Mode |
|---|---|---|---|
| IC / PM | Manager, squad lead | Weekly / sprint | **MODE A — Team** |
| VP / CPO | CEO, leadership team | Weekly / monthly | **MODE B — Leadership** |
| VP / CPO / CEO | Board, investors | Monthly / quarterly | **MODE C — Board** |

---

## Step 2 — Gather Inputs

Ask only what's missing. Don't ask for things already stated.

**For all modes:**
1. What period does this update cover?
2. What were the 2–3 headline things that happened?
3. What's blocked or at risk right now?
4. What decisions or support do you need from the reader?

**Additional for MODE B and C:**
5. What are the key metrics the audience tracks? What moved?
6. Is there anything sensitive — a miss, a team change, a budget issue — that
   must be addressed rather than avoided?

---

## MODE A — Team / Manager Update (IC / PM)

**Format:** Structured message or short doc. Tone: direct, transparent, no
spin. Under 400 words. Easy to scan in 2 minutes.

**Template:**

---

**[Product Area] — [Week / Sprint / Period] Update**

**Period:** [dates]

**TL;DR:** [One sentence — the single most important thing this period]

**What shipped:**
- [Initiative]: [outcome in numbers if possible]
- [Initiative]: [outcome in numbers if possible]

**What's in progress:**
- [Initiative]: [status, expected completion, any blockers]

**Blockers and risks:**
- [Blocker]: [what it is, who owns the unblock, by when]

**Metrics pulse:**
| Metric | Last week | This week | Target | Status |
|---|---|---|---|---|

**Decisions I need:**
- [Decision topic]: [context in one sentence, what you need from them]

**Next week focus:**
- [Priority 1]
- [Priority 2]

---

**Tone rules for MODE A:**
- Write to a manager who skims first and reads detail only when flagged
- Be specific about blockers — vague "there are some delays" is not useful
- Flag risks before they become escalations — early warning is a leadership signal
- Keep metrics honest — if a number is missing, say "[data pending]" not silence

---

## MODE B — VP / CPO to CEO / Leadership Team

**Format:** Structured doc or async message. Tone: strategic, data-anchored,
decision-ready. The CEO is reading 20 of these. Make yours the one that needs
no follow-up questions.

**Template:**

---

**[Function / Product] — [Period] Leadership Update**

**Period:** [dates]
**From:** [name / role]

**Headline:** [One sentence — the story of this period in strategic terms]

**Scorecard:**

| Metric | Target | Actual | vs Plan | Trend | Commentary |
|---|---|---|---|---|---|

Use RAG status (🟢 Green / 🟡 Amber / 🔴 Red) for each metric. Red always
gets one line of explanation and a mitigation action.

**Strategic progress:**

For each active initiative (max 3):

**[Initiative name]** — 🟢 / 🟡 / 🔴
- Progress: [what moved, in numbers]
- Next milestone: [specific outcome, by date]
- Risk: [if any — one line]

**Wins worth noting:**
- [Specific win with metric]: [why it matters strategically]

**Misses and what we're doing:**
- [Miss]: [root cause in one sentence]. [Corrective action and timeline].

**Decisions needed:**

Format each as a decision-ready recommendation, not a question:

> "Recommendation: [specific action]. Options considered: [A] or [B].
> My recommendation is [X] because [reason]. Impact of delay: [cost].
> Decision needed by [date]."

**Headcount and resource pulse:** [Only if relevant — any changes, requests,
or blockers]

**Next period focus:** [Top 2–3 priorities, one line each]

---

**Tone rules for MODE B:**
- The CEO should be able to forward this to the board with zero editing
- Don't bury misses in positive framing — own them directly, then pivot to the fix
- Every amber or red metric needs an owner and a date, not just an explanation
- Decisions are recommendations, not questions — arrive with a view
- Length: 1 page max. If it's longer, it's not ready

---

## MODE C — Board-Level Update

**Format:** Tight narrative with structured data. Tone: investor-grade.
Every word earns its place. The board reads this in 3 minutes and asks
questions about what isn't there.

**Template:**

---

**[Company / Division] — [Period] Board Update**

**Period:** [dates]
**Prepared by:** [name / role]

**Executive Summary**

[2–3 sentences maximum. What happened, what it means, what we're asking for.
This is the entire update for board members who read nothing else.]

**Business Performance**

| KPI | Prior Period | This Period | vs Plan | Commentary |
|---|---|---|---|---|

Red metrics get a dedicated paragraph — not a table note. Write it in plain
English. "Revenue missed plan by 12% due to payment gateway downtime in Week 3,
which cost us approximately [X] in GMV. Root cause resolved. Recovery plan
targets [metric] by [date]."

**Strategic Priorities — Progress**

[List the 3 strategic priorities the board approved last quarter. For each:]

**Priority [N]: [Name]**
Status: 🟢 On Track / 🟡 At Risk / 🔴 Off Track
Progress: [2–3 bullet points, numbers first]
Outlook: [What happens next quarter]

**Key Decisions Required**

[This is the most important section. Boards hate being informed of things they
should have been asked to decide. Get ahead of it.]

For each decision:

**Decision: [Topic]**
Context: [1–2 sentences — why this is on the agenda]
Options: [A] [B] [C] — brief
Recommendation: [Your view, stated clearly]
Consequence of deferring: [Specific, not vague]
Resolution needed by: [Date]

**Risk Register Update**

Only escalate risks that are new, changed in severity, or board-material.
Don't pad.

| Risk | Change from last period | Mitigation | Owner |
|---|---|---|---|

**Upcoming Milestones**

| Milestone | Date | Owner | Status |
|---|---|---|---|

**Appendix (optional):** Detailed financials, cohort data, or product metrics
for board members who want to go deeper.

---

**Tone rules for MODE C:**
- Write like the board already knows the context — they do
- Never use jargon that isn't standard in the industry
- If there's an elephant in the room, address it in paragraph 1, not buried
  in an appendix
- Decisions must arrive with a recommendation — boards are not here to brainstorm
- Length: 2 pages max for the main body. Appendix is unlimited.

---

## Universal Quality Rules (All Modes)

**RAG is a communication tool, not decoration.** Every Red needs an owner,
a root cause, and a date for resolution. Amber needs a watch condition.

**Numbers over narrative.** "DAU up 18% WoW" beats "strong user engagement."

**Decisions, not discussions.** Never end an update with "let us know your
thoughts." End with a specific ask or a specific next action.

**Placeholders over fabrication.** If data isn't provided, use "[insert
current value]" — never invent a number.

**Proactive on misses.** A miss surfaced in an update is a sign of trust and
competence. A miss surfaced in a board meeting is a sign of misalignment.

---

## Suggest Next Commands

After drafting, offer:
- `/stakeholder-map` — to review the power-interest landscape before sending
- `/pre-mortem` — if the update involves a plan that hasn't shipped yet
- `/quarterly-planning` — if the update reveals gaps that need a planning refresh

---

## Examples

**MODE A trigger:**
"Write a weekly update for my PM manager — here's what happened this sprint."

**MODE B trigger:**
"Help me write my monthly update to the CEO. I run the credit card P&L."

**MODE C trigger:**
"I need to prep a board update for next Thursday. We missed GMV by 15%."

**Ambiguous trigger (ask):**
"Can you help me write a stakeholder update?"
→ Respond: "Happy to. Are you writing as a PM to your manager, as a VP/CPO
to your CEO, or is this a board-level update? And is it weekly, monthly,
or milestone-based?"
