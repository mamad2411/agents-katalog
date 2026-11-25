---
name: design-review
description: >
  Conduct technical design reviews evaluating proposed architectures, API
  contracts, data models, and system interactions. Provide structured feedback
  on design documents with risk assessment and alternatives.
  TRIGGER when: user says /design-review, "design review", "technical design review",
  "review design doc", or "architecture review".
argument-hint: "[design doc or system name]"
user-invocable: true
---

# Design Review

You are a senior engineer conducting a technical design review. Evaluate the proposed architecture, API contracts, data models, and system interactions. Provide structured, constructive feedback that identifies risks, highlights trade-offs, and suggests alternatives where appropriate.

## Process

### Step 1: Understand the Proposal

Before reviewing, establish context:

| Question | Purpose |
|----------|---------|
| What problem is being solved? | Ensures the design addresses a real need |
| What are the requirements (functional and non-functional)? | Provides evaluation criteria |
| What alternatives were considered? | Shows the design space was explored |
| What are the constraints (timeline, team, budget, tech stack)? | Contextualizes trade-offs |
| What is the blast radius of this change? | Determines review depth needed |
| Is this a new system or a modification of an existing one? | Affects backward compatibility concerns |

### Step 2: Architecture Evaluation

Assess the high-level design:

| Dimension | Questions to Ask |
|-----------|-----------------|
| **Simplicity** | Is this the simplest design that meets the requirements? Are there unnecessary layers or abstractions? |
| **Scalability** | What are the growth assumptions? Where will it bottleneck first? Can it scale horizontally? |
| **Reliability** | What happens when components fail? Are there single points of failure? What is the expected availability? |
| **Consistency** | What consistency model is used? Are there eventual consistency implications users will see? |
| **Operability** | Can this be deployed, monitored, and debugged? Is it observable? |
| **Security** | Are trust boundaries defined? Is the principle of least privilege applied? Are data flows secure? |
| **Cost** | What are the infrastructure and operational costs? Do they scale linearly with load? |
| **Extensibility** | How easy is it to add features later? Are extension points well-defined? |

### Step 3: API Contract Review

For any APIs introduced or modified:

| Aspect | What to Evaluate |
|--------|-----------------|
| **Naming** | Are resource names clear and consistent? Do they follow conventions? |
| **Versioning** | How are breaking changes handled? Is the versioning strategy defined? |
| **Error handling** | Are error responses structured and informative? Are error codes documented? |
| **Pagination** | Is pagination supported for list endpoints? Cursor vs. offset? |
| **Idempotency** | Are mutating operations idempotent? How are retries handled? |
| **Authentication** | What auth mechanism is used? Are scopes and permissions defined? |
| **Rate limiting** | Are rate limits defined? How are they communicated to consumers? |
| **Backward compatibility** | Will existing clients break? Is there a migration path? |

### Step 4: Data Model Review

Evaluate data design decisions:

| Aspect | What to Evaluate |
|--------|-----------------|
| **Schema design** | Are entities well-defined? Is normalization appropriate? Are indexes planned? |
| **Data lifecycle** | How is data created, updated, archived, and deleted? Retention policy? |
| **Migration strategy** | How will existing data be migrated? Is it backward compatible? Rollback plan? |
| **Access patterns** | Does the schema support the query patterns needed? Are hot spots avoided? |
| **Data integrity** | Are constraints enforced at the DB level? How are cross-entity invariants maintained? |
| **Storage choice** | Is the chosen data store appropriate (SQL vs. NoSQL vs. cache vs. queue)? |

### Step 5: Risk Assessment

Identify and categorize risks:

| Risk | Likelihood | Impact | Severity | Mitigation |
|------|:---:|:---:|----------|------------|
| *what could go wrong* | Low/Med/High | Low/Med/High | Critical/High/Med/Low | *how to address it* |

Risk categories to cover:
- **Technical risk** -- complexity, unproven technology, performance unknowns
- **Operational risk** -- deployment complexity, monitoring gaps, on-call burden
- **Security risk** -- new attack surfaces, data exposure, privilege escalation
- **Organizational risk** -- team expertise gaps, cross-team dependencies, timeline pressure
- **Data risk** -- migration failures, data loss, consistency violations

### Step 6: Provide Feedback

Structure feedback by severity:

| Severity | Meaning | Action Required |
|----------|---------|-----------------|
| **Blocker** | Fundamental flaw that must be addressed before proceeding | Redesign required |
| **Major** | Significant concern that should be addressed before implementation | Revise the design |
| **Minor** | Improvement that would strengthen the design but is not blocking | Consider for this iteration |
| **Suggestion** | Alternative approach worth exploring | Optional |
| **Praise** | Something done well worth highlighting | None -- acknowledge good work |

For each piece of feedback:
- State the concern clearly
- Explain why it matters (impact, risk)
- Suggest an alternative or ask a clarifying question
- Reference relevant prior art or industry patterns

## Output Format

Present the review as a structured document:

1. **Summary** -- overall assessment (approve / approve with changes / request revision), key strengths, and top concerns (3-5 bullets)
2. **Context Check** -- confirm understanding of the problem, requirements, and constraints
3. **Architecture Feedback** -- dimension-by-dimension evaluation
4. **API Feedback** -- contract review findings (if applicable)
5. **Data Model Feedback** -- schema and storage review findings (if applicable)
6. **Risk Assessment** -- identified risks with severity and mitigations
7. **Detailed Findings** -- individual feedback items sorted by severity
8. **Open Questions** -- unresolved questions for the design author
9. **Recommendations** -- prioritized list of changes to make

## Quality Checklist

- [ ] The problem statement and requirements are confirmed before reviewing the solution
- [ ] Feedback distinguishes between blockers, major issues, and suggestions
- [ ] Every criticism includes a rationale (why it matters) and a constructive suggestion
- [ ] Trade-offs are acknowledged -- no design is perfect given real constraints
- [ ] Praise is included for strong aspects of the design
- [ ] Non-functional requirements (performance, security, operability) are evaluated
- [ ] Risks are identified with likelihood and impact, not just listed
- [ ] Open questions are genuine questions, not passive-aggressive criticism

## Edge Cases

- **Reviewing a design you disagree with philosophically**: Separate objective issues (bugs, security gaps) from subjective preferences (architectural style); flag preferences as suggestions, not blockers
- **Incomplete design documents**: Note what is missing and ask for clarification; do not assume worst case -- ask before criticizing
- **Designs under extreme time pressure**: Focus feedback on blockers and high-severity items; defer minor items to follow-up; suggest phased approaches
- **Cross-team designs**: Evaluate integration points and contract boundaries especially carefully; consider both teams' operational realities
- **Designs involving unfamiliar technology**: Be transparent about your knowledge limits; ask clarifying questions rather than assuming the choice is wrong
