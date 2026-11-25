---
name: miadi-react
description: >
  Read the emoji reactions people leave on GitHub issues and comments, as Miadi
  stores them, and know the open choices for letting a reaction hand work to an
  agent's tmux lane. GitHub sends no webhook for reactions; Miadi polls the
  Reactions API and keeps each reaction under owner/repo/issue and comment in
  Redis. Use the `miadi-react` CLI as it is (scan, show, events, watch, poll),
  or plan the next step with the human. Triggers on "reaction", "who reacted",
  "emoji on the issue", "thumbs up on the comment", "miadi-react", "react to
  trigger", "a reaction should start an agent", "delegate on reaction".
---

# miadi-react

## What exists

Miadi sees emoji reactions on GitHub issues, pull request conversations and
their comments. GitHub sends no webhook when someone reacts, so Miadi reads the
Reactions API:

- when any `issues` or `issue_comment` event arrives for a thread, right away;
- every 15 minutes, for every thread that had activity in the last 7 days
  (crontab of `mia` on gaia: `miadi-react poll --quiet`);
- whenever someone runs `miadi-react scan`.

Each reaction is stored under its thread (owner/repo#issue) and its subject
(the issue body, or one comment). Added and removed reactions go to an event
feed. Each new reaction runs `.github-hooks/reaction` in the Miadi checkout.

The first scan of a thread records what is already there without emitting
events, so old reactions do not arrive as new ones.

Built in jgwill/Miadi#688. This skill is tracked in
jgwill/miadi-orchestration-kit#57.

## Commands

```bash
miadi-react scan  owner/repo#N        # read the thread from GitHub now, store, print
miadi-react show  owner/repo#N        # print what is stored, without asking GitHub
miadi-react events [owner/repo#N]     # reactions added and removed, newest first (--limit N)
miadi-react watch                     # threads the poll rescans, most recently active first
miadi-react poll [--days 7] [--quiet] # rescan every thread active in the window
```

A thread can be written `owner/repo#N` or pasted as a GitHub URL. Add `--json`
to any command to get the API answer for parsing.

```
$ miadi-react scan jgwill/Miadi#688
🔎 jgwill/Miadi#688: 1 reaction(s), 1 added, 0 removed
jgwill/Miadi#688 — Reactions on issues and comments are stored per thread …
  https://github.com/jgwill/Miadi/issues/688
  scanned 2026-09-27T07:36:59.969Z · 1 reaction(s)
  issue               👀 eyes	miadisabelle	2026-09-27T07:36:58Z
```

On gaia the command is `/usr/local/bin/miadi-react`, a link to
`scripts/miadi-react` in the Miadi checkout. From another host, set
`MIADI_BASE_URL` to the Miadi front and `MIADI_API_TOKEN_WRITER` to a writer
token, or call the API directly:

```bash
curl -s "$MIADI_BASE_URL/api/github/reactions?thread=jgwill/Miadi%23688"
curl -s "$MIADI_BASE_URL/api/github/reactions?events=1&limit=20"
curl -s -X POST -H "Authorization: Bearer $MIADI_API_TOKEN_WRITER" \
  -H 'Content-Type: application/json' -d '{"thread":"jgwill/Miadi#688"}' \
  "$MIADI_BASE_URL/api/github/reactions"
```

## Using it now, as it is

- **Ask for a reaction instead of a reply.** When you post a proposal or a
  draft on an issue, tell the human that a 👍 or 👎 on that comment is enough.
  Read the answer with `miadi-react show owner/repo#N`, and match the
  `comment <id>` to the comment you posted.
- **Check before acting.** Before starting work on an issue, `miadi-react show`
  tells you whether the human already reacted to the issue or to one of the
  agents' comments.
- **Read the feed at the start of a session.** `miadi-react events --limit 20`
  lists what people reacted to since you last looked.

A reaction's `created_at` is GitHub's time. An event's `at` is when Miadi's
scan saw it, which can be up to 15 minutes later.

## Where it lives in jgwill/Miadi

| part | path |
|---|---|
| thread reference, keys, comparison (pure, tested) | `lib/github-reactions.ts`, `lib/github-reactions.test.ts` |
| GitHub fetch, Redis writes, hook run, poll | `lib/github-reactions-store.ts` |
| API door | `app/api/github/reactions/route.ts` |
| webhook trigger | `app/api/workflow/webhook/route.ts` (block "Reaction capture") |
| hook | `.github-hooks/reaction` (env: `WEBHOOK_REACTION_CONTENT`, `_USER`, `_SUBJECT`, `WEBHOOK_ISSUE_NUMBER`, `WEBHOOK_COMMENT_ID`, …) |
| CLI | `scripts/miadi-react` |

Redis keys:

```
reactions:thread:<owner>:<repo>:<n>   HASH  issue:<rid> | comment:<cid>:<rid> → reaction
reactions:meta:<owner>:<repo>:<n>     HASH  title, url, total, scanned_at, baseline_at
reactions:events                      LIST  added/removed events, newest first, 1000 kept
reactions:watch                       ZSET  owner/repo#n by last activity
```

Traces go to `/src/logs.miadi.log` under `reactions.scan`, `reactions.poll`,
`reactions.scan.error`. The poll's own log is `/a/src/logs.miadi-react.log`.

## Not covered

- Reactions on pull request review comments (the inline code comments). They
  have their own API endpoint, which the scan does not read.
- A thread with no activity for 7 days leaves the poll. Its reactions are read
  only when someone runs `scan`, or when the thread becomes active again.

## Next: a reaction hands work to a tmux lane

Not built. `.github-hooks/reaction` only writes a log line today. The route a
delegation would take already exists for mentions: `.github-hooks/stc` posts to
`POST /api/stc/steer` with the writer token, and the steering layer
(`lib/stc/steering.ts`, `config/stc-steering.json`, jgwill/Miadi#549) renders a
prompt and types it into the target tmux session: `stcbot` (Mino) by default,
seat `mia` for the `architecture` and `review` classes. A reaction would follow
the same path, from `.github-hooks/reaction` to `/api/stc/steer`.

These choices belong to the human. Present them, record the answers on
jgwill/Miadi#688, and do not wire delegation before Q1 to Q3 are answered.

### Q1. What each reaction asks for

A starting proposal to accept or change:

| reaction | proposed meaning |
|---|---|
| 👀 eyes | look at this: triage it |
| 🚀 rocket | start the work this issue or comment describes |
| 👍 +1 | approve what was reacted to (a draft, a plan, a verdict) |
| 👎 -1 | decline it |
| 😕 confused | the comment is unclear: ask a question back |
| ❤️ 😄 🎉 | acknowledgement: store, no action |

### Q2. Which lane receives it

- `stcbot` (Mino) for every reaction, as mentions do today.
- A lane by meaning, reusing `classRoutes`: 🚀 to the seat that builds, 👀 to
  `stcbot`.
- The lane already working on that issue, when one is alive (a tmux session or
  herdr workspace named for the issue), and `stcbot` otherwise.

### Q3. Whose reactions count

- An allowlist, like `MIADI_AGENT_ALLOWED_AUTHORS` (default `jgwill`) for
  `/agent` comments.
- The agents' own GitHub accounts must never trigger a lane. `gh` on gaia acts
  as `miadisabelle`, so an agent's own reaction would otherwise wake an agent.

### Q4. What the subject changes

A reaction on an agent's own comment answers that comment. A reaction on the
issue body is about the whole issue. The prompt sent to the lane should say
which it is, and include the comment's text when it is a comment.

### Q5. Dry run first

The steering layer supports `dryRun`. Run delegation in dry run until the human
has seen a few rendered prompts and agrees with the map.

## Related

- jgwill/Miadi#688: the feature, and where the delegation answers are recorded
- jgwill/miadi-orchestration-kit#57: this skill
- jgwill/Miadi#549: STC steering, the path to a tmux lane
- `chronicle-episode`, `hear-ground-weave`: when a reaction should become part
  of an episode or a day's coordination loop
