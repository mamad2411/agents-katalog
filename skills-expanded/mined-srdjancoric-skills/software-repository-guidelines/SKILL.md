---
name: software-repository-guidelines
description: Manually assess a repository's engineering health against a practical checklist and return evidence-backed, prioritized hardening recommendations. Invoke explicitly for a repository audit, setup, or hardening initiative; it never runs automatically during planning, implementation, testing, review, or PR work.
disable-model-invocation: true
---

# Repository Health Audit

Run this skill only when the user explicitly asks to assess, bootstrap, or harden a repository. It
is an audit, not a routine development gate. Do not invoke it from another skill and do not turn an
ordinary feature, bug fix, or review into a repository-wide hardening project.

## Process

1. Establish the audit scope with the user: full repository, or one of developer experience,
   validation and CI, security, documentation, or release readiness.
2. Inspect the repository and load `references/00-overview.md` plus only the references relevant to
   that scope. Load every reference only for a requested full audit.
3. Gather evidence from version-controlled files, canonical commands, CI configuration, and provider
   configuration when the user authorizes access. Do not treat an assertion as evidence.
4. Classify every inspected item as `complete`, `gap`, `not applicable`, `deferred`, or
   `accepted risk`. A complete item satisfies the evidence rule in `references/00-overview.md`.
5. Return a compact report. Do not edit repository files unless the user separately asks to plan or
   implement selected recommendations.

## Output

Include:

- audit scope and references loaded;
- evidence-backed complete items;
- gaps, each with impact, evidence, and smallest recommended remediation;
- not-applicable items and their repository-specific reason;
- deferred and accepted-risk items with an owner or recorded user rationale;
- a prioritized shortlist of independently deliverable follow-up tasks.

Prioritize concrete risks and missing feedback loops over checklist completeness. Do not recommend a
container, CODEOWNERS, coverage threshold, pre-commit hook, ADR process, or similar mechanism unless
its reference applies and repository evidence supports the recommendation.

## Reference index

- `references/00-overview.md` — purpose and completion evidence rule
- `references/01-style-and-code-quality.md`
- `references/02-testing.md`
- `references/03-documentation.md`
- `references/04-developer-environment.md`
- `references/05-ci-cd.md`
- `references/06-code-health-and-maintainability.md`
- `references/07-security.md`
- `references/08-recommended-canonical-commands.md`
- `references/09-expected-repository-files.md`
- `references/10-definition-of-done.md`
