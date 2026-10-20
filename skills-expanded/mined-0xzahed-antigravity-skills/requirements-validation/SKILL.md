---
name: requirements-validation
description: Validate that requirements are correct and aligned with business
  goals. Use before committing to a spec.
metadata:
  tags: requirements, validation
---

# Requirements Validation

## Use this skill when
- Validating requirements against business goals before implementation
- Confirming requirements are testable and unambiguous
- Reviewing non-functional expectations (performance, scale, security)

## Do not use this skill when
- Implementing the validated requirements
- Requirements are already approved and in flight

## Instructions
1. For each requirement, confirm it is SMART: specific, measurable, achievable, relevant, time-bound.
2. Verify feasibility against the current architecture and stack.
3. Check that acceptance criteria can be objectively tested.
4. Verify requirements do not conflict with existing product behavior.
5. Output a validation report listing pass/fail and blocking issues for each requirement.

## Output Format
- Requirement | Validation Result | Evidence | Recommendation

## Common Mistakes
- Approving requirements without checking testability
- Ignoring technical-debt interactions
- Validating only the happy path
