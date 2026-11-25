---
name: bot-run
description: "How to run an @bot line: delegate it to its own session and wait for the result."
hidden: true
---

# Running an @bot line

Every `[subagent·@name]` line in the message is that Bot's work, not yours. Hand it to a session of
its own and wait for the answer — you are the dispatcher for these lines, not the executor. The
turn is: write a brief (§1), POST it (§2), wait (`wait.md`), report (§3).

Do **not** read the `BOT.md` or `bot-turn` of a Bot you are delegating to. They are listed at the
end of the message under "pass the path along; do not open them yourself" — that is the only
reason you have those paths. The child reads them and works from them; keeping them out of this
session is the point.

## `[main·@name]` is the opposite instruction

A line tagged `[main·@name]` means that Bot's directory **is this
session's own working directory**. There is nothing to delegate — you are already sitting in the
files a child would have been started to reach. Read the `bot-turn` path, then that Bot's
`BOT.md` — both are in the "read these skill files first" list rather than the handoff list,
because you are their reader this time — and do the task yourself, in the voice its identity files
define. Nothing else in this file applies to such a line: no brief, no delegate call, no polling.

A message may carry both tags. When it does, the order matters: **POST every `[subagent·@name]`
brief first, then do your own `[main·@name]` work, then poll.** The children run while you
work; doing your own part first only makes them start late. In that message `bot-turn` is listed
in both blocks on purpose — you read it for your own line and hand the same path over for theirs.

## What else to open, and when

Two files live next to this one and are opened only when the turn reaches them — **check this
table before you act, not after**:

| Open | When | Why it is not here |
|---|---|---|
| `{{COCKPIT_DIR}}/skills/bot-run/wait.md` | **The moment a delegate POST has returned** — before any status call | The poll loop, the budget rule, and what each status means. Every delegation needs it and no `[main·@name]` line does, so it stays one read away rather than in front of a session that never delegates |
| `{{COCKPIT_DIR}}/skills/bot-run/followup.md` | The Bot asked something back, or the user answers your report | Continuing a session that already exists. Usually a later turn, and the turn that delegates does not need it in hand |

**Never poll from memory of how this works.** If a POST has returned and you have not opened
`wait.md` this turn, stop and open it. Hand-rolled status checks fail in one direction only —
they exit at once and you report a result the child never produced — and that failure is invisible
from here, because a confident summary of a run that never finished reads exactly like a real one.

## 1. Write a self-contained brief

The child sees none of this conversation. Everything it needs goes in the brief: the user's
intent in their own words, the context you have accumulated here (which repository, which files
are in scope, what was already decided, what it should NOT re-litigate), and what "done" looks
like. This is the whole value of delegating from here rather than letting the user type it — the
brief you write is the part the user did not have to.

Start it with both paths, in this order — the general contract, then the particular Bot:

> Read `<the bot-turn path>` for how a Bot turn works, then `<the Bot's BOT.md path>` for who this
> Bot is and which of its files to read. Follow its "Before working" section, then do the task in
> the voice its identity files define.

Both paths are in the list at the end of the message. Pass them verbatim; a child that is missing
`bot-turn` has no write-lock protocol and will invent one.

**Write only what you learned here; never assert what the Bot remembers.** You have not read its
files — it has. A brief that says "this is already settled in its memory" is a guess dressed as a
citation, and the child will take it as a premise it may not re-open. Say where a constraint
actually came from ("the user said so in this conversation"), and leave its memory to it.

## 2. Delegate — fire every @bot line before waiting on any of them

```bash
BRIEF=$(mktemp /tmp/cockpit-brief.XXXXXX)
cat > "$BRIEF" <<'EOF_BRIEF'
<the brief>
EOF_BRIEF

curl -sS --fail-with-body -X POST "{{BASE_URL}}/api/sessions/delegate" \
  -H "Content-Type: application/json" -H "x-cockpit-run-id: $COCKPIT_RUN_ID" \
  --data-binary @- <<EOF_JSON
{"cwd": "${COCKPIT_CWD:-$PWD}", "title": "@<name>: <short label>", "briefPath": "$BRIEF"}
EOF_JSON
```

The body is `{ cwd, engine?, model?, title?, prompt? | briefPath? }`:

- **Do not delete the brief file.** The POST returns before the child has read it: the endpoint
  only checks that the file exists, and the child is handed the *path*. Tidying up `$BRIEF` after
  the call leaves it with a task it cannot read.
- **`cwd` has two right answers, decided by what the line asks for:**

  | The `@name` line is | `cwd` |
  |---|---|
  | ordinary work | `${COCKPIT_CWD:-$PWD}` — exactly as written above, a variable you never resolve yourself |
  | "导出 / export", "复盘 / review", "装上 / attach" | the Bot's own directory: `dirname` of the BOT.md path listed at the end of the message |

  Ordinary work happens in the project, and the Bot reaches its own files by absolute path. The
  three maintenance verbs are work *on the Bot*: its files are the subject, its `.locks/` is
  there, and a review writes `.reviews/` into it — a child sitting in some unrelated project would
  reach all of that by absolute path for no reason, and `git` inside the Bot's own repository
  would not work at all. Taking `dirname` of that path is not opening it; the rule against reading
  it stands.

  **`COCKPIT_CWD` is this session's own working directory, exported by Cockpit.** Leave it as a
  variable in the JSON — the heredoc expands it. Never substitute a path you worked out instead:
  not the git root, not the nearest directory with a CLAUDE.md, not any parent that looks more
  like a project than where you are. Doing that silently moves the child one or more levels above
  where the user is working, and its transcript then lands under a different project in the
  session list — which is what happened when a session working inside a subdirectory delegated a
  child at the repository root instead. It is also not `pwd`: `pwd` follows any `cd` this turn has
  made, which is why the fallback is only there for a Cockpit too old to export the variable.
- **Leave `engine` unset unless the user named one.** Omitted, the child inherits the engine this
  session is running on — the `x-cockpit-run-id` header is what tells the server which that is, so
  send the header exactly as written above. Set it only when the `@name` line says which engine to
  use ("用 codex 跑一下", "run this one on glm"); one of `claude`, `codex`, `deepseek`, `kimi`,
  `glm`, `ollama`. Never open `BOT.md` to invent a preference — a Bot manifest has only `name` and
  `description`, and it is not where this decision lives.
- Leave `model` unset. It is not inherited: the engine picks its own default, and a model chosen
  for this conversation would otherwise be multiplied across every child you start.
- `title` is optional but always worth setting — it is how the session is listed later.
- For a one-line task you may send `"prompt": "..."` instead of `briefPath` (escape `"` and `\`).
  A Bot task rarely is one: the brief carries the accumulated context, which is the whole point.
- The receipt comes back at once: `{ cwd, engine, model?, sessionId, link, title, createdAt,
  parent? }`. Post every Bot's brief first, **then open `wait.md`** — one wait covers them all.
- A 400 names the problem — cwd missing, relative, or not a directory; a brief file that does not
  exist; too many delegated sessions already running. Report what it says; do not retry blindly.

## 3. Report

One short section per Bot: its conclusion in a few lines, then `[open session](<link>)`. The full
answer lives in that session — do not paste it wholesale, and do not restate it as your own.
`lastReply` is cut at 4000 characters; when `lastReplyTruncated` is true and you need the rest,
repeat the status call with `--data-urlencode "full=1"`. Use the receipt's `link` exactly as
returned — it is the only record of the delegation, and tool output is not searchable later.

**A `[main·@name]` line has no link**, because it happened here. Give it its own section
alongside the delegated ones and close it the way `bot-turn` §2 requires — the answer, then the
list of Bot files you read and changed. That list is the only record of what the answer stood on,
and this is the one line in the message that may have edited those files directly.

**A numbered list is a special case.** Some Bot tasks (a review sweep, for instance) end in a list
of findings the user picks from. Relay it whole with its numbering intact, and keep whatever path
the child saved it to — the user answers either in that session or by naming that file in a new
one, and dropping either detail strands the work.

Pressing stop here does not stop a delegated session — it is a separate run. Say so if the user
expects otherwise. A `[main·@name]` line is the exception: it runs in this session, so
stop really does stop it.

When the user answers your report — a correction, a pick from a numbered list, an answer to a
question the Bot asked — that reply belongs in the session it came from. Open `followup.md`; do
not start a second one.
