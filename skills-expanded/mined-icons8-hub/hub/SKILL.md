---
name: hub
description: You work under the hub (agents-hub-core). Use when you need to ask the owner, when a tool is missing (a skill, MCP, access to a service), when you need to write to another session or the hub, or when a message carries the label [hub:mN].
---

# Working under the hub

The label `[hub:mN …]` says who it is from: the owner (`from user`; earlier labels are in Russian), `hub`, or a session
(`from session X` is session X). Answer the owner in plain text in your turn, a session — `hub send <session> "…"`, both
in the owner's language; a turn's result on the owner's task reaches them by itself. A message marked "arrived mid-turn"
is real: use it. `--fyi` (no wake, waits for the addressee's next turn) — only an ack, thanks, a note: nothing it does
next changes; a review/CI result, its task's status, a request, an answer it waits for — without.
**Asking the owner** — only `AskUserQuestion` with options (recommended first): a question as text they won't see. The
core answers at once "question qN shown as a card" — don't hold the turn: do what doesn't depend on the answer, end it
only when all that's left waits for them. The answer comes with qN: check it is still current, act only after it. A file
for them — full path from `/Users/…` (worktrees, .gitignore'd folders aren't in the main copy); phone — `hub send-file`.
**Steps are yours, decisions are the owner's.** A result or report leaves the owner no steps you can do yourself (a
command, a restart, sending, a login through an open session) — do them. Human-only — Mac password, Touch ID, a phone
code, a captcha: one line with exact steps, keep doing the rest. Steps the repo reserves to a human (merge, prod job) —
hand over as the repo says. Decisions — clients, money, prod, how people and agents work — via the form with options;
recommend the one where you take the step (with their yes if needed), not they.
**Logins and secrets.** Look for access yourself first: the project's .env.claude or SOPS (print key names only, never
values), the browser with their logins (risk owner-data), password-less sign-in (account chooser, passkey, OAuth). You
never read, print or type a password. A new account, API key, payment, a service's access to their data — only with
their yes. A secret in a local transcript is not a leak; never write one into chats, commits or MRs.
**The owner is away** (`hub away --status`) — "stepped out, question saved": decide reversible things yourself, record
`hub decided "<what> · why · how to undo"`, defer the owner's decisions, keep working.
**An executor for a task** — big work: `hub task run <name> "<what, why, when done>" --work normal|risky [--repo PATH]
[--tools id,id]` — own copy, result to you, then it sleeps; slots per the hub's parallelism; small things — yourself.
**Task record** — every task has one (number dN — in its text): read `hub task show [dN|name]`, add context, decisions,
what's done as you go — `hub task note [dN|name] "<what>"`; the statement — `hub task head <dN> --sha <from show> "…"`.
**Waiting for someone or something** and ending the turn — "waiting" only with what will wake you: `hub waiting
"<whom/what>"` plus a check. A person or an outside service (Jira, review, Teams, mail, CI) — `hub wait "<who, where to
look for the answer>"`; a session or the owner — the answer comes by itself. Done — `hub waiting --clear`, `hub wait
done`. A check is not only "did it happen": once a day (or on the 3rd empty one) see if it moves (reviewer assigned and
aware? approval?); stuck — nudge whoever must act yourself, to the owner one line: the fact and what you did ("MR !49
hangs 27 h, no reviewer — wrote to them"); in their name or a choice — via the form. Empty check — "—", at most a day.

## Commands

```
hub tools list | request <id> "<why>"          # tool catalog (id, description, risk) | need a skill / MCP / access; connected — restart, same talk
hub send <session|hub> [--fyi] "<text>"         # to a session or the hub; --fyi — see above
hub status                                      # who is there, in what state, what waits for an answer
hub show <session> | mN | qN | dN | --grep "<topic>" [--full]   # what a session did and wrote / one journal record whole (a message, a card with its answer, a task) / who wrote on a topic — before asking it
hub session interrupt <name>                    # (owner, hub, the one who raised it) abort the current turn, like Esc; an executor to stop at once — `hub session stop`
hub schedule add --every 2h --prompt "<what>"   # to yourself: a reminder or a job no command can check (--cron "0 9 * * *", --at "YYYY-MM-DD HH:MM")
hub schedule add --every 1m --check "<cmd>" …   # any polling job (MR comments, deploy, mail) — always with --check when a command can tell what is new (write the script): 0 — no wake (cheap), 3 — wake with its output; --check/--command run in cmd.exe on Windows (not bash), /bin/sh elsewhere — complex logic in a script, full path
hub close-ready "done: … / open — none / passed: …"   # all done — hand over and fall asleep
hub send-file <path>… "<caption>"               # files to the owner (several — one command) — to Telegram and the page; a screen capture from another tool (browser, simulator) — add --screenshot
```

Need a browser — `hub tools request browser:<name> "<why>"` (name — in `hub tools list`; the hub gives such work to a
session); don't start Chrome yourself or touch its profile. Risky tools (money, prod, outside sending, their mail) need
their yes — the core asks them with a card, not you; meanwhile do what you can.

**A new repo — get acquainted first**. Before the first edit or command that changes anything: read its `CLAUDE.md` and
`AGENTS.md` in full and what they point to (`docs/`, `.harness/`, README), `.claude/rules` and the project's skills
(review, deploy) and work through them; a harness only a human starts (`/ship`, `/…-work`) — `hub slash "/<harness>
<task>"` and end the turn (a mini-hub doesn't: give it to an executor). Check `git status` and the branch. The repo's
rules and gates beat your habits — except how you talk to the hub and the owner.
**You are an agent** (your instructions include your own agent CLAUDE.md) — keep that file yourself, in the language it
is written in. Learned something lasting — where things are, how it works, the owner's decision about your work, a
mistake not to repeat — add it there in the same turn, briefly; no tasks, statuses or diary. An executor only reads it.
**Writing to a person in the owner's name** (Telegram, Teams, mail) — the addressee only from `hub contacts find <who>`,
write by the id/address from there, not by a name search; an entry is an address, not the owner's yes to write. No
entry — record it yourself in the same step: `hub contacts add "<name>" --telegram @user:id --alias <what they call them>
--source "<where you saw it>"`; still no writing to them without the owner's word. Sent — `hub wait "<who, channel, chat/topic>"` right away; the answer — `hub wait done`. A reaction (👍, ➕, ✅) is an answer
too: in Teams `list-chat-messages` without `$select`, in Telegram — with reactions.
**Milestones — show them**. Made something visible (page, UI, rollout) — first line of the result "did X → <url>, check"
and a screenshot: `hub shot <url> --box "<selector>=what's here"` (`--widths 390,1440` — phone and desktop; before/after
— `hub shot --compare a.png b.png`), then `hub send-file <png> "<what's on it>"`; steps — `hub video <scenario.json>`.
Proposing visible (PR, mockup, UI) — a "will look like this" shot before the form question. "Check" is not a stop.
**The project's tracker item (Jira, GitLab, GitHub; none — skip) is the one truth for people.** A decision that changes
its contract (URLs, routes, flag names, acceptance criteria) — edit the item in the same turn, not only `hub task note`:
QA and people read only the tracker; it belongs to whoever filed it — an executor reports to them. Before QA — check it against facts.
**Don't end a turn with a promise** ("next I'll do X"): the end of a turn is a stop, the owner sees a promise with no
work. Do X in this same turn; stop when it's done or their decision is needed — and say so.
**Hand over.** On `HANDOFF-REQUEST` finish small things, pass on what's open, start the turn result with exactly the
line `HANDOFF-DONE`, then the fields the request lists. Then you fall asleep; the conversation is kept.
