# Repository Agent Instructions

## Instruction Scope

- This file contains rules shared by the whole repository.
- Before changing a subtree, check for a nearer `AGENTS.md`; local instructions add to or override this file for that subtree.
- This repository uses only `AGENTS.md` for agent instructions and `CONTEXT.md` for domain context. Do not duplicate these rules in tool-specific instruction files.
- Keep one `AGENTS.md` and one `CONTEXT.md` per independently managed large module. Do not add finer-grained files unless that subtree has genuinely independent ownership and rules.
- Agent hosts that do not discover `AGENTS.md` automatically must be configured or prompted to read the applicable files.
- See [`docs/agents/instruction-files.md`](docs/agents/instruction-files.md) for discovery and precedence rules.

## Domain Documentation

- Before changing domain behavior or terminology, read the root [`CONTEXT.md`](CONTEXT.md), then the relevant module `CONTEXT.md` and ADRs.
- `CONTEXT.md` files are glossaries only. Put implementation constraints in `AGENTS.md` and durable architectural decisions in ADRs.
- All ADRs live in the root [`docs/adr/`](docs/adr/), including decisions scoped to a single module.
- See [`docs/agents/domain.md`](docs/agents/domain.md).

## Issue Tracker

- Issues and PRDs are tracked in GitHub Issues through `gh`. See [`docs/agents/issue-tracker.md`](docs/agents/issue-tracker.md).
- Use the canonical triage labels documented in [`docs/agents/triage-labels.md`](docs/agents/triage-labels.md).

## Testing

- Before writing, changing, reviewing, or running tests, read [`docs/test/testing-guide.md`](docs/test/testing-guide.md).
- Keep tests under the owning module's `src/test`; do not use `src/intg-test`.
- Run fast backend tests with `mvn -f apps/server/pom.xml test`.
- Run the complete backend suite with `mvn -f apps/server/pom.xml verify`. It requires Docker for Testcontainers MySQL 8 and Redis 8; do not substitute H2, local services, or shared services.

## Git And Delivery

- Leave changes uncommitted unless the user explicitly requests a commit.
- When a commit is requested, use `pnpm run commit`; never invoke `git commit` directly.
- Do not push or create or update a pull request unless the user explicitly requests remote delivery.
- Remote delivery must use a pull request. Never push directly to `main` or another target branch; default the PR base to `main` unless the user specifies otherwise.
