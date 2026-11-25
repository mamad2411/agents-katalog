# /project:sprint-planning

**Interactive Sprint Planning & Task Breakdown**

Works in: Cursor IDE chat + Claude Code + CLI

## Usage

```
/project:sprint-planning AB#123
/project:sprint-planning AB#123 --sprint=12
/project:sprint-planning AB#123 --post-comments
```

## What This Does

1. **Loads sprint story** with acceptance criteria
2. **Breaks down into developer tasks** (BE, FE, QA, DevOps)
3. **Estimates effort** (hours) per task
4. **Assigns tasks** to team members (if known)
5. **Posts task breakdown as ADO comment** (user provides notes in chat before posting)
6. **Generates sprint board** view with dependencies

## Interactive Flow

```
User: /project:sprint-planning AB#123 --sprint=12

Claude: 📅 Sprint Planning & Task Breakdown

✅ STORY LOADED:
  Story: Phone verification & OTP (Sprint 12)
  Story Points: 5
  AC: 6 items (phone entry, OTP send, OTP verify, error handling, edge cases)
  Team: Multi-disciplinary (Backend, Frontend, QA)

🎯 TASK BREAKDOWN:

Based on AC, suggest these tasks:

**Backend Tasks:**
  • BKD-01: Setup signup service (auth + phone validation) — 4h
  • BKD-02: Implement OTP generation + SMS dispatch (Twilio) — 3h
  • BKD-03: OTP verification + session management — 2h
  • BKD-04: Error handling + rate limiting — 2h

**Frontend Tasks:**
  • FE-01: Design phone entry screen (UI/UX) — 2h
  • FE-02: Implement phone form component + validation — 3h
  • FE-03: Implement OTP input screen + countdown — 2h
  • FE-04: Error messaging + accessibility — 1h

**QA Tasks:**
  • QA-01: Test happy path (phone entry to success) — 2h
  • QA-02: Test all error scenarios (invalid phone, expired OTP) — 2h
  • QA-03: Load test (verify >1000 RPS feasibility) — 3h

Total Estimated: 26 hours (if evenly distributed over 2-week sprint)

Accept breakdown?
  [1] Yes, create all tasks
  [2] Adjust task estimates
  [3] Rebalance by team size
  [4] Edit task descriptions first

User: [1]

👥 TEAM ASSIGNMENT:

Team members in Sprint 12?
  [1] Select from existing team
  [2] Auto-assign based on availability
  [3] Leave unassigned (assign later)

User: [1]

Available team:
  BE: Alice (5h available), Bob (6h available)
  FE: Carol (8h available), Dave (4h available)
  QA: Eve (7h available)

Suggested assignment:
  • Alice → BKD-02 (3h) + BKD-04 (2h) [5h total]
  • Bob → BKD-01 (4h) + BKD-03 (2h) [6h total]
  • Carol → FE-01 (2h) + FE-02 (3h) + FE-04 (1h) [6h available, 6h assigned] ✓
  • Dave → FE-03 (2h) [4h available, 2h assigned] ✓
  • Eve → QA-01 (2h) + QA-02 (2h) + QA-03 (3h) [7h total] ✓

Confirm assignment?
  [1] Yes, auto-assign as suggested
  [2] Manually adjust assignments
  [3] Leave unassigned

User: [1]

✓ Assignments confirmed.

📊 SPRINT BOARD PREVIEW:

Sprint 12: Multi-language Signup Phase 1

[Backlog] → [To Do] → [In Progress] → [Review] → [Done]

To Do (11 tasks, 26h):
  • BKD-01 (Bob, 4h, blocker for FE)
  • BKD-02 (Alice, 3h)
  • BKD-03 (Bob, 2h, depends on BKD-02)
  • BKD-04 (Alice, 2h)
  • FE-01 (Carol, 2h)
  • FE-02 (Carol, 3h, depends on FE-01)
  • FE-03 (Dave, 2h, depends on BKD-03)
  • FE-04 (Carol, 1h)
  • QA-01 (Eve, 2h, depends on all dev complete)
  • QA-02 (Eve, 2h)
  • QA-03 (Eve, 3h)

Critical Path: BKD-01 (4h) → BKD-03 (2h) → FE-03 (2h) → QA (7h) = 15h
Slack (can run in parallel): All other backend/frontend = 11h

⚠️ RISKS & DEPENDENCIES:

  • BKD-01 is critical path blocker (FE-03 depends on it)
  • QA-03 (load testing) may fail if infrastructure not ready
  • Twilio API integration (external dependency) may cause delays

Mitigation:
  • Start BKD-01 immediately (day 1)
  • Parallel QA environment setup (day 1)
  • Mock Twilio for early testing (FE can proceed in parallel)

POST TASK BREAKDOWN AS ADO COMMENT?
  [1] Yes, post as comment on AB#123
  [2] Let me add notes first, then post as comment
  [3] Preview comment first
  [4] Cancel

User: [1]

✓ Posted task breakdown as ADO comment on AB#123
✓ Linked all tasks to story AB#123
✓ Set task dependencies
✓ Assigned to team members
✓ Saved sprint plan to .sdlc/memory/sprint-planning-AB#123.md

PUBLISH SPRINT PLAN?
  [1] Yes, update ADO story with sprint summary
  [2] Just save locally
  [3] Cancel

User: [1]

✓ Published sprint plan comment to AB#123
✓ Sprint planning complete
```

## CLI Mode

```bash
$ sdlc skill sprint-planning AB#123 --sprint=12
$ sdlc skill sprint-planning AB#123 --post-comments --auto-assign
$ sdlc skill sprint-planning --sprint=12 --batch
```

## ADO Outcomes

- **Task Breakdown Comment**: Posted as ADO comment with all tasks listed
- **Dependencies Linked**: Predecessor/successor relationships
- **Team Assignments**: User or task owner assigned
- **Estimates**: Hours estimated per task
- **Sprint Board**: Visual layout with critical path highlighted

## G5 Gate Clear Conditions

Gate G5 is CLEAR when:
- All sprint stories have task breakdowns
- Team capacity validated (total hours <available)
- Dependencies documented (no circular dependencies)
- Critical path identified and mitigated
- Sprint board ready for standup

## Next Commands

- `/project:implementation AB#123` - Begin development
- `/project:code-review AB#123` - Review code during sprint
- `/project:test-design AB#123` - Design QA approach

---

## Model & Token Budget
- **Model Tier:** Sonnet (task generation + assignment logic)
- Input: ~1.5K tokens (story + team roster)
- Output: ~2.5K tokens (task breakdown + assignments + plan)

