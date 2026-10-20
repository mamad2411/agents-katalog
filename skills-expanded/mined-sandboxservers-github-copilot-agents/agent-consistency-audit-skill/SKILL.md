---
name: Agent Consistency Audit
description: Identify and resolve conflicts when multiple agents provide guidance on overlapping domains
when-to-use: After adding new agents, expanding overlapping knowledge, or when users report contradictory advice
categories:
  - Quality Assurance
  - Agent Design
  - Knowledge Management
---

# Agent Consistency Audit

**Purpose:** When multiple agents cover the same topic (e.g., security, cost, infrastructure), they may give conflicting guidance. This skill provides a framework to identify, evaluate, and resolve those conflicts — distinguishing between *legitimate* perspective differences and *knowledge gaps*.

## When to Use

- **New agent added** — Especially if it touches existing domains (e.g., adding a new compute specialist when one already exists)
- **Knowledge expansion** — When you add a new chunk file that overlaps with another agent's expertise
- **User reports conflict** — "Agent A says do X, Agent B says do Y"
- **Regular audit** — Quarterly or semi-annually, pick 5-10 common cross-domain topics and audit

## The Audit Process

### 1. Identify Overlap Candidates

Map agents by domain. Look for natural overlaps:

| Domain | Agents | Overlap Risk |
|--------|--------|-------------|
| **Security** | Security Analyst, App Infra Architect, Network Engineer, Database Specialist | HIGH — all touch auth, encryption, access control |
| **Cost** | Cost Specialist, all code authors | HIGH — "cheapest" vs "maintainable" may conflict |
| **Testing** | Testing Engineer, all code authors, DevOps Lead | MEDIUM — different perspectives on scope |
| **IaC** | Terraform Author, Bicep Author, Platform Lead | MEDIUM — when to use Terraform vs Bicep |
| **Deployment** | DevOps Lead, Platform Lead, Code Authors | MEDIUM — sequencing and responsibility |

### 2. Pick a Topic and Query Both Agents

Select a topic that both agents might address. Ask them the same question.

**Example:**

**Topic**: "Should I pin Azure provider versions in Terraform modules?"

**Query to Terraform Author**: "In a Terraform module I'm publishing to the registry, should I pin the azurerm provider version in the `required_providers` block, or leave it open-ended?"

**Query to Security Analyst**: "From a security and reproducibility standpoint, should Terraform modules pin their provider versions?"

### 3. Capture Responses and Compare

Document both responses:

```markdown
## Topic: Provider Version Pinning in Terraform Modules

### Terraform Author Response
[Full response or summary]

**Position**: [Pin major version only, e.g., `>= 3.0, < 4.0`]
**Rationale**: [Explanation — in this case, "balances stability with security updates"]

### Security Analyst Response
[Full response or summary]

**Position**: [Pin major.minor tightly, validate all updates in test env]
**Rationale**: [Explanation — in this case, "reproducibility and audit trail for compliance"]
```

### 4. Classify the Conflict

**Type A — Legitimate Perspective Difference** (No fix needed)
- Both positions are valid from their viewpoint
- The agents' voice/priorities explain the difference
- Users should understand *why* they're getting different advice
- **Action**: Document this as a known disagreement; add a cross-reference in both agents' knowledge files

**Example**: "Terraform Author prioritizes readability. Security Analyst prioritizes auditability. On version pinning, they'll disagree — use Security Analyst's advice for regulated environments, Terraform Author's for internal projects."

**Type B — Knowledge Gap** (Fix required)
- One agent is outdated, missing context, or wrong
- The other agent's position is the correct one
- **Action**: Update the outdated agent's knowledge; add a decision rule to their voice guide

**Example**: "Terraform Author didn't know that Azure occasionally releases critical CVE patches to major versions without a major-version bump. Update their knowledge file; clarify in voice guide: 'Monitor Azure security advisories, not just version numbers.'"

**Type C — Missing Decision Rule** (Add a skill)
- Both agents are correct, but there's no unified guidance for when to use which approach
- Need a shared skill or decision tree
- **Action**: Create a skill (e.g., `terraform-module-patterns` or expand `terraform-style-guide`) that lays out the decision rules

**Example**: "Terraform Author and Platform Lead both provide valid approaches. Create a skill: 'When to use Terraform modules vs. root modules: decision tree based on team size, regulatory needs, publication scope.'"

### 5. Resolve (Document or Fix)

**If Type A (legitimate difference):**
```markdown
## Known Disagreement: Provider Version Pinning

**Position 1** (Terraform Author): Pin major version only
- Rationale: Balances stability with security updates
- Use when: Internal projects, fast-moving teams

**Position 2** (Security Analyst): Pin major.minor tightly
- Rationale: Reproducibility, compliance auditability
- Use when: Regulated environments, long-lived infrastructure

**Guidance**: Defer to Security Analyst if compliance required; otherwise follow Terraform Author.
```

**If Type B (knowledge gap):**
1. Update the outdated agent's knowledge files
2. Update their voice guide to capture the missing decision rule
3. Link to corrected knowledge from the other agent

**If Type C (missing rule):**
1. Create a new skill or expand an existing one
2. Link from both agents' "Related Skills" sections
3. Update both agents' knowledge files to reference the skill

## Audit Template

Use this template to document an audit:

```markdown
# Consistency Audit: [Topic Name]

**Date**: [Date]
**Agents Involved**: [List]
**Initiated By**: [User report / regular audit / new agent]

## Query
[Question asked to both agents]

## Responses

### [Agent 1]
Position: [Summary]
Rationale: [Why]
Reference: [Knowledge file / source]

### [Agent 2]
Position: [Summary]
Rationale: [Why]
Reference: [Knowledge file / source]

## Analysis
[Type A/B/C classification and reasoning]

## Resolution
[Action taken or documented]

## Related Changes
[PRs, updated knowledge files, new skills, updated voice guides]
```

## Running a Quarterly Audit

Each quarter, pick 5-10 topics and audit:

1. **Security-related** (1-2 topics): Access control, encryption, secrets management
2. **Cost-related** (1-2 topics): Rightsizing, commitment discounts, waste
3. **Operational** (1-2 topics): Deployment strategy, testing, monitoring
4. **Technical** (1-2 topics): IaC patterns, service selection, architecture

Document all audits in `audits/YYYY-QN-consistency.md`.

## Red Flags

Stop and audit immediately if:

- A new agent's knowledge directly contradicts an existing agent's on the same topic
- A user reports "Agent A said X, Agent B said Y, which is right?"
- An agent's knowledge file references another agent without explaining potential conflicts
- A skill or decision rule hasn't been updated in 6+ months but related agent knowledge has

## Related Skills

- `agent-voice-guide` — Define personality/perspective for each agent (explains *why* they might differ)
- Any domain-specific style guides (e.g., `terraform-style-guide`, `bicep-style-guide`) — capture unified decisions

## Reference

See `skills/` folder for related decision frameworks. See `agent-memory/` for knowledge files that may overlap.
