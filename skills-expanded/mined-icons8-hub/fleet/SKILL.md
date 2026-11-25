---
name: fleet
description: Hub commands for the session fleet and the tool catalog — raise or close a session for a task, hand over a task, start or find a direction ("start a direction", "find my direction", "this is a direction"), decide a tool request, see the state. Use in the hub session whenever something has to be done with sessions, directions or tools.
---

# Fleet and tools

State — only from the core: `hub status` (or `hub status --json`). Don't infer it from indirect signs.

## Sessions

```
hub session new <name> [--cwd <project dir>] [--mode auto|default]   # bypassPermissions; no --cwd — its own folder
hub send <name> [--fyi] "<text>"   # a message, not a task; --fyi — changes none of its next steps (an ack, a note):
                                   # no wake; a review/CI result, its task's status, an answer it waits for — without it
hub session close <name>      # put to sleep: the session hands over (HANDOFF-DONE), then sleeps; talk and set stay
hub session wake|reload <name>  # wake with the same conversation | anew once free (MCP didn't connect)
hub session effort|model <name> high|opus  # struggling — higher level (low…max) or model; cwd <name> <dir> — move
hub session parallel <name> <N|default>   # by the owner's word: own number of executors of an agent/direction; 0 — none
hub session rename <name> <new>   # asleep only: talk, messages and schedule go with it, the old name stays an address
hub session icon <name> <emoji>|--clear   # own icon in the list; while set, `role --icon` doesn't override it
hub layout [move <name> <group>|none | ungroup <group> | reset]  # list groups; none — outside groups; reset — "Reset"
```

A sleeping session wakes by itself when written to (`hub send` without `--fyi`) and when you call `hub session new` with
its name: a wake with the same conversation, not a new session. A finished executor doesn't: messages go to whoever
raised it; you or the owner wake it (`hub session wake <name> "<what>"`). Who a message is from — the label `[hub:mN
…]`. `close` is refused with a reason while a turn runs, there's a question to the owner, an open task or a queue.
Handed over — `HANDOFF-DONE <name> …` comes to you: a line for the day's summary, don't ask the owner.

**Whom to give a task — by role.** Look at `hub status` in this order:
1. **Agent** (a line "agent … what it does") by profile — to it, even asleep: it's permanent, a new session doesn't
   replace it. Repos inside its folder (`<dir>/repos/*`) are its: the task to it, it raises executors there itself. No
   fitting one and the work recurs — propose an agent: `hub session new <name> --cwd <dir> --agent --about "<what it
   does>" --icon <emoji>` or `hub session role <name> agent --about "…"`. Firing (`role <name> worker`) — theirs.
2. **Direction** (`hub direction list`) by topic — to its session. The owner names a direction ("start a direction for
   payments", "this is a direction") — find it in the list, none — start it. Clear along the way that it's a direction
   (own backlog, a long topic) — start it yourself and tell the owner with a `hub decided` line.
3. Otherwise an **executor**: `hub task run <name> "<what, why, when done>" --repo <dir> --tools <id,id> --work
   normal|risky` — tools for the task right in it (a `grant` after start arrives only after its turn); work kind — per
   the hub's CLAUDE.md, the same for `task new` and `route … executor`. Own copy, result to you, then it sleeps (wake —
   `hub session wake`); no slot — it waits. Don't resend closed work: first `hub show`, `--grep "<topic>"`.

**Agent busy** — your task waits in its queue; to give it to its executor — `hub route <dN> executor --work <kind>
--name <gist>` (its profile and tools, without its conversation; the result goes where the agent's answer would).
Others' messages wait in its queue, you aren't told (yourself — `hub route <ref> executor | drop "<why>" | now`). An
addition to a task it or its executor already does — `hub send <agent> --about <dN or the owner's mN>`.

A session starts in the project folder and loads all the project brings: CLAUDE.md, skills, `.mcp.json`. Name — Latin,
short and about the task (`shop-api`, `growth-plan`). An owner's message without an address comes to you.

## Tasks

```
hub task new <session> --for <mN> "<context and when done, 1–3 lines>"   # mN — the owner's message from its label
hub task new <session> "<task>"                             # the hub's own task, the result comes to you
hub task new <session> --for-session <who asked> "<task>"   # a session asked for a new session: the answer goes to it
hub send <agent> --about <dN|mN> "<addition>"               # to a task already given: reaches whoever does it
hub task list | done <dN>                                   # task board | "Done" — only after checking
```

The core itself puts the owner's verbatim words and the contract into the task; don't add "answer me like this". The
executor answers **the owner** directly: its turn result lands under the owner's message. You get `[hub:mK …] REPLIED dN
…` from the core — read it, check the task is closed, and close it: `hub task done dN`; don't retell it to the owner. An
interim answer ("waiting for the agent") — no `done`: the continuation goes to the owner (or session) directly, in the
same thread, not to you — see `hub task list`. `STOPPED` — the turn broke off: read the session's feed, narrow the task
or give it to another session, don't do the work yourself. `TIMEOUT` — 90 min without a result: check the work is alive;
`TIMEOUT` saying it is free with no result, or an interim answer and silence: done → close; needed → nudge (`hub
send <s> --about dN`; asleep — `hub session wake <s> --about dN`) or reassign; not needed → close. Not to the owner.

## Directions

A big task the owner calls a direction ("direction sso", "start a direction …") — one long session with its own backlog.
Does it exist — `hub direction list`; new — `hub direction new <slug>` (+ `--repo <project repo>`, if any). The topic
already runs in a session (your executor, "make it a direction") — add `--session <its name>` (later — `hub direction
lead <slug> <session>`): without it the backlog waits for a session named `<slug>`. A new one you open in the repo (`hub
direction where <slug>`) named `<slug>`, grant it `directions` and give the task (`hub task new`) "direction <slug>". It
picks slices itself; to the owner — forks and slice results. Only the owner finishes it, by their word, not because the
tasks ran out: `hub direction archive <slug>`. "Show the board" — `hub direction board <slug>`; `backlog browser` — no.

**"I'm away" / "I'm back".** "I'm away [for N h]" — `hub away [--hours N]`, a one-line reply; "I'm back" — `hub back`:
the core builds the summary and sends reminders about their questions, not you.

## Browsers and schedule

A browser is the tool `browser:<name>` (`hub tools grant`); the core runs a local one itself, a remote one is someone's
CDP; with the owner's logins — risk `owner-data`. "Every morning at 9…" is not memory but `hub schedule add --session
<who> --cron "0 9 * * *" --prompt "…"` (`--every 2h`, `--at "…"`); a watcher "anything new?" — `--check "<command>"` (0
— don't wake, 3 — wake with its output). Tidying up — `hub schedule apply` (JSON of all your jobs); `[⏰ schedule id]`
saying session X is gone — `hub schedule retarget <id> <session>` or `rm <id>`.

## The hub's own code

Requests to change the hub (page, Telegram, core, modules, hub skills), updates, extensions — to agent `hub-dev`: `hub
task new hub-dev --for mN "<context>"`. It asks "for me" or "for everyone" and knows how to handle each; "[hub update]
…" too.

## Restarting the hub

New core or module code works only after a restart. The owner asks ("restart the hub") or a session that edits the hub
says it's needed — `hub restart "<why>"`: the core waits until sessions are free and without background work, but no
longer than `restart_wait_minutes` (20 min) — then without them, telling them "continue" (who holds it and how long —
`hub status`); you come back with the same conversation and get "Hub restarted" — tell the owner the result. `--now`
breaks turns and background work — only by their word; `--cancel` cancels. Only the page, Telegram, files (sessions
untouched) — `hub restart web telegram files`. No `launchctl`, `kill` or scripts.

## Plugins and modules from catalogs

Catalogs — `hub marketplace list|search [words]`; install or update to the catalog's version — `hub marketplace install
<entry>@<catalog>`, remove — `hub marketplace uninstall <key>`, add a catalog — `hub marketplace add <owner/repo>`: only
on their direct word (someone's code on their machine), `--for mN|qN`; first show what it does (page, process, skills).
Refused as "asks for more" — ask them by a form naming the plugin and those rights; `--accept` only `--for qN` of it.

A GitHub link not in a catalog — `hub market review <link>`: Hub Developer reads the code, the verdict — in "Settings" →
"Plugins"; install only ok or risky, on their yes after it: `hub market install <owner>/<repo> --reviewed --for mN|qN`.

## Tools

```
hub tools list
hub tools grant <session> <id>          # connect (to yourself too: <session> = hub)
hub tools grant <session> <id> --for mN # risky: the owner's mN to you or card qN names the tool
hub tools deny <session> <id> "<reason>"
hub tools revoke <session> <id>
hub tools discover                     # what the owner has in Claude Code and the catalog lacks
```

The owner's own tools (their skills, plugins, MCP in Claude Code) don't get into sessions: clean sessions learn on runs;
their root ~/.claude/CLAUDE.md sessions read themselves (Claude Code loads it); don't pass env and settings. Asked "look
at my superpowers and projects" — `hub tools discover`, show what the hub lacks and add what they pick (projects — to
`projects` with "what about"; tools: `hub tools import set|skill <name>`, `hub tools import mcp <name> --about "<what it
does>" --risk <…>`, risk — by access). Don't print config values. A session asks for an outside skill — putting it in
`~/.claude/skills/<name>` isn't enough (hub sessions run without personal settings): then `hub tools import skill <name>
--risk <…>` and `hub tools grant <session> <name>@my-skills`. "Check my CLAUDE.md" — read it, show briefly: outdated
(commands, paths that don't exist), over-control ("ask before every step"), what belongs in a project's CLAUDE.md; edit
on their choice.

The owner's rule: you connect yourself from the catalog. A tool with risk (`risk: money`, `prod`, `external`,
`owner-data`) needs the owner's yes, and it is asked **once**:
- Their own words to you, or the question or answer of any session's card they answered, name the tool (its id or
  plugin name; "the browser", a bare "yes" or a session's retelling do not) — `grant … --for mN|qN` (mN of `[hub:mN …]`).
- Otherwise don't ask in chat, just `grant`: the core asks them with a card. Its output says NOT yet connected, waiting
  for the owner's yes — pass that on, don't write that it's connected.
- Never call `approve` yourself or confirm for the owner — that's their word.

Connecting restarts the session once free, conversation kept; if it stopped for it, the core tells it to continue.

Pick a tool for a task by its catalog description. Read the whole catalog (`hub tools list`, it's short), don't grep:
what you need may be named otherwise (the hub once searched "mail|login" and missed the browser with logins). Need the
owner's logins (their mail, GitHub, dashboards) — a browser with risk `owner-data` (logged in); a clean one is useless.
