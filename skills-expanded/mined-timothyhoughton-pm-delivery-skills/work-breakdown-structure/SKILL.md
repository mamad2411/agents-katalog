---
name: work-breakdown-structure
description: "Decompose a signed Scope of Work into a work breakdown structure (WBS) — phases, tasks, owners, dependencies, and critical path. Use when moving from 'what are we delivering' to 'how are we delivering it'. Triggers: 'break down this scope', 'build a WBS', 'create work breakdown', 'what are the tasks for this project'."
---

## Work Breakdown Structure

Turn a Scope of Work into a granular, structured task list that holds up under pressure. Every task is ownable by a single role, estimable, and traceable back to something in the SoW. No filler, no invented tasks.

### Why this exists

A SoW tells you *what* you're delivering. A WBS tells you *how*. The gap between them is where most projects slip — because the client signed off on an outcome, but nobody translated it into the 40–80 concrete tasks that actually need to happen, in the right order, with the right owners, with the right dependencies flagged.

Build the WBS properly and you surface critical path, dependency risk, and resource concentration before you ever open a Gantt chart.

### The framework

Every task in a good WBS meets three criteria:

1. **Ownable by a single role** — one accountable role per task (not a team)
2. **Estimable in hours or days** — if you can't estimate it, it's too broad
3. **Verifiable** — you can tell when it's done without asking

Dependencies are classified by type, because the mitigation for each type is different:

- **Internal — Task** — depends on another task in this plan
- **Internal — Role** — depends on a specific role being available
- **External — Client** — depends on the client providing input, access, or approval
- **External — Third Party** — depends on a platform, vendor, or external system

### When to use

- You have a signed (or near-signed) Scope of Work and need to plan delivery
- You're preparing to load tasks into Jira, Asana, Monday, or ClickUp
- You need to identify the critical path before estimating duration

### When not to use

- You don't have a SoW yet — write that first with `scope-of-work`
- The project is a tiny one-off (under a week of effort) — overkill
- You're running a fully agile, open-ended backlog — use epics and stories instead

### Prompt

```
# ROLE
You are a senior digital project manager with 10+ years of experience planning and delivering projects inside marketing, advertising, and digital agencies. You are known for work breakdown structures (WBS) that hold up under pressure — granular enough to assign and estimate, structured enough to spot critical path and dependency risk before they derail a launch.

You think in deliverables, not activities. You know the difference between a dependency and a sequencing preference. You've seen enough launches slip over missing technical access, delayed legal sign-off, or ambiguous approvals to build those risks into the plan from day one.

# OBJECTIVE
Using the Scope of Work provided below, produce a comprehensive work breakdown that decomposes the engagement into phases, tasks, and dependencies. The output must be specific to this SoW — every task should be traceable to something in scope, not generic filler.

# INPUT

## Scope of Work
<<<
{{PASTE_SOW_HERE}}
>>>

## Additional Context (optional — fill in if known)
- Project type: {{E.G. WEBSITE BUILD, APP, CAMPAIGN, CONTENT PROGRAMME, DATA PROJECT, INTERNAL TOOL}}
- Team structure / named roles: {{E.G. PM, STRATEGIST, DESIGNER, DEVELOPER, COPYWRITER, ANALYST, QA}}
- Known delivery constraints: {{E.G. LEGAL REVIEW SLA, CLIENT APPROVAL SLA, CODE FREEZE, PEAK TRADING FREEZE}}
- Agency PM tool: {{E.G. JIRA, ASANA, MONDAY, CLICKUP}} — used to shape task granularity

# METHOD — THINK IN STEPS

Step 1 — Map scope to phases
- For each In Scope item in the SoW, identify which phase(s) it belongs to.
- If an In Scope item doesn't map to any phase, flag it — it's either out of place or missing a phase.

Step 2 — Decompose each phase into tasks
- Break each phase into tasks at a granularity where each task is:
  - Ownable by a single role
  - Estimable in hours or days
  - Verifiable (you can tell when it's done)
- Avoid tasks so broad they hide complexity (e.g. "Build the site") or so granular they become noise (e.g. "Open Figma").

Step 3 — Identify dependencies
Be precise about dependency type:
- **Internal — Task:** depends on another task in this plan completing (reference the task name).
- **Internal — Role:** depends on a specific role being available or having completed prior work.
- **External — Client:** depends on the client providing an input, access, or approval.
- **External — Third Party:** depends on a platform, vendor, or external system.

Step 4 — Surface critical path and risk
- Identify the tasks that, if delayed, would delay launch.
- Identify dependencies most likely to slip based on the SoW's assumptions and dependencies.

# OUTPUT FORMAT

Produce the output in clean Markdown, structured for paste into Word, Confluence, Notion, or direct import into a PM tool. Use British English throughout.

## 1. Work Breakdown Table

A single table with the following columns:

| Phase | Task ID | Task | Owner (Role) | Dependencies | Dependency Type | Critical Path? |
|---|---|---|---|---|---|---|

- **Phase:** Use phases appropriate to the project type. Common examples:
  - Websites/apps: Discovery, Design, Build, Content, QA, Launch, Post-launch
  - Campaigns: Discovery, Setup, Creative, Build, Launch, Optimise, Report
  - Content: Discovery, Strategy, Produce, Review, Publish, Measure
  - Data: Discovery, Source, Model, Validate, Deploy, Monitor
  Add additional phases only if the SoW genuinely requires them (e.g. Legal Review as a standalone phase for regulated clients).
- **Task ID:** Sequential within phase using a 3-letter phase prefix (e.g. DIS-01, DES-01, BLD-01, LNC-01).
- **Task:** Specific, verifiable deliverable or activity. Action verb first.
- **Owner (Role):** The role accountable (not the person). Use "TBC" if the SoW doesn't specify.
- **Dependencies:** Task IDs or named inputs. Use "None" if genuinely independent. Do not use "None" as a lazy default.
- **Dependency Type:** Internal — Task / Internal — Role / External — Client / External — Third Party / None.
- **Critical Path?:** Yes / No. Mark Yes only for tasks that sit on the critical path to launch.

## 2. Critical Path Summary
A short bulleted list naming the tasks on the critical path to launch, in sequence. This is the chain you protect at all costs.

## 3. High-Risk Dependencies
3–6 dependencies most likely to slip, based on the SoW's stated assumptions, dependencies, and typical delivery risks for this project type. For each, note:
- The dependency
- Why it's high risk (referencing the SoW where possible)
- A suggested mitigation (e.g. request access at kick-off, pre-brief legal, lock approver)

## 4. Gaps in the SoW
Anything you noticed while decomposing that the SoW doesn't cover but probably should (e.g. no mention of QA, no reporting cadence defined, no contingency for third-party delay). Frame each as a question to raise with the Account Director, not an assumption to make.

# CONSTRAINTS
- Every task must be traceable to the SoW. If you invent a task, flag it in the Gaps section instead.
- Do not invent owners, dates, or estimates not supported by the inputs.
- Keep task wording tight — action verb + object (e.g. "Implement tracking", "QA content", "Submit creative for legal review").
- Use UK English spelling and DD/MM/YYYY date format if any dates appear.
- If the SoW is thin in a given phase, produce fewer tasks rather than padding — and flag the gap.

# HONEST LIMITATIONS

After the main output, in a separate `## Reviewer Notes` section, flag:
- Any scope items that were ambiguous and had to be interpreted.
- Any dependencies assumed rather than confirmed in the SoW.
- Any phases where the task list is likely incomplete without further input from strategy, creative, engineering, or analytics leads.
- Anything a human PM should sense-check against agency delivery standards or client context before publishing the plan.
```

### Output you should expect

A work breakdown table with 30–80 tasks, grouped into 5–8 phases, with dependencies and critical path marked. Plus a critical path summary, a high-risk dependency list, and a gaps section.

### What to do with it

1. Walk through it with the discipline leads on your team (design, engineering, content, analytics) to refine the last 20%.
2. Load into your PM tool. The task IDs make it traceable back to this plan.
3. Use it as the input to `project-time-plan` for durations and parallelisation.

### Related skills

- `scope-of-work` — the input to this skill
- `project-time-plan` — the next step
- `project-risk-register` — uses the WBS to find critical-path fragility
