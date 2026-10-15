---
name: tdad-fullstack
description: >-
  Test impact analysis for fullstack repos. Fork of tdad v0.2.0 with Vue SFC
  support and CLI enhancements. Use when you need to find which tests are
  affected by code changes in a polyglot project — e.g. changed a Python
  utility + a Vue component, want to know which pytest + vitest + jest files
  to re-run. Activate when you see a `.tdad/` directory in a project with
  both `pyproject.toml` (or `package.json`) AND `.vue` files, or when working
  on a multi-language monorepo. Replaces ad-hoc `git diff | xargs jest
  --findRelatedTests` workflows with one graph.
license: MIT
metadata:
  author: ZhenSiRong
  upstream: tdad (pepealonso95) — MIT, Copyright (c) 2026 Rafael Alonso
  fork-of: https://github.com/pepealonso95/tdad
  upstream-version: "0.2.0"
  fork-deltas: "vue-sfc-support + cli-changed-flag + multi-runner-dispatch + language-tagged-impact-report"
---

# TDAD Fullstack

**Multi-language test impact analysis with first-class Vue SFC support.**

Fork of [tdad v0.2.0](https://github.com/pepealonso95/tdad) that adds:

| What | Why |
|---|---|
| **Vue SFC** (`.vue`) parsing | Upstream v0.2.0 covers Python / JS / TS / Go / Java / Rust / Dart. **Vue is the gap this fork fills.** |
| `tdad impact --changed [REF]` flag | Auto-discover changed files via `git diff` (Vitest-style). Upstream requires manual `--files`. |
| Per-language tagging in `impact` output | Each row in the impacted-tests report shows `[python]` / `[jest]` / `[vitest]` / `[go]` / etc. so the agent knows which runner to dispatch to. |
| `tdad run-tests --runner=auto` | Groups test files by language and calls `pytest` / `vitest run` / `jest --findRelatedTests` / `go test` per group. |

Everything else (Python/JS/TS/Go/Java/Rust/Dart parsers, Neo4j/networkx backends, naming-convention + static-analysis test linker, the `tree-sitter-*` extras) is **inherited from upstream v0.2.0 unchanged**.

## When this skill activates

- A `.tdad/` directory exists in the repo
- The repo is polyglot and includes `.vue` files (or any combination of `.py` / `.js` / `.ts` / `.go` / `.java` / `.rs` / `.dart`)
- You want to run *only* the tests affected by recent code changes

## Setup (one-time per repo)

```bash
# Install CLI (npx symlinks bin/tdad-fullstack into PATH)
npx skills add ZhenSiRong/tdad-fullstack

# OR via pip
pip install -e ".[vue]"   # vue extra includes tree-sitter-javascript for parsing <script> blocks

# Build the code-test graph
tdad-fullstack index .
```

The first run auto-detects which languages are present in the repo.

## Workflow

### 1. Make a change

Edit source files as normal.

### 2. Find impacted tests

```bash
# Auto-discover from git diff (Vitest-style — the killer feature of this fork)
tdad-fullstack impact . --changed
tdad-fullstack impact . --changed HEAD~1
tdad-fullstack impact . --changed origin/main

# Or explicit file list
tdad-fullstack impact . --files src/utils.py src/components/Button.vue
```

Output (Markdown table):

```
## Impacted Tests (3 found)

| Score | Test | File | Language | Reason |
|-------|------|------|----------|--------|
| 0.88 | test_greet | src/test_utils.py | [python] | Directly tests changed code |
| 0.72 | Button.spec | src/components/Button.spec.vue | [vitest] | Imports changed code |
| 0.66 | api.test | frontend/__tests__/api.test.js | [jest] | Imports changed code |
```

The **Language** column is your run-dispatch hint.

### 3. Run only the impacted tests

```bash
# Auto-dispatch: pytest for .py, vitest for .vue, jest for .js/.ts, go test for .go
tdad-fullstack run-tests . --tests src/test_utils.py src/components/Button.spec.vue --runner=auto
```

## Languages supported

| Language   | Parser (upstream)               | Test runner dispatch            |
|------------|----------------------------------|----------------------------------|
| Python     | stdlib `ast`                     | `pytest`                         |
| JavaScript | tree-sitter-javascript           | `jest` / `vitest run`            |
| TypeScript | tree-sitter-typescript           | `jest` / `vitest run`            |
| **Vue (SFC)** | **regex-split + JS parser** (this fork) | **`vitest run`**            |
| Go         | tree-sitter-go                   | `go test`                        |
| Java       | tree-sitter-java                 | `mvn test`                       |
| Rust       | tree-sitter-rust                 | `cargo test`                     |
| Dart       | tree-sitter-dart-orchard         | `dart test`                      |

## Local conventions

- Tests live in `tests/` (pytest) or `__tests__/` (Vitest/Jest) — discovered automatically
- For Vue: `*.spec.vue` / `*.test.vue` files, plus anything under `tests/` or `__tests__/`, are treated as test files
- Re-run `tdad-fullstack index .` after major refactors (auto-incremental otherwise)
- Neo4j is optional — without it, falls back to networkx + graph.pkl

## When NOT to use this skill

- The repo is **pure Python** and doesn't use Vue — use the upstream `tdad` skill instead (lighter, no Vue extras)
- You need mutation testing (test quality, not test selection) — use Stryker / mutmut

## See also

- `references/upstream-design.md` — what we kept from tdad
- `references/vue-sfc-design.md` — how Vue parsing works (regex split + JS reuse)
