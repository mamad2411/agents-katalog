---
name: specrail-heavy
description: Use only when the user explicitly says SpecRail Heavy, heavy mode, or asks to invoke the SpecRail heavy profile. Provide deeper planning and repository-native verification.
---

# SpecRail Heavy

Heavy mode is explicit and task-scoped. Installing this skill does not activate
it for ordinary development.

Use Heavy for ambiguous product behavior, cross-module changes, public API or
data migrations, security-sensitive work, architecture changes, or a long
issue/PR queue whose failure cost justifies deeper preparation.

## Start

1. Read repository instructions and current GitHub truth.
2. Search for existing Issues, PRs, branches, specs, and overlapping code.
3. State goal, non-goals, constraints, compatibility policy, and measurable
   done-when.
4. Identify affected components, owners, risks, rollback, and verification.
5. Present the implementation plan before editing.

## Durable working set

Use the target repository's chosen documentation location. For non-trivial
work, keep:

- user-visible requirements and acceptance criteria;
- technical design, affected files, interfaces, risks, migration, and rollback;
- numbered tasks with dependencies, owners, done-when, and exact native checks.

Do not create documents merely to satisfy a profile. Existing clear
requirements may be reused.

## Execute

1. Implement one planned task at a time.
2. Run its focused repository-native checks before advancing.
3. Keep the original branch and PR when work already exists.
4. Add tests for changed behavior without weakening current assertions.
5. Diagnose failures from fresh evidence and one root-cause hypothesis.
6. Re-read current remote state before external writes.

## Review and finish

- Map every acceptance criterion to code and test evidence.
- Review correctness, regressions, error handling, security, compatibility,
  operational risk, and unintended scope.
- Resolve current review findings on the original PR.
- Run the repository's full required verification.
- Report remaining risks and unknown remote state.
- Push, comment, close, publish, or merge only within the caller's explicit
  authorization.

Heavy mode adds depth, not a second state machine. It must not invoke retired
SpecRail checker scripts, manufacture approval evidence, or override repository
policy.
