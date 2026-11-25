---
name: config-reconcile
description: Reconcile one project's Claude instructions (CLAUDE.md, CLAUDE.local.md, AGENTS.md, .claude/rules/, and its auto-memory) against the global ~/.claude/CLAUDE.md and its @imports. Classifies each project rule as duplicate, narrower, override, conflict or project-only; reports first, edits only after approval, and records every dropped rule verbatim in a reviewable drop log. Use when the user asks to reconcile, dedupe or align a project's CLAUDE.md or memory with their global defaults.
argument-hint: [project-path]
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Skill: config-reconcile

Reconcile one project at a time. The project is `$ARGUMENTS`, or the current directory if empty.
`<date>` is today as `YYYY-MM-DD`. `<out>` is `${RECONCILE_DIR:-~/.claude/reconcile}/<date>/`.

## Steps

1. **Collect.** Run `bash ${CLAUDE_PLUGIN_ROOT}/skills/config-reconcile/scripts/collect.sh <project>`.
   Read every file it lists: the reference set, the project instruction files, and every memory
   file. Note the `ownership` line. Only `owned` repos get instruction-file edits. `upstream`,
   `fork` and `shared` (others have committed to the instruction files) are memory-only: their
   instruction files are a community config, and edits to them ride along in contributions and
   reach other contributors. Read those files as context, but do not propose edits to them, even
   where they duplicate a global rule. Edit one only if the user names that file and says to.
   For `local` or `not-git`, ask the user whether the instruction files are theirs to edit.
   A `PARENT-DIR memory` line is a memory about this repo saved from a session in a parent
   directory; sessions in the repo never load it. Read it and propose moving it here.
2. **Classify.** Split each source into rules (a memory file is one rule; a CLAUDE.md bullet or
   paragraph is one rule). Compare each against the reference set and assign one class:

   | Class | Meaning | Action |
   |---|---|---|
   | Duplicate | A global rule already says this | Delete. Memory: delete the file and its `MEMORY.md` line |
   | Narrower | Global covers the general case; the project adds a specific | Keep as written; trim the overlap only if the user asks |
   | Override | Project deliberately does it differently | Keep; add "Overrides global <file> § <section> because …" |
   | Conflict | Contradicts a global rule with no stated reason | Ask the user: override or delete |
   | Project-only | Global says nothing about it | Keep |

   The goal is to settle conflicts, not to tidy. Delete only what the global rule fully covers;
   if a rule adds any project-specific content, keep it unchanged. Judge by meaning, not wording. Facts about the project (commands, layout, data paths) are
   project-only even when they mention git or tools. When unsure between Duplicate and Narrower,
   choose Narrower. Also list housekeeping you saw: dangling or
   unindexed memory links, memories that look stale, and a `MEMORY.md` used as a status document
   rather than an index (propose moving the content into topic files). Report these items; do
   not fix them silently.
3. **Report in plain language.** Open with one sentence on where Claude's instructions come from
   (global files, project files, memories). Then list only the items that need a decision:
   conflicts first, then full duplicates, then housekeeping. For each item, say in a sentence or
   two what the project text says, what the global text says, and what Claude would do
   differently after the change. End each with a direct question. Do not use class names, IDs
   or unexplained file paths as the main content; mention the source file once, in passing. Do
   not list items you would keep unchanged. Then stop and wait. Do not edit anything before the user approves;
   the user may reclassify rows.
4. **Back up memory.** Before any memory edit, copy the whole memory dir to
   `~/.claude/backups/config-reconcile-<date>/<slug>/` with `cp -a <memory-dir> <backup>`. If
   that backup already exists (a second pass the same day), use `<slug>-pass2`, `-pass3` …:
   never copy over an existing backup. Memory is not in git; the backup is the only undo.
5. **Apply.** For instruction files in an owned repo: if the tree is dirty, stop and ask. Otherwise
   create branch `config-reconcile` from the default branch (`config-reconcile-<date>` if that
   name is taken; ask if `collect.sh` reports the default branch as unknown), make the edits, and commit once in the
   repo's `git log` style. Edit memory files in place and keep `MEMORY.md` in step.
6. **Write the drop log.** Owned repo: `<repo>/.claude/reconcile-<date>.md`, committed in the same
   commit. Upstream or memory-only: `<out>/<slug>-dropped.md`. Format:

   ```markdown
   # config-reconcile drop log — <project> — <date>
   Reference set: <global files>. Memory backup: <backup path>.

   ## <n>. <short rule name> — <Duplicate|Narrower, trimmed>
   Source: <file:line | memory/<file>.md>
   Covered by: <global file> § <section> — "<quoted global text>"
   Removed (verbatim):
   ~~~
   <exact removed text, as whole original lines even when only part of a line changed;
    for a memory, the whole file including frontmatter>
   ~~~
   Kept (trimmed Narrower only): <what remains>
   ```

   The checker counts removed text only inside a fence. Use a longer fence (`~~~~`) when the
   text itself contains one. Strip trailing whitespace from quoted lines; pre-commit hooks
   reject it, and the checker ignores edge whitespace. After the entries, add `## Overrides` and `## Conflicts resolved`, one line each.
7. **Check the log.** Run `bash ${CLAUDE_PLUGIN_ROOT}/skills/config-reconcile/scripts/check-droplog.sh
   <log> [--repo <repo> <default-branch>] [--memory <backup>/ <live-memory-dir>]`. Fix the log
   until it prints `drop log complete`.
8. **Write the summary** to `<out>/<slug>.json`:
   `{"project": path, "ownership": str, "counts": {"duplicate": n, "narrower": n, "override": n,
   "conflict": n, "project_only": n}, "overrides": [{"rule", "global", "reason"}],
   "narrower": [{"rule", "global", "kept"}], "conflicts": [{"rule", "global", "resolution"}]}`.
   Validate with `python3 -I -m json.tool`.
9. **Hand over.** Tell the user the branch, the drop log path, the backup path and
   `git diff <default-branch>...<branch>`. Stop. Merge (`--no-ff`) only when the user says so.

## Constraints

- Report before edit, always. One project per run.
- Never edit instruction files in an upstream, fork or shared repo unless the user names the file
  and says to. Never edit anything under `~/.*` outside `~/.claude/`.
- Never push, and never merge without the user's word.
- Never delete a memory without the backup in place and an entry in the drop log.
- Do not reword project-only rules. This pass removes overlap; it does not restyle.
- The reference set is the authority. If a project rule looks better than the global one, still
  classify it, and note it as a candidate for the global pass.
