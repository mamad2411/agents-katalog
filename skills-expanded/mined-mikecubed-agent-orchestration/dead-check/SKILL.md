---
name: dead-check
description: >
  Enforces dead code elimination rules (DEAD-1 through DEAD-5). Loaded by the
  conductor for review, refactor, and cleanup operations. Detects commented-out
  code, unused exports, orphaned files, unlinked TODOs, and stub/placeholder
  functions. References scripts/lint_dead_code.py for export and orphan
  detection.
version: "1.0.0"
last-reviewed: "2026-03-04"
languages: [typescript, python, go, rust, javascript]
changelog: "../../CHANGELOG.md"
tools: Read, Grep, Glob, Bash
model: opus
permissionMode: default
---

# Dead Check — Dead Code Elimination

**Hook coverage check (run first)**:
Before running DEAD-1 detection, check whether the hook already flagged
commented-out code blocks in this session for the file(s) in scope:

```bash
cat "$COVERAGE_FILE" 2>/dev/null   # COVERAGE_FILE = /tmp/codex-hook-coverage-<PROJECT_HASH>.jsonl
```

For each JSON line where `"rule"` is `"DEAD-1"`, extract `file`, `line`, and
`end_line`. When scanning, skip any file+line range that matches an existing
coverage record.
Log: `"Skipping DEAD-1 at {file}:{line}-{end_line} — already reported by hook this session."`

If no coverage file exists, proceed with the full DEAD-1 analysis.

**For unused export and orphan detection**: invoke
`scripts/lint_dead_code.py --path {scope}` and parse its JSON output.
Requires **Python 3.12+** (`python3.12 scripts/lint_dead_code.py --path {scope}`).

Precedence in the overall system: SEC → TDD → ARCH/TYPE → **NAME/SIZE/DEAD** →
quality BLOCK.

---

## What Counts as Dead Code

| Category              | Description                                                  |
|-----------------------|--------------------------------------------------------------|
| Commented-out code    | Any block of syntactically valid code inside a `//` or `/* */` comment |
| Unused export         | An exported symbol with zero import references in the codebase |
| Orphaned file         | A source file unreachable from any entry point via imports   |
| Unlinked TODO         | `TODO:` / `FIXME:` / `HACK:` without an issue tracker reference |
| Stub / placeholder    | Function body that is only `pass`, `throw new Error('not implemented')`, `todo!()`, `unimplemented!()` |

---

## Rules

### DEAD-1 — No Commented-Out Code
**Severity**: BLOCK | **Languages**: * | **Source**: CCC

**What it prohibits**: Blocks of code that have been commented out rather than
deleted. This includes single-line and multi-line commented code, regardless of
how recently it was added.

**Exemptions** (not flagged):
- Single-line explanatory comments (non-code English prose)
- JSDoc / rustdoc / godoc comment blocks above declarations
- `//nolint:`, `# noqa:`, `#[allow(...)]` suppression comments
- Example code inside documentation comments (within `///` or `/** */`)

**Detection**:
1. Grep for comment blocks where the content after removing comment markers
   (`//`, `#`, `/*`, `*`) is valid code syntax:
   - Contains assignment operators (`=`, `:=`)
   - Contains function call patterns (`name(`)
   - Contains control flow (`if `, `for `, `while `, `return `)
   - Contains closing braces/parens (`}`, `)`) at line start
2. Multi-line comment blocks where ≥ 3 consecutive lines match the above
3. Flag each occurrence

**agent_action**:
1. Cite: `DEAD-1 (BLOCK): Commented-out code block at {file}:{start_line}-{end_line}.`
2. Show the commented block
3. State: "This code should be deleted. Git history preserves it if needed."
4. If `--fix`: delete the commented block (no confirmation required — git is
   the backup)
5. DO NOT preserve commented-out code when writing or refactoring

**Bypass prohibition**: "I might need it later", "it's a reference",
"it documents what was tried" → Refuse. Cite DEAD-1. Write a commit message.
Delete the code.

---

### DEAD-2 — No Unused Exports
**Severity**: WARN | **Languages**: typescript, javascript, python, rust | **Source**: CCC

**What it prohibits**: Exported/public symbols (functions, classes, constants,
types) that are not imported or referenced anywhere in the codebase. These
inflate public API surface area and imply tests must be written for them.

**Go note**: Go's compiler enforces unused imports natively. Unexported symbols
in Go are not flagged by this rule — only exported (PascalCase) symbols.

**Detection**:
1. Run: `python3.12 scripts/lint_dead_code.py --path {scope}`
2. Parse JSON output — `unused_exports` array
3. Each entry: `{ "file": "...", "line": N, "symbol": "..." }`

**agent_action**:
1. Cite: `DEAD-2 (WARN): Unused export '{symbol}' at {file}:{line}.`
2. Ask: "Is this export part of a public library API intended for external
   consumers?" If yes → add a suppression waiver. If no → delete.
3. If `--fix` and confirmed not part of public API: remove the export and its
   declaration if it has no internal usages either
4. Do not remove if any external consumer may exist (library context)

---

### DEAD-3 — No Orphaned Files
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: Source files that are not reachable from any entry point
via the import graph. Orphaned files are often the remains of deleted features
or refactored modules that were never cleaned up.

**Entry points** (heuristic — adapt to project):
- `index.ts` / `main.ts` / `app.ts` / `server.ts`
- `main.py` / `__main__.py`
- `main.go`
- `main.rs`
- Test files (`*.test.*`, `test_*.py`, `*_test.go`, `#[cfg(test)]` modules)

**Detection**:
1. Run: `python3.12 scripts/lint_dead_code.py --path {scope}`
2. Parse JSON output — `orphaned_files` array
3. Each entry: `{ "file": "...", "reason": "..." }`

**agent_action**:
1. Cite: `DEAD-3 (WARN): Orphaned file '{file}' — not reachable from any entry point.`
2. Show possible reasons: deleted import, renamed module, leftover scaffold
3. **⚠️ Requires explicit confirmation before deletion** — even in `--fix` mode
4. Present: "Proposed action: delete `{file}`. Proceed? (y/n)"
5. Only delete after explicit `y` confirmation

---

### DEAD-4 — TODOs Must Reference an Issue Tracker
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: `TODO:`, `FIXME:`, `HACK:`, `XXX:`, `BUG:` comments that
do not reference an issue tracker ticket. Unlinked TODOs become permanent
fixtures. Every deferred item must have an owner and a tracking number.

**Compliant formats**:
```
// TODO(#123): Implement retry logic after rate limiting
// TODO(GH-456): Remove after migration to v2 API
# FIXME(JIRA-789): Handle None case for legacy records
// HACK(#234): Temporary workaround for upstream bug — remove after v3.1
```

**Non-compliant formats**:
```
// TODO: fix this later
// FIXME: handle error
// HACK: temporary workaround
```

**Detection**:
1. Grep for `TODO:`, `FIXME:`, `HACK:`, `XXX:`, `BUG:` without a `(#...)` or
   `(GH-...)` or `(JIRA-...)` or `([A-Z]+-[0-9]+)` pattern immediately after

**agent_action**:
1. Cite: `DEAD-4 (WARN): Unlinked TODO at {file}:{line}: '{comment}'.`
2. Propose conversion: `TODO: {text}` → `TODO(#{issue_number}): {text}`
3. If no issue exists yet: "Create an issue for '{text}' and add the reference."
4. If `--fix`: convert format to `TODO(#?): {text}` with `?` as placeholder,
   noting that the issue number must be filled in

---

### DEAD-5 — No Placeholders or Stubs in Production Code
**Severity**: BLOCK | **Languages**: * | **Source**: CCC

**What it prohibits**: Functions in non-test code whose body consists only of:
- `pass` (Python)
- `throw new Error('not implemented')` / `throw new Error('TODO')` (TypeScript/JavaScript)
- `todo!()` / `unimplemented!()` (Rust)
- `panic("not implemented")` (Go)
- An empty body `{}`

These are scaffolding artifacts. They imply a contract without delivering it
and will cause runtime failures when called.

**Exemptions**:
- Abstract method declarations in abstract classes (the stub IS the contract)
- Interface method signatures (no body)
- Test doubles / mocks in test files (`*.test.*`, `test_*.py`, etc.)

**Detection**:
1. Grep for `throw new Error('not implemented')`, `todo!()`, `unimplemented!()`,
   `panic("not implemented")` outside test files
2. Grep for single-statement function bodies containing only `pass` (Python),
   in non-test files

**agent_action**:
1. Cite: `DEAD-5 (BLOCK): Stub/placeholder function '{name}' at {file}:{line}.`
2. Options:
   - If this is a planned feature: create an issue, replace with a DEAD-4
     compliant TODO comment above the function, and implement a minimal real
     body (even if it returns a zero value)
   - If this is scaffolding that was never implemented: delete the function
     and all call sites
3. DO NOT produce code that calls or wraps a stub function

**Bypass prohibition**: "I'll implement it later" → Refuse. Cite DEAD-5.
Either implement the minimum viable version or delete it and track via issue.

---

Report schema: see `skills/conductor/shared-contracts.md`.
