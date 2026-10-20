# CLAUDE.md

## Project Overview

**QoQ (Quality over Quantity)** — a monorepo of npm packages published as
`@ladamczyk/qoq-*`, orchestrating Prettier, ESLint, Knip, JSCPD, Stylelint,
Structurelint, Skillslint and npm-outdated behind one CLI. Node >=22.15.0.

Structurelint and Skillslint are the separate `@ladamczyk/structurelint` and
`@ladamczyk/skillslint` packages — not in this workspace.

## Commands

| Command              | Notes                                                   |
| -------------------- | ------------------------------------------------------- |
| `npm install`        |                                                         |
| `npm run build`      | all packages, via Lerna                                 |
| `npm test`           | config-inspector first, then vitest across all packages |
| `npm test Name`      | to run specific test                                    |
| `npm run test:skill` | the skill's own scripts (`node:test`, not vitest)       |
| `npm run qoq:check`  | full quality check — this is what CI and pre-push run   |
| `npm run qoq:fix`    | auto-fix                                                |

<!-- qoq:discovery -->

- test (full suite): `npm test`
- test (one file): `npm test {file}`
- build: `npm run build`
- runner: vitest, globals off, no React

<!-- /qoq:discovery -->

## Versioning

`.claude-plugin/marketplace.json` is generated, not authored: `metadata.version`
tracks the lib version and the plugin `description` is copied from
`skills/qoq/SKILL.md`'s frontmatter. `scripts/sync-plugin-version.js` writes both
from semantic-release's `prepare` step (`npm run sync:plugin-version`), and
`@semantic-release/git` commits them. **Never edit either by hand** — the release
run overwrites them, and a plugin description that disagrees with `SKILL.md` is a
second stale trigger blurb in every session's context.

## Monorepo Layout

- `packages/cli` — the `qoq` CLI binary; main orchestrator
- `packages/utils` — shared utilities
- `packages/check-engine` — node version enforcement
- `packages/eslint-v9-*` — ESLint flat config templates (JS/TS × framework × test runner). Each package exports its own delta layer plus `configs.*` `defineConfig` arrays composed from its ancestry, so ESLint's own per-file cascade does the merging instead of a pre-merge step
- `packages/prettier[-with-json-sort]` — Prettier config templates
- `packages/knip` — Knip config template
- `packages/jscpd` — JSCPD config template
- `packages/stylelint-{css,scss}` — Stylelint config templates

## Testing

`packages/*/src/**/*.spec.{ts,js}`, Vitest across all packages.

The `skills/qoq/scripts/*.spec.mjs` files are **`node:test`, not Vitest** —
`vitest.config.js`'s `projects: ['packages/*']` never sees them. `npm run
test:skill` runs them, and `husky:pre-push` does too. Appending them to `npm
test` would break the documented `npm test Name`, since npm puts extra args at
the end of the script string.

`npm run config:diff` compares what ESLint actually resolves (via `calculateConfigForFile`)
for every `eslint-v9-*` package against a git ref, defaulting to `master` — it checks the ref
out to a temporary worktree, builds it there, and diffs the result against the current
checkout. It's on-demand, not part of the gate: it isn't wired into `qoq:check` or
`husky:pre-push` because installing and building a second checkout takes minutes.

## The `qoq` skill and its diagrams

The skill is `skills/qoq/` — `SKILL.md` routes and holds only what every command
needs, `references/*.md` hold each command's rules, `agents/*.md` are the six
subagents, `assets/patterns/` is `qoq-designer`'s catalogue — a base index plus
one per stack (`react/index.md` today), which it reads, and twenty-one write-ups
only `refactor` opens, one at a time. Rationale lives in exactly one of those layers: a paragraph in both
`SKILL.md` and a reference is paid for twice by the same thread. Its eval set is
`evals/qoq-evals.json`, outside the skill so it doesn't ship in the plugin.

Two things live **outside** the skill so an agent reading it never pays for what
it can't act on: the Mermaid diagrams at `docs/qoq-workflows.md`, and the
_design rationale_ at `docs/qoq-design.md`. The rule that separates them — a why
that stops a wrong action stays in the skill; a why that only argues for a
decision already made goes to `qoq-design.md` — is `references/compress.md`'s own
test, applied to the skill itself.

**All three change in the same commit, every direction.** Prose in `skills/qoq/`
→ update the matching diagram in `docs/qoq-workflows.md` and any design note in
`docs/qoq-design.md` that argues for it. A diagram → update the reference file
its header table names.

Prose wins on a disagreement. But a stale diagram or a design note for a rule
that no longer exists is worse than none: it's what a person reaches for, and
they have no reason to doubt it. Landing on one side only isn't finished.

<!-- qoq:discovery -->

- test (full suite): `npm test`
- test (one file): `npm test {file}`
- build: `npm run build`
- runner: vitest, globals off, no React

<!-- /qoq:discovery -->
