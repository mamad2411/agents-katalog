---
name: session-review
description: "Review a finished session from its transcript: for each request, which skill should have fired and did not, or fired late, and for each miss one proposal — a trigger wording change or a deterministic check. Reads a transcript, edits nothing. Trigger words (RU+EN): разбор сессии, какой скилл не сработал, скилл сработал поздно, ретро по транскрипту / session review, which skill did not fire, skill fired late, transcript retro."
disable-model-invocation: true
---

# Session review

Whether a skill fires on the request it was written for is assumed, not looked at. This skill looks:
it reads one transcript, lines each request up against the skill descriptions that session had, and
names what should have fired and did not, or fired late. A miss found here costs one reading; found
by its damage, it costs a review round or a broken run.

## Input

A transcript: `~/.claude/projects/<project dir>/<session id>.jsonl`, the project dir being the
project path with every character other than a letter or a digit replaced by `-`
(`/srv/my_app` → `-srv-my-app`). Without a path, list them by time, this session left out, and
ask which: `ls -lt ~/.claude/projects/<project dir>/*.jsonl | grep -v "$CLAUDE_CODE_SESSION_ID" |
head -6`. Other sessions may be running in parallel: a file written in the last minutes is one of
them, not a finished session. Several transcripts are reviewed one by one and merged in the output.
Needs `jq`; without it, stop and say so — reading the raw transcript instead means megabytes of tool
output.

## Step 1 — the timeline

One line per event, numbered. `ASK` is a request: the owner's text or a peer session's message,
the peer's name in brackets. A message typed while the agent works is stored apart from the turn
(a queued command), and the program reads both places. `SKILL` is a skill call or a slash command,
with its arguments after `·`; a built-in command (`/model`, `/reload-plugins`) shows the same way
and is not a skill. `TOOL` is any other tool call, with its path or command.
`DONE` is a background job or a sub-agent coming back — for a review role, its first line is the
verdict, and that is the moment findings arrive. A sub-agent run in the foreground returns as the
result of its own `TOOL Agent` line and leaves no `DONE`: read that result in the transcript.

```sh
T=<transcript.jsonl>
jq -r '
def clip(n): gsub("\\s+"; " ") | .[:n];
def text: if type == "string" then . else (map(select(.type == "text") | .text) | join(" ")) end;
def event($meta):
  if test("<command-name>") then "SKILL  " + (capture("<command-name>/?(?<c>[^<]*)").c)
      + ((try capture("<command-args>(?<a>[^<]+)").a catch "") | if . == "" then "" else " · " + clip(100) end)
  elif test("^\\s*<task-notification>") then "DONE   " + ((try capture("<summary>(?<s>[^<]*)").s catch "") | clip(120))
  elif test("<agent-message") then "DONE   " + (sub("^[\\s\\S]*?The report follows:"; "") | clip(120))
  elif test("<cross-session-message") then "ASK    [" + ((try capture("from-name=\"(?<n>[^\"]*)\"").n catch "peer"))
      + "] " + (sub("^[\\s\\S]*?<cross-session-message[^>]*>"; "") | sub("</cross-session-message>[\\s\\S]*$"; "") | clip(140))
  elif $meta or . == "" then empty
  elif test("^\\s*(<(system-reminder|local-command)|This session is being continued|\\[Request interrupted)") then empty
  else "ASK    " + clip(160) end;
if .type == "user" then (.isMeta // false) as $m | .message.content | text | event($m)
elif .type == "attachment" and .attachment.type == "queued_command" then
  (.attachment.origin.kind != "human") as $m | .attachment.prompt | text | event($m)
elif .type == "assistant" then
  .message.content[]? | select(.type == "tool_use")
  | if .name == "Skill" then "SKILL  " + .input.skill
    else "TOOL   " + .name + " " + ((.input.file_path // .input.command // .input.description // "") | tostring | clip(70)) end
else empty end' "$T" | cat -n
```

The skills that session had, with their descriptions — judge against these, not the current tree:

```sh
jq -r 'select(.type == "attachment" and .attachment.type == "skill_listing") | .attachment.content' "$T"
```

A session may hold several listings: a resumed session repeats the initial one, and a later
non-initial one adds the skills that appeared mid-session. A long timeline is read around each
`ASK`, not whole: the `TOOL Bash` lines are most of it. No `ASK` line, or no listing, means the
transcript's format moved and nothing was extracted — say exactly that, never «no misses».

## Step 2 — judge each request

For each `ASK`, find the skills whose description matches it — its trigger words, or the kind of
work it starts («a code task», «a hard bug», «before searching»). Then find the first `SKILL` line
with that name and the first `TOOL` line the description says the skill must come BEFORE (an edit,
a commit, a grep, a new file, a teardown). An edit is not only `Edit` and `Write`: where those
tools are closed, files change through `Bash` — `git rm`, `sed -i`, `python3 - <<EOF`, `cat >`.
A write into memory or a scratch file is not the task's edit. One verdict per pair:

| verdict | when |
|---|---|
| `ok` | the skill fired before that tool line |
| `late` | it fired, after that tool line — give both line numbers |
| `missed` | it did not fire on this work at all |
| `stray` | it fired, and no request in range matches its description |

Not a miss, so not counted:
- a request with no new work — «go», «ok», «merge», an answer to a question in flight;
- a skill already loaded earlier on the same work;
- an owner-invoked skill: the agent cannot call it; the most it owed was to name the command;
- a case the skill's own «When NOT to apply» section excludes — read it before writing `missed`;
- a skill the session's listing does not hold.

## Step 3 — one proposal per miss

Decide by whether the miss is mechanical:

- **Mechanical** — visible in the event stream without judgement: an edit before any `task-cycle`,
  a new file before `complexity-budget`, a push before a review role ran. Propose a deterministic
  check and name the existing place it would join before a new one: a row in the write advisor's
  table (`hooks/write_advice.rules`, kind · file mask · skill) when a file kind gives the work
  away, otherwise a hook, the route, a gate step.
- **Judgement** — the request's words were not among the triggers, or the description reads as
  another skill's. Propose the wording: the words to add to the description, quoting the request.

A miss that repeats across transcripts weighs more than one; say how many sessions show it.

## Output

In the language of the request. Per session, a table:

| # | request | should fire | verdict | lines | proposal |
|---|---|---|---|---|---|

Then the proposals grouped by skill, one line each, the repeated ones first.

The output quotes requests and verdicts, not commands: a `TOOL` line can carry a token. Anything
that leaves the session — a task comment, a message — goes through the project's secret masking
first.

## When NOT to apply

- Not for judging the work itself or the code — that is the review roles; this reads only which
  skills fired and when.
- Not on a session still running: its transcript stops mid-work and every late skill reads as missed.
- It edits nothing — no skill, hook or setting. A proposal becomes a change through the owner and a
  task.
- A sub-agent's work lives in its own transcript; here it shows as its `TOOL Agent` line and its
  report.
