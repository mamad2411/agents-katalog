# GitHub Copilot Instructions

> **The authoritative instructions for AI agents in this repo are in [`AGENTS.md`](../AGENTS.md).**
> This file exists because GitHub Copilot Chat reads `.github/copilot-instructions.md` by default and does not yet follow the AGENTS.md convention.

## How to use this repo

1. Read [`AGENTS.md`](../AGENTS.md) first — it lists every engineering practice this template enforces and the assistant compatibility matrix.
2. Read [`CLAUDE.md`](../CLAUDE.md) for the concise architecture reference (base classes, TypeScript constraints, test patterns).
3. Read [`README.md`](../README.md) for the stack overview, commands, and feature matrix.

**Source of truth for engineering rules:** [`.claude/skills/`](../.claude/skills/). All other assistants (Cursor, Windsurf, Cline, Continue, Aider) read auto-generated adapters produced by `scripts/sync-rules.mjs` from those skills. See [ADR-007](../docs/adrs/007-multi-assistant-rules-strategy.md).

## Always-on rules (the non-negotiables)

- **TDD inside-out** — write the test before the production code. Tests are co-located: `Foo.test.ts` lives next to `Foo.ts`. Domain → Application → Infrastructure.
- **ADR before architectural decisions** — search [`docs/adrs/`](../docs/adrs/); if no ADR covers the decision, create one before implementing.
- **Hexagonal dependency rule** — `infrastructure → application → domain`. Domain has zero framework imports (no `@mikro-orm/*`, no HTTP, no nodemailer).
- **Readable code** — zero magic numbers, no nested ternaries, no functional chains hiding business logic, descriptive names.
- **Doc sync** — after every code change evaluate if `README.md`, `CLAUDE.md`, `docs/`, or an ADR needs updating.

## Template-specific footguns to avoid

- **All MikroORM ORM entities (root + children) MUST `extends PlainObject` from `@mikro-orm/core`.** Without it, MikroORM proxies break mappers and trigger subtle hydration bugs. This is the #1 footgun.
- **Use cases NEVER call `repository.save()`** — aggregates auto-track on the first `addDomainEvent()`. The `MikroOrmUnitOfWork` flushes inside `em.transactional()` on commit.
- **Adapters always call `Command.of(...primitives)`** — never construct VOs directly. Commands have private constructors.

## Where to find detailed guidance

For specific tasks, see the relevant skill file in [`.claude/skills/`](../.claude/skills/):

- New bounded context / aggregate / use case → [`module-walkthrough`](../.claude/skills/module-walkthrough/SKILL.md)
- "How does X work" → [`architecture-explainer`](../.claude/skills/architecture-explainer/SKILL.md)
- Onboarding / project tour → [`project-onboarding`](../.claude/skills/project-onboarding/SKILL.md)
- TDD cycle → [`tdd-workflow`](../.claude/skills/tdd-workflow/SKILL.md)
- Refactoring → [`safe-refactoring`](../.claude/skills/safe-refactoring/SKILL.md)
- Creating PRs → [`pr-template`](../.claude/skills/pr-template/SKILL.md)
- Code review → [`code-review`](../.claude/skills/code-review/SKILL.md)
