---
name: mutation-testing
description: Mutation testing ile test suite kalitesini olc. Stryker, mutmut, go-mutesting destegi. Grok-native with Production Contract, hooks, compound, palace.
when-to-use: When evaluating test effectiveness, finding weak tests, or improving kill ratio in TDD flows. Use with tdd-guide, test-enforcement, arbiter.
---

# Mutation Testing Skill (Grok Port)

Measure how good your tests really are by introducing small code changes (mutants) and seeing if tests catch them.

## Why Mutation Testing
- Code coverage lies. 100% coverage can still miss logic bugs.
- Mutation score = % of mutants killed by tests. Target 80%+ for critical code.
- Finds: missing assertions, weak mocks, untested branches, copy-paste errors.

## Supported Tools (Grok)
- JavaScript/TS: Stryker (best for modern stacks, integrates with Jest, Vitest, etc.)
- Python: mutmut (simple, fast for pytest)
- Go: go-mutesting

## Core Workflow
1. Run on changed code or critical modules (not whole repo every time).
2. Review "survived" mutants — these are your real gaps.
3. Fix by adding tests or strengthening existing ones.
4. Re-run until score acceptable.
5. Record friction for patterns that keep surviving (e.g. "our mocks never assert on side effects").

## Grok Integration
- Use with tdd-guide / test-enforcement / arbiter in swarms.
- on_test or on_linter_friction hooks can suggest running mutation after coverage passes.
- Pre-Flight: "Have we run mutation on the new logic or refactored area?"
- Ledger for big refactors where test quality matters.
- Handoff: include mutation report summary + top survived mutants + recommended tests.
- Friction + compound: every "this mutant survived because our test only checked happy path" → compound to improve test templates or linter rules.
- Palace: store "for payment flows we always require mutation score > 85%".
- Claim-verif: never claim "tests are solid" without mutation evidence + read of the report.

## Quick Commands
```bash
# Stryker (Node)
npx stryker run

# mutmut (Python)
mutmut run
mutmut results

# Go
go-mutesting ./...
```

## Common Weak Spots Found
- Tests that pass on any non-error result.
- Mocks that accept anything.
- Missing boundary checks.
- Error paths never asserted.

Run it. Your coverage number will never lie to you again.
