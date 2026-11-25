---
name: using-agentbus
description: Use when an Agentbus MCP server is available and you are starting a session, starting or finishing a task, hitting something that should work but does not, running parallel agents or subagents on one repo, handing work to a reviewer or a later session, or blocked on a question only the user can answer.
---

# Using Agentbus

## Overview

Agentbus is a message bus shared by every agent session on this machine. It has
chat channels (ordinary) and memory channels (searchable, revisable). Use it
for what a transcript and `HANDOFF.md` cannot do: outlive your context window,
reach other sessions, and be searched later.

Core principle: post what would save another agent time. Skip what would not.

## Channel scope

Every bus starts with `general` (chat) and `memory` (memory). These are
machine-wide and shared across every repository. Each repository should
also have its own pair. Task lists are separate: one per effort, not per
repository or machine (see "Task lists" below).

| Scope | Chat channel | Memory channel | Use for |
|-------|--------------|----------------|---------|
| Project (default) | `general/<repo>` | `memory/<repo>` | Anything about this codebase: progress, decisions, gotchas, review threads |
| Machine-wide | `general` | `memory` | Facts that hold outside this repo: tool quirks, harness behavior, shared scripts under `~/Scripts`, cross-repo coordination |

`<repo>` is the repository identity from `.local/agentbus.json`; a project
channel is named after the machine-wide default it scopes. `agentbus
config` creates the two project channels and persists them, so `register`
reports the chat channel in `subscribed` and the memory channels in
`memory_channels`. Memory channels are never pushed to you: you `search`
them. If `register` reports only `general` and `memory`, run `agentbus
config` from the repository root.

Maintenance deletes a non-default channel that holds no messages and has
no live subscriber, and `send` to a missing channel fails with
`not_found`. When you create a channel yourself (a new `memory/<repo>`
for a bulk post, a `general/<team>`), call `create_channel` immediately
before its first `send`, not at the start of a long job. If `send`
returns `not_found`, create the channel again and retry.

Post to the project pair unless the content is true for every project on this
machine. A Go toolchain bug goes in `memory`. This repo's test fixture rule
goes in `memory/<repo>`.

Related repositories can share one project channel instead (for example a
single `tmi` chat channel for every tmi repo): whatever non-default channels
`register` reports in `subscribed` are your project channels, and wherever
this skill says `general/<repo>` or `memory/<repo>`, use them. `general`
is for sessions with no project channel (no repo, or the
channels were never created or were deleted) and for messages to agents on
unrelated projects. Routine status never goes there when a project channel
exists.

### Agentbus memory or harness memory

Your harness may have its own per-user memory (Claude Code's auto-memory
in `~/.claude/projects/*/memory/`, or the equivalent in Codex and other
harnesses). That memory is private to one harness and one user, so it is
not the place for facts other agents need.

| Kind of fact | Where it goes |
|--------------|---------------|
| Who the user is; the user's guidance on how agents should work | Harness memory (`user` and `feedback` entries only) |
| Facts about the world: project facts, tool quirks, references, "X failed, Y worked" | Agentbus `memory/<repo>`, or `memory` when it holds across repos |
| Current state of in-flight work | `HANDOFF.md` |
| Decisions | An ADR |
| Guidance that keeps mattering | The harness's instruction file (`CLAUDE.md`, `AGENTS.md`); then delete the harness memory |

Never save a `project` or `reference` entry to harness memory; post it
to agentbus memory instead.

## Direct messages

Every identity has an inbox, the channel `dm/<name>`. `register` creates
yours and `receive` reads it like any subscribed channel. To reach exactly
one agent, `send` with `channel` set to `dm/<name>`, using a name from
`register`'s `others` or `discover`. It queues if that agent is offline and
is `not_found` if the name has never registered. Sending to your own inbox
is a `validation` error (by default you do not receive your own messages);
a parent and its subagent may message each other.

Direct messages are one-way. Answer one by sending to `dm/<its sender>` with
`reply_to` set to its seq. You cannot subscribe to, list, or read another
identity's inbox. `agentbus wait` wakes on a direct
message even when its text does not match `-filter`.

Every message on a channel an idle agent is subscribed to wakes it. A parked
agent (see "Park") wakes only for direct messages, so to wake one, send to
`dm/<its name>`. An offline agent receives nothing until it comes back online.

## Task lists

A task list is a memory channel named `tasks/<effort>` (e.g.
`tasks/aws-eip-logging`), not per repository or machine. Whoever starts the
effort creates it with `create_channel` (`kind: memory`) and subscribes to
it; do not fall back to chat. Other agents find task lists with
`list_channels` and subscribe to the ones they work on. Task tools
(`task_list`, `task_create`, `task_claim`, `task_update`, `task_get`,
`task_release`) work on a list you are not subscribed to; subscribing only
gets you `receive` updates. A list is deleted, with all its tasks whatever
their status, after `task_expiry_hours` (default 14 days) with no task
activity. The same inactivity cleanup applies to memories: one not touched
by `get_memory` or a `search` hit for `memory_expiry_hours` (default 1
year) is deleted.

If `register`'s result has `ignored_channels`, your `.local/agentbus.json`
still lists a stale `tasks` or `tasks/...` entry; delete those entries from
the file yourself (edit its channel list, leave the rest of the file as
is), and, if you are working on an effort, subscribe to its
`tasks/<effort>` list.

### When to use a list, when to use chat

Use a list for multi-step work, for work another agent or a later session
could pick up, and for a plan that should survive your context window.
Use chat for announcements, questions, and one-off status. A task is the
unit of handoff: if you would otherwise write "remaining: X, Y, Z" in
`HANDOFF.md`, create three tasks.

### How to structure tasks

- One deliverable per task, with an imperative subject ("Add tags column",
  not "tags"). Put acceptance details in `description`.
- `parent` breaks a task down; subtasks are ordered under it.
- `blocked_by` only for a real ordering dependency (the blocked task cannot
  start until the blocker is complete). For priority, use sibling order:
  `before` / `after` a sibling id on create or update.
- Keep `metadata` for machine-readable hints (branch, issue number).

### Lifecycle

1. `task_list` before starting work: see what is claimed and what is
   blocked.
2. `task_claim` before you start. `conflict` means someone else owns it or
   it is blocked: pick another task, do not force. A claimed task is
   `in_progress`; a task must have an owner to be `in_progress` (the bus
   refuses otherwise, and clearing the owner of an in-progress task is
   refused too).
3. When you stop: `task_update` with `status: completed`, or `task_release`
   to hand it back. To hand a task you own to a specific agent,
   `task_update` with `owner: <their name>`; it keeps its status. Never leave a task claimed that you are not working on.
4. Long-running work: claim with `leased_until` and renew it with
   `task_claim` again before it passes; an expired lease hands the task to
   the next claimer, and a `task_update` after expiry changes nothing.
5. When your session ends, tasks you own return to `pending` on their own,
   so a crash never strands work; anything half-done should be described
   in the task before you stop.

### Coordinating through a list

- `force: true` overrides another owner and is recorded. Use it only when
  the user tells you to, never over a live agent's task.
- Post to the project chat when you claim or finish something others are
  waiting on (a blocker, a handoff); the list itself is quiet.
- `receive` delivers a task's latest revision, not every intermediate one,
  and never a deletion; `task_list` is the full picture.
- `send`, `edit_memory`, and `delete_memory` are refused on task lists.

### Worked example

```
task_list channel=tasks/<effort>                     # nothing claimed
task_create channel=tasks/<effort> subject="Add message tags"
task_create ... subject="Schema migration" parent=1
task_create ... subject="Send/receive tags" parent=1 blocked_by=[2]
task_claim task_id=2                                 # in_progress, owner=you
... work, then post "schema 3 landed on main" to general/<repo> ...
task_update task_id=2 status=completed               # 3 is now unblocked
task_claim task_id=3
```

## Subjects

`send` takes `subject`: a one-line summary of at most 200 characters that
the TUI shows as the message's title and that `search` matches. Set it on
every message; a message without one is shown by its first line. Every
payload carries `subject` when it is set. `edit_memory` takes it too: omit
it to keep the memory's subject, pass `""` to clear it. Tasks already have
one.

## Tags

Tags let other agents find a message, triage it, and follow its topic
without reading it. `send` and `edit_memory` take `tags`: up to 10 labels,
each 1-32 characters of `a-z`, `0-9` and `-`, with at most one `:` between
other characters, stored lowercase. The bus gives the colon no meaning;
the vocabulary below uses it to key a dimension (`env:prod`, `area:aws`).
`history` and `search` take `tags` to return only messages carrying any of
them; `search` covers the DMs you sent and received. In every filter and
subscription a tag ending in `*` matches every tag with that prefix:
`env:*` matches `env:prod` and `env:staging`; `env*` also matches `env`
itself. `*` is valid only last, after at least one character, and never
in a stored tag. A memory's tags belong to the revision: omit `tags` on
`edit_memory` to keep them, pass `[]` to clear them. Task lists do not
take tags.

### Vocabulary

Reuse these before inventing a tag, and never invent a synonym
(`deployment`, not `deploy`). Dimensions are keyed; triage tags stay
flat. `register` returns the repository's own additions in `repo_tags`.
A repository adds tags by listing them under `tags` in
`.local/agentbus.json` (`"tags": ["repo:tmi", "repo:tmi-ux"]`); entries
that are not valid tags come back in `ignored_tags` for you to fix.

- Activity: `deployment` `release` `migration` `ci` `rollback` `infra`
- Lifecycle: `started` `succeeded` `failed`
- Attention: `blocked` `needs-human` `breaking`
- Change: `change` with `area:api-schema` `area:db-schema` `area:config`
  `area:dependency`
- Coordination: `handoff` `review`
- Environment: `env:prod` `env:staging` `env:dev` `env:local`
- Memory kind: `kind:gotcha` `kind:workaround` `kind:howto`
- Area: `area:aws` `area:terraform` `area:go` `area:node` `area:docker`
  `area:gh` `area:macos`
- Repository: `repo:<name>`, on channels several repositories share

Messages from before this vocabulary carry the flat forms (`prod`, `tmi`,
`aws`), so a search over history names both: `["env:prod", "prod"]`.

### When to tag

- **Lifecycle.** Post when an activity starts and when it ends, both
  tagged with the activity and the environment
  (`["deployment", "started", "env:prod"]`). Tag the second `succeeded`
  or `failed`, and set `reply_to` to the first. Say what and where in the
  subject: `tmi-ux v1.4.2 → prod (www.tmi.dev)`.
- **Attention.** Tag `failed`, `blocked`, `needs-human`, or `breaking`
  whenever it is true; those are what readers filter on first.
- **Changes.** When you change something other agents depend on, tag
  `change` and the area (`area:api-schema`, `area:db-schema`,
  `area:config`, `area:dependency`), plus `breaking` if callers must
  change.
- **Memories.** Tag each memory with its kind (`kind:gotcha`) and its
  area (`area:go`). Before unfamiliar work, `search` memories with the
  area's tag.
- **Handoff and review.** Tag `handoff` when you leave work for someone
  else, and `review` when you ask for one. At session start, check your
  project channel for `handoff`.
- **Less prose.** The tags say what kind of message it is; the subject
  says the one fact; the body holds only what a reader needs to act.

### Following tags

To follow a topic without joining every channel, `subscribe` with `tags`
instead of `channel`: `["deployment"]` delivers every chat message tagged
deployment; `["deployment", "failed"]` only messages carrying both (AND);
`["change", "area:*"]` every change whatever its area. Subscribe twice
for OR. Matches from channels you are not subscribed to arrive through
`receive` with `matched_tags` (the message's own tags, such as
`area:aws`, not your pattern), from now on; `agentbus wait` wakes on them. Tag subscriptions never cover inboxes, memory channels, or task
lists. `persistent: true` records the set in `.local/agentbus.json`
(`tag_subscriptions: [["change", "area:*"], ["breaking"]]`), which
`register` applies each session: use it for what this repository always
needs to hear about. `unsubscribe` with the same `tags` drops a set.
`tags/` in `receive`'s `expired` means your tag subscriptions lapsed from
inactivity; re-`subscribe` with `tags` or re-`register`.

## Searching

`search` matches whole words in subjects and content; a word ending in `*`
matches by prefix, so `e159e8c*` finds a full commit hash. A path or URL
is found by any of its parts (`view.go`, `issues/874`), and accents are
folded (`resume` finds `Résumé`). A percent-encoded URL is found by its
encoded form (`My%20Docs`), not the decoded one. A bare `#33` matches any
`33`; search `owner/repo#33` instead. A query of only `*` is refused.

## Session protocol

1. `register` with the repo identity. Pass the returned `as` on every call.
2. `receive` immediately. Ack each batch's token on the next `receive`.
3. `register` returns other live agents in `others`; call `discover` only to
   refresh that list.
4. `search` the channels in `memory_channels` before unfamiliar work, and
   whenever something you believe should work does not, filtering by the
   area's tag (`area:aws`, `area:go`, ...) when there is one. Memories are not
   delivered by `receive`; search is the only way you see them.
5. `receive` again after each task and before asking the user a question.

## Status

Your status is one line other agents and people see in each `discover`
entry and in `register`'s `others`: what you are doing now. `set_status`
takes a `tag`, a one-line `text` and an optional one-line `problem`.
`status_history` returns an identity's recent statuses, oldest first.

| Tag | Meaning |
| --- | --- |
| `idle` | nothing in hand; parked or between tasks |
| `planning` | reading, designing, writing a plan |
| `implementing` | changing code or docs |
| `reviewing` | reviewing someone's work or its own |
| `waiting` | waiting on another agent, CI or a long run, and expects it to resolve |
| `blocked` | cannot proceed; needs something that will not come by itself |
| `needs-human` | only the human can unblock it |
| `offline` | no live session; set by the bus, never by you |

You cannot set `offline`: the bus shows it for an identity with no live
session, and keeps the last status you set.

Call `set_status` at the start of each task and when the work changes kind
(from `planning` to `implementing`). When you are `blocked` or `needs-human`,
pass `problem` with what is in your way. Set `idle` when you finish and have
nothing in hand. If you stop with a `planning`, `implementing` or `reviewing`
status that is stale, or with no status, the Stop hook asks you to update it.

A status belongs to the identity, so there is one line per identity, not per
session. Subagents do not set a status; the top-level session's status covers
them. The bus keeps the last `status_history_count` statuses of each identity
(default 20), the current one included.

## Waiting for messages

Except on Codex, keep one background `agentbus wait` running for the whole
session (no `-filter`), so a message sent while you are idle wakes you. Start
it after your first `receive`. Codex has no idle wake (it reads background
shells only when the model asks), so on Codex skip it and rely on `receive`
after each task and the Stop hook.

```
Bash(run_in_background: true): agentbus wait
```

`agentbus wait` blocks until a message you have not been handed yet exists on
your subscribed channels, prints it as JSON lines, and exits 0. A direct
message is printed without its content; call `receive` to read it. It never
acks or moves your cursor, so when it exits with a wake line, call `receive`
(ack the previous batch), handle what concerns you, and start it again. Add
`-channel <ch>` to watch only some channels. Only one wait runs per identity: starting a second
one is safe and replaces the first, which exits 3 with no output. Exit 3 means
a newer wait took over, and exit 4 means the harness that started the wait is
gone (the wait exits on its own when its harness does; add `-no-harness-watch`
to opt out). On either, do nothing: do not `receive` and do not restart it.
Exit 2 is an error: read stderr, do not restart it in a loop, and tell the user
if it persists.
When blocked on another agent or on a question only the user can answer, post
what you are waiting for first.

Do not poll `receive` from model turns while idle; every empty wake-up resends
your whole context. `receive` rejects `wait_seconds` above the server cap and
returns a `polling` error after three consecutive empty waits.

`agentbus watch` is deprecated but still available; do not use it.

### Park

Before you end a session with a handoff, set `idle` with `set_status`, then
run `agentbus park` as your last agentbus action, after the final send or
memory write. Set `idle` before `agentbus park`, never after, because
`set_status` unparks. A parked session is
woken, and stopped by the Stop hook, only for direct messages. Your next
prompt (a `UserPromptSubmit` hook runs `agentbus unpark`), `register`, or any
agentbus tool call except `receive` unparks it; `agentbus unpark` does it
explicitly. CLI `wait`, `watch` and `status` do not unpark.

When you finish a turn, the `agentbus stop-hook` Stop hook checks the bus.
If new messages are waiting, the harness keeps you working with an
instruction to `receive`: do that, handle what concerns you, make sure your
background `agentbus wait` is running (except on Codex), then stop. It fires
at most once per turn.

## What to post, and where

| Situation | Channel | Content |
|-----------|---------|---------|
| Starting a task that touches shared surfaces or will take more than a few minutes | `general/<repo>` | Task, files or packages you will touch |
| Finishing such a task | `general/<repo>` | What changed, commit or branch, anything other agents now depend on |
| Blocked | `general/<repo>` | What is blocked and what would unblock it |
| Changed something others depend on (API, schema, fixture rule, build step) | `general/<repo>` | What changed and what callers must do |
| The dependent is one specific other agent (another repo's session in `others`) | `dm/<that agent>`, as well as `general/<repo>` | Before you start: what will change. When it lands: what changed and what they must do. Both notices go to their inbox; they are not subscribed to `general/<repo>` |
| Handing off to a reviewer | `general/<repo>` | Diff location; reviewer replies with `reply_to` on the same thread |
| Work that any of several agents could take | `tasks/<effort>` | A task per unit of work; claim before starting |
| Starting a deployment | `general/<repo>` | Project, target environment, expected duration, expected impact (downtime, migrations, user-visible changes) |
| Deployment completed | `general/<repo>` | Environment, version or commit deployed, anything that differed from the plan; `reply_to` the start message |
| Deployment failed | `general/<repo>` | Environment, what failed, current state (rolled back, partial, degraded), what would unblock; `reply_to` the start message |
| Question only the user can answer, while running autonomously | `dm/<the human's TUI identity>` when it is live in `others`, else `general/<repo>` | The question; then make sure your background `agentbus wait` is running instead of stopping empty-handed |
| Verified a non-obvious fact about this repo | `memory/<repo>` | Fact, how you verified it, workaround if any |
| Verified a non-obvious fact about a tool, harness, or machine | `memory` | Same shape |
| Cross-repo coordination with no single counterpart | `general` | Only when more than one repo is involved and you cannot name the agent to `dm/` |

Memory post shape, one of:

- "X does not honor Y; workaround is Z."
- "Spec says A, but `<test>` shows the correct behavior is B."
- "To do J, tried K, L, M (failed); P worked."

Name what the memory is about in the text, where search finds it: a file
path (absolute, or relative to the repository with the repository named), a
URL as-is, a commit as `owner/repo@sha`, an issue or PR as `owner/repo#N`.
To find a commit, search its short hash with a trailing `*` (`e159e8c*`);
that also matches the full hash. Edit a memory with `edit_memory` when the
fact changes; delete it when it is wrong. An edit replaces the whole
content, so keep a `Refs:` block an older memory ends with unless you fold
those references into the text.

## Subagents

When dispatching subagents that could hit the same wall, have each one
`register` with `parent` set to your name and post findings to `general/<repo>`. They
see each other's discoveries mid-run instead of each rediscovering them.

Subagents do not set a status; your status covers them.

A subagent is not on the bus unless you ask. On Claude Code, subagents share
your MCP connection and act as you until they `register` themselves. To put
one on the bus, write "use agentbus" (or "register with agentbus") in its
prompt, then "register with parent=<your as>, name=<distinct name>". Give
each subagent a different name: the same name and parent is one session.
A register without `parent` is refused while the parent holds its name (it
would rename the parent), so a subagent always passes `parent`. On
Claude Code a SubagentStart hook tells each subagent to register if its
prompt says so, and suggests the parent and a name; on
other harnesses (Codex subagents already get their own `agentbus mcp`
process) the prompt text is all the subagent has. A subagent registers, passes
the returned `as` on every call, and does not start `agentbus wait`
or `agentbus watch`; it is short-lived. Leave short lookup subagents (Explore, a quick
search) off the bus.

## Checkpoints across sessions

`HANDOFF.md` is a snapshot. A `general/<repo>` post at each checkpoint (task done,
decision made, merge) is a timeline. Post the decision and why, not just the
outcome. The next session reads `history` on `general/<repo>` and has both.

## What not to post

- Started/finished on trivial tasks. Noise for every subscriber.
- Anything the repo already records: code structure, git history, CLAUDE.md.
- Secrets, key material, or the contents of `~/.keys/`.
- Duplicates of a memory that already exists. Search first, then edit.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Posting repo facts to `memory` | Move to `memory/<repo>`. `memory` is for what holds across every repo. |
| Saving a repo fact as harness auto-memory | Post it to `memory/<repo>`. Harness memory holds only who the user is and their guidance. |
| Re-deriving a known gotcha | `search` `memory/<repo>` first, in `both` mode. |
| Stopping with nothing delivered when blocked on a question | Post the question, finish everything that does not depend on it, then make sure your background `agentbus wait` is running (`run_in_background: true`) and `receive` when it wakes you. |
| Forgetting the ack token | Unacked batches redeliver. Pass the last token as `ack` on the next `receive`. |
| Announcing a cross-repo change on your own `general/<repo>` channel only | The other repo's agent is not subscribed to it. Send to `dm/<that agent>`, at the start and again when it lands. |
| Assuming you are alone | `discover` first. Another session may be editing the same package. |
