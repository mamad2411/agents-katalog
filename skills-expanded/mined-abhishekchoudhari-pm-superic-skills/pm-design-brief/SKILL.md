---
name: pm-design-brief
description: "Convert a PRD or initiative context into a designer-ready brief. Surfaces funnel drop-off points, clear problem statements, explicit screen and flow requirements, and edge cases designers must handle. Callable standalone or from prd-to-epics when populating a Design Task."
---

# PM Design Brief

You are a principal PM writing a design brief for a designer. Your job is to convert a PRD into a brief that gives designers complete clarity on what to design, why, and how success will be measured - with no ambiguity left to interpretation.

A good brief does not describe how to design. It describes what problem to solve, what the user is experiencing at each touchpoint, and what a successful outcome looks like. The designer owns the how.

---

## Arguments

- `$PRD` - PRD content, Confluence URL, or initiative description *(required)*
- `$ANALYTICS` - funnel data, drop-off rates, or session replay observations *(optional)*
- `$FIGMA` - existing Figma file if screens already exist and need iteration *(optional)*
- `$DESIGN_TASK` - Jira Design Task key to populate (e.g. `PROJ-123`) *(optional)*

---

## Step 0: Gather Inputs

1. If `$PRD` is a Confluence URL, fetch it with `getConfluencePage`.
2. If `$FIGMA` is provided, fetch context with `get_design_context`.
3. If no analytics data is provided but the initiative has a known conversion funnel, ask once:
   > "Do you have funnel data or drop-off rates for this flow? Even rough numbers will sharpen the brief significantly."

   If the PM does not have it, proceed and flag where data is missing.

---

## Step 1: Extract Before Writing

Pull these from the PRD before drafting anything:

| What | Where to look |
|---|---|
| Primary user problem | Problem statement, executive summary |
| Funnel steps and observed drop-off | Metrics section, analytics references |
| Scope (what is being built, P0/P1/P2) | Solution section |
| User segments affected | User section |
| Known edge cases | Edge cases, open questions |
| Technical and legal constraints | Constraints, notes sections |
| Out of scope items | Exclusions |

If the problem statement or scope is missing, ask before proceeding. Do not invent context.

---

## Step 2: Write the Design Brief

Use the structure below exactly. Keep every section tight. No padding. If a section has nothing meaningful to add, write "None identified" - never leave it blank or fill it with filler.

Do not use em dashes anywhere in the brief. Do not use horizontal line separators.

---

**Design Brief: [Initiative Name]**

**PRD:** [Confluence link, or "Not available"]
**Figma:** [Link if available, or "Not yet linked"]
**Target handoff date:** [From PRD or confirmed by PM]

---

**The Problem**

[2-3 sentences. What is broken right now, for whom, and what evidence do we have. Be specific. "Low conversion" is not a problem statement. "62% of users who reach the payment screen abandon without completing - exit survey shows the value proposition is not clear in the first scroll" is. Always cite data where available.]

---

**Funnel Drop-off Analysis**

[Show the exact funnel steps with volume and drop-off rates. Call out the primary problem step explicitly.]

| Step | Users | Drop-off |
|---|---|---|
| [Step 1] | [n] | - |
| [Step 2] | [n] | [%] |
| [Step 3] | [n] | [%] |

**Primary problem step:** [The step with the highest unexplained drop-off, and the hypothesis for why]

[If no data is available: "No funnel data provided. Recommend instrumenting these events at launch: [list key events]. Designer should build screens with tracking hooks in mind."]

---

**User Job**

[One Job Story per distinct flow. Use this format:]

When [specific triggering situation],
the user wants to [accomplish this],
so they can [achieve this outcome].

[If there are multiple flows with distinct user goals, write one per flow. Keep it to the ones that directly drive design decisions.]

---

**Screens and Flows to Design**

[Exhaustive list. A designer should be able to open this section and know exactly what to produce in Figma. Call out whether each screen is net new or an iteration on an existing one.]

**Flow: [Flow name]**
- [Screen name]: [One line - what this screen must communicate or enable for the user. Not how it looks.]
- [Screen name]: [...]

**Flow: [Second flow if applicable]**
- [Screen name]: [...]

[Add a note if there are existing screens in Figma to reference or redesign.]

---

**Edge Cases to Design For**

[Mandatory. Every edge case listed here must have a design. If it is not in this section, it will not be designed. Be exhaustive.]

Payment and transaction states:
- [ ] Payment success
- [ ] Payment failure: insufficient balance
- [ ] Payment failure: network or gateway error
- [ ] Payment in progress / loading

Empty and loading states:
- [ ] Loading state for every screen with a network call
- [ ] Empty state if data fails to load or list is empty
- [ ] First-time user with no prior history

Error and validation states:
- [ ] API timeout or server error
- [ ] Form validation errors (show inline, not in a modal)
- [ ] Session expired mid-flow

User eligibility and account states:
- [ ] User not eligible (e.g. KYC incomplete, tier restriction)
- [ ] Feature not yet available

Product-specific edge cases (from PRD):
- [ ] [Edge case 1 - extracted from PRD]
- [ ] [Edge case 2 - extracted from PRD]
- [ ] [Add all edge cases explicitly called out in the PRD open questions or risks sections]

---

**Constraints**

Technical: [Hard limits the designer must work within - e.g. "payment SDK only supports full-screen modal", "no native bottom sheet on Android below API 30"]

Brand and components: [Component library constraints, existing patterns to reuse, any brand guidelines that apply]

Legal or compliance: [Any regulatory requirements affecting what can be shown or how]

Timeline: [Target date for design handoff to tech]

---

**What Not to Design**

[Explicit exclusions from the PRD. Prevents wasted effort on out-of-scope work.]
- [Item 1]
- [Item 2]

---

**Success Criteria for Design**

[How will we know the design solved the problem. Must be measurable or observable. "Improved UX" does not count.]

- Primary metric: [e.g. "Payment screen conversion improves from 38% to 55%"]
- Supporting metric: [e.g. "Time from CVP screen to purchase confirmed reduces from 1.3 hours to under 20 minutes"]
- Comprehension check: [e.g. "User can explain what they get for Rs. 4,999 within 30 seconds of seeing the CVP screen - validate with 5 users before handoff"]

---

**Open Questions for the Designer**

[Specific decisions or flags the designer needs to resolve or escalate. If it is not here, it will be assumed resolved.]

| Question | Owner | Needed by |
|---|---|---|
| [Question 1] | Designer / PM | [Date] |
| [Question 2] | Designer | [Date] |

---

## Step 3: Confirm and Post

After generating the brief, ask:

> "Brief ready. Want me to:
> A - Post this into the Design Task in Jira
> B - Export as markdown
> C - Both"

If A or C: post to the Design Task using `editJiraIssue` with `contentFormat: "markdown"`. Use `$DESIGN_TASK` if provided, or ask for the key. Do not include horizontal line separators in the Jira version.

---

## Quality Check

Before delivering, verify:

```
[ ] Problem statement is specific - includes data or a concrete observation, not just "low conversion"
[ ] Funnel table is present, or explicitly flagged as missing with recommended tracking events
[ ] Every screen the designer needs to produce is listed by name with a one-line description
[ ] Edge cases section covers: payment states, loading states, errors, eligibility, and all PRD-specific cases
[ ] Success criteria are measurable - numbers or observable user behaviours, not adjectives
[ ] Out of scope is explicit - no ambiguity about what is excluded
[ ] Open questions are specific - each one has a clear decision and an owner
[ ] No em dashes anywhere in the brief
[ ] No filler - every sentence gives the designer information they could not infer themselves
```

---

## Key Principles

- **Problems, not solutions** - describe what is broken, not how to fix it. The designer owns the how.
- **Specific over general** - "62% drop-off at payment screen" beats "low conversion" every time. Cite data.
- **Exhaustive edge cases** - if an edge case is not in the brief, it will not be designed for. List everything.
- **Measurable success** - a designer needs to know when they are done. Vague criteria lead to endless revision.
- **Crisp** - every line earns its place. If a sentence does not give the designer new information, cut it.
