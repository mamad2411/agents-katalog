---
name: tabcrew
description: Run the AI chats in the user's own local Chrome (DeepSeek, ChatGPT, Gemini; pluggable) as a crew of agents orchestrated by Claude Code via Claude in Chrome — no copy-paste. Workflows - solo (one chat leads, Claude Code executes in the repo), debate (two chats discuss and converge, then hand the conclusion to Claude Code), fanout (several chats research subtopics in parallel, Claude Code synthesizes and acts). One named background agent per seat extracts, in any language, the part of each chat reply meant for Claude Code or for the other chat. Use when the user says "deepseek ile çalış", "chatgpt ile çalış", "gemini ile çalış", "chatgpt ile deepseek tartışsın", "iki chat açıp araştırsın", "tabcrew", "/tabcrew", "copy-paste between chat and Claude Code", or wants browser AI chats to work together with Claude Code.
---

# tabcrew

Browser AI chats become a crew of agents; Claude Code is the orchestrator.

```
                 ┌──── seat A: DeepSeek tab ────┐
Claude Code ◀──▶ │  (send / wait_read ops)      │ ◀── each seat's agent decides: to Claude Code?
(orchestrator)   ├──── seat B: ChatGPT tab  ────┤      to the other seat? ask the user? done?
                 └──── seat N: …           ─────┘
```

Talk to the user **in the language they write in**, in short, plain sentences. All skill files are in English; translate the wording when you speak to the user.

## Tree

```
tabcrew/
├── SKILL.md                     ← orchestrator: flow + map (you are here)
├── README.md · CONTRIBUTING.md  ← for humans (users · contributors)
├── pillars/
│   ├── 0-safety/SAFETY.md       hard rules (read first, always apply)
│   ├── 1-connection/            local-Chrome-only preflight
│   ├── 2-crew/CREW.md           workflow + seats + mode questions; open tabs; verify logins
│   ├── 3-routing/               one named background agent per seat (+ router-prompt.md)
│   ├── 4-turn/                  TURN.md (one turn, parallel turns) · QUESTIONS.md (who answers a chat's question)
│   ├── 5-workflows/             solo.md · debate.md · fanout.md · templates/
│   └── 6-memory/MEMORY.md       dated project wiki in .tabcrew/ (read at start, write each round)
├── providers/
│   ├── CONTRACT.md              adapter interface (status / send / wait_read / toggle)
│   ├── deepseek/                ready
│   ├── chatgpt/                 ready
│   └── gemini/                  ready
└── tools/                       fill_op.py (install ops, short calls) · fill_template.py (fill templates) · join_reply.py (decode + verify a reply) · save_server.py (receive generated images) · e2e.sh (smoke tests)
```

## Flow (read each file when you reach its step; paths are relative to this file's folder)

| Step | File | Output |
|---|---|---|
| 0 | `pillars/0-safety/SAFETY.md` | rules in mind |
| 1 | `pillars/1-connection/CONNECTION.md` | local browser selected |
| 2 | `pillars/2-crew/CREW.md` | `WORKFLOW`, `SEATS[]` (each: id, provider, tab, url, role), `MODE`, `MAX_ROUNDS`, `GOAL`; tabs open, logins verified |
| 3 | `pillars/6-memory/MEMORY.md` § When to read | earlier sessions and chat handoffs as context; session file created |
| 4 | `pillars/3-routing/ROUTING.md` | one named seat agent per seat (emoji + color + persona) |
| 5 | `pillars/5-workflows/<WORKFLOW>.md` | the workflow; it uses `pillars/4-turn/TURN.md` for every exchange and appends to memory each round |
| 6 | the workflow's § Finish | memory written, summary to the user |

Browser actions on a chat always go through its provider adapter (`providers/<provider>/*.js`, run as described in `providers/CONTRACT.md`). Pillars and workflows never hard-code selectors. Build every op as a short call with `python -I tools/fill_op.py … --call`; only when a call returns `not_installed`, run the installer (`python -I tools/fill_op.py --install providers/<id>`) once (it caches the ops in the site, see `providers/CONTRACT.md`) and turn every `wait_read` result into text with `python -I tools/join_reply.py …` (run both from this skill's folder). Never hand-escape or hand-decode.

Load all tools in ONE ToolSearch call at the start:

```
select:mcp__claude-in-chrome__list_connected_browsers,mcp__claude-in-chrome__select_browser,mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__tabs_close_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__javascript_tool,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__browser_batch,SendMessage
```

**Skill args** (optional; each one skips its question):

```
workflow=solo|debate|fanout
seats=deepseek,chatgpt            providers in seat order; "provider:<chat url>" attaches an existing chat
mode=auto|confirm   rounds=10 (0 or unlimited = until the task is done)   goal="..."   topics="subtopic 1|subtopic 2"   (fanout)
```

**Stop anytime** when the user asks to stop (in any language, e.g. "stop", "dur").
