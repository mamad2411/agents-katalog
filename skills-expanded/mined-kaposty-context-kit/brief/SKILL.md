---
name: brief
description: >
  Briefing on what happened while you were away, so a person can stay in the loop over
  autonomous work. Answers "what happened", which no built in display does: /status shows
  active settings sources, /permissions the resolved rules, /context what is loaded. Reads
  the transcript, git and the hook log for facts, the session ledger and project state file
  for the reasons, then writes six short blocks: progress, in progress, blocked, learned,
  open problems, next steps. Writes no file, and its one action is the closing step: what is
  blocked on the user is put to the user.
  TRIGGERS: "/brief", "brief me", "what happened", "where do we stand", "catch me up",
  "was ist passiert", "wo stehen wir", and the same intent in any other language.
  Project agnostic: no assumptions about language, stack, or repository layout.
---

# Brief: what happened while you were away

An agent can work for hours without you. When you come back, the question is not what is
configured, it is what happened, what is stuck, and what needs you. This skill answers that
in one screen.

It is the mirror image of the checkpoint. The checkpoint writes durable context **for the
model**, so reasoning survives a compaction. This writes a briefing **for the person**, once,
on screen, and it dies when you have read it. That is why it stores nothing.

## Rules that are not negotiable

- **It writes no file.** No report, no cache, no marker. A briefing is re-derivable, and a
  stored one only goes stale. The window comes from the transcript, which already records
  every earlier run of this command.
- **It changes nothing else either.** No commits, no flushing the ledger, no fixing what it
  finds. It names the next steps and stops. Self starting maintenance was measured as noise
  in this kit before, and it is not coming back through a status command. The one exception
  is the closing step: what is blocked on the user is put to the user. It touches no file.
- **It reports in the user's language**, matching the language they write in, and in that
  language's own characters. Never transliterate an accent or a diacritic away: a project may
  ban them in file and code names for portability, and that rule stops at the filename.

## The process

### 1. Get the facts

Run the digest, from the project root, exactly like this:

```bash
for d in .claude/tools tools "$(ls -dt "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/plugins/cache/*/context-kit/*/tools 2>/dev/null | head -1)"; do [ -f "$d/brief-digest.sh" ] && { bash "$d/brief-digest.sh"; break; }; done
```

The line resolves the install itself, which is the point of writing it out. Naming one path
and the other as an aside makes the model guess, and a guess is a failed call, a second call
to look for the file, and a third to finally run it. Measured: exactly that, three tool calls
and a wrong-path error, on a standalone install. It tests for the FILE and not for the
directory, because a project that keeps its own `tools/` or half a copy under
`.claude/tools/` otherwise wins the lookup and the call dies with exit 127: measured twice in
a real project, days apart. `CLAUDE_CONFIG_DIR` and not `CLAUDE_PLUGIN_ROOT`, because the
latter is substituted for hook commands only and is empty in a call you make. And the cache
branch takes `ls -dt ... | head -1` rather than the bare glob it used to: the cache keeps
EVERY version ever installed, a shell glob sorts them lexically, and the loop breaks on the
first hit, so `1.0.0` beat `1.5.1` and a plugin user who had ever updated kept running the
digest they first installed [measured 2026-08-19, eight versions in one cache]. Newest by
write time is the one that was just installed. An argument goes after the script name and
overrides the window: `24h`, `90m`, `3d`, or a date. It prints facts only, capped at a character budget, and
it names what it had to cut. Pass that on rather than hiding it.

If the header says `INCOMPLETE`, `python3` is missing and the transcript half is unreachable.
Say so in the briefing, in one line, and mark the affected blocks as guesses. A degradation
that reads like a normal result is worse than no result.

### 2. Get the reasons

The digest knows what happened, not why. Read the session ledger and, if the project keeps
one, the project state file named in the ledger's `PLAN` section. They carry the decisions,
the dropped paths and the open questions. Do not repeat their content wholesale: use them to
explain what the facts show.

### 3. Judge, and mark where the judgement comes from

Every line gets a provenance tag:

- `[measured]` for anything with a command, a file, a count or a log line behind it.
- `[read]` for anything inferred from the conversation.

This is not decoration. A briefing that mixes a failing test with an impression, and presents
both in the same voice, costs more time than it saves.

**A briefing where every line says `[measured]` has stopped distinguishing.** Two shapes give
it away, and both were observed in a real report that carried the tag on all fourteen lines:
a counterfactual ("a reboot would have killed it") and a self-assessment ("without the
counter-check I would have recommended it"). Neither was measured, both were reasonable, both
belong under `[read]`. Measured means someone could re-run it and get the same answer.

Judge the facts, do not relay them. The digest lists every recorded failure, and most of them
are not problems: a command that failed and was fixed in the next call is how work looks from
the inside. A failure belongs under open problems only if it is still true, or if nobody
looked at it. Same for uncommitted files, which are normal in the middle of a task and only
notable when the task appears finished.

### 4. Write it

Six blocks, this order, no other:

| | Block | Holds |
|---|---|---|
| 🟢 | Progress | finished and backed by evidence |
| 🟡 | In progress | still running, or started and left half done |
| 🔴 | Blocked | waiting on the user or on something outside |
| 💡 | Learned | knowledge that outlives the task |
| ⚠️ | Open problems | failures, findings, unsaved reasoning |
| ➡️ | Next | the recommended steps, cheapest useful order first |

**Use these words, not synonyms.** "Done" for Progress and "Waiting on you" for Blocked are
not wrong, they are just different, and a heading that changes between two runs cannot be
scanned by habit. The emoji and the word are one label, and both stay fixed. Translate them
into the user's language, keep them stable there.

**A block with nothing in it does not appear.** Empty headings are what makes a report
unreadable, and the presence of a block is itself the signal: a calm day is two blocks long,
a bad one is six. `➡️ Next` always appears.

`🔴 Blocked` includes everything that will not move without a person: decisions waiting on
the user, gated work, anything held up outside the project. **Every line in it says what it
waits on**, and the two cases do not look alike from where the reader sits: a decision only
they can make is theirs to act on this minute, an expired VM window or a queued pipeline is
not. A red block that does not separate the two makes the reader re-derive it every morning.

`➡️ Next` is the guide to the next stretch of work: it names what to do, ordered by
efficiency rather than by importance. If one step makes another cheaper or unnecessary, it
goes first, and the line says why in three words. **Each step also carries a rough effort**,
in the coarsest unit that is honest: minutes, an hour, a day. At eight in the morning the
difference between five minutes and half a day is the actual decision, and a list without it
forces the reader to open each item to find out. This is a recommendation, not an action.

**One step is one piece of work, not one command.** A chain that only runs in one order is a
single step, named by its end state and carrying the handle the reader picks it up by: where
the work stands now, and which file holds the parts. `Take plan-v1 from M2.3 to the end, half
a day, the live probe in PROBE.md is the open end` is one step and still a guide. The same
thing spread over five lines is the plan file copied into the briefing, and the plan file is
where those five lines already live.

**A step that names only a plan is an identifier standing in for the change**, the defect the
next section bans for tickets and commits. `Finish the plan` tells the reader that a file
exists. A step is written so the work can be started from the line itself, with at most one
file to open, or it is not a step.

**Nothing is dropped for space: whatever does not fit is counted and located**, in one line
under the list, for example `4 more in .claude/plan-v1.md`. That is what the questions in
step 5 already do with the ones that did not fit, and for the same reason: an invisible cut
reads as a short list, and the reader plans a day around a list that is missing its second
half. There is no fixed number of steps. What bounds the block is the 25 lines and the shape
of the work behind it: past about five steps the work has more than five open fronts, and
that is the finding, not the list.

### Form

- Start with one line naming the window and its real span, for example
  `since your last brief (3d 4h)`, and say if it fell back to a default.
- **Anything that limits how far the report can be trusted belongs in that first line**, not
  in a footnote: a `CUT FOR SPACE`, an `INCOMPLETE`, a window widened by the digest or set by
  hand. Observed at the bottom in italics, under the last step, where it reaches nobody. It
  is not an apology at the end, it is a property of everything above it.
- **Every number carries what it is measured against**, or it only looks like evidence.
  `0 of 16 chunks over 507 tokens` cannot be read: is 507 the limit, or the largest one seen?
  `no chunk over the 512 limit, the largest is 507` can. Same for a percentage without its
  base and for a "from 89 to 100 percent" without what those percent count.
- Bullets, not paragraphs. Bold the thing that matters in the line.
- A table only where it genuinely beats a list.
- Plain language. No jargon the user did not use first.
- **Never let an identifier stand in for the change.** `#3021 merged` reports nothing: it
  tells the reader that a number moved, and to learn what happened they have to leave the
  briefing and open a browser. Write what the change does, and put the identifier in
  parentheses only if it is genuinely needed to find it again: `the tokenizer now ships in
  the image instead of being fetched (#3021)`. The same holds for tickets, decision records,
  commits and branch names. This is the most common way a briefing looks informative and
  informs nobody.
- Around 25 lines. If there is more, the extra belongs in the ledger, not here.

### 5. Put what is blocked on you to you

The report ends, and then the blockers that are **yours** go into one `AskUserQuestion`
call. This is last on purpose: the six blocks stand complete even if the dialog is
dismissed, and a question asked before the report is a question asked without its context.

- **Only where the user is the blocker.** A release, an access, a decision that is theirs.
  "Waits on the outside: the build VM window expired" is not a question, it is a fact, and
  it belongs in the report and nowhere else.
- **One call, at most four.** That is the tool's own limit. Take the four that hold up the
  most, and **name in the report which ones did not fit**, so the cut is visible instead of
  looking like there were only four.
- **The recommendation is the first option, and its description says why.** A recommended
  option without a reason is a pre-selection, not a recommendation.
- **Where `AskUserQuestion` does not exist** (a headless run, a sub agent, a scheduled run,
  another harness), the same questions are the last lines of the report, numbered, and not
  buried in a paragraph.
- If nothing is blocked on the user, there is no call. Silence here is the healthy case.

## What good looks like

```
## Brief, since your last brief (3d 4h). The digest cut WHAT WAS SAID for space.

### 🟢 Progress
- **Foreign install brought current**, hooks are silent again
  (0 visible characters, was 2200)  [measured]
- **The tokenizer ships in the image now instead of being fetched**, so a build without
  network gives the same result (#3021)  [measured]

### 🟡 In progress
- **3 background agents started, none reported back**  [measured]
- Working tree has 2 uncommitted paths  [measured]

### 🔴 Blocked
- **Waits on you: the commit address.** Nothing else moves until it is set  [read]
- **Waits on the outside: the build VM window expired** after 24h, a fresh one is needed
  before the next release  [measured]

### ⚠️ Open problems
- **Ledger unsaved through 200 entries of work**  [measured]
- The rollback would probably have worked, but nobody tried it  [read]

➡️ **Next**
1. Set the commit address, 2 minutes, unblocks everything else
2. Save the ledger, 30 seconds, makes step 3 clean
3. Run the measurement under a full window, half a day
4. Take the hardening plan to the end, half a day, it stands at the timezone case and the
   parts are in .claude/plan-haertung.md
2 more steps in .claude/plan-haertung.md, both behind step 4
```

## Why this is not the ledger

They answer the same question for different readers, and that is the whole reason both
exist. The ledger is written so a **model** can pick the reasoning back up after a
compaction, and it is the only carrier measured to do that. The briefing is written so a
**person** can pick the work back up after being away, and it never re-enters the model's
context. This skill reads the ledger; it never replaces it and never writes to it.
