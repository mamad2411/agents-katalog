---
name: project-tracker
description: "Creates a project management database in Notion with tasks, statuses, owners, due dates, and priorities, pre-populated from a project brief or scope document. Use when a user needs to set up project tracking for a new engagement, wants to replace spreadsheet-based task management, or needs a lightweight PM system without paid software."
allowed-tools: Read Write Glob mcp__claude_ai_Notion__notion-create-database mcp__claude_ai_Notion__notion-create-pages mcp__claude_ai_Notion__notion-search mcp__claude_ai_Notion__notion-fetch
metadata:
  author: Salah-XD
  version: "1.0"
---

# Project Tracker

## When to Use This Skill

Use this skill when you need to:
- Create a project task database in Notion from a project brief, scope document, or verbal description
- Replace a spreadsheet, whiteboard, or sticky-note system for tracking project tasks
- Set up task tracking for a new client engagement, product launch, or internal initiative
- Build a lightweight project management system without paying for Asana, Monday, or ClickUp
- Pre-populate a task board with phases, owners, due dates, and priorities from a project plan

**DO NOT** use this skill for:
- Client or contact relationship tracking (use a client-crm skill instead)
- Kanban-only boards with no task metadata (just use a plain Notion board)
- Enterprise portfolio management across dozens of projects (too complex for a single database)
- Time tracking or invoicing (different schema and tooling needed)
- Recurring task management or habit tracking (this is for finite project scopes)

---

## Quick Reference: Project Tracker Features

| Feature | Details |
|---------|---------|
| Properties | 9 fields per task record |
| Status stages | 5 (Not Started through Blocked) |
| Priority levels | 4 (Urgent, High, Medium, Low) |
| Database views | 5 pre-built filtered views |
| Seeding | Bulk import from project brief, scope doc, or task list |
| Usage guide | Common operations documented for the user |

## Quick Reference: Database Schema

| Property | Type | Purpose | Default/Options |
|----------|------|---------|-----------------|
| Task Name | Title | Short, action-oriented task description | Required |
| Status | Select | Current state of the task | Not Started |
| Priority | Select | Urgency and importance level | Medium |
| Owner | Rich text | Person responsible for the task | Empty |
| Due Date | Date | Deadline for task completion | Empty |
| Project Phase | Select | Which phase of the project this task belongs to | See options below |
| Description | Rich text | Detailed requirements, acceptance criteria, or notes | Empty |
| Dependencies | Rich text | Other tasks that must complete before this one can start | Empty |
| Tags | Multi-select | Categories for filtering and grouping | See options below |

### Status Options

```
Not Started --> In Progress --> In Review --> Complete --> Blocked
```

| Status | Meaning | Action Required |
|--------|---------|-----------------|
| Not Started | Task is defined but work has not begun | Assign owner and due date if missing |
| In Progress | Actively being worked on | Owner updates Description with progress notes |
| In Review | Work is done, awaiting approval or feedback | Reviewer provides feedback within 2 business days |
| Complete | Task is finished and approved | No further action needed |
| Blocked | Cannot proceed due to a dependency or issue | Log the blocker in Description, escalate to project lead |

### Priority Options

| Priority | Color | When to Use |
|----------|-------|-------------|
| Urgent | Red | Blocks other tasks or has a deadline within 48 hours |
| High | Orange | Critical path item, needed this week |
| Medium | Yellow | Standard task, due within the current phase |
| Low | Gray | Nice-to-have, can slip without impacting the project |

### Default Project Phase Options

Phases are customized per project. If the user does not specify phases, use these defaults:

| Phase | Purpose |
|-------|---------|
| Planning | Research, requirements gathering, scoping |
| Design | Wireframes, mockups, architecture, strategy |
| Build | Development, writing, creation, production |
| Review | Testing, QA, feedback, revisions |
| Launch | Deployment, go-live, publishing, delivery |

### Default Tag Options

`milestone`, `client-facing`, `internal`, `content`, `design`, `development`, `admin`, `research`, `meeting`, `deliverable`

---

## Core Workflow

EVERY PROJECT TRACKER STARTS BY GATHERING THE PROJECT DETAILS AND CREATING THE DATABASE WITH THE FULL SCHEMA BEFORE ADDING ANY TASKS -- NEVER ADD PAGES TO A DATABASE THAT IS MISSING PROPERTIES.

### Phase 1: Gather Project Details

Collect these details from the user before building anything:

1. **Project name** -- what is this project called
2. **Notion parent page** -- where should the tracker database live (page name or URL)
3. **Project phases** -- custom phase names, or accept the 5 defaults (Planning, Design, Build, Review, Launch)
4. **Team members** -- list of people who will own tasks (names only; these go in the Owner field)
5. **Timeline** -- overall start date, end date, or phase-level deadlines
6. **Project brief or task list** -- a scope document, brief, bullet list, or verbal description of what needs to get done

If the user provides only items 1 and 2, proceed with all defaults and generate tasks from context. Ask only about missing critical details.

**Brief template for vague requests:**

```
I'll build your project tracker in Notion. Quick answers needed:

1. What is the project name?
2. Which Notion page should I create the tracker under?
3. What are the project phases? (default: Planning, Design, Build, Review, Launch)
4. Who are the team members? (names for task ownership)
5. What is the timeline? (start date, end date, or key deadlines)
6. Do you have a project brief, scope doc, or task list I should use to pre-populate tasks?
```

### Phase 2: Create the Database in Notion

1. Call `notion-search` with the page name or keywords the user provided to locate the parent page
2. Confirm the parent page with the user if multiple matches exist
3. Call `notion-create-database` with the parent page ID and full schema:

**Database title:** `[Project Name] Tracker`

**Properties to create:**

```
Task Name      -> title
Status         -> select
  options: Not Started, In Progress, In Review, Complete, Blocked
  colors:  gray, blue, purple, green, red
Priority       -> select
  options: Urgent, High, Medium, Low
  colors:  red, orange, yellow, gray
Owner          -> rich_text
Due Date       -> date
Project Phase  -> select
  options: [user's custom phases OR defaults: Planning, Design, Build, Review, Launch]
  colors:  blue, purple, orange, green, pink
Description    -> rich_text
Dependencies   -> rich_text
Tags           -> multi_select
  options: milestone, client-facing, internal, content, design, development,
           admin, research, meeting, deliverable
  colors:  red, blue, gray, pink, purple, green, brown, yellow, orange, default
```

4. Verify the database was created by calling `notion-fetch` with the returned database ID

5. Confirm creation to the user:

```
Project tracker created: "[Project Name] Tracker"
Database ID: db_xyz789

Properties configured:
  - Task Name (title)
  - Status (5 stages: Not Started > In Progress > In Review > Complete > Blocked)
  - Priority (4 levels: Urgent, High, Medium, Low)
  - Owner (text)
  - Due Date (date)
  - Project Phase ([number] phases)
  - Description (rich text)
  - Dependencies (rich text)
  - Tags (10 default tags)
```

**IF THE PARENT PAGE IS NOT FOUND:**
- Ask the user for the exact page title or a URL
- Try `notion-search` again with the corrected term
- If still not found, ask the user to share the page with the Notion integration
- **After 3 failed searches, stop and explain:** "I cannot find that page. Please verify the page exists and that the Notion integration has access to it. Check Settings > Connections in Notion."

**IF DATABASE CREATION FAILS:**
- Check the error message for permission issues
- Verify the parent page ID by calling `notion-fetch` on it
- Retry once with the same parameters
- **If it fails again:** "Database creation failed. This usually means the Notion integration does not have permission to create content on that page. Go to the parent page in Notion, click the three-dot menu, go to Connections, and ensure the integration has 'Can edit' access."

### Phase 3: Pre-Populate Tasks from Project Brief

1. Parse the user's project brief, scope document, or task list into discrete tasks
2. For each task, map the data to the schema:
   - **Task Name** -- short, action-oriented (start with a verb: "Design homepage wireframe", "Write onboarding email sequence")
   - **Status** -- default to "Not Started" for all new tasks
   - **Priority** -- infer from context; milestone items and deadline-sensitive tasks get "High" or "Urgent"; default to "Medium"
   - **Owner** -- assign based on user instructions or skill/role matching; leave empty if no team info provided
   - **Due Date** -- calculate from timeline if provided; distribute tasks across phases evenly if only start/end dates given
   - **Project Phase** -- assign based on task nature and project flow
   - **Description** -- extract relevant details, acceptance criteria, or specifications from the brief
   - **Dependencies** -- note if a task explicitly depends on another task (e.g., "Design must complete before Build begins")
   - **Tags** -- infer from task content (e.g., client deliverable = `client-facing` + `deliverable`, research task = `research`)

3. Call `notion-create-pages` to add all tasks to the database

4. Report seeding results:

```
Tasks imported: 20 of 20 successful

  PLANNING (4 tasks):
    Define project requirements          — Medium, Sarah, Due: Mar 10
    Audit existing website analytics     — High, Marcus, Due: Mar 12
    Stakeholder kickoff meeting          — Urgent, Sarah, Due: Mar 7
    Compile brand asset inventory        — Low, Unassigned, Due: Mar 14

  DESIGN (5 tasks): [listed with owner, priority, due date]
  BUILD (7 tasks): [listed with owner, priority, due date]
  REVIEW (2 tasks): [listed with owner, priority, due date]
  LAUNCH (2 tasks): [listed with owner, priority, due date]

Total: 20 tasks | Assigned: 16 | Unassigned: 4 | Milestones: 3
```

**IF THE BRIEF IS VAGUE OR INCOMPLETE:**
- Generate reasonable tasks based on the project type and phases
- Present the generated task list to the user for approval BEFORE creating pages:
  ```
  I generated 18 tasks from your brief. Here is the breakdown by phase:

  PLANNING (3 tasks):
    1. Define target audience and goals — Medium
    2. Audit competitor websites — Medium
    3. Gather brand assets and copy — High

  Want me to proceed, or would you like to add, remove, or modify any tasks?
  ```
- **NEVER create tasks without confirmation when the data is inferred rather than explicit**

**IF BATCH CREATION PARTIALLY FAILS:**
- Report which tasks succeeded and which failed
- Retry each failed task individually with `notion-create-pages`
- If individual retries fail, provide the task details formatted for manual entry

### Phase 4: Set Up Views and Confirm

After the database and tasks are in place, guide the user on setting up filtered views. **Notion MCP does not support creating views programmatically**, so provide exact instructions.

Present these 5 views for the user to create manually:

```
RECOMMENDED VIEWS (create these in Notion):

1. ALL TASKS (Table view)
   - View type: Table
   - Sort: Due Date (ascending)
   - No filter
   - Purpose: Full task list ordered by deadline

2. MY TASKS (Table view)
   - View type: Table
   - Filter: Owner contains [your name]
   - Sort: Due Date (ascending), then Priority (Urgent first)
   - Purpose: Personal task list for each team member

3. THIS WEEK (Table view)
   - View type: Table
   - Filter: Due Date is within the next 7 days AND Status is not "Complete"
   - Sort: Priority (Urgent first), then Due Date (ascending)
   - Purpose: Weekly sprint view showing what needs attention now

4. BY PHASE (Board view)
   - View type: Board
   - Group by: Project Phase
   - Filter: Status is not "Complete"
   - Sort: Priority (Urgent first)
   - Purpose: See active tasks organized by project phase

5. BLOCKED ITEMS (Table view)
   - View type: Table
   - Filter: Status is "Blocked"
   - Sort: Priority (Urgent first)
   - Purpose: Escalation list — resolve blockers before they cascade
```

Deliver a final summary including: database name and ID, task count by phase with date ranges, assigned vs. unassigned count, milestone count, and 3-4 concrete next steps (create views, assign unassigned tasks, review weekly, check blocked items daily).

---

## Example 1: Website Redesign Project

**User request:** "We are redesigning our company website. 4 phases: Discovery, Design, Development, QA/Launch. Team is Sarah (PM), Marcus (designer), Priya (developer), and James (copywriter). Timeline is March 3 to April 25. My Notion page is called 'Active Projects'. Here is our scope..."

**Execution:**

1. **Gather:** Project name "Website Redesign", parent page "Active Projects", 4 custom phases, 4 team members, 8-week timeline, scope document provided
2. **Search:** `notion-search` for "Active Projects" -> found `pg_active456`, confirmed
3. **Create:** `notion-create-database` with parent `pg_active456`, title "Website Redesign Tracker", custom phases (Discovery, Design, Development, QA/Launch) -> `db_redesign789`
4. **Seed 20 tasks:**

```
DISCOVERY (5 tasks, Mar 3-10):
  Stakeholder kickoff meeting            — Urgent, Sarah, milestone
  Audit current site analytics           — High, Marcus
  Competitor analysis (5 sites)          — Medium, James
  Define sitemap and page hierarchy      — High, Sarah
  Compile brand guidelines and assets    — Medium, James

DESIGN (6 tasks, Mar 14-24):
  Create wireframes for 8 key pages     — High, Marcus
  Design homepage mockup                — Urgent, Marcus, milestone
  Design inner page templates           — High, Marcus
  Write homepage copy                   — High, James
  Write service page copy (4 pages)     — Medium, James
  Client design review and approval     — High, Sarah, client-facing

DEVELOPMENT (6 tasks, Mar 25 - Apr 7):
  Set up staging environment            — High, Priya
  Build homepage                        — Urgent, Priya
  Build inner page templates            — High, Priya
  Integrate contact form and CRM        — Medium, Priya
  Mobile responsive QA pass             — High, Priya
  Content migration (blog posts)        — Medium, James

QA/LAUNCH (3 tasks, Apr 11-25):
  Full QA testing across browsers       — High, Priya
  Client UAT and final approval         — Urgent, Sarah, milestone, client-facing
  DNS switch and go-live                — Urgent, Priya, milestone

Total: 20 tasks | Assigned: 20 | Milestones: 4 | Client-facing: 2
```

5. **Deliver:** View instructions + final summary with phase breakdown and next steps

---

## Example 2: Product Launch Project

**User request:** "I am launching a new online course in 6 weeks. Phases are Pre-Launch, Launch Week, and Post-Launch. It is just me doing everything. My Notion workspace has a page called 'Course Business'. I have a rough outline of what needs to happen."

**Execution:**

1. **Gather:** Project name "Online Course Launch", parent page "Course Business", 3 custom phases, solo operator, 6-week timeline, rough outline provided
2. **Search:** `notion-search` for "Course Business" -> found `pg_course321`, confirmed
3. **Create:** `notion-create-database` with parent `pg_course321`, title "Online Course Launch Tracker", custom phases (Pre-Launch, Launch Week, Post-Launch) -> `db_launch654`
4. **Seed 15 tasks:**

```
PRE-LAUNCH (9 tasks, Week 1-4):
  Finalize course curriculum outline       — Urgent, You, milestone
  Record video lessons (8 modules)         — High, You
  Edit and upload videos to platform       — High, You
  Write sales page copy                    — High, You, client-facing
  Design course thumbnail and graphics     — Medium, You, design
  Set up payment and checkout flow         — High, You
  Build email waitlist sequence (5 emails) — High, You, content
  Create 3 social media teaser posts       — Medium, You, content
  Set up affiliate tracking links          — Low, You

LAUNCH WEEK (4 tasks, Week 5):
  Send launch email to waitlist            — Urgent, You, milestone
  Publish sales page and open cart         — Urgent, You, milestone
  Post daily social media content (5 days) — High, You, content
  Run live Q&A or webinar                  — High, You, client-facing

POST-LAUNCH (2 tasks, Week 6):
  Send follow-up email to non-buyers       — Medium, You, content
  Collect testimonials from first students  — High, You, milestone, client-facing

Total: 15 tasks | Assigned: 15 | Milestones: 4 | Content: 4
```

5. **Deliver:** View instructions (with solopreneur tip: skip "My Tasks" view, use "All Tasks" and "This Week" instead) + final summary with phase breakdown and milestone checkpoints

---

## Pre-Delivery Checklist

Run this checklist before delivering the tracker to the user. **DO NOT SKIP ANY ITEM.**

| Check | What to Verify | How |
|-------|----------------|-----|
| Database exists | Database was created and is accessible | Call `notion-fetch` with database ID |
| All 9 properties present | Every property from the schema is configured | Verify in the `notion-fetch` response |
| Status options correct | All 5 statuses exist as select options | Check select options in database schema |
| Priority options correct | All 4 priorities exist as select options | Check select options in database schema |
| Project phases correct | All custom or default phases exist as select options | Check select options in database schema |
| Tags configured | All 10 default tags (or custom set) exist as multi-select options | Check multi-select options in database schema |
| Due Date configured | Due Date is a date type property | Verify property type in schema |
| Tasks seeded | All tasks were created successfully | Count created pages vs. expected |
| No duplicate tasks | Same task was not added twice during seeding | Check for duplicate task names |
| Owners assigned | Tasks have owners where team info was provided | Verify Owner field on seeded pages |
| Due dates set | Tasks have due dates where timeline was provided | Verify Date values on seeded pages |
| Milestones tagged | Key deliverables are tagged with "milestone" | Verify Tags on milestone tasks |
| View instructions delivered | User received setup instructions for all 5 views | Confirm in delivery message |
| Parent page correct | Database lives under the page the user requested | Verify parent in `notion-fetch` response |

```
Pre-Delivery Checklist:
  [x] Database created and accessible
  [x] All 9 properties configured
  [x] Status options correct (5 stages)
  [x] Priority options correct (4 levels)
  [x] Project phases correct (custom or default)
  [x] Tags configured (10 default or custom)
  [x] Due Date property configured
  [x] All tasks seeded successfully
  [x] No duplicate tasks
  [x] Owners assigned where applicable
  [x] Due dates set from timeline
  [x] Milestones tagged
  [x] View setup instructions delivered
  [x] Database under correct parent page
```

---

## Recovery and Troubleshooting

### Notion Search Returns No Results

If `notion-search` cannot find the target parent page:

1. Ask the user for the exact page title (case-sensitive)
2. Try searching with a shorter keyword (e.g., "Projects" instead of "Active Projects Dashboard")
3. Ask the user to confirm the page exists and is not in a private section
4. **If 3 searches fail:** "I cannot locate that page. Please verify the page title and ensure the Notion integration has access. Check Settings > Connections in Notion, find the integration, and confirm the page is shared with it."

### Database Creation Fails

If `notion-create-database` returns an error:

1. Verify the parent page ID by calling `notion-fetch` on it
2. Check for permission errors in the response -- the integration may lack write access
3. Retry once with the same parameters
4. **If it fails again:** "Database creation failed due to a permissions issue. Please go to the parent page in Notion, click the three-dot menu, go to Connections, and ensure the integration has 'Can edit' access."

### Task Seeding Partially Fails

If some tasks fail to create:

1. Report which tasks succeeded and which failed
2. Retry each failed task individually with `notion-create-pages`
3. If individual retries fail, check if a required property is missing or malformed
4. **If retries continue to fail:** Provide the task details formatted for manual entry:
   ```
   Could not import these tasks automatically:

     Set up staging environment — High, Priya, Due: Mar 25

   To add manually: open the tracker database in Notion, click "+ New",
   and enter the details above.
   ```

### Notion API Rate Limits

If you receive rate limit errors during bulk seeding:

1. Pause for 10 seconds between batches
2. Reduce batch size to 5 tasks per `notion-create-pages` call
3. Continue until all tasks are imported
4. **DO NOT skip tasks due to rate limits** -- slow down and retry

### User Wants to Modify the Schema Later

**Notion MCP does not support modifying existing database schemas.** Instruct the user:
- To add a property: open the tracker, click "+" in the header row, choose type, name it
- To modify a property: click the column header, select "Edit property", change type/name/options

### User Wants to Add More Tasks Later

1. Call `notion-fetch` to confirm the database ID and schema
2. Parse the new tasks following the same mapping rules in Phase 3
3. Call `notion-create-pages` to add the new tasks
4. Report the additions and updated totals

### Duplicate Detection

Flag potential duplicates before creating pages (e.g., "Write homepage copy" and "Draft homepage content" -- same task?). Present them to the user for confirmation. **NEVER create duplicate task records** -- always confirm first.

---

## Anti-Patterns

- **DO NOT** create the database without the full property schema -- adding properties after pages exist causes data alignment issues
- **DO NOT** invent task details not present in the brief -- if the brief is vague, present generated tasks for approval first
- **DO NOT** skip the parent page confirmation -- creating a tracker under the wrong page is difficult to undo
- **DO NOT** assign owners that the user did not mention -- leave the Owner field empty for unassigned tasks
- **DO NOT** deliver without the view setup instructions -- the tracker is only valuable when the user can filter and sort tasks
- **DO NOT** set all tasks to "Urgent" or "High" -- a project where everything is urgent has no prioritization at all
- **DO NOT** create views programmatically -- Notion MCP does not support this; provide manual instructions instead
- **DO NOT** promise automated reminders, notifications, or status updates -- this is a database, not a project management app with automations
