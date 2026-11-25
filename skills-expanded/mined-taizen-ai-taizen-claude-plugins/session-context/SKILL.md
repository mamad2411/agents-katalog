---
name: session-context
description: Establishes user role and team context at session start to personalize outputs. Runs silently without producing visible output.
user-invocable: false
---

# Session Context Skill

Automatically gather context about the current user to personalize all subsequent outputs.

## Purpose

Identify the current user and gather context about their role, team, and responsibilities to personalize all subsequent interactions and outputs.

> **Note**: This is a **background skill** that runs automatically when other skills need user context. It does not produce visible output and is not meant to be invoked directly by users.

---

## Skills That Reference This Context

The following skills automatically use session-context to personalize their outputs:

- `account-research` - Adapts account briefs to user's role
- `discovery-prep` - Tailors prep materials to sales methodology
- `sales-coaching` - Personalizes coaching to rep's experience level
- `executive-briefings` - Adjusts detail level based on seniority
- `buyer-profiles` - Emphasizes relevant personas for user's deals
- `competitive-intelligence` - Focuses on relevant competitive scenarios
- `email-sequences` - Adjusts tone for user's communication style
- `outreach-templates` - Personalizes based on user's territory/focus

## Related Background Skills

- `product-context` - Provides product positioning and messaging that this skill uses alongside user context
- `feedback-collector` - Captures corrections to improve personalization accuracy

---

## Required Integrations

> **Setup**: Connect these data sources to enable user context identification.

### Data Sources

```yaml
# SESSION CONTEXT DATA SOURCES
# Configure the sources for user identification

# Enterprise Search (searches across all internal sources)
- source: enterprise_search
  connector: "{{GLEAN | MOVEWORKS | ELASTIC}}"
  data:
    - people_directory
    - org_charts
    - team_membership

# HR / Directory
- source: hr_system
  connector: "{{WORKDAY | BAMBOOHR | RIPPLING}}"
  data:
    - employee_profiles
    - job_titles
    - departments
    - managers

# CRM (for sales user context)
- source: crm
  connector: "{{SALESFORCE | HUBSPOT}}"
  data:
    - user_records
    - territory_assignments
    - quota_data
```

---

## Workflow

1. **Identify User**: Search for the user's first and last name in available context (environment variables, git config, or ask if needed)

2. **Determine Role**: Based on user identification, determine:
   - Job title and function (Sales, Marketing, Customer Success, etc.)
   - Team or department
   - Seniority level
   - Key responsibilities

3. **Set Session Context**: Store this context to inform all subsequent skill outputs:
   - Adapt language and terminology to user's expertise level
   - Focus on metrics and outcomes relevant to their role
   - Tailor recommendations to their sphere of influence

## Context Variables to Set

- `user_name`: Full name of the user
- `user_role`: Job title/function
- `user_team`: Department or team
- `user_seniority`: Level (IC, Manager, Director, VP, C-level)
- `user_focus_areas`: Primary responsibilities

## Output Behavior

This skill is **silent** - it does not produce visible output to the user. Instead, it sets internal context that other skills will reference.

When context is successfully gathered, proceed with the user's original request using the established context.

If unable to determine user context, proceed with reasonable defaults for a GTM professional.

---

## Role-Based Personalization

### Sales Roles
- Focus on deal-related outputs
- Include CRM integration
- Emphasize competitive intelligence
- Prioritize meeting prep and follow-ups

### Marketing Roles
- Focus on content and campaign outputs
- Include analytics integration
- Emphasize messaging consistency
- Prioritize content calendar and performance

### Customer Success Roles
- Focus on customer health and expansion
- Include CS platform integration
- Emphasize retention metrics
- Prioritize renewal and upsell prep

### Leadership Roles
- Focus on strategic summaries
- Include cross-functional data
- Emphasize business impact
- Prioritize executive-ready outputs
