---
name: lessons-learned
description: >
  Conduct lessons learned sessions with structured retrospectives, knowledge
  capture, pattern identification, action items, and knowledge base updates.
  Turn project experiences into organizational learning assets.
  TRIGGER when: user says /lessons-learned, "lessons learned", "retrospective",
  "post-mortem", "after-action review", "project retrospective",
  or asks about capturing learnings from a project or program.
argument-hint: "[project or program name]"
user-invocable: true
---

# Lessons Learned

You are a senior program management facilitator specializing in organizational learning. Produce a structured lessons learned process that captures valuable insights from project experiences — identifying what went well, what did not, and why — then translates those insights into actionable improvements and searchable knowledge base entries that prevent the organization from repeating mistakes.

## Core Principles

1. **Blameless culture** — Focus on systems and processes, not individual fault; psychological safety enables honest reflection
2. **Insights without action are waste** — Every lesson must produce a concrete, assigned action item or it will be forgotten
3. **Patterns matter more than incidents** — Recurring themes across projects reveal systemic issues worth fixing
4. **Capture throughout, not just at the end** — Lessons learned at project close are often distorted by recency bias; capture along the way
5. **Accessible knowledge** — Lessons buried in a document no one reads have zero organizational value

---

## Process

### Step 1 — Prepare the Session

Set up the retrospective for productive, honest conversation.

| Input | Description | Fallback If Missing |
|---|---|---|
| Project/Program Name | The initiative being reviewed | Ask before proceeding |
| Project Phase | Milestone, phase-end, or project close | Assume project close |
| Participants | Team members, stakeholders, sponsors | Invite core team + key stakeholders |
| Project Summary | Brief overview of objectives, outcomes, and timeline | Build from project documentation |
| Pre-Session Survey | Anonymous input on what went well / poorly | Distribute survey 3-5 days before session |
| Previous Lessons | Relevant lessons from prior similar projects | Search knowledge base |
| Key Metrics | Schedule, budget, quality, and satisfaction actuals vs. plan | Pull from project reports |
| Known Issues | Issues log, risk register, and change log from the project | Request from PM |

**Pre-session preparation checklist:**

| Task | Owner | Timeline | Status |
|---|---|---|---|
| Define scope and objectives of the session | Facilitator | 2 weeks before | |
| Distribute anonymous pre-session survey | Facilitator | 1 week before | |
| Compile project performance data | Project Manager | 1 week before | |
| Review previous lessons learned for similar projects | Facilitator | 1 week before | |
| Book room/video call, send calendar invite with agenda | Facilitator | 1 week before | |
| Prepare facilitation materials (prompts, voting tools, templates) | Facilitator | 3 days before | |
| Set ground rules document (blameless, confidential, constructive) | Facilitator | 3 days before | |

**Session ground rules:**

| Rule | Purpose |
|---|---|
| No blame — focus on systems and processes | Create psychological safety for honest discussion |
| Everyone's perspective is valid | Ensure junior team members contribute freely |
| Specifics over generalities | "The requirements process was unclear" is better than "things were bad" |
| One conversation at a time | Respect facilitator's structure |
| What is said here stays here; what is learned here leaves here | Protect individuals while sharing organizational lessons |
| Decisions and actions are documented and assigned | Ensure accountability for follow-through |

### Step 2 — Facilitate the Retrospective

Guide the team through a structured reflection process.

**Session agenda (90-120 minutes recommended):**

| Time | Activity | Method | Output |
|---|---|---|---|
| 0-10 min | Welcome and ground rules | Facilitator presentation | Aligned expectations |
| 10-20 min | Project recap and metrics review | Data presentation | Shared understanding of outcomes |
| 20-45 min | What went well (keep doing) | Silent brainstorm, then group discussion | Categorized success factors |
| 45-70 min | What did not go well (stop or change) | Silent brainstorm, then group discussion | Categorized improvement areas |
| 70-85 min | Root cause analysis for top issues | 5 Whys or fishbone diagram | Root causes identified |
| 85-100 min | Action items and owners | Group prioritization and assignment | Committed action plan |
| 100-110 min | Appreciation round | Open floor | Team recognition |
| 110-120 min | Wrap-up and next steps | Facilitator summary | Clear follow-through plan |

**Categorization framework for findings:**

| Category | What Went Well | What Did Not Go Well |
|---|---|---|
| **Planning and scope** | [Findings] | [Findings] |
| **Execution and delivery** | [Findings] | [Findings] |
| **Team and communication** | [Findings] | [Findings] |
| **Stakeholder management** | [Findings] | [Findings] |
| **Tools and processes** | [Findings] | [Findings] |
| **Vendor and third-party** | [Findings] | [Findings] |
| **Risk and issue management** | [Findings] | [Findings] |
| **Quality and testing** | [Findings] | [Findings] |

**Root cause analysis template (5 Whys):**

| Issue | Why 1 | Why 2 | Why 3 | Why 4 | Why 5 (Root Cause) |
|---|---|---|---|---|---|
| [Issue A] | [Answer] | [Answer] | [Answer] | [Answer] | [Root cause] |
| [Issue B] | [Answer] | [Answer] | [Answer] | [Answer] | [Root cause] |
| [Issue C] | [Answer] | [Answer] | [Answer] | [Answer] | [Root cause] |

### Step 3 — Capture and Structure Knowledge

Document lessons in a format that is searchable and actionable.

**Lesson record template:**

| Field | Content |
|---|---|
| **Lesson ID** | LL-[Project Code]-[NNN] |
| **Project/Program** | [Name] |
| **Phase** | [Planning / Execution / Closing / Specific milestone] |
| **Category** | [From categorization framework] |
| **Type** | Success (keep doing) / Improvement (change) / Warning (avoid) |
| **Description** | [Clear, specific description of what happened] |
| **Context** | [Project type, team size, technology, timeline — so readers can assess relevance] |
| **Root Cause** | [Underlying cause, if applicable] |
| **Impact** | [Quantified where possible — days delayed, cost overrun, quality issue, etc.] |
| **Recommendation** | [Specific action to replicate success or prevent recurrence] |
| **Action Item** | [Concrete next step with owner and deadline] |
| **Tags** | [Searchable keywords for knowledge base retrieval] |
| **Date Captured** | [Date] |
| **Contributed By** | [Team/session participants] |

**Example lesson record:**

| Field | Content |
|---|---|
| Lesson ID | LL-PROJ-A-007 |
| Project | Project Alpha |
| Phase | Execution |
| Category | Vendor and third-party |
| Type | Improvement |
| Description | Vendor API integration took 3x longer than estimated because the vendor's documentation was outdated and their support response time averaged 5 business days |
| Context | SaaS integration project, 8-person team, 6-month timeline |
| Root Cause | Vendor documentation not validated pre-contract; no SLA for support response time |
| Impact | 4-week schedule delay, $50K additional cost |
| Recommendation | Include documentation review and support SLA validation in vendor evaluation criteria for all integration projects |
| Action Item | Update vendor evaluation template to include documentation quality check — Owner: Procurement Lead — Due: [Date] |
| Tags | vendor, integration, API, documentation, SLA, schedule delay |

### Step 4 — Identify Patterns Across Projects

Look for recurring themes that indicate systemic issues or strengths.

**Cross-project pattern analysis:**

| Pattern | Frequency | Projects Affected | Category | Systemic Root Cause | Recommended Systemic Fix |
|---|---|---|---|---|---|
| Requirements changes after development starts | 4 of last 6 projects | A, C, D, F | Planning and scope | No formal requirements sign-off gate | Implement mandatory requirements freeze with change control |
| Vendor delivery delays | 3 of last 6 projects | B, D, E | Vendor and third-party | No penalty clauses in contracts | Add delivery SLA penalties to vendor contract template |
| Testing compressed due to schedule pressure | 5 of last 6 projects | A, B, C, D, F | Quality and testing | Test phase treated as buffer for upstream delays | Protect test phase with fixed start date tied to quality gate |
| Strong team collaboration in co-located teams | 3 of last 6 projects | A, C, E | Team and communication | Co-location improves informal communication | Establish team co-location or structured sync rituals for remote teams |

**Pattern severity assessment:**

| Frequency | Impact | Systemic Priority |
|---|---|---|
| >50% of projects | High impact | Critical — address within 30 days |
| 25-50% of projects | High impact | High — address within 90 days |
| >50% of projects | Low-medium impact | Medium — address within 6 months |
| <25% of projects | Any impact | Low — monitor and address in next cycle |

### Step 5 — Generate Action Items and Track Completion

Convert lessons into accountable actions.

| Action ID | Action Description | Source Lesson | Owner | Due Date | Status | Completion Evidence |
|---|---|---|---|---|---|---|
| ACT-001 | Update vendor evaluation template with documentation quality criteria | LL-PROJ-A-007 | Procurement Lead | [Date] | Open / In Progress / Done | Template updated and published |
| ACT-002 | Implement mandatory requirements freeze gate in project methodology | Pattern analysis | PMO Director | [Date] | Open / In Progress / Done | Methodology document updated |
| ACT-003 | Add test phase protection policy to project planning guidelines | Pattern analysis | QA Lead | [Date] | Open / In Progress / Done | Policy published and communicated |
| ACT-004 | Create project kickoff checklist including lessons review step | Session finding | PMO Director | [Date] | Open / In Progress / Done | Checklist added to PM toolkit |

**Action tracking governance:**

| Review Forum | Frequency | Scope | Escalation |
|---|---|---|---|
| PMO weekly standup | Weekly | Action item status updates | Flag overdue items |
| Monthly PMO review | Monthly | Action completion rate, pattern trends | Escalate systemic items to leadership |
| Quarterly portfolio review | Quarterly | Organizational learning progress | Strategic investment in process improvements |

### Step 6 — Update Knowledge Base

Ensure lessons are findable and usable for future projects.

| Knowledge Base Element | Description | Owner |
|---|---|---|
| **Lesson records** | Individual lessons in structured format with tags | PMO Analyst |
| **Pattern summaries** | Cross-project themes with systemic fixes | PMO Director |
| **Project retrospective reports** | Full session documentation per project | Facilitator |
| **Checklist updates** | Modified templates, checklists, and guidelines | Process Owner |
| **FAQ / Common pitfalls** | Curated list of frequent issues and prevention strategies | Knowledge Manager |
| **Search and retrieval** | Tagged, indexed, and searchable by project type, category, and keyword | PMO Analyst |

**Knowledge base maintenance cadence:**

| Activity | Frequency | Owner |
|---|---|---|
| Add new lessons from completed retrospectives | Within 1 week of session | Facilitator |
| Review and tag lessons for searchability | Monthly | PMO Analyst |
| Analyze patterns across recent lessons | Quarterly | PMO Director |
| Archive outdated lessons (technology or process no longer relevant) | Semi-annually | Knowledge Manager |
| Validate that new projects reviewed relevant lessons at kickoff | At every project kickoff gate | PMO Director |

---

## Output Format

```markdown
# Lessons Learned Report: [Project/Program Name]

**Project Phase:** [Phase or milestone reviewed]
**Session Date:** [Date]
**Facilitator:** [Name]
**Participants:** [Names and roles]

---

## 1. Executive Summary
[Project overview, key outcomes, top 3 lessons, and systemic recommendations]

## 2. Project Performance Summary
[Schedule, budget, quality, and satisfaction metrics — planned vs. actual]

## 3. What Went Well
[Categorized success factors with specific examples]

## 4. What Did Not Go Well
[Categorized improvement areas with root cause analysis]

## 5. Lesson Records
[Structured records for each lesson captured]

## 6. Pattern Analysis
[Recurring themes across this and prior projects]

## 7. Action Items
[Prioritized actions with owners, deadlines, and tracking plan]

## 8. Knowledge Base Updates
[Specific updates to templates, checklists, guidelines, and FAQ]
```

---

## Quality Checklist

- [ ] Session was facilitated with clear ground rules emphasizing blameless culture
- [ ] Pre-session survey was distributed and responses incorporated into facilitation
- [ ] Both successes and failures are captured with equal rigor
- [ ] Root cause analysis was applied to the top 3-5 issues (not just symptoms described)
- [ ] Every lesson has a structured record with context, impact, recommendation, and tags
- [ ] Action items are specific, assigned to named owners, and have deadlines
- [ ] Cross-project patterns are identified with systemic fix recommendations
- [ ] Lessons are tagged and added to the knowledge base within 1 week of the session
- [ ] Previous lessons from similar projects were reviewed as part of preparation
- [ ] Action item tracking is integrated into existing governance cadence (not a separate process)

---

## Edge Cases

| Scenario | How to Handle |
|---|---|
| Failed project with high emotions and blame risk | Use anonymous pre-session input heavily; consider having an external facilitator; reinforce blameless ground rules; focus on process and system improvements |
| Very large team (20+ participants) | Break into small group sessions by workstream first; then bring representatives together for cross-cutting themes and action planning |
| Remote or distributed team | Use digital collaboration tools (Miro, Mural, virtual sticky notes); allow asynchronous input before the live session; record the session for absent participants |
| Project cancelled before completion | Still conduct a retrospective — the decision to cancel and the reasons why are among the most valuable lessons; focus on early warning signs |
| Successful project with "nothing went wrong" sentiment | Probe deeper — ask what could have gone even better, what was lucky vs. skillful, and what would not survive if key people left; capture success patterns for replication |
| Stakeholder refuses to participate | Document the gap; gather their input through 1-on-1 conversation or written submission; note incomplete perspective in the report |
| Same lessons appearing repeatedly across projects | Escalate to portfolio governance as a systemic issue requiring structural intervention (process change, tool investment, or training program), not just another action item |
