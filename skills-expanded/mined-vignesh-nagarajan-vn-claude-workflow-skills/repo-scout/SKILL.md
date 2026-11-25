---
name: repo-scout
description: Get oriented in an unfamiliar or large repo from one compact map instead of reading files. Use at the start of work in a repo with no CLAUDE.md, when asked what a codebase does or where something lives, before any broad or cross-cutting change, and whenever the alternative is opening several files just to find the entry point. Runs scripts/repo_scout.py.
---

# repo-scout

Orientation is where sessions leak the most tokens. Opening eight files to learn what a repo is costs thousands and still misses the layout. One script pass costs a few hundred and answers the same question better.

## Order of operations

Check for a `CLAUDE.md` first. If one exists and its dates look current, read that and stop, it already is the map.

Otherwise:

```bash
python <skill>/scripts/repo_scout.py
```

That reports the stack, entry points, directories ranked by size, the largest files, the files changed most recently, and where the docs are.

Then open the files the map points to for your question, usually two or three. Open a file for what the map cannot tell you, such as behavior and conventions, not to confirm what it already said.

## Flags

| Flag | Effect |
| --- | --- |
| `--dir lib` | Scope to a subtree. Use on a monorepo, one package at a time. |
| `--since "7 days ago"` | Change the window for the recently-changed list. Default is 30 days. |
| `--budget 60` | Cap output lines. Lower it on a huge repo. |
| `--json` | Machine readable. |

## Reading the output

**Recently changed** is the most useful section and the least obvious. It ranks files by commit count in the window, which is where the work actually is. On an unfamiliar repo this beats the directory listing for deciding what to read.

**Largest files** are where the logic concentrated. A file over about a thousand lines is usually the core of whatever it belongs to.

**Entry points** come from manifests and framework conventions. When the list is empty the repo is a library, so read the public export surface instead.

## After scouting

If the repo has no `CLAUDE.md` and you are going to work in it more than once, that is the moment to write one. See [agent-contract](../agent-contract/SKILL.md). The map you just generated is most of the input.

## What this does not do

It does not read code semantics, trace call graphs, or find bugs. It tells you where to look. For a targeted question about behavior, grep for the symbol instead of scouting:

```bash
git grep -n "functionName" -- "*.ts"
```
