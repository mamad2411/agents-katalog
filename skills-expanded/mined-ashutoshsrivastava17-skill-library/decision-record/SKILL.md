---
name: decision-record
description: >
  Write Architecture Decision Records (ADRs) — document context, decision,
  consequences, alternatives considered, and status for technical decisions.
  TRIGGER when: user says /decision-record, "write an ADR", "architecture decision",
  "document this technical decision", or "ADR".
argument-hint: "[technical decision to document]"
user-invocable: true
---

# Architecture Decision Record (ADR)

You are a software architect writing clear ADRs. Document technical decisions so future team members understand what was decided, why, and what alternatives were rejected.

## Process

### Step 1: Identify the Decision

| Field | Description |
|-------|-------------|
| Title | Short, descriptive name (e.g., "Use PostgreSQL for user data") |
| Status | Proposed / Accepted / Deprecated / Superseded by ADR-NNN |
| Date | When the decision was made |
| Deciders | Who participated in the decision |
| Technical area | Backend, frontend, infrastructure, data, security |

### Step 2: Write the ADR

Follow the standard ADR template:

#### Context
What is the technical problem or question? What forces are at play (requirements, constraints, team skills, timeline)?

#### Decision
State the decision clearly and concisely. Use active voice: "We will use X for Y."

#### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|------------|------|------|-------------|
| [Option A] | [Benefits] | [Drawbacks] | [Primary reason] |
| [Option B] | [Benefits] | [Drawbacks] | [Primary reason] |

#### Consequences

| Type | Consequence |
|------|------------|
| **Positive** | [Benefits gained] |
| **Negative** | [Trade-offs accepted] |
| **Neutral** | [Things that change but aren't better or worse] |

### Step 3: Link and Index

- Link to related ADRs (supersedes, depends on, relates to)
- Add to the project's ADR index/log
- Reference from relevant code or documentation

## Output Format

```markdown
# ADR-[NNN]: [Title]

**Status:** [Proposed/Accepted/Deprecated/Superseded]
**Date:** [YYYY-MM-DD]
**Deciders:** [Names]

## Context
[Problem statement and forces at play]

## Decision
[What we decided and why — 1-3 sentences]

## Alternatives Considered
| Alternative | Pros | Cons | Why Rejected |

## Consequences
- **Positive:** [Benefits]
- **Negative:** [Trade-offs]
- **Risks:** [What could go wrong]

## Related
- Supersedes: [ADR-NNN]
- Related: [ADR-NNN]
```

## Quality Checklist

- [ ] Decision is stated in clear, active language
- [ ] Context explains the "why" — not just the "what"
- [ ] At least two alternatives are considered
- [ ] Consequences include both positive and negative outcomes
- [ ] Status is set correctly
- [ ] Related ADRs are cross-linked

## Edge Cases

- **Reversible decision**: Still document it — note that it's low-cost to change later
- **Inherited decision**: Document decisions made before the team existed if they constrain current work
- **Decision by default**: If no explicit choice was made but a pattern emerged, document the implicit decision
- **Superseding an ADR**: Mark the old one as superseded; link both ways
