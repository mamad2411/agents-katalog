---
name: workflow-mapper
description: Maps business processes into text-based flowcharts with decision points, handoffs, and timing estimates, then identifies bottlenecks and automation opportunities. Use when a user wants to document how their business actually works, find inefficiencies, visualize a process, or decide what to automate.
allowed-tools: Read Write Bash(mkdir:*)
---

# Workflow Mapper

## When to Use This Skill

- User wants to document a business process or workflow
- User says "map my process" or "flowchart" or "how does this work" or "find bottlenecks"
- User is deciding what to automate and needs to see the current process first
- User is onboarding a team member and needs to show how things work
- User is experiencing inefficiency and cannot pinpoint where

## Core Principle

MAP THE PROCESS AS IT ACTUALLY IS, NOT AS IT SHOULD BE. Document reality first, then optimize. Premature optimization without understanding the current state always fails.

## Workflow

### Step 1: Identify the Process

Ask the user:
1. What process do you want to map? (e.g., "how we onboard a new client")
2. Where does it start? (trigger event)
3. Where does it end? (completion criteria)
4. Who is involved? (people, roles, tools)
5. How often does this process run? (daily, weekly, per client, etc.)

### Step 2: Walk Through the Process

Use this interviewing method:

1. "What happens first after [trigger]?"
2. "Then what? Who does that?"
3. "Are there any decisions or branches here?" (if yes, map both paths)
4. "How long does this step take?"
5. "What tool or system do you use for this?"
6. "What goes wrong here most often?"

Repeat until the user says "then it's done."

### Step 3: Build the Text-Based Flowchart

Use this notation system:

```
NOTATION GUIDE:
[Step]          = Action step
<Decision?>     = Yes/No branch
((Start/End))   = Process boundary
-->             = Flow direction
{Tool}          = System or tool used
*Role*          = Person responsible
~15 min~        = Time estimate
!! BOTTLENECK   = Identified problem
```

### Step 4: Analyze the Map

For every mapped process, deliver:

1. **Total process time** — Sum of all step durations
2. **Bottlenecks** — Steps that are slow, manual, or error-prone
3. **Handoff points** — Where work passes between people (high-risk for delays)
4. **Redundancies** — Steps that duplicate effort or information
5. **Automation candidates** — Steps that are rule-based, repetitive, and require no judgment

**Automation scoring:**

| Criteria | Score |
|----------|-------|
| Rule-based (no judgment needed) | +3 |
| Repetitive (happens daily/weekly) | +2 |
| Data moves between two tools | +2 |
| Takes more than 15 min each time | +1 |
| Error-prone when done manually | +2 |
| **Total 7+: Strong automation candidate** | |
| **Total 4-6: Partial automation possible** | |
| **Total 0-3: Keep manual** | |

### Step 5: Deliver Recommendations

Provide a prioritized improvement plan:

1. **Quick wins** — Changes that take under 1 hour and save time immediately
2. **Automation projects** — Tools or integrations to implement (with specific recommendations)
3. **Process redesigns** — Steps to eliminate, combine, or reorder
4. **Measurement** — How to track whether the improvement worked

## Example 1: Client Onboarding Process (Service Business)

**Context:** A branding agency onboards new clients after they sign a proposal.

```
WORKFLOW MAP: Client Onboarding — Branding Agency
===================================================
Trigger: Client signs proposal
End: Kickoff call completed, project begins

((CLIENT SIGNS PROPOSAL))
         |
         v
[Send welcome email with next steps]
  *Account Manager*  {Gmail}  ~10 min~
         |
         v
[Create client folder in Google Drive]
  *Account Manager*  {Google Drive}  ~5 min~
         |
         v
[Set up project in Asana with template]
  *Account Manager*  {Asana}  ~15 min~
         |
         v
[Send intake questionnaire]
  *Account Manager*  {Typeform}  ~5 min~
         |
         v
<Client completes questionnaire?>
     |              |
    YES             NO
     |              |
     v              v
     |         [Send reminder email — Day 3]
     |           *Account Manager*  {Gmail}  ~5 min~
     |              |
     |              v
     |         <Completed after reminder?>
     |           |              |
     |          YES             NO
     |           |              |
     |           v              v
     |           |         [Call client to walk through it]
     |           |           *Account Manager*  {Zoom}  ~30 min~
     |           |              |        !! BOTTLENECK: 40% of clients
     |           |              |           need this call. Questionnaire
     |           |              |           is too long (47 questions).
     |           |              v
     |<----------|<-------------|
     v
[Review questionnaire responses]
  *Creative Director*  {Typeform + Docs}  ~20 min~
         |
         v
[Prepare kickoff presentation]
  *Creative Director*  {Google Slides}  ~45 min~
         |                          !! BOTTLENECK: Done from scratch
         |                             every time. No template.
         v
[Schedule kickoff call]
  *Account Manager*  {Calendly}  ~5 min~
         |
         v
[Run kickoff call]
  *Creative Director + Account Manager*  {Zoom}  ~60 min~
         |
         v
[Send kickoff summary + timeline]
  *Account Manager*  {Gmail + Asana}  ~20 min~
         |
         v
((ONBOARDING COMPLETE — PROJECT BEGINS))


PROCESS ANALYSIS
=================

Total time (happy path):     2 hrs 45 min
Total time (with reminders): 3 hrs 50 min
People involved:             2 (Account Manager, Creative Director)
Tools used:                  5 (Gmail, Google Drive, Asana, Typeform, Zoom)
Handoff points:              2 (AM to CD for questionnaire review, CD back to AM for scheduling)

BOTTLENECKS IDENTIFIED:
1. Intake questionnaire completion (40% need a follow-up call)
   Root cause: 47 questions is too many
   Fix: Reduce to 15 essential questions, move rest to kickoff call

2. Kickoff presentation created from scratch every time
   Root cause: No template exists
   Fix: Build a master template, customize 3-4 slides per client

3. Manual folder + project setup (3 separate tools)
   Root cause: No automation between tools
   Fix: Zapier — proposal signed triggers folder + Asana project + welcome email

AUTOMATION CANDIDATES:
| Step                          | Score | Tool              |
|-------------------------------|-------|-------------------|
| Create Google Drive folder    | 8     | Zapier            |
| Set up Asana project          | 9     | Zapier + template |
| Send welcome email            | 7     | Zapier            |
| Send intake questionnaire     | 7     | Zapier            |
| Send reminder (Day 3)         | 8     | Typeform reminder  |
| Schedule kickoff call         | 5     | Calendly auto-link |

RECOMMENDED IMPROVEMENTS (Priority Order):
1. QUICK WIN: Reduce questionnaire from 47 to 15 questions [saves 30 min/client]
2. QUICK WIN: Build kickoff presentation template [saves 30 min/client]
3. AUTOMATION: Zapier workflow for folder + Asana + welcome email [saves 30 min/client]
4. PROCESS: Embed Calendly link in welcome email to eliminate scheduling step [saves 5 min]

TOTAL TIME AFTER IMPROVEMENTS: 1 hr 15 min (from 3 hrs 50 min)
```

## Example 2: Content Publishing Process (Solo Creator)

**Context:** A solo content creator publishes one blog post per week.

```
WORKFLOW MAP: Weekly Blog Post — Solo Creator
===============================================
Trigger: Monday morning (weekly cadence)
End: Post published and promoted

((MONDAY: CONTENT WEEK BEGINS))
         |
         v
[Choose topic from content calendar]
  *Creator*  {Notion}  ~10 min~
         |
         v
[Research keywords and outline]
  *Creator*  {Ahrefs + Google Docs}  ~45 min~
         |
         v
[Write first draft]
  *Creator*  {Google Docs}  ~2.5 hrs~
         |                    !! BOTTLENECK: Writing takes longest.
         |                       Often interrupted, spread across 2 days.
         v
[Edit and polish draft]
  *Creator*  {Google Docs + Grammarly}  ~45 min~
         |
         v
[Create featured image]
  *Creator*  {Canva}  ~30 min~
         |
         v
[Format and publish in WordPress]
  *Creator*  {WordPress}  ~30 min~
         |                    !! BOTTLENECK: Manual formatting —
         |                       copy-pasting, adding headers, images,
         |                       meta description, alt text every time.
         v
[Write social media posts (3 platforms)]
  *Creator*  {Buffer}  ~45 min~
         |
         v
[Write newsletter teaser]
  *Creator*  {ConvertKit}  ~20 min~
         |
         v
[Schedule everything]
  *Creator*  {Buffer + ConvertKit}  ~15 min~
         |
         v
((POST PUBLISHED AND PROMOTED))


PROCESS ANALYSIS
=================

Total time:        6 hrs 40 min per blog post
People involved:   1
Tools used:        7 (Notion, Ahrefs, Google Docs, Grammarly, Canva, WordPress, Buffer, ConvertKit)

BOTTLENECKS:
1. Writing draft (2.5 hrs, often interrupted)
   Fix: Time-block 2 hrs on Tuesday morning, no meetings
2. WordPress formatting (30 min of repetitive manual work)
   Fix: Use a blog post template in WordPress with pre-set formatting
3. Social media writing (45 min to write 3 platform versions)
   Fix: Use Claude to generate platform variations from the blog post

AUTOMATION CANDIDATES:
| Step                        | Score | Tool                    |
|-----------------------------|-------|-------------------------|
| WordPress formatting        | 7     | WordPress block template |
| Social post scheduling      | 6     | Buffer RSS auto-post     |
| Newsletter teaser            | 5     | ConvertKit automation    |
| Featured image              | 4     | Canva template           |

RECOMMENDED IMPROVEMENTS:
1. QUICK WIN: Create WordPress post template [saves 20 min/week]
2. QUICK WIN: Build 3 Canva templates for featured images [saves 20 min/week]
3. PROCESS: Time-block writing on Tuesday 8-10am [reduces total time by focusing]
4. AUTOMATION: Use Claude to draft social posts from blog content [saves 30 min/week]

TOTAL TIME AFTER IMPROVEMENTS: 4 hrs 50 min (from 6 hrs 40 min)
```

## Recovery and Fallback

- If the user cannot walk through the process in order, ask: "What was the last time you did this? Walk me through that specific instance from memory."
- If the process has too many branches (more than 5 decision points), map the main happy path first, then add branches one at a time
- If the user does not know how long steps take, estimate in ranges (15-30 min) and mark with "~estimated~"
- If the process involves tools the user cannot name specifically, use generic labels and note "identify specific tool" as an action item
- If the process is informal and undocumented ("we just kind of figure it out"), that is the finding — document what actually happens, then formalize

## Constraints

- **ALWAYS map the current process first** before suggesting improvements — never jump to the optimized version
- **ALWAYS include time estimates** for every step, even if approximate
- **ALWAYS identify at least one bottleneck** — if none exist, the process is too simple to map
- **ALWAYS include an automation scoring table** for processes with 5+ steps
- Use text-based notation only (no Mermaid, no images, no external diagramming tools)
- Mark every bottleneck with `!! BOTTLENECK` inline in the flowchart
- Include the role/person responsible at every step
- Include the tool/system used at every step
- Keep flowcharts under 40 steps (break larger processes into sub-processes)
