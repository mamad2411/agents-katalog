---
name: prd-builder
description: "Use when generating Product Requirements Documents, project instructions, and custom development resources. Transforms ideas into structured, actionable PRDs."
version: "1.0"
tags:
  - prd
  - product-management
  - requirements
  - documentation
  - project-planning
---

# PRD Builder

## Overview

Transforms raw product ideas into structured, actionable Product Requirements Documents (PRDs). Produces documents that engineering teams can actually build from — not vague vision statements. Generates project instructions, user stories, acceptance criteria, and development roadmaps.

## When to Use

- A founder has an app idea and needs a documented spec
- A PM needs to turn stakeholder requests into structured requirements
- A developer needs clear acceptance criteria before starting a feature
- A team needs alignment on scope, priorities, and success metrics
- Pre-development: before any code is written, document what "done" means

## How It Works

The PRD follows a **Problem → Solution → Scope → Spec → Roadmap** pipeline. Each section builds on the previous one. The output is a self-contained markdown document ready for Notion, Linear, Jira, or GitHub Projects.

## Steps

### Step 1: Problem Discovery
Answer these before writing:
- What problem does this solve? (user pain point)
- Who has this problem? (user persona + market size if relevant)
- How do they solve it today? (existing alternatives/workarounds)
- Why now? (timing, market shift, technology enablement)

### Step 2: Solution Definition
Define the solution at two altitudes:
- **Elevator pitch**: 2-3 sentences anyone can understand
- **Core value prop**: The one thing that makes users switch

### Step 3: Scope & Non-Scope
Explicitly define what's IN and what's OUT:
```
✅ IN SCOPE:
- Feature A with X, Y, Z
- Integration with Service B
- Admin dashboard for role C

❌ OUT OF SCOPE (v1):
- Mobile app (web only for v1)
- AI recommendations (v2)
- Multi-tenant (single tenant for v1)
```

### Step 4: User Stories & Acceptance Criteria
Write user stories in the format:
```
As a [user type], I want to [action] so that [outcome].

Acceptance Criteria:
- [ ] Given [precondition], when [action], then [expected result]
- [ ] Edge case: [scenario] → [expected behavior]
```

Prioritize with MoSCoW:
- **Must have**: Blocking, v1 cannot ship without
- **Should have**: Important, can defer if timeline slips
- **Could have**: Nice to have, v1.1 candidate
- **Won't have**: Explicitly deferred

### Step 5: Technical Requirements
Document constraints and preferences:
- **Stack**: Language, framework, database, hosting
- **Integrations**: APIs, third-party services
- **Performance**: Load times, concurrency, data volumes
- **Security**: Auth model, data handling, compliance (GDPR, SOC2)
- **Platforms**: Web, iOS, Android, API

### Step 6: Design Requirements
- **Information architecture**: Page/screen map
- **Key flows**: Critical user journeys (happy path + edge cases)
- **Design system**: Existing or new? Reference designs
- **Accessibility**: WCAG level target

### Step 7: Success Metrics
Define measurable outcomes:
- **North star metric**: The one number that defines success
- **Supporting metrics**: 3-5 KPIs that validate progress
- **Baseline & target**: Current state → desired state with timeline

### Step 8: Roadmap & Milestones
```
Week 1-2: Auth + Core data model
Week 3-4: Primary user flow
Week 5: Integrations
Week 6: Testing + polish
Week 7: Beta launch
Week 8: Public launch
```

### Step 9: Generate Deliverable
Compile into a single markdown PRD with:
- Executive summary (1 page)
- Full PRD (all sections above)
- Appendix: Glossary, references, competitor links

## Common Pitfalls

- **Solution-first thinking**: Jumping to "build a dashboard" before defining the problem. Always start with problem discovery.
- **Vague acceptance criteria**: "User can log in" is not testable. Specify: "Given valid email + password, when clicking 'Sign In', then redirected to dashboard within 2 seconds."
- **No explicit non-scope**: Without a "won't have" list, scope creeps indefinitely.
- **Skipping success metrics**: If you can't define what success looks like, you can't prioritize or know when to stop.
- **Over-engineering v1**: The best v1 is the smallest thing that validates the core hypothesis. Cut everything else.

## Source

Consolidates PRD generation best practices from multiple custom GPTs focused on product requirements and development resource generation.
