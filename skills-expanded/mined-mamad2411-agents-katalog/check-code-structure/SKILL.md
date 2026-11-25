---
name: check-code-structure
description: Analyze and improve code structure with sg outline: symbols, exports, members, cohesion
argument-hint: "[scope]"
allowed-tools:
  - exec
  - grep
  - glob
  - find_file_by_name
related:
  - deep-analyze
  - use-astgrep
  - deep-review-codebase
  - refactor
  - deep-validate
  - scan-codebase

---

## Goal

Analyze and improve micro-level code structure with `sg outline` to fix top-level symbols, exports, members, SRP violations, and cohesion issues

## Scope

Applies to source code that needs structural cleanup, such as `src/` or any single workspace. Covers top-level symbols, exports, imports, members, and code grouping patterns. It is a sub-step of `/deep-analyze` Step 3

See more: /use-astgrep, /deep-review-codebase

## Execute

### 1. Review And Inventory

> Goal: Review And Inventory

1. Run `/scan-codebase` to understand the project structure
2. Run `/update-astgrep-rules` if there are relevant `ast-grep` rules (`rules/`)
3. Read `## Sg Outline` below to understand how to use `sg outline` and its available options
4. Choose `sg outline` flags according to scope (see `## Sg Outline`)
5. Identify the target paths to improve
6. If `sg outline` is unavailable → stop and report

### 2. Analyze Code Structure

> Goal: Analyze Code Structure

1. Read `## Sg Outline` to pick the flags that fit the scope
2. Run `sg outline` with the chosen flags:
   - `sg outline --view expanded --items structure <paths>` for top-level symbols and members
   - `sg outline --view signatures --items exports <paths>` for the exported surface
   - `sg outline --json compact --items all <paths>` for structured aggregation
3. Use `sg outline --items imports` to inspect import/export relationships between modules
4. For a large scope, use `--type` or `--match` to cut down noise
5. If the analysis fails → re-run; if it still fails after 3 attempts → stop and report

### 3. Identify Structure Issues

> Goal: Identify Structure Issues

Goal: identify structure issues from `sg outline` output before starting any cleanup

1. Check top-level symbols per file: more than 5 may signal mixed concerns
2. Check members per type/class: more than 10 may violate SRP
3. Check exports that shouldn't be public: internal utilities, helper types
4. Check imports that cross a boundary or layer
5. Check files that mix symbols from several domains or layers
6. Use `/use-astgrep` for patterns `sg outline` doesn't cover, such as God classes
7. If a filesystem review is also needed, run `/deep-review-codebase` separately
8. For a deeper review of refactor opportunities, run `/deep-review-codebase` separately

### 4. Validate Findings

> Goal: Validate Findings

1. Run `/deep-validate` to validate the findings
2. Rank severity: Critical → High → Medium → Low
3. Note the false positives found
4. If there are no issues to improve → stop and report

### 5. Improve Code Structure

> Goal: Improve Code Structure

Goal reminder: improve code structure according to the findings from Step 3

1. Split files with more than 5 top-level symbols into smaller files by domain or responsibility
2. Reduce public members in types/classes that exceed 10 by extracting them into a sub-type or helper
3. Run `/deep-review-codebase` to handle barrel exports and import aliases — hide internal exports that needn't be public, replace convoluted relative paths
4. Fix imports that cross a boundary or layer
5. Separate files that hold symbols from multiple domains
6. Use `/rename` to rename identifiers and `/update-references` after every split or rename
7. If the physical structure needs adjusting, run `/refactor` structure scope

### 6. Verify

> Goal: Verify

1. Read `## Sg Outline` to confirm how to use `sg outline` for verification
2. Re-run `sg outline --items structure <paths>` to confirm the issues were fixed
3. Run `sg outline --items exports <paths>` to check that the public API didn't change unintentionally
4. Run `/run-verify` lint and typecheck
5. If it fails, run `/resolve-errors`
6. If it still fails after 3 attempts → stop and report

### 7. Report

> Goal: Report

1. Run `/report`
2. Build the Structure Metrics table: File, Top-Level Symbols, Exports, Public Members, Status
3. Build the Improvements table: File, Issue Type, Action Taken, Severity, Result
4. Build the Recommended Actions table: Priority, Action, Impact, Workflow
5. Run `/suggest-next-action` to recommend the next action

## Rules

### 1. Severity Classification

- Critical: circular import, cross-layer import, files with multiple domains on a critical path, exported internal API that breaks a boundary
- High: files exceeding 5 unrelated top-level symbols, types/classes exceeding 10 public members, files in the wrong layer
- Medium: files with 4-5 top-level symbols, types with 6-10 members, inconsistent exports
- Low: naming that doesn't reflect responsibility, inconsistent export style

### 2. Evidence-Based Findings

- Every finding must carry a file path, line number, or symbol name from `sg outline`
- Use `sg outline` as the primary evidence; don't guess
- Note the false positives

### 3. Review Before Improve

- Fully analyze and validate the findings before starting to improve
- For a deep refactor, run `/deep-review-codebase` separately before improving
- Keep the improvement process separate from other review processes such as `/deep-review-codebase`

### 4. Follow Write Standards

- Run `/update-references` after every split, rename, or file move
- Use `/rename` to rename code identifiers that don't reflect responsibility
- Keep each file at or under 250 lines
- Each function/type/class does one job
- Use `sg outline` to confirm the structure after improving

### 5. sg outline Flags

See all flags and options in `## Sg Outline` below

### 6. Scope Boundaries

- Don't improve the architecture that `/deep-review-codebase` handles
- Don't improve the filesystem organization that `/deep-review-codebase` handles
- Don't do the deep separation-of-concerns refactoring that `/refactor` handles
- Focus on code-level structure: symbols, exports, members, cohesion
- For a system-wide view, run `/deep-review-codebase`

- Use /use-astgrep-programmatic if needed

## Sg Outline

> Goal: use `sg outline` (`ast-grep outline`) to explore code structure without building an index

### Basic Usage

```bash
sg outline src/parser.ts          # file → items=structure, view=digest
sg outline src                    # directory → items=exports, view=names
sg outline src/a.ts src/b.ts      # multiple files
```

### Items (`--items`)

| Value | Meaning |
|-------|---------|
| `auto` | `structure` for file/stdin, `exports` for directory (default) |
| `structure` | top-level items in a file (excluding imports) |
| `exports` | exported top-level items |
| `imports` | imported items/dependencies |
| `all` | imports + exports |

### View (`--view`)

| Value | Meaning |
|-------|---------|
| `names` | grouped name lines per symbol type |
| `signatures` | one signature line per top-level item |
| `digest` | signatures + compact member digests (default file) |
| `expanded` | signatures + one line per direct member |

### Filters

```bash
sg outline src --type class,enum                 # filter by symbol type (OR)
sg outline src --match Parser                    # regex on symbol names
sg outline src --items imports --match lodash    # imports matching a dependency
sg outline src --view expanded --pub-members     # public members only
sg outline src/parser.ts --match Parser --type class --view expanded  # expand a single symbol
sg outline src --json compact --items all        # machine-readable output
```

### Symbol Types (`--type`)

LSP `DocumentSymbol.kind` — `class`, `function`, `interface`, `method`, `property`, `field`, `constructor`, `enum`, `enumMember`, `struct`, `module`, `namespace`, `variable`, `constant`, `typeParameter`, etc. — lower camel case, comma = OR

### Stdin And Rules

- stdin input always requires `--lang`
- extraction rules: bundled per language; custom via `customLanguages.<name>.outlineRules` in `sgconfig.yml` or `--outline-rules <file>`; `--no-default-outline-rules` replaces the bundled ones
- exit codes: `0` = ok (including empty), `2` = fatal read/parse/config error

### When To Use

- Use: view structure/exports/members before reading a file, check dependencies, filter symbols
- Don't use: pattern search (`ast-grep run`/`scan`), rewriting code, cross-file analysis (local-only), semantic relationships (doesn't normalize extends/implements)

## Expected Outcome

- Code structure improved: symbols per file, exports, members, and cohesion within thresholds
- Report the Structure Metrics table with status before and after improving
- Report Improvements with file, issue, action, severity, result
- Report Recommended Actions with priority and workflow
- Note the false positives found
- Recommend the next action via `/suggest-next-action`
