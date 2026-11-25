---
name: agent-skill-kit-commons
description: Shared assets and reference implementations consumed by every other skill in the agent-skills-kit. Holds the runtime packages (mjs + py implementations of `skills-ref`), the canonical test/audit/lint/parser fixtures consumed by both runtimes, the parity-test scripts that pin mjs ↔ py twin behavior, and the closure-walks examples that anchor SDK documentation against real CLI behavior. Use when an agent needs to invoke `skills-ref`, run a parity check, regenerate a fixture, or learn the canonical test corpus. Other skills load this one as a dependency so they can rely on a single canonical asset tree instead of duplicating fixtures.
tier: org
license: MIT
compatibility: requires node>=20 and uv (Python 3.11+) installed on PATH for full functionality
metadata:
  role: commons
  consumer-pattern: dependency
---

# Agent-Skills Kit Commons

## Purpose

This skill is the single canonical home for assets shared across every other skill in the toolkit. Before this skill existed, four sibling directories (`packages/`, `fixtures/`, `scripts/`, `examples/`) sat at the repo root and were referenced by relative paths from the Makefile, CI workflow, pre-commit hooks, parity scripts, and four other SKILL.md files. The relocation under `.agents/skills/agent-skill-kit-commons/` makes the commons surface discoverable to the skills tooling itself: `skills-ref deps` now sees it as a dependency target, `skills-ref to-prompt` exports it to the LLM context, and external consumers can pull it via the planned `npx skills-ref add` install verb.

## Contents

After phases 2–5 of the restructure land, this skill owns four sub-trees:

### `packages/` — runtime implementations

- `packages/mjs/` — Node ESM implementation of `skills-ref` (npm package `skills-ref-mjs`). Owns the validator, linter, auditor, dependency resolver, prompt emitter, optimizer, and properties reader. The `bin/skills-ref` entry point is invoked as `npx --prefix <commons-skill>/packages/mjs skills-ref <verb>`.
- `packages/py/` — Python twin (uv-managed, package `skills_ref`). Identical surface, parity-tested against mjs. Asset files are symlinked back to `../mjs/assets/` so both runtimes load the same regex/keyword tables; the sibling assumption is preserved by moving both packages together.

### `fixtures/` — canonical test corpus

Shared between mjs `vitest` tests and py `pytest` tests. Sub-trees:
- `parsed/` — frontmatter parser snapshots (canonical JSON pinned across runtimes).
- `audit/` — clean-suite and with-injections fixtures for the security auditor.
- `lint/` — descriptions + expected scores for the discoverability scorer.
- `optimize/` — input descriptions + expected rewrites for the deterministic optimizer.
- `prompt/` — 5-skill chain expected output for `to-prompt`.
- `naming/` — `<slug>` validation cases.
- `deps/`, `invalid/`, `valid/`, `properties/` — supporting cases.

Test inputs whose expected output encodes the path (`fixtures/parsed/expected/valid-optional.json:1` carries `_path`) use the `<REPO>` placeholder so the fixtures are location-independent.

### `scripts/` — parity harness

Seven `parity-*.sh` scripts that pin mjs ↔ py output equality on every CI run, plus `run-parity.sh` (the validate/audit/deps parity driver) and `test-workflow.sh` (CI workflow smoke test). All scripts anchor on `git rev-parse --show-toplevel` for `$ROOT` so they don't misroute when the script directory moves; the prior `$(dirname "$0")/..` pattern silently pointed at the wrong tree after relocation.

### `examples/` — anchored SDK documentation

- `examples/closure-walks.md` — walks the published SDK doc procedures (validate one skill, build registry, score description, etc.) against the *actual* CLI behavior on this repo and reports MATCH / DRIFT per walk. The doc is regenerated when a CLI behavior shift moves a sample value.

## Consumer Pattern: `npx skills-ref add`

The forward-looking consumer story: other repos pull this commons skill as a dependency via `skills-ref add agent-skill-kit-commons` (planned verb). The install mechanism:

1. `skills-ref add` reads the consumer repo's `.agents/skills/<other-skill>/SKILL.md` for a `dependencies:` entry referencing this commons skill.
2. The verb fetches the commons skill tarball from npm (published as `skills-ref-commons` or pulled from `skills-ref-mjs`'s `assets/` directory at the package level) and unpacks it under the consumer's `.agents/skills/agent-skill-kit-commons/`.
3. The consumer skill's tests then reference `../agent-skill-kit-commons/fixtures/...` via the skill-tree relative path.

This pattern means: change a regex in `packages/mjs/assets/injection_patterns.json`, bump the commons skill version, every consumer skill pulls the new regex on next `skills-ref add` run. No duplicated assets in N consumer repos.

## How Other Skills Reference This One

Inside the same repo, every other SKILL.md that needs commons assets references them via the canonical skill-tree path:

```
.agents/skills/agent-skill-kit-commons/
  packages/mjs/bin/skills-ref      # runtime CLI
  packages/py/                      # python twin
  fixtures/audit/clean-suite/      # auditor input cases
  scripts/parity-lint.sh           # parity harness
  examples/closure-walks.md         # SDK doc oracle
```

The `Makefile`, `.pre-commit-config.yaml`, and `.github/workflows/agent-skills-ci.yml` invoke the runtime via `node .agents/skills/agent-skill-kit-commons/packages/mjs/bin/skills-ref` (or `npx --prefix` of the same path).

The other `agent-skill-kit-*` skills can declare commons as a dependency in their own frontmatter:

```yaml
dependencies:
  - agent-skill-kit-commons@^0.1
```

Dependency direction is governed by the `tier:` frontmatter field, not by the directory name: app-tier and project-tier skills may depend on org-tier commons, never the inverse (§3.3 spec rule).

## Validation and CI

- `make ci` runs the mjs and py test suites against the fixture tree under `fixtures/`.
- `make parity` runs the eight parity scripts under `scripts/`; every one must report `OK` for the build to pass.
- `make validate-suite` runs `skills-ref validate` against `.agents/skills/` including this commons skill.

## Migration Notes

Phases 1–5 of the restructure are tracked in `.plan/<session-id>/plan.md`. Phase 1 (this SKILL.md) creates the commons skill as a pointer documenting the intended layout; phases 2–5 physically relocate the four sub-trees and update all 50+ cross-references. The CI must remain green between every phase.
