---
name: scope-of-work
description: "Write a tight, commercially watertight Scope of Work under 500 words, using the client brief and your scoping answers as input. Use when discovery questions have been answered and you're ready to lock in what's in, what's out, and who's doing what. Triggers: 'write the SoW', 'draft scope of work', 'turn this into a SoW', 'write a statement of work'."
---

## Scope of Work

Produce a Scope of Work (SoW) that is specific to the engagement, under 500 words, and impossible to weaponise against the agency later. Works for any digital project type — the structure is fixed, the content is bespoke.

### Why this exists

A good SoW does three jobs at once: it confirms the project goal in plain language, sets clear boundaries (what's in, what's out), and captures the assumptions and dependencies that would trigger a change request if they turn out to be wrong.

Most SoWs fail because they try to do more than this. They pile on clauses, they hedge with boilerplate, they bury the load-bearing paragraph (Assumptions) under legalese. A 500-word limit forces the document to be useful.

### The framework

Every SoW in this skill follows the same 8-section structure:

1. **Project Goal** — one sentence, describes the business outcome, not the activity
2. **Success Criteria** — 3–5 measurable outcomes
3. **In Scope** — concrete, verifiable deliverables
4. **Out of Scope** — the exclusions that prevent scope creep
5. **Key Stakeholders** — names/roles with decision-making authority
6. **Dependencies** — what must happen, who owns it, the risk if it's late
7. **Assumptions** — what would trigger a change request if wrong
8. **Change Control Note** — single line at the end

### When to use

- Scoping questions have been answered and you're ready to commit to a scope
- You've inherited a project that has no SoW and need to back-fill one
- You're preparing a proposal and need the scope section

### When not to use

- You don't have answers to the critical questions yet — run `scoping-questions` first
- You need a full contract — this is the scope section, not the master services agreement
- You're scoping something fluid or iterative that genuinely can't be bounded (e.g. open-ended R&D) — use a statement of work for the first sprint only

### Prompt

```
# ROLE
You are a senior digital project manager and commercial operator with 10+ years of experience writing Scopes of Work for digital projects inside marketing, advertising, and digital agencies. You are equally fluent in delivery reality and commercial protection — your SoWs are known for being tight, unambiguous, and impossible to weaponise against the agency later.

You write in plain, confident language. No jargon for jargon's sake. No hedging. No filler.

# OBJECTIVE
Using the client brief and scoping answers provided below, produce a Scope of Work document that is clear, commercially watertight, and under 500 words. The document must be specific to this engagement — every section should reference real details from the inputs, not generic boilerplate.

# INPUTS

## Client Brief
<<<
{{PASTE_CLIENT_BRIEF_HERE}}
>>>

## Scoping Answers
<<<
{{PASTE_SCOPING_ANSWERS_HERE}}
>>>

## Additional Context (optional — fill in if known)
- Agency name: {{AGENCY_NAME}}
- Client / brand name: {{CLIENT_NAME}}
- Project name: {{PROJECT_NAME}}
- Project type: {{E.G. WEBSITE BUILD, APP, CAMPAIGN, CONTENT PROGRAMME, INTERNAL TOOL}}
- Proposed start date: {{DD/MM/YYYY}}
- Proposed end date: {{DD/MM/YYYY}}
- Commercial model: {{E.G. FIXED FEE, T&M, RETAINER, % OF MEDIA}}
- Known constraints: {{E.G. LEGAL REVIEW REQUIRED, OFFSHORE STAKEHOLDERS, PEAK TRADING PERIOD}}

# METHOD — THINK IN PHASES

Phase 1 — Reconcile inputs
- Cross-reference the brief against the scoping answers.
- Identify contradictions, gaps, or items where the scoping answers changed the original brief.
- Note anything the scoping answers still didn't resolve — these become Assumptions or Dependencies, not invented facts.

Phase 2 — Pressure-test each section
- For every In Scope item, ask: "Could a client argue this means more than I intended?" If yes, tighten the wording.
- For every Out of Scope item, ask: "Is this something the client might reasonably expect to be included?" If yes, it must be explicitly excluded.
- For every Success Criterion, ask: "Is this measurable, and does the agency control the levers to influence it?" If not, reframe or move to Assumptions.

Phase 3 — Write tight
- Cut anything that isn't load-bearing.
- Use active voice. Short sentences. Concrete nouns.
- Stay under 500 words total across all sections.

# OUTPUT FORMAT

Produce the SoW in clean Markdown, ready to paste into Word, Confluence, or Notion. Use British English, DD/MM/YYYY dates, and £ for any currency references.

Structure exactly as follows:

---

# Scope of Work: {{PROJECT_NAME}}

**Client:** {{CLIENT_NAME}} | **Agency:** {{AGENCY_NAME}} | **Dates:** {{START}} – {{END}}

## Project Goal
One sentence. Plain language. Describes the business outcome the project is driving toward — not the activity.

## Success Criteria
3–5 measurable outcomes, expressed as specific targets or thresholds where possible. If the scoping answers didn't give numbers, state "Target to be confirmed at kick-off" rather than inventing them.

## In Scope
A tight, bulleted list of specific deliverables and activities the agency will produce or perform. Each bullet should be concrete enough that a third party could tell whether it had been delivered. Group logically (e.g. Strategy, Design, Build, Content, Launch) if the list exceeds ~6 items.

## Out of Scope
Explicitly excluded items the client might otherwise assume are included. Prioritise exclusions that protect margin or prevent common scope-creep traps for this project type.

## Key Stakeholders
A short table or list with:
- **Name / Role / Organisation**
- **Decision-making authority** (Approver, Reviewer, Informed, Day-to-day contact)

Include both client-side and agency-side stakeholders. If names aren't in the inputs, use role placeholders (e.g. "Client Marketing Lead — TBC").

## Dependencies
Things that must happen before or during the engagement for the agency to deliver. Be specific about who owns each dependency and the risk if it's late (e.g. "Client to provide brand assets by DD/MM/YYYY — delay will push launch date").

## Assumptions
What the agency is assuming to be true in order to scope this engagement. If any assumption proves false, it is a trigger for a change request. Cover: review/approval rounds, approval turnaround times, asset availability, platform access, third-party inputs, and reporting cadence.

---

## Change Control Note
> Any changes to the above — including additional deliverables, extended timelines, or shifts in spend — will be managed via a written change request and may impact fees and delivery dates.

# CONSTRAINTS
- Hard limit: **under 500 words total** across the SoW (excluding the title block and Change Control Note).
- Plain language. No agency jargon unless it's standard client-side vocabulary.
- Every section must reference specifics from the brief or scoping answers. No generic boilerplate.
- Do not invent numbers, names, dates, or commitments not present in the inputs. If something is missing, surface it as an Assumption or Dependency.
- Use UK English spelling and DD/MM/YYYY date format.

# HONEST LIMITATIONS

After the SoW, in a separate `## Reviewer Notes` section (not counted in the 500-word limit), flag:
- Any gaps in the inputs that forced an assumption.
- Any clauses a human PM or Account Director should pressure-test before sending to the client.
- Any commercial or legal items that should be reviewed by Finance/Legal before signature.
```

### Output you should expect

A clean markdown SoW, under 500 words, ready to paste into Word, Confluence, or Notion. Plus Reviewer Notes flagging gaps and items to sense-check.

### What to do with it

1. Give the LLM your agency's existing SoW template if you have one — it will fill it in rather than generate from scratch.
2. Share the draft internally with your Account Director or Delivery Lead before sending externally.
3. Send to the client for sign-off. Even a reply saying "Yep, that's right" is enough — you now have something to point back to when priorities shift.
4. Use the signed SoW as the input to `work-breakdown-structure`.

### Related skills

- `scoping-questions` — the input to this skill
- `assumptions-and-dependencies` — for stress-testing the load-bearing assumptions
- `scope-change-control` — for handling changes once the SoW is signed
- `work-breakdown-structure` — the next step in the scoping chain
