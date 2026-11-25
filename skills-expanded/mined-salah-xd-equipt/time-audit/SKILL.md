---
name: time-audit
description: Analyzes time allocation across activities and recommends optimization strategies with categorization, value scoring, and reallocation plans. Use when a freelancer or solopreneur feels busy but unproductive, wants to find where their time goes, needs to free up hours for higher-value work, or suspects they are spending too much time on low-impact tasks.
allowed-tools: Read Write Bash(mkdir:*)
---

# Time Audit

## When to Use This Skill

- User says "I'm so busy but nothing gets done" or "where does my time go"
- User wants to free up hours in their week for a new project or priority
- User is working 50+ hours and wants to get to 40
- User suspects they are spending time on low-value activities
- User says "time audit" or "time tracking" or "optimize my schedule"

## Core Principle

TIME IS NOT MANAGED — IT IS ALLOCATED. The goal is not to do more in less time. The goal is to SPEND MORE TIME ON HIGH-VALUE ACTIVITIES AND LESS ON EVERYTHING ELSE.

## Workflow

### Step 1: Capture the Raw Data

Ask the user to describe a typical week. Use this interview approach:

"Walk me through a typical Monday, hour by hour. Start from when you wake up."

Repeat for each workday. If the user cannot do all 5 days, get at least 3 representative days.

For each activity, capture:
- What they did
- How long it took
- Whether it was planned or reactive
- How they felt doing it (energized, neutral, drained)

### Step 2: Categorize Every Activity

Place each activity into one of these categories:

| Category | Definition | Examples |
|----------|-----------|----------|
| **Revenue-Generating** | Directly produces income | Client work, sales calls, product creation |
| **Revenue-Enabling** | Supports future income | Marketing, networking, content creation |
| **Operations** | Keeps the business running | Email, invoicing, scheduling, admin |
| **Development** | Builds skills or systems | Learning, SOPs, tool setup, hiring |
| **Waste** | No business value | Endless scrolling, unnecessary meetings, perfectionism loops |

### Step 3: Score Each Activity

Apply the Value-Energy Matrix:

```
                    HIGH VALUE
                        |
          ZONE A:       |       ZONE B:
          PROTECT       |       MAXIMIZE
          (high value,  |       (high value,
           draining)    |        energizing)
                        |
  DRAINING -------------|------------- ENERGIZING
                        |
          ZONE C:       |       ZONE D:
          ELIMINATE      |       AUTOMATE/DELEGATE
          (low value,   |       (low value,
           draining)    |        energizing but
                        |        a trap)
                        |
                    LOW VALUE
```

- **Zone A** tasks: Keep but limit. Schedule them when energy is highest.
- **Zone B** tasks: Protect and expand. This is where you do your best work.
- **Zone C** tasks: Eliminate or delegate immediately. These destroy productivity.
- **Zone D** tasks: Beware — these feel good but do not move the needle. Automate or time-cap.

### Step 4: Build the Time Allocation Report

```
TIME AUDIT REPORT
==================

CURRENT WEEKLY TIME ALLOCATION:

Category            | Hours/Week | % of Total | Target % | Gap
--------------------|-----------|------------|----------|----
Revenue-Generating  |    XX     |    XX%     |   40%    | +/-
Revenue-Enabling    |    XX     |    XX%     |   25%    | +/-
Operations          |    XX     |    XX%     |   20%    | +/-
Development         |    XX     |    XX%     |   10%    | +/-
Waste               |    XX     |    XX%     |    5%    | +/-
TOTAL               |    XX     |   100%     |  100%    |

TOP 5 TIME CONSUMERS:
1. [Activity] — XX hrs/week (Category, Zone X)
2. [Activity] — XX hrs/week (Category, Zone X)
3. [Activity] — XX hrs/week (Category, Zone X)
4. [Activity] — XX hrs/week (Category, Zone X)
5. [Activity] — XX hrs/week (Category, Zone X)

BIGGEST SURPRISES:
- [Activity the user did not realize was taking so much time]
- [Category that is over/under-represented]
```

### Step 5: Create the Reallocation Plan

Deliver specific, actionable recommendations:

```
REALLOCATION PLAN
==================

ELIMINATE (save X hrs/week):
- [Activity]: Why it can go, what happens if you stop
- [Activity]: Why it can go, what happens if you stop

DELEGATE (save X hrs/week):
- [Activity]: Who could do this, estimated cost
- [Activity]: Who could do this, estimated cost

AUTOMATE (save X hrs/week):
- [Activity]: Tool recommendation, setup time
- [Activity]: Tool recommendation, setup time

BATCH (save X hrs/week):
- [Activity]: Move from daily to 2x/week, batch on [days]
- [Activity]: Move from reactive to scheduled, block on [day/time]

PROTECT (add X hrs/week):
- [Activity]: Block [day] [time] as non-negotiable
- [Activity]: Increase from X to Y hrs/week

NET RESULT: [X] hours freed, reallocated to [specific activities]
```

## Example 1: Freelance Web Designer

**Context:** Alex is a freelance web designer working 52 hours/week. Wants to get to 40 hours and launch a course.

```
TIME AUDIT REPORT: Alex — Freelance Web Designer
==================================================

CURRENT WEEKLY TIME ALLOCATION (52 hrs):

Category            | Hours/Week | % of Total | Target % | Gap
--------------------|-----------|------------|----------|-------
Revenue-Generating  |    18     |    35%     |   40%    | -5%
Revenue-Enabling    |     6     |    12%     |   25%    | -13%
Operations          |    19     |    37%     |   20%    | +17%
Development         |     3     |     6%     |   10%    | -4%
Waste               |     6     |    12%     |    5%    | +7%
TOTAL               |    52     |   100%     |  100%    |

TOP 5 TIME CONSUMERS:
1. Client design work — 15 hrs/week (Revenue-Generating, Zone B)
2. Email + Slack — 8 hrs/week (Operations, Zone C)
3. Client revisions — 6 hrs/week (Operations, Zone A)
4. Social media browsing — 4 hrs/week (Waste, Zone C)
5. Administrative tasks — 4 hrs/week (Operations, Zone C)

BIGGEST SURPRISES:
- Email/Slack consumes 8 hrs/week (1.5 hrs/day!) — Alex checks it 30+ times/day
- Client revisions take 6 hrs/week because revision scope is undefined in contracts
- Only 6 hrs/week on marketing — explains why pipeline is inconsistent

VALUE-ENERGY MATRIX PLACEMENT:
Zone A (Protect, high value but draining): Client revisions, sales calls
Zone B (Maximize, high value + energizing): Design work, content creation, course planning
Zone C (Eliminate, low value + draining): Email triage, admin, social browsing
Zone D (Automate, low value + energizing): Exploring new design tools, reorganizing files


REALLOCATION PLAN
==================

ELIMINATE (save 4 hrs/week):
- Social media browsing during work hours: Install site blocker (Cold Turkey)
  during 9am-12pm and 1pm-5pm. Allow 30 min at lunch only. Saves 3 hrs/week.
- Attending 2 optional industry meetups/month: Drop to 1. Saves 1 hr/week.

DELEGATE (save 3 hrs/week):
- Invoice creation and payment follow-up: Hire bookkeeper ($200/month).
  Saves 2 hrs/week.
- Email inbox first-pass triage: VA reviews at 9am and 2pm, flags
  client emails, archives rest. Saves 1 hr/week.

AUTOMATE (save 3 hrs/week):
- Proposal creation: Use a Notion template with pre-filled sections
  instead of writing from scratch. Saves 1.5 hrs/week.
- Client onboarding: Zapier triggers welcome email + folder creation
  + Asana project when proposal is signed. Saves 1 hr/week.
- Meeting scheduling: Replace email back-and-forth with Calendly.
  Saves 30 min/week.

BATCH (save 2 hrs/week):
- Email: Check 3x/day (9am, 1pm, 5pm) instead of constantly.
  Saves 2 hrs/week in context-switching.

PROTECT (reallocate 8 hrs):
- Course development: Block Tuesday + Thursday 8-10am. Add 4 hrs/week.
- Content creation (LinkedIn + portfolio): Block Friday 9-11am. Add 2 hrs/week.
- Prospecting and outreach: Block Monday 9-10am. Add 1 hr/week.

PROCESS FIX:
- Add "3 revision rounds included" clause to all contracts.
  Revision 4+ billed at $150/hr. Saves 2-3 hrs/week over time.

NET RESULT:
- Before: 52 hrs/week, 12% on marketing, 0% on course
- After: 40 hrs/week, 25% on marketing + course, operations cut in half
- Course launch feasible in 12 weeks at 4 hrs/week
```

## Example 2: E-commerce Store Owner

**Context:** Priya runs a Shopify store selling handmade candles. Works 45 hrs/week. Revenue plateaued at $6K/month.

```
TIME AUDIT REPORT: Priya — E-commerce (Handmade Candles)
=========================================================

CURRENT WEEKLY TIME ALLOCATION (45 hrs):

Category            | Hours/Week | % of Total | Target % | Gap
--------------------|-----------|------------|----------|-------
Revenue-Generating  |    20     |    44%     |   40%    | +4%
Revenue-Enabling    |     5     |    11%     |   25%    | -14%
Operations          |    14     |    31%     |   20%    | +11%
Development         |     2     |     4%     |   10%    | -6%
Waste               |     4     |     9%     |    5%    | +4%
TOTAL               |    45     |   100%     |  100%    |

TOP 5 TIME CONSUMERS:
1. Making candles (production) — 15 hrs/week (Revenue-Generating, Zone B)
2. Order fulfillment + shipping — 8 hrs/week (Operations, Zone C)
3. Customer service emails — 4 hrs/week (Operations, Zone C)
4. Instagram posting + stories — 3 hrs/week (Revenue-Enabling, Zone D)
5. Inventory management — 3 hrs/week (Operations, Zone A)

CRITICAL INSIGHT:
Priya spends 44% of her time MAKING candles and 31% SHIPPING them.
Only 11% goes to marketing. Revenue is plateaued because she is
maxed on production capacity, not demand. She needs to either:
  A) Outsource production to scale volume, OR
  B) Raise prices to increase revenue per unit

REALLOCATION PLAN
==================

ELIMINATE (save 2 hrs/week):
- Perfectionism on Instagram stories: Set 20-min timer per story.
  Currently spending 45 min editing each one. Saves 1.5 hrs/week.
- Manual inventory counting: Trust Shopify numbers, count monthly
  not weekly. Saves 30 min/week.

DELEGATE (save 5 hrs/week):
- Order fulfillment: Hire part-time helper for packing + shipping
  ($15/hr, 8 hrs/week = $120/week). Saves 6 hrs/week for Priya
  (she stays for 2 hrs to QC). Net: 5 hrs reclaimed.

AUTOMATE (save 3 hrs/week):
- Customer service: Set up FAQ page + auto-responses for top 5
  questions (shipping times, ingredients, returns). 60% of emails
  are the same 5 questions. Saves 2.5 hrs/week.
- Shipping label creation: Use Shopify Shipping auto-labels
  instead of manual USPS entry. Saves 30 min/week.

PROTECT (reallocate 7 hrs):
- Marketing strategy + email list building: Block Mon + Wed
  2-4pm. Add 4 hrs/week.
- Product development (new scents, bundles): Block Friday
  morning. Add 2 hrs/week.
- Wholesale outreach: Block Tuesday 9-10am. Add 1 hr/week.

NET RESULT:
- Before: 45 hrs/week, 11% on marketing, revenue stuck at $6K
- After: 38 hrs/week, 28% on marketing + growth
- Projected impact: Email list + wholesale = $8-10K/month in 90 days
```

## Recovery and Fallback

- If the user cannot recall their week hour by hour, ask them to track for 3 days using a simple spreadsheet (activity, start time, end time, category) and come back
- If the user's time is mostly reactive (customer emergencies, boss interruptions), focus the audit on identifying which reactive tasks can be prevented or systematized
- If the user works irregular hours (gig worker, parent, etc.), audit 2 "typical" days rather than a full week and extrapolate
- If the user resists cutting activities ("everything is important"), ask: "If you had a medical emergency and could only work 20 hours next week, what would you do?" — that reveals true priorities
- If time data is too vague to analyze, use ranges and mark confidence levels (HIGH/MEDIUM/LOW confidence in estimate)

## Constraints

- **ALWAYS categorize every activity** into the 5 categories — uncategorized time is invisible time
- **ALWAYS calculate percentages** — raw hours without percentages hide the real story
- **ALWAYS include the Value-Energy Matrix** — it prevents the user from cutting energizing work they need
- **ALWAYS provide a concrete reallocation plan** — the audit without actions is just a guilt trip
- **NEVER recommend working more hours** — the goal is reallocation, not expansion
- Include target percentages for comparison (40/25/20/10/5 as defaults, adjustable)
- Round time estimates to nearest 30 minutes
- Cap recommendations at 5-7 actions (more than that overwhelms)
