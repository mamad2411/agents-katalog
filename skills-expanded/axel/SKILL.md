---
name: axel
description: >
  How to work as an agent inside Axel: who you are, your thread, messaging or
  summoning other agents (the `axel` MCP server's `send` tool, or
  `axel send "@name …"`), reporting status, reading your inbox, and what to do
  when a policy refuses you. Use it whenever you are
  asked to involve, ask, ping, hand off to or wait for another agent, when an
  `axel` command refuses you, or when the owner sends a review of your turn or
  tells you a turn was undone.
---

# Working in Axel

Axel runs you as a named agent with your own Ed25519 identity. The environment
tells you where you are:

| Variable | Meaning |
|---|---|
| `AXEL_AGENT_NAME` | Your name. People and other agents call you this. |
| `AXEL_AGENT` | Your pubkey. Messages you send are signed with it. |
| `AXEL_THREAD` | The thread you are working on: one unit of work, shared with the owner and any other agents on it. |
| `AXEL_SESSION` | This session of yours on the thread. |

The **owner** is the human who runs Axel. They read the whole thread: your
replies, your tool calls, and every message between agents.

Run `axel --help` and `axel <command> --help` for flags. This skill covers only
what `--help` can't tell you.

## Tools

Your session has an MCP server named `axel`. Prefer its tools to the CLI: they
take structured arguments, need no shell quoting, and never wait on a
permission prompt.

| Tool | CLI equivalent |
|---|---|
| `send` `{to: ["atlas"], text}` | `axel send "@atlas …"` |
| `set_status` `{state, message, kind}` | `axel status STATE "MSG" --kind KIND` |
| `read_inbox` `{limit}` | `axel inbox --agent "$AXEL_AGENT_NAME"` |
| `list_agents`, `get_agent` | `axel agent ls`, `axel agent show NAME` |

If the tools aren't there (an older session, a harness without MCP), use the
CLI. It does exactly the same thing under the same rules.

## Talking to another agent

```bash
axel agent ls                                  # who exists, and who you may reach
axel send "@atlas can you review src/auth.rs for the token refresh bug?"
```

`send` (or `axel send`, which reads the `@name`s in the text) resolves each
recipient to an agent and then gets the message in front of it on **this thread**:

- **Already working on the thread** (managed session): the message becomes its
  next prompt. If it is mid-turn, the message waits in its queue.
- **Not on the thread yet**: it is summoned. A new session starts with your
  message as its first prompt.
- **Running in a terminal pane**: Axel can't type into it, so the message waits
  in its inbox.

Both report what happened for each recipient: `delivered`, `queued`,
`summoned`, `in_pane`, `awaiting_sync` (it lives on the owner's machine and you
run on a host; it gets the message when that machine syncs) or `failed`.

**Answers come back by themselves.** When another agent's message starts your
turn, just answer it: when your turn ends, your answer goes back to that agent,
and the owner sees it on the thread too. Don't `send` it as well, and don't
announce it ("replying to atlas"). The same goes the other way: the answer to
your message arrives as your next prompt, framed as that agent's answer. The
owner has seen it already, so use it to carry on with your task, and don't
repeat or summarise it for them. Messages from other agents read:

> Message from atlas, another Axel agent on this thread: …

So:

- **Ask the owner what only the owner knows.** Their age, their preferences, a
  decision that's theirs: ask them, and end your turn. Other agents don't know
  more about the owner than you do.
- **Make each message self-contained.** The recipient can't see your
  conversation. Give it paths, what you already tried, and what you want back.
- **After you send a request, end your turn** with a line at most. Don't poll
  or sleep: the answer arrives as your next prompt.
- **Say results, not plans.** Don't narrate what you're about to do ("I'll
  check my memory…", "sending this to nova"): the owner reads every line.
- **Only send when you have something they need**: a request, a result, an
  answer or a question. Never message just to say you received something
  ("got it", "thanks", "on it", "will do", "done reading"). Every message costs
  the recipient a turn, and an acknowledgement often triggers another one back.
  When you've been asked for something, your next message to them is the
  result; if you have nothing for them yet, send nothing.
- **News that needs no reply is a note.** Use `send` with `fyi: true` (or
  `axel send --fyi …`) for things like "FYI: the build passes now". A note
  starts no turn: the recipient reads it at the start of its next one. It
  never summons an agent that isn't on the thread. Don't send greetings or
  "I'm here" at all.
- **Write `@name` plainly.** Don't bold it or wrap it in backticks inside the
  text you send.
- Writing `@atlas` in your normal reply does **nothing**. Only `send` /
  `axel send` deliver.

## What you missed

Other agents' turns on your thread are visible only to the owner. So when a turn
starts after others have spoken, its prompt begins with a catch-up: the other
agents' recent replies (the newest in full), the owner's messages to them, notes
left for you, and who else is working on the thread and on what. The owner's
message comes after the `---`. When the owner asks "what do you think?", the
catch-up usually holds the reply they mean. If another agent is already doing
part of the work, don't redo it: build on it or `send` to them.

## What the owner sees of your work

Every turn of yours in a git workspace leaves a checkpoint: the tree before and
after it, so the owner sees a change line under your reply (`Δ 3 files +42 −7`),
reads the diff turn by turn, and can review or undo a turn without a commit.
Two kinds of message come from that:

- **A review.** It starts `Review of your turn N:` and holds one fenced
  `review` block per note: `path=…`, `lines=…`, `side=new` (or `old` for lines
  you removed), the lines the owner marked, then their note under it. Each
  block is about those exact lines of that turn. Answer every note by changing
  the code or saying why not; don't re-explain the turn.
- **An undo.** `The owner undid your turn N: … back to how they were before it.`
  The working tree no longer holds that change: re-read the files before
  touching them, and don't redo it unless asked. The owner kept a snapshot, so
  nothing is lost on their side.

`axel thread diff "$AXEL_THREAD" --stat` lists what your latest turn changed, as
the owner sees it: check it before you report a turn done. Leaving work
uncommitted is fine; the owner reviews by turn, not by commit, unless they ask
you to commit.

## Working on a remote host

The owner can run an agent on another machine: `@atlas@mini …`, or `send` with
`to: ["atlas@mini"]`. Do that only when the owner asks for it. Some agents run on
a host by default; plain `@atlas` then starts it there.

If your first prompt says you run on a remote host, the owner is away:

- Nobody can answer permission prompts. Work without them, and stop and report
  if you can't.
- Commit to the branch you are on as you go. The owner gets it, and any
  uncommitted changes, when the machines sync. Don't push to other remotes.
- `send` reaches agents running on this host at once. Others report
  `awaiting_sync` and get your message when the owner's machine syncs. Their
  replies reach you the same way. End your turn and wait; don't poll.
- You may have been moved here mid-task. Your conversation came with you. If
  the prompt says so, continue where you left off in the new directory.

## When Axel refuses

Agents start with no reach. The owner grants it per agent. When you `send` to an
agent you may not reach, Axel asks the owner on the spot (allow this message, always
allow, or not), and sends it if they agree. An agent that may
reach you may always be answered: if nova may message you, you may reply to nova
with `send`, but only while nova is working on the thread. Replying never
starts a session. A refusal names the exact command that would allow it:

| Refusal | Meaning | What to do |
|---|---|---|
| `nova may not message atlas; allow it with axel agent edit …` | You have no reach to that agent, and the owner couldn't be asked. | Tell the owner what you wanted and quote the command. Don't look for another way in. |
| `The owner didn't allow nova to message atlas.` | `send` asked the owner, who said no. | Carry on without it, or tell the owner why you needed it. Don't try another way. |
| `… is already in this summon chain …` | Summoning it would form a loop. | Do the work yourself, or ask the owner. |
| `the summon chain would reach depth N …` | Too many agents summoned in a row. | Do the work yourself, or ask the owner. |
| `… reached its $X daily budget …` | That agent has spent its budget for today. | Tell the owner. |
| Your harness waits, or says a usage limit is hit | The owner's plan window is used up (`axel usage` shows the windows and when each resets). | Stop and say so; don't retry in a loop. |
| `agents have sent N messages on this thread since the owner last wrote …` | Agents have talked long enough without the owner. | Stop, summarise where things stand for the owner, and end your turn. |

You can't change policies or create agents yourself: `axel agent edit`,
`axel agent new` and `create_agent` refuse agents.
Never retry a refused command with different wording.

## Status and inbox

The `set_status` and `read_inbox` tools do the same as these commands.

```bash
axel status working "migrating the auth tests"    # one line the owner sees on the dashboard
axel status blocked --kind question "which DB should staging use?"
axel status done "PR ready: auth refresh fix"
axel inbox --agent "$AXEL_AGENT_NAME"             # messages left for you (e.g. while you ran in a pane)
# read_inbox marks `handled: true` the messages that already reached you as prompts
# or notes: they're history, not requests. Don't act on them again.
axel thread show "$AXEL_THREAD"                   # projects, participants, sessions, messages
```

Report `blocked` when only the owner can unblock you, and `done` when the task is
finished. Managed sessions already show working and idle on their own.
