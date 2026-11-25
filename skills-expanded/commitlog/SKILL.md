---
name: commitLog
description: Write the log entry every log-cli commit needs, in the day's file log/<date>.md (indexed from log.md). On commit, the pre-commit hook parses the staged code into an abstract syntax tree (AST), writes which declarations and tests were added, changed or removed into a template entry, and feeds that back to the agent. The agent then writes What changed, Why and Checked from the AST before the commit can go through.
---

# commitLog

The log is the running record of the repo, one entry per commit. It is kept
in one file per day, `log/<date>.md` (the day in UTC, newest entry at the
bottom), and `log.md` is the index of every day, newest first. One file was
too big for GitHub to show (1.6 MB), a day's file isn't. lefthook's pre-commit (`lefthook.yml`) runs `scripts/commitLog/commitLog.mjs`, which uses
`scripts/commitLog/astSummary.mjs`:

- `.ts` / `.mjs` files are parsed with the TypeScript compiler API.
- `.py` files are parsed with Python's own `ast` module.
- For each file it compares the syntax tree before and after the change and
  lists what was added, changed or removed: top-level functions, classes,
  interfaces, types, enums, consts, re-exports, and test titles in
  `*.test.ts`. Formatting-only edits don't count as changes.

## Hard boundaries

1. **Every commit gets an entry.** No `--no-verify`, ever.
2. **Never edit the AST block.** The tool writes it. If it looks wrong, fix
   `scripts/commitLog/astSummary.mjs`, not the entry. The hook rejects a block that
   doesn't match the staged code, and rewrites it.
3. **Never edit old entries.** Only add.
4. **Write the three fields from the AST,** in plain words, naming the real
   behaviour, commands and results. No `<fill in>` left.

## The routine

```bash
GIT_CONFIG_COUNT=0 git add <files>
GIT_CONFIG_COUNT=0 git commit -m "..."
# 1st try: the hook prints the AST of the staged change, appends the entry
#          to today's log/<date>.md, updates the index log.md, and stops the commit
# write What changed / Why / Checked under the AST block
GIT_CONFIG_COUNT=0 git add log.md log
GIT_CONFIG_COUNT=0 git commit -m "..."
# 2nd try: the hook re-parses the staged code; if it matches the block and the
#          fields are written, the commit goes through
```

If you change code after the entry was written, the hook updates the AST
block in place and stops once more. Re-read your What changed line, re-stage
`log.md log`, commit again. If only the index is stale, the hook rewrites
log.md and asks for `git add log.md`.

To see the AST for any commit: `node scripts/commitLog/astSummary.mjs <commit>`. With
no argument it shows the staged change.

## The entry

```markdown
## 2026-10-18 05:40Z · feat/branchName

AST (generated from the staged code by scripts/commitLog/astSummary.mjs, don't edit):
- `src/camofox/worker/helpers/fromCamofoxStatus.ts`: added function fromCamofoxStatus
- `src/cli/live/index.ts`: added const connectCommand · removed const loginCommand

What changed: <fill in>
Why: <fill in>
Checked: <fill in>
```

- **What changed**: the behaviour behind the AST lines. Example: "`log facebook connect`
  replaces `log login` for Facebook sessions", not "edited index.ts".
- **Why**: the request or bug behind it. Quote matt's ask when there is one.
- **Checked**: the exact command and its result (`bun run check`: 62 pass),
  plus any real run. Say what you didn't check.

If the commit also adds a rule from matt, `skills/captureRule/SKILL.md`
applies too.
