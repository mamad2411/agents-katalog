> ⚠️ PROJECT SCOPED: Read/write .claude/skills/ only.

Manages the local skill cache. Behaviour depends on argument.

## /r-cache warm — rebuild all cache files from memory (do this after /r-memory scan)

1. Read .claude/memory/context.md, rules.md, patterns.md, gotchas.md, dependencies.md
2. Read ALL files in .claude/modules/

Rebuild _base.md with: project name + stack, top 10 rules, top 5 patterns, top 10 gotchas, timestamp.
Rebuild _stack.md with: stack + source folders, stack-specific rules, dev commands, timestamp.
Rebuild _modules-index.md with: one row per module (name | file | confidence | last updated), timestamp.

Report: ✅ _base.md / ✅ _stack.md / ✅ _modules-index.md rebuilt.
⚡ Cache is WARM — future commands load skills/ first.
Remind: commit .claude/skills/ so teammates benefit.

## /r-cache status — check cache health (read-only)

Read all three cache files.
Report:

| File                                                              | Status            | Generated   | Size          |
| ----------------------------------------------------------------- | ----------------- | ----------- | ------------- |
| _base.md                                                          | 🟢 Warm / 🔴 Cold | [timestamp] | [lines] lines |
| _stack.md                                                         | 🟢 Warm / 🔴 Cold | [timestamp] | [lines] lines |
| _modules-index.md                                                 | 🟢 Warm / 🔴 Cold | [timestamp] | [X] modules   |
| Overall: 🟢 All warm / 🟡 Partial / 🔴 All cold                   |
| Suggest /r-cache warm if any file is 🔴 Cold or timestamp is old. |

## /r-cache (no argument) — defaults to status
