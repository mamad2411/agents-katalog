# Branch Delta Review — Prompt Template

You are performing a structured code review. Follow the instructions below precisely.

## Context Loading

Before reviewing, load and internalize the following:

1. **Review Policy**: `shared/review-policy.md`
   - Severity levels (CRITICAL, HIGH, MEDIUM, LOW, INFO)
   - Required checks (correctness, security, architecture, testing)
   - Output format requirements
   - Approval criteria

2. **Architecture Rules**: `shared/architecture-rules.md`
   - Layered architecture constraints
   - Portability rules (P-1, P-2, P-3)
   - Security rules (S-1, S-2, S-3)
   - Simplicity rules (K-1, K-2, K-3)

3. **Jira Issue** (if provided): `{{JIRA_ISSUE}}`
   - Use this to understand the intended behavior
   - Flag any divergence between the issue requirements and the implementation

## Branch Information

- **Base branch**: `{{BASE_BRANCH}}`
- **Feature branch**: `{{FEATURE_BRANCH}}`
- **Changed files**:
```
{{CHANGED_FILES}}
```

## Diff to Review

```diff
{{BRANCH_DIFF}}
```

## Review Instructions

Analyze the diff above and produce a structured review.

### Step 1: Understand Intent
Read the diff and form a mental model of what this branch is trying to accomplish.
If a Jira issue is provided, cross-reference the implementation against requirements.

### Step 2: Check Correctness
For each changed file, ask:
- Are edge cases handled? (null, empty, overflow, off-by-one)
- Are error paths handled and propagated?
- Is async/concurrent code safe?
- Does the logic match the intent?

### Step 3: Check Security
- Are there hardcoded secrets or tokens?
- Is user input validated and sanitized before use?
- Are there injection vectors (SQL, command, XSS)?
- Are authentication or authorization checks bypassed?

### Step 4: Check Architecture
Apply the rules from `shared/architecture-rules.md`:
- Does the code respect layer boundaries?
- Are portability rules (P-1, P-2, P-3) followed?
- Are security rules (S-1, S-2, S-3) followed?
- Are simplicity rules (K-1, K-2, K-3) followed?

### Step 5: Check Testing
- Does new behavior have test coverage?
- Do existing tests still cover the changed behavior?
- Are tests testing behavior, not implementation details?

### Step 6: Identify Risky Changes
Flag any changes that, even if correct, introduce risk:
- Large surface area changes
- Changes to authentication or authorization
- Changes to data storage or migration
- Changes that affect multiple unrelated systems

## Output

Produce the review in this exact format:

---

## Summary

[One paragraph describing what the branch does and your overall impression]

## Bug Findings

<!-- Use this format for each finding: -->
<!-- - [SEVERITY] `file.ext:LINE` — description -->
<!--   Suggestion: how to fix it -->

[List findings here, or write "None found." if no bugs are identified]

## Architecture Concerns

<!-- Use this format for each concern: -->
<!-- - [SEVERITY] description -->
<!--   Reference: architecture-rules.md#rule-id -->

[List concerns here, or write "None found." if no violations are identified]

## Risky Changes

<!-- Use this format for each risk: -->
<!-- - [SEVERITY] description -->
<!--   Risk: what could go wrong -->
<!--   Mitigation: suggested action -->

[List risks here, or write "None found." if no risks are identified]

## Recommendation

**[APPROVE | REQUEST_CHANGES | NEEDS_DISCUSSION]**

Rationale: [One sentence explaining the recommendation]

---
