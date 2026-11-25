---
name: wrap
description: "Close out a session — record what was learned, update any connected stores, commit coherent work, and leave a relay doc for a fresh start."
disable-model-invocation: true
---

# Wrap

End-of-session close-out. Run at a milestone, when the work is worth recording and the session may not be returned to.

Two stores ship with Polaris, and both are local to this machine and this repo:

| Store | What lives there |
|---|---|
| Session memory — `~/.claude/projects/<path>/memory/` | Corrections, preferences, how to work with this user |
| Project context — `.claude/context/` | Decisions, conventions, patterns for *this* repo |

Anything beyond that — a cross-project knowledge base, an external task tracker — is an **extension**. See below. If none is installed, wrap is memory, context, a commit, and a relay doc.

Wrap ends by writing a [`relay`](../relay/SKILL.md) doc. Relay on its own hands in-flight work to a fresh session mid-task; wrap closes work out and leaves the same kind of doc behind, so the user can start fresh with the background instead of resuming a long transcript.

## One pass, no questions

**Wrap never stops to ask.** Every write happens, in one turn, and the report at the end is the review. A wrap that pauses for approval is a wrap that gets abandoned with nothing written; a wrap that writes and reports gives the user something to read and, if wrong, revert. Memory entries are files, context entries are lines, commits are `git revert`. All cheap to undo, none cheap to reconstruct.

Order by dependency, not by risk:

1. Memory and project context
2. Extension writes, cheap ones then curated ones
3. Commit
4. Relay doc (last, so its pointers can name what steps 1–3 produced)
5. Report

## Step 1 — memory and project context

Follow the [`reflect`](../reflect/SKILL.md) skill's process — scan, filter, classify, write. Read it rather than re-deriving the formats; it owns them.

One change: **write the surviving findings instead of proposing them.** Reflect proposes because it's used interactively. Wrap assumes nobody is watching. The filter carries the weight — anything failing reflect's four checks is discarded, not written and not mentioned.

## Step 2 — extensions

Run each installed extension's `## Close-out` section in full: its Phase 1 writes, then its Phase 2 writes. Both are written. The difference is only in the report: Phase 2 items are curated (status lines, priority ordering, tasks another person reads), so each one is listed individually with what changed, where the Phase 1 writes can be summarised.

## Step 3 — commit

Look at the working tree.

If it holds **one coherent change**, commit it with a message following [`commit-conventions`](../commit-conventions/SKILL.md). No approval step.

If it holds **several unrelated changes, or work that is plainly half-finished**, commit nothing and say so in the report. Close-out is exactly when unfinished work gets shipped by accident, and this guard is the only thing standing between wrap and that mistake. When in doubt, don't commit — an uncommitted tree is a line in the report; a bad commit on a shared branch is somebody else's morning.

**Never push.** Report what is unpushed instead.

## Step 4 — relay doc

Write a relay doc exactly as the [`relay`](../relay/SKILL.md) skill's Mode 1 describes — same path (`~/.claude/relays/<slug>-<timestamp>.md`), same template, same one rule: **narrative and pointers, never status.** Read that skill for the format; do not re-derive it.

One difference from running `/relay` by hand: **do not ask the steering question.** Weight the doc toward what the session itself understood as next — the last thing the user asked for, the item left queued, the ruling that opened the next piece of work. If genuinely nothing is next, the doc says so in one line and the Next section is short.

Everything the session did that a fresh session cannot recompute goes here: why this approach, what was tried and abandoned, what the user decided, what is deliberately out of scope. Everything it can recompute — branch state, test results, task status — stays out. Pointers only: branch names, file paths, task IDs, the commit hash from step 3.

Sanitize as relay does: no secrets by value, ever.

## Extensions

Some setups have stores that Polaris knows nothing about: a personal knowledge vault, a shared team wiki, an issue tracker, a status page.

**Wrap does not define those. It runs them.**

An extension is any available skill that owns such a store and documents a `## Close-out` section. Its description will say what it owns — a second brain, a vault, cross-project knowledge, a task tracker. At wrap time, check the available skills for one, read it, and follow its `## Close-out` section: both phases written, Phase 2 items reported individually.

If nothing is installed, skip this step silently. Absence is the normal case, not an error.

### Writing a Close-out section

Two requirements, and discovery fails without the first: **the skill's `description` must name what it owns** (a second brain, a vault, a task tracker) — that description is the only thing wrap sees when scanning for extensions, so a Close-out section in a skill whose description doesn't flag it will never be found. Second, the section itself:

```markdown
## Close-out

Invoked by `/wrap`. Resolve the target first — never guess which record to write.

**Phase 1 (write, summarise in the report):** <the cheap, correctable writes —
capture files, completing work that demonstrably finished>

**Phase 2 (write, list each in the report):** <the curated writes — status
lines, priority ordering, anything another person reads. Written outright;
the report is where the user reviews them>
```

Two rules for any extension:

- **Resolve the target before writing.** If the current repo can't be matched to a record with confidence, capture to whatever the store's inbox equivalent is and say so. A confident write into the wrong record is worse than no write.
- **Never record what's derivable.** Branch state, deploy status, test results — all recomputable in seconds, all stale by the next read, and all still reading as authoritative. Record what happened and why.

## Report

A few lines, in this order:

1. **What landed.** Memory and context in one line. Each curated extension write on its own line, with the file or record and what changed, so any of them can be reverted from the report alone. The commit hash, or the reason nothing was committed.
2. **What's still dirty.** Uncommitted, untracked, unpushed. The most useful line in the summary.
3. **Skipped stores**, with why. Silence implies covered.
4. **The relay closing block**, last and verbatim, exactly as relay's "Closing block" section describes: the doc's absolute path, the directory to open, and the paste-ready fenced block that starts with the `cd`.

## Common mistakes

- **Asking.** Wrap has no questions. If something needs a ruling, write the conservative option and flag it in the report.
- **Committing to be tidy.** Half-finished work shipped at close-out is the failure this is most likely to cause. The coherence guard in step 3 is not optional.
- **A relay doc that carries status.** If the doc says "done", "passing", or "3 commits ahead", it is already wrong. Narrative and pointers only.
- **Re-deriving reflect's or relay's formats, or an extension's.** Read the skill that owns them.
- **Treating a missing extension as a problem.** Most setups have none.
- **Reporting only successes.** What's still dirty and what was deliberately not committed are the lines the user actually needs.
