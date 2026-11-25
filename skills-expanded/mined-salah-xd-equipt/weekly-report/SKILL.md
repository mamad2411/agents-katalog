---
name: weekly-report
description: "Transforms bullet-point inputs into structured weekly reports with executive summary, metrics tables, wins, blockers with proposed solutions, and next-week priorities. Use when a user needs to compile a weekly status update, wants to present progress to clients or stakeholders, or needs to document team accomplishments and blockers."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Weekly Report

## When to Use This Skill

Use this skill when:
- A user has raw bullets or scattered updates and needs a polished weekly report
- Someone needs to send a status update to a client, boss, investor, or team
- A user says "write my weekly update," "status report," or similar

**DO NOT** use for daily standups, monthly/quarterly reports, proposals, or meeting notes.

---

## Core Principle

EVERY WEEKLY REPORT ANSWERS THREE QUESTIONS: WHAT GOT DONE, WHAT IS STUCK, AND WHAT HAPPENS NEXT. STRIP EVERYTHING ELSE.

---

## Audience Reference

| Audience | Tone | Focus |
|----------|------|-------|
| **Boss** | Concise, direct | Results, metrics, numbers |
| **Client** | Professional, outcome-focused | Deliverables, value delivered |
| **Team** | Detailed, transparent | Blockers, context, handoffs |
| **Investor** | Confident, growth-oriented | Milestones, revenue, MRR |

**DEFAULT: Client-facing tone** if audience is unspecified.

---

## Step 1: Understand

Gather these inputs (items 5-7 can be defaulted):

1. **Bullet points** -- what happened this week
2. **Metrics** -- any numbers worth reporting
3. **Wins** -- anything that exceeded expectations
4. **Blockers** -- anything stuck or waiting on someone
5. **Audience** -- boss, client, team, or investor (default: client)
6. **Project name** -- what this report covers
7. **Week dates** -- reporting period (default: current Mon-Fri)

If the user dumps a raw list, extract what you can and ask only for what is missing.

**GATE: Do not proceed until you have at least 3 bullets and know (or have defaulted) the audience.**

---

## Step 2: Structure

Organize inputs into six sections in this order:

| Section | Format | Rules |
|---------|--------|-------|
| **Executive Summary** | 2-3 sentences | Write LAST. Include status: on track / at risk / blocked. Must stand alone. |
| **Key Metrics** | Table: Metric, This Week, Last Week, Change | Only user-provided metrics. Omit Last Week/Change columns if no prior data. If none: "No metrics this week." |
| **Wins** | Bullet list | WHAT happened + WHY it matters. Min 1, max 5. Promote top completed task if no explicit wins. |
| **Work Completed** | Table: Task, Status, Notes | Map every bullet to a row. Status: "Done" or "In Progress (X%)". Group if 10+. |
| **Blockers & Solutions** | Table: Blocker, Impact, Solution, Owner | Every blocker MUST have a solution. Propose one if omitted. If none: "No blockers this week." |
| **Next Week Priorities** | Numbered list | 3-5 specific deliverables. Infer from in-progress tasks if not provided. |

Report header: `# Weekly Report: [Project Name]` with Period and Prepared For fields.

---

## Step 3: Present

1. Display the complete report in chat.
2. Call out inferences you made (promoted wins, inferred priorities).
3. Ask for approval before saving.

**GATE: Do not write to file until the user approves.**

---

## Step 4: Deliver

1. Write to file. Default: `weekly-report-[YYYY-MM-DD].md` (Friday date). Use user path if specified.
2. Confirm delivery. Suggest copying into email or Slack.
3. Offer to draft a send-along message.

---

## Example 1: Client-Facing Report -- Marketing Retainer

**Input:** "Greenleaf Organics retainer, client audience. 3 blog posts published, traffic +18%, newsletter 42% open rate, reel 12K views (record), 8 social posts drafted but need client photos, banner delayed -- no product photos. Next week: spring promo emails, April social calendar."

**Output:** Client tone. Summary leads with reel record and open rate. Blockers have specific asks ("Send photos by Wednesday"). Priorities: spring promo, April calendar, banner.

---

## Example 2: Internal Team Report -- Product Sprint

**Input:** "Beacon app sprint, team audience. Shipped notifications API, fixed 4 QA bugs, onboarding at 60% needs UX review, velocity 34/40 (85%), server costs $2,100 up from $1,800, Stripe sandbox 500 errors (ticket opened), Maria finished wireframes early. Next week: onboarding, push notification UI, Stripe."

**Output:** Team tone with technical detail. Summary: "85% velocity, API shipped, Stripe blocked." Metrics: velocity 85%, server costs +17%. Wins: API shipped (unblocks next work), Maria early, bugs down 25%. Blockers: Stripe (escalate Monday, staging fallback), UX review (Monday session).

---

## Recovery

| Situation | Action |
|-----------|--------|
| **Fewer than 3 bullets** | Ask for more. If user insists, work with what exists. Note "partial inputs." Never invent work. |
| **No metrics** | Replace table with "No metrics this week." Suggest tracking 2-3 consistent metrics going forward. |
| **No next-week priorities** | Infer from in-progress tasks. Flag inferences so user can adjust. |
| **Vague blocker** | Ask what specifically is blocking. If unclear, propose: "Schedule a sync to identify the obstacle." |
| **Different format** | Adapt. Always keep executive summary and blockers. |
| **File write fails** | Present in chat. Retry different path. After 3 failures, stop. |

---

## Anti-Patterns

- **DO NOT invent tasks, metrics, or wins** the user did not mention
- **DO NOT write blockers without solutions** -- a blocker without a path forward is a complaint
- **DO NOT exceed 5 next-week priorities** -- force-rank if more are provided
- **DO NOT use filler** like "progress was made on several fronts" -- every line must be specific
- **DO NOT change audience tone mid-report** -- client reports stay client-facing throughout
- **DO NOT skip the executive summary** -- busy readers often read only this section
