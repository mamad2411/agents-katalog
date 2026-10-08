---
unit-id: S2
plan: docs/plans/2026-06-05-001-slice-pwrl-plan-skill.md
status: archived
superseded-by: docs/plans/2026-06-10-002-fix-and-verify-pwrl-plan.md (Units U1-U8)
created: 2026-06-05
type: PWRL Task
archived: 2026-06-10
dependencies: [S1]
files:
  - skills/pwrl-plan-scope/SKILL.md (new)
  - skills/pwrl-plan-scope/references/ (new, if needed)
learnings: []
---

> ⚠️ **ARCHIVED & SUPERSEDED** — 2026-06-10
> 
> This task has been superseded by a comprehensive fix & verification plan:
> **[Fix and Verify PWRL Plan Micro-Skills for Production Readiness](docs/plans/2026-06-10-002-fix-and-verify-pwrl-plan.md)**
> 
> The implementation from this task (pwrl-plan-scope/SKILL.md) is complete and in use.
> However, critical P0/P1 findings from code review require fixes to enable production deployment.
> 
> **Related work:** 
> - Code review: `.context/pwrl-review/pwrl-plan-comprehensive-review/review.md`
> - New plan: `docs/plans/2026-06-10-002-fix-and-verify-pwrl-plan.md`
> - New tasks: `docs/tasks/to-do/2026-06-10-u*.md`
> 
> ---

# S2: Create pwrl-plan-scope Micro-Skill

## Goal

Extract Phase 1 (Context & Scope) logic from the monolithic `pwrl-plan/SKILL.md` into a standalone `pwrl-plan-scope` micro-skill. This skill gathers context, checks learnings, validates domain, and returns a scoped context object that downstream skills (S3, S4, S5) consume.

## Context

Phase 1 of the planning workflow handles:
- Resuming or creating new plans
- Searching for relevant brainstorms, requirements, and learnings
- Validating domain (software vs. non-software)
- Bootstrapping initial context if no docs exist

This task extracts that logic as an independent skill that can be tested and used separately.

**Why this matters:** S2 is the entry point to the planning workflow; its output (scoped context) flows to all downstream skills.

**Dependency:** Depends on S1 (templates must exist). Can be parallelized with other skills once S1 is done.

## Related Learnings

- **Learning: Planning Workflow Fundamentals** (if exists at `docs/learnings/planning-workflow.md`)
  - *Applicability:* Covers Phase 1 concepts; guides question sequencing and context gathering.

**Learning Gap:** If no learning exists for "Scope Gathering Patterns", create one via `/pwrl-learnings` after S2 completes.

## Implementation Steps

1. **Extract Phase 1 Logic from pwrl-plan/SKILL.md**
   - Read Phase 1: Context & Scope section from pwrl-plan/SKILL.md completely
   - Identify all sub-steps:
     - Resume or Create plan decision
     - Requirements check (search docs/brainstorms/, docs/requirements/, docs/learnings/INDEX.md)
     - Learnings Index gate (identify related learnings)
     - Domain check (software vs. non-software)
     - Bootstrap (if no docs, define Problem Frame, Intended Behavior, Success Criteria)
   - Note any ask_user tool calls for decision points

2. **Design Skill Interface**
   - **Input:** Task description (from user)
   - **Output:** Scoped context object (JSON or markdown) with:
     ```
     {
       "problem": "...",
       "intended_behavior": "...",
       "success_criteria": ["...", "..."],
       "domain": "software|non-software",
       "existing_plan": "path/to/plan.md|null",
       "related_learnings": ["docs/learnings/...md", ...],
       "learning_gaps": ["gap_name", ...],
       "requirements": { ... }
     }
     ```
   - Document state passing to S3 (pwrl-plan-research)

3. **Create SKILL.md**
   - Path: `skills/pwrl-plan-scope/SKILL.md`
   - Structure:
     ```markdown
     ---
     name: pwrl-plan-scope
     description: "Gather context and scope for planning workflow"
     argument-hint: "[task description or goal to plan]"
     ---
     
     # Scope Gathering
     
     [Extracted Phase 1 logic]
     
     ## Interaction Method
     [ask_user tool usage, question sequencing]
     
     ## Workflow
     [Sub-steps for each phase decision]
     ```

4. **Implement Decision Logic**
   - **If existing plan found:**
     - Ask user: Resume? Review? Archive? Delete? Create new?
     - Handle each choice
   - **If no existing plan:**
     - Ask: Is this software-related? (domain validation)
     - Ask: What's the problem? (bootstrap Problem Frame)
     - Ask: What should happen? (bootstrap Intended Behavior)
     - Ask: How do we know it works? (bootstrap Success Criteria)

5. **Implement Learnings Index Gate**
   - Read `docs/learnings/INDEX.md`
   - Search for entries related to task description
   - Return list of related learnings with applicability notes
   - Mark any identified learning gaps (e.g., "no learning for Auth patterns" if task is auth-related)

6. **Implement Requirements Search**
   - Search `docs/brainstorms/` for matching files
   - Search `docs/requirements/` for matching files
   - Return: List of found documents + extracted relevant sections

7. **Create references/ subdirectory (if needed)**
   - If context detection needs helper logic, create reference docs
   - E.g., domain detection rules, typical questions for bootstrap, etc.

## Code Patterns

**Example: Scoped Context Output (Markdown)**

```markdown
---
scope-id: 2026-06-05-001-scope
domain: software
status: confirmed
---

# Scoped Context

## Problem
User wants to plan decomposition of planning skill into micro-skills.

## Intended Behavior
Planning workflow is split into 4 independent skills that orchestrate via agent.

## Success Criteria
- All phases have dedicated skills
- Agent successfully calls them in sequence
- Fallback works if agents unavailable

## Related Learnings
- docs/learnings/planning-workflow.md
- docs/learnings/agent-orchestration.md

## Learning Gaps
- No learning for "Fallback Strategy & Agent Detection"
  (Follow-up: Document during/after S7)

## Requirements Found
- docs/requirements/planning-phases.md (relevant: lists Phase 1-4)
```

**Example: ask_user Integration**

```
## Workflow

1. **Existing Plan Check**
   - Search docs/plans/ for related plans
   - If found: ask_user with options (Resume | Review | Archive | Delete | Create New)
   - If not found: proceed to domain check

2. **Domain Validation**
   - Ask: "Is this a software/code planning task?"
   - If yes: software domain
   - If no: suggest universal planning template (outside scope of pwrl-plan)
```

## Edge Cases

1. **Existing plan is outdated**
   - Solution: Show plan summary; ask user if they want to resume or create new
   - Default: Create new (safer)

2. **Multiple related learnings found**
   - Solution: Return all related learnings; user can filter in downstream skills
   - Mark which are most relevant (high/medium/low)

3. **No brainstorms/requirements found**
   - Solution: That's OK; proceed with bootstrap approach
   - Document in context: "No existing requirements; bootstrapped from scratch"

4. **Task description is vague**
   - Solution: Ask clarifying questions (e.g., "Is this a new feature, bug fix, or refactor?")
   - Iterate until Problem Frame is clear

5. **Learning gaps identified**
   - Solution: Include learning gap notes in output
   - Suggest `/pwrl-learnings` follow-up in downstream skills

## Testing

### Unit Test: Existing Plan Resume

- **Input:** User task + existing plan in docs/plans/
- **Verification:**
  - Skill detects existing plan
  - ask_user presents options (Resume | Review | Archive | Delete | Create New)
  - User can select each option without errors
  - Scoped context reflects chosen action

### Unit Test: Bootstrap from Scratch

- **Input:** User task description (no existing plan)
- **Verification:**
  - Skill asks domain validation question
  - If software: asks Problem Frame, Intended Behavior, Success Criteria
  - Scoped context includes bootstrapped values
  - All required fields are populated

### Unit Test: Learnings Index Gate

- **Input:** Task description + docs/learnings/INDEX.md
- **Verification:**
  - Skill searches INDEX.md for related entries
  - Returns list of related learnings with file paths
  - Identifies learning gaps
  - Marks each learning with applicability (high/medium/low)

### Unit Test: Requirements Search

- **Input:** Task description + docs/brainstorms/ + docs/requirements/
- **Verification:**
  - Skill searches both directories
  - Returns matching file paths + relevant excerpts
  - Gracefully handles missing directories
  - Returns empty list if no matches found

### Integration Test: Full Scope Workflow (with S3 state passing)

- **Input:** User task description
- **Verification:**
  - Skill completes all Phase 1 steps
  - Scoped context is valid JSON/markdown
  - Context can be parsed and passed to S3 (pwrl-plan-research) without additional user input
  - All output fields match expected schema

## Acceptance Criteria

✅ `skills/pwrl-plan-scope/SKILL.md` exists and is functional  
✅ Skill handles "existing plan" scenario (resume/review/archive/delete/create options)  
✅ Skill handles "new plan" scenario (domain validation + bootstrap)  
✅ Learnings Index gate works: searches `docs/learnings/INDEX.md`, returns related entries  
✅ Requirements search works: finds docs in `docs/brainstorms/` and `docs/requirements/`  
✅ Scoped context output includes all required fields (problem, behavior, criteria, domain, learnings, gaps)  
✅ ask_user tool is used for all decision points (no plain-text questions)  
✅ Skill works independently; can be tested without S3  
✅ State passing to S3 is documented; context schema is clear  

## References

- Source: Phase 1 section in `skills/pwrl-plan/SKILL.md`
- Used by: S3 (pwrl-plan-research) — receives scoped context
- Integration: ask_user tool for user decisions
- Output state: Passed to S3 for research phase

