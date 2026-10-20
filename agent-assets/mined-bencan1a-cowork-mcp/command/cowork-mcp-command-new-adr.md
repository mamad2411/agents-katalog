# New Architecture Decision Record

Create a new ADR (Architecture Decision Record) in the cowork-mcp project.

**Topic:** $ARGUMENTS

## What To Do

### 1. Determine Next ADR Number

List existing ADRs in `docs/decisions/` and determine the next sequential number (e.g., if ADR-001 exists, the next is ADR-002).

If `docs/decisions/` does not exist yet, create it. The first ADR will be ADR-001.

### 2. Gather Context

Ask the user (if not provided via $ARGUMENTS):
- What decision needs to be recorded?
- What is the context or problem that prompted this decision?
- What alternatives were considered?
- What is the chosen approach and why?

### 3. Create the ADR

Write the ADR to `docs/decisions/ADR-{NNN}-{slug}.md` using this format:

```markdown
# ADR-{NNN}: {Title}

**Status:** Proposed | Accepted | Superseded | Deprecated
**Date:** YYYY-MM-DD
**Supersedes:** (if applicable)

## Context

{What is the problem or situation that requires a decision?}

## Decision

{What is the change being proposed or decided?}

## Alternatives Considered

| Alternative | Pros | Cons |
|-------------|------|------|
| {option} | {pros} | {cons} |

## Consequences

### Positive
- {benefit}

### Negative
- {trade-off}

### Neutral
- {observation}

## References

- {links to research, specs, or discussions}
```

### 4. Note the Decision

If `docs/CONTEXT.md` exists and has a "Key Decisions" section, add a one-line entry for the new ADR.
