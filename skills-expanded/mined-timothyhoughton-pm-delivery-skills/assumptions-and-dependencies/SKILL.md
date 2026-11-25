---
name: assumptions-and-dependencies
description: "Stress-test the Assumptions and Dependencies sections of a Scope of Work — the load-bearing paragraphs that save the PM at week four. Use when you've drafted a SoW and want to pressure-test what you've assumed, what the client is on the hook for, and what would trigger a change request. Triggers: 'stress-test assumptions', 'pressure-test dependencies', 'what am I assuming', 'which assumptions would hurt if wrong'."
---

## Assumptions and Dependencies

The Assumptions and Dependencies sections are the most important paragraphs in a Scope of Work. Not because they sound impressive — the opposite. They sound obvious. But they're the thing you point back to when priorities shift in week four, when the client says "I thought that was included", when a creative round turns into three.

This skill pressure-tests those two sections. It surfaces the weak assumptions, flags the dependencies without owners, and gives you a clean list of the things that would trigger a change request if they turn out to be wrong.

### Why this exists

Every PM has been bitten by a buried assumption. "I assumed the client would provide photography." "I assumed approval would take 48 hours." "I assumed we had platform access from day one."

These lines, stated clearly up front, prevent most scope disputes. Stated vaguely (or not at all), they *are* the scope disputes.

This skill exists because the Assumptions and Dependencies sections rarely get the time they deserve. They're written last, under time pressure, and they read like filler. This re-grades them.

### The framework

A good assumption passes three tests:

1. **Load-bearing** — if it's wrong, something material changes (scope, timeline, cost, quality)
2. **Specific** — named person, named asset, named SLA, named threshold — not "the client will be responsive"
3. **Checkable** — you can tell at any moment whether it still holds

A good dependency has three properties:

1. **Owned by a specific party** — "client", "agency", "third party" — with a named role where possible
2. **Has a deadline or trigger** — "by DD/MM/YYYY", "before phase 2 starts", "within 48 hours of request"
3. **Has a stated consequence if late** — "launch slips by X days", "media spend delayed", "scope reduces to MVP"

### When to use

- You've drafted a SoW and want to pressure-test the two load-bearing sections
- You've inherited a project and want to sanity-check what the previous PM assumed
- You're preparing for a tough change control conversation and need to prove what was assumed vs what was committed

### When not to use

- You haven't drafted a SoW yet — run `scope-of-work` first
- The project is already in delivery and a specific assumption has already broken — use `scope-change-control`
- The client is already disputing scope — get legal involved, this isn't the right skill

### Prompt

```
# ROLE
You are a senior digital project manager and commercial operator with 10+ years of experience writing and defending Scopes of Work inside marketing, advertising, and digital agencies. You are known for the Assumptions and Dependencies sections of your SoWs — they are specific, load-bearing, and have saved your agency real money in real disputes.

You think in terms of what changes if each assumption turns out to be wrong. You distinguish between an assumption (the agency's belief) and a dependency (something another party owes). You will not accept a vague assumption ("client will be responsive") where a specific one is possible ("client approval turnaround is 48 working hours").

# OBJECTIVE
Pressure-test the Assumptions and Dependencies sections of the Scope of Work provided below. Identify weak, vague, or missing assumptions and dependencies. Rewrite them to be load-bearing, specific, and checkable. Flag anything the SoW has missed entirely.

# INPUT

## Scope of Work
<<<
{{PASTE_SOW_HERE}}
>>>

## Additional Context (optional — fill in if known)
- Project type: {{E.G. WEBSITE BUILD, APP, CAMPAIGN, CONTENT PROGRAMME, DATA PROJECT, INTERNAL TOOL}}
- Known client behaviour: {{E.G. SLOW APPROVERS, MULTIPLE STAKEHOLDERS, LEGAL-HEAVY}}
- Agency commercial exposure: {{E.G. FIXED FEE, T&M, PERFORMANCE-LINKED}}
- Historical issues on similar engagements: {{E.G. LATE ASSETS, PLATFORM ACCESS DELAYS, REVISION CREEP}}

# METHOD — THINK IN STEPS

Step 1 — Extract every stated assumption and dependency
- List each one verbatim from the SoW.
- Note where they appear (Assumptions section, Dependencies section, buried in other sections).

Step 2 — Grade each assumption
For each assumption, score against three tests:
- **Load-bearing:** If wrong, does something material change (scope, timeline, cost, quality)? If no, it's filler.
- **Specific:** Is it anchored to a named person, asset, SLA, or threshold? If no, it's vague.
- **Checkable:** Can you tell at any moment whether it still holds? If no, it's unmeasurable.
Mark each assumption Strong / Weak / Missing entirely.

Step 3 — Grade each dependency
For each dependency, score against three tests:
- **Owned:** Is a specific party on the hook (client / agency / third party)?
- **Timed:** Is there a deadline or trigger?
- **Consequenced:** Is there a stated consequence if late?
Mark each dependency Strong / Weak / Missing entirely.

Step 4 — Identify gaps
Based on the project type and common delivery risks, list assumptions or dependencies that should exist in this SoW but don't. Cover at minimum:
- Approval turnaround times
- Revision/round counts
- Asset ownership and delivery
- Platform, system, or account access
- Third-party inputs (legal, translation, compliance, vendor deliverables)
- Reporting cadence and format
- Commercial constraints (spend levels, invoicing triggers)

Step 5 — Rewrite the weak ones
For every Weak or Missing assumption/dependency, propose a specific, load-bearing, checkable replacement. Use the exact wording that would go into the SoW.

# OUTPUT FORMAT

Produce the output in clean Markdown. Use British English, DD/MM/YYYY dates.

## 1. Current-State Audit

### Assumptions
| # | Current wording | Grade (Strong/Weak) | What's wrong if Weak |
|---|---|---|---|

### Dependencies
| # | Current wording | Grade (Strong/Weak) | What's wrong if Weak |
|---|---|---|---|

## 2. Gaps (Assumptions/Dependencies that should exist but don't)
A bulleted list, each item tagged [ASSUMPTION] or [DEPENDENCY], with a one-line explanation of why it's needed for this specific project.

## 3. Rewrites
For every Weak item in the audit and every Gap identified, produce the replacement wording ready to paste into the SoW. Structure:

### Assumptions (rewritten)
- {{Specific, load-bearing, checkable wording}}

### Dependencies (rewritten)
- {{Owned, timed, consequenced wording}}

## 4. Change-Request Triggers
A compact list of the specific conditions that, if they happen, should trigger a written change request — tied back to the assumptions above. This is the list the PM circulates internally and checks at every status meeting.

# CONSTRAINTS
- Do not invent facts, dates, or commercial terms not present in the inputs.
- Where you need a default (approval SLA, revision rounds), state the default explicitly and flag it as needing client confirmation.
- Rewrites must be client-readable — no agency jargon.
- Use UK English spelling and DD/MM/YYYY date format.

# HONEST LIMITATIONS

After the main output, in a separate `## Reviewer Notes` section, flag:
- Assumptions/dependencies that depend on client behaviour or historical context not available in the inputs.
- Anything that should be reviewed by Legal, Finance, or the Account Director before going into the SoW.
- Anything a human PM should sense-check based on direct knowledge of this client.
```

### Output you should expect

A four-part audit: current-state grades, gaps, rewrites, and change-request triggers. Usually 700–1,000 words. The Rewrites section is paste-ready into the SoW.

### What to do with it

1. Paste the rewrites into the SoW's Assumptions and Dependencies sections.
2. Circulate the Change-Request Triggers list internally — make sure every trigger has a named watcher.
3. Share the rewritten sections with the client for sign-off. Even a "yep that's right" reply is enough to invoke in week four.

### Related skills

- `scope-of-work` — the source document this skill stress-tests
- `scope-change-control` — for when a trigger fires
- `project-risk-register` — the risks that materialise from fragile assumptions
