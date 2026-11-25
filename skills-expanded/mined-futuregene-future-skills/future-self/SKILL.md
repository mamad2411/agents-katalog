---
version: 1.14.0
name: future-self
description: Inspect and adjust this FutureOS installation — global agent settings, the desktop app's own settings and workspaces, sessions, skills, tools and models, the account and credit balance, the machines paired to this one's remote desktop, a backup or restore of the local record, the user's recorded conversations, and the source that implements the agent — to answer "how am I configured", "why do I behave this way", "what do I know about you", "what did we do before", "how is my account", "which device is controlling this machine" or "show me my balance", and to personalise or proactively help. Use for self-inspection, cross-session recall of past conversations, slicing one session's own records (including thinking and tool inputs/outputs), reading or changing global agent or desktop-app settings, adding a workspace from the terminal, pruning idle conversations, pairing or unpairing a remote device, backing up or restoring the installation, reloading the model registry after a hand-edited models.json, changing a provider's key, address or models, probing which thinking levels a model accepts (重载/刷新模型), pinning or unpinning a conversation or workspace, understanding the code behind a behaviour, or account profile and credit balance. Never for reading credentials, and not for ordinary task work on the user's project.
allowed-tools: Bash(future:*)
category: tools
---

# Knowing yourself and the user

Everything this installation knows is local and readable through the `future`
CLI: how the agent is configured, which skills and tools are installed, every
conversation that was recorded, what it cost — and, where a source checkout is
present, the code that produces all of it. The account and credit balance are the
one part that comes from the Future platform instead of this disk. This skill is
the entry point for using all of it, so the agent can adapt instead of asking for
something that is already available, and explain a behaviour instead of guessing
at it.

Read state before acting; ask before changing anything that outlives this turn.

## 1. Ground rules

- **Never read or print `~/.future/agent/auth.json`.** It holds API keys. The
  CLI reads it for you, `future config get` deliberately returns no credential
  material, and `future auth credential` exists for shell scripts, not for
  browsing — do not run it to "see what is configured".
- **Never report a negative you cannot prove.** History search covers a bounded
  window of sessions and is literal matching. "We never discussed that" is only
  defensible when the response says `truncated: false` and `hasMore: false`.
- **Changes to settings are the user's decision.** They persist past this
  session and change how every future session behaves. Propose the change and
  the old value; make it only when the user agrees (or when they asked for it).
  Report what you changed and when it takes effect.
- **Reading code is for understanding, not for patching.** Never edit the
  FutureOS source to change your own behaviour: that forks the installation from
  the release the user actually has, and the change disappears at the next
  update. Behaviour that has a knob goes through `future config set` / `future
  desktop settings set` / `future session set` / skills; anything else is a bug
  to report, not to fix behind the user's back.
- **Reading history is reading the user's own record, and it is appropriate —
  but stay purposeful.** Search for what answers the question; do not page
  through conversations to satisfy curiosity.
- **Quote, do not paraphrase, when the distinction matters.** A stored
  preference is a quotation from the user; a pattern you noticed is your
  inference. Keep them apart when you report back.

## 2. Where to look

This skill is an index: each area below is a small, self-contained reference.
Open the one that matches the question and answer from it — they carry the
command options, the caveats and the limits that make an answer correct, and a
detail recalled from this page alone is usually a detail missed.

| The question | Read |
|---|---|
| What is configured, installed, running, or recorded? What is this build? Which session am I? | `references/inspecting.md` |
| What happened in a conversation? Did we ever discuss X? Slice one session's records. | `references/recall.md` |
| The account, the credit balance, whether a login exists. | `references/account.md` |
| Change a setting, a session, a skill; stop a run; answer an approval; delete old conversations; refresh the model registry. | `references/settings.md` |
| The desktop app's own preferences, its workspaces, and what is pinned. | `references/desktop-app.md` |
| The devices that drive this machine, the desktops it drives, hosting headless, a self-hosted relay. | `references/remote.md` |
| Back up, verify or restore the whole local record. | `references/data.md` |
| Why does it behave this way? Read the code that implements it. | `references/source.md` |
| The bound behind a claim, or what this skill cannot know. | `references/limits.md` |

## 3. The commands you will reach for most

| Command | What it answers |
|---|---|
| `future config get [<key>] [--json]` | The effective global settings, defaults included |
| `future desktop settings [<key>] [--json]` | The desktop app's own settings, defaults included |
| `future workspace list --json` | The desktop app's workspaces (see `references/desktop-app.md`) |
| `future workspace list --pinned` | The app's **pinned** workspaces, in the order the sidebar draws them |
| `future workspace pin <path\|id\|name>` / `unpin` | Move a workspace in or out of the pinned section |
| `future version --json` | Which build this is: version, **commit**, target, dirty |
| `future session list --json` | Every session, newest first, with its `cwd`, model and title |
| `future session status <id> [--json]` | One session's **live state**: permission, context, runs |
| `future session status <id> --system-prompt` | The whole prompt that session's next run would send |
| `future session transcript --session <id> --counts --json` | What kinds of records a session holds |
| `future session reset <id> <selectors> [--yes]` | Delete part of one session's **own** history (dry run unless `--yes`; backed up) |
| `future session history search --all --query <text> --json` | Whether a topic appears anywhere |
| `future session prune --older-than <age> [--yes]` | Delete conversations idle longer than `<age>` (dry run unless `--yes`; no undo) |
| `future session pinned` / `pin <id>` / `unpin <id>` | Which conversations are pinned — and the one thing that changes it |
| `future remote status --json` | Whether this machine is serving its remote desktop, and who is in control |
| `future account balance` | Remaining credits (a remote call — see `references/account.md`) |
| `future doctor` | One pass over login, agent, sandbox, providers, sessions, skills |
| `future mcp list` | MCP servers this CLI can call (using them is the `future-mcp` skill) |

**`session info` and `session status` answer different questions and are easy to
confuse.** `info` reads what was recorded; `status` reads what the agent is doing
and how the session is configured *right now*. A session can run at `workspace`
permission while `future config get defaultPermissionLevel` says `all`, and be
using 40% of its context window while `info` reports 40M lifetime tokens — only
`status` is correct in either case.

**A pin is the desktop app's flag, not the Agent's.** `future session pinned`,
`future session pin` and `future session unpin` read and write
`~/.future/app/app.db`, which is why they work with no Agent running — while
`future session list` is a gRPC call that carries no pin at all. The two lists
differ for that reason: the app's holds what it imported, the Agent's holds
sessions it has never opened. Both rules, and what archiving does to a pin, are
in `references/desktop-app.md`.

**Most session and model commands need a running Agent.** `future session
list/info/status/transcript/history/forks/wait/approvals` and `future models` ask
the Agent over local IPC and fail with `unable to connect to Future Agent` when
none is reachable, rather than returning an empty result. The reads that work with
nothing running are `future config get`, `future desktop settings`, `future
workspace`, `future session pinned`, `future version`, `future auth status`, `future
skills list` and `future doctor` — plus the `future remote` commands that only
read its pairing books (`references/remote.md`).

## 4. Building a picture of the user

The point of all of the above is a personal agent that needs less re-explaining.

- **Start from evidence, not from a template.** Settings the user changed,
  skills they installed, the model they keep choosing, and repeated phrasings in
  their prompts are observations. A profile you assume is a guess.
- **Keep quotations and inferences separate.** "You asked for responses in
  Chinese" (observed) is different from "you prefer terse answers" (inferred).
  Say which one you are acting on when it changes what you do.
- **Preferences are not stored anywhere by default.** If the user wants the
  agent to remember something, propose writing it down explicitly — a standing
  rule for one conversation goes in that session's system prompt
  (`future session set <id> --append-system-prompt "…"`, see
  `references/settings.md`), something that should hold everywhere goes in a
  `future config` value when the setting exists, and otherwise a notes file in
  their workspace — and say where you put it. Do not silently accumulate a
  private profile.
- **Prefer asking to inferring when the cost of being wrong is real.** Changing
  a default model, permission level or sandbox tier on an inferred preference
  is not acceptable; on an explicit request it is.
- **Use it to reduce friction, not to fill silence.** Reading the previous
  session before asking "what were we working on?" is the win. Interrupting with
  advice nobody asked for is not.

## 5. Limits worth having in your head

The full list is `references/limits.md`; these are the ones that turn into a
false statement if you forget them.

- **Literal, not semantic.** No embeddings, synonyms or stemming — two words are
  one substring.
- **Bounded.** Every scan, match list and read has a cap; a truncated result is
  a partial answer and must be reported as one.
- **Local state is local.** Sessions under another `FUTURE_HOME`, or on another
  device, are invisible — and there is no source checkout to read unless one is
  actually here. The account commands are the one remote exception.
- **`future desktop settings` and `future workspace` ignore `FUTURE_HOME`**:
  they target the real `~/.future/app/app.db`, exactly as the desktop app does.
- **Source is not behaviour.** A file in the checkout is not proof of what the
  running binary does; `future version --json` says which binary you are running.
- **No credentials, ever.** Not in reads, not in summaries, not in files you
  write for the user.

## Resources

- `references/inspecting.md` — the whole read surface, the `info`/`status` and
  "my tools" confusions, session identity, and the build-identity checks.
- `references/recall.md` — history search/read semantics, and slicing one
  session's records with `transcript`.
- `references/account.md` — the platform account and the credit balance.
- `references/settings.md` — changing global settings, sessions and skills;
  stopping runs; approvals; deleting old conversations; refreshing the model
  registry.
- `references/desktop-app.md` — the desktop app's own store: its settings and its
  workspaces (`future workspace`).
- `references/remote.md` — this machine as a host (`future remote devices`, `future
  headless`) and as a client (`future remote peers`), plus a self-hosted relay.
- `references/data.md` — `future data`: a backup, an interrupted restore and its
  fence, and what is not recoverable without one.
- `references/source.md` — reading the code that implements this agent, and
  attributing a behaviour to the right build.
- `references/limits.md` — every bound, and which of them make a claim unsafe.
