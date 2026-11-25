---
name: fullstack-delivery
description: Full-stack delivery workflow — spec, TDD, review, CI, deploy, observe.
---

# fullstack-delivery

> Full-stack delivery workflow: spec → TDD → review → CI → deploy → observe.

## Guardrails (read first)

- **No production deploy without tests passing and a rollback plan.** If either is missing, the deploy stops.
- **No secrets in code, logs, or commits.** Run the secret scan before every push.
- **No breaking database change without a migration.** Backwards-compatible first; destructive changes need a plan and a backup.
- **Accessibility is a release gate, not a polish step.** Keyboard, focus, and contrast are checked before release, not after.

## When to use

- Building a feature end to end: API + database + frontend.
- Fixing a bug without breaking something else.
- Shipping a release: staging → production → monitoring.
- Reviewing a pull request.

## Workflow

### 1. Spec first

- Write the spec before code: what changes, for whom, how it is verified. See [github/spec-kit](https://github.com/github/spec-kit).
- List the API contract (endpoints, inputs, outputs, errors) and the data model (tables, migrations) before writing a line of code.

### 2. TDD

- Red: write a failing test for the behaviour.
- Green: write the smallest code that passes.
- Refactor: clean up, tests still green.
- Cover: happy path, error path, and the edge case most likely to break in production.

### 3. Code review

- Review checklist: does it do what the spec says? Are errors handled? Are secrets absent? Are queries safe (parameterised, no string-built SQL)? Is the UI keyboard-accessible?
- Small PRs only — one feature, one PR. A PR nobody can review in 15 minutes is too big.

### 4. CI

- Every PR runs: lint, type check, tests, secret scan.
- A red pipeline blocks the merge. No exceptions, no "fix it later".

### 5. Deploy

- Staging first, smoke test, then production.
- Database migrations run before the code that needs them; rollbacks are tested, not assumed.
- Release notes: what changed, what to watch, how to roll back.

### 6. Observe

- After deploy: check error rate, latency, and the one business metric the feature should move.
- If an error spikes, roll back first, investigate second.

## Release gate checklist

- [ ] Spec written and linked in the PR?
- [ ] Tests pass (unit + the critical end-to-end path)?
- [ ] Secret scan clean?
- [ ] Migration backwards-compatible, backup taken?
- [ ] Accessibility checked (keyboard, focus, contrast)?
- [ ] Rollback plan written down?
- [ ] Monitoring checked after deploy?

## Related skills (link only, not copied)

- [github/spec-kit](https://github.com/github/spec-kit) — spec-driven development (Tier 1).
- [evanklem/evanflow](https://github.com/evanklem/evanflow) — TDD (gap filler).
- [antonbabenko/terraform-skill](https://github.com/antonbabenko/terraform-skill) — Terraform & OpenTofu (DevOps pack, verified).
- [LukasNiessen/kubernetes-skill](https://github.com/LukasNiessen/kubernetes-skill) — Kubernetes (DevOps pack, verified).
- [vstorm-co/production-stack-skills](https://github.com/vstorm-co/production-stack-skills) — production deploy checklist (DevOps pack, verified).
- Lumitome: `docs-pack`, `finishing-a-development-branch`, `code-review`, `tdd-red-green-refactor`.
