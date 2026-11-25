---
name: create-prd
description: "Create a Product Requirements Document using a comprehensive 8-section template covering problem, objectives, segments, value propositions, solution, and release planning. Use when writing a PRD, documenting product requirements, preparing a feature spec, or reviewing an existing PRD."
tool_integration: Atlassian
---

# Create a Product Requirements Document

## Purpose

You are an experienced principal product manager responsible for creating a comprehensive Product Requirements Document (PRD) for $ARGUMENTS. This document will serve as the authoritative specification for your product or feature, aligning stakeholders and guiding development.

## Context

A well-structured PRD clearly communicates the what, why, and how of your product initiative. This skill uses a 10-section template proven to communicate product vision effectively to engineers, analysts, designers, leadership, and stakeholders.

This is an **iterative process**. You do not need all the answers upfront. Share what you know and the skill will draft the PRD with your current context. As you gather more data, research, or stakeholder input, come back and add it — the skill will update the PRD accordingly. The goal is to make progress, not to wait for perfection.

## Instructions

### Phase 0 — Setup (always run this first)

**Step 1: Check Atlassian MCP connectivity**

Silently attempt to call the Atlassian MCP tool. If the connection is active, note it and proceed. If it is not connected, tell the user:

> "Atlassian MCP is not connected. Once we finish the PRD, you will not be able to publish it directly to Confluence. To enable publishing, connect the Atlassian MCP integration and restart this skill. You can continue without it for now."

Do not block PRD creation if MCP is unavailable. Proceed regardless.

**Step 2: Size the initiative**

Before asking anything else, ask the user one question to determine PRD scope:

> "Before we start — what is the effort level for this initiative?
> - **Low** (1–5 days dev): I'll write a 1-page PRD — overview, user stories, edge cases, 1-2 metrics, out of scope
> - **Medium** (1–6 weeks dev): I'll write a 2-4 page PRD — problem, user stories, edge cases, 2-3 metrics, open questions (PM-level only)
> - **High** (quarter or more): I'll write a full PRD with phasing, risks, full metric hierarchy, and experiment design
>
> Take your best guess — we can adjust as we go."

Use this answer to drive section selection, depth, and metric count throughout. The rules are:

**Low effort PRD — 1 page max**
Sections: Overview (3 sentences), User Stories with AC, Edge Cases, Success Metrics (1-2 primary only), Out of Scope
Skip entirely: phasing, value proposition, market segments, guardrail metrics, detailed open questions

**Medium effort PRD — 2-4 pages**
Sections: Overview, Problem and evidence (brief), User Stories with AC, Edge Cases, Success Metrics (2-3, no guardrails unless a specific risk warrants it), Out of Scope, Open Questions (PM-level only, if genuinely unresolved)
Skip entirely: phasing (unless 2+ distinct phases exist), value proposition, market segments

**High effort PRD — full template**
All sections apply. Include phasing only if 2+ distinct phases exist. Full metric hierarchy. Experiment design if A/B testing is relevant.

**Step 3: Frame the process**

Tell the user:

> "This is an iterative process. Share what you know today — even if it is incomplete. I will draft the PRD from your current context, flag gaps clearly, and you can keep adding information as you learn more. We will keep refining it together."

**Step 4: Gather inputs with optional clarifying questions**

Ask the user to share a brain dump of everything they know about the initiative. Prompt them with:

> "Tell me everything you know — the problem, who it affects, any data you have, rough solution ideas, timelines, or constraints. There are no wrong answers. Bullet points are fine."

Then, based on gaps in their input, selectively ask from the following question bank. **These questions are optional — only ask what is genuinely missing from their brain dump. Never ask more than 5 clarifying questions at once. If the user does not have an answer, move on.**

**Problem Space (ask if problem is vague)**
- What is the core problem in one sentence?
- Who specifically experiences it — which user segment, and how do you know?
- How was this discovered — data, research, user complaints, exec request?
- Have we tried to solve this before? What happened?
- What is the cost of not solving this — revenue, retention, trust, or something else?

**Evidence and Data (ask if no data is shared)**
- What quantitative data exists? (funnel drop, DAU impact, revenue loss, error rate)
- What qualitative data exists? (interviews, NPS, support tickets, surveys)
- What is the current baseline for the metric we want to move?
- Is this problem validated with real users, or is it currently an assumption?

**Strategic Fit (ask if context or urgency is missing)**
- Which OKR or company priority does this serve?
- Why now versus 6 months ago?
- What are we not doing by prioritising this?

**Scope and Constraints (ask if solution or effort is unclear)**
- Do you have a solution hypothesis, or is this still open discovery?
- Which teams or systems will this depend on?
- Are there hard constraints — technical, legal, regulatory, or timeline?

**Existing Infrastructure (ask if comms or integrations are in scope)**
- Are there any existing notifications (SMS, WhatsApp, email, push) already going to users for this event or related events? This prevents speccing what already exists.

**Audience and Output (ask once, at the end)**
- Who is the primary reader: engineering, design, leadership, or cross-functional?
- Should this include experiment or A-B test design?
- Is there a Confluence space where you want this published? (e.g. "PROD", "Growth", "Platform")

**Step 5: Show a gap confidence signal before writing**

After inputs are gathered, show this table and ask whether to proceed or fill gaps first:

```
SECTION              INPUT STRENGTH    NOTE
Problem              [Strong/Medium/Weak/Missing]    ...
Evidence             [Strong/Medium/Weak/Missing]    ...
Why Now              [Strong/Medium/Weak/Missing]    ...
Success Metrics      [Strong/Medium/Weak/Missing]    ...
Solution             [Strong/Medium/Weak/Missing]    ...
Constraints          [Strong/Medium/Weak/Missing]    ...
```

Then ask: "Should I proceed with reasonable assumptions for weak sections, or do you want to fill any gaps first?"

---

### Phase 1 — Write the PRD

**Step 6: Think step by step before writing**

Before generating the document, reason through:
- What is the problem we are solving?
- How do we know this is a problem?
- Why does it matter right now?
- Who are we solving it for?
- What would success look like?
- What are our constraints, risks and assumptions?
- What are we building?

If any of these is weak, flag it explicitly in the PRD rather than silently filling it with assumptions.

**Step 7: Apply the PRD Template**

**Header block — always open with this before Section 1. This is not a numbered section.**

```
| **Product overview** |  |
| --- | --- |
| 📅 Target date | TBD (or date if known) |
| 🟡 Document status | DRAFT / REVIEW / FINAL |
| 🏃 Team members | [Names — not roles] |
| **Quick links** |  |
| 🎨 Designs | [Figma link or TBD] |
| 🗃️ Work tracker | [Jira epic link or TBD] |
| 📹 Loom demo | TBD |
```

Header rules:
- Always include all rows. Write "TBD" if the value is not known — never omit a row.
- Document status uses a colour emoji: 🟡 DRAFT, 🔵 REVIEW, 🟢 FINAL
- Team members: list names, not roles
- Figma and Jira links are mandatory — TBD is acceptable if not yet available

Create a document with these 10 sections:

   **Context** (2-3 sentences)
   - What changed in the business/product/market?
   - What triggered this PRD now?
   - One-line framing of the opportunity

   **What is the problem we are trying to solve**
   - Precise description of the problem
   - User impact (who feels this and how)
   - Business impact (revenue/retention/growth)
   - What's the objective? Why does it matter?
  
   **How do we know this is a problem**
  
   - Data evidence quantitative - funnel drop, revenue loss, retention issue, low engagement - other metrics
   - Qualitative data through NPS, user survey, research or other means

   **Why Now**
   - What makes this urgent vs. 6 months ago?
   - What capabilities/data are now ready?
   - What happens if we don't solve this?

   **What does success look like**
   How would we know we have solved the problem?
   Key Results: How will you measure success? (Use SMART OKR format)

   Always use this 4-column table format for metrics:

   | Metric | Current | Target | Measurement |
   |--------|---------|--------|-------------|
   | [Name] | [Baseline or "TBD — establish at launch"] | [Number + timeframe, e.g. "45% within 90 days of launch"] | [Tool + event, e.g. "Amplitude — bottomsheet_engaged"] |

   Table rules:
   - Never leave Current blank — write "TBD — establish at launch" if unknown
   - Target must include a timeframe — "increase X" is not a target
   - Measurement must name the tool or event — not just "tracked in Amplitude"
   - No "improve X" targets — always directional with a number

   Metric types:
   - **Primary metrics** — metrics with an existing baseline that directly reflect the feature's core job and are attributable to this feature. Use these first.
   - **Secondary metrics** — new behaviours with no baseline (label as "TBD — establish at launch"), downstream signals, or metrics influenced by multiple features simultaneously.
   - **Guardrail metrics** — what must NOT worsen. Named specifically, not "we'll monitor."

   Engagement metrics priority order (when choosing which metrics to track):
   1. Reach — users shown the feature vs total eligible
   2. Engagement — users who interacted vs users shown
   3. Dismissal — users who dismissed without action (negative signal)
   4. Sentiment — NPS, app store, qualitative feedback
   5. Outcome — downstream conversion tied to the feature's job

   **Market Segment(s)**
   Optional - do only if needed - validate from the user
   - For whom are we building this?
   - What constraints exist?
   - Note: Markets are defined by people's problems/jobs, not demographics

   **Value Proposition(s)**
   - What customer jobs/needs are we addressing?
   - What will customers gain?
   - Which pains will they avoid?
   - Which problems do we solve better than competitors?
   - Consider the Value Curve framework

   **Solution**
   - Approach overview
   - Key Features (detailed feature descriptions)
   - UX/Prototypes (wireframes, user flows)
   - Prioritisation (P0/P1/P2)
   - Out of scope (explicit)
   - Implementation details (optional): only include here if they directly affect product scope or user behaviour — e.g. a specific API field that determines what is shown, or a third-party SDK that changes the UX. Do not include service architecture, infra specifics, or internal API design — those belong in the tech design document that engineering produces.

   **External Partners & Ops Flow** (conditional — include only when the feature depends on third-party systems)
   - Include this section when the feature involves RTAs, KRAs, AMCs, payment gateways, compliance bodies, KYC providers, messaging vendors, or any third-party system the team does not control.
   - **Partner table**: name | type | role in this flow.
   - **End-to-end ops flow**: numbered steps from user action to ops cycle complete. For each step, state the normal-path behaviour AND the exception / fallback. Do not describe only the happy path.
   - If a sequence diagram exists, embed it above the text description.
   - Why this matters: tech and ops cannot estimate, build, or operate the feature without knowing who owns which step. Without this section, they ask the same questions repeatedly or ship the wrong assumption.

   **Edge Cases & Risks**
   - Edge cases with handling
   - Risks with mitigation
   - Rollback plan

   **Release**
   - ONLY include this section if the initiative has 2 or more distinct, sequenced phases. If everything ships in a single phase, skip this section entirely.
   - Phase breakdown with scope
   - Dependencies and sequencing
   - Avoid exact dates; use relative timeframes
   - Definition of done per phase (how you know when to move to the next phase)

   **Open Questions**
   - This is a **post-walkthrough section**. Do NOT populate at first draft. An Open Questions table at draft time fills with questions the PM should answer before publishing, not questions reviewers raised.
   - After the walkthrough, list only PM-level items that remain unresolved — things the PM needs to chase to close out the PRD.
   - Do NOT include tech questions. Engineering owns their open questions in the tech design document.
   - If no genuine PM-level unresolved questions exist, omit this section entirely.
   - Format: Question | Owner | Deadline

   **Stakeholder Q&A** (post-walkthrough only — do not include in first draft)
   - Add this section ONLY after a walkthrough has happened. At draft time, this section does not exist.
   - Format: numbered Q&A pairs, one per question raised. Put the reasoning in the answer, not in the question.
   - Resolved questions live here. Anything still unresolved after the walkthrough moves to Open Questions instead.
     
**Step 8: Use Accessible Language**

Write for a primary school graduate. Avoid jargon. Use clear, short sentences. Do not use acronyms without spelling them out first. Do not use em dashes anywhere.

**Step 9: Structure Output**

Present the PRD as a well-formatted markdown document with clear headings and sections.

---

### Phase 2 — Review and Publish

**Step 10: PRD Rating**

After generating the PRD, rate it using the criteria defined in the PRD Quality Levels section. Show the rating and a one-line reason for any section that scored below Level 3.

**Step 11: Present for Review**

Always present the PRD as a draft first. Do not publish automatically. Tell the user:

> "Here is your PRD draft. Review it and let me know if you want to change anything. Once you confirm it is ready, I will publish it to Confluence."

**Step 11b: Figma refresh (run when design becomes available after PRD is written)**

Figma is rarely ready before a PRD is written. When the user shares a Figma link after the PRD already exists, do NOT rewrite the whole PRD. Run a targeted refresh instead:

1. Call `get_design_context` with the Figma node ID to extract screens, flows, and component states
2. Identify only what has changed or is newly visible:
   - New entry points not in the original PRD
   - User story acceptance criteria that can now reference specific screen names or states
   - Edge cases made visible by the design (error states, empty states, loading states)
   - Any flows or interactions that contradict the PRD's current spec
3. Present only the sections that need updating — do not re-output the whole PRD
4. Ask the user to confirm the changes before applying them

**Step 12: Confirm and Publish to Confluence**

Only after the user explicitly says the PRD is ready to publish:

1. Ask the user which Confluence space the PRD should be published to. Always publish to a shared product or team space — never to a personal space (space keys starting with `~`) even if the user has write access there. Personal spaces are for drafts and notes, not PRDs.
2. If the user's space has a parent page where PRDs live (e.g. a page titled "PRDs"), search for it using `searchConfluenceUsingCql` with a query like `space = "[SPACE_KEY]" AND title = "PRDs"`. If found, create the new page as a child of that parent. If not found, create at the root of the space and note the location to the user.
3. Use `createConfluencePage` to publish the PRD in markdown format.
4. Return the Confluence page URL to the user once created.

If MCP is not connected, save the PRD as a markdown file instead: `PRD-[product-name].md` and confirm the file path to the user.

## Notes

- Be specific and data-driven where possible
- Link each section back to the overall strategy
- Flag assumptions clearly so the team can validate them
- Keep the document concise but complete
- Avoid using acronyms, don't use em dashes anywhere

**Confluence formatting rules — apply when publishing:**
- No horizontal rules (`---`) between sections. Confluence renders these as visual dividers that break PDF export.
- No `>` symbol at the start of table cells. Confluence parses this as a blockquote, creating an unwanted vertical bar. Write "above 30%" not ">30%", "below 10%" not "<10%".
- Bold only for metrics that are the core of a claim, or key decisions that need to stand out when scanning. Never bold entire sentences or to fill visual space.
- No emojis in body content (sections 1–10). Emojis are only used in the header block metadata table.
- Tables preferred over bullet lists for structured comparisons.

## The 5 Core Skills

---

### Skill 1: Problem Sharpening

**Bad:**
> "Users are dropping off during onboarding"

**Good:**
> "Only 10% of new users successfully onboard onto a product 
> post-activation. Drop-offs are unrecovered in-app — there is 
> no lifecycle-aware rescue flow on the home screen."

**The technique:**
```
Step 1: State the symptom
Step 2: Add the number
Step 3: Add the consequence
Step 4: Add why current state can't fix it

Template:
"[X% of users] experience [specific friction]
at [specific moment], resulting in [measured outcome].
Currently [no mechanism exists / wrong mechanism is used]
to address this."
```

---

### Skill 2: Metric Selection

Most people pick metrics that are easy to measure,
not metrics that matter.

**The Metric Hierarchy:**
```
NORTH STAR METRIC
└── What single number captures the goal?
    e.g. M1 Retention

PRIMARY METRICS (2-3)
└── What directly moves the north star?
    e.g. % users doing 3+ txns in 14 days

SECONDARY METRICS (2-4)
└── What are early signals we're on track?
    e.g. CTR on lifecycle widgets

GUARDRAIL METRICS
└── What must NOT get worse?
    e.g. App crash rate, CSAT score
```

**Common mistake to avoid:**
Setting targets without baselines.

```
Wrong:
"Increase BillPay adoption"

Right:
"Increase BillPay adoption from 2.5% → 3%
in non-TPAP cohorts within 60 days of launch"
```

---

### Skill 3: Scoping Decisions

The hardest part of a PRD isn't what to include.
It's what to explicitly exclude.

**Framework:**
```
For every potential feature, ask:

1. MUST HAVE     Breaks core experience if absent?
2. SHOULD HAVE   Significantly improves outcome?
3. NICE TO HAVE  Good but not outcome-critical?
4. NOT NOW       Valid but wrong timing or phase?
5. NEVER         Out of scope for this PRD entirely?
```

**Rule:**
Every out-of-scope item should say WHEN it will be addressed.

```
Good example:
Out of Scope for Phase 1:
✓ Phase 2 progression list widget     → Phase 2
✓ Savings account card redesign       → Phase 2
✓ AA linking / Investments onboarding → Phase 3
```

---

### Skill 4: Writing for Multiple Readers

A PRD has 4 audiences with different needs:

```
READER           WHAT THEY NEED
──────────────────────────────────────────────
Engineering      Exact specifications, edge cases,
                 technical constraints, APIs needed

Design           User states, flows, principles,
                 component hierarchy, content rules

Data/Analytics   Metric definitions, tracking events,
                 experiment design, cohort logic

Leadership       Business case, ROI, risk, timeline,
                 strategic fit
```

**Technique:**
Write once, signal to each audience via section headers.

```
→ "Technical Considerations"  for Eng
→ "Design / UX Principles"    for Design
→ "Tracking Requirements"     for Data
→ "Success Metrics"           for Leadership
```

---

### Skill 5: The "So What" Test

After every claim in your PRD, ask: "So what?"

```
WEAK CHAIN:
"We have low M3 retention"

STRONGER CHAIN:
"We have low M3 retention (~18%)"
→ So what?
"Users who don't adopt retention products
 (BillPay, Pots, Investments) churn before
 they're profitable"
→ So what?
"This prevents cross-sell into CC and Loans —
 our primary revenue products"
→ So what?
"AOP revenue targets cannot be hit without
 fixing this funnel"
```

Each "so what" makes the business case harder to dismiss.

---

## Red Flags Checklist

Before submitting any PRD, verify:

```
PROBLEM SECTION
□ Every problem has a data point
□ Data is sourced — not "we think" or "probably"
□ User impact is described, not just business impact
□ Root cause is identified, not just symptom

SOLUTION SECTION
□ At least 2 alternatives were considered
□ Why this solution vs alternatives is explained
□ Dependencies on other teams are named
□ Edge cases are handled, not deferred

METRICS SECTION
□ Baseline numbers exist for all targets
□ Guardrail metrics are defined
□ Measurement method is specified
□ Timeline for measurement is set

EXECUTION SECTION
□ Phases are clearly bounded
□ Out of scope is explicitly listed
□ Open questions have owners and deadlines
□ Rollback plan exists
```

---

## The One-Page PRD

For smaller features, compress the PRD to this:

```
PROBLEM
In one sentence: what is broken and how do we know?
[Data point]

WHY NOW
One reason this can't wait.

SOLUTION
What we're building in 3 bullet points.

SUCCESS LOOKS LIKE
[Metric]: [Current] → [Target] by [Date]

OUT OF SCOPE
3 things we are explicitly NOT doing.

OPEN QUESTIONS
[Question] | Owner: [Name] | Due: [Date]
```

---

## PRD Quality Levels

```
LEVEL 1 — DRAFT
• Problem is described qualitatively
• Solution is roughly defined
• No metrics

LEVEL 2 — REVIEW READY
• Problem has supporting data
• Solution has scope and phasing
• Success metrics defined with baselines

LEVEL 3 — EXECUTION READY
• All edge cases handled
• Tracking instrumentation specified
• Experiment design included
• Rollback plan exists
• All stakeholders have reviewed

LEVEL 4 — EXCELLENT
• Alternative solutions evaluated
• Cost/ROI analysis included
• User research cited
• Phased metrics per launch stage
• Post-launch review plan defined
```

---

## Summary Table

| Dimension          | What to Master                                              |
|--------------------|-------------------------------------------------------------|
| Problem writing    | Symptom + number + consequence + why current state fails    |
| Metric selection   | North star → primary → secondary → guardrails               |
| Scoping            | Explicit in AND explicit out, per phase                     |
| Audience writing   | One doc, four readers, clear signposting                    |
| Business case      | Chain of "so what" until revenue/retention impact           |
| Risk thinking      | Edge cases resolved, not deferred                           |
| Experiment design  | How will you know which change caused what?                 |

---

## The Core Principle

> The best PRDs don't just describe what to build.
> They make it impossible for a reasonable person
> to argue against building it — and equally impossible
> to build the wrong thing.

---

### Further Reading

- [How to Write a Product Requirements Document? The Best PRD Template.](https://www.productcompass.pm/p/prd-template)
- [A Proven AI PRD Template by Miqdad Jaffer (Product Lead @ OpenAI)](https://www.productcompass.pm/p/ai-prd-template)
