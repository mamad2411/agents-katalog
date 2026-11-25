---
name: workflow-improve-skill
description: "Analyze, score, and improve existing SKILL.md files using parallel audit agents and a weighted quality rubric. Use when a skill needs improvement, quality assessment, or maintenance. Triggers on 'improve this skill', 'audit skill quality', 'score this skill', 'upgrade skill', 'fix this skill'."
alwaysAllow: ["Task", "Read", "Glob", "Grep", "Edit", "Write"]
---

# Improve Skill: Parallel Audit + Weighted Scoring

<objective>
Analyze, score, and improve an existing skill using 6 parallel audit agents and a 7-criterion weighted quality rubric. Produces a baseline score, prioritized improvement plan, executes approved changes, and re-scores to measure improvement.
</objective>

<essential_principles>

1. **Measure before and after.** Every improvement session starts with a baseline score and ends with a comparison table. No unmeasured changes.

2. **Parallel agents, independent lenses.** Six agents run simultaneously, each with a single focus area. They review independently — conflicts between agents are signal, not noise.

3. **Severity drives priority.** Critical findings first, Important second, Minor last. Within the same severity, prefer high-impact/low-effort improvements.

4. **Approval before action.** Never apply changes without user consent. The 4-option gate (apply all / by severity / review each / report only) is mandatory.

5. **Verify after every edit.** Read back modified sections. Check cross-file references still resolve. Broken edits are worse than no edits.

6. **Don't invent — improve.** Fix what's wrong, don't add speculative features. Preserve the skill's voice and intent.

</essential_principles>

## Process

### Phase 1: Target Discovery & Baseline

1. Parse argument: skill name, path, or enumerate `~/.claude/skills/` for selection
2. Read complete skill structure (SKILL.md + references/ + workflows/ + scripts/ + assets/)
3. Count baseline lines per file
4. Record full content for before/after comparison

### Phase 2: Parallel Audit (6 Agents)

Launch all simultaneously:

| Agent | Focus | Key Checks |
|-------|-------|------------|
| Structure Auditor | YAML frontmatter, file organization | Valid name/description, under 500 lines, references exist |
| Content Quality Reviewer | Clarity, actionability, specificity | Concrete steps, real examples, verifiable criteria |
| Freshness Verifier | External claims accuracy | Categorize dependency type, WebSearch for changes, flag deprecated |
| Progressive Disclosure Analyst | Information architecture | SKILL.md as router, knowledge in references, procedures in workflows |
| Gap Analyst | Missing content | Setup, config, error handling, testing, examples, integration |
| Ecosystem Consistency Reviewer | Skill ecosystem fit | Naming, description style, cross-skill chains, no duplicates |

Each agent returns findings with **severity** (Critical/Important/Minor), **quotes**, and **suggested fixes**.

### Phase 3: Score Synthesis

<required_reading>
Read `references/quality-rubric.md` for the full 7-criterion rubric with scoring levels.
</required_reading>

Map agent findings to the 7-criterion weighted rubric:

| Criterion | Weight | Primary Agent | Supporting |
|-----------|--------|--------------|------------|
| Structure & Conformance | 15 pts | Structure Auditor | Progressive Disclosure |
| Description Quality | 10 pts | Structure Auditor | Ecosystem Consistency |
| Content Accuracy & Freshness | 20 pts | Freshness Verifier | Gap Analyst |
| Actionability | 20 pts | Content Quality | Gap Analyst |
| Progressive Disclosure | 15 pts | Progressive Disclosure | Structure Auditor |
| Examples & Patterns | 10 pts | Content Quality | Gap Analyst |
| Conciseness | 10 pts | Content Quality | Progressive Disclosure |

**Grade scale:** A (90-100), B (70-89), C (50-69), D (30-49), F (0-29)

Output: Quality report with score, grade, strengths, and findings by severity.

### Phase 4: Improvement Plan

<required_reading>
Read `references/improvement-categories.md` for the 8 improvement categories and severity mapping.
</required_reading>

Convert findings to prioritized improvement actions:
- Each action: what to change, which file, before/after text, expected score impact, effort (S/M/L)
- Grouped: Critical → Important → Minor
- Within group: highest impact first

### Phase 5: Approval Gate

4 options:
1. **Apply all** — Execute all improvements
2. **Apply by severity** — Critical first, confirm for Important, then Minor
3. **Review each** — Before/after diff per improvement, approve individually
4. **Report only** — No changes

**Wait for user response. Do not proceed without approval.**

### Phase 6: Execute Improvements

For each approved improvement:
1. Show before/after diff
2. Apply using Edit tool
3. Read back to verify edit applied correctly
4. Cross-file consistency check (all references resolve, no duplicates)

### Phase 7: Verification & Before/After

Re-score using the same rubric. Present comparison table:

```markdown
| Criterion | Before | After | Change |
|-----------|--------|-------|--------|
| Structure & Conformance | X/15 | Y/15 | +Z |
| ... | ... | ... | ... |
| **Total** | **XX/100** | **YY/100** | **+ZZ** |
```

### Phase 8: Next Steps

Route to:
- `/workflows:improve-skill [name]` — improve another skill
- `/heal-skill` — targeted fix
- `/workflows:compound` — document learnings
- Commit changes

## Scoring Overview

7 criteria, 100 points total. See `references/quality-rubric.md` for the full rubric with 4 scoring levels per criterion.

**Quick reference:**

| Criterion | Max | What it measures |
|-----------|-----|-----------------|
| Structure & Conformance | 15 | Frontmatter, file organization, required sections |
| Description Quality | 10 | Trigger phrases, what + when, third person |
| Content Accuracy & Freshness | 20 | External claims still true, no deprecated patterns |
| Actionability | 20 | Concrete steps, copy-paste commands, real paths |
| Progressive Disclosure | 15 | SKILL.md as router, proper content separation |
| Examples & Patterns | 10 | Realistic examples, common use cases, error handling |
| Conciseness | 10 | No filler, no redundancy, each line adds value |

## Anti-Patterns

- **Scoring without reading**: Always read the full skill before launching agents
- **Sequential agents**: All 6 must run in parallel
- **Applying without approval**: Phase 5 is a hard gate, never skip it
- **Ignoring cross-file references**: After edits, verify all references still resolve
- **Over-improving**: Fix what's wrong, don't rewrite the entire skill
- **Inventing content**: Improvements should address real findings, not add speculation
- **Skipping re-score**: The before/after comparison is the primary deliverable

## Next Step

When improvements are complete, document what you learned: **`/workflows:compound`**
