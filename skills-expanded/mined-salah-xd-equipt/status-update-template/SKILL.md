---
name: status-update-template
description: "Creates reusable status update templates for projects, clients, or stakeholders with progress indicators and clear formatting."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Status Update Template

## When to Use This Skill

Use this skill when you need to:
- Create a reusable template for project or client status updates
- Standardize how progress is reported across projects
- Build stakeholder-appropriate update formats with the right level of detail
- Save time on weekly or monthly reporting with fill-in-the-blank templates

**DO NOT** use this skill for detailed project plans, meeting agendas, or performance reviews. This is for recurring progress communication.

---

## Core Principle

A STATUS UPDATE SHOULD TAKE 5 MINUTES TO WRITE AND 2 MINUTES TO READ — IF IT TAKES LONGER, THE TEMPLATE IS WRONG OR THE PROJECT NEEDS A MEETING INSTEAD.

---

## Phase 1: Context

Define who receives the update and what they need to know.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Audience** | "Who reads these updates? (client, team, investors, stakeholders)" | Client |
| **Frequency** | "How often do you send updates? (daily, weekly, biweekly, monthly)" | Weekly |
| **Format** | "How do you send them? (email, Slack, project tool, document)" | Email |
| **Current pain** | "What is broken about your current update process?" | Takes too long, inconsistent |
| **Projects/topics** | "What are you reporting on? (single project, multiple clients, department)" | Single project |

**GATE: Confirm audience and format before building the template.**

---

## Phase 2: Build Template

Create the status update template matched to the audience.

### Client Status Update

```
Subject: [Project Name] — Weekly Update [Date]

Hi [Name],

**Overall status:** 🟢 On Track / 🟡 At Risk / 🔴 Off Track

## This Week
- [Accomplishment 1]
- [Accomplishment 2]
- [Accomplishment 3]

## Next Week
- [Planned task 1]
- [Planned task 2]

## Needs from You
- [Decision or input needed — with deadline]
- [Approval needed — with deadline]

## Risks / Blockers
- [Risk or issue — and proposed solution]

[Name]
```

### Team/Internal Status Update

```
## [Project/Team] Status — Week of [Date]

**Status:** 🟢 / 🟡 / 🔴

### Progress
| Task | Owner | Status | Notes |
|------|-------|--------|-------|
| [Task] | [Name] | Done / In Progress / Blocked | [Note] |

### Key Metrics
| Metric | Last Week | This Week | Trend |
|--------|----------|-----------|-------|
| [Metric] | [Value] | [Value] | Up / Down / Flat |

### Blockers
- [Blocker + who can unblock it]

### Decisions Needed
- [Decision + deadline]
```

### Investor/Stakeholder Update

```
## [Business Name] — [Month] Update

### Highlights
- [Top win or milestone]
- [Key metric improvement]
- [Strategic development]

### Key Metrics
| Metric | Last Month | This Month | Target | Status |
|--------|-----------|-----------|--------|--------|
| Revenue | $[X] | $[X] | $[X] | On/Off Track |
| [Metric] | [Value] | [Value] | [Target] | On/Off Track |

### Challenges
- [Challenge + what you are doing about it]

### Next Month Focus
- [Priority 1]
- [Priority 2]

### Ask (if any)
- [Specific request — intro, advice, resource]
```

**GATE: Present template(s) for review and customization.**

---

## Phase 3: Customize

Refine the template to fit the user's specific needs.

### Status Indicators

Define what each status color means for consistency:

```
🟢 **On Track:** All deliverables on schedule, no blockers
🟡 **At Risk:** Minor issues that could delay if not addressed this week
🔴 **Off Track:** Deadline will be missed or major blocker exists
```

### Section Customization

- Add project-specific sections (budget tracking, hours logged, milestone progress)
- Remove sections that do not apply
- Adjust detail level — clients want outcomes, teams want tasks, investors want metrics

### Distribution Checklist

```
## Update Distribution

- [ ] Write update using template (5 min target)
- [ ] Review for clarity and completeness (2 min)
- [ ] Attach any relevant files or links
- [ ] Send to [audience] via [channel]
- [ ] File a copy in [project folder]
```

---

## Phase 4: Automate

Help the user make updates as effortless as possible.

### Time-Saving Tips

- Block 15 minutes on the same day each week for writing updates
- Keep a running "done" list during the week so you do not have to remember on Friday
- Use the same template every time — consistency speeds up both writing and reading
- Pre-populate next week's "planned" section from this week's update

### Review Triggers

Update the template when:
- The audience requests different information
- A new project type requires different sections
- Updates consistently take more than 10 minutes to write

---

## Anti-Patterns

- **Too much detail** — the client does not need to know you fixed a CSS bug. Report outcomes, not activities.
- **No status indicator** — making the reader hunt for whether things are on track wastes their time. Lead with the status.
- **Missing "needs from you"** — if the update does not say what the reader should do, it is informational noise.
- **Inconsistent timing** — updates that arrive on random days lose trust. Same day, same time, every period.
- **Writing from scratch each time** — without a template, each update takes 3x longer and covers different things.

---

## Recovery

- **Client says updates are not useful:** Ask what they want to see. Often they want less detail and more "what do you need from me."
- **User forgets to send updates:** Set a recurring calendar event. The update is not optional — it is a trust-building habit.
- **Multiple projects, one template:** Create a master template with project-specific sections, or send separate short updates per project.
- **User has nothing to report:** "No progress this week due to [reason]. Expected to resume [date]." is a valid update. Silence is worse.
- **Stakeholder wants more detail:** Add an appendix section for deep-dives. Keep the main update scannable.
