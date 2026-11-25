---
name: skill-forge-judge
description: "Evaluate any LLM prompt (SKILL.md, CLAUDE.md, system prompts, bash guidance) for quality: grouped dimensional scoring with letter grade and step-through-ready numbered improvements list. Triggers: judge/review/audit/score/evaluate this skill or prompt."
compatibility: Claude Code
---

# Skill Forge Judge

Evaluate any LLM-consumed prompt against quality standards, focused on knowledge delta, instruction clarity, and practical usability.

---

## Core Philosophy

> **Good Prompt = Expert-only Knowledge − What Claude Already Knows**

Restating defaults is token waste.

### Three Types of Knowledge

| Type | Definition | Treatment |
|------|------------|-----------|
| **Expert** | Claude genuinely doesn't know this | Must keep — this is the value |
| **Activation** | Claude knows but may not think of | Keep if brief — serves as reminder |
| **Redundant** | Claude definitely knows this | Delete — wastes tokens |

Good prompt: >70% Expert, <20% Activation, <10% Redundant.


## Evaluation Dimensions

Dimensions are grouped. Universal dimensions always apply. Type-specific modules apply based on what the prompt is. Multiple groups can apply to a single prompt.

**Final grade = total score / total applicable points (as %)**

| Grade | % | Meaning |
|-------|---|---------|
| A | 90%+ | Excellent — production-ready |
| B | 80–89% | Good — minor improvements needed |
| C | 70–79% | Adequate — clear improvement path |
| D | 60–69% | Below average — significant issues |
| F | <60% | Poor — needs fundamental redesign |

### Group U: Universal (80 pts) — always scored

**MANDATORY — READ [`references/universal-dimensions.md`](references/universal-dimensions.md)**

| ID | Dimension | Pts |
|----|-----------|-----|
| U1 | Knowledge/Instruction Delta | 20 |
| U2 | Mindset + Procedures | 15 |
| U3 | Anti-Pattern Quality | 15 |
| U4 | Freedom Calibration | 15 |
| U5 | Practical Usability | 15 |

### Group S: Skill Module (40 pts) — SKILL.md targets only

**MANDATORY — READ [`references/skill-dimensions.md`](references/skill-dimensions.md)**

| ID | Dimension | Pts |
|----|-----------|-----|
| S1 | Specification Compliance | 15 |
| S2 | Progressive Disclosure | 15 |
| S3 | Pattern Recognition | 10 |

### Group C: CLAUDE.md / System Prompt Module (40 pts) — prompts that govern LLM behavior settings

**MANDATORY — READ [`references/claude-md-dimensions.md`](references/claude-md-dimensions.md)**

| ID | Dimension | Pts |
|----|-----------|-----|
| C1 | Behavioral Clarity | 15 |
| C2 | Scope Definition | 15 |
| C3 | Structural Organization | 10 |

### Group B: Bash/Shell Module (30 pts) — prompts that contain shell/CLI guidance

**MANDATORY — READ [`references/bash-dimensions.md`](references/bash-dimensions.md)**

| ID | Dimension | Pts |
|----|-----------|-----|
| B1 | Rule Specificity & WHY | 10 |
| B2 | Anti-Pattern Coverage | 10 |
| B3 | Scope & Exceptions | 10 |

---

## Evaluation Protocol

> **Evaluator's Lens:** Before reading the target, adopt this question: "Does Claude already know this?" — every section gets marked [E], [A], or [R] before scoring begins.

### Step 0: Detect Prompt Type

Read the target and identify which groups apply:

```
[ ] Is it a SKILL.md file?              → Score U + S. Do NOT load claude-md-dimensions.md or bash-dimensions.md.
                                          MANDATORY: Load agentskills spec via Spec Cache (below) before scoring S1.
[ ] Is it a CLAUDE.md / system prompt?  → Score U + C. Do NOT load skill-dimensions.md.
[ ] Does it contain bash/shell rules?   → Also score B. Load bash-dimensions.md.
[ ] Is it something else?               → Score U only. Do NOT load any type-specific reference.
```

Multiple groups can apply (e.g. a CLAUDE.md with bash guidance → U + C + B).

**Edge cases**:
- SKILL.md that also contains bash guidance → U + S + B
- A referenced sub-file (e.g. `references/bash.md`, not a root prompt) → U only; note "sub-file, not root prompt" in report
- Ambiguous type (could be CLAUDE.md or skill) → score both C and S groups; note the ambiguity in the Summary

### Spec Cache

The agentskills.io specification is cached daily so evaluations don't pay a network fetch on every run.

```
Cache dir:  ~/.claude/tmp/
Filename:   agentskills-spec-YYYY-MM-DD.md   (today's date, e.g. agentskills-spec-2026-04-14.md)

1. Glob ~/.claude/tmp/agentskills-spec-<today>.md
2. If found  → Read it — done.
3. If not    → Bash: mkdir -p ~/.claude/tmp
               WebFetch https://agentskills.io/specification
               If WebFetch fails → score S1 from training knowledge; note "spec unavailable" in S1 Notes cell — done.
               Write result to ~/.claude/tmp/agentskills-spec-<today>.md
               Read the file — done.
```

Only fetch when the target is a SKILL.md (S1 scoring). Skip entirely for CLAUDE.md / system prompt / other evaluations.

### Step 1: First Pass — Knowledge Delta Scan

Read completely. Mark each section **[E] Expert** | **[A] Activation** | **[R] Redundant**. Calculate E:A:R ratio — target >70% Expert.

### Step 2: Structure Analysis

Note prompt type(s), applicable groups, length, reference files, and loading/trigger mechanisms.

### Step 3: Score Each Applicable Dimension

Before opening the rubric, ask: what does this section assume Claude doesn't already know?

Load the reference file for each applicable group. For each dimension: find specific evidence, assign score with one-line justification, note improvements if score < max.

If a reference file cannot be read, halt and report: `[ERROR] Cannot score Group X — reference file not found: <path>`. Do not proceed with that group.

### Step 4: Calculate Score & Grade

`Grade = (sum of scored dimensions) / (sum of applicable maxes)` → apply grade scale.

### Step 5: Generate Report

```markdown
# Prompt Evaluation Report: [Name]

## Executive Summary
[1–2 sentences max. Overall verdict + one top strength or weakness. No scores, no tables, no lists — prose only.]

## Summary
- **Type**: [Skill / CLAUDE.md / System Prompt / Other] + applicable groups
- **Score**: X / Y (Z%)
- **Grade**: [A/B/C/D/F]
- **Knowledge Ratio**: Expert:Activation:Redundant = X:Y:Z
- **Verdict**: [One sentence assessment]

## Group Scores

| Group | Score | Max | % |
|-------|-------|-----|---|
| U: Universal | | 80 | |
| S: Skill | | 40 | | ← if applicable
| C: CLAUDE.md | | 40 | | ← if applicable
| B: Bash/Shell | | 30 | | ← if applicable
| **Total** | | | |

## Dimension Scores

Include only rows for groups detected in Step 0. Omit rows for groups that don't apply.

| ID | Dimension | Score | Max | Notes |
|----|-----------|-------|-----|-------|
| U1 | Knowledge/Instruction Delta | | 20 | One-line justification + primary gap if score < max |
| U2 | Mindset + Procedures | | 15 | One-line justification + primary gap if score < max |
| U3 | Anti-Pattern Quality | | 15 | One-line justification + primary gap if score < max |
| U4 | Freedom Calibration | | 15 | One-line justification + primary gap if score < max |
| U5 | Practical Usability | | 15 | One-line justification + primary gap if score < max |
| S1 | Specification Compliance | | 15 | One-line justification + primary gap if score < max |
| S2 | Progressive Disclosure | | 15 | One-line justification + primary gap if score < max |
| S3 | Pattern Recognition | | 10 | One-line justification + primary gap if score < max |
| C1 | Behavioral Clarity | | 15 | One-line justification + primary gap if score < max |
| C2 | Scope Definition | | 15 | One-line justification + primary gap if score < max |
| C3 | Structural Organization | | 10 | One-line justification + primary gap if score < max |
| B1 | Rule Specificity & WHY | | 10 | One-line justification + primary gap if score < max |
| B2 | Anti-Pattern Coverage | | 10 | One-line justification + primary gap if score < max |
| B3 | Scope & Exceptions | | 10 | One-line justification + primary gap if score < max |

## Critical Issues
[Must-fix problems that significantly impact effectiveness]

## Detailed Analysis
[For each dimension scoring below 80%, provide:
- What's missing or problematic
- Specific evidence with line numbers
- Concrete suggestions for improvement]

## Numbered Improvements
1. [Highest impact improvement with specific guidance]
2. [Second priority]
3. ...

(skill-forge-hitl-compatible — invoke /skill-forge-hitl to step through each item.)
```

---

## Common Failure Patterns

**MANDATORY — READ [`references/failure-patterns.md`](references/failure-patterns.md)**

---

## Extending skill-forge-judge

To add a new evaluation group, **MANDATORY — READ [`references/extending-groups.md`](references/extending-groups.md)** before proposing any new group. Do NOT load this file during a normal evaluation run.

---

## Self-Application

skill-forge-judge can and should evaluate itself. The criteria must be self-consistent — if skill-forge-judge can't score well against its own rubric, the rubric is wrong.

**Applicable groups**: skill-forge-judge is a SKILL.md with no bash guidance → U + S (120 pts max).

**Expected score**: ≥B (80%+, ≥96/120). A score below B indicates the rubric has drifted from its own standards and the lowest-scoring dimensions should be revisited. A score of A (90%+) on self-evaluation is a warning sign — it may mean the criteria were written to fit the evaluator rather than the other way around.

**Known limitation**: self-evaluation can be gamed by writing criteria the evaluator happens to satisfy. When evaluating skill-forge-judge itself, pay extra attention to whether dimensions capture genuine expert knowledge vs. formalizing what any thoughtful evaluator would do anyway.

---

## NEVER Do When Evaluating

- **NEVER** give high scores just because it "looks professional" or is well-formatted — formatting is cheap; rewarding it masks content gaps and trains authors to polish instead of improve
  **INSTEAD:** Score content for expert knowledge density, not visual polish.
- **NEVER** ignore token waste — redundant content dilutes expert signal and teaches authors that padding is acceptable; deduct consistently to create the right incentive
  **INSTEAD:** Deduct from U1 consistently regardless of overall quality; note the specific redundant lines.
- **NEVER** let length impress you — a 500-line prompt with 80% activation content is worse than a 50-line one with pure expert knowledge; length is effort, not value
  **INSTEAD:** Measure the Expert:Activation:Redundant ratio; a short high-Expert prompt outscores a long Activation-heavy one.
- **NEVER** skip mentally testing decision trees — plausible-looking trees often have unreachable branches or missing cases that only surface when traced
  **INSTEAD:** Trace each branch to verify it terminates with a clear action; flag any branch that dead-ends or loops.
- **NEVER** forgive explaining basics with "but it provides helpful context" — it sets a precedent that activation content earns tokens; future versions accumulate more
  **INSTEAD:** Mark the section [R] and deduct from U1; note the specific lines in Detailed Analysis.
- **NEVER** overlook missing anti-patterns — absence of a NEVER list usually means the author hasn't hit the failure modes yet, not that they don't exist
  **INSTEAD:** Note "NEVER list absent" as a Critical Issue and deduct from U3.
- **NEVER** assume all procedures are valuable — generic procedures (open, edit, save) inflate U2 scores without adding knowledge delta
  **INSTEAD:** Ask "would Claude follow this procedure without being told?" — if yes, mark [A] or [R], not [E].
- **NEVER** undervalue the description field for Skills — it is the only thing the agent sees before deciding whether to load the skill; poor description = skill never activates regardless of content quality, making all other work invisible
  **INSTEAD:** Score S1 harshly for vague or keyword-poor descriptions; a skill that doesn't activate is a failed skill regardless of body quality.
- **NEVER** compare percentage scores across evaluations without checking which groups were scored — U+S (120 pts) and U+C+B (150 pts) are different denominators; the percentages are comparable, the raw scores are not
  **INSTEAD:** Always note the denominator in the report (e.g., "89% on U+S = 107/120") so cross-evaluation comparisons are valid.
- **NEVER** place Numbered Improvements before Detailed Analysis — the reader needs context before recommendations; without it, improvements land without evidence and get dismissed or misapplied
  **INSTEAD:** Always write Detailed Analysis first, then Numbered Improvements immediately after.
