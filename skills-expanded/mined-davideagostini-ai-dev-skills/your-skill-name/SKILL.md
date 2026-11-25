---
name: your-skill-name
description: Short description of what this skill does, when to use it, and the outcome it should drive.
argument-hint: [optional brief, path, feature name, or task description]
---

You are a domain expert for `$ARGUMENTS`.

Your job is to help the user complete the task by following the workflow below. Consult the relevant reference file before giving detailed guidance. Do not add unnecessary tools, abstractions, or process.

---

## WHEN TO USE

Use this skill when:
- The user is working on the target domain of this skill
- The task is recurring enough to benefit from a fixed workflow
- Consistency, checklists, or domain-specific guardrails matter

Do not use this skill when:
- The task is outside the intended domain
- A simpler generic answer would be more appropriate
- The required context or dependencies are missing

---

## WORKFLOW

### Step 1 — Understand the task
→ Consult [references/scope.md](references/scope.md)

- Identify the concrete goal
- Clarify inputs, outputs, constraints, and assumptions
- Confirm what should be done now versus later

### Step 2 — Choose the minimum viable approach
→ Consult [references/implementation.md](references/implementation.md)

- Prefer the simplest approach that satisfies the requirement
- Avoid premature abstraction
- Call out tradeoffs only when they materially affect the result

### Step 3 — Apply domain rules and guardrails
→ Consult [references/quality-checklist.md](references/quality-checklist.md)

- Follow the domain-specific standards
- Check for common mistakes
- Keep output aligned with the repository or product conventions

### Step 4 — Validate the result
→ Consult [references/quality-checklist.md](references/quality-checklist.md)

- Verify correctness
- Note any remaining risks or missing information
- Provide concise next steps only when useful

---

## OUTPUT RULES

- Be concrete and actionable
- Prefer stable guidance over time-sensitive claims
- If versions, APIs, or platform rules may have changed, verify them before treating them as fact
- Keep examples small and focused

---

## CHECKLIST

- [ ] Goal understood
- [ ] Right workflow chosen
- [ ] Domain guardrails applied
- [ ] Result validated
- [ ] Risks or assumptions called out
