---
name: "test-gap-finder"
description: "Identify missing or weak tests by mapping changed or risky code to absent unit, integration, contract, and UI coverage. Use when a user asks to review test coverage, find testing gaps, prepare release confidence, or as part of $full-test-suite pre-release work."
---

# Test Gap Finder

Find the highest-risk testing gaps and promote only actionable coverage findings.

## Focus Areas

- changed code with no nearby tests
- risky logic paths with only happy-path coverage
- missing contract, migration, or regression tests
- flaky or misleading test signals

## Outputs

- findings in `project-audit-findings.md`
- concrete missing test recommendations, and test additions when fixing is in scope

## References

- Finding format: `../_shared-project-ops/references/finding-format.md`
- Verification template: `../_shared-project-ops/references/verification-template.md`
