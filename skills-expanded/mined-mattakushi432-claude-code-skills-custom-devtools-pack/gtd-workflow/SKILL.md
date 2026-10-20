---
name: gtd-workflow
description: "When to activate: GTD, Getting Things Done, task capture, inbox zero, next actions, weekly review, contexts, projects list, someday maybe, trusted system"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: productivity
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# GTD Workflow Patterns

## Core GTD Model

### The Five Steps
```
1. CAPTURE  → Get everything out of your head
2. CLARIFY  → Process what each item means
3. ORGANIZE → Put things where they belong
4. REFLECT  → Review your system regularly
5. ENGAGE   → Do the right thing at the right time
```

## Step 1: Capture

### Capture Triggers (Mind Sweep)
Run this list when setting up or weekly review to capture everything:

**Personal:**
- Projects in progress
- Projects to start
- Commitments to others
- Things to follow up on
- Someday/maybe ideas
- Purchases to make
- Places to go
- People to contact

**Professional:**
- Waiting-for items
- Meetings to schedule
- Reports to write
- Emails to respond to
- Decisions to make
- Delegated tasks to track

**Rules:**
- One capture tool (or set of defined tools)
- Frictionless — capture must be faster than doing
- Not for storage — capture goes into inbox, then gets processed

## Step 2: Clarify

### The Clarify Decision Tree
```
Is it actionable?
├── NO → Trash / Someday-Maybe / Reference
└── YES → What is the next physical action?
    ├── Takes < 2 min? → DO IT NOW
    ├── Should someone else do it? → DELEGATE (add to Waiting-For)
    └── You should do it → DEFER
        ├── Specific date/time? → CALENDAR
        └── ASAP? → NEXT ACTIONS list
```

### What "Next Action" Means
A next action must be:
- Physical and visible (can be started without further thought)
- Context-appropriate (what device, place, person is needed?)

```
❌ "Work on proposal" → unclear starting point
✅ "Draft outline for Q3 proposal in Google Docs" → can start now

❌ "Fix relationship with Sarah" → not physical
✅ "Call Sarah, apologize for last week's email" → clear action

❌ "Exercise" → vague
✅ "Put gym shoes in car tonight" → first physical step
```

## Step 3: Organize

### The Six Lists
| List | Contents | Review |
|------|----------|--------|
| **Inbox** | Unprocessed captures | Continuously → empty |
| **Next Actions** | Physical next steps, by context | Daily |
| **Projects** | Any outcome requiring 2+ steps | Weekly |
| **Calendar** | Time/date specific + day-specific | Daily |
| **Waiting For** | Delegated items + expected date | Weekly |
| **Someday/Maybe** | Future ideas not committed to | Weekly |

### Context Labels (customize to your life)
```
@computer    — needs laptop or desktop
@phone       — calls to make
@errands     — out-of-house tasks to batch
@home        — tasks only doable at home
@office      — tasks only doable in office
@agenda:Name — items to discuss with specific person
@energy:low  — tasks doable when mentally tired
@waiting     — tracking others' deliverables
```

### Projects List Hygiene
```
A project = any desired outcome requiring 2+ next actions

Every project must have:
- Clear outcome statement (what does "done" look like?)
- At least one next action on the Next Actions list

Review monthly:
- Is this still active?
- Does it have a next action?
- Should it move to Someday/Maybe or be abandoned?

Project card template:
Project: [Desired outcome stated as completion]
Due: [If any]
Next action: [Specific first step]
Waiting for: [Any blocked items]
Notes: [Context, resources, constraints]
```

## Step 4: Reflect

### Weekly Review Checklist
```
COLLECT (empty inboxes)
□ Process all physical inboxes
□ Process all email inboxes to zero
□ Process all digital capture tools
□ Review meeting notes from the week
□ Mind sweep (use trigger list)

PROCESS (clarify everything collected)
□ All items processed per decision tree
□ Nothing left in inbox

ORGANIZE (update lists)
□ Review calendar (past 2 weeks + next 4 weeks)
□ Review all Projects — do each have a next action?
□ Review Next Actions — still relevant? Add new ones
□ Review Waiting For — chase anything overdue
□ Review Someday/Maybe — activate anything ready?

REFLECT
□ What went well this week?
□ What's the most important thing for next week?
□ Am I working on the right projects overall?
```

## Step 5: Engage

### Choosing What to Do Now (Three Models)

**Model 1: Four Criteria**
1. Context — what can I do here/now?
2. Time available — how much time do I have?
3. Energy — how much mental energy do I have?
4. Priority — given 1-3, what's most important?

**Model 2: Horizons of Focus**
| Horizon | Timeframe | Example |
|---------|-----------|---------|
| Runway | Current actions | Reply to email |
| 10K ft | Projects | Launch new feature |
| 20K ft | Areas of responsibility | Engineering excellence |
| 30K ft | 1-3 year goals | Become CTO |
| 40K ft | 3-5 year vision | Build $10M business |
| 50K ft | Life purpose | What kind of person? |

## GTD Tool Setup

### Minimal Viable GTD Stack
```
Capture: Notes app on phone (fastest friction)
Processing: Desktop app (Todoist, Things, OmniFocus, Notion)
Calendar: Google Calendar / Apple Calendar
Reference: Notion, Obsidian, or Google Drive
```

### Todoist GTD Setup
```
Projects:
├── Inbox (default)
├── Next Actions (with labels @computer, @phone, etc.)
├── Projects
│   ├── Project 1
│   └── Project 2
├── Waiting For (use due dates for expected date)
└── Someday Maybe
    ├── Books to read
    ├── Trips to take
    └── Project ideas
```

### Common GTD Failure Modes
| Problem | Cause | Fix |
|---------|-------|-----|
| Inbox never empties | Skipping clarify step | Time-box 30 min processing daily |
| Next Actions list huge | No prioritization | Limit to 10 "most important" flagged |
| System abandoned | Too complex | Simplify to 3 lists: Today, Next, Someday |
| Projects stall | No next action | Weekly review non-negotiable |
| Capture fails | Too many inboxes | Reduce to 2 (phone + email) |
