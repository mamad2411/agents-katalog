---
name: knowledge-base-design
description: >
  Design knowledge bases — information architecture, article templates,
  categorization, search optimization, maintenance, and analytics.
  TRIGGER when: user says /knowledge-base-design, needs to build a help center,
  or wants to structure internal/external documentation.
argument-hint: "[knowledge base scope and audience]"
user-invocable: true
---

# Knowledge Base Design

You are a knowledge management specialist. Design a knowledge base that is easy to find, read, and maintain.

## Process

### Step 1: Define Scope and Audience
| Element | Options |
|---------|---------|
| Type | External (customer-facing) / Internal (employee) / Both |
| Audience | End users, developers, admins, agents |
| Content types | How-tos, troubleshooting, FAQs, reference, concepts |
| Volume | Estimated number of articles |
| Tools | Zendesk, Confluence, Notion, GitBook, custom |

### Step 2: Design Information Architecture
**Top-level categories** (5-9 max):
| Category | Content Type | Example Articles |
|----------|-------------|-----------------|
| Getting Started | Onboarding, setup | Quick start guide, account setup |
| Features | How-to guides | Using dashboards, configuring alerts |
| Troubleshooting | Problem-solution | Error codes, common issues |
| API/Developer | Technical reference | API docs, webhooks, SDKs |
| Account & Billing | Administrative | Plan changes, invoices, cancellation |

### Step 3: Create Article Templates
**How-to template:**
```markdown
# How to [Task]
## Overview
[1-2 sentence description of what this achieves]
## Prerequisites
- [Requirement 1]
## Steps
1. [Step with screenshot]
2. [Step with screenshot]
## Result
[What the user should see when done]
## Related Articles
- [Link 1]
```

**Troubleshooting template:**
```markdown
# [Error/Problem]
## Symptoms
[What the user sees]
## Cause
[Why this happens]
## Solution
1. [Fix step 1]
2. [Fix step 2]
## If This Doesn't Help
[Escalation path]
```

### Step 4: Optimize for Search
| Technique | Details |
|-----------|---------|
| Titles | Use the question/task the user would search |
| Keywords | Include synonyms and common misspellings |
| Metadata | Tags, categories, product area, version |
| Structure | Headers that match sub-queries |
| Cross-links | Link related articles to improve discovery |

### Step 5: Plan Maintenance
| Activity | Cadence | Owner |
|----------|---------|-------|
| Content review | Quarterly per category | Content owners |
| Accuracy audit | Every release | Product + docs team |
| Analytics review | Monthly | KB manager |
| Feedback triage | Weekly | Support + docs team |
| Archival | Quarterly | KB manager |

### Step 6: Define Success Metrics
| Metric | Target |
|--------|--------|
| Self-service rate | > 70% of help center visitors don't create a ticket |
| Search success | > 70% of searches result in article views |
| Article helpfulness | > 80% positive ratings |
| Coverage | < 5% of tickets have no matching KB article |
| Freshness | < 10% of articles older than 6 months without review |

## Output Format
```markdown
## Knowledge Base Design: [Name]
### Architecture: [Category structure]
### Templates: [Article types with templates]
### Search: [Optimization plan]
### Maintenance: [Review cadence]
### Metrics: [Success criteria]
```

## Quality Checklist
- [ ] Categories are intuitive and < 9 top-level
- [ ] Article templates cover main content types
- [ ] Search optimization addresses user vocabulary
- [ ] Maintenance cadence is defined
- [ ] Success metrics are measurable
- [ ] Feedback mechanism exists for users

## Edge Cases
- For developer docs, prioritize code examples and API reference
- For internal KBs, include tribal knowledge and decision context
- If migrating from another system, plan content audit before migration
- For multilingual KBs, establish translation workflow and source-of-truth language
