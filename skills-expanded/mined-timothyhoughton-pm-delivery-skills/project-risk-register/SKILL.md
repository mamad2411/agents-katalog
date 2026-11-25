---
name: project-risk-register
description: "Produce a risk register with the top 5 risks to a specific project — ranked by exposure (likelihood × impact), with early warning signs, owners, and executable contingencies. Use after the SoW and time plan are drafted, to pressure-test delivery. Triggers: 'flag the risks', 'risk register', 'what could go wrong', 'build a RAID log'."
---

## Project Risk Register

Identify the five risks most likely to derail this specific project — derived from the real SoW and time plan, not a generic list of PM platitudes. Each risk has an early warning sign, a named owner, and a contingency a PM or Account Director can actually execute.

### Why this exists

Generic risk registers are useless. "Client may not approve on time" is true of every project ever run. A useful risk register is tied to *this* SoW, *this* time plan, *this* team structure — and focuses on the intersections where things actually break.

A good risk register is read on a Tuesday morning status call and changes what the PM does that week. If it doesn't do that, it's just a template.

### The framework

Risks live at structural intersections. Look for:

- **Critical path fragility** — long chains with no float, or critical-path tasks owned by a single role
- **External dependency risk** — client inputs, third-party implementations, platform approvals on the critical path
- **Resource concentration** — one role owning multiple critical-path tasks
- **Scope ambiguity** — vaguely defined In Scope items, or Out of Scope items the client will push back on
- **Assumption fragility** — assumptions that, if wrong, would trigger rework or a change request
- **Commercial exposure** — where the fee model amplifies delivery risk (e.g. fixed fee + unlimited revisions appetite)

Scoring is simple: likelihood (Low/Medium/High) × impact (quantified in days, £, or rework) = exposure. Rank the top 5. Contingencies must be executable inside normal agency authority — "escalate early" doesn't count.

### When to use

- SoW and time plan are drafted, and you want a realistic view of what might go wrong
- Project is about to start and you need a risk view for the kick-off pack
- Mid-project replan — you need to reset the risk register to match new reality

### When not to use

- You don't have a SoW or a time plan yet — build those first
- You want a formal ISO-style RAID log — this produces a top-5 view, not a full register
- You're looking for generic industry risks — this is project-specific only

### Prompt

```
# ROLE
You are a senior digital project manager and delivery risk specialist with 10+ years of experience running digital projects inside marketing, advertising, and digital agencies. You've seen every way a launch can slip — and every early warning sign that, if spotted a week earlier, would have saved it.

You think like an insurer, not an optimist. You price risk honestly, rank it by exposure (likelihood × impact), and design contingencies that are executable inside the real constraints of agency delivery — not theoretical mitigations that assume infinite budget or resource.

# OBJECTIVE
Using the Scope of Work and Time Plan provided below, identify the top 5 risks to successful delivery. Each risk must be specific to this project — derived from the actual timeline, team structure, dependencies, and scope — not a generic risk list.

# INPUTS

## Scope of Work
<<<
{{PASTE_SOW_HERE}}
>>>

## Time Plan
<<<
{{PASTE_TIME_PLAN_HERE}}
>>>

## Additional Context (optional — fill in if known)
- Project type: {{E.G. WEBSITE BUILD, APP, CAMPAIGN, CONTENT PROGRAMME, DATA PROJECT, INTERNAL TOOL}}
- Client relationship status: {{E.G. NEW CLIENT, ESTABLISHED RETAINER, RECENTLY RENEWED, UNDER REVIEW}}
- Known client behaviour: {{E.G. SLOW APPROVERS, MULTIPLE STAKEHOLDERS, LEGAL-HEAVY, PRICE-SENSITIVE}}
- Agency commercial exposure: {{E.G. FIXED FEE, T&M, PERFORMANCE-LINKED}}
- Team stability: {{E.G. RECENT CHANGES, KEY ROLE ON NOTICE, SHARED ACROSS ACCOUNTS}}
- Historical issues on this or similar engagements: {{E.G. LATE LEGAL REVIEW, REVISION CREEP, ACCESS DELAYS}}

# METHOD — THINK IN STEPS

Step 1 — Cross-reference SoW and Time Plan
- Identify where the Time Plan's critical path touches the SoW's assumptions, dependencies, and excluded items.
- The highest-value risks usually live at these intersections.

Step 2 — Scan for structural risk
Look specifically for:
- **Critical path fragility:** long chains with no float, or single tasks on the critical path owned by a single role.
- **External dependency risk:** client inputs, third-party implementations, platform approvals on critical path.
- **Resource concentration:** one role owning multiple critical path tasks, or team members shared across accounts.
- **Scope ambiguity:** In Scope items that are vaguely defined, or Out of Scope items the client is likely to push back on.
- **Assumption fragility:** assumptions that, if wrong, would trigger rework or a change request.
- **Commercial exposure:** where the agency's fee model amplifies delivery risk.

Step 3 — Score each candidate risk
For each candidate:
- **Likelihood:** Low / Medium / High — based on what the SoW, Time Plan, and context actually say.
- **Impact:** what specifically happens if it materialises — launch delay (quantified in days), margin erosion, client escalation, compliance exposure, reputational damage.
- **Exposure:** likelihood × impact, used to rank.

Step 4 — Select top 5 by exposure
Not the five most common risks. The five with the highest exposure on this specific project. If two risks have similar exposure, prefer the one that is more actionable now.

Step 5 — Design contingencies that actually work
For each risk, design:
- An **early warning sign** — a specific, observable signal that appears before the risk materialises, with a trigger threshold where possible.
- A **contingency action** — a specific, executable response, with an owner and a clear decision point. Avoid vague mitigations ("escalate early", "increase communication").

# OUTPUT FORMAT

Produce the output in clean Markdown, structured for paste into Word, Confluence, Notion, or a RAID log. Use British English throughout, DD/MM/YYYY for any dates.

## 1. Risk Register (Top 5)

For each risk, use this format:

---

### Risk {{N}}: {{Short, specific risk title}}
- **Description:** 1–2 sentences. Specific to this project, referencing the SoW or Time Plan directly.
- **Trigger conditions:** What has to go wrong for this risk to materialise.
- **Likelihood:** Low / Medium / High — with a one-line justification tied to the inputs.
- **Impact if it happens:** Concrete consequences — quantified where possible (e.g. "3–5 working day launch delay", "£{{X}} margin erosion", "change request required").
- **Exposure rank:** 1 (highest) to 5.
- **Early warning sign:** Specific, observable signal, ideally with a threshold (e.g. "Client approval on DIS-03 not received within 48 hours of submission").
- **Owner of the warning sign:** Who is actively watching for it (role, not person if unknown).
- **Contingency action:** Specific, executable response. Include who does what by when, and the decision point at which the contingency is triggered.
- **Pre-emptive mitigation (if applicable):** Something that can be done now to reduce likelihood or impact, before the risk materialises.

---

## 2. Risk Heat View
A compact table ranking all 5 risks, for at-a-glance use in status reports and steerco decks:

| Rank | Risk | Likelihood | Impact | Owner of Early Warning | Contingency Triggered When |
|---|---|---|---|---|---|

## 3. What's Not On This List
A short paragraph explaining the risks you considered but didn't include in the top 5 — and why. This protects against blind spots: sometimes the risk that didn't make the cut is still worth a watching brief.

## 4. Recommended Next Actions
A prioritised bulleted list (max 5) of things the PM should do this week to reduce exposure. Each should reference a specific risk, be assignable, and be achievable inside normal agency delivery constraints.

# CONSTRAINTS
- Every risk must be traceable to the SoW or Time Plan. If a risk is generic, it doesn't make the cut.
- Do not invent facts, names, dates, or commercial terms not present in the inputs.
- Quantify impact wherever possible (days, £, rounds of rework). Vague impact = weak risk.
- Contingencies must be executable by a PM or Account Director inside normal agency authority — not "hire another designer" or "renegotiate the contract".
- Use UK English spelling and DD/MM/YYYY date format.

# HONEST LIMITATIONS

After the main output, in a separate `## Reviewer Notes` section, flag:
- Risks where likelihood or impact is a judgement call that should be validated by the Delivery Lead or Account Director.
- Risks that depend on context not provided in the inputs (e.g. client behaviour, team stability) and would shift materially with better context.
- Any structural risks you noticed that sit outside the PM's authority to mitigate and should be escalated.
- Anything a human should sense-check before this register is published or added to a RAID log.
```

### Output you should expect

Five ranked risks with full descriptions, early warning signs, owners, contingency actions, and pre-emptive mitigations. Plus a heat view, a "what's not on this list" paragraph, and 3–5 prioritised next actions for the PM this week.

### What to do with it

1. Paste into your project's RAID log or status tracker.
2. Assign the early-warning owners explicitly — a risk with no named owner doesn't get watched.
3. Take the "Recommended Next Actions" list into your PM one-on-one this week. Those are the things that actually reduce exposure.
4. Re-run this skill whenever the time plan materially changes.

### Related skills

- `project-time-plan` — the input to this skill
- `scope-change-control` — for handling when a risk materialises into a change request
- `assumptions-and-dependencies` — for deeper work on the assumptions underpinning the risks
