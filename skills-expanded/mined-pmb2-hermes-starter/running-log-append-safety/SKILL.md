---
name: running-log-append-safety
description: "Append to running logs: patch displacement, MSYS paths."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [pulse, cron, logs, appending, PULSE.md, digest, changelog, running-log, write_file, patch]
    triggers: [append to log, pulse entry, PULSE.md, daily digest, changelog entry, append findings, running log, journal entry]
    related_skills: [recurring-status-checks, discord-report-format, systematic-debugging, fix-verification]
---

# Running Log Append Safety

How to append entries to multi-entry running logs (PULSE.md, daily digests, changelogs, findings journals) WITHOUT destroying or reordering existing content. Applies to pulse/cron cycles and interactive maintenance.

## The Rules

1. **`write_file` ALWAYS replaces the whole file** — it has no append mode. Only use it after a FULL read (no offset/limit), then write existing + new content. It warns on partial-view writes; heed the warning.
2. **`patch`-anchor appends can DISPLACE adjacent trailing lines.** The fuzzy matcher treats the anchor + following content as one region. If the file ends with `entry body ... final bullet` followed by more lines (e.g. a trailing `- **Next Action**` line), the trailing line can be re-emitted AFTER the inserted entry — orphaned from its own entry. Treat patch-anchor appends as insert-BETWEEN, never append-AFTER.
3. **ALWAYS read back the tail after any append** (last ~20 lines) and verify every entry is complete and in order. The returned unified diff shows the displacement as a `-` deletion with no `+` re-add in the original position — that's the detection signal. Fix immediately: (a) restore the displaced line under its own entry, (b) remove the orphaned duplicate at EOF.
4. **Digest scripts on Windows: pass `E:/...` paths, never `/e/...` MSYS paths.** `python` in cron resolves to the native Windows runtime with no MSYS path translation — `python ${MY_REPOS}/.../append-digest.py` fails with `can't open file 'C:\e\yourdata\...'`. Use `python "${MY_REPOS}/.../append-digest.py"` (forward slashes work in native python).

## Worked Example (Forge pulse 2026-08-11)

Appended a new entry to PULSE.md via `patch` anchored on the previous entry's final cross-pulse bullet. The diff showed the prior entry's `- **Next Action**` line as a deletion in its original position. Read-back confirmed it had been orphaned to EOF, AFTER the new entry — the prior entry was left incomplete. Fixed with two follow-up patches (restore line under its entry via the anchor region; remove the orphaned duplicate at EOF). Content was never lost, but ordering required repair.

## Landing WIP Found in the Working Tree (pulse pattern)

When a pulse scan finds uncommitted work in the repo working tree (fresh mtime, consistent with an agent's in-flight fix):

1. **Read the diff + the relevant helper definitions** — confirm the change follows the established pattern in that codebase (e.g. `_native_tool_arg` vs `_escape_shell_arg` semantics), don't just eyeball the diff lines.
2. **Run targeted tests** for the changed region, then the **full file suite**.
3. **Compare failures against the documented pre-existing baseline** (e.g. "8 known failures: atomic-write perms / symlink / find-fallback") — same failure set = zero new regressions.
4. **Commit if green** with a message that documents the root cause and test evidence. Flag at-risk if not ready.

## Verification Checklist

- [ ] Read back last ~20 lines of the log after appending
- [ ] Every entry has its own complete section (no orphaned lines)
- [ ] No duplicate lines at EOF
- [ ] Digest script invoked with Windows-style path (`E:/...`), not MSYS (`/e/...`)
- [ ] WIP commits verified against test baseline before landing
