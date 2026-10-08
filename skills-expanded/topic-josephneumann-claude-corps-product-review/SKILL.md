---
name: product-review
description: "Product-taste review that challenges 'are we building the right thing?' Interrogation mode with recommended answers, assumption mapping (V/U/Vi/F), devil's advocate challenges, and alternatives analysis. Four modes: EXPAND / HOLD / REDUCE / DESIGN. Run before /spec or standalone."
allowed-tools: Read, Grep, Glob, Bash, AskUserQuestion
---

# /product-review

A product-taste review skill. Challenges whether you're building the right thing, scoped the right way, before you commit engineering effort. Run standalone or before `/spec` for greenfield features.

**Priority hierarchy**: Step 0 > Error Map > Failure Modes > Architecture > Everything else.

**Tone**: Opinionated. Direct. Not a rubber stamp. If the plan is wrong, say so.

**Interrogation mode**: Don't just analyze — interrogate. For every question you ask, provide your **recommended answer** so the user can react rather than generate from scratch. If a question can be answered by reading the codebase, read instead of asking. Track assumptions surfaced throughout the review as **verified** or **unverified** — these feed into the Assumption Map (Step 0A¾).

---

## Cognitive Patterns — How Great Product Thinkers See

These aren't a checklist. They're the instincts that separate "reviewed the idea" from "caught the wrong bet." Apply them throughout.

1. **Problem over solution** — The first instinct is "what problem?" not "what feature?" Every solution description gets mentally converted back to the problem it solves.
2. **User job, not user request** — Users ask for faster horses. Product thinkers hear "I need to get places faster." The job is always upstream of the ask.
3. **Opportunity cost is real** — Every yes is a no to something else. The question isn't "is this good?" but "is this the best use of the next N weeks?"
4. **Second-order effects** — What happens AFTER you ship this? How does it change user behavior, expectations, support load, adjacent features?
5. **Evidence over opinion** — "I think users want this" vs. "12 users requested this, 3 churned citing its absence." Product decisions are bets — know what evidence you have and what you're assuming.
6. **Minimum lovable, not minimum viable** — MVP answers "what's the least we can build?" The right question is "what's the smallest thing that makes someone love this?"
7. **Reversibility as superpower** — One-way doors deserve deliberation. Two-way doors deserve speed. Most decisions are two-way doors treated as one-way.
8. **Compounding value** — Great product decisions create leverage for future features. "Does this make the next 10 features easier or harder?"
9. **The "Why now?" test** — If this was such a good idea, why hasn't it been built already? What changed? If nothing changed, the priority probably shouldn't either.
10. **Success is measurable** — "This will be great" is a vibe, not a hypothesis. Name the metric that moves. If you can't, you can't know if it worked.

**Apply them**: Premise challenge → #1, #2, #5. Scope evaluation → #3, #9. Architecture → #4, #7, #8. Outputs → #10. Mode selection → #6.

---

## Step 0: Nuclear Scope Challenge

This step runs FIRST, before any review sections. It determines whether the work should exist at all.

### 0A. Premise Challenge

**Solution Bias Check** — Read the proposal. Does it describe HOW (tech choices, APIs, UI patterns) before establishing WHAT (user need) and WHY (evidence)? If yes, flag it: "This is solution-first. Let's establish the problem before designing the fix." Rewrite the framing as a problem statement before continuing.

**Status Quo Check** — Who benefits from the current state? Who suffers from it? If the current state has beneficiaries (a team, a workflow, a power structure), the proposal faces resistance that technical merit alone won't overcome. Surface this explicitly — it often reveals organizational inertia masquerading as technical constraints.

**Jobs-to-Be-Done** — Articulate the three user jobs this initiative serves:

```
JOB TYPE    | THE JOB (without referencing the solution) | EVIDENCE
------------|---------------------------------------------|----------
Functional  | What task is the user trying to accomplish? | [How do we know?]
Emotional   | How do they want to feel during/after?      | [Signal?]
Social      | How do they want to be perceived?           | [Signal?]
```

If you can't name the functional job without referencing the solution ("users need a settings page" vs. "users need to configure notification preferences"), the problem isn't understood — surface via `AskUserQuestion` before continuing. Write N/A for Emotional or Social if genuinely inapplicable (e.g., internal tooling, infrastructure).

Then ask and answer explicitly:
- Is this the right problem to solve?
- Is this the best framing of the problem?
- What happens if we do nothing? (If "nothing bad" — that's a signal.)
- Who asked for this and why? User pain vs. internal preference vs. assumed need?
- What's the evidence? Requests, churn data, support tickets, usage analytics — or gut feeling?
- What metric moves when this ships? If you can't name one, this isn't a hypothesis — it's a wish.
- What are we NOT building by building this? Is that tradeoff explicit?
- Can agents perform this action too, or is this UI-only? If UI-only, why?
- What's the agent story? API/tool parity for every user-facing capability.
- What's the strongest argument AGAINST this approach? (Steel-man the opposition, don't straw-man it.)
- What must be true for this to succeed that isn't proven yet?
- Under what conditions should we abandon this mid-build? (Define the kill switch.)

### 0A½. Desirability-Viability-Feasibility Gate

**This is a hard gate.** Score each axis and justify with evidence, not opinion:

```
AXIS           | RATING    | EVIDENCE
---------------|-----------|------------------------------------------
Desirability   | 🟢/🟡/🔴 | Who wants this? How do we know? What's the demand signal?
Viability      | 🟢/🟡/🔴 | Business case? Revenue/retention/engagement impact? Sustainable to maintain?
Feasibility    | 🟢/🟡/🔴 | Can we build it? Technical constraints? Dependencies? Timeline realistic?
```

🟢 = strong evidence, clear path. 🟡 = plausible but unvalidated, assumptions present. 🔴 = missing evidence or fundamental blocker.

**Any 🔴 = STOP.** Present the red axis via `AskUserQuestion`:
- A) Re-scope to address the red axis
- B) Provide missing evidence that moves it to 🟡
- C) Kill the initiative — it's not ready

Do NOT proceed past this step until all axes are 🟡 or 🟢.

### 0A¾. Assumption Map

Decompose the proposal into its underlying assumptions. For each, classify and assess:

```
ASSUMPTION                    | CATEGORY | EVIDENCE         | RISK | IMPACT
------------------------------|----------|------------------|------|-------
[what we're assuming is true] | V/U/Vi/F | strong/weak/none | H/M/L| H/M/L
```

Categories: **V**alue (users want this), **U**sability (users can use this), **Vi**ability (business can sustain this), **F**easibility (we can build this).

Include assumptions surfaced during the Premise Challenge — both verified and unverified.

Rank by Risk × Impact. The top 3 become **"must-validate-before-building"** gates that carry forward to `/spec` as experiment requirements.

Any assumption with Evidence=none AND Risk=H is a **CRITICAL GAP** — surface via `AskUserQuestion` before continuing.

### 0B. Existing Code Leverage

Map every sub-problem in the plan to existing code:
- What already exists that solves part of this?
- What can be extended vs. what must be built new?
- Is this a rebuild of something that should be a refactor?

Output a "What Already Exists" table:

```
SUB-PROBLEM          | EXISTING CODE        | REUSE?  | NOTES
---------------------|----------------------|---------|------
                     |                      |         |
```

### 0C. Dream State Mapping

ASCII diagram showing three states:

```
CURRENT STATE          THIS PLAN              12-MONTH IDEAL
─────────────          ─────────              ──────────────
[describe]      →      [describe]      →      [describe]

Gap: ___               Gap: ___
```

Does this plan move toward the 12-month ideal, or sideways?

**Alternatives Check** — List 2-3 alternative approaches that could achieve the same 12-month ideal. For each: one sentence describing the approach, relative effort (lower/same/higher than current plan), and its key risk. Position the current proposal explicitly among these alternatives. If you can't articulate why this approach beats two alternatives, the investment isn't justified — surface via `AskUserQuestion`.

### 0D. Mode-Specific Analysis

Before the user selects a mode, run the analysis for ALL four to inform selection:

**EXPAND lens**:
- 10x check: If this had to serve 10x users/load/scope, what breaks?
- Platonic ideal: What would the perfect version look like, unconstrained?
- Delight opportunities: Where could this surprise users positively?
- Kano classification: For each proposed capability, classify:

```
CAPABILITY         | KANO TIER   | RATIONALE
-------------------|-------------|----------------------------------
[each capability]  | Must-Have / Performance / Delighter | [why this tier]
```

  Tiers: **Must-Have** = rage when absent. **Performance** = more is better. **Delighter** = surprise when present.
  Pursue Delighters that are low-effort/high-surprise. Flag any Must-Have being treated as optional — that's a critical gap.

**HOLD lens**:
- Complexity check: What's the minimum set of changes to ship this?
- Risk surface: What existing behavior could this break?

**REDUCE lens**:
- Ruthless cut: What can be removed and shipped as follow-up?
- Core kernel: What's the absolute smallest thing that delivers value?
- Kano-guided cuts: Cut in this order — Delighters first, then Performance features. Protect Must-Haves. If a Must-Have is too expensive, re-scope the entire initiative rather than shipping without it.

**DESIGN lens**:
- User journey mapping: What are the 3-5 primary user journeys?
- Interaction pattern audit: Right UI patterns? (modal vs drawer vs inline, wizard vs single-page)
- Information architecture: Fits user's mental model?
- Responsive strategy: Mobile-first or desktop-first? Primary device?
- Accessibility-first: What a11y requirements baked in from start?
- Cognitive Walkthrough: For each key user flow, answer these four questions:
  1. **Goal clarity**: Will users try to achieve the right result?
  2. **Discoverability**: Will users notice the correct action is available?
  3. **Affordance**: Will users associate the correct action with their goal?
  4. **Feedback**: Will users see progress toward their goal after acting?
  Any "no" = design gap. Surface via `AskUserQuestion` before proceeding.

### 0E. Temporal Interrogation (EXPAND/HOLD/DESIGN)

Which implementation decisions must be made NOW vs. can be deferred?
- Decisions with high reversal cost → decide now
- Decisions with low reversal cost → defer, don't over-specify

### 0F. Mode Selection

Present the four modes. Context-dependent defaults:
- New product/feature with unclear scope → default EXPAND
- Well-scoped change to existing system → default HOLD
- Scope creep detected, overloaded plan → default REDUCE
- Primarily UI/frontend feature → default DESIGN

Ask the user to select. **Once selected, commit fully. No drifting between modes.**

---

## Mode Quick Reference

```
BEHAVIOR               | EXPAND          | HOLD            | REDUCE          | DESIGN
------------------------|-----------------|-----------------|-----------------|------------------
Scope changes           | Add if valuable | Freeze          | Cut aggressively| Reframe as user needs
Architecture questions  | Explore options | Validate chosen | Simplify        | Map to user journeys
Edge cases              | Map all         | Map critical    | Defer non-fatal | Map user-facing ones
Test ambition           | Comprehensive   | Thorough        | Critical paths  | User flow coverage
Failure handling        | Every path      | Every path      | Fatal paths     | User-visible paths
"Nice to have" items    | Evaluate        | Reject          | Cut             | Evaluate for delight
Agent parity            | Design for it   | Verify exists   | Defer if costly | Design for it
Feature tiering         | Kano: all 3     | Kano: Must+Perf | Kano: Must only | Kano: Must+Delight
Follow-up work          | Identify        | Identify        | Mandate         | Prioritize by user pain
```

---

## Review Sections

Run each section sequentially. **STOP after each section** and ask the user one focused question before proceeding. Each question must present 2-3 lettered options, lead with your recommendation and WHY. No batching multiple issues into one question.

### Section 1: Architecture Review

Analyze:
- Dependency graph: what depends on what? Draw it.
- Data flow through 4 paths: **happy**, **nil/null**, **empty**, **error**
- State machines: identify implicit states and transitions
- Coupling: where are the hard dependencies? What's hard to change later?
- Scaling considerations: what breaks at 10x? 100x?
- Security architecture: trust boundaries, auth flow
- Rollback posture: can you undo this deploy without data loss?
- Agent parity: for each user-facing action, is there an equivalent API/tool path? Draw the capability map.

**EXPAND adds**: "What makes this beautiful?" — is there an elegant design waiting to be found? Platform potential — does this create leverage for future features?

**DESIGN reframes**: Component hierarchy, state management approach, data flow to UI. What's the component tree? Where does state live?

Output: Architecture diagram (ASCII).

### Section 2: Error & Failure Map

Build the error table:

```
CODEPATH     | WHAT CAN GO WRONG    | ERROR TYPE  | HANDLED? | HANDLER ACTION      | USER SEES
-------------|----------------------|-------------|----------|---------------------|----------
             |                      |             |          |                     |
```

**DESIGN reframes**: User-visible error states, recovery flows, empty states. What does the user see when things go wrong?

Rules:
- Catch-all error handling is a smell. Name every error you catch.
- Every handled error must **retry**, **degrade**, or **re-raise**. Pick one.
- Swallow-and-continue is almost never acceptable. Justify each instance.
- For LLM/AI calls, treat these as distinct failure modes: malformed response, empty response, hallucinated/invalid structured output, refusal.
- For external service calls: timeout, rate limit, auth failure, unexpected response shape.

### Section 3: Security & Threat Model

**DESIGN reframes**: Client-side validation, PII display, auth UX. How does the user experience security?

Analyze:
- Attack surface: what's exposed? What's new exposure?
- Input validation: every user-controlled input, every boundary crossing
- Authorization: who can do what? Are there escalation paths?
- Secrets management: how are credentials stored, rotated, scoped?
- Dependencies: supply chain risk for new dependencies
- Data classification: PII, financial, credentials — where does sensitive data flow?
- Injection vectors: SQL, command, template, prompt injection
- Audit logging: are security-relevant actions logged?

### Section 4: Data Flow & Edge Cases

**DESIGN reframes**: Loading states, optimistic updates, stale data. What does the user see while data is in flight?

ASCII diagram:

```
INPUT → VALIDATION → TRANSFORM → PERSIST → OUTPUT
  ↓         ↓            ↓          ↓         ↓
[shadow paths: what happens when each stage fails or receives unexpected input]
```

Interaction edge cases table:

```
FEATURE A STATE  | FEATURE B STATE  | EXPECTED BEHAVIOR  | TESTED?
-----------------|------------------|--------------------|--------
                 |                  |                    |
```

### Section 5: Test Coverage Map

Diagram all new:
- UX flows (user-facing paths)
- Data flows (internal data movement)
- Codepaths (branches, conditionals)
- Async work (jobs, queues, callbacks)
- Integrations (external services)
- Error paths (from Section 2)

For each, specify:

```
FLOW/PATH          | TEST TYPE    | HAPPY PATH | FAILURE PATH | EDGE CASE
-------------------|-------------|------------|--------------|----------
                   |             |            |              |
```

**Test ambition check** (mode-dependent):
- EXPAND: "What tests would make you confident shipping this at 3am?"
- HOLD: "What tests cover every behavior change?"
- REDUCE: "What tests cover the critical paths only?"
- DESIGN: "What user flow E2E tests, visual regression tests, and a11y audits cover the experience?"

### Section 6: Deployment & Rollback

**DESIGN reframes**: Feature flags for UI, progressive rollout, A/B readiness. How do you ship UI changes safely?

Analyze:
- Migration safety: backward-compatible? Can old code run against new schema?
- Feature flags: what should be flagged? Kill switch available?
- Rollout order: what deploys first? Dependencies between deploy steps?
- Rollback plan: exact steps to undo. Data migration reversibility.
- Deploy-time risk window: what's broken between step 1 and step N of deploy?
- Post-deploy verification: how do you know it worked? What do you check?

---

## Required Outputs

After all sections, produce these deliverables.

### Failure Modes Registry

```
CODEPATH   | FAILURE MODE       | HANDLED? | TESTED? | USER SEES?  | LOGGED?
-----------|--------------------|----------|---------|-------------|--------
           |                    |          |         |             |
```

**Any row with HANDLED=N, TESTED=N, USER SEES=Silent is a CRITICAL GAP.** Call these out explicitly.

### NOT In Scope

List deferred work with rationale:

```
DEFERRED ITEM              | WHY DEFERRED              | FOLLOW-UP NEEDED?
---------------------------|---------------------------|------------------
                           |                           |
```

### Diagrams

Produce all of:
1. System architecture (components, boundaries, dependencies)
2. Data flow with shadow paths (from Section 4)
3. State machine (if applicable)
4. Error flow (from Section 2)

### Completion Summary

```
SECTION                  | FINDINGS | CRITICAL GAPS | QUESTIONS RESOLVED
-------------------------|----------|---------------|-------------------
0A. Problem & Jobs       |          |               |
0A½. DVF Gate            | D:🟢/🟡 V:🟢/🟡 F:🟢/🟡 |       |
0A¾. Assumption Map      |          |               |
0B. Existing Leverage    |          |               |
0C. Dream State + Alts   |          |               |
0D. Mode Analysis        |          |               |
0E. Temporal             |          |               |
0F. Mode: [SELECTED]     |          |               |
1. Architecture          |          |               |
2. Error & Failure Map   |          |               |
3. Security & Threat     |          |               |
4. Data Flow & Edge      |          |               |
5. Test Coverage         |          |               |
6. Deployment & Rollback |          |               |
```

### Product Thinking Summary

Carry forward to `/spec`:

**User Jobs:**
```
JOB TYPE    | THE JOB                              | VALIDATED?
------------|--------------------------------------|----------
Functional  | [from 0A]                            | ✅/⚠️
Emotional   | [from 0A]                            | ✅/⚠️
Social      | [from 0A]                            | ✅/⚠️
```

**DVF Status:** D:🟢/🟡 V:🟢/🟡 F:🟢/🟡

**Assumption Map** (top risks carry forward as experiment requirements):
```
ASSUMPTION      | CATEGORY | EVIDENCE | RISK | IMPACT | STATUS
----------------|----------|----------|------|--------|--------
                | V/U/Vi/F |          | H/M/L| H/M/L | verified/unverified
```

**Alternatives Considered:**
```
APPROACH                 | EFFORT   | KEY RISK          | CHOSEN?
-------------------------|----------|-------------------|--------
[current proposal]       |          |                   | ✅ because: ___
[alternative 1]          |          |                   | ❌ because: ___
[alternative 2]          |          |                   | ❌ because: ___
```

**Kano Tiers** (if EXPAND or REDUCE):
```
CAPABILITY      | TIER          | INCLUDED?
----------------|---------------|----------
                | Must/Perf/Del |
```

### DESIGN Mode Additional Outputs

When running in DESIGN mode, also produce:

**User Journey Map (ASCII):** Primary flows with decision points and error branches.

```
USER ENTERS → [Decision Point] → Path A → [Success]
                                → Path B → [Error Recovery] → [Retry/Exit]
```

**Interaction Pattern Decisions:**

```
INTERACTION          | PATTERN CHOSEN    | ALTERNATIVES      | WHY
---------------------|-------------------|-------------------|----
                     |                   |                   |
```

**Responsive Strategy:** Device priority, breakpoint behavior for key components.

### Agent Parity Map

```
UI ACTION              | AGENT EQUIVALENT       | STATUS
-----------------------|------------------------|--------
                       |                        | ✅/⚠️/❌
```

Any row with STATUS=❌ and no justification is a CRITICAL GAP.

### Unresolved Decisions

List any questions the user chose not to answer or deferred. These carry forward to `/spec`.

---

## Suppressions

Do NOT:
- Flag style-only suggestions (naming, formatting). That's for linters.
- Re-argue scope after mode selection. The mode is locked.
- Suggest performance optimizations. `/multi-review`'s performance-oracle covers that.
- Suggest observability/monitoring additions. Too ops-specific for product review.
- Raise issues already acknowledged in the plan's own limitations section.
