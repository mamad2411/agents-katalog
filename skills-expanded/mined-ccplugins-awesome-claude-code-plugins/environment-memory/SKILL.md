---
name: environment-memory
description: Use before retrying any command, tool, or approach that failed once, and immediately after discovering any OS/shell/tool-specific quirk — checks and updates a stable cross-project quirks file so failed approaches are never silently repeated.
---

# Environment Memory

## Overview

Trial-and-error against the same broken assumption — "maybe bash works this time" — wastes turns
and tokens without new information. Any OS, shell, or tool quirk discovered once should be usable
forever after, in every project, not just the one where it was found.

**Core principle:** a quirk discovered once should never be rediscovered by trial and error.

## The file

`~/.claude/craftsman-memory/environment-quirks.md` — deliberately outside this plugin's own
install directory, so a plugin update never wipes it. Deliberately outside any single project's
memory folder too, since quirks like "hooks run via CMD.exe not bash on this machine" apply
everywhere, not just to the project where they were found.

Format: flat, append-only, one line per entry —
```
<symptom> → <fix> (discovered: <date>, context: <where>)
```

No YAML frontmatter, no index, no categorization — this file is meant to be read in full whenever
it's relevant, so keep it short and skimmable rather than structured for querying (token-cheap by
design).

## Before retrying a failed command or approach

1. Check `~/.claude/craftsman-memory/environment-quirks.md` for a matching symptom before trying
   the same thing a second way, or a different way that might hit the same underlying constraint
   (e.g. "PowerShell syntax works where bash syntax silently no-ops" applies to any bash-syntax
   attempt, not just the exact command that first failed).
2. If a matching entry exists, apply its fix directly — don't re-verify from scratch unless the
   context has genuinely changed (different machine, different Claude Code version).

## After discovering a new quirk

1. Confirm it's actually environment/tool-specific (OS, shell, PATH, tool version) and not a
   one-off bug in the current task — this file is for durable facts about the machine/toolchain,
   not task-specific notes (those belong in `KNOWN_ISSUES.md` for the project instead).
2. Append one line in the format above. Don't ask before appending to this file specifically —
   unlike creating a new project file, this is pure append-only record-keeping with no
   file-creation side effect the first time it's used organically; do ask before creating the file
   itself if it doesn't exist yet, since that's a new file outside the current project.

## Notion / Obsidian

- Obsidian: the whole `~/.claude/craftsman-memory/` folder is a valid Obsidian vault as-is (plain
  markdown, no export step). Users can **Open folder as vault** on it to get search, backlinks, and
  graph view over the quirks log while Claude Code keeps writing the same files. Nothing here needs
  to change to support that — just keep the plain-markdown format intact.
- Notion: only mirror an entry to Notion when the user explicitly asks, or when closing out an
  entry they flagged as important. Never mirror automatically — this file is checked frequently
  and a network round-trip on every check would defeat the point of keeping it cheap.
