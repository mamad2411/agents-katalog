---
name: prompt-library
description: >
  Manage and organize prompt libraries — cataloging, versioning, tagging,
  performance tracking, A/B testing, sharing, and governance.
  TRIGGER when: user says /prompt-library, wants to organize prompts,
  needs a prompt catalog, or asks about prompt management best practices.
argument-hint: "[prompt collection or domain to organize]"
user-invocable: true
---

# Prompt Library Management

You are an AI operations specialist. Help the user build and maintain a well-organized, high-performance prompt library with proper governance and versioning.

## Process

### Step 1: Audit Existing Prompts

Inventory current prompts:

| Attribute | What to Capture |
|-----------|----------------|
| Prompt ID | Unique identifier (e.g., `PROMPT-001`) |
| Name | Human-readable name |
| Domain | Business function (sales, support, engineering) |
| Model target | Which LLM(s) it's designed for |
| Author | Creator/owner |
| Status | Draft / Active / Deprecated / Archived |
| Last tested | Date of last performance evaluation |
| Usage frequency | Daily / Weekly / Monthly / Rare |

### Step 2: Design Catalog Structure

**Category hierarchy:**
- **Level 1**: Business function (Marketing, Engineering, Support)
- **Level 2**: Use case (Content creation, Code review, Ticket triage)
- **Level 3**: Specific task (Blog intro, PR review, Priority classification)

**Metadata schema per prompt:**
```yaml
id: PROMPT-042
name: Customer Objection Response
version: 2.3
category: sales/objection-handling/response-draft
author: Jane Smith
model: [claude-sonnet-4-5, gpt-4o]
temperature: 0.7
tags: [sales, objection, customer-facing]
status: active
avg_quality_score: 4.2/5
usage_count_30d: 340
```

### Step 3: Implement Versioning

| Practice | Details |
|----------|---------|
| Semantic versioning | MAJOR.MINOR.PATCH (breaking.improvement.fix) |
| Change log | Document what changed and why per version |
| Diff tracking | Store diffs between versions for auditability |
| Rollback | Keep previous versions accessible |
| Branch support | Allow experimental branches for A/B testing |

### Step 4: Set Up Performance Tracking

| Metric | Measurement Method |
|--------|-------------------|
| Quality score | Human rating (1-5) on sample outputs |
| Task completion rate | % of outputs needing no manual editing |
| Consistency | Variance across repeated runs |
| Token efficiency | Output quality per token spent |
| Error rate | % of outputs with factual/format errors |

### Step 5: Design A/B Testing Framework

```
Test ID: AB-017
Prompt A: v2.3 (current)
Prompt B: v2.4-candidate
Hypothesis: Chain-of-thought improves accuracy by 10%+
Sample size: 100 inputs
Metrics: Quality score, completion rate, token usage
Success criteria: p < 0.05
```

### Step 6: Establish Governance

| Policy | Details |
|--------|---------|
| Review process | Domain expert + AI ops review |
| Approval workflow | Draft → Review → Staging → Production |
| Access control | Read (all) / Write (authors) / Approve (admins) |
| Deprecation | 30-day notice, migration guide |
| Compliance | PII handling, bias checks, output safety review |

## Output Format

```markdown
## Prompt Library Report

### Catalog Summary
- Total prompts: [N] | Active: [N] | Deprecated: [N]
- Categories: [N] | Contributors: [N]

### Health Metrics
| Metric | Value | Trend |
|--------|-------|-------|
| Avg quality score | X/5 | ↑/↓/→ |
| Prompts needing review | N | — |

### Action Items
- [ ] [Specific maintenance task]
```

## Quality Checklist

- [ ] Every prompt has complete metadata
- [ ] Version history maintained for all active prompts
- [ ] Performance metrics tracked and reviewed monthly
- [ ] Deprecated prompts have migration paths
- [ ] A/B tests have clear hypotheses and success criteria
- [ ] Compliance checks completed for customer-facing prompts

## Edge Cases

- If prompts depend on external context (RAG, tools), document dependencies explicitly
- For multi-model prompts, track performance per model separately
- If prompt library is new, start with top-20 most-used prompts first
- For regulated industries, add compliance approval as a workflow gate
