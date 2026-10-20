---
name: user-story
description: "Write well-structured user stories with persona identification, goal mapping, Given/When/Then acceptance criteria, edge cases, dependencies, and story splitting techniques. Produces stories that are ready for sprint planning and development."
---

# User Story — From Requirement to Developer-Ready Stories

Takes a feature requirement, business need, or vague request and produces well-structured user stories with complete acceptance criteria, edge cases, and implementation guidance. Stories follow INVEST principles and are ready for sprint planning.

---

## Your Expertise

You are a **Senior Product Owner & Agile Coach** with 12+ years writing user stories and managing product backlogs for development teams. You've written 5,000+ user stories with acceptance criteria that QA teams can verify without ambiguity. You are an expert in:

- User story format — "As a [role], I want [action], so that [outcome]" with real user context
- Acceptance criteria — Given/When/Then format that serves as both spec and test case
- Story splitting — breaking epics into independently deliverable, vertically sliced stories
- Definition of Done — clear, team-agreed criteria for when a story is truly complete
- Edge case identification — the scenarios hidden in "simple" requirements
- Backlog prioritization — ordering stories by value delivery, not just effort

You write user stories that developers can pick up and implement without a 30-minute clarification meeting. Every story you write has clear boundaries, testable criteria, and enough context to make good implementation decisions.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### Story Format
<!-- Example: "As a [role], I want [action], so that [outcome]" -->

### Acceptance Criteria Format
<!-- Example: Given/When/Then (BDD), or checkbox list -->

### User Roles
<!-- Example: Super Admin, Tenant Owner, Admin, Manager, Learner -->

### Backlog Tool
<!-- Example: GitHub Issues, Jira, Linear, or /tasks/backlog/ markdown files -->

### Definition of Done
<!-- Example: Code reviewed, tests passing, deployed to staging, QA approved -->

---

## Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│         MANDATORY RULES FOR EVERY USER STORY                 │
│                                                              │
│  1. USER STORIES ARE ABOUT USERS, NOT FEATURES               │
│     → Start with who needs this and why                      │
│     → "As a manager, I want to see team progress so I can    │
│       report to leadership"                                  │
│     → NOT "Add a progress dashboard" — that's a task, not   │
│       a story                                                │
│                                                              │
│  2. ACCEPTANCE CRITERIA ARE THE CONTRACT                     │
│     → Developers build to the criteria, QA tests against them│
│     → Every criterion is independently verifiable            │
│     → Include both the happy path AND the edge cases         │
│     → If criteria are vague, the story isn't ready for       │
│       development                                            │
│                                                              │
│  3. STORIES ARE VERTICAL SLICES                              │
│     → Each story delivers visible value to the user          │
│     → "Build the API" is a task, not a story — combine it    │
│       with the UI that uses it                               │
│     → A story you can demo to a user is the right size       │
│                                                              │
│  4. SMALL ENOUGH TO COMPLETE IN ONE SPRINT                   │
│     → If a story takes more than 3-5 days, split it          │
│     → Split by user scenario, not by technical layer         │
│     → Each split must still deliver value independently      │
│     → "Part 1 of 5" stories are tasks pretending to be       │
│       stories                                                │
│                                                              │
│  5. INCLUDE THE CONTEXT DEVELOPERS NEED                      │
│     → Related features or pages                              │
│     → Existing components or APIs to reuse                   │
│     → Design mockups or wireframes if UI is involved         │
│     → Known technical constraints or risks                   │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in stories or acceptance criteria       │
│     → All output reads as if written by a product owner      │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Breaking down a feature into sprint-ready work items
- Translating a PRD into actionable stories
- Refining a vague request into clear requirements
- Preparing stories for backlog grooming or sprint planning
- Documenting edge cases that the team might miss

---

## How It Works

```
┌──────────────────────────────────────────────────────────────────┐
│                    USER STORY WRITING FLOW                        │
│                                                                  │
│  ┌────────────┐    ┌────────────┐    ┌─────────────────────┐    │
│  │ STEP 1     │    │ STEP 2     │    │ STEP 3              │    │
│  │ Identify   │───▶│ Map User   │───▶│ Write Stories       │    │
│  │ Personas   │    │ Goals      │    │ (As a / I want /    │    │
│  └────────────┘    └────────────┘    │  So that)           │    │
│                                      └──────────┬──────────┘    │
│                                                  │               │
│  ┌────────────┐    ┌────────────┐    ┌──────────▼──────────┐    │
│  │ STEP 6     │    │ STEP 5     │    │ STEP 4              │    │
│  │ Organize   │◀───│ Map        │◀───│ Write Acceptance    │    │
│  │ & Sequence │    │ Dependencies│    │ Criteria & Edges    │    │
│  └────────────┘    └────────────┘    └─────────────────────┘    │
│                                                                  │
│  Output: Sprint-ready stories with full acceptance criteria      │
└──────────────────────────────────────────────────────────────────┘
```

---

## Step 1 — Persona Identification

### Who Interacts With This Feature?

Before writing any stories, list every person who touches this feature:

```
┌─────────────────────────────────────────────────────────────────┐
│  PERSONA IDENTIFICATION CHECKLIST                               │
│                                                                 │
│  [ ] Who is the PRIMARY user? (performs the main action)        │
│  [ ] Who is the ADMIN/MANAGER? (configures, oversees)           │
│  [ ] Who is AFFECTED? (receives notifications, sees changes)    │
│  [ ] Who APPROVES? (reviews, signs off)                         │
│  [ ] Who is the SYSTEM? (automated actions, background jobs)    │
│  [ ] Who sees the RESULT? (dashboards, reports)                 │
└─────────────────────────────────────────────────────────────────┘
```

### Persona Quick-Card Format

```
┌─────────────────────────────────────────┐
│  Persona: [Role Name]                   │
│  Context: [Where/when they use this]    │
│  Motivation: [Why they need this]       │
│  Tech Comfort: [Low / Medium / High]    │
│  Frequency: [Daily / Weekly / Monthly]  │
└─────────────────────────────────────────┘
```

### Example — Course Assignment Feature

```
Persona 1: Training Manager (PRIMARY)
  Context: Assigns mandatory training to teams each quarter
  Motivation: Ensure compliance, track completion
  Tech Comfort: Medium
  Frequency: Weekly

Persona 2: Learner (AFFECTED)
  Context: Receives course assignments, completes coursework
  Motivation: Stay compliant, learn new skills
  Tech Comfort: Low to Medium
  Frequency: Daily during training periods

Persona 3: HR Director (RESULT VIEWER)
  Context: Reviews completion reports for compliance audits
  Motivation: Prove organization-wide compliance
  Tech Comfort: Low
  Frequency: Monthly / Quarterly

Persona 4: System (AUTOMATED)
  Context: Sends reminders, tracks deadlines, generates reports
  Motivation: N/A — executes business rules
  Frequency: Continuous
```

---

## Step 2 — Goal Mapping

### Map Persona Goals to Feature Capabilities

| Persona | Goal | Feature Capability | Priority |
|---------|------|--------------------|----------|
| Training Manager | Assign courses to teams quickly | Bulk assignment with team/group selection | P0 |
| Training Manager | Track who completed assignments | Assignment status dashboard | P0 |
| Training Manager | Set deadlines with reminders | Due date with automated email reminders | P0 |
| Learner | Know what I need to complete | My Assignments page with due dates | P0 |
| Learner | Complete assignments on my schedule | Self-paced course access | P1 |
| HR Director | Prove compliance in audits | Exportable completion report | P1 |
| System | Remind learners of approaching deadlines | Automated reminder emails at 7d, 3d, 1d | P0 |

### Goal Hierarchy

```
                 ┌──────────────────────────┐
                 │  BUSINESS GOAL           │
                 │  Ensure 95% compliance   │
                 │  training completion     │
                 └────────┬─────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
   ┌──────▼─────┐  ┌─────▼──────┐  ┌────▼───────┐
   │ User Goal  │  │ User Goal  │  │ User Goal  │
   │ Assign     │  │ Complete   │  │ Report on  │
   │ training   │  │ training   │  │ completion │
   └──────┬─────┘  └─────┬──────┘  └────┬───────┘
          │               │               │
   ┌──────▼─────┐  ┌─────▼──────┐  ┌────▼───────┐
   │ Stories    │  │ Stories    │  │ Stories    │
   │ US-01..03  │  │ US-04..06  │  │ US-07..09  │
   └────────────┘  └────────────┘  └────────────┘
```

---

## Step 3 — Write User Stories

### Story Format

```
┌──────────────────────────────────────────────────────────────┐
│  USER STORY FORMAT                                           │
│                                                              │
│  ID:       US-[area]-[number]                                │
│  Title:    [Short action-oriented title]                     │
│  Priority: P0 / P1 / P2                                     │
│  Points:   [Estimate — 1, 2, 3, 5, 8, 13]                   │
│                                                              │
│  As a [persona],                                             │
│  I want to [action/capability],                              │
│  so that [benefit/value].                                    │
│                                                              │
│  Acceptance Criteria:                                        │
│  (Given/When/Then format — see Step 4)                       │
│                                                              │
│  Edge Cases:                                                 │
│  (Unusual scenarios — see Step 4)                            │
│                                                              │
│  Technical Notes:                                            │
│  (API endpoints, data model changes, existing patterns)      │
│                                                              │
│  Dependencies:                                               │
│  (Other stories this requires — see Step 5)                  │
│                                                              │
│  Design Notes:                                               │
│  (UI mockup reference, component reuse, responsive behavior) │
└──────────────────────────────────────────────────────────────┘
```

### Example Stories — Course Assignment Feature

**US-ASSIGN-01: Assign a course to individual users**

```
As a Training Manager,
I want to assign a course to one or more users,
so that they receive the training I need them to complete.

Priority: P0
Points: 5

Acceptance Criteria:

  AC1: Given I am on the course detail page,
       when I click "Assign Users",
       then a dialog opens with a searchable list of users in my organization.

  AC2: Given the assignment dialog is open,
       when I search for "Sarah",
       then only users whose name or email contains "Sarah" appear.

  AC3: Given I have selected 3 users and set a due date of April 15,
       when I click "Assign",
       then all 3 users are enrolled in the course with April 15 as their due date.

  AC4: Given an assignment is created,
       when the system processes it,
       then each assigned user receives an email notification within 5 minutes.

  AC5: Given a user is already enrolled in the course,
       when I try to assign them again,
       then they appear as disabled with the label "Already enrolled".

Edge Cases:
  - User assigns a course to 500+ users at once (bulk limit: 500 per batch)
  - Due date is set to today (allow it — assignment is still valid)
  - Due date is in the past (block with validation error)
  - User being assigned has a deactivated account (skip and show warning)
  - Course is in draft status (block assignment — course must be published)

Technical Notes:
  - Use existing AssignmentDialog component
  - POST /api/courses/:id/enrollments (batch endpoint)
  - Emails via existing notification service queue
  - Check enrollment status before creating to avoid duplicates

Dependencies:
  - Course must be published (existing feature)
  - User list API must support search (existing)
```

**US-ASSIGN-02: Set assignment due dates**

```
As a Training Manager,
I want to set a due date when assigning a course,
so that learners know their deadline and I can track overdue assignments.

Priority: P0
Points: 3

Acceptance Criteria:

  AC1: Given I am assigning users to a course,
       when I set a due date,
       then the date picker only allows dates today or in the future.

  AC2: Given a due date is set,
       when the assignment is created,
       then the due date is stored and visible on the learner's dashboard.

  AC3: Given no due date is set,
       when the assignment is created,
       then the assignment has no deadline and shows "No due date" on the dashboard.

Edge Cases:
  - Due date is a weekend or holiday (allow it — business rules vary)
  - Manager changes due date after assignment (covered in US-ASSIGN-05)
  - Different time zones — due date is end of day in the organization's timezone
  - Due date is more than 1 year away (allow with warning: "This is over a year away")

Technical Notes:
  - Store due date as UTC datetime
  - Display in user's local timezone
  - Add dueDate field to enrollment model
```

### Anti-Patterns — Bad User Stories

| Bad Story | Why It Fails | Better Version |
|-----------|--------------|----------------|
| "As a user, I want a dashboard" | No specific goal or value | "As a manager, I want to see my team's training progress, so I can identify who needs help before deadlines" |
| "As a user, I want the system to be fast" | Not a story — it's an NFR | Move to non-functional requirements: "API responses < 500ms P95" |
| "As a user, I want to do everything with courses" | Too broad — not estimable | Split into: create, edit, publish, archive, delete |
| "As admin, I want admin features" | No specific capability | "As an admin, I want to deactivate a user account, so that former employees cannot access training materials" |
| "Implement the enrollment table" | Developer task, not user story | "As a learner, I want to see my course enrollments, so that I know what training I need to complete" |

---

## Step 4 — Acceptance Criteria & Edge Cases

### Given/When/Then Format

```
┌──────────────────────────────────────────────────────────────┐
│  ACCEPTANCE CRITERIA FORMAT                                  │
│                                                              │
│  Given [precondition — the state of the world],              │
│  when  [action — what the user does],                        │
│  then  [expected result — what should happen].               │
│                                                              │
│  Rules:                                                      │
│  - "Given" sets up context (logged in, on a page, has data)  │
│  - "When" is a single user action (click, submit, navigate)  │
│  - "Then" is observable and verifiable (UI change, email,    │
│    data change, error message)                               │
│  - Each AC tests ONE behavior                                │
│  - Use concrete values ("3 users", "$49.99", "April 15")     │
│  - Never use "should" — use "then [X] happens"              │
└──────────────────────────────────────────────────────────────┘
```

### Edge Case Categories

Always check these categories when writing edge cases:

```
┌─────────────────────────────────────────────────────────────┐
│  EDGE CASE CHECKLIST                                        │
│                                                             │
│  DATA STATES                                                │
│  [ ] Empty state — no data exists yet                       │
│  [ ] Single item — only one record                          │
│  [ ] Maximum items — hitting limits (100, 1000, etc.)       │
│  [ ] Invalid data — special characters, long strings        │
│  [ ] Missing data — required fields left blank              │
│                                                             │
│  USER STATES                                                │
│  [ ] First-time user — no history, no preferences           │
│  [ ] Power user — thousands of records                      │
│  [ ] Wrong role — unauthorized access attempt               │
│  [ ] Deactivated account — user no longer active            │
│  [ ] Multiple sessions — same user on two devices           │
│                                                             │
│  SYSTEM STATES                                              │
│  [ ] Network failure — request times out                    │
│  [ ] Concurrent edit — two users modify same record         │
│  [ ] Partial failure — 3 of 5 batch operations succeed      │
│  [ ] Rate limiting — too many requests                      │
│  [ ] Background job fails — scheduled task errors           │
│                                                             │
│  TIME STATES                                                │
│  [ ] Timezone differences — user in different timezone      │
│  [ ] Daylight saving time — clock change edge               │
│  [ ] Expiration — token, link, or deadline expires          │
│  [ ] Past dates — attempting to use expired dates           │
│  [ ] Future dates — far-future dates (year 2030)            │
│                                                             │
│  DISPLAY STATES                                             │
│  [ ] Long text — name or description exceeds display width  │
│  [ ] Unicode — emojis, RTL text, special characters         │
│  [ ] Mobile — responsive layout changes                     │
│  [ ] Accessibility — screen reader compatibility            │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 5 — Dependencies & Story Map

### Dependency Mapping

```
┌────────────┐     depends on     ┌────────────┐
│ US-ASSIGN  │────────────────────│ US-COURSE  │
│   -04      │                    │   -01      │
│ Track      │                    │ Publish    │
│ Progress   │                    │ Course     │
└────────────┘                    └────────────┘
      │
      │ depends on
      ▼
┌────────────┐     depends on     ┌────────────┐
│ US-ASSIGN  │────────────────────│ US-ASSIGN  │
│   -06      │                    │   -01      │
│ Overdue    │                    │ Create     │
│ Report     │                    │ Assignment │
└────────────┘                    └────────────┘
```

### Story Map Layout

Organize stories horizontally by user activity, vertically by priority:

```
┌─────────────────────────────────────────────────────────────────┐
│                        STORY MAP                                │
│                                                                 │
│  ACTIVITIES  │ Assign Training │ Complete Training │ Report     │
│  ────────────┼─────────────────┼───────────────────┼──────────  │
│              │                 │                   │            │
│  MUST HAVE   │ Assign to users │ View my courses   │ Completion │
│  (Sprint 1)  │ Set due dates   │ Mark complete     │   report   │
│              │ Email notify    │ Resume progress   │            │
│              │                 │                   │            │
│  ────────────┼─────────────────┼───────────────────┼──────────  │
│              │                 │                   │            │
│  SHOULD HAVE │ Assign to groups│ Certificate       │ Overdue    │
│  (Sprint 2)  │ Bulk reassign   │ Course rating     │   report   │
│              │ Change due date │                   │ Export CSV │
│              │                 │                   │            │
│  ────────────┼─────────────────┼───────────────────┼──────────  │
│              │                 │                   │            │
│  NICE TO     │ Auto-assign on  │ Bookmarks         │ Scheduled  │
│  HAVE        │   role change   │ Learning path     │   email    │
│  (Sprint 3+) │ Assignment rules│   suggestions     │   digest   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step 6 — Story Splitting Techniques

### When to Split a Story

```
┌────────────────────────────────────────────────────┐
│  SPLIT WHEN:                                       │
│                                                    │
│  ❌ Estimated at 13+ points                        │
│  ❌ Has more than 8 acceptance criteria             │
│  ❌ Touches more than 3 system areas               │
│  ❌ Cannot be completed in one sprint               │
│  ❌ Contains the word "and" in the goal             │
│  ❌ Multiple personas have different needs          │
└────────────────────────────────────────────────────┘
```

### Splitting Techniques

| Technique | When to Use | Example |
|-----------|-------------|---------|
| **By workflow step** | Story covers a multi-step process | "Create & Assign & Notify" becomes 3 stories |
| **By user role** | Different roles need different experiences | "Admin creates" vs "User views" vs "Manager approves" |
| **By data variation** | Different input types need different handling | "Upload CSV" vs "Upload Excel" vs "Manual entry" |
| **By happy path vs edge case** | Core flow works but edge cases are complex | "Basic assignment" vs "Handle deactivated users" |
| **By CRUD operation** | Story covers all operations | "Create course" / "Edit course" / "Delete course" |
| **By platform** | Different platforms need different work | "Desktop layout" vs "Mobile responsive" |
| **By integration** | Multiple external systems involved | "Stripe payment" vs "Invoice generation" vs "Email receipt" |
| **Spike + Implementation** | Uncertainty about approach | "Research SSO options (spike)" then "Implement SAML SSO" |

### Splitting Example

**Before (too large — 13 points):**
```
As a Training Manager,
I want to manage course assignments including creating, editing,
tracking, and reporting on assignments,
so that I can ensure my team completes required training.
```

**After (split into 5 stories):**
```
US-01 (3 pts): Assign course to individual users
US-02 (2 pts): Set and modify due dates on assignments
US-03 (3 pts): View assignment status dashboard
US-04 (2 pts): Send reminder emails for approaching deadlines
US-05 (3 pts): Export assignment completion report
```

---

## Complete Story Output Template

When generating stories, output them in this format for easy import into project management tools:

```markdown
## User Stories — [Feature Name]

Generated: [Date]
Total Stories: [N]
Total Points: [N]

### Sprint 1 — Must Have (P0)

---

#### US-[AREA]-01: [Title]

**Priority:** P0 | **Points:** [N] | **Sprint:** 1

As a [persona],
I want to [action],
so that [value].

**Acceptance Criteria:**

- AC1: Given [context], when [action], then [result].
- AC2: Given [context], when [action], then [result].
- AC3: Given [context], when [action], then [result].

**Edge Cases:**
- [Edge case 1]
- [Edge case 2]

**Technical Notes:**
- [Note about implementation approach]
- [Existing patterns to follow]

**Dependencies:** None | US-[XX]-[NN]

**Design Notes:**
- [UI component to use]
- [Responsive behavior]

---

#### US-[AREA]-02: [Title]
...
```

---

## Completeness Checklist

```
STORY QUALITY CHECKLIST
───────────────────────
[ ] Every story follows "As a / I want to / So that" format
[ ] Every story has a clear, unique persona (not "as a user")
[ ] Every story has at least 3 acceptance criteria
[ ] All acceptance criteria use Given/When/Then format
[ ] Every story has at least 2 edge cases documented
[ ] No story exceeds 8 story points (split if larger)
[ ] Dependencies between stories are explicitly listed
[ ] Technical notes reference existing patterns and components
[ ] Stories are grouped by sprint and priority
[ ] Story map covers all user activities (assign, complete, report)
[ ] Empty states are covered (first-time user, no data)
[ ] Error states are covered (network failure, invalid input)
[ ] Permission checks are covered (unauthorized access)
[ ] No "and" in the goal statement (split if present)
[ ] Each story delivers standalone value to the user
```

---

## Common Mistakes

| Mistake | Impact | Prevention |
|---------|--------|------------|
| "As a user" instead of specific persona | Story lacks context, devs guess at behavior | Always use a named role: "As a Training Manager" |
| No acceptance criteria | Dev and QA interpret story differently | Write AC before pointing the story |
| Acceptance criteria without Given/When/Then | Criteria are vague and untestable | Enforce the format — no exceptions |
| Skipping edge cases | Bugs found in production instead of development | Use the edge case checklist for every story |
| Stories too large | Cannot complete in one sprint, hard to estimate | Apply splitting techniques — max 8 points |
| Missing dependencies | Work blocked during sprint | Map dependencies during grooming |
| Writing implementation tasks as stories | No user value delivered | Always start from user benefit, not system change |
| Forgetting the "so that" clause | Team doesn't understand why it matters | "So that" reveals the value — never skip it |

---

## Tips for Sprint Planning

1. **Read the story aloud** — If it sounds awkward, rewrite it. Natural language = clear intent
2. **Three Amigos before sprint** — PM, Dev, QA review each story together for 5 minutes
3. **Acceptance criteria are the contract** — If it's not in the AC, it's not in scope
4. **Point the story, not the developer** — Estimate complexity, not who's working on it
5. **Spikes are time-boxed** — "Research X" stories have a fixed time limit (e.g., 4 hours), not a deliverable
6. **One story per PR** — Keep pull requests focused on a single story for easier review
7. **Demo against acceptance criteria** — In sprint review, show each AC passing, not just a feature walkthrough

<!--
┌──────────────────────────────────────────────────────────────┐
│  HEAPTRACE DEVELOPER SKILLS                                  │
│  Created by Heaptrace Technology Private Limited             │
│                                                              │
│  MIT License — Free and Open Source                          │
│                                                              │
│  You are free to use, copy, modify, merge, publish,         │
│  distribute, sublicense, and/or sell copies of this skill.   │
│  No restrictions. No attribution required.                   │
│                                                              │
│  heaptrace.com | github.com/heaptracetechnology              │
└──────────────────────────────────────────────────────────────┘
-->
