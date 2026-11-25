---
name: architecture-decision-records
description: >-
  Process and template for documenting architecture decisions. Captures the
  context, decision rationale, and consequences to build institutional knowledge
  and avoid repeating past discussions.
when-to-use: >-
  Use when making significant architectural decisions: technology choices, system
  design changes, migration strategies, or patterns that will affect multiple
  teams or have long-term implications.
categories:
  - architecture
  - documentation
  - decision-making
---

# Architecture Decision Records (ADR)

Format for documenting architecture decisions. ADRs capture the problem, options considered, decision made, and consequences—building shared understanding and preventing repeated discussions.

## Why ADRs Matter

1. **Shared Context**: New team members understand *why* a decision was made, not just *what* was decided
2. **Avoid Regression**: Prevents re-litigating settled decisions
3. **Institutional Memory**: Survives personnel changes
4. **Design Rationale**: Shows tradeoffs considered, not just the winning option

## When to Write an ADR

Write an ADR when:
- ✅ Choosing between technologies (Terraform vs Pulumi, Postgres vs DynamoDB)
- ✅ Major system redesign (moving to microservices, event-driven architecture)
- ✅ Technology upgrade with significant impact (Node.js 18 → 20, Python 3.9 → 3.12)
- ✅ Security/compliance decision (OAuth 2.0 + SAML for identity)
- ✅ Team process change (moving test framework, renaming branch strategy)
- ✅ Expensive infrastructure choice (reserved instances, multi-region)

Don't write an ADR for:
- ❌ Routine tech debt fixes
- ❌ Bug fixes
- ❌ Minor refactors
- ❌ Day-to-day implementation details

---

## ADR Template

Save as `doc/adr/NNNN-brief-title.md` (e.g., `doc/adr/0001-use-terraform-not-pulumi.md`)

```markdown
# ADR-NNNN: [Brief Title]

**Status**: [Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

**Date**: [YYYY-MM-DD]

**Decision Maker(s)**: [Names of people who made decision]

**Stakeholders**: [Teams affected]

## Problem Statement

[Describe the problem or decision point. What prompted this decision?]

**Context:**
- Background information
- Current state of the system
- Why this matters now

## Decision

[Concise statement of the decision made]

## Options Considered

### Option A: [Name]
**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

**Cost Estimate:** [if applicable]

### Option B: [Name]
**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

**Cost Estimate:** [if applicable]

### Option C: [Name]
...

## Why This Option

[Explain why Option X was chosen over the others. What factors were decisive?]

- Aligns with [company goal/constraint]
- Best supports [use case/requirement]
- Enables [future capability]
- Lower cost/complexity than alternatives

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative / Risks
- [Risk 1: How to mitigate?]
- [Risk 2: How to mitigate?]

### Effort & Cost
- Estimated effort to implement: [e.g., 3 weeks for 2 engineers]
- Ongoing operational cost: [e.g., $500/month for managed service]
- Training cost: [time to upskill team]

## Implementation Plan

1. [Phase 1]
2. [Phase 2]
3. [Migration/rollback procedure]

**Timeline**: [When will this be implemented?]

**Rollback Plan**: [What if it goes wrong?]

## Related Decisions

- Supersedes ADR-XXXX: [Old decision this replaces]
- Related to ADR-YYYY: [Decision this builds on]
- Informs ADR-ZZZZ: [Future decision this enables/constrains]

## References

- [Relevant docs, RFC links, etc.]
- [Tool/service documentation]
- [Team discussion thread, meeting notes]
```

---

## Writing Tips

### Be Specific

❌ **Bad**: "We need better database performance"
✅ **Good**: "Queries on user_events table take >5s at peak load; causing 10% timeout rate in search UI"

### Show Your Work

Don't just state the decision. Show:
- Options you considered (even rejected ones)
- Why you didn't pick the alternatives
- What would need to change to reconsider

### Anticipate Questions

Address:
- "Won't this break X?" → Explain migration path
- "What about cost?" → Give concrete numbers
- "How do we roll back?" → Detail rollback procedure
- "Who maintains this?" → Identify owner/team

### Include the Downsides

Good ADRs acknowledge tradeoffs:
- "We lose [capability], but gain [benefit]"
- "This increases ops burden by [amount] but saves [cost]"

Bad ADRs pretend there are no downsides.

---

## Example ADR

### ADR-0001: Use Terraform for Infrastructure as Code

**Status**: Accepted

**Date**: 2024-03-15

**Decision Maker(s)**: Platform Engineering Lead, Cloud Engineering Lead

**Stakeholders**: All infrastructure teams, security team

## Problem Statement

We manage infrastructure across AWS and Azure using mix of CloudFormation, manual Azure Portal clicks, and adhoc scripts. This causes:
- Drift between dev/prod environments
- Slow onboarding (no reproducible environments)
- No audit trail for infrastructure changes
- Difficult to code-review infrastructure changes

We need a unified IaC tool to enforce consistency and enable code review.

## Decision

**Adopt Terraform as primary IaC tool across all infrastructure.**

## Options Considered

### Option A: Terraform
**Pros:**
- Multi-cloud support (AWS, Azure, GCP)
- Largest community / ecosystem
- HCL is expressive and readable
- State management well-understood
- Works well with GitOps

**Cons:**
- Learning curve for ops team
- State file management required
- Occasional provider bugs
- Not ideal for Kubernetes (though Helm covers this)

**Cost**: $0 (open source; paid Terraform Cloud optional later)

### Option B: Pulumi
**Pros:**
- Use general-purpose languages (Python, Go, TypeScript)
- Easier for engineers coming from software dev
- Strong type system
- Good for complex logic

**Cons:**
- Smaller ecosystem than Terraform
- Requires language runtime (adds complexity)
- Less mature for Kubernetes
- SaaS offering required for team collaboration ($25/user/mo)

**Cost**: $25/user/mo for Terraform Cloud equivalent

### Option C: CloudFormation + ARM Templates
**Pros:**
- Native to AWS/Azure
- No new tool to learn
- First-party support

**Cons:**
- Not multi-cloud
- CloudFormation/ARM JSON very verbose
- No code reuse across platforms
- Forces us to pick AWS or Azure

**Cost**: $0, but locks us to one cloud

## Why Terraform

1. **Multi-cloud flexibility**: We use both AWS and Azure. Terraform lets us treat them consistently.
2. **Maturity & community**: Terraform has largest user base, most examples, best troubleshooting resources.
3. **Cost**: Open source; we avoid vendor lock-in and licensing costs.
4. **Enables code review**: HCL + Git workflow makes peer review natural.
5. **Compatibility**: Most open-source modules built for Terraform.

## Consequences

### Positive
- Reproducible environments (dev = prod)
- Infrastructure changes trackable via git
- Faster onboarding (automation instead of manual steps)
- Audit trail for compliance
- Enables self-service infrastructure (less OpsOps)

### Negative / Risks
- **Learning curve**: Team needs training (~2 weeks per engineer)
  - Mitigation: Hire contractor for initial pair programming
- **State file management**: Terraform state is sensitive
  - Mitigation: Store in encrypted S3/blob, enable locking
- **Breaking changes**: Terraform major versions may require refactoring
  - Mitigation: Test upgrades in dev first, keep pinned version until ready

### Effort & Cost
- Implementation: 4 weeks for 2 engineers to migrate existing infrastructure
- Training: 1 week per engineer for team
- Ongoing operational cost: $0 (unless we adopt Terraform Cloud for state sharing, then ~$70/mo for Team & Governance tier)

## Implementation Plan

1. **Week 1-2**: Hire Terraform consultant to establish patterns and best practices
2. **Week 2-4**: Migrate 3 non-critical services to prove approach
3. **Week 5-8**: Migrate critical services (database, identity, API gateways)
4. **Week 9+**: Team assumes ongoing maintenance

**Rollback Plan**: Keep CloudFormation/manual scripts as backup for first 3 months. If Terraform adoption stalls, revert to manual process (not ideal, but safe).

## Related Decisions

- Informs ADR-0002: "Use GitOps for deployment automation" (needs IaC first)
- Related to ADR-0003: "Standardize on AWS for primary workloads" (though Terraform helps avoid lock-in)

## References

- [Terraform AWS provider docs](https://registry.terraform.io/providers/hashicorp/aws/)
- [Terraform Azure provider docs](https://registry.terraform.io/providers/hashicorp/azurerm/)
- [Terraform Best Practices by Anton Babenko](https://github.com/antonbabenko/terraform-best-practices)
- [Team discussion thread](https://slack.com/archives/C012345/p1234567890123456) (internal)
