---
name: commit-discipline
description: >-
  Use when about to commit, when asked to commit, to write a commit message or to split a
  change, or when the guard reports too many uncommitted changes. One use case or concept
  per commit, messages scoped by context.
allowed-tools:
  - Bash(git status *)
  - Bash(git diff *)
  - Bash(git log *)
  - Bash(git add *)
  - Bash(npx ddd-ts-kit check *)
  - Bash(npx ddd-ts-kit todo *)
  - Bash(npx ddd-ts-kit docs --check)
---

# Commit discipline

A commit is one thing a reviewer can understand and a team can revert. In this architecture
that thing has a natural size: **one slice**. The checks before the commit are skill
`ddd-ts-kit:quality-gate`.

## What goes in one commit

| Commit | Holds |
|---|---|
| a use case | its `application/commands|queries/<use-case>/` folder, the domain behaviour it needs, its route, their specs |
| a concept alone, when the use case would grow too large | one aggregate, value object or policy with its spec and builder |
| a contract | one integration event or read contract of a `published-language/`, with its publisher |
| a strategic step | one artefact of `docs/architecture/` and the updated plan |
| a decision | one `docs/adr/` record and the config entry it justifies |

Always in the same commit as what caused them: the files the generator wrote and updated
(the `created`, `updated` and `deleted` lists of its output), the regenerated declarations
(`<context>.declarations.ts` and the `<layer>.declarations.ts` of each layer it touched),
the generated lists of `CONTEXT.md`, the glossary row a new
name needed, the contracts under `openapi/`, the event catalog, `docs/context-map.md`. A generated
file committed alone, or left for later, breaks `docs --check` on one side of the history.

Never in the same commit: two use cases, two contexts (except a contract and its first
consumer, when agreed), a refactoring and a behaviour change, a rule relaxation and the code
that needed it.

## Size

Target: at most `commit.maxFiles` files and `commit.maxLines` changed lines
(`ddd-ts-kit.config.json`; 20 and 600 when the key is absent), generated files and the
lockfile not counted. `npx ddd-ts-kit check --commit-size` measures what is about to be
committed against them (`--staged` reads the index only; advisory, `--strict` exits 1 when
over). A generated use case with its route is 10 to 15 files, most of them small. The guard
says so once, without blocking, when the working tree goes past the limits, and names the
slices it sees.

## Message

Conventional commits, checked by commitlint at `commit-msg`:

```text
<type>(<context>): <what the business can now do, imperative, lower case>
```

- `type`: `feat` (behaviour), `fix`, `refactor` (no behaviour change), `test`, `docs`,
  `chore`, `build`, `ci`.
- scope: the bounded context; `platform` for `src/platform/`; none for the whole project.
- summary in the ubiquitous language: `feat(ordering): refuse an order without lines`, not
  `feat: add validation to handler`.
- body only for the why, a decision record number, or a breaking change (`!` after the
  scope, and `BREAKING CHANGE:` in the body for a contract).

## Before committing

1. `git status --short` and read it by slice: one use-case folder, its route, its specs.
2. `npx ddd-ts-kit check --changed-since HEAD`, `npx ddd-ts-kit docs --check`, and
   `npx ddd-ts-kit todo <context> --brief`: no marker left in the slice.
3. Stage by path, never everything at once when several slices are pending:
   `git add src/contexts/<context>/application/commands/<use-case> <its route> <its specs> <the declarations of their layers> <CONTEXT.md>`.
4. Read `git diff --cached --stat` and `npx ddd-ts-kit check --commit-size --staged`: one
   story, within the limits?
5. Commit. The pre-commit hook runs the linter and the architecture check on the staged
   files, regenerates and adds the pages of what the tests state when a spec is staged, and reads
   the commit size. Never skip them: not `--no-verify` (on `commit`, `push`, `merge`), not `git commit -n`,
   not `-c core.hooksPath=...`, not `LEFTHOOK=0` or `HUSKY=0`. The hooks are the local gate of the
   pipeline and the guard refuses the command. If a hook fails, fix what it reports; if the hook is
   itself broken, report it to the project owner.

Propose the commit (files and message) and let the user confirm, unless you were asked to
commit or you are a worker in your own worktree, where each finished slice is committed.

## A change that grew

Split it along the order it could have been built in, each commit green on its own:

1. glossary terms and documents;
2. each domain concept with its spec (value object, then aggregate behaviour);
3. each use case with its handler spec;
4. each route with the regenerated contract.

Stage path by path in that order. When two slices are tangled in one file, commit the first
with the whole file and say so in the body rather than rewriting history. If the split is
not obvious, the change did two things: say which, and ask.

## Never

- commit with `TODO(domain)` or `it.todo` left in the slice and call it done;
- commit a failing check "to fix later", or skip the hooks;
- amend or rewrite a commit that was pushed: add a new one.
