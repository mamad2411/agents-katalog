---
name: project-scope-change
description: "Writes scope change request documents with impact assessment, revised timeline, and cost adjustments for client projects."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Project Scope Change

## When to Use This Skill

Use this skill when you need to:
- Document a scope change request during an active client project
- Assess the timeline and cost impact of requested changes
- Present change options to the client in a professional format
- Protect your project boundaries while accommodating client needs

**DO NOT** use this skill for initial scope of work creation, contract amendments, or post-project change orders. This is for mid-project scope change management.

---

## Core Principle

EVERY SCOPE CHANGE HAS A COST — TIME, MONEY, OR BOTH. YOUR JOB IS TO MAKE THAT TRADE-OFF VISIBLE TO THE CLIENT SO THEY CAN MAKE AN INFORMED DECISION.

---

## Phase 1: Change Assessment

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Original scope reference** | "What was the agreed scope? Share the SOW or project brief." | No default — must be provided |
| **Requested change** | "What is the client asking to add, remove, or modify?" | No default — must be provided |
| **Who requested it** | "Did the client request this, or did the need arise during work?" | Client requested |
| **Current project status** | "Where are you in the project timeline?" | Mid-project |
| **Urgency** | "Does this change need a decision immediately, or can it wait?" | Non-urgent — decision within 5 business days |

**GATE: Confirm the original scope and the requested change before drafting the impact assessment.**

---

## Phase 2: Impact Analysis

### Change Impact Template

```
## Scope Change Request — [Project Name]

**Date:** [Date]
**SCR #:** [Sequential number]
**Requested by:** [Client name]
**Assessed by:** [Your name]

---

### Change Description

[Clear, specific description of what the client wants to add, modify, or remove.
Use their words where possible, then clarify with specifics.]

### Impact Assessment

| Factor | Original Scope | With Change | Difference |
|--------|---------------|-------------|------------|
| Timeline | [X] weeks | [Y] weeks | +[Z] weeks |
| Budget | $[amount] | $[amount] | +$[amount] |
| Deliverables | [count/list] | [count/list] | +[count] |
| Resources | [who] | [who + additional] | [additional needs] |

### Risk Assessment

- **Timeline risk:** [Does this push the deadline? Conflict with other milestones?]
- **Quality risk:** [Does rushing this change compromise other deliverables?]
- **Dependency risk:** [Does this change affect other parts of the project?]
- **Budget risk:** [Does this approach the client's budget ceiling?]
```

---

## Phase 3: Options Presentation

### Present Three Options

Always give the client choices, not ultimatums:

```
### Option A: Approve Change (Full Scope)

Add the requested change with full impact:
- Additional cost: $[amount]
- Extended timeline: +[X] days/weeks
- New completion date: [date]

### Option B: Approve Change with Trade-off

Add the requested change but remove or defer something else:
- Swap [new item] for [existing deliverable to defer]
- No additional cost
- Timeline impact: [minimal / none / +X days]

### Option C: Defer Change

Complete the original scope as planned and address this change in a follow-up phase:
- No impact on current timeline or budget
- Change quoted separately for Phase 2 at $[amount]
- Can begin immediately after current project delivery

### Recommended Option: [A/B/C]

[1-2 sentences explaining why you recommend this option based on the client's goals.]
```

---

## Phase 4: Documentation & Approval

### Change Order Form

```
## CHANGE ORDER

**Project:** [Name]
**SCR #:** [Number]
**Date:** [Date]

**Description of change:**
[Specific change description]

**Selected option:** [A / B / C]

**Revised timeline:** [New completion date]
**Additional cost:** $[amount]
**Revised total project fee:** $[amount]

**Payment for change:** [Due upon approval / Added to next milestone / Billed separately]

---

**Client approval:**

Signature: _______________
Name: _______________
Date: _______________

**Provider acknowledgment:**

Signature: _______________
Name: _______________
Date: _______________
```

### Communication Template

```
Subject: Scope Change Request — [Project Name] — SCR #[X]

Hi [Client Name],

Following our discussion about [brief description of change], I've assessed
the impact on our project timeline and budget.

I've attached a formal Scope Change Request with three options for how we
can handle this. Here's a quick summary:

- **Option A:** Full change — adds $[X] and [X] days
- **Option B:** Change with trade-off — no additional cost, swap [X] for [Y]
- **Option C:** Defer to Phase 2 — no impact on current project

I recommend Option [X] because [brief reason].

Please review and let me know which option you'd like to go with.
I'll hold the current project timeline until I hear from you.

[Your name]
```

### Process Checklist

- [ ] Change is documented in writing (not just verbal agreement)
- [ ] Impact on timeline, budget, and deliverables is assessed
- [ ] Three options presented with a recommendation
- [ ] Client approves in writing before work begins
- [ ] Change order is signed and filed with the original SOW
- [ ] Project plan is updated to reflect the approved change

---

## Anti-Patterns

- **Absorbing changes silently** — doing extra work without documenting it trains clients to expect free scope expansion.
- **Presenting changes as problems** — frame changes as options, not obstacles. The client should feel in control.
- **Only offering "yes at extra cost"** — always include a trade-off or deferral option. Flexibility builds trust.
- **Verbal agreements** — "Sure, I'll add that" without a written change order leads to disputes about what was agreed.
- **Delaying the conversation** — address scope changes immediately. The longer you wait, the more complicated the project becomes.

---

## Recovery

- **Client pushes back on additional cost:** Show the impact math transparently. If they cannot afford it, recommend Option B (trade-off) or C (deferral).
- **Multiple changes accumulating:** Batch small changes into a single change order. If changes are constant, pause and re-scope the entire project.
- **Client says "this should have been in the original scope":** Reference the SOW and exclusions list. If the original scope was genuinely ambiguous, negotiate a fair split.
- **Change is urgent and cannot wait for formal approval:** Get verbal approval, start work, and send the written change order immediately for retroactive sign-off.
- **You caused the scope change:** Own it. If your work uncovered a need that was not in the original scope, present options without charging for your oversight.
