---
name: session-ledger
description: |
  Keep a session's durable reasoning alive across context compaction. Maintains a
  small on-disk ledger of what was decided, what is still open, what was verified
  and by which command, and what was dropped and why. A compaction summary
  flattens reasoning; this preserves it. Invoke explicitly to start, inspect,
  repair, or hand over a ledger. The per-session maintenance discipline is primed
  automatically by the session-start hook, so routine appends need no invocation.
  Project-agnostic: no assumptions about language, stack, or repository layout.
---

# Session Ledger: reasoning that survives compaction

When a session grows long, the harness summarises the earlier turns. Root
instruction files and the memory index are re-read from disk and survive intact.
**Your reasoning does not.** The summary keeps roughly what happened; it loses why.
The decision you locked after twenty minutes of argument, the fact you verified
with a specific command, the approach you abandoned for a good reason: all of that
becomes prose, or vanishes.

The cost is not the lost text. It is that a later turn re-opens a settled question,
re-verifies a proven fact, or retries an abandoned path, and nobody notices,
because the record of the decision went with the summary.

The Session Ledger is a small file that holds exactly the state a summary destroys,
and nothing that a summary preserves or that one command can recompute.

## The one rule that shapes everything

**Preserve only what is not cheaply re-derivable.**

Your git branch, the open pull requests, the todo list, the build status: these are
one command away, always current, and never worth carrying. They are re-derived
after compaction, not preserved.

Decisions, rationale, verification provenance, and dead ends cannot be recomputed
from anything. Once the summary flattens them, they are gone. Those are the ledger's
only business.

A ledger that fills up with status snapshots has become the thing it was built to
replace.

## The contract with the harness

Three facts govern the design. They are load-bearing, so verify them against your
harness version before trusting this skill.

1. **A pre-compaction hook cannot steer the summary.** It can block compaction or
   run a side-effect. It cannot tell the summariser what to keep. There is no
   "please preserve this" for the summary.
2. **The only working mechanism is write-to-disk, then read back after.** A
   session-start hook with a `compact` source can re-inject once the summary exists,
   but only best-effort (it fires late on a manual `/compact`), so the reliable carrier
   is the file on disk plus a re-read instruction in your CLAUDE.md. A PostCompact hook
   was tried for this and removed: it failed live ("Hook cancelled") and is undocumented.
3. **Hook output is capped** (10,000 characters in current Claude Code). Past the
   cap, output is replaced by a file pointer. A fat re-inject silently becomes no
   re-inject. This is not a style preference; it is the reason the ledger is thin.

The consequence that surprises people: a shell hook cannot write the semantic part
of the ledger, because a shell script does not know what you decided. **The model
maintains the ledger during the session.** The hooks only prime it and read it back.

## The ledger

One file, one working directory, at a stable path the hooks and the model agree on:

```
.claude/session-ledger.md
```

One ledger per working directory. Parallel sessions belong in separate worktrees;
two sessions sharing a directory will interleave their reasoning into one file and
corrupt both. If your harness enforces worktree isolation, this is already handled.

### Sections

The order is deliberate and **restore-first**: orientation at the top (what are we doing,
where do I continue, what is unresolved), reference material below (what was settled,
proven, abandoned). After a compaction nobody reads a ledger top to bottom, they read the
first two sections and act.

```markdown
# Session Ledger
_started: <ISO timestamp>_

## TASK
One line: what this session is actually trying to achieve.

## NEXT
One line: the single most valuable next action, ready to pick up cold.

## OPEN
- <question still unresolved, and what would settle it>

## DECIDED
- <decision>: <the reason it beat the alternative>

## VERIFIED
- <fact> [<the exact command or probe that proved it>]

## DROPPED
- <approach abandoned>: <why, so it is never retried>

## PLAN
Pointers, never copies: the active plan file, and the project state file if the project
keeps one. A path each.
```

`NEXT` is the section that earns its place fastest. Everything else tells you what
happened; `NEXT` tells you what to do, which is the one thing a freshly compacted window
cannot re-derive on its own. It is a judgement, not a lookup, so it has to be written
down. Keep it to one line and rewrite it with every append that touches the file, never as
an append of its own (see *When to append*): a stale `NEXT` is worse than none, because it
is followed.

`VERIFIED` carries the command, not just the claim. A fact without its provenance
degrades into a belief the moment the summary paraphrases it, and a belief gets
re-verified or, worse, trusted when it should not be.

`DROPPED` is the section people skip and regret. An abandoned approach without its
reason will be proposed again, confidently, by a future turn that has no memory of
why it failed.

`PLAN` holds paths, and this is the section that decides whether a durable file is read at
all. A file on disk survives compaction by itself, but the model only opens what it has been
pointed at, so an unpointed file is write-only no matter how carefully it is maintained.
That is why the **project state file belongs here too**, next to the plan. Never paste
either into the ledger: duplicating a file that already survives burns the cap the ledger
needs.

## When to append

Event-driven, never per-turn. Appending on every turn produces a log, and a log is
the wrong shape: it grows without bound and buries the signal it was meant to keep.

Append when, and only when, one of these happens:

- **A decision gets locked.** The user chose an option, or an argument settled.
  Record the decision and what it beat.
- **A fact gets verified.** A command returned an answer that the work now leans on.
  Record the fact and the command.
- **A branch opens.** A real question surfaced that is not yet resolved.
- **A path gets dropped.** An approach was abandoned. Record why.
- **The task changes.** Rewrite `TASK`. Rare, and worth a write of its own: a ledger
  pointing at the wrong task misdirects everything restored under it.

`NEXT` is deliberately not on that list. It changes more often than everything else
combined, and it is the cheapest content in the file: one sentence, overwritten, never
appended to. Written on its own it buys a visible file write for a line that the next
append would have carried anyway, and a discipline meant to be invisible should not be the
thing the user watches most often. So `NEXT` **rides along**: refresh it inside the next
append from the list above, and at every checkpoint, never by itself.

What that costs is bounded by the last event rather than by the clock. `NEXT` is at worst
as old as the most recent decision, verified fact, opened question, dropped path or task
change, and a stretch with none of those produced nothing new to point at. That bound is
what makes the deferral safe under automatic compaction too, where no checkpoint runs
first to catch it.

**Carried out means gone from here.** Once an item has been moved into the project state
file, it leaves the ledger. Keeping both copies was measured at 54 percent overlap in a real
pair of files, with three `OPEN` items word for word identical, and a duplicate does more
than waste the cap: two copies drift, and then nobody can tell which one is current. The
ledger holds what **this task** still has open; what outlives the task lives in the project
state and is reached through `PLAN`.

An `OPEN` item that only the user can close is put to them in the same turn it is written,
through `AskUserQuestion` where that tool exists. Writing a question down is not asking it,
and an item nobody was ever asked stays open for a reason that has nothing to do with the
work.

Resolving an item means editing it in place: an answered `OPEN` becomes a `DECIDED`
or a `VERIFIED`, and leaves `OPEN`. The ledger reflects the current state of the
reasoning, not its history. It is a working set, not a changelog.

### When the write is refused

Plan mode refuses `Write` and `Edit`, and this file is not an exception. The refusal names
no cause: `Permission to use Write has been denied`, nothing more, so it reads like a rule
about the path when it is a gate on the mode. Measured on 2026-08-24 in two unrelated
projects: one session read it as a path problem and tried the plan file, a project
directory and twice a shell heredoc, then asked a sleeping user which route to take. Three
of the refusals that night landed on the ledger itself (2026-08-22 02:02, 2026-08-22 18:37,
2026-08-24 00:09), and the gate can outlast the approval: after one approved plan, four
writes in the same turn were refused across 58 minutes, and the identical write went
through unchanged in the turn after the next user message.

**The shell is not the second route either, whatever the harness says.** In
`bypassPermissions` mode Claude Code carries a system reminder asking for file changes
through `sed`, heredocs or short scripts. That is right for normal work and wrong here:
on a refusal it does not lift a lock, it walks around a permission decision. Measured
2026-08-30: a session met the refusal, wrote that the harness itself points at Bash, and
took the heredoc. A rule that contradicts a system reminder without naming it loses to it,
which is why this one names it.

So: **retry the same write once, and never take a second route to disk.** A retry is often
all it takes, and not only in plan mode: measured on 2026-08-24 at 16:33:52 and 16:44:27,
outside any plan pass, a refused write went through on the next attempt 21 and 38 seconds
later, unchanged. If it stays refused, hold the events in your reply and end the turn
instead of hunting; the next turn writes them in one go.

What counts as that next turn is narrower than it looks, and guessing wrong wastes another
quarter of an hour. A tool result does not count: an `AskUserQuestion` answer arrives inside
the running turn and the next write is refused exactly as before, measured three times. A
message from another session does not count either: it arrives as a queued command, measured
2026-08-30, delivered at 11:45:57 and the identical write refused again at 11:47:59. What did
work, four times, is a message a person typed into the session while it was idle. Whether a
blocked stop counts is the open question `hooks/write-gate-probe.sh` exists to answer; until
its log says so, do not assume it does.

Hunting is what makes this expensive. Measured the same day: a plan approved at 18:22:47,
then a project path, a shell redirect and a scratchpad path tried in sequence, all refused,
and the session stopped 29 minutes later to ask a question it could have avoided. This
matters more than it sounds: a planning pass is the phase that produces the most `DECIDED`
and `DROPPED` material of any, which is exactly the content the ledger exists for.

**After an approval, the first act is not a write, it is the end of the turn.** The plan file
already exists, the harness wrote it, and the gate outlasts the approval for the rest of that
turn. Measured five times across two projects and three harness versions, most recently
2026-08-30: plan approved at 10:01:18, writes refused at 10:02:25 and 10:03:57, the user
asked whether the refusal was intended, answered, and the identical write refused again at
10:05:20. Ending the turn there costs one message that the user, who has just approved, was
going to send anyway; staying in the turn has cost between 12 and 29 minutes every time.

The plan itself needs no write from you. `ExitPlanMode` carries it, the harness saves it to
`~/.claude/plans/<slug>.md` on approval and names that path in the approval message, and a
copy inside the project is an act of implementation that belongs after the approval.

## Size discipline

Target well under the hook cap, since the whole ledger is re-injected as one block.
If it grows past roughly 150 lines, it is carrying things it should not:

- status that should be re-derived,
- narrative that should be a single line,
- resolved items that should have been edited in place rather than appended.

If it is genuinely large and every line earns its place, the re-inject hook degrades
by PRIORITY, not by position: every canonical section keeps a floor, DROPPED and
VERIFIED outrank DECIDED, non-canonical sections are cut first, and anything clipped is
named in the block. A plain head-and-pointer cut was measured and rejected, because it
drops whatever sits late in the file, which is exactly the delta sections. If a restore is
not complete, the canary is withheld and the block says so, so detail stays retrievable
on disk instead of being truncated into nothing.

## What the ledger must never contain

- **Secrets.** It is a plain file, it is re-injected into context, and it will be
  read by every future turn. Record that a credential was configured, never its value.
- **Copies of files that already survive.** Root instruction files and the memory
  index are re-read from disk by the harness. Re-injecting them is pure duplication
  and eats the cap that the ledger needs.
- **Re-derivable status.** See the one rule.

## Lifecycle

- **Session start.** The prime hook injects the maintenance protocol once and restores the
  ledger. **Age is never a reason to retire it.** Chats are timeless: a conversation picked
  up a week later has exactly the context it had, so a ledger that has not been touched in
  a month is restored like any other. Two age-based rules were tried and both destroyed
  continuity, the second one invisibly: rotating anything older than twelve hours meant that
  opening a new session in a directory archived the ledger of an old session that was still
  alive, and resuming that conversation later found its carrier gone.
- **Same directory, different task.** What matters is ownership, not age, and it is
  detectable: the ledger carries the id of the session that wrote it. At session start no
  prompt exists yet, so the hook cannot decide what the new task is; it restores the ledger
  **and** says it belongs to another session, with the archive command ready. Decide on the
  first turn: same task, continue; different task, archive it first. Never append new
  reasoning to another task's ledger, a mixed ledger restores the wrong decisions after a
  compaction.
- **During the session.** The model appends on the events above.
- **After compaction or resume.** The re-inject hook emits the ledger, best-effort. The
  model re-derives mechanical state itself if it needs it.
- **Before archiving, carry the durable half over.** Archiving ends the ledger's reach, so
  whatever outlives the task has to leave first: the decision and what it beat, the dropped
  path and why, where the work stands. That goes to the project state file
  (`.claude/project-state.md`, or the path the manifest names), which is the carrier for
  everything wider than one task; anything useful in a *different* project goes to memory
  instead. The checkpoint does this as a matter of course, so a ledger that was checkpointed
  is already safe to archive.
- **Session end.** The ledger stays on disk. Nothing removes it on a timer; it is replaced
  when a new task deliberately archives it. Archived ledgers are a useful record of how a
  decision was reached, and they cost kilobytes.

## Using this skill explicitly

Invoke it to:

- **start** a ledger when the hooks are not installed, or mid-session,
- **inspect** the current ledger and judge whether it is carrying the right things,
- **repair** a ledger that has drifted into a status log,
- **hand over**: read the ledger and reconstruct where the work stands.

For routine appends you do not need to invoke anything. The protocol is primed at
session start; appending is a two-line edit.

## Honest limits

The ledger preserves what the model chose to write down. If a decision was never
recorded, no hook recovers it: this is a discipline with mechanical support, not a
mechanism that works unattended. It also cannot make the summary better, because
nothing can. It routes around the summary instead.

Finally, the harness contract above is version-dependent. Before relying on this in
a new environment, run one real compaction and confirm the ledger actually comes
back. A design that is right in principle and unwired in practice preserves nothing.
