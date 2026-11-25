---
name: bridger
description: Coordinate with another Claude Code session over the bridge — discover peers, ask them, answer their questions — INSTEAD of guessing or asking the user. Trigger this the moment the task depends on something another repo's session knows: a dependency/library that changed and this code consumes it, an API or schema contract owned by a different session, a monorepo service another session is editing, a migration to a new version, or coordinating a planner/implementer split. Also trigger when an incoming bridge message (a terse line "#<seq> <from> <type>: <body>") appears in a watcher notification and must be answered.
---

# Talking to peer sessions over the bridger

The bridger is a file-based message bus between Claude Code sessions. Each
session is a named peer; messages are immutable JSON files in a per-pair
thread. The CLI is `bridger`: the session-start hook links it onto `$PATH`
(`~/.local/bin/bridger`). If the shell cannot find it there, call
`${CLAUDE_PLUGIN_ROOT}/bin/bridger` — every example below works either way.

## Message format

Delivered messages are one terse line each:
`#<seq> <from> <type>[ re#<ref>]: <body>` — e.g. `#3 my-library answer re#2: use authenticate()`.
`re#<ref>` marks a reply to that seq. Types by convention: `chat` (no reply
expected), `ask` (peer should reply), `answer` (reply, carries ref).
On disk each message is full JSON (`{seq, from, to, type, body, ts, ref?}`);
`poll --json` / `ask --json` emit that form when fields are needed.

## When a message arrives (watcher notification or `poll` output)

1. Read the type and body from the line.
2. `ask` → answer it **from your own live context** — that is the whole point
   of the bridger; the asking session cannot see this repo or conversation.
   Read your own files if needed, then:
   `bridger send <from> answer "<text>" --ref <seq>`
3. If you cannot answer without more information from the asker, send a
   counter-question instead: `bridger send <from> ask "<question>" --ref <seq>`.
   The asker treats a reply of type `ask` as "answer this first".
4. `chat` → surface it to the user; reply only if it requests something.
5. Never leave an `ask` unanswered silently — if you genuinely cannot answer,
   say so in an `answer` message.

## Wire style — how to write message bodies

Bodies are read by the peer AGENT, not by a person. Optimize for the agent
parsing it exactly, in the fewest tokens; a human skimming `bridger log` is
secondary. Rules:

- Telegraphic. Drop greetings, hedging, filler, framing ("I was wondering
  if you could..."). Start with the payload.
- NEVER drop precision. Exact identifiers always survive compression: full
  symbol names, `path/to/file.ts:42`, versions, error text quoted verbatim.
  A short vague message is worse than a long exact one.
- Structure over prose. `key: value` lines, `->` for renames/moves, `!` for
  breaking, `?` prefix for each thing you need answered.
- One message = one intent. Two unrelated questions are two asks, so each
  reply correlates cleanly by ref.
- Address only who it concerns: `send w1,w3` or `send @all`. A message to an
  uninvolved peer wastes that session's context.
- In an ask, state the answer shape you want: "reply: list of `old -> new`",
  "reply: yes|no + reason".
- Answers mirror the question's structure and add nothing else. If the
  answer is a value, send the value.

Example — same content, wire style:

    verbose (~60 tokens):
      "Hi! I noticed you recently made some changes to the auth module.
       Could you let me know which functions changed and how I should
       update my calls? Thanks!"

    wire (~25 tokens):
      "? auth module breaking changes since v1.x. reply: list old -> new
       + call-site notes"

    answer:
      "login() -> authenticate(cfg: Config); getUser() -> getCurrentUser(),
       returns UserProfile; refreshToken() removed (auto). callers: replace
       try/catch AuthError -> AuthException"

## Don't monologue at a peer that isn't listening

`send` succeeds whether or not anything is reading. When the target has no
watcher running, it prints a warning on stderr naming how many of your
messages are still unread. Treat that as a stop signal, not noise:

- **Do not send the next message.** Queueing five where one is unread changes
  nothing about when they are read, and buries the one that mattered.
- Check `bridger status` — `unread-by-them` is how much of what you've said
  has not landed. Growing means you are talking to yourself.
- If you are blocked on that peer, say so to your user and name the peer.
  They can bring that session back; you cannot.
- If you are not blocked, carry on with what does not depend on it and handle
  the reply when it comes.

An `ask` that times out is the same signal in blocking form. Don't re-ask.

## Asking a peer

`bridger ask <peer> "<question>" --timeout 120` blocks until the matching
reply — from that peer, with ref == your ask's seq — and prints it. Both
halves are required, so another peer answering with the same ref cannot
satisfy your ask. While waiting, unrelated consumed messages are echoed to
stderr — handle them after the ask resolves.

## Automate this — recognize the pattern, then act without being asked

The point of the bridge is to ask a peer instead of guessing. When any of
these appear mid-task, run `bridger peers` first (see who is registered and
what they are working on from their summaries), then `ask` the right one:

- **You're about to guess at something another session owns.** A function
  signature, an API response shape, a config key, why a value changed — and a
  registered peer authored it. Ask; don't infer from a stale file or a diff.
- **A dependency changed under you.** Build breaks or types don't line up
  after a version bump, and the library's repo has a peer. Ask it for the
  breaking changes and the migration, then apply them.
- **The user points at "the other session" / another repo.** "update our app
  to the new lib", "match the backend's new contract". Resolve the peer and ask.
- **Cross-service work in a monorepo.** Your change touches a boundary another
  session is editing. Coordinate before you both land conflicting edits.
- **You finished work a coordinating session is waiting on.** Notify it
  (`send <peer> chat "..."`) so it can proceed.

Decision rule: if the missing fact lives in another **session's live context**
(not in this repo, not derivable from the diff), that is a bridge `ask`, not a
guess and not a question for the user. If it lives in a **file or command
output here**, just read it — don't bridge for what you can look up.

Before asking, set your own summary once (`bridger summary "<one line>"`) so
the peer you're contacting can see who you are in its own `peers` list.

## Status is not reachability; a poll is not a subscription

Two failure modes that look like "the peer isn't there". Neither is.

**`queued` does not mean absent.** Peer status measures exactly one thing: is
that peer's watcher process running. It cannot distinguish a closed session
from a live session that never armed a watch — registration does not start
one. A `queued` peer is registered, addressable, and receiving. Never skip an
ask because of it; the only test of reachability is `ask` with a `--timeout`.

**The peer record is not a liveness signal either.** Read peers through
`bridger peers`, never by opening `~/.claude/bridger/peers/<name>.json`. No
field in that file tracks contact: `created` and `last_registered` are both
registration stamps, refreshed when the session registers and at no other time,
so a peer that has been listening and delivering for hours still carries an
hours-old stamp. An agent that read the old name for that field (`last_seen`,
pre-0.16) reported a working peer as dead on the strength of it. Liveness lives
in `<name>.beat`, which `peers` already reads for you — and even that only
answers "is a watcher running", not "will this peer reply". Only `ask` answers
that.

**Arming the watch is not optional, and registering does not do it.**
`bridger register` makes this session addressable — it can be named, and it can
send. Receiving is a separate step: `wait --follow`, run as a persistent
background task. Its output is what re-invokes you when a message lands, and it
is the **only** thing that reaches this session once your turn ends. Skipping
it leaves you registered and deaf. Arm it immediately after registering.

Hooks cover the gaps around it, but none of them replaces it:

- mid-task, between tool calls, waiting messages are surfaced once on arrival;
- at the start of a turn, anything still unread is surfaced again;
- at the end of a turn, a registered session with no watcher is blocked once
  until it arms one.

All three need the session to be *doing* something. An idle session — the
usual state of a peer someone is about to ask — is reached by the watcher or
not at all. So also:

- If the watch may have died, re-run `bridger poll --peek` before you commit to
  a long deliverable that depends on a peer, and again before you deliver it.
- Reconsider the deliverable against what arrived. A message read after the
  work is written still changes the work — revise it, don't ship the version
  that predates the message.

**A name registered outside your own directory is not your mailbox.** `bridger
register <name>` registers the directory you are working in — the normal form.
`bridger register <name> <dir>` registers a different one, and who owns it is
decided by the same rule `bridger whoami` uses: a peer you registered is yours
when its directory IS your cwd or contains it, and when two of yours do, the
longer directory wins — the other is shadowed, as unreachable as if it never
covered you. Name a directory that does neither — a scratch path, a sibling
repo — and that peer becomes real and other sessions can send to it, but you do
not become it: `poll`, `send` and the watcher all resolve identity from your own
directory, so its mail piles up unread on disk and never reaches you, and the
statusline badge goes on showing the name you do answer to.
To hold that name, work in its directory.

## Housekeeping

- `bridger peers` — who is addressable: name, live status (`listening` /
  `queued` — both receive), directory, branch, self-set summary. The bridger is
  opt-in: only registered directories appear.
- `missing` is `queued` plus two facts: that peer's registered directory no
  longer exists, and no watcher process is running for the name.
  It is still addressable and still receives — it may be a
  session reading from the removed path — so keep treating it as a normal peer.
  Usually it is a leftover registration from a deleted worktree; `bridger reap`
  lists those with what they still hold, `bridger reap --force` drops them.
- `departed` is the one status that is NOT addressable, and it appears only in
  `bridger status`, never in `bridger peers` (that lists addresses). The name has
  no registration at all — it ran `bridger leave`, or `reap --force` dropped it —
  so `send` to it fails. Its thread is kept regardless: anything it sent still
  arrives on your next `poll`, anything you sent still waits in case the name is
  registered again, and `bridger log <name>` reads the history either way. A peer
  that proved a channel with `register → send → leave` leaves exactly this
  behind, and the messages are real — do not read the sender's absence as
  evidence nothing was sent.
- `bridger summary "<one line>"` — describe what this session is doing so
  other agents pick the right peer.
- `bridger status` — identity, peers, unread counts.
- `bridger poll --peek` — inspect unread without consuming.
- `bridger log <peer>` — full audit trail of a thread.
- Only one session per peer name should be open at a time; the cursor that
  tracks read position assumes a single consumer.
