---
name: verification
version: 1.0.0
description: Check outputs against defined criteria to confirm correctness, completeness, and quality
uses: []
requires:
  tools: []
  env: []
security:
  risk_level: read
  capabilities:
    - verification:execute
  requires_approval: false
---

# Verification

Check outputs against defined criteria to confirm correctness, completeness, and quality before delivery or further processing.

## Execution Model

This is an **agent-handled skill** (`handler: type: agent`). When `verify` is invoked, you (the agent) systematically evaluate the subject against provided criteria using your reasoning capabilities. There is no backing code — you follow these instructions directly. The tool schema in tool.yaml defines the external contract; this document guides how you fulfill it. An orchestrator may route this skill to any agent that has `validation/verification` in its skill list.

## When to Use

- Checking whether a deliverable meets its acceptance criteria before release
- Validating that a plan, analysis, or report is complete and correct
- Confirming outputs from another agent or skill meet quality standards
- Performing a pre-flight check before executing a high-impact action
- Reviewing generated content against requirements before publishing
- Auditing a process output for compliance with rules or constraints

## Methodology

### 1. Define What to Verify

Clarify the verification target and scope:
- **Subject**: What exactly is being verified? (a document, a plan, a code change, an analysis, an output)
- **Source criteria**: Where do the acceptance criteria come from? (requirements doc, task description, quality checklist, specification, standards)
- **Verification type**: What kind of check is needed? (see types below)

### 2. Select Verification Type

Choose the appropriate verification approach:

| Type | What It Checks | When to Use |
|------|---------------|-------------|
| **Completeness** | All required elements are present | Checklists, deliverable reviews |
| **Correctness** | Facts, logic, and calculations are accurate | Analysis outputs, data reports |
| **Consistency** | No internal contradictions | Multi-section documents, plans with dependencies |
| **Conformance** | Meets format, style, or regulatory requirements | Compliance reviews, template adherence |
| **Criteria-match** | Output satisfies specific acceptance criteria | Task completion, requirement validation |

Multiple types can be applied to a single subject.

### 3. Build a Verification Checklist

Before evaluating, construct an explicit checklist from the criteria:
- Convert vague requirements into checkable items ("high quality" → "no factual errors, all claims cited, appropriate tone for audience")
- Each item must be binary: pass or fail (not "mostly good")
- Group items by verification type
- Include both positive checks ("X is present") and negative checks ("Y is absent")

### 4. Evaluate Systematically

Work through the checklist item by item:
- For each item, state the finding with evidence
- **Pass**: Criterion is met — cite the specific evidence
- **Fail**: Criterion is not met — describe what's wrong and what's expected
- **Partial**: Criterion is partially met — describe what's present and what's missing
- Do NOT skip items or batch them — each gets individual evaluation

### 5. Assess Overall Verdict

After evaluating all items:
- **Pass**: All items pass. Subject meets criteria.
- **Fail**: One or more critical items fail. Subject does not meet criteria.
- **Conditional Pass**: Non-critical items fail. Subject meets criteria with noted exceptions.
- Count: X of Y items pass, Z items fail, W items partial

### 6. Provide Actionable Feedback

For each failed or partial item:
- **What's wrong**: Specific description of the gap
- **Where**: Exact location in the subject (section, line, field)
- **How to fix**: Concrete suggestion for remediation
- **Severity**: Critical (blocks delivery) / Major (should fix) / Minor (nice to fix)

## Output Format

```
## Verification: [Subject]

### Criteria Source
[Where the criteria came from]

### Verification Type
[Completeness / Correctness / Consistency / Conformance / Criteria-match]

### Checklist Results

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | [Criterion] | Pass | [Evidence] |
| 2 | [Criterion] | Fail | [What's wrong] |
| 3 | [Criterion] | Partial | [What's present / missing] |

### Verdict: [Pass / Fail / Conditional Pass]
[X of Y passed, Z failed, W partial]

### Failures
1. **[Criterion]** — Severity: [Critical/Major/Minor]
   - Problem: [What's wrong]
   - Location: [Where in the subject]
   - Fix: [How to remediate]

### Summary
[One-paragraph assessment of overall quality]
```

## Quality Criteria

- Every criterion is evaluated individually with evidence
- No items are skipped or batched
- Failed items have specific, actionable remediation suggestions
- Severity is assigned to each failure
- Verdict accurately reflects the checklist results
- Feedback is objective, not opinion-based
- Location is specific enough to find the issue

## Common Mistakes

- **Vague criteria**: "Is it good?" is not verifiable. Convert to specific, checkable items before evaluating.
- **Rubber-stamping**: Marking everything as "pass" without evidence. Each pass needs a citation.
- **Missing the forest for the trees**: Passing all checklist items but missing a fundamental flaw not in the checklist. Always do a holistic assessment after the checklist.
- **Conflating severity levels**: Not every failure is critical. A typo is minor; a wrong calculation is critical. Severity guides remediation priority.
- **Skipping negative checks**: Only checking "is X present?" without checking "is Y absent?" (e.g., checking that sources are cited but not checking for unsupported claims).
- **Evaluating against unstated criteria**: Only verify against criteria that were defined, not against personal preferences.
- **No remediation guidance**: Saying "this fails" without saying how to fix it is unhelpful. Every failure needs a concrete fix suggestion.

## Completion

Verification is complete when:
- All criteria are converted into a checkable checklist
- Every checklist item is individually evaluated with evidence
- A clear verdict is rendered (pass / fail / conditional pass)
- All failures have severity, location, and remediation suggestions
- A holistic assessment confirms the checklist didn't miss anything fundamental
