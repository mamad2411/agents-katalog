---
name: low-token-copy
description: Performs file copies, moves, and renames via shell ops (mv, cp, git mv) instead of read-then-write, and uses Grep + StrReplace for reference updates. Use when copying, moving, renaming, or relocating files or directories.
---

# Low Token Copy

Move files and update their references without ever reading file contents you do not need to edit. Reading a file just to re-emit it at a new path — or to change a few imports — is the anti-pattern this skill exists to prevent.

## Move Rule

1. Use a dedicated copy/move tool if the environment exposes one.
2. Otherwise use the OS-appropriate shell command below.
3. Move the directory, not its contents (`git mv old-dir new-dir`), so the operation is one call instead of N.
4. For tracked files, prefer `git mv` so rename history is preserved.
5. Only fall back to read + write when the destination must differ from the source in ways that genuinely require partial-content edits — and even then, copy first, then edit at the new path.

## Shell Examples

Pick the command that matches the current OS. Do not write a helper script just to perform a copy or move.

```bash
# macOS / Linux / POSIX
git mv "src/old-dir" "src/new-dir"          # tracked dir, preserves history
mv "old/path.ts" "new/path.ts"
cp "source/path.ts" "dest/path.ts"
cp -R "source/dir" "dest/dir"
mkdir -p "new/directory"
```

```powershell
# Windows PowerShell
git mv "src/old-dir" "src/new-dir"
Move-Item "old/path.ts" "new/path.ts"
Copy-Item "source/path.ts" "dest/path.ts"
Copy-Item -Recurse "source/dir" "dest/dir"
New-Item -ItemType Directory -Force -Path "new/directory"
```

## Reference Update Workflow

After the move, update references the cheap way:

1. **Grep first.** Find every file that references the old path. Grep returns file names, not contents — orders of magnitude cheaper than reading.

   ```bash
   rg "utils/legacy-helpers" --files-with-matches
   ```

2. **`StrReplace` with `replace_all`** instead of Read + Write. The `old_string` (e.g., the full old import path) is usually unique enough to replace blindly.

3. **Skip the pre-edit Read** when `old_string` is specific. If you need to confirm match count first, use `rg -c` — still far cheaper than reading the file body.

4. **Trust tool success reports.** Move and StrReplace both report what they did. Skip post-op verification reads unless something looked wrong.

## Anti-Patterns

- Reading a file into context just to re-emit it at a new path.
- Reading a whole file just to change a few imports — use Grep + StrReplace instead.
- Moving files one at a time when one `git mv directory` would do.
- Re-reading a file after a successful StrReplace or Move just to "confirm" it worked.
- Generating a temporary script file to perform a single copy or move.

## Common Slip Patterns

These are mistakes the agent — including the agent that wrote this skill — actually makes in practice. Each one looks innocent and is the exact thing the rules above are meant to prevent. Concrete examples to recognise:

### Slip 1 — "One more verify won't hurt"

```text
Tool 1: Move-Item "old" "new"; Get-ChildItem "new"   ← move + listing in one call ✓
Tool 2: Get-ChildItem -Recurse "new"                 ← second listing "to be sure" ✗
```

The first tool already returned the new tree. The second call adds latency and tokens for zero new information. **Rule: trust the first success report. Verify only when something looked wrong.**

### Slip 2 — "Read before edit, just in case"

```text
Tool 1: Read README.md           ← "I want to see current contents before editing" ✗
Tool 2: StrReplace README.md ... ← old_string was unique; Read was unnecessary
```

If the `old_string` is specific (a full path, a unique import line, a code-fenced block), `StrReplace` will succeed without a prior `Read`. If you need to confirm the match exists, `rg -c "old_string"` is ~20 tokens vs the file body's hundreds-to-thousands. **Rule: only Read when StrReplace would genuinely be ambiguous.**

### Slip 3 — "Cleanup as a separate call"

```text
Tool 1: New-Item dir; Move-Item "old" "new"                       ← move ✓
Tool 2: Remove-Item "old/leftover-empty-dir" -Recurse             ← cleanup as second call ✗
```

Filesystem cleanup that you already know about should be chained into the same shell call as the move:

```powershell
New-Item -ItemType Directory -Force -Path "tests/fixtures" | Out-Null
Move-Item "src" "tests/fixtures/sample"
Remove-Item "tests/fixtures/sample/leftover" -Recurse -Force -EA SilentlyContinue
```

**Rule: one shell call per logical operation, even if that operation is three sub-commands.**

### Slip 4 — "I'll Grep, but I'll also Read each hit"

```text
Tool 1: Grep "old-path" --files-with-matches  → returns 3 paths ✓
Tool 2: Read file1.ts                          ← reads 600 tokens ✗
Tool 3: Read file2.ts                          ← reads 800 tokens ✗
Tool 4: Read file3.ts                          ← reads 400 tokens ✗
Tool 5–7: StrReplace each file
```

Grep already proved the `old_string` exists in each file. Going straight to `StrReplace replace_all` skips the Reads entirely. **Rule: Grep + StrReplace is a two-step pipeline, not a Grep + Read + StrReplace three-step one.**

## Required Follow-Up

After moves and reference updates:

1. Update tests, mocks, fixtures, and snapshots that hardcode paths.
2. Update docs, configs, and build manifests that hardcode paths.
3. Delete obsolete originals only after confirming no remaining references (`rg "old/path"`).
4. Run targeted verification (typecheck, lint, or test) for the affected area.
