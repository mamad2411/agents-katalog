---
name: sessions
description: Use when counting what the text of the craft skills costs in the local Claude Code sessions, which of their scripts failed, and how often a rule's text came before its moment.
disable-model-invocation: true
argument-hint: "[days]"
---

# Sessions

This skill counts the local Claude Code transcripts of all projects on this
computer. For each skill of craft, it gives what its text costs and which of
its scripts failed. For each rule of `scripts/rules.json`, it gives how often
the rule's text reached the context before its moment. The counts have one
correct result, so a script makes them, and no model reads a transcript.

1. **Count.** The argument is a number of days, 14 when there is none. Run
   `bash <dir>/scripts/count.sh <days>` with a timeout of 10 minutes, where
   `<dir>` is this skill's base directory: 14 days take about a minute.
   The script reads `~/.claude/projects/`. It takes a transcript that
   changed in those days and that a person's session wrote: a `claude -p`
   run is left out. A subagent's transcript is a context of its own.
2. **Show the tables.** The first has these meanings:

   | Column | What it counts |
   | --- | --- |
   | `contexts` | the transcripts that loaded the skill, by the `Skill` tool or by a command that the person typed |
   | `loads` | all its loads. Claude Code adds a second copy only when the text differs, as with other arguments |
   | `twice` | the contexts that loaded it more than once |
   | `chars` | the characters that its loads put in the context: the line with the base directory, the text of `SKILL.md` with no front matter, and the `ARGUMENTS:` line when the load has arguments. Not the copies that a compaction attaches again |
   | `compacted` | the contexts with a compaction after a load. Then Claude Code attaches the last load of each skill again, the newest first: the first 20,000 characters of each, and about 100,000 in all, shared by every skill that the context loaded, from a plugin or not. An older skill that does not fit drops out whole |
   | `read` | the characters of the skill's `.md` files that `Read` returned, and the output of each Bash call in which a `cat`, `sed`, `head`, `tail`, `grep` or `awk` command names one of them. A call has one output, so all of it but the line with the exit code counts, for one skill only, also when the call runs a script too |
   | `failed` | the Bash calls that ran one of its scripts, with `bash` or by its path, and ended with an exit code other than 0. A call has one exit code, so it counts only for the script that its last command runs, as in `bash x.sh` or `for n in 1 2; do bash x.sh $n; done`, not in `bash x.sh \| tail -5`. A call or a `Read` that ended with an error and no exit code, as one that the harness, a hook or the person stopped, counts neither here nor in `read` |

   The line under the table gives, for each context that loaded a
   `SKILL.md`, the sum of their characters: the median, the 90th percentile
   and the maximum. Then each script with failed calls.

   The last table has one row per rule of `scripts/rules.json`: a rule that
   names a tool call as its moment, and the text that must come before it.
   `contexts` counts the main sessions with a moment in those days, after
   the text that states the rule (`from` and `says` in `rules.json`:
   `rules.md` from a hook, or a `SKILL.md` that loaded); a context with an
   old version of that text has no moment. The first such moment decides:
   `kept` counts the contexts where the rule's `text` came before it. That
   is a load from the plugin cache, when the `text` is a `SKILL.md`, or a
   read of all or part of the file whose result came before the call of
   the moment: by `Read`, or by `cat`, `sed`, `head`, `tail`, `grep` or
   `awk` when it shows lines of the file: not `sed -i`, not a `grep` that
   counts or lists, not an `awk` that prints no line or field of it, and not
   with its output sent to a file by `>`. In a pipeline, the last command
   decides: none into a count (`wc`, a counting `grep`, a checksum,
   `head -0`, a `jq` length) or a file, and none in an
   `x=$(...)`, whose output a variable takes. A read or a load in the
   same call or the same message of the model as the moment comes after it,
   since the model writes every call of a message first. The file can be in
   the plugin cache or in a checkout, not in a folder `claude/skills`, where
   a skill of the same name is another one. `share` is `kept` of
   `contexts`, and `-` with no moment. The next three columns count the
   subagents the same way. A rule with `main` has no moment there: a
   read-only subagent does not load review-loop for a review or github for
   a `gh` call, and the type of a subagent does not show that it is
   read-only, as a review runs as `general-purpose`.
3. **Read it.** About 3 characters are one token of the model.
   `tests/rules_test.sh` caps each `skills/*/SKILL.md` at 20,000 characters
   (ADR 0006), with a debt list of the files over it. A failed call is a
   candidate, not a defect: `invariants.sh` exits 1 at a failing invariant
   and `take-in-check.sh` at a refusal. Each one is a defect only by *Make
   sure the plugin is wrong* in `skills/github/plugin-defect.md`. A share under
   100 % is a candidate too: the steps of ADR 0009 decide what its misses
   change. A new rule in `rules.json` comes with a case in
   `tests/fixtures/sessions/rules/` where its text comes first and one where
   it does not, a new moment with its samples in
   `tests/fixtures/sessions/moments.tsv`, and a new read form with its
   samples in `tests/fixtures/sessions/reads.tsv`.
4. **The output stays on this computer.** The transcripts are of private
   projects too. A finding goes to the public tracker only as its shape and
   its counts (*Public repositories* in `skills/github/SKILL.md`). Ask the
   person before you file it, unlike a defect that you find in the code of
   this checkout: the counts come from the private transcripts of other
   projects.

Claude Code deletes a transcript after `cleanupPeriodDays`, 30 days by
default, so a count of more days can find fewer transcripts than it asks
for. Codex keeps its sessions as compressed files: the script does not read
them.
