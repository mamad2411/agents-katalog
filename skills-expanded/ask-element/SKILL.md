---
name: ask-element
description: "Work skill. The architect wants an element of this node to check or find out something and you to bring the answer («попроси template проверить …», «узнай у auth …»), or wants you to start or close an element's agent yourself. Also when «агент элемента … сообщил, что закончил (надзор …)» wakes you after such a task."
---

# Ask an element and bring its answer

**Process: working** — nothing changes in git: the element answers as a job, you pass the answer on.

A hint, not a law: models of late 2026 work worse under rigid step-by-step instructions.

**Why this way.** The architect asked you, so they are not asked again in Telegram to turn agents on and off (owner, 2026-10-20:
«агент ядра мог управлять включением агентов элементов и их выключением»). Your lead is the node's permission: a task to an element
you lead starts its agent at once, and its «done» wakes you at once — both without a Telegram question. Every running agent holds
about 300 MB of the person's memory, so you turn off what you turned on.

**The language.** An element answers in the language you speak with the person — never English by default (the owner 2026-11-08:
«на каком языке ты отвечаешь на том языке должны отвечать элементы»). The first `npm run task` or `npm run wake` of a conversation
carries `--lang <code>` of that language (`ru` when the person writes Russian); it is kept for the next ones and changed by the next
`--lang` when the person switches. The task itself stays English: the line about the language is added by the command. The same `--lang`
sets your own language line; without a task — `npm run lang -- <code>`.

1. Who: the id or address the architect named, or `npm run find -- <English words>`.
2. A build task sets one cycle of your lead by itself (step 695), so its «done» wakes you; `npm run supervise -- <id> main --max N` only
   for more cycles.
3. `npm run task -- <id> --work "Task from the core's main agent: <the check, in the architect's words>. It is a check, not a build:
   save the result with npm run reply-core -- \"<result>\" and finish as usual."` — its worker answers, not its builder (step 670-2).
   A check of its code or its build (a guard, a commit) — the same without `--work`. It prints «its worker … woke with the job» or
   «pasted into the live session» (the architect is working with it — do not turn it off later). Tell the architect in one line that
   the element is asked and that the answer comes from you.
   **The same job for several elements is ONE batch** (node step 681; the owner, 2026-11-07, about nine «no report» wakes: «фатальная
   глупая ситуация»): `npm run task -- <id>,<id>,… --work "…"` — no `supervise` per element, no polling of your own; one wake comes when
   the last worker is done, with every report in it — answer the person once, for all of them.
4. Its «done» wakes you (a new session) → `npm run state -- <id>`: «Report to you» is its answer, «Turned on by you» says whether you
   switched its builder on (a worker closes itself at its «done»). No report — say so; never guess for it.
5. `npm run person` → a Telegram bot: send the report with the channel's reply tool to that chat_id; no bot: write it here. A few
   lines, the architect's language, the element named, nothing added.
6. `npm run supervise -- <id> off` — your lead was for this one check; «Turned on by you: yes» → `npm run close -- <id>`; then
   `npm run done -- --close`.
