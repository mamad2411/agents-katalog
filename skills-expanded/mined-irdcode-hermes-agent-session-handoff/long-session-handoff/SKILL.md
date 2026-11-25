---
name: long-session-handoff
description: Chat handoff — measure the session, read the parent in full, continue.
when_to_use: A working session is approaching the token limit that ends it (the compaction trigger, or the provider's hard limit), and the work is not finished. ALSO whenever you are standing IN a continuation chat, because Rule Zero says the parent transcript gets read in full first.
version: 2.0.0
languages: all
author: IRDkiya
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [session-management, context, handoff, continuity, productivity]
    homepage: https://github.com/IRDcode/hermes-agent-session-handoff
---

# Long-session handoff

Move an unfinished long session into a fresh chat that **reads the parent
transcript in full** before it does anything, instead of letting the context
limit decide what survives.

Three scripts do the work. Everything below is either an instruction to you or
the measurement that justifies it.

```
scripts/session_weight.py        measure -- is this session actually heavy?
scripts/dump_parent_session.py  export -- 01..05 files on disk
scripts/handoff.py              do the whole handoff in one command
```

`$SKILL_DIR` below means this skill's own directory. Resolve it once:

```bash
# Hermes home is $HERMES_HOME, or %LOCALAPPDATA%\hermes (Windows) / ~/.hermes
SKILL_DIR="$HERMES_HOME/skills/productivity/long-session-handoff"
```

## RULE ZERO — the continuation reads the parent IN FULL, always

Not conditional, not "if it seems relevant", not a summary. **Every handoff, the
continuation chat reads the parent session's own transcript before it does
anything else**, and it proves the read with counts.

Why a brief is never enough: a brief is written BY the agent that is handing off,
so it inherits that agent's blind spots — and those blind spots are what made the
session run long. The transcript has the user's own wording, every "no", every
instruction they had to repeat, and the asks that were quietly dropped. A brief
has the agent's version of those.

This exact failure happened twice in practice: the seeding prompt named only the
brief, so only the brief was read, and the user had to ask a second time. The
brief is step 2 of the read, never step 1, and never the whole of it.

One command does the export:

```bash
python "$SKILL_DIR/scripts/dump_parent_session.py" <parent_session_id> [out_dir]
```

It writes five files and prints the counts:

| file | what it is | read it? |
|---|---|---|
| `01-user-messages.md` | every user message, verbatim, deduped | **IN FULL. No skimming.** |
| `02-decisions.md` | assistant messages > 400 chars — decisions + measurements | in full |
| `03-full-transcript.txt` | everything, tool calls and results included | search it; read the stretches that matter |
| `04-index.json` | counts, tool census, time span, weight at export | check the numbers |
| `05-dropped-context.md` | turns compaction removed, recovered from disk | when the brief references something you cannot find |

Gate, and state it out loud in the child's first message: *"parent read: N live
rows, U unique user messages"*. If you cannot quote those numbers, you did not
read it, and the handoff is not done. An unquantified "I read it" is a
mislabelled success.

## What Hermes actually does at the limit (and why file 05 exists)

Hermes does **not** delete your history when it compacts. It rewrites the live
context in place and keeps the replaced turns in `state.db` with
`active = 0, compacted = 1` — still searchable, still recoverable.

Two consequences, and both matter:

1. **A past compaction is not a reason to hand off.** It is evidence that
   context was already reclaimed. The right response to "this session was
   compacted" is to recover the dropped rows (file 05), not to migrate a session
   that has room.
2. **Counting rows is not measuring context.** Measured on real sessions, total
   rows ran **2 to 4 times** the live set (worst case 4.0x: 3,389 rows on disk,
   832 live). Scoring rows is how a detector fires on a session at 32% of its
   limit.

`05-dropped-context.md` is the only thing that recovers those turns for reading.
Measured: 661 rows / 270 KB in one session, 1,219 archived rows / 1.5 MB in
another, including 7 user messages that no longer existed in the live context.

## Measuring the weight — never guess

```bash
python "$SKILL_DIR/scripts/session_weight.py"                    # newest session
python "$SKILL_DIR/scripts/session_weight.py" --session-id <id>
python "$SKILL_DIR/scripts/session_weight.py" --session-id <id> --json
python "$SKILL_DIR/scripts/session_weight.py" --list
```

The report names every input, so a wrong number is visible rather than silent:

```
WINDOW
  context window   1,000,000   (source context_length_cache.yaml)
  threshold        0.50 configured -> 0.50 effective
  compression      enabled

WALL -- the token count past which this session stops growing
  500,000 tokens, then Hermes COMPACTS IN PLACE

NOW
  live rows        251   (archived on disk: 1)
  context          227,037 / 500,000  [#####.....] 45%
  token source     provider (usage delta)
  active time      1.6h   (elapsed span 1.8h, idle included)

VERDICT  STAY HERE  (below gate (45% < 62%))
```

### The wall, and where the numbers come from

```
compaction fires at   window x threshold   (floored at 64,000 tokens)
provider refuses at   window - reserved output      (compression disabled)
```

Two floors in Hermes surprise people, so the script mirrors both: a window
**under 512,000 compacts at 75%**, not at the configured 50%; and a window at or
below 64,000 triggers at 85% instead. Verified live against Hermes' own log —
window 1,000,000, threshold 0.50, and Hermes logged
`~501,079 tokens >= 500,000 threshold`.

The window comes from `context_length_cache.yaml` (what Hermes discovered by
probing your endpoint) before any guess, because that value cannot be wrong
about a window Hermes measured, and it survives Hermes refactors.

### The gate: 62% of the wall, or no handoff

| signal | threshold |
|---|---|
| context vs the wall | ≥ 62% counts, ≥ 85% hand off, ≥ 95% act without asking twice |
| live rows (`active = 1`) | > 400 |
| tool calls | ≥ 250 |
| active working time | > 4 h |

**Nothing is offered below 62% of the wall, whatever else tripped.** Rows, tool
calls and hours are proxies for context pressure, invented for tools that could
not measure context directly. Here it can be measured, so they only sharpen
urgency once context itself says moving is due.

Measured justification: re-scoring 21 historical firings of the pre-gate
detector, 6 sat below 40% of the wall. The worst had 1,685 rows and 5.2 active
hours while its live context was 157,759 of a 500,000 wall — **32%**. Handing off
there abandons ~340,000 tokens of paid-for headroom and makes the continuation
spend ~25,000 re-learning what the parent already knew.

### Two measurement traps, both of which shipped as bugs

**Trap 1: elapsed time is not working time.** A chat left open overnight has a
16-hour span and 90 minutes of work in it. Measured: one session reported a
15.98h span of which a single gap was 14.43h of sleep — **1.55h** of actual work.
Sum only the gaps shorter than ~10 minutes.

```python
stamps = [float(r[0]) for r in cur.execute(
    "SELECT timestamp FROM messages WHERE session_id=? ORDER BY timestamp", (sid,))]
active = sum(b - a for a, b in zip(stamps, stamps[1:]) if 0 <= b - a < 600) / 3600
span   = (stamps[-1] - stamps[0]) / 3600     # report it, never score it
```

**Trap 2: markers you only READ are not markers that happened.**
`content LIKE '%CONTEXT COMPACTION%'` matches the agent's own tool output the
moment anyone greps for it. Measured in one database: **35 tool rows** contain
that string purely because a session read a file quoting it, and one session
scored 3 compactions having never been compacted. Count structurally instead —
archived rows with `compacted = 1` — or at minimum anchor the match at position 0
and exclude `role='tool'`.

**Trap 3: the token estimate is ~28% low on its own.** Tool schemas ride every
request and live in neither the database nor the message list. Measured live: the
provider reported 297,239 prompt tokens where chars/4 over the same live set gave
214,715 (0.72x). `session_weight.py` corrects for this by differencing
`sessions.input_tokens / api_call_count` between two turns — exact, from the
provider — and learning the per-session overhead. It needs **two turns** to
learn; the first turn is deliberately conservative.

## Asking permission

**Ask, never decide alone.** Handing off is like running a destructive command:
the user says yes first. One `clarify` call, three options, no prose walls. Say
what is measured, what carries over, and what the new chat will be called.

```python
clarify(questions=[{
  "question": ("This chat is at 87% of its context limit (312k of 360k tokens, "
               "5.1h of work). I suggest continuing in a fresh chat: the full "
               "transcript and every decision carry over, and the name will say "
               "it continues this one. What would you like?"),
  "choices": ["Move to a fresh chat (recommended)",
              "Keep working here",
              "Finish the current task first, then move"],
}])
```

If the answer is "stay", respect it. The watcher will not ask again until the
session has grown another ~200 rows or crossed another tenth of the wall, with a
15-minute floor either way.

## Doing the handoff — one command

```bash
python "$SKILL_DIR/scripts/handoff.py" <parent_session_id> \
    --brief ".hermes/handoff/<slug>-continuation-2.md" \
    --task "the next open item, stated concretely" \
    --workdir "/path/to/project"
```

It runs seven steps and prints what each one did:

1. **measure** — refuses to move a session below the gate unless `--force`
2. **export** — `dump_parent_session.py` into `<home>/handoffs/<parent>/`
3. **create + seed** — makes the continuation and has it read the export, then
   report the counts back, so the read is verified rather than claimed
4. **name** — parent's words verbatim plus a continuation marker
5. **pin** — model, provider, endpoint, reasoning config and iteration budget
   written onto the child row; `end_reason`/`ended_at` cleared; stale turn lease
   deleted
6. **record** — `handoffs/chains.json` plus `_handoff_from` in the child's
   `model_config`, and the parent is marked so the watcher stops offering a
   migration that already happened
7. **kickoff** — with `--task`, the continuation continues the work itself

Useful flags: `--dry-run` (prints every change, writes nothing), `--no-kickoff`
(seed and verify only), `--title` / `--marker` (naming), `--skills a,b`,
`--profile NAME`, `--seed-turns` / `--work-turns`, `--force`.

### Naming the continuation

The name must make the lineage obvious to the user. The parent's topic words are
kept **verbatim** — that is what they search by — and numbering starts at 2,
because the original chat is 1. The marker matches the title's own language:

```
Refactor auth              ->  Refactor auth (cont. 2)
۳کانس: هویت بصری ایرانی     ->  ۳کانس: هویت بصری ایرانی — ادامه ۲
تحليل البيانات              ->  تحليل البيانات (الجزء ٢)
重构登录流程                  ->  重构登录流程（续 2）
ログイン改修                  ->  ログイン改修（続き 2）
```

An existing marker is incremented, not stacked: «X — ادامه ۳» becomes
«X — ادامه ۴», in the digit family the author used.

### Why the title is written directly to the database

`hermes sessions rename` runs the title through a sanitiser that strips
U+200B–U+200F. That range includes the **ZERO WIDTH NON-JOINER**, which is a
letter-level character in Persian, Arabic and Urdu. Measured: renaming to
«تست‌های انتقال» stored «تستهای انتقال» — a spelling error in the user's own
project name. `handoff.py` writes `sessions.title` directly and reads it back.
If you do it by hand:

```python
import sqlite3, json
want = "۳کانس: نقش\u200cها و مأموریت\u200cها — ادامه ۲"
w = sqlite3.connect(db, timeout=20)          # writable, NOT mode=ro
w.execute("update sessions set title=?, title_source='user' where id=?", (want, sid))
w.commit()
assert w.execute("select title from sessions where id=?", (sid,)).fetchone()[0] == want
```

### Why the model is pinned by writing the row

`-m` on `hermes chat` does **not** persist. Measured: creating with
`-m "GO/claude-opus-5-thinking"` stored a different string in `sessions.model`,
and a later `--resume -m …` did not rewrite it either — the flag applies to that
process, then the row keeps whatever the config default resolved to. There is no
`hermes sessions set-model`, and `hermes model` is the interactive global picker,
which would change every future chat.

Copy the parent's exact strings (`select model, model_config from sessions where
id=<parent>`) rather than typing a name from memory: a wrong provider prefix
silently falls back.

Three more things that must be written in the same transaction:

- **`max_iterations`** — `--max-turns N` on the creating call freezes
  `max_iterations = N` on the child row. 25 is right for "read and report" and
  then permanently starves the real work; rewrite it to ~120.
- **`end_reason = NULL, ended_at = NULL`** — a `hermes chat` seeding run leaves
  `end_reason='cli_close'`, so the session reads as *ended* in the desktop list
  and the user opens a chat that looks dead.
- **`delete from session_turn_leases where conversation_id = <child>`** — a
  leftover lease makes the app believe a turn is still running.

### Why lineage is NOT written to `parent_session_id`

That column marks implementation-detail children (subagent runs, compression
continuations) and Hermes' listing query hides them. Measured: **51 of 52** rows
carrying `parent_session_id` were invisible to `hermes sessions list`. A handoff
must stay visible, so lineage lives in `model_config._handoff_from` and in
`handoffs/chains.json`.

## The handoff brief

Write it to a file **before** opening the new chat, so it survives if something
goes wrong. Keep it readable in a minute:

```
.hermes/handoff/<slug>-continuation-<n>.md
```

Contents, in this order:

1. **What we are building** — two sentences.
2. **Where it runs** — paths, the service/process, how to restart it.
3. **Decisions already made** — with the measurement that justified each. This
   is the part that prevents re-litigating settled questions.
4. **Root causes already found** — one line each, so no bug is re-diagnosed.
5. **State of the work right now** — done, verified, pushed.
6. **Open items** — what is still broken and what the user asked for last.
7. **Standing instructions from the user** — tone, language, what they refuse.

If the brief is longer than a page it will not be read, and the new chat starts
as confused as the old one ended. Decisions and root causes only — no play-by-play.

## Variant: the user already opened the new chat

Sometimes the user opens a fresh chat, pastes the old chat's title, and says
"continue here, read everything from the old one". That is a *pull* handoff: the
continuation already exists and you are standing in it. Skip creation and skip
the kickoff (nobody is asleep — the user is waiting). Do this instead:

1. **Find the parent by title**, not by guessing:
   `session_search(query="\"<the title they pasted>\"", limit=5)`.
2. **Export it** — `session_search` returns bookends plus a ±5 window, which is
   not the transcript:
   `python "$SKILL_DIR/scripts/dump_parent_session.py" <parent_id> ".hermes/handoff/parent-<parent_id>"`
3. **Read `01` completely and `02` completely**, then the brief if one exists.
   Do not assume `role='tool'` rows are redundant — measurements frequently
   appear ONLY there and never get restated in prose.
4. **Rescue the data, not just the prose.** A long analysis session leaves its
   real value in temp directories and in
   `<hermes home>/cache/delegation/subagent-summary-*.txt`. Temp gets cleaned and
   those summaries are the only copy of work that was paid for. Copy both into
   the project and point the brief at them.
5. **Rename this session** to the continuation name (see the ZWNJ warning above).
6. Re-verify live state with one cheap command, report three lines, stop.

## Then WAKE IT UP — a handoff is not a parking space

The seeding turn ends and the process exits, so the continuation is asleep. If
you stop there, the work stops there.

Where the work must live: **inside the continuation session**, with no process
attached to the parent chat. `hermes chat --resume` does record every message and
tool call in the child's session — but launching it with
`terminal(background=True)` leaves the launcher attached to the PARENT chat,
which the user sees and will object to.

So prefer a launch that this chat does not own:

```python
# BEST -- durable, owned by the scheduler, nothing runs in the parent chat.
cronjob(action="create", schedule="in 1m", repeat=1,
        name="<topic> — continuation kickoff",
        workdir="/path/to/project",
        prompt="""Continue session <child_id>. First open item: <task>.
                  Order: measure, then code, then test, then restart, then report.
                  Standing rules: <from the brief>.""")
```

`handoff.py --task "..."` does the equivalent inline. Use
`terminal(background=True)` only when the user is watching this chat and wants to
see progress here.

**Skip the kickoff when the user is present.** If they said "let's continue
there", they are about to open the chat themselves — the seeding turn's report IS
the handoff, and a kickoff would race their first message. Kick off autonomously
only when the handoff leaves them absent.

The kickoff prompt needs three things: `--work-turns 120` (8 or 25 is a
read-and-report budget and dies mid-task), a **numbered order of operations**
(measure → code → test → restart → report; without it the child writes code
before establishing facts), and **the standing rules repeated inline** — the child
read the brief, but the kickoff is what it is actually answering.

## Continuing in the new chat

- **READ THE PARENT IN FULL FIRST** — Rule Zero, before the brief, before
  `git status`, before answering anything. Treat any conflict as the transcript
  being right and the brief being stale.
- What to look for that briefs routinely lose: every "no" and why; instructions
  repeated more than once; judgements on specific artefacts; requests never
  completed; and the numbers — timings, HTTP codes, pixel measurements — that
  only exist in tool output.
- **State the counts in your first message.** "parent read: 844 live rows, 26
  unique user messages".
- Load the same skills the old chat used, explicitly, by name.
- Re-verify live state with one cheap command rather than trusting the brief
  (process alive? tests green? branch pushed?).
- Reference the parent by its `@session:<profile>/<id>` link once so the user can
  jump back.
- **This applies even when the user did not ask.** If a message references
  earlier work you cannot see, or a brief mentions a parent session id, that is
  the trigger.

## The `[SESSION WEIGHT …]` notice

If the `session-weight-watch` plugin is installed, a notice like this arrives
inside the user message when the thresholds are crossed:

```
[SESSION WEIGHT -- runtime measurement, not a user message]
Context is 344,116 of 500,000 tokens (69% of the point where Hermes will compact …
ACTION THIS TURN: finish the user's current question, then load the
`long-session-handoff` skill and follow it …
```

**That text is the runtime talking, not the user.** Finish answering the current
question first, then run measure → `clarify` → handoff.

It is a measurement, and measurements have bugs — this one shipped three. If the
numbers feel wrong, verify with `session_weight.py --session-id <id>` before
offering anything. A handoff offered on fabricated numbers is a mislabelled
success.

To park a session the watcher keeps flagging wrongly, set `suppressed` in
`<hermes home>/runtime/session-weight-watch.json`:

```json
{ "20260101_120000_abc123": { "suppressed": true, "why": "false positive: <what was wrong>" } }
```

A plugin loads once per process, so a fix on disk changes nothing until Hermes
restarts. Say that plainly; never claim a fix is live in the current chat.

## Pitfalls

- **Handing off silently.** The user loses trust instantly if a chat "moves"
  without being asked. Always `clarify` first.
- **Handing off mid-operation.** Never switch while a batch, deploy, or write is
  in flight. Finish or cleanly cancel it, confirm the system is at rest, then go.
- **Reading the brief and calling that "reading the parent".** The brief is step
  2 of the read, never step 1.
- **Scoring rows instead of tokens.** 2-4x overcount, and the source of every
  false alarm this tool has produced.
- **Scoring elapsed time.** Fires on sleep. Sum gaps under 10 minutes.
- **Treating a past compaction as a trigger.** It is a permanent historical fact;
  scored as a trigger it fires forever, on a session whose context is now small
  precisely BECAUSE it was compacted. Recover file 05 instead.
- **A brief that is a transcript.** Longer than a page means unread.
- **Losing the measurements.** The value of a long session is the facts it
  established (timings, HTTP codes, ids). Those go in the brief verbatim;
  opinions do not.
- **A name that does not say "continuation".** Without the marker the user cannot
  tell the chats apart. And never number from 1 — the original chat is 1.
- **Leaving the launcher process attached to the parent chat.** The point of a
  handoff is that this chat becomes idle.
- **Handing off and stopping there.** Approval is permission to MOVE the work,
  not to pause it.
- **Assuming `-m` pinned the child's model.** Read the row back.
- **Telling the user to open the chat themselves.** You can create it.
- **Querying `messages.created_at`.** The column is `timestamp` (float epoch),
  and `sessions` has `started_at` / `last_activity_at`, not `created_at`. Read
  `pragma table_info(...)` once instead of guessing schema.
- **Building a sqlite URI by hand.** `f"file:{path}?mode=ro"` breaks on a home
  directory containing `#` — sqlite truncates at the fragment, CREATES an empty
  database, and reports "no such table". Use `Path(p).as_uri() + "?mode=ro"`.
- **Printing session titles on a Windows console without forcing UTF-8.** The
  crash lands after the files are written, so a successful export looks like a
  total failure.

## Verification

- [ ] The weight was measured with real numbers, not a feeling.
- [ ] Permission was asked in one question with selectable options.
- [ ] Nothing was in flight at the moment of handoff.
- [ ] `dump_parent_session.py` ran and its files exist on disk, next to the brief
      when the handoff must outlive a reboot.
- [ ] The brief exists on disk and is under a page.
- [ ] The seeding prompt names the parent dump paths, not only the brief.
- [ ] **The continuation READ `01-user-messages.md` and `02-decisions.md` IN FULL**
      and quoted the row/unique counts back.
- [ ] The continuation session was created BY YOU and its id recorded.
- [ ] `sessions.model` was READ BACK and matches the parent (or what the user asked for).
- [ ] `max_iterations` is a working budget, not the seeding budget.
- [ ] `end_reason` is NULL and no stale turn lease remains.
- [ ] The new chat's name carries the parent's topic words plus a continuation marker.
- [ ] The new chat re-verified live state before continuing, and started nothing
      on its own.
- [ ] Either the continuation was KICKED OFF autonomously with no process
      attached to the parent chat, or the user is present and about to open it.
- [ ] The user was told what is now running and where, not asked to open a chat.
