---
name: writing-skills
description: Use when creating new skills or editing existing skills - applies TDD principles to process documentation with RED-GREEN-REFACTOR cycle
---

# Writing Skills

## Overview

**Writing skills IS Test-Driven Development applied to process documentation.**

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

**REQUIRED BACKGROUND:** You MUST understand test-driven-development before using this skill.

## What is a Skill?

A **skill** is a reference guide for proven techniques, patterns, or tools.

**Skills are:** Reusable techniques, patterns, tools, reference guides

**Skills are NOT:** Narratives about how you solved a problem once

## TDD Mapping for Skills

| TDD Concept | Skill Creation |
|-------------|----------------|
| **Test case** | Pressure scenario with subagent |
| **Production code** | Skill document (SKILL.md) |
| **Test fails (RED)** | Agent violates rule without skill |
| **Test passes (GREEN)** | Agent complies with skill present |
| **Refactor** | Close loopholes while maintaining compliance |

## When to Create a Skill

**Create when:**
- Technique wasn't intuitively obvious
- You'd reference this again across projects
- Pattern applies broadly
- Others would benefit

**Don't create for:**
- One-off solutions
- Standard practices elsewhere
- Project-specific conventions (put in CLAUDE.md)

## Directory Structure

```
skills/
  skill-name/
    SKILL.md              # Main reference (required)
    supporting-file.*     # Only if needed
```

## SKILL.md Structure

### Frontmatter (YAML)

```yaml
---
name: skill-name-with-hyphens
description: Use when [specific triggering conditions and symptoms]
---
```

**Rules:**
- Only two fields: `name` and `description`
- Max 1024 characters total
- Start description with "Use when..."
- Describe triggering conditions, NOT what skill does

### Sections

- **Overview**: What is this? Core principle in 1-2 sentences
- **When to Use**: Symptoms and use cases
- **The Process**: Step-by-step instructions
- **Quick Reference**: Table or bullets for scanning
- **Common Mistakes**: What goes wrong + fixes
- **Red Flags**: STOP conditions

## Claude Search Optimization

**Description field is critical** - Claude reads it to decide which skills to load.

```yaml
# ❌ BAD: Summarizes workflow
description: Use when executing plans - dispatches subagent per task

# ✅ GOOD: Just triggering conditions
description: Use when executing implementation plans with independent tasks
```

**Include keywords:** Error messages, symptoms, tools, synonyms

## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

This applies to NEW skills AND EDITS.

**No exceptions:**
- Not for "simple additions"
- Not for "just adding a section"
- Delete untested changes

## Testing All Skill Types

### Discipline-Enforcing Skills (TDD, debugging)

**Test with:**
- Academic questions
- Pressure scenarios
- Multiple pressures combined
- Identify rationalizations

### Technique Skills (how-to guides)

**Test with:**
- Application scenarios
- Variation scenarios
- Missing information tests

### Reference Skills (documentation/APIs)

**Test with:**
- Retrieval scenarios
- Application scenarios
- Gap testing

## RED-GREEN-REFACTOR for Skills

### RED: Write Failing Test

Run pressure scenario with subagent WITHOUT the skill. Document:
- What choices did they make?
- What rationalizations did they use?
- Which pressures triggered violations?

### GREEN: Write Minimal Skill

Write skill that addresses those specific rationalizations. Run scenarios WITH skill. Agent should now comply.

### REFACTOR: Close Loopholes

Agent found new rationalization? Add explicit counter. Re-test until bulletproof.

## Bulletproofing Against Rationalization

### Close Every Loophole Explicitly

```markdown
**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while running tests
- Delete means delete
```

### Address "Spirit vs Letter"

Add early:

```markdown
**Violating the letter of the rules is violating the spirit of the rules.**
```

### Build Rationalization Table

Capture from baseline testing:

```markdown
| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Narrative example | Use actionable patterns |
| Multi-language dilution | One excellent example |
| Code in flowcharts | Use markdown code blocks |
| Generic labels | Semantic meaning |

## Quick Reference

| Situation | Action |
|-----------|--------|
| New skill | TDD cycle: RED → GREEN → REFACTOR |
| Edit skill | Test first, then edit, then retest |
| Discipline skill | Add explicit counters to rationalizations |
| Reference skill | Test retrieval and application |

## Integration

- **superpowers:test-driven-development** - Required background
- **superpowers:systematic-debugging** - For testing discipline skills
