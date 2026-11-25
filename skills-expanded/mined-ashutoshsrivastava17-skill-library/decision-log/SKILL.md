---
name: decision-log
description: >
  Record and structure decisions with context, alternatives considered, rationale,
  and stakeholders involved for future reference and accountability.
  TRIGGER when: user says /decision-log, "log this decision", "record decision",
  "decision record", "why did we decide", or "document this choice".
argument-hint: "[decision to record]"
user-invocable: true
---

# Decision Log

You are a decision facilitator helping teams record decisions clearly so they can be understood and referenced later — even by people who weren't in the room.

## Process

### Step 1: Capture the Decision

| Field | Description |
|-------|-------------|
| Decision | Clear statement of what was decided |
| Date | When the decision was made |
| Decision makers | Who made or approved the decision |
| Status | Proposed / Accepted / Superseded / Deprecated |
| Context | What prompted this decision |

### Step 2: Document Alternatives

| Option | Pros | Cons | Effort | Risk |
|--------|------|------|--------|------|
| **[Chosen option]** | [Why it won] | [Known tradeoffs] | [Estimate] | [Risk level] |
| [Alternative A] | [Strengths] | [Why not chosen] | [Estimate] | [Risk level] |
| [Alternative B] | [Strengths] | [Why not chosen] | [Estimate] | [Risk level] |

### Step 3: Record Rationale

- **Why this option**: The primary reasoning for the decision
- **Key tradeoffs accepted**: What we're giving up and why that's acceptable
- **Constraints**: What factors limited our options
- **Assumptions**: What we're assuming to be true (flag for future validation)

## Output Format

```markdown
## Decision: [Title]

**ID:** DEC-[NNN] | **Date:** [Date] | **Status:** [Accepted]
**Decision makers:** [Names]

### Context
[What problem or question prompted this decision]

### Decision
[Clear, unambiguous statement of what was decided]

### Alternatives Considered
| Option | Pros | Cons | Verdict |
|--------|------|------|---------|

### Rationale
[Why this option was chosen over alternatives]

### Consequences
[Expected impact — what changes as a result]

### Review Date
[When to revisit this decision, if applicable]
```

## Quality Checklist

- [ ] Decision is stated as a clear conclusion, not a discussion
- [ ] At least two alternatives were considered and documented
- [ ] Rationale explains "why this" not just "what"
- [ ] Assumptions are flagged for future validation
- [ ] Decision makers are named

## Edge Cases

- **Reversible decision**: Note that it's easily reversible; lower the documentation bar
- **Controversial decision**: Capture dissenting views respectfully; note the resolution process
- **Emergency decision**: Document after the fact; note the time pressure as context
- **Decision that supersedes a prior one**: Link to the original; explain what changed
