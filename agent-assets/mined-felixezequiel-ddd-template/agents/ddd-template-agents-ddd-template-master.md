# AGENTS.md

> Generic instructions for AI coding assistants and IDE agents (Cursor, GitHub Copilot, Codex CLI, Cline, Aider, Continue, Windsurf, etc.).
> Claude Code reads `CLAUDE.md` natively — this file mirrors the same conventions in a tool-agnostic format and points to the **skill files** as the source of truth.

## Assistant compatibility matrix

| Assistant | What it reads | How |
| --- | --- | --- |
| **Claude Code** | `CLAUDE.md` + `.claude/skills/*/SKILL.md` + `.claude/settings.json` (hooks) | Native |
| **Cursor** | `.cursor/rules/*.mdc` (auto-generated) | `npm run sync:rules` |
| **Windsurf** | `.windsurf/rules/*.md` (auto-generated) | `npm run sync:rules` |
| **Cline** | `.clinerules/*.md` (auto-generated) | `npm run sync:rules` |
| **Continue** | `.continue/rules/*.md` (auto-generated) | `npm run sync:rules` |
| **Aider** | `CONVENTIONS.md` (auto-generated) | `npm run sync:rules` |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Manual (stable, rarely changes) |
| **Codex CLI / Zed / generic** | This file (`AGENTS.md`) | Manual (stable, rarely changes) |

**Single source of truth:** `.claude/skills/<name>/SKILL.md`. All adapters above
(except `AGENTS.md` and `copilot-instructions.md`) are **regenerated** by
`scripts/sync-rules.mjs` and **must not be edited manually**. See
[ADR-007](docs/adrs/007-multi-assistant-rules-strategy.md).

The git pre-commit (`scripts/precommit.mjs`) is the deterministic safety net —
it blocks commits that violate TDD/Hexagonal/PlainObject regardless of which
assistant produced the code.

## What this repository is

A **TypeScript DDD + Hexagonal Architecture template** with battle-tested building
blocks (event store, transactional Unit of Work, automatic aggregate tracking,
multi-tenancy, SSE, observability) and a complete `User` reference module.

For the full overview, read [`README.md`](README.md) and [`CLAUDE.md`](CLAUDE.md).
For the request lifecycle diagram, read [`docs/architecture.md`](docs/architecture.md).

## Skills (single source of truth)

Every engineering practice this project enforces lives in a structured skill file
at [`.claude/skills/<name>/SKILL.md`](.claude/skills/). Each file uses **Ring format**
(YAML frontmatter declaring `trigger`, `skip_when`, `sequence`, `related` + a
markdown body with rules). The frontmatter is machine-readable; the body is
human-readable.

| Skill                                                                                  | When it applies                                              |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| [`adr`](.claude/skills/adr/SKILL.md)                                                   | Always before implementation when an architectural decision is involved |
| [`readable-code`](.claude/skills/readable-code/SKILL.md)                               | Always — every line of code written                          |
| [`doc-sync`](.claude/skills/doc-sync/SKILL.md)                                         | Always after code changes                                    |
| [`tdd-workflow`](.claude/skills/tdd-workflow/SKILL.md)                                 | "create", "implement", "add", "fix", "bug"                   |
| [`safe-refactoring`](.claude/skills/safe-refactoring/SKILL.md)                         | "refactor", "improve", "extract", "rewrite"                  |
| [`ddd-patterns`](.claude/skills/ddd-patterns/SKILL.md)                                 | "entity", "value object", "aggregate", "domain event"        |
| [`hexagonal-architecture`](.claude/skills/hexagonal-architecture/SKILL.md)             | "where to put", "which layer", "ports and adapters"          |
| [`pr-template`](.claude/skills/pr-template/SKILL.md)                                   | "create PR", "open PR"                                       |
| [`code-review`](.claude/skills/code-review/SKILL.md)                                   | "review", "/review"                                          |
| [`task-breakdown`](.claude/skills/task-breakdown/SKILL.md)                             | "break tasks", "plan PRs", "divide work"                     |
| [`project-onboarding`](.claude/skills/project-onboarding/SKILL.md)                     | "I'm new", "introduction", "tour", "where do I start"        |
| [`architecture-explainer`](.claude/skills/architecture-explainer/SKILL.md)             | "how does X work", "explain Y", "why Z"                      |
| [`module-walkthrough`](.claude/skills/module-walkthrough/SKILL.md)                     | "new bounded context", "new aggregate", "new use case"       |

**As an AI agent on this repo, read the skill file before applying its practice.** The
files are short (≈150 lines each) and contain the explicit MUST / MUST NOT rules.

## Always-on rules (the non-negotiables)

These are enforced both at the LLM layer (skills) and at the harness layer (hooks):

1. **TDD inside-out** — tests before production code. Co-located: `Foo.test.ts` next to `Foo.ts`. Domain → Application → Infrastructure.
2. **ADR before architectural decisions** — search [`docs/adrs/`](docs/adrs/) first; create a new ADR before implementing if missing.
3. **Readable code** — zero magic numbers, no nested ternaries, no long functional chains hiding business logic, descriptive names.
4. **Hexagonal dependency rule** — `infrastructure → application → domain`. Domain has zero framework imports.
5. **Doc sync** — after every code change, evaluate if [`README.md`](README.md), [`CLAUDE.md`](CLAUDE.md), [`docs/`](docs/) or an ADR needs updating.

## Template-specific rules (the footguns)

- **All MikroORM ORM entities MUST `extends PlainObject` from `@mikro-orm/core`** — root and children. See [`hexagonal-architecture` skill](.claude/skills/hexagonal-architecture/SKILL.md#mikroorm-orm-entities--the-plainobject-rule).
- **Use cases NEVER call `repository.save()`** — aggregates auto-track on the first `addDomainEvent()`. The `MikroOrmUnitOfWork` flushes inside `em.transactional()` on commit.
- **Adapters always call `Command.of(...primitives)`** — never construct VOs directly. Commands have private constructors.
- **VOs use `protected` props** — subclasses expose domain-meaningful getters (`get value()`, not `props.value`).

## Stack at a glance

- TypeScript 5.9 (`strict`, `exactOptionalPropertyTypes`, `noUncheckedIndexedAccess`)
- Node 24+ with native `node:test` runner — no Jest, no Vitest
- ESM + SWC on-the-fly transpilation — no build step
- MikroORM 7 + SQLite (default, swappable to Postgres in 4 lines — see README)
- GraphQL alongside REST
- ESLint 9 flat config + Prettier + GitHub Actions CI

## Commands

```bash
npm start                  # boot REST :3000 + GraphQL :4000 (runs migrations on boot)
npm test                   # all tests
npm run test:unit          # exclude integration / performance tests
npm run test:changed       # tests for files changed since HEAD (fast TDD loop)
npm run test:watch         # watch mode
npm run typecheck          # tsc --noEmit
npm run lint
npm run lint:fix
npm run format
npm run bench
npm run migration:create -- --name=MyMigration
npm run migration:up
```

## Hooks (deterministic enforcement)

Pure-Node hooks in [`.claude/hooks/`](.claude/hooks/), wired via [`.claude/settings.json`](.claude/settings.json) for Claude Code and via a git pre-commit hook for every other agent. Zero env var requirements, zero non-Node dependencies.

### Two enforcement layers (same checks, both layers)

The validation logic lives in [`.claude/hooks/checks/`](.claude/hooks/checks/) as pure functions. Two thin runners consume it:

1. **Claude Code runtime hooks** — interactive, real-time, run via [`.claude/settings.json`](.claude/settings.json). Read JSON from stdin, emit JSON to stdout following the Claude Code hook contract.
2. **Git pre-commit hook** — runs for every commit regardless of which AI agent made the changes (Cursor, Copilot, Codex, Aider, Cline, Continue, Windsurf, manual edits, CI bots). Installed automatically on `npm install` (or via `npm run hooks:install`).

This means the same TDD / Hexagonal / PlainObject / Readable-code rules are enforced **whichever agent you use**.

### Claude Code hooks (interactive)

| Hook                            | Event                            | Purpose                                                              |
| ------------------------------- | -------------------------------- | -------------------------------------------------------------------- |
| `adr-detector.mjs`              | UserPromptSubmit                 | Reminds about ADRs when prompt mentions architectural changes        |
| `tdd-checker.mjs`               | PreToolUse Edit/Write            | Reminds to write the test first when no co-located `.test.ts` exists |
| `hexagonal-validator.mjs`       | PreToolUse Write                 | Asks before writing if domain/application imports infrastructure     |
| `plainobject-checker.mjs`       | PreToolUse Write                 | Asks before writing an ORM entity that doesn't extend `PlainObject`  |
| `safe-refactoring-checker.mjs`  | PreToolUse Edit                  | Reminds about parallel implementation on `refactor/*` branches       |
| `pr-template-validator.mjs`     | PreToolUse Bash\|PowerShell      | Asks if `gh pr create` body is missing Summary or Test plan          |
| `readable-code-checker.mjs`     | PostToolUse Edit/Write           | Flags magic numbers, nested ternaries, long functional chains        |
| `doc-sync-tracker.mjs` + `doc-sync-checker.mjs` | PostToolUse + Stop | Blocks stop with reminder if code changed but no docs updated      |

### Git pre-commit (works for every agent)

The pre-commit runner in [`scripts/precommit.mjs`](scripts/precommit.mjs) blocks commits that violate:

- **TDD** — production `.ts` file staged without a co-located `*.test.ts`
- **Hexagonal** — `domain/` or `application/` files importing from infrastructure or frameworks
- **PlainObject** — ORM entity classes missing `extends PlainObject` from `@mikro-orm/core`

It also surfaces non-blocking **readable-code** warnings (magic numbers, nested ternaries, long functional chains).

**Requirement:** Node 24+ in PATH (already required by the project). No PowerShell, no `pwsh`, no env vars, no extra binaries.

### Validating the hooks themselves

```bash
npm run hooks:test       # runs 20 smoke tests against all hooks
npm run hooks:install    # re-installs the git pre-commit hook
npm run precommit        # runs the pre-commit checks against currently staged files
npm run sync:rules       # regenerates Cursor / Windsurf / Cline / Continue / Aider adapters
npm run setup:ai         # OPTIONAL — installs skills + hooks globally at $HOME/.claude/
```

All scripts are pure Node ESM (`.mjs`) — they run identically on Windows,
macOS and Linux. No bash, no PowerShell, no extra dependencies beyond Node 24+.

## Working with this template

When you (an AI agent) are asked to:

| Task                                                  | Do this                                                                                  |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| "Add a new bounded context"                           | Follow [`module-walkthrough` skill](.claude/skills/module-walkthrough/SKILL.md) walkthrough A and [`docs/adding-a-bounded-context.md`](docs/adding-a-bounded-context.md) |
| "Add a new use case in module X"                      | Follow [`module-walkthrough` skill](.claude/skills/module-walkthrough/SKILL.md) walkthrough C, with TDD |
| "Explain how X works"                                 | Use [`architecture-explainer` skill](.claude/skills/architecture-explainer/SKILL.md) — find the topic in its index |
| "I'm new, where do I start"                           | Use [`project-onboarding` skill](.claude/skills/project-onboarding/SKILL.md)              |
| "Refactor module X"                                   | Follow [`safe-refactoring` skill](.claude/skills/safe-refactoring/SKILL.md) — parallel implementation behind a toggle |
| "Create a PR"                                         | Follow [`pr-template` skill](.claude/skills/pr-template/SKILL.md)                          |
| "Review this PR"                                      | Follow [`code-review` skill](.claude/skills/code-review/SKILL.md) — Mermaid diagram of execution cycle |

## License

ISC. See [`LICENSE`](LICENSE) (or `package.json`).
