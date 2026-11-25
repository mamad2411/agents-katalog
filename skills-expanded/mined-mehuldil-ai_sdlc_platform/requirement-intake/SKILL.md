# /project:requirement-intake

**Interactive Requirement Intake & Work Item Creation**

Works in: Cursor IDE chat + Claude Code + CLI

## Usage

```
/project:requirement-intake
/project:requirement-intake --title="Feature description"
/project:requirement-intake --epic=AB#123 --type=user-story
```

## What This Does

1. **Captures requirements** from user description or PRD upload
2. **Classifies task type** (feature, bug, task, epic)
3. **Detects missing information** (scope, acceptance criteria, estimation)
4. **Asks clarifying questions** (audience, constraints, success metrics)
5. **Generates ADO work item** with all fields populated
6. **Creates memory record** for session continuity

## Interactive Flow

```
User: /project:requirement-intake

Claude: 📋 Requirement Intake & Work Item Creation

What are we building?
  [1] New feature (user-facing capability)
  [2] Bug fix (defect resolution)
  [3] Technical task (refactor, tooling)
  [4] Epic (large initiative)

User: [1]

Tell me about the feature:

User: "Multi-language support for signup flow"

✅ UNDERSTANDING:
  • Type: Feature
  • Scope: Signup flow internationalization
  • Language support: Multiple

❓ MISSING INFORMATION:

1. Target languages?
   Need: List of languages (e.g., EN, ES, FR, DE, ZH, JA)

2. Scope: Full app or just signup?
   Need: Clarification on phase 1 vs future phases

3. Success metric?
   Need: How will we measure success?

4. User stories breakdown?
   Need: Any phased approach (backend > frontend)?

Next?
  [1] Answer questions now
  [2] Skip questions (I'll fill later)
  [3] Upload PRD document
  [4] Cancel

User: [1]

📝 Target languages?

User: "EN, ES, FR, DE, ZH"

✓ Captured: 5 languages

📝 Full app or just signup?

User: "Just signup phase 1"

✓ Captured: Phase 1 scope

[Continue for remaining questions...]

📊 SUMMARY:

Feature: Multi-language support (signup)
Languages: EN, ES, FR, DE, ZH (phase 1)
Type: Epic (suggests breaking into stories)
Success: X% completion of translations, Y% user signups in non-EN languages

CREATE WORK ITEM?
  [1] Create Epic + Master Story
  [2] Create as single User Story
  [3] Review & edit before creating
  [4] Cancel

User: [1]

✓ Created Epic AB#12345 (Multi-language signup)
✓ Created Master Story AB#12346
✓ Saved to .sdlc/memory/requirement-intake-AB#12345.md

ADO Links:
- Epic: https://dev.azure.com/.../AB#12345
- Master: https://dev.azure.com/.../AB#12346
```

## CLI Mode

```bash
# Interactive
$ sdlc skill requirement-intake

# With title
$ sdlc skill requirement-intake --title="Feature description"

# Create as specific type
$ sdlc skill requirement-intake --type=feature --epic=AB#123

# Batch mode (provide file)
$ sdlc skill requirement-intake --file=requirements.txt --auto-create
```

## Skill: requirement-classifier

Analyzes input and determines:
- Work item type (Epic, Feature, Story, Task, Bug)
- Scope complexity (simple, medium, complex)
- Required estimation approach
- Phasing strategy (single story vs multi-story epic)
- Dependency detection (needs architecture review? design? etc.)

## ADO Work Item Creation

Creates work items with:
- **Title**: Captured from user description
- **Description**: Structured narrative with goals, scope, success metrics
- **Acceptance Criteria**: Initial AC list (may be refined in grooming)
- **Story Points**: Auto-estimate based on type and complexity
- **Tags**: `claude:generated`, `intake:done`, `ready:pre-grooming`
- **Parent**: Linked to parent Epic (if specified)

## G1 Gate Clear Conditions

Gate G1 is CLEAR when:
- Work item created (has ADO ID)
- Basic fields populated (title, description, AC stubs)
- Memory record saved for future stages
- No blocking questions left unanswered

## Next Commands

- `/project:prd-review AB#12345` - Review PRD/requirements for gaps
- `/project:grooming AB#12345 --type=master` - Generate master story
- `/project:architecture-review AB#12345` - Architecture feasibility check

---

## Model & Token Budget
- **Model Tier:** Haiku (simple classification) or Sonnet (complex feature analysis)
- Input: ~1.5K tokens (user description + classification)
- Output: ~2K tokens (questions + recommendations + work item)

