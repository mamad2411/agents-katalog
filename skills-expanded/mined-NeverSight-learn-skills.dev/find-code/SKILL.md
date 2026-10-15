---
name: find-code
description: Locate files and code using grep and shell scripts — never by AI scanning. Returns exact file paths and line numbers so the agent can jump directly to the location. Use whenever the agent needs to find a function, class, variable, import, file, or any pattern in the codebase. Code and file discovery must always be a tool call, never an AI guess.
---

# Find Code

**Rule**: Never scan the repo with AI. Run a tool, read the results, go directly to the file or refine the search and run again.

## Quick Start

```bash
# Find anything by pattern
bash <skill-dir>/scripts/find.sh "createUser"

# Find a file by name
bash <skill-dir>/scripts/find.sh --file "userService"

# Find where a symbol is defined
bash <skill-dir>/scripts/find.sh --def "createUser"

# Find all callers of a function
bash <skill-dir>/scripts/find.sh --callers "createUser"
```

Output is always `file:line: content` — use the file path and line number to jump directly.

## Workflow

### 1. Choose a search mode

| Goal | Command |
|---|---|
| Find text / regex anywhere | `find.sh "pattern"` |
| Find a file by name | `find.sh --file "name"` |
| Find where symbol is defined | `find.sh --def "SymbolName"` |
| Find all callers / usages | `find.sh --callers "SymbolName"` |
| Find all imports of a module | `find.sh --imports "moduleName"` |
| Find by file type | `find.sh "pattern" --ext ts` |
| Find in a specific folder | `find.sh "pattern" --in src/services` |

### 2. Read results — never re-scan

Results come back as:
```
src/services/userService.ts:14:export async function createUser(
src/handlers/users.ts:31:  const user = await createUser(body);
```

Each line tells you: **which file**, **which line**, **what's there**. Navigate directly — do not open other files to double-check.

### 3. Refine if needed

If results are too broad, narrow the search:
```bash
# Too many results → scope to a folder
bash <skill-dir>/scripts/find.sh "create" --in src/services

# Still too broad → add file type filter
bash <skill-dir>/scripts/find.sh "create" --in src/services --ext ts

# Looking for exact function signature
bash <skill-dir>/scripts/find.sh --def "createUser" --ext ts
```

If results are empty, broaden:
```bash
# Try case-insensitive
bash <skill-dir>/scripts/find.sh "createuser" --flags "-i"

# Try filename only
bash <skill-dir>/scripts/find.sh --file "user"
```

### 4. Jump to the file

Once you have `file:line`, read only that file starting at that line:
```bash
# Agent reads file at the exact line — no re-scanning
```

## Guardrails

- Never use AI to guess file locations — always run `find.sh` first.
- Never open a file to search inside it — run another `find.sh` instead.
- Results cap at 50 lines by default. If truncated, narrow the search rather than raising the limit.
- Do not chain more than 3 refinements without reporting back to the user.

## References

- [REFERENCE.md](REFERENCE.md) — grep recipes, regex patterns by language, common search scenarios.
