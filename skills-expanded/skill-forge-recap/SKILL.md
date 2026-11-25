---
name: skill-forge-recap
description: "Read a skill's body and report what it actually does vs. what the description claims: drift, undeclared behaviors, verdict. After the recap, offers context-sensitive actions: fix frontmatter via HITL, hand off to skill-forge-update, or run skill-forge-judge. Use before updating a skill. Triggers: recap [skill], what does [skill] do, audit [skill] description, summarize [skill]."
---

# Skill Forge Recap
<!-- Pattern: Tool (structured audit output) -->

Audit a skill by reading its actual implementation and reporting what it *really* does — independent of what the description claims. The description is a claim; the body is the ground truth.

---

## What to Read

Use the path provided or resolved by the environment. Environment-level path overrides (e.g. CLAUDE.md remapping) take precedence over any default path.

If the file doesn't exist, report: "Skill not found — check name spelling" and stop. Do not search for alternatives.

Also read any `references/` files marked **MANDATORY READ** — behaviors that live outside the main body still count.

If a `references/` directory exists but no files are marked MANDATORY READ, include this note in **Undeclared behaviors**: "references/ directory present but no MANDATORY READ triggers — possible Pattern 3 (Orphan References)."

---

## What to Compare

The description makes four implicit claims. Check each against the body:

1. **WHAT it does** — does the body do this, or something adjacent?
2. **WHEN to use it** — do trigger phrases match actual entry conditions?
3. **Keywords** — do searchable terms reflect what the body covers?
4. **Scope** — does the description under- or over-state coverage?

Also scan for **undeclared behaviors**: things the body does that the description never mentions. Focus on the locations where iterative edits silently accumulate new behavior: NEVER rules, phases/steps, skip/exit conditions, reference-loading triggers, and confirmation loops.

**Before writing your verdict, ask:** *Would an agent picking skills from descriptions alone make the right call?* If the description would misroute the skill, that's Significant drift regardless of how small the wording gap appears.

---

## Output Format

```
## Recap: <skill-name>

**Description claims:** [one-line summary of what description promises]

**Body actually does:** [one-line summary derived independently from reading the body]

**Drift found:**
- [specific discrepancy]
(or "None found")

**Undeclared behaviors:**
- [behavior in body not mentioned in description]
(or "None found")

**Verdict:** Aligned / Minor drift / Significant drift
```

---

## Post-Recap Actions

After writing the recap block, classify the findings into two buckets:

- **Frontmatter drift**: discrepancies in the `name` or `description` fields
- **Body drift**: behavioral discrepancies or undeclared behaviors

If neither bucket has findings, output "No drift found." and stop — do not show the action menu.

Otherwise, show only the options relevant to what was found:

```
(f)ix frontmatter — HITL through corrected name/description fields  [only if frontmatter drift]
(u)pdate body     — hand off to skill-forge-update with drift loaded [only if body drift]
(j)udge           — run skill-forge-judge for quality scoring        [always]
```

If both frontmatter and body drift are detected, show all applicable options together.

### (f) Fix frontmatter

Produce a numbered findings list covering only the drifted fields, formatted for skill-forge-hitl. Each item must include the current value and the corrected value:

```
1. name: "<current>" → "<corrected>"
2. description: "<current>" → "<corrected>"
```

Include only fields where drift was found. Then invoke `/skill-forge-hitl` on that list.

### (u) Update body

Invoke `/skill-forge-update` and pass the recap output as pre-loaded context. State explicitly that Phase 0 is already complete so skill-forge-update skips directly to Phase 1 change elicitation.

### (j) Judge

Invoke `/skill-forge-judge` on the recapped skill. This is always available — continuous refinement applies even when no drift was detected.

---

## Verdict Criteria

**Minor drift**: Description is imprecise but not misleading. The skill would still be selected for the right task.

**Significant drift**: Description would cause the skill to be selected for the wrong task, OR the agent would miss a key behavior because the description omits it.

An *incomplete* description (missing behaviors) differs from a *wrong* description (claiming behaviors that don't exist). Flag both, label them separately.

---

## NEVER

- **NEVER start your "body actually does" summary by paraphrasing the description**
  **Instead:** Read the body first, form an independent summary, then compare to the description.
  **Why:** Starting from the description anchors you to its framing — you'll miss drift because your summary will match it by construction.

- **NEVER skip MANDATORY READ reference files**
  **Instead:** Load them before forming your assessment.
  **Why:** Key behaviors — NEVER rules, decision trees, phase logic — often live in references, not the main body.

- **NEVER mark a description as "wrong" when it's merely "incomplete"**
  **Instead:** Label each discrepancy explicitly: *incomplete* (body has behaviors the description omits) vs. *wrong* (description claims behaviors the body doesn't have).
  **Why:** The remediation differs — incomplete descriptions need additions; wrong descriptions need corrections or removal. Conflating them produces vague, unactionable findings.

- **NEVER use Glob to discover `references/` files**
  **Instead:** Run `Bash ls <skill-path>/references/` to check whether the directory exists and what files it contains.
  **Why:** Glob does not reliably find files in skill subdirectories and produces a silent false negative — causing an incorrect "references missing" verdict when the files are actually present.
