# Comprehensive Project Interview

## Purpose

Conduct an exhaustive interview using interactive questions to fully define a project before implementation begins. Continue asking questions until every aspect is unambiguous and the user confirms completeness.

## Execution Rules

1. Ask ONE question at a time
2. Wait for the answer before proceeding
3. Never assume or fill in answers
4. Follow up immediately on any ambiguity
5. Challenge stated requirements—ask "why" at least twice
6. Quantify everything (replace "fast" with "< 200ms")
7. Track which phases are complete

## Interview Phases

Work through each phase systematically. See [phases.md](phases.md) for detailed questions.

### Phase 1: Problem Space Discovery

Understand the underlying problem, not just the stated solution:

- What triggered the need for this?
- Who are the actual end users vs stakeholders?
- What happens if this doesn't get built?
- What existing solutions were rejected and why?

### Phase 2: User Journey & Edge Cases

- Walk through the exact user flow step-by-step
- What happens when X fails halfway through?
- How do users recover from mistakes?
- What's the offline behavior?

### Phase 3: Data & State Architecture

- What's the source of truth for each entity?
- What's the data lifecycle?
- Expected data volume in 1 year? 5 years?
- What needs to sync across devices/sessions?

### Phase 4: Integration Boundaries

- What external systems does this touch?
- What happens when an integration is down?
- What auth flows are required?

### Phase 5: Security & Authorization

- Who can see what? Who can do what?
- Row-level or field-level permissions?
- What PII exists?

### Phase 6: Performance & Scale

- Acceptable latency per operation?
- Expected concurrent users?
- What needs real-time vs eventual consistency?

### Phase 7: Error Handling & Observability

- What errors should users see vs hide?
- What metrics matter for success?
- How do you debug production issues?

### Phase 8: Non-Functional Requirements

- Deployment strategy?
- Testing strategy?
- Documentation requirements?

### Phase 9: Tradeoffs & Constraints

- Speed to market vs technical excellence?
- What technical debt is acceptable?
- What's explicitly out of scope?

### Phase 10: Validation & Acceptance

- How do we know this is done?
- What does success look like in 30/60/90 days?

## Question Patterns

See [question-patterns.md](question-patterns.md) for effective question types.

### DO Ask:

- "What happens when..." (edge cases)
- "How do you handle..." (error states)
- "What if two users simultaneously..." (concurrency)
- "What's the exact format of..." (data specifics)

### DON'T Ask:

- Questions with obvious answers from context
- Yes/no questions
- Multiple questions in one

## Completion Criteria

The interview is complete when:

1. Every entity and relationship is explicitly defined
2. All user flows have happy paths AND error paths
3. All integrations have contracts and failure modes
4. All authorization rules are explicit
5. All performance requirements are quantified
6. All scope boundaries are explicit
7. The user confirms nothing feels ambiguous

## Output

After completion, generate:

1. Requirements document with all specifications
2. Decision log with rationale
3. Open questions requiring research
4. Risk register with mitigations
