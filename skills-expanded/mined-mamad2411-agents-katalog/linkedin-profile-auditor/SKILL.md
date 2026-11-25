---
name: linkedin-profile-auditor
description: 4-step Claude Projects setup for auditing LinkedIn profiles section by section — loads a system prompt + voice guide into a project, then runs a structured audit starting with 3 clarifying questions before reviewing each profile section
---

# LinkedIn Profile Auditor

A structured Claude Projects workflow for auditing LinkedIn profiles. Set up once, then run audits in any chat within the project.

## Setup (one-time, 4 steps)

### Step 1 — Create a Claude project
Open Claude, go to **Projects** in the sidebar, and create a new project. Name it **LinkedIn Profile Audit**.

### Step 2 — Paste the system prompt
Get the LinkedIn Profile Audit System Prompt file (search "Claude Profile Auditor" or comment "AUDIT" on the original post by the creator). Copy it in full and paste into the project's **Project Instructions**.

### Step 3 — Upload your voice guide and example audits
Add two files to the **Project Knowledge** base:
1. **Voice guide** — describes your writing style and tone so audits sound like you
2. **Example audits** — 1–3 past audits you liked, to calibrate quality and format

### Step 4 — Run your first profile audit
Start a new chat inside the project. Introduce yourself. Claude asks **3 quick questions**, then audits the profile section by section:
- Headline
- About / Summary
- Experience (top 2–3 roles)
- Featured section
- Skills
- Overall positioning and CTA

## Paste-ready intro prompt

```
Hi. I'd like to audit a LinkedIn profile. Let's begin.
```

Claude asks 3 clarifying questions (whose profile, audit goal, target audience), then proceeds section by section.

## Getting the full system prompt

Comment "AUDIT" on the original creator's post, or search "Claude Profile Auditor LinkedIn" to find the downloadable system prompt file. Without it in project instructions the audit still runs, but loses the structured section-by-section format.

## Related skills

- `linkedin-signal-outreach` — outreach sequencing once the profile is optimized
- `linkedin-virality-playbook` — content strategy once the profile is audit-ready
- `client-acquisition-skills` — converting profile visitors into inbound leads
