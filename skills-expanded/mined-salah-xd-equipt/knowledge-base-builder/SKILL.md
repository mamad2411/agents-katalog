---
name: knowledge-base-builder
description: "Structures internal knowledge bases with categories, article templates, and maintenance procedures for organized business documentation."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Knowledge Base Builder

## When to Use This Skill

Use this skill when you need to:
- Structure an internal knowledge base from scratch with clear categories
- Create article templates for consistent documentation
- Build maintenance procedures to keep documentation current
- Organize tribal knowledge into a searchable, accessible system

**DO NOT** use this skill for customer-facing help centers (use help-center-article instead), wiki software setup, or content management system configuration. This is for structuring the knowledge architecture.

---

## Core Principle

A KNOWLEDGE BASE IS ONLY VALUABLE IF PEOPLE CAN FIND WHAT THEY NEED IN UNDER 60 SECONDS — STRUCTURE AND NAMING MATTER MORE THAN VOLUME.

---

## Phase 1: Audit

Understand what knowledge exists and where it lives today.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business type** | "What does your business do?" | No default |
| **Team size** | "How many people need access to this knowledge?" | 1-5 |
| **Current state** | "Where does your documentation live now? (Notion, Google Docs, nowhere, scattered)" | Scattered across tools |
| **Pain points** | "What questions do you or your team answer repeatedly?" | No default |
| **Platform** | "Where will the knowledge base live? (Notion, Confluence, Google Sites, etc.)" | Notion |

### Knowledge Audit Template

```
## Knowledge Audit

| Topic | Currently Documented? | Where? | Up to Date? | Priority |
|-------|----------------------|--------|-------------|----------|
| [Topic] | Yes / No / Partially | [Location] | Yes / No | High / Medium / Low |
```

**GATE: Complete the audit before designing the structure.**

---

## Phase 2: Architecture

Design the category structure and navigation.

### Category Framework

```
## Knowledge Base Structure

### 1. [Category Name]
   - [Subcategory]
   - [Subcategory]
   - [Subcategory]

### 2. [Category Name]
   - [Subcategory]
   - [Subcategory]
```

### Standard Categories for Solopreneurs

- **Operations:** SOPs, daily workflows, tool guides, vendor contacts
- **Sales & Marketing:** Scripts, templates, campaign playbooks, brand guidelines
- **Finance:** Invoicing procedures, expense policies, tax prep checklists
- **Client Delivery:** Service processes, quality standards, client communication templates
- **HR / Team:** Onboarding, policies, role descriptions, training materials
- **Tech & Tools:** Tool setup guides, troubleshooting, integration documentation
- **Templates:** Reusable documents, email templates, proposal templates

### Naming Conventions

- Use consistent naming: `[Category] - [Topic] - [Type]`
- Example: "Operations - Invoice Processing - SOP"
- Avoid jargon — write titles the way someone would search for them
- Include keywords people actually use, not internal shorthand

**GATE: Present the architecture for approval before creating templates.**

---

## Phase 3: Article Templates

Create standardized templates for each documentation type.

### SOP Template

```
# [Process Name] — Standard Operating Procedure

**Last updated:** [Date]
**Owner:** [Name]
**Review frequency:** [Quarterly / Biannually]

## Purpose
[One sentence: why this process exists]

## When to Use
[Trigger conditions for this process]

## Steps
1. [Step with specific detail]
2. [Step with specific detail]
3. [Step with specific detail]

## Common Issues
| Issue | Solution |
|-------|---------|
| [Issue] | [Fix] |

## Related Documents
- [Link to related article]
```

### How-To Guide Template

```
# How to [Task]

**Difficulty:** [Easy / Medium / Advanced]
**Time required:** [X minutes]
**Tools needed:** [List]

## Prerequisites
- [What you need before starting]

## Steps
1. [Step with screenshot placeholder: [Screenshot: description]]
2. [Step]
3. [Step]

## Troubleshooting
- **If [problem]:** [Solution]

## Related Guides
- [Links]
```

### Reference Document Template

```
# [Topic] Reference

**Last updated:** [Date]

## Overview
[2-3 sentence summary]

## Key Information
| Item | Detail |
|------|--------|
| [Item] | [Detail] |

## Notes
[Additional context]
```

---

## Phase 4: Maintenance

Build systems to keep the knowledge base alive and accurate.

### Maintenance Schedule

```
## Knowledge Base Maintenance

**Weekly:** Review any flagged articles for updates
**Monthly:** Check top 10 most-viewed articles for accuracy
**Quarterly:** Full category review — archive outdated content, identify gaps
**After any process change:** Update affected articles within 48 hours
```

### Article Lifecycle

- **Draft:** Written but not reviewed
- **Published:** Reviewed and current
- **Under Review:** Flagged for update
- **Archived:** No longer relevant but kept for reference

### Quality Checks

- Every article has an owner and a review date
- No article older than 6 months without a review
- Broken links checked monthly
- New team members flag confusing or missing documentation during onboarding

---

## Anti-Patterns

- **Dumping everything in one folder** — without categories, the knowledge base becomes a digital junk drawer.
- **Writing for experts** — documentation should be usable by someone on their first day. Write for the newest team member.
- **No ownership** — articles without owners never get updated. Every article needs one responsible person.
- **Perfection paralysis** — a rough SOP published today beats a perfect one written never. Start messy, refine later.
- **Duplicating content** — link to the source of truth, do not copy-paste. Copies drift out of sync.

---

## Recovery

- **User is overwhelmed by the scope:** Start with the 5 most frequently asked questions. Document those first. Everything else can wait.
- **No one reads the knowledge base:** It is a search problem, not a content problem. Improve titles, add search tags, and link to articles in the workflow where they are needed.
- **Articles are outdated:** Assign ownership and set calendar reminders. Flag outdated articles visibly so readers know to verify.
- **User works alone:** The knowledge base is still valuable — it is your "hit by a bus" insurance and your contractor onboarding kit.
- **Too many tools to document:** Prioritize tools used daily. If a tool is used less than weekly, a bookmark to its help docs is sufficient.
