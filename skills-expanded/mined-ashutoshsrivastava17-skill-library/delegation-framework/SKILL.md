---
name: delegation-framework
description: >
  Build delegation frameworks — task categorization, skill matching,
  authority levels, feedback loops, and accountability tracking.
  TRIGGER when: user says /delegation-framework or asks about effective delegation.
argument-hint: "[role or team context]"
user-invocable: true
---
# Delegation Framework
## Process
### Step 1: Categorize Tasks
| Category | Delegate? | Example |
|----------|----------|---------|
| Only I can do | No | Strategy decisions, key relationships |
| I should do | Selectively | Complex problems, mentoring |
| Others can do | Yes | Recurring tasks, well-defined processes |
| Others should do | Definitely | Growth opportunities, skill building |
### Step 2: Match Tasks to People
| Factor | Assessment |
|--------|-----------|
| Skill level | Can they do it now, or need development? |
| Interest | Motivated by this type of work? |
| Capacity | Have bandwidth? |
| Growth | Will this stretch them appropriately? |
### Step 3: Define Authority Levels
| Level | Description | Example |
|-------|-----------|---------|
| 1 | Investigate and report | "Research options and present to me" |
| 2 | Recommend | "Recommend an approach for my approval" |
| 3 | Act and inform | "Handle it and keep me updated" |
| 4 | Act independently | "Own this completely" |
### Step 4: Set Up Feedback Loops
| Checkpoint | Frequency | Format |
|-----------|-----------|--------|
| Brief check-in | Weekly | Quick status update |
| Progress review | Milestone-based | Detailed discussion |
| Final review | On completion | Quality assessment |
### Step 5: Track Accountability
| Delegated Task | To | Authority | Deadline | Status |
|---------------|-----|-----------|----------|--------|
| [task] | [name] | Level X | [date] | On track/At risk |
## Output Format
```markdown
## Delegation Plan
### Tasks: [Categorized list]
### Assignments: [Task-person matching]
### Authority: [Level per assignment]
### Check-ins: [Schedule]
```
## Quality Checklist
- [ ] Tasks categorized honestly (not hoarding)
- [ ] Assignments match skill and capacity
- [ ] Authority level is clear
- [ ] Check-in cadence balances support and autonomy
- [ ] Accountability is tracked
## Edge Cases
- For new team members, start at lower authority levels and increase
- If delegation fails, diagnose (clarity? capacity? skill?) before re-assigning
- For time-sensitive tasks, delegate with authority level 3-4 to avoid bottlenecks
