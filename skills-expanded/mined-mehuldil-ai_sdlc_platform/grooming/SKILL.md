# /project:grooming

**Interactive Story Breakdown & Estimation**

Works in: Cursor IDE chat + Claude Code + CLI

## Usage

```
/project:grooming AB#123
/project:grooming AB#123 --type=master
/project:grooming AB#123 --type=sprint --sprint=12
```

## What This Does

1. **Loads PRD** from work item
2. **Breaks down into stories** (master → sprint → tasks)
3. **Asks for role-specific input** (acceptance criteria, edge cases)
4. **Generates story cards** with full details
5. **Estimates story points** based on complexity
6. **Creates ADO stories** with linked parent

## Interactive Flow

```
User: /project:grooming AB#123

Claude: 🎯 Story Breakdown & Grooming

Grooming type?
  [1] Master Story (feature-level breakdown)
  [2] Sprint Story (sprint-level slice of master)
  [3] Both (create master + 2-3 sprint stories)

User: [1]

✅ LOADED PRD:
  Epic: Multi-language signup (AB#12345)
  Feature: 5 target languages (EN, ES, FR, DE, ZH)
  Scope: Signup flow only

📊 MASTER STORY STRUCTURE:

Based on PRD, suggests breaking into:
  1. Backend: Language pack delivery + API
  2. Frontend: UI translation + language selector
  3. Database: i18n schema + migration
  4. QA: Testing across languages

Generate MASTER story breaking these into phases?
  [1] Yes, create it
  [2] Customize breakdown first
  [3] Skip master, go straight to sprint

User: [1]

✓ Generating Master Story...

**MASTER STORY: Multi-language signup support**

[AC-01 through AC-E02 acceptance criteria]
[Success metrics]
[Design references]
[Dependencies]

📝 ADDITIONAL DETAILS?

  [1] Add edge cases (e.g., RTL languages)
  [2] Add analytics events
  [3] Add performance requirements
  [4] Create it as-is

User: [1]

Adding edge cases for RTL language support...

✓ Updated AC with RTL considerations

CREATE MASTER STORY?
  [1] Yes, post to ADO
  [2] Preview first
  [3] Edit details
  [4] Cancel

User: [1]

✓ Created Master Story AB#12346
✓ Saved grooming output to .sdlc/memory/grooming-AB#12346.md
```

## CLI Mode

```bash
# Interactive
$ sdlc skill grooming AB#123 --type=master

# Sprint story from master
$ sdlc skill grooming AB#123 --type=sprint --sprint=12

# Auto-generate both
$ sdlc skill grooming AB#123 --type=both --auto-create
```

## Skill: story-generator

Templates for:
- Master User Story (16 sections: metadata, goals, personas, AC, success metrics, etc.)
- Sprint User Story (sliced AC, focus on sprint capacity)
- Technical Task breakdown (DB migration, API design, etc.)
- Story point estimation based on:
  - Complexity (simple, medium, complex)
  - Scope (lines of code, components affected)
  - Risk (unknown tech, external dependency)

## ADO Story Creation

Creates with:
- **Master Story**: Full 16-section template, story points 13-21
- **Sprint Story**: Subset of AC, story points 3-8
- **Tasks**: Backend, Frontend, QA tasks with estimates
- **Tags**: `story:product`, `claude:generated`, `grooming:done`
- **Parent**: Linked to Epic or Master Story

## G3 Gate Clear Conditions

Gate G3 is CLEAR when:
- Sprint story created with AC (AC-01 through AC-E02)
- All AC independently testable
- Story points assigned (3-8 range)
- No AC dependencies on each other
- Design assets linked (if UX-heavy)

## Next Commands

- `/project:architecture-review AB#123` - Review architecture feasibility
- `/project:system-design AB#123` - Design system and APIs
- `/project:sprint-planning AB#123` - Plan sprint with team

---

## Model & Token Budget
- **Model Tier:** Sonnet (complex story generation)
- Input: ~2K tokens (PRD + template)
- Output: ~4K tokens (master + sprint stories)

