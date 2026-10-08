# Sample Skill File — Code Review Workflow

This is a real example of a skill file.
Skills are instruction files that teach an AI agent how to perform a repeatable workflow.
Unlike rules (which are always on), a skill is invoked on demand when the student or tutor triggers it.

**How to invoke this skill:** "Run the code review skill on my Python file."

---

## Skill: Python Code Review

### Purpose
Review a Python file for quality, clarity, and correctness before it is submitted or shared.

### When to Use
- Before submitting any coding assignment
- Before running code that accesses external files or APIs
- After completing the TODO sections in a starter file

### Step-by-Step Procedure

**Step 1 — Read the file**
Read the full Python file from top to bottom without making any changes yet.

**Step 2 — Check for correctness**
Look for:
- Syntax errors (missing colons, unclosed brackets, wrong indentation)
- Logic errors (conditions that can never be true, variables used before they are set)
- Division by zero or index-out-of-range risks

**Step 3 — Check for clarity**
Look for:
- Variables with unclear names (e.g., `x`, `temp`, `data` with no context)
- Missing or unclear comments on non-obvious logic
- Functions that do more than one thing

**Step 4 — Check for completeness**
Look for:
- TODO comments that were not completed
- Missing edge cases (what if the list is empty? what if the user types a letter instead of a number?)

**Step 5 — Produce the review report**
Output a review with:
- One sentence summary of what the code does
- A list of issues found (label each: Error / Warning / Suggestion)
- A suggested improved version of any code with an Error

**Step 6 — Final sign-off**
If no errors are found, output: "Code review complete — ready to submit."
If errors are found, output: "Code review complete — fix errors before submitting."

---

## Activity Questions

1. How is this skill different from a rule? (Hint: is it always-on or triggered on demand?)
2. How is this skill different from a tool? (Hint: does it call an external system or just give instructions?)
3. Write a one-sentence summary of when you would create a new skill vs a new rule.
4. Design a second skill for your capstone project — give it a name and list the steps.
