---
name: skill-linter
description: Optimize SKILL.md content — make language concise and accurate without changing thinking logic. Use when user asks to polish skill, improve skill writing, lint skill content, or review skill quality.
---

# Skill Linter

Optimize SKILL.md files. Two rules:
1. Language must be **concise and accurate**
2. **Never change the thinking logic**

---

## Principles

### Concise

- Remove filler: "This skill provides...", "You can use this skill to..."
- Remove redundant explanations that the AI already knows
- Use short sentences. One idea per line.
- Prefer verbs over noun phrases: "Check code" not "Perform code checking"

### Accurate

- Replace vague words with specifics: "lint errors" not "issues"
- Replace subjective words with measurable criteria: "0 warnings" not "good quality"
- Use action verbs, not passive: "Run tests" not "Tests should be run"

### Preserve Logic

- **Never remove** conditions, constraints, or decision trees
- **Never simplify** multi-step processes into fewer steps
- **Never merge** distinct rules that serve different purposes
- If unsure whether something is logic or fluff → keep it

---

## Bad → Good

| Bad | Good | Why |
|-----|------|-----|
| "This skill provides a way to check code quality" | "Check code quality" | Remove intro fluff |
| "When the user needs to, carefully review the code" | "Review code when asked" | Remove vague/subjective words |
| "The skill will output a list of issues found" | "Output issue list" | Remove redundant subject |
| "Helps developers write better code" | "Check code and output lint errors" | Specific, not subjective |
| "I recommend you should..." | Direct instruction | No first person |

---

## Process

1. Read the SKILL.md
2. Identify and mark thinking logic (conditions, rules, steps, decisions)
3. Rewrite non-logic sections for conciseness and accuracy
4. Show diff: original → optimized
5. Ask user to confirm before writing

---

## Output Format

```
SKILL LINT REPORT
===================
changes: X lines removed, Y lines rewritten

diff:
- "This skill provides a comprehensive way to help users..."
+ "Check code quality. Use when user asks for review."

logic preserved: ✅
```

---

## Anti-Patterns (what NOT to do)

| Anti-Pattern | Why |
|--------------|-----|
| Removing condition checks | Breaks logic |
| Merging separate rules | Loses specificity |
| Shortening multi-step flows | Changes execution order |
| Removing examples | Reduces clarity |
| Rewriting technical terms | May change meaning |
