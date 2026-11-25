---
name: crm-setup-guide
description: "Design CRM setups with pipelines, automations, and workflows. TRIGGERS - Use when user wants to set up a CRM, design sales pipelines, or configure deal stages."
disable-model-invocation: false
category: general
version: 1.0.0
source: "https://github.com/Winbda/claude-skills-collection"
license: "MIT"
---
# CRM Setup Guide

## Output Format

```markdown
# CRM Setup: [Business Name]

## Pipeline Design

### Sales Pipeline
| Stage | Entry Criteria | Exit Criteria | Auto-actions |
|-------|---------------|---------------|-------------|
| Lead | [criteria] | [criteria] | [automation] |
| Qualified | [criteria] | [criteria] | [automation] |
| Proposal | [criteria] | [criteria] | [automation] |
| Negotiation | [criteria] | [criteria] | [automation] |
| Won/Lost | [criteria] | — | [automation] |

## Custom Fields
| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| [field] | [type] | Yes/No | [why] |

## Automations
1. **[Trigger]** → [Action]
2. **[Trigger]** → [Action]

## Email Templates
[Pre-built templates for each stage]

## Reporting Dashboard
[Key metrics to track]

## Team Setup
[Roles, permissions, territory assignment]
```
