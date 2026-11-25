---
name: coding-workflow
description: Route non-trivial coding work across target-state implementation, codebase impact, Superpowers, Context7, security review, PR workflow, and verification. Skip for tiny edits or simple reads.
---

# Coding Workflow Adapter

The AI assistant is the supervisor. This skill routes work; it does not duplicate Superpowers.

## Route

- Unclear feature/design: use `decision-alignment`, then Superpowers brainstorming/writing-plans if substantial.
- Confirmed implementation: use `codebase-impact` and `implementation-quality`.
- Feature or bugfix implementation: use `superpowers:test-driven-development` when tests are appropriate.
- Bug, failing test, regression: use `superpowers:systematic-debugging`.
- API/library/version-sensitive work: use Context7 or official docs.
- Security/trust boundary: use `security-review`.
- PR/CI/review-comment loop: use `pr-workflow`.
- Completion claim: use `superpowers:verification-before-completion`.

## Target-State Rule

After the plan is confirmed, implement the target design directly. Do not create avoidable temporary states, duplicate logic, or known cleanup debt.
