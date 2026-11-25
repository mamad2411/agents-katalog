---
name: assess-skill
description: >
  Evaluates an existing SKILL.md against the full set of structural patterns,
  research-grounded quality dimensions, and anti-patterns established in the
  Writing Good Skills course. Use when a skill is written and needs a quality
  review before deployment. Do NOT use when writing a skill from scratch — see
  write-skill for that.
---

# Assess Skill

## Prerequisites

- A complete or draft SKILL.md to evaluate (paste inline or provide path)
- If assessing a skill package, also note any companion files present (EXAMPLES.md, resources/, etc.)

## Instructions

### Stage 1 — Read Before Judging

1. Read the entire SKILL.md once without commenting. Understand what the skill is trying to do before evaluating whether it does it well.
2. Identify the domain and the intended trigger moment. Hold both in mind throughout the assessment.

### Stage 2 — Frontmatter Assessment

3. Check the `name` field: must be `action-noun` format, lowercase, hyphens only. Flag: CamelCase, underscores, noun-only names (e.g. `testing`), verb-only names (e.g. `review`).
4. Check the `description` field against the trigger contract formula: `[what it does] + [when to use] + [when NOT to use]`. Flag any of the three that are missing.
5. Check description voice: must be third person. Flag any "I", "you", or "we".
6. Check description specificity: strip the skill name and ask — does this description uniquely identify what the skill does? Could it be copy-pasted onto a neighbor skill without changing meaning? If yes, flag as non-retrievable. (Source: *Skills in the Wild*, arXiv 2604.04323 — vague descriptions collapse retrieval from 55.4% to 19.8%.)
7. Check description length: flag if over 3 sentences. The description is injected as a system prompt fragment — it must be dense, not long.

### Stage 3 — Structural Completeness

8. Verify the Instructions section exists and is non-empty.
9. Verify at least one of: Anti-Patterns, Gotchas, or Verify section is present. Flag skills with Instructions only as incomplete.
10. Check total line count. Flag if over 500 lines. If over 500, identify which section is causing the overflow and recommend either moving content to a `references/` file or splitting the skill. (Source: SkillsBench, arXiv 2602.12670 — focused 2–3 module skills outperform comprehensive documentation.)
11. Check if an Examples section or EXAMPLES.md is present. Note its absence as a recommendation, not a blocking issue.

### Stage 4 — Directive Quality

12. Read each sentence in the Instructions section. Apply the three directive tests:
    - **Imperative test:** Does it start with a command verb? Flag sentences starting with "It's important", "Consider", "Remember", "You should", "Think about".
    - **Observable test:** Can someone verify from the output whether this directive was followed? Flag directives with unmeasurable terms: "appropriately", "correctly", "carefully", "well", "good", "clean".
    - **Domain-specific test:** Could this sentence appear unchanged in a skill for a completely different domain? If yes, flag it as general knowledge that wastes context. (Source: Hamelsmu meta-skill — "Cut general knowledge. Only include domain-specific procedures agents wouldn't know.")
13. For each flagged directive, write a one-line rewrite that passes all three tests.

### Stage 5 — Anti-Patterns and Gotchas Quality

14. Check if Anti-Patterns are one-liners. Flag any anti-pattern that spans more than one line — it should be a scannable signal, not an explanation.
15. Check if Gotchas contain domain-specific failure modes — things a practitioner would only know from experience. Flag generic entries like "be careful with edge cases" or "some inputs may behave unexpectedly". (Source: ACE, ICLR 2026 — brevity bias compresses domain-specific heuristics into generic warnings, collapsing skill effectiveness.)
16. Count the Anti-Patterns. If fewer than 3, flag: a skill that can't name 3 things not to do may be under-specified or too narrow.

### Stage 6 — Scope Assessment

17. Identify whether the skill owns exactly one concern. Look for compound verbs in the description ("reviews and refactors", "writes and tests", "designs and implements") — each compound is a scope violation.
18. Name the natural neighbor skills — adjacent concerns this skill does NOT cover. Verify they are excluded in the description or in an Exclusion Conditions section. (Source: *Skills in the Wild* — missing exclusion conditions cause skills to fire in neighbor territory.)
19. Apply the independence test: could this skill's output be verified without running any other skill? If no, the skill likely has scope entanglement — it depends on state that another skill is responsible for. (Source: *Atomic Skills*, arXiv 2604.05013 — independence is a required property of correctly scoped skills.)

### Stage 7 — Verification Quality

20. Locate the Verify section. Flag its absence as a blocking issue.
21. Check each verify item: is it observable from the output, or is it a judgment call? Flag items like "output is clear" or "code looks right". Require items like "all three paths return typed errors" or "line count < 30".
22. Check whether the verify items collectively confirm the skill's stated purpose — not just that something was done, but that it was done correctly.

### Stage 8 — Research Quality Gate (SkillNet 5 Dimensions)

Evaluate against the five quality dimensions from SkillNet (arXiv 2603.04448):

23. **Safety:** Does any instruction risk a destructive, irreversible, or harmful action without a guard? Flag unchecked destructive operations (file deletion, database mutations, API calls with side effects).
24. **Completeness:** Are all steps needed to complete the task present, or does the agent have to fill gaps? Flag missing steps that require domain knowledge not in the skill.
25. **Executability:** Can the skill run as-is? Flag broken references to files, tools, or setup steps not defined in Prerequisites. This is the most commonly missed dimension.
26. **Maintainability:** Is the structure clear enough that one section could be updated without reworking the whole skill? Flag skills with no section headers — flat unstructured instruction blocks are unmaintainable.
27. **Cost-awareness:** Is the scope proportionate to the task? Flag if the skill requires loading large reference files, running expensive operations, or activating for tasks a simpler approach would handle.

### Stage 9 — Produce the Assessment Report

28. Produce the report in this exact structure:

```
## Skill Assessment: [skill-name]

### Summary
[2-sentence verdict: what the skill does well and the single most important fix]

### Blocking Issues (must fix before deployment)
[Numbered list. Each item: what the problem is + one-line rewrite or fix]

### Recommendations (improve before deployment)
[Numbered list. Same format]

### Observations (optional improvements)
[Bulleted list. Lower-priority notes]

### Scores
| Dimension         | Score (0–2) | Note |
|-------------------|-------------|------|
| Description quality | | |
| Directive quality   | | |
| Scope discipline    | | |
| Gotchas specificity | | |
| Verify completeness | | |
| Executability       | | |

**Overall:** [total]/12 — [Ready to ship / One revision needed / Major revision needed]
```

29. Score each dimension: 0 = failing, 1 = partial, 2 = passes. Overall 10–12 = ship, 7–9 = one revision, < 7 = major revision.
30. For every blocking issue, write the fix — not just the diagnosis. The report should be actionable without requiring the author to re-read course materials.

## Anti-Patterns

❌ Reporting "good" or "needs improvement" without naming the specific line or section  
❌ Flagging style preferences as blocking issues — only block on patterns with research or observability evidence  
❌ Skipping Stage 1 (reading first) — assessments written before understanding the skill's intent produce false positives  
❌ Flagging the description for being "too short" — short descriptions that are specific are correct; long descriptions that are vague are wrong  
❌ Treating missing Examples as a blocking issue — it is a recommendation, not a requirement  
❌ Rewriting directives into wisdom during Stage 4 ("Flag X" → "It's important to flag X")

## Gotchas

- A description that passes the formula check (what + when + not when) can still fail the retrieval test — verify specificity separately from structure
- Skills with compound concerns often have compliant-looking descriptions that bury the second concern in a clause ("reviews code and suggests refactors") — read slowly
- The independence test (Stage 6, step 19) catches scope entanglement that the 500-line ceiling misses — a skill can be short and still be entangled
- Executability failures are often invisible to the skill author because they know the environment — read Prerequisites as a first-time user who has only this file
- Brevity bias: if the Gotchas section looks generic after your assessment, you may have fallen into the same trap you're assessing for — name the specific failure modes you found

## Verify

- [ ] Assessment report includes Summary, Blocking Issues, Recommendations, Observations, and Scores sections
- [ ] Every blocking issue has a specific fix or rewrite, not just a diagnosis
- [ ] Scores are calibrated: a skill with 0 blocking issues scores ≥ 8/12
- [ ] The retrieval test (Stage 2, step 6) was applied to the description, not just the formula check
- [ ] At least one research citation was used to justify a blocking issue (prevents the assessment from being opinion-based)
