---
name: decision-log
description: "Captures product decisions in a structured, searchable format inspired by Architecture Decision Records (ADRs). Documents the context, options considered, decision made, and consequences, creating institutional memory that prevents relitigating settled decisions and helps new team members understand why things are the way they are."
category: planning
default_depth: standard
---

# Decision Log / Product Decision Record (PDR)

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Captures product decisions in a structured, searchable format inspired by Architecture Decision Records (ADRs). Documents the context, options considered, decision made, and consequences, creating institutional memory that prevents relitigating settled decisions and helps new team members understand why things are the way they are.

## When to Use

- Any time a significant product decision is made (scope, strategy, prioritization, trade-off)
- When a decision is likely to be questioned later ("why did we do it this way?")
- During retrospectives when the team realizes decisions aren't being documented
- Onboarding new PMs or team members who need to understand historical context
- When the same decision keeps getting relitigated in meetings

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | S3 tactical decision; team-internal, easily reversible | PDR Template (Status through Decision only), Decision Log Entry |
| **Standard** | S2 significant decision; cross-team or multi-sprint impact | All sections |
| **Deep** | S1 strategic decision; changes product direction or requires exec approval | All sections + extended Options Considered with effort estimates, stakeholder influence context (from stakeholder-mapping if available, or inline assessment), formal Communication Summary with escalation plan |

**Omit rules:** At Light depth, skip Options Considered, Consequences, Revisit Criteria, and Communication Summary. Produce only the Decision Record core (Status, Date, Decision-Maker, Context, Decision) and a Decision Log Entry row.

## Framework

### Product Decision Record Template

```markdown
# PDR-[NNN]: [Decision Title]

## Status
[Proposed / Accepted / Deprecated / Superseded by PDR-XXX]

## Date
[Date decision was made]

## Decision-Maker
[Who made the final call, name and role]

## Participants
[Who was involved in the discussion]

## Context
[What situation or problem prompted this decision? Include relevant background, constraints, and timing pressures. Write this for someone who wasn't in the room.]

## Decision
[State the decision clearly and unambiguously in 1-3 sentences.]

## Options Considered

### Option A: [Name]
- **Description:** [What this option entails]
- **Pros:** [Advantages]
- **Cons:** [Disadvantages]
- **Estimated effort:** [If relevant]

### Option B: [Name] (CHOSEN)
- **Description:** [What this option entails]
- **Pros:** [Advantages]
- **Cons:** [Disadvantages, yes, document the downsides of the chosen path too]
- **Estimated effort:** [If relevant]

### Option C: [Name]
- **Description:** [What this option entails]
- **Pros:** [Advantages]
- **Cons:** [Disadvantages]

## Rationale
[Why Option B was chosen over the others. Be specific about the trade-offs that were made and the values or priorities that drove the decision.]

## Consequences

### What this enables:
- [Positive consequence 1]
- [Positive consequence 2]

### What this constrains:
- [Constraint 1, future options we're giving up]
- [Constraint 2]

### What we're accepting:
- [Known downside we're choosing to live with]
- [Technical debt or limitation we're taking on]

## Revisit Criteria
[Under what conditions should we reconsider this decision?]
- [Trigger 1, e.g., "If [metric] drops below [threshold]"]
- [Trigger 2, e.g., "If [assumption] turns out to be false"]
- [Trigger 3, e.g., "At the [Q3] strategy review"]

## Related Decisions
- [PDR-XXX]: [Related decision title]
- [PDR-YYY]: [Decision this supersedes or builds on]
```

### Decision Categories

Tag each PDR with a category for searchability:

| Category | Examples |
|---|---|
| **Scope** | "Descoped feature X from v1," "Added requirement Y" |
| **Strategy** | "Focus on SMB before enterprise," "Build vs. buy for Z" |
| **Prioritization** | "Chose initiative A over B for Q2" |
| **Technical** | "Selected Postgres over DynamoDB," "Adopted microservices" |
| **Design** | "Chose wizard over inline setup," "Adopted design system X" |
| **Pricing** | "Moved from per-seat to usage-based," "Added free tier" |
| **Process** | "Adopted 2-week sprints," "Changed release cadence" |
| **Partnership** | "Integrated with X instead of Y," "Selected vendor Z" |

### Decision Severity

| Severity | Criteria | Reversibility | Approval Required |
|---|---|---|---|
| **S1, Strategic** | Changes product direction, affects multiple teams | Hard to reverse | VP/C-level |
| **S2, Significant** | Affects scope, timeline, or resources for a major initiative | Moderate to reverse | PM + Engineering Lead |
| **S3, Tactical** | Affects current sprint or feature implementation details | Easy to reverse | PM or Tech Lead |

### Decision Log Index

Maintain a running index:

```markdown
## Decision Log, [Product Name]

| PDR | Date | Title | Category | Severity | Status |
|---|---|---|---|---|---|
| PDR-001 | 2026-01-15 | Focus on SMB before enterprise | Strategy | S1 | Accepted |
| PDR-002 | 2026-01-22 | Use event-driven architecture for notifications | Technical | S2 | Accepted |
| PDR-003 | 2026-02-03 | Descope advanced analytics from v1 launch | Scope | S2 | Accepted |
| PDR-004 | 2026-02-10 | Adopt usage-based pricing for API product | Pricing | S1 | Accepted |
```

## Minimum Evidence Bar

**Required inputs:** The decision being made (or already made), who made it, at least two options that were considered, and the reasoning for the chosen path.

**Acceptable evidence:** Meeting notes, Slack threads, verbal accounts from participants, prior PRDs or specs that constrained the decision, relevant metrics or data referenced during discussion.

**Insufficient evidence:** If the rationale behind the decision cannot be articulated beyond "we just decided," produce a partial PDR with the Rationale section marked `[TBD, requires: interview with decision-maker to capture reasoning and trade-offs]` and flag the artifact as draft-only.

**Hypotheses vs. findings:**
- **Findings:** Context, Decision, Options Considered, and Rationale must reflect what actually happened.
- **Hypotheses:** Consequences (especially long-term constraints) and Revisit Criteria may be forward-looking projections, label speculative consequences as "Expected."

## Output Format

Produce:
1. **Decision Record**, fully structured PDR for the specific decision
2. **Decision Log Entry**, row for the index
3. **Communication Summary**, who needs to be informed and how (for S1 and S2 decisions)

**Shipwright Signature (required closing):**
4. **Decision Frame**, Restate the chosen option as a trade-off statement ("We chose X over Y because Z"), confidence level tied to evidence quality, decision owner, decision date, revisit trigger
5. **Unknowns & Evidence Gaps**, Consequences not yet validated, assumptions underlying the rationale, options rejected without full evaluation
6. **Pass/Fail Readiness**, PASS if the PDR has a clear decision statement and documented rationale; FAIL if rationale is missing. (At Light depth, Options Considered is omitted, so the two-option requirement does not apply.)
7. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Only documenting the decision, not the alternatives**, Future teams need to know what was considered and rejected
- **Missing the "why"**, The rationale is the most important part; "we chose B" without "because X" is useless
- **No revisit criteria**, Without these, decisions are permanent by default even when conditions change
- **Documenting too late**, Write the PDR when the decision is made, not weeks later when memory has faded
- **Only documenting big decisions**, S3 decisions add up; a light-touch PDR is better than no record at all

## Weak vs. Strong Output

**Weak:**
> **Rationale:** We decided to go with Option B because it seemed like the best approach for our needs.

No specific trade-off articulated; a reader six months later learns nothing about why Option A was rejected.

**Strong:**
> **Rationale:** We chose event-driven notifications (Option B) over polling (Option A) because our p95 latency requirement of <200ms rules out polling's 5-second minimum delay, and the 3-week implementation cost is justified by eliminating the need to revisit this when we add real-time features in Q3.

Names the constraint, quantifies the trade-off, and connects the decision to a future roadmap item.
