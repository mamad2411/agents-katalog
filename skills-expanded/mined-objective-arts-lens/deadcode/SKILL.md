---
name: deadcode
description: Detecting and removing dead code across polyglot projects to eliminate unused exports, unreachable code, unused dependencies, and orphaned files when users want to find dead code, clean up unused code, or remove unused exports. Requires language-specific tools (knip for JS/TS, vulture for Python, deadcode for Go). Respects @keep markers. Does NOT auto-delete without confirmation, touch test files, or analyze node_modules/vendor directories.
allowed-tools:
  - Bash(npx knip*)
  - Bash(uvx vulture*)
  - Bash(go run golang.org/x/tools/cmd/deadcode*)
  - Bash(cargo +nightly udeps*)
  - Read
  - Grep
  - Glob
  - Edit
  - Write
  - AskUserQuestion
---

# Dead Code Detection

## Purpose
Find and remove dead code across polyglot codebases using best-in-class static analysis tools.

## When to Use
- User asks to "find dead code" or "detect unused code"
- User wants to "clean up unused exports" or "remove dead functions"
- User asks "what's unused in this project"
- Pre-refactor cleanup to identify removable code

## When NOT to Use
- User wants runtime coverage analysis (use coverage tools instead)
- User wants to find duplicate code (use jscpd or similar)
- Single-file analysis only (tools work at project level)

## Process

### 1. Detect Project Languages
Scan for language markers:
- `package.json` / `tsconfig.json` → JavaScript/TypeScript
- `pyproject.toml` / `requirements.txt` / `*.py` → Python
- `go.mod` → Go
- `Cargo.toml` → Rust

### 2. Run Language-Specific Tools

<critical>Always run in report mode first. Never delete without showing results.</critical>

| Language | Tool | Command |
|----------|------|---------|
| JS/TS | knip | `npx knip --reporter compact` |
| Python | vulture | `uvx vulture . --min-confidence 80` |
| Go | deadcode | `go run golang.org/x/tools/cmd/deadcode@latest -test=false ./...` |
| Rust | cargo-udeps | `cargo +nightly udeps --all-targets` |

### 3. Filter Results
Remove from consideration:
- Lines containing `@keep` or `// keep` or `# keep`
- Files in test directories (`**/test/**`, `**/__tests__/**`, `**/*_test.*`, `**/*.test.*`)
- Files in `node_modules/`, `vendor/`, `.venv/`, `target/`

### 4. Present Findings
Group by category:
```
## Unused Exports (12 items)
- src/utils/helpers.ts: formatDate, parseQuery, oldValidator
- src/api/client.ts: deprecatedFetch

## Unused Dependencies (3 items)
- lodash (package.json)
- moment (package.json)

## Unreachable Code (2 items)
- src/auth/login.ts:45-52 (after return statement)

## Unused Files (1 item)
- src/legacy/old-parser.ts (no imports found)
```

### 5. Confirm Before Removal

<never>Delete code without explicit user confirmation</never>

Ask user:
```
Found [N] items of dead code. Options:
1. Remove all (I'll create a backup branch first)
2. Remove by category (choose which types)
3. Review individually (confirm each item)
4. Export report only (no changes)
```

### 6. Apply Fixes
For confirmed removals:
- **Unused exports**: Remove export keyword or entire declaration
- **Unused dependencies**: Remove from package.json/requirements.txt/etc.
- **Unreachable code**: Delete the unreachable lines
- **Unused files**: Delete the file (after final confirmation)

<critical>Create a git stash or branch before bulk deletions: `git stash push -m "pre-deadcode-cleanup"`</critical>

### 7. Verify
After removal:
- Run the tool again to confirm reduction
- Run project's test suite if available
- Report: "Removed X items. Dead code reduced from Y to Z."

## Tool Installation

If tools are missing, offer to install:
```bash
# JS/TS
npm install -D knip

# Python (no install needed, uvx runs directly)

# Go (no install needed, go run fetches)

# Rust
cargo install cargo-udeps
```

## Output Contract

Final report includes:
1. Summary: items found, items removed, items skipped (@keep)
2. Backup location (git stash or branch name)
3. Verification: tool re-run showing remaining issues
4. Next steps: any manual review recommended

## Limitations

- **Dynamic requires**: `require(variable)` can't be statically analyzed
- **Reflection**: Languages with heavy reflection may have false positives
- **Entry points**: Ensure tools know your entry points (knip uses package.json exports)
- **Monorepos**: May need workspace configuration

<avoid>
- Removing code that looks unused but is accessed via reflection/dynamic import
- Deleting public API surface without checking external consumers
- Running on uncommitted changes (always commit or stash first)
</avoid>
