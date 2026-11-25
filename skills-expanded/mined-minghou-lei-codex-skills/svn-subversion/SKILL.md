---
name: svn-subversion
description: >-
  Use when a repository uses SVN/Subversion or a mixed Git+SVN workflow,
  especially on Windows working copies, Chinese paths, legacy encodings, game
  assets, release automation, status/diff/add/revert/update/commit/log/conflict
  tasks, branch/tag/merge/history operations, svn properties, externals,
  locks, or automation that must avoid mis-parsing paths, corrupting messages,
  committing the wrong scope, or treating SVN like Git.
---

# SVN Subversion

Use this skill to operate safely in SVN working copies and mixed Git/SVN trees.
The high-risk defaults are: use SVN machine output, preserve Windows/Chinese
path and message encodings, and commit only an explicit reviewed path set.

Command notes in the bundled references were validated against SVN 1.14.3 unless
they are explicitly marked as platform-specific or unverified.

## Core Rules

1. Parse structured output, not human text. Use `svn status --xml`,
   `svn log --xml`, and `svn info --show-item`; parse XML with a real parser.
2. Treat console encoding, pipe encoding, path encoding, and file-content
   encoding as separate layers. Set Windows UTF-8 handling before SVN commands.
3. Use UTF-8-no-BOM files for path lists and commit messages:
   `--targets targets.txt` where supported, plus `-F msg.txt --encoding UTF-8`.
4. Build and review a commit whitelist before every commit. SVN has no Git
   staging index; `svn commit <dir>` includes all local modifications below it.
5. Add `--non-interactive` in automation so auth, certificate, and conflict
   prompts cannot hang the run.
6. After `svn update`, query status for conflicts. A conflicting update can
   still exit 0.
7. After `svn add --force`, re-audit with `svn status --xml --no-ignore`; SVN
   can recursively schedule generated files and hidden children.
8. In Git+SVN checkouts, inspect both `svn status` and `git status` because the
   two tools track different local state.

## Safe Automation Shape

For scripts and repeatable agent work:

1. Run `svn cleanup --non-interactive` if the working copy may be locked.
2. Query state with `svn status --xml --no-ignore`.
3. Classify paths from XML entries.
4. Write a reviewed targets file as UTF-8 without BOM.
5. Write the commit message file as UTF-8 without BOM.
6. Run the SVN command with `--targets` only on subcommands that accept it.
7. Re-query `svn status --xml --no-ignore` and report remaining changes,
   conflicts, locks, and ignored/unversioned files that affect scope.

`--targets` is accepted by common path-based commands such as `commit`, `add`,
`delete`, `revert`, `info`, `lock`, `unlock`, `changelist`, `propset`, and
`log`. It is not accepted by `status` or `update`; pass paths positionally or
loop over a reviewed list for those commands.

## Daily Map

| Intent | SVN command | Notes |
|--------|-------------|-------|
| Status | `svn status --xml --no-ignore` | Script-safe; includes ignored items |
| Path info | `svn info --show-item <field> <path>` | Useful fields: `url`, `revision`, `wc-root` |
| Diff | `svn diff <path>` | Recursive by default; large diffs should go to a file |
| Add | `svn add <path>` | New files must be scheduled explicitly |
| Delete | `svn delete <path>` | Local paths schedule deletes; URLs commit immediately |
| Revert local edits | `svn revert <path>` | Not equivalent to `git revert <commit>` |
| Update | `svn update --accept postpone` | Check status after update |
| Commit | `svn commit --targets targets.txt -F msg.txt --encoding UTF-8 --non-interactive` | Prefer explicit scope |
| History | `svn log --xml <path-or-url>` | Use XML for scripts |

## Status Semantics

`svn status` is column-positional and not space-delimited. In scripts, prefer
XML. If text status must be read, the path starts at column 9.

| Status | Meaning | Safe response |
|--------|---------|---------------|
| `?` | Unversioned | Add only if in scope |
| `!` | Versioned but missing from disk | `svn delete` to remove, or `svn revert` to restore |
| `A` | Scheduled for add | Include added parent directories and children in commit targets |
| `D` | Scheduled for delete | Commit deliberately or revert |
| column-1 `M` | Content change | Inspect with `svn diff` |
| column-2 `M` | Property change | Inspect with `svn diff --properties-only` |
| `C` | Conflict | Inspect before resolving |
| `L` | Working-copy lock | Run `svn cleanup --non-interactive` |

Unversioned directories appear as one line and SVN does not enumerate their
children in status. Generated directories in engine repos must be filtered
before add/commit.

## Model Traps

- SVN has no staging index; changelists are useful but are not Git staging.
- Mixed-revision working copies are normal. Use `svn export URL@REV` for
  reproducible release inputs.
- Properties are versioned changes: `svn:eol-style`, `svn:mime-type`,
  `svn:ignore`, `svn:global-ignores`, `svn:needs-lock`, and `svn:mergeinfo`.
- `svn:ignore` is not `.gitignore` and is not recursive.
- `mine-full` and `theirs-full` discard the other side of a conflict.
- URL copy/move/delete operations commit immediately; working-copy path
  operations usually schedule local changes.
- Case-only renames on Windows need a temporary filename flow on
  case-insensitive filesystems.
- Garbled `????` output is usually display decoding, not repository damage;
  confirm with XML or `svn info` before destructive actions.

## Reference Files

Load only the file needed for the current task:

- [references/daily-commands.md](references/daily-commands.md): pre-flight,
  status/info parsing, where `--targets` works, update, add/delete/move,
  revert, commit, diff safety, cleanup, changelists, automation flags, and log.
- [references/encoding-and-paths.md](references/encoding-and-paths.md):
  Windows UTF-8 setup, Chinese path/message traps, TortoiseSVN Unicode path
  behavior, URL encoding, and file-content encoding cautions.
- [references/conflicts-and-merging.md](references/conflicts-and-merging.md):
  branch/tag/switch, merge and reverse-merge, conflict resolution, and tree
  conflicts.
- [references/properties-and-assets.md](references/properties-and-assets.md):
  `svn:ignore`, `svn:global-ignores`, EOL/MIME properties, binary asset locks,
  and stash workarounds.
- [references/automation-and-troubleshooting.md](references/automation-and-troubleshooting.md):
  machine-readable automation patterns, probing state, PowerShell exit-code
  traps, log capture, and Git+SVN update checks.
- [references/game-engine-shortcuts.md](references/game-engine-shortcuts.md):
  copy-paste snippets for engine repos, shader/C++ filters, changelist commits,
  subsystem reverts, and generated-directory ignore baselines.
