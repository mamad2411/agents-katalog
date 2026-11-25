---
name: check-file-relation
description: Check file import relations + concat all or related files into one output — Rust CLI, custom regex
argument-hint: "<dir> [--all|--from <file>|--summary|--json] [--ext|--include|--order|--pattern|--max-lines]"
related:
  - read-all-files
  - follow-create-cli
  - update-devin-global-skills
  - deep-review-codebase
  - check-long-files
  - check-code-structure
  - analyze-file-structure
  - run-check

---

## Goal

Rust CLI that detects the dependency graph between files from import statements (TS/JS, Rust, Go, Python, Java, Kotlin, C#, Vue, Svelte) + custom regex — and concatenates files into a single output `===== <path> =====` + content (repomix-style) for feeding into an LLM/review — the core engine of `/read-all-files`

## Scope

- Read-only analysis — never modifies the scanned files
- Built-in extractors: `import`/`export from`/`require`/dynamic `import()` (JS/TS family), `use`/`mod`/`crate::`/`super::` (Rust), `import` (Go), `import`/`from x import` (Python), `import` (Java/Kotlin), `using` (C#)
- Custom patterns via `--pattern '<regex>'` (repeatable, first capture group = module specifier)
- Resolve relative/`crate::`/`@/`/`~/` paths to real files (filling in extensions, `index.*`, `mod.rs`, `__init__.py`)
- Single source: `src/main.rs` + `Cargo.toml` — deps: `ignore`, `regex`, `serde`/`serde_json`, `globset`

## Execute

### 0. Build

> Goal: compile the binary (first time or after editing source)

```bash
cd <skill-dir> && cargo build --release
# binary: <skill-dir>/target/release/check-file-relation.exe
```

The examples below use `cfr` in place of the binary path

### 1. Relation Map

> Goal: get the directory's dependency graph

```bash
cfr <dir>                  # file → imports (resolved path or [external])
cfr src --summary          # top imported internal files only
cfr src --json             # machine-readable graph for downstream tooling
```

### 2. Concat Files

> Goal: a single output with files concatenated as `===== <path> =====` + content

```bash
cfr src --all                          # all matching files
cfr src --all --order smart            # config → entry → deps topo → rest
cfr src --from src/index.ts            # only files reachable from the entry (default order = deps)
cfr src --all --max-lines 250          # limit lines per file
cfr src --all --out bundle.txt         # write to a file instead of stdout
```

### 3. Filters

> Goal: scope to just the languages/file groups you want

```bash
cfr . --ext ts,tsx                            # extension filter
cfr . --include "src/**/*.ts"                 # glob vs root-rel path (repeatable, accepts csv)
cfr . --include "*.json" --include "*.toml"   # include non-source files too (override --ext)
cfr . --ext rs --no-ignore                    # include target/ dist/ too
```

### 4. Custom Import Patterns

> Goal: support framework/import styles the built-ins don't cover

```bash
cfr src --pattern '#include\s+"([^"]+)"'
cfr src --pattern 'from\s+([\w./-]+)\s+import' --ext py
```

- `--pattern` can be repeated — merges with the built-in extractor for that extension
- The first capture group must be the module specifier/path

### 5. Options Reference

> Goal: document every CLI flag with its default so callers don't guess

| Flag | Argument | Meaning |
|------|----------|----------|
| (default) | — | relation map `file → imports` |
| `--all` | — | concat all matching files |
| `--from` | `<file>` | concat only the entry + transitive internal deps (default `--order deps`) |
| `--summary` | — | stats + top imported internal files |
| `--json` | — | JSON `{root, files, edges, internal, graph}` |
| `--ext` | `<csv>` | filter extensions (default: `ts,tsx,js,jsx,mts,cts,rs,go,py,java,kt,kts,cs,vue,svelte`) |
| `--include` | `<glob>` | match root-rel path — repeatable/csv; override `--ext` to match non-source files (`*.json`, `*.toml`) |
| `--pattern` | `<regex>` | custom import matcher, capture group 1 = specifier (repeatable) |
| `--order` | `alpha\|deps\|smart` | concat order — `alpha` by name, `deps` topological (deps first), `smart` = config → entry → deps → rest |
| `--max-lines` | `<n>` | truncate each file in concat modes |
| `--no-ignore` | — | include `node_modules`, `.git`, `target`, `dist`, `build`, ... |
| `--out` | `<file>` | write output to a file instead of stdout |
| `-h`, `--help` | — | usage |

### 6. Interpret Results

> Goal: use the results in the main workflows

1. `[external]` = bare specifier/npm package — not resolved to a file in the tree
2. Resolved path = internal edge — used to find cycles, orphans, shared hubs
3. Pass the `--json` graph on to `/deep-review-codebase` (domain `review-architecture`) or other scripts via `/use-scripts`
4. The concat output is used by `/read-all-files` — `--order smart` for `all` mode, `--from <entry>` for related files

## Rules

### 1. Read-Only

- Never modify scanned files — writing only via `--out`/redirect
- `--all`/`--from` output may contain credentials — run `/check-secrets` before feeding it to an LLM

### 2. Performance

- Skips `node_modules`, `.git`, `target`, `dist`, `build`, `out`, `.next`, `.nuxt`, `.svelte-kit`, `coverage`, `.output`, `vendor`, `__pycache__` by default (use `--no-ignore` if needed)
- Very large codebase → scope with `--ext`, `--include`, sub-paths, or `--max-lines`

### 3. Accuracy

- Regex extraction is not a full parser — imports in comments, re-export chains, conditional imports, and macro-generated mods may be missed or over-matched
- Need higher precision → `/use-astgrep`, `/check-code-structure` (`sg outline --items imports`) or compiler APIs (`tsc --listFiles`, `cargo modules`) per the `/check-my-global-cli` tool map

## Expected Outcome

- Relation map: `file → imports` with resolved paths or `[external]`; `--summary` = the most-imported internal files; `--json` = a graph for downstream tooling
- Concat: a single `===== path =====` + content output in `alpha`/`deps`/`smart` order, or only the related set via `--from` — ready to pipe/redirect/feed into an LLM
