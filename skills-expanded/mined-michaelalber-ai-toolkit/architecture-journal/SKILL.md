---
name: architecture-journal
audience: professional
description: Lightweight ADR templates with retrospective prompts at 30/90/180 days — converts experience into transferable expertise. Use when making architecture decisions, recording technical choices, or reviewing past decisions to extract lessons.
disable-model-invocation: true
---

# Architecture Journal

> "Architecture decisions are the most important decisions we make — and the ones we most often fail to record. The cost of a forgotten decision is not the decision itself, but the weeks spent relitigating it."
> -- Michael Nygard, "Documenting Architecture Decisions"

## Core Philosophy

Experience without reflection is just time passing. This skill converts architecture decisions into transferable expertise through structured recording and timed retrospectives. The goal is not documentation — it is building judgment.

**The Journal Principle:** A decision recorded at the moment of choosing, reviewed at 30, 90, and 180 days, teaches more than a decade of unexamined experience.

**Non-Negotiable Constraints:**
1. **Alternatives must be named** — a decision with one option is a default, not a decision; push for at least two genuine alternatives
2. **Consequences are predictions** — record observable, checkable outcomes ("p99 under 200ms on /checkout"), never "better performance"
3. **Context is specific** — dates, numbers, constraints and forces, not "we needed it to be faster"
4. **Reviews happen at 30 / 90 / 180 days** — every recorded decision gets concrete review dates; overdue reviews are raised at session start
5. **Retrospectives are honest** — "would you make it again?" is answered against what is known now, and wrong calls are recorded as wrong

## Workflow

### CACR Loop — Recording a New Decision

Identify a decision that needs recording (triggers: "we decided to..." in a meeting or PR, evaluating two or more technical approaches, changing an existing architectural pattern, adopting or dropping a technology, any choice hard to reverse). User drafts the ADR using the standard template — title, status, context (forces/constraints/requirements), decision statement, alternatives with trade-offs, predicted consequences, and review schedule. Coach reviews the draft for completeness: are alternatives genuinely distinct? Is context specific enough to reconstruct the situation? Are consequences predictions (testable) or hopes (vague)? User improves the record and answers: "What did writing this down reveal about my reasoning?" "Am I more or less confident now?" "What would change my mind?"

ADR triggers to offer recording for: any meeting where "we decided" appears; any PR that changes infrastructure or architecture; any technology adoption or abandonment; any choice the team debates for more than one meeting.

### Retrospective Workflow — Reviewing Past Decisions

**30-Day Review (Early Signals):** Has the decision been implemented as described? Any unexpected friction? Are predicted positive consequences materializing? Any early negative signals? Would you still make the same decision?

**90-Day Review (Medium-Term Effects):** What has this decision enabled or prevented? What costs have materialized (technical debt, complexity, coupling)? Have any rejected alternatives proven to be better choices? Has the original context changed? What would you tell someone facing the same decision today?

**180-Day Review (Long-Term Consequences):** Was this a good decision? Be honest. What did you over-estimate or under-estimate? What pattern does this decision represent? If you could go back, what would you change about the decision process? Extract one transferable principle. Should this decision be superseded?

### Decision Inventory Review

Periodically (monthly recommended): list all active decisions with next review date, identify overdue reviews, check for contradictions between active decisions, look for patterns across recent decisions, extract learning themes.

**Load on demand — `references/operating-guide.md`:** Domain Principles, Knowledge Base Lookups (run them before the first phase), AI Discipline Rules, Anti-Patterns, Error Recovery.

## State Block

```
<journal-state>
mode: record | retrospective | review
current_adr: [ADR number and title, or "none"]
project_context: [project name or area]
decisions_recorded: [count of ADRs in this project]
decisions_due_for_review: [list of ADR numbers with overdue retrospectives]
last_action: [what was just completed]
next_action: [what should happen next]
</journal-state>
```

**Example:**
```
<journal-state>
mode: record
current_adr: ADR-0012 Adopt PostgreSQL for Order Service
project_context: order-management-platform
decisions_recorded: 11
decisions_due_for_review: [ADR-0003, ADR-0007, ADR-0009]
last_action: User identified a new database decision to record
next_action: Draft ADR using standard template
</journal-state>
```

## Output Templates

```markdown
# ADR-[NUMBER]: [TITLE]
**Date**: [YYYY-MM-DD] | **Status**: [Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]
**Deciders**: [who] | **Related ADRs**: [list or "none"]

## Context
[Forces, constraints, requirements — specific enough to reconstruct the situation: dates, numbers, SLAs]

## Decision
We will [decision].

## Alternatives Considered
[At least two. Each: Description, Pros, Cons, Why rejected]

## Consequences
**Expected Positive**: [specific, observable predictions]
**Expected Negative**: [specific, observable predictions]
**Risks**: [what could go wrong]

## Review Schedule
- 30-day: [DATE] | 90-day: [DATE] | 180-day: [DATE]
```

Full retrospective templates (30/90/180-day), decision inventory, and learning extract: `references/adr-templates.md` and `references/retrospective-prompts.md`.

**Reference files:**

- [ADR Templates](references/adr-templates.md) — Standard and lightweight ADR formats, naming conventions, example ADRs, project organization guidance
- [Retrospective Prompts](references/retrospective-prompts.md) — Detailed question sets for 30/90/180-day reviews, cross-decision pattern analysis, learning extraction techniques

## Integration with Other Skills

- **`architecture-review`** — Use architecture-review for evaluating current system state; use architecture-journal for recording and reviewing decisions over time. Architecture reviews often surface decisions that should be recorded as ADRs.
- **`pattern-tradeoff-analyzer`** — Use it when evaluating which pattern to apply. Record the decision as an ADR — the trade-off analysis becomes the "Alternatives Considered" section.
- **`technical-debt-assessor`** — Technical debt often originates from architecture decisions. When debt is identified, check for a related ADR; if absent, write a retrospective ADR.
- **`dependency-mapper`** — Dependency maps reveal the consequences of architecture decisions. Use at 90/180-day reviews to see how decisions affected coupling and dependencies.
