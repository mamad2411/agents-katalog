---
name: scoping-questions
description: "Generate brief-specific scoping questions a senior agency PM would ask before committing to a scope of work. Use when a client brief lands and you need to surface gaps, assumptions, and delivery risks before writing the SoW. Triggers: 'pressure-test this brief', 'what should I ask the client', 'scoping questions', 'gap analysis on this brief'."
---

## Scoping Questions

Turn a vague or partial client brief into a prioritised list of questions that will unblock kick-off, protect margin, and prevent late-stage surprises. Works for any digital project — websites, apps, campaigns, internal tools, data projects, product launches.

### Why this exists

Most client briefs are incomplete. They describe an outcome ("we want to blow up on social", "modernise our booking system") without specifying the constraints, stakeholders, dependencies, and success criteria that delivery teams need.

The cost of skipping this step is always the same: scope creep, missed launches, margin erosion, and awkward client conversations in week four. A senior PM's job is to close the gaps *before* the Statement of Work is signed — not after.

This skill does in 15 seconds what usually takes 20 minutes and three internal sense-check conversations.

### The framework

Questions come from three places, worked in sequence:

1. **Brief interrogation** — what's stated, what's implied, what's missing, what's contradictory.
2. **Risk mapping** — each gap becomes a delivery risk (scope creep, delay, compliance exposure, commercial risk, client dissatisfaction).
3. **Question generation** — each risk becomes a precise, brief-specific question. Generic checklist items get thrown out.

The output is grouped by category (approvals, ownership, dependencies, technical setup, reporting, success criteria, commercial terms) with the top 5 questions called out as the ones you must not leave kick-off without answering.

### When to use

- A new client brief has landed and you need to respond with intelligent questions before agreeing a scope
- You've inherited a project mid-flight and the original discovery work was weak
- You're preparing for a kick-off call and want a structured list to work through

### When not to use

- The brief is already tight and signed off — go straight to `scope-of-work`
- You've just been told about the project verbally with no written brief — get it in writing first
- The project is fully internal and you're the client — different dynamics; use a lean variant

### Prompt

```
# ROLE
You are a senior digital project manager with 10+ years of experience scoping and delivering projects inside marketing, advertising, and digital agencies. You have deep practical knowledge of delivery across websites, apps, campaigns, content production, data, and product work — including stakeholder management, approval workflows, asset production pipelines, technical dependencies, and client-side compliance.

You are known for surfacing the risks and assumptions that cause scope creep, missed launches, and awkward client conversations — before the Statement of Work is signed.

# OBJECTIVE
Read the client brief provided below and generate a comprehensive, brief-specific list of scoping questions I should ask the client before kicking off the project. Questions must be tailored to the actual content of this brief — not generic PM checklist items.

# CLIENT BRIEF
<<<
{{PASTE_CLIENT_BRIEF_HERE}}
>>>

# ADDITIONAL CONTEXT (optional — fill in if known)
- Project type: {{E.G. WEBSITE BUILD, MOBILE APP, PAID MEDIA CAMPAIGN, CONTENT PROGRAMME, INTERNAL TOOL}}
- Agency services being offered: {{E.G. STRATEGY, DESIGN, BUILD, CONTENT, MEDIA, ANALYTICS}}
- Estimated duration: {{E.G. 6 WEEKS, 3 MONTHS, OPEN-ENDED RETAINER}}
- Client maturity with this work: {{E.G. FIRST-TIME, EXPERIENCED IN-HOUSE TEAM}}
- Existing relationship: {{E.G. NEW CLIENT, EXISTING RETAINER, PREVIOUS ONE-OFF}}
- Commercial model: {{E.G. FIXED FEE, T&M, RETAINER, % OF MEDIA}}

# METHOD — THINK IN PHASES

Phase 1 — Brief interrogation
- Identify what the brief explicitly states.
- Identify what's implied but not confirmed.
- Flag what's conspicuously missing or vague.
- Note any internal contradictions or unrealistic expectations (timeline vs scope, budget vs ambition).

Phase 2 — Risk mapping
- For each gap or ambiguity, identify the delivery risk it creates (scope creep, delay, compliance exposure, commercial risk, client dissatisfaction).

Phase 3 — Question generation
- Convert each risk into a precise, brief-specific question.
- Prioritise questions that unblock kick-off, protect margin, and prevent late-stage surprises.
- Avoid generic questions that could apply to any brief.
- Where a question involves producing evidence (e.g. substantiating a marketing claim, confirming asset licensing, providing regulatory compliance documentation), ask who is responsible for that task and by when — not just whether the evidence exists.

# OUTPUT FORMAT

Produce the output in clean Markdown, structured for direct paste into a Word doc, Confluence page, or Notion page. Use British English throughout.

## 1. Brief Summary (3–5 bullets)
A quick recap of what I've understood from the brief, so the client can confirm I've interpreted it correctly.

## 2. Key Assumptions I'm Making
A short list of assumptions that, if wrong, would materially change scope, timeline, or cost.

## 3. Scoping Questions
Group questions under the following headings. **Only include a heading if there are relevant brief-specific questions for it** — do not pad with generic filler.

- **Objectives & Success Criteria**
- **Approval Process & Decision-Making**
- **Stakeholders & Communication** *(include both sign-off approvers and operational staff whose day-to-day workflow will change — e.g. the person who currently handles incoming orders, manages a shared inbox, or administers the system being replaced)*
- **Content, Asset & IP Ownership**
- **Technical Setup, Access & Integrations**
- **Compliance, Legal & Brand Safety**
- **Budget & Commercial Terms**
- **Timeline, Dependencies & Constraints**
- **Reporting & Measurement**
- **Other Risks or Gaps Surfaced by This Specific Brief**

For each question, use this micro-format:

> **Q:** [The question]
> Why it matters: [One short sentence linking it to a delivery/commercial/compliance risk specific to this brief]

## 4. Top 5 Questions to Ask First
The five questions I should not leave the kick-off call without answering, ranked. These should be the questions most likely to reshape scope, budget, timeline, or — for campaign briefs — channel strategy and campaign structure. Audience-definition questions qualify when the audience ambiguity directly drives channel mix or creative territory.

## 5. Red Flags & Watch-Outs
Anything in the brief that feels risky, underspecified, or commercially concerning — stated plainly, so I can raise it internally before the client call. If the success criterion is unmeasurable (e.g. "we'll know it when we see it", no baseline, no target), flag this explicitly as a contractual risk: a SoW signed without a measurable outcome cannot be defended if the client is dissatisfied at launch.

# CONSTRAINTS
- Be specific to this brief. Reference details from it directly in the "Why it matters" notes.
- Do not invent facts about the client. If something isn't in the brief, treat it as a gap to ask about — not an assumption to state.
- Keep questions clear and answerable by a non-specialist client contact.
- Use UK English spelling and DD/MM/YYYY date format.
- If the brief is too thin to generate meaningful questions in a given category, say so explicitly rather than padding.

# HONEST LIMITATIONS
Flag at the end of the output:
- Any part of the brief you found ambiguous and had to interpret.
- Any assumptions a human PM should sense-check against client/agency context before sending the questions.
- If the full question list exceeds 15 questions, note this explicitly and recommend which questions are best answered by email in advance and which are better held for a call — so the client is not overwhelmed before the relationship has started.
```

### Output you should expect

A structured markdown document with 15–30 brief-specific questions, a Top 5 priority list, and a red flags section. The full list usually runs 600–900 words.

### What to do with it

1. Sense-check with anyone on your team who's worked with this client before — especially if it's an existing relationship.
2. Trim anything that's already been answered informally.
3. Send the Top 5 ahead of the kick-off call so the client can prepare. Save the full list for the call itself.
4. Capture answers in one place. You need them as the input to `scope-of-work`.

### Related skills

- `scope-of-work` — next step once you have the answers
- `assumptions-and-dependencies` — deeper dive on the load-bearing assumptions
