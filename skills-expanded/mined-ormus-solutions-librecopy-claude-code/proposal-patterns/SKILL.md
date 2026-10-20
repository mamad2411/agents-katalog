---
name: "proposal-patterns"
description: "Proposal patterns: problem-first structure, the quality bar for alternatives, success metrics, the one-pager format, open questions, the review process, and anti-patterns such as consensus theater. Use when writing or reviewing RFCs and design docs."
---

# Proposal Writing Patterns

## Problem-First Structure

The most common proposal mistake: opening with the solution. Reviewers who disagree with the framing of the problem will block everything that follows.

```markdown
# Bad: starts with solution
## Proposed Solution
We should replace our current session-based auth with JWTs.

Benefit: JWTs are stateless, which means...

# Good: starts with problem
## Problem Statement
Our auth service maintains a session store that is shared across all API instances.
This shared state prevents us from scaling the API horizontally without session affinity:
- New API instances cannot serve requests for sessions they didn't create
- Session store is a single point of failure (2 outages in the last 6 months)
- Read latency for the session lookup is 12ms p99 (15% of our total p99 budget)
```

## Alternatives Considered: Quality Bar

Alternatives must be taken seriously, not strawmanned:

```markdown
# Bad: alternatives dismissed without substance
We considered using Option B but it's more complex and harder to maintain.

# Good: alternatives with concrete analysis
| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| Redis session store (proposed) | Existing ops expertise, atomic operations | Additional infrastructure, 12ms latency | Chosen |
| Database sessions | No new infrastructure | 40ms+ latency unacceptable for our SLA | Rejected: latency |
| In-process sessions | Zero latency | Cannot share across instances, blocks horizontal scaling | Rejected: fundamental |
| JWT (stateless) | Eliminates session store entirely | Token revocation complexity, larger request headers | Deferred: evaluate for v2 |
```

Key rule: rejected alternatives should be rejected for **specific, verifiable reasons**. "More complex" is not a reason. "Requires 3 additional operational runbooks and monitoring dashboards we don't have" is.

## Success Metrics Pattern

Success metrics defined before implementation prevent "success" being redefined after the fact:

```markdown
# Bad: vague success criteria
The system will be more reliable and scale better.

# Good: measurable success criteria
| Metric | Current | Target | Measured By | Review At |
|--------|---------|--------|-------------|-----------|
| Auth service p99 latency | 12ms | ≤4ms | Datadog dashboard | 30 days post-launch |
| Auth-related support tickets | 42/month | ≤10/month | Zendesk tag `auth-issue` | 90 days post-launch |
| Auth service availability | 99.7% | 99.95% | Uptime robot | 60 days post-launch |
```

## One-Pager Format

For small decisions, a full RFC is overkill. Use a one-pager that gets to the point:

```markdown
# [Decision Title]

**Author**: [Name] | **Date**: [Date] | **Status**: Proposed

## TL;DR

[One sentence: what are you proposing?]

## Problem

[2-3 sentences: the current state and why it's a problem. Include data.]

## Proposal

[2-3 sentences: what you want to do.]

## Alternatives

1. **[Option B]**: [one sentence why rejected]
2. **Status quo**: [one sentence why insufficient]

## Risks

- **[Risk]**: [Mitigation]

## Decision needed by

[Date, with brief reason for urgency]
```

## Open Questions Format

Open questions invite reviewer engagement. They signal intellectual honesty:

```markdown
## Open Questions

- [ ] **Security team**: Are there PCI compliance implications for storing session data in Redis vs in-process? [Alice]
- [ ] **Infrastructure**: What is the operational cost of adding a Redis cluster? Estimate needed before approval. [Bob]
- [ ] **Unresolved**: What is the token revocation strategy if a user's permissions change between token issuance and expiry? [RFC author]
```

Tag each question with the person responsible for answering it.

## Proposal Review Process

### Comment period structure
1. Author posts RFC with explicit review deadline
2. Reviewers post comments asynchronously (prefer async)
3. Author responds to all substantive comments
4. If significant changes result, restart the clock (1 week)
5. Silence = consent after the review period (document this explicitly)

### Types of reviewer responses
```markdown
# Blocking objection (must resolve before moving forward)
**BLOCKING**: The rollback plan assumes we can restore the session store from backup
within 5 minutes. Our backup restore time is actually 2 hours. This is a showstopper.

# Non-blocking concern (should address but won't block)
**NON-BLOCKING**: The latency targets seem optimistic. I'd recommend adding a monitoring
task in Phase 1 to validate before Phase 2. [Name]

# Question (seeking clarification)
**QUESTION**: Does this approach require changes to the mobile app auth flow?

# Approval
**APPROVED**: The problem is real, the solution is sound, alternatives are adequately
considered. [Name]
```

## Anti-Patterns

### Solution disguised as problem
```
# Bad: "problem" is actually a solution preference
The problem is that we're not using Kubernetes.

# Good: actual problem
The problem is that deployments take 45 minutes (target: 10 minutes) because
our current deployment process involves 8 manual steps.
```

### Missing status quo alternative
Every alternatives section must include "do nothing" or "continue current approach" as an option. If status quo isn't worth documenting, the problem probably isn't worth solving.

### RFC that seeks approval for already-completed work
Writing an RFC for work that's already been implemented or approved elsewhere defeats the purpose. Note "Recorded retroactively" and document the actual decision process.

### Consensus theater
Requesting broad review when you've already made the decision. Sets the wrong expectation and wastes reviewers' time. Use a one-pager with explicit "FYI" framing instead.

## References
- [Google's technical writing for proposals](https://developers.google.com/tech-writing)
- [Rust RFC process](https://github.com/rust-lang/rfcs) - example of open RFC culture
- [Amazon's Working Backwards / 6-pager](https://www.aboutamazon.com/news/workplace/jeff-bezos-and-the-six-page-memo)
- [Shape Up - Writing Pitches](https://basecamp.com/shapeup/1.5-chapter-06) - Basecamp's RFC-like process
