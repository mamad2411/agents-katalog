---
name: 10x-campaigns
description: Pre-built marketing campaign workflows for 10X Vibe Marketer. Use when the user wants to run a structured campaign like a product launch, SEO audit, content calendar, competitor analysis, email sequence, social media blitz, brand refresh, or funnel optimization. Invoke with /campaign.
---

# 10X Campaign Templates

## Overview

Campaign Templates are pre-built, multi-phase marketing workflows that coordinate multiple specialist agents to deliver complete marketing initiatives. Each template defines the exact sequence of tasks, agent assignments, dependencies, and expected deliverables -- so you go from brief to execution with zero guesswork.

When a user invokes `/campaign`, the orchestrator loads the selected template from the `templates/` folder, briefs all assigned agents, manages phase dependencies, and tracks progress through to completion.

---

## Available Campaign Templates

| # | Template | File | Description |
|---|----------|------|-------------|
| 1 | **Full Product Launch** | `full-launch.md` | End-to-end product/service launch covering research, strategy, content creation, distribution, and optimization. |
| 2 | **SEO Audit** | `seo-audit.md` | Comprehensive SEO audit spanning technical, content, and competitor analysis with prioritized recommendations. |
| 3 | **Content Calendar** | `content-calendar.md` | Monthly content calendar built from audit insights, keyword strategy, and audience mapping. |
| 4 | **Competitor Analysis** | `competitor-analysis.md` | Deep competitor research with positioning analysis and strategic counter-moves. |
| 5 | **Email Sequence** | `email-sequence.md` | Multi-step email campaign from strategy through copywriting, optimization, and performance reporting. |
| 6 | **Social Media Blitz** | `social-media-blitz.md` | Multi-platform social media campaign with platform-specific content and engagement strategy. |
| 7 | **Brand Refresh** | `brand-refresh.md` | Brand identity overhaul covering audit, strategy, voice, messaging, and final guidelines. |
| 8 | **Funnel Optimization** | `funnel-optimization.md` | Conversion funnel audit with hypothesis-driven optimization and A/B test recommendations. |

---

## How Templates Work

### Structure

Each template file defines:

- **Campaign Name & Description** -- What the campaign achieves.
- **Target Outcomes** -- Measurable goals the campaign aims to hit.
- **Phases (3-5)** -- Sequential stages with clear entry/exit criteria.
- **Tasks per Phase** -- Specific work items with agent assignments.
- **Dependencies** -- Which phases must complete before the next begins.
- **Deliverables** -- Concrete outputs produced at each phase.
- **Success Metrics** -- KPIs to measure campaign effectiveness.

### Agent Assignments

Each task within a phase is assigned to a specific agent from the 10X Vibe Marketer agent roster. The orchestrator dispatches work to these agents in parallel where dependencies allow, and sequentially where outputs from one phase feed into the next.

### Execution Flow

```
User selects template via /campaign
       |
       v
Orchestrator loads template from templates/
       |
       v
Phase 1 tasks dispatched to assigned agents
       |
       v
Phase 1 deliverables collected and validated
       |
       v
Phase 2 tasks dispatched (using Phase 1 outputs)
       |
       v
  ... continues through all phases ...
       |
       v
Final deliverables compiled and presented to user
```

---

## Orchestrator Instructions

When executing a campaign template:

1. **Load** the selected template file from `templates/`.
2. **Parse** all phases, tasks, agent assignments, and dependencies.
3. **Brief** each assigned agent with context from the user's original request plus any brand kit data from `resources/brand-kit/`.
4. **Execute Phase 1** -- dispatch all Phase 1 tasks to their assigned agents. Tasks within the same phase can run in parallel unless otherwise noted.
5. **Collect & Validate** -- gather all Phase 1 deliverables, verify completeness.
6. **Pass Forward** -- feed Phase 1 outputs into Phase 2 tasks as context.
7. **Repeat** for each subsequent phase.
8. **Compile** final deliverables into a structured output in `output/campaigns/`.
9. **Report** -- generate a completion summary with links to all deliverables.

### Error Handling

- If an agent fails a task, retry once with additional context.
- If a phase is blocked, notify the user and suggest manual intervention.
- Always save partial progress so campaigns can be resumed.

---

## Database Campaign Tracking

When DoltgreSQL is available, campaigns are tracked in the database alongside file outputs:

### On Campaign Start
```sql
INSERT INTO campaigns (brand_id, campaign_name, campaign_type, description, goal, target_audience, channels, start_date, total_phases)
VALUES ({brand_id}, '{name}', '{template_type}', '{description}', '{goal}', '{audience}', '{channels}'::jsonb, CURRENT_DATE, {phase_count})
RETURNING id;
```

### Per Phase
```sql
INSERT INTO campaign_phases (campaign_id, phase_number, phase_name, description, status, planned_start)
VALUES ({campaign_id}, {n}, '{phase_name}', '{description}', 'pending', '{start_date}');
```

### Per Task
```sql
INSERT INTO campaign_tasks (campaign_id, phase_id, task_name, description, assigned_agent, model_tier, status)
VALUES ({campaign_id}, {phase_id}, '{task}', '{desc}', '{agent}', '{model}', 'pending');
```

### On Task Completion
```sql
UPDATE campaign_tasks SET status = 'completed', quality_score = {score}, output_file = '{path}', completed_at = CURRENT_TIMESTAMP WHERE id = {task_id};
```

### On Campaign Completion
```sql
UPDATE campaigns SET status = 'completed', quality_score = {avg_score}, updated_at = CURRENT_TIMESTAMP WHERE id = {campaign_id};
```

### Fallback
If database is unavailable, campaign tracking uses file-based system in `output/tracking/campaigns/` (existing behavior).

---

## Quick Start

```
/campaign                    # Browse all templates
/campaign full-launch        # Jump straight to product launch
/campaign seo-audit          # Run an SEO audit
/campaign content-calendar   # Plan a month of content
```

---

*Developed by 10x.in*
