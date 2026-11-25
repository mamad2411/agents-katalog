---
name: research-analyst
description: Analyze transcripts and customer research with strategic alignment checks. Use for /research workflows before PRD work.
---

# Research Analyst Skill

Procedural guidance for turning raw calls, interviews, and feedback into actionable initiative research.

## When to Use

- Running `/research [initiative]`
- Reviewing transcripts, meeting notes, or customer feedback
- Preparing evidence before writing a PRD

## Inputs

- Initiative name
- Transcript, notes, or linked source material
- Optional context from Slack, HubSpot, Linear, Notion, and PostHog

## Required Context

Load before analysis:

- `pm-workspace-docs/company-context/product-vision.md`
- `pm-workspace-docs/company-context/strategic-guardrails.md`
- `pm-workspace-docs/company-context/personas.md`

## MCP Servers

- `composio-config`: Slack, HubSpot, Linear, Notion, PostHog
- `hubspot`: account and deal context when customer identity matters
- `linear`: issue history for matching requests to known work
- `notion`: related specs and docs
- `posthog`: quantitative usage context

## Workflow

1. Confirm initiative and source material.
2. Extract key decisions, actions, problems, requests, and open questions.
3. Pull quantitative evidence when a feature area is measurable.
4. Score strategic alignment: `Strong`, `Moderate`, `Weak`, or `Needs Discussion`.
5. Flag anti-vision risks, trust concerns, and missing evidence.
6. Recommend next step: more discovery or move to `/pm`.

## Required Output Sections

- TL;DR
- Strategic Alignment
- Key Decisions
- Action Items
- User Problems with quotes
- Feature Requests
- Questions to Answer Before PRD
- Primary JTBD
- User Breakdown
- Feedback Plan

## Save Locations

- Initiative research: `pm-workspace-docs/initiatives/active/[name]/research.md`
- Meeting notes: `pm-workspace-docs/meeting-notes/YYYY-MM-DD-[topic].md`
- Signals: `pm-workspace-docs/signals/`

