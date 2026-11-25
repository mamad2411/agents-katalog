---
name: writing-skills
description: "How to author and structure Claude Code skills: SKILL.md frontmatter, writing trigger-focused descriptions, file organization, and naming. Apply when creating or editing a skill (a SKILL.md file)."
paths: ["**/SKILL.md"]
---

# Writing Skills (Meta-Skill)

> Adapted from [obra/superpowers](https://github.com/obra/superpowers)

## Overview

A guide for creating effective, discoverable, and well-tested skills. Use this when authoring new skills for this repo.

## What is a Skill?

A **skill** is a reference guide for proven techniques, patterns, or tools. Skills help AI agents find and apply effective approaches.

**Skills are:** Reusable techniques, patterns, tools, reference guides
**Skills are NOT:** Narratives about how you solved a problem once

## When to Create a Skill

**Create when:**
- Technique wasn't intuitively obvious
- You'd reference this again across projects
- Pattern applies broadly (not project-specific)
- Others would benefit

**Don't create for:**
- One-off solutions
- Standard practices well-documented elsewhere
- Project-specific conventions (put in CLAUDE.md instead)
- Mechanical constraints enforceable with linting/validation

## Skill Types

- **Technique:** Concrete method with steps (condition-based-waiting, root-cause-tracing)
- **Pattern:** Way of thinking about problems (flatten-with-flags, test-invariants)
- **Reference:** API docs, syntax guides, tool documentation

## SKILL.md Structure

Every skill is a `skills/<skill-name>/SKILL.md` file that opens with YAML frontmatter, then markdown:

```markdown
---
name: skill-name
description: One line — lead with the trigger use case (this drives auto-invocation).
# disable-model-invocation: true   # command-only: won't auto-trigger; run as /skill-name
# paths: ["**/*.py"]               # auto-trigger only when working on matching files
---

# Skill Name

## Overview
What is this? Core principle in 1-2 sentences.

## When to Use
Bullet list with SYMPTOMS and use cases.
When NOT to use.

## Core Pattern
Before/after comparison or step-by-step process.

## Quick Reference
Table or bullets for scanning common operations.

## Common Mistakes
What goes wrong + fixes.
```

## Discovery Optimization

Future Claude instances need to FIND your skill. Optimize for this:

**Description:** Start with "Use when..." to focus on triggering conditions. Describe the *problem*, not the *solution*. NEVER summarize the skill's workflow in the description — Claude may follow the description shortcut instead of reading the full skill.

```
# BAD: Summarizes workflow
description: Use when executing plans - dispatches subagent per task with code review

# GOOD: Just triggering conditions
description: Use when implementing any feature or bugfix, before writing implementation code
```

**Keywords:** Use words Claude would search for — error messages, symptoms, synonyms, tool names.

**Naming:** Kebab-case directory names. For a command-only skill the directory name *is* the slash command (`scaffold`, `verify-django`, `nextjs-bootstrap`) — name it exactly what you'd type. For an auto-triggering skill use a clear noun/verb phrase that matches its trigger (`django-patterns`, `work-discipline`, `plan-and-scope`). Match the repo's existing names; don't force gerunds.

## Token Efficiency

Every token in frequently-loaded skills counts.

- Move details to supporting files, reference with cross-links
- Use cross-references instead of repeating content
- Compress examples — one excellent example beats many mediocre ones
- Don't repeat what's in cross-referenced skills
- Target: <200 words for frequently-loaded skills, <500 words for others

## Code Examples

**One excellent example beats many mediocre ones.** Choose the most relevant language for the pattern. Make it complete, runnable, and well-commented. Don't implement in 5+ languages.

## File Organization

```
skills/
  skill-name/
    SKILL.md              # Main reference (required)
    supporting-file.*     # Only if needed (heavy reference, reusable tools)
```

Keep content inline unless it exceeds ~100 lines of reference material or is a reusable script/utility.

## Testing Skills

Before deploying a skill, validate it works:

1. **Baseline:** Run a scenario WITHOUT the skill — document what the agent does wrong
2. **With skill:** Run the same scenario WITH the skill — verify the agent now complies
3. **Edge cases:** Try pressure scenarios where the agent might rationalize skipping the skill
4. **Close loopholes:** If the agent finds workarounds, add explicit counters

Different skill types need different test approaches:
- **Discipline skills** (rules/requirements): Test with pressure scenarios
- **Technique skills** (how-to): Test with application scenarios and edge cases
- **Pattern skills** (mental models): Test recognition and counter-examples
- **Reference skills** (docs): Test retrieval and correct application

## Anti-Patterns

- **Narrative style:** "In session 2025-10-03, we found..." — too specific, not reusable
- **Multi-language dilution:** examples in 5 languages — mediocre quality, maintenance burden
- **Code in flowcharts:** Can't copy-paste, hard to read
- **Generic labels:** "step1", "helper2" — labels should have semantic meaning
- **Untested skills:** If you didn't watch an agent fail without the skill, you don't know if it teaches the right thing

## Checklist for New Skills

- [ ] Name uses letters, numbers, hyphens only
- [ ] Clear overview with core principle in 1-2 sentences
- [ ] "When to Use" section with specific triggers/symptoms
- [ ] Keywords throughout for search discovery
- [ ] One excellent code example (if applicable)
- [ ] Quick reference table for scanning
- [ ] Common mistakes section
- [ ] Tested against baseline behavior
- [ ] No narrative storytelling
- [ ] Supporting files only for heavy reference or reusable tools
