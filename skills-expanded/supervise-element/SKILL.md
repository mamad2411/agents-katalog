---
name: supervise-element
description: "Build process. Lead an element's development for the architect when they chose you (supervise main) — its «done» wakes you; read its state, answer its confirming lines or give the next task, report, stop at the end. Load it when you are woken with «Узел: агент элемента … сообщил, что закончил (надзор …)» or the person asks you to lead or stop leading an element."
---

# Lead an element for the architect

**Process: build** — you change no code yourself, yet you lead an element's development: its code changes by the answers and tasks you pass to its agent.

A hint, not a law: models of late 2026 work worse under rigid step-by-step instructions.

## Why it exists

The architect said (2026-10-19) that the node, «выступая в качестве старшего руководителя разработки», may follow an element's
work and pass it new tasks «без личного участия». You do it only for elements whose record says so; the architect can take it
back at any time (`npm run supervise -- <id> architect`).

**The language.** An element answers in the language you speak with the person — never English by default (the owner 2026-11-08:
«на каком языке ты отвечаешь на том языке должны отвечать элементы»). The first `npm run task` or `npm run wake` of a conversation
carries `--lang <code>` of that language (`ru` when the person writes Russian); it is kept for the next ones and changed by the next
`--lang` when the person switches. The task itself stays English: the line about the language is added by the command.

**The node's messages carry a head** — `⟦node · <kind> · <element> · <HH:MM>⟧` (step 698): `supervision-done`, `job-done`,
`first-session-done`, `limit-resume`, `core-back`, `held-during-build`, `build-failed`. Act by the kind; what each asks —
`lib/agent-kit/NODE-LINES.md`.

## One cycle

1. `npm run state -- <id>` — its role, who leads, intake, last commits and `current-step.md`.
2. Decide by the task in its intake (the person's words) and its current step:
   - it waits for a «yes» on three confirming lines or a plan → it matches the task: `npm run task -- <id> "Да, делай."`; it
     does not: one correction in plain words;
   - it asks a question — a product quiz question too → answer it from the architect's words in its task, quoting them: for this
     work you are its person (its instruction says so), and the quiz item it records carries those words. Only what the task
     does not say goes to the architect — tell the element it waits for them (✗ 2026-10-20: the main agent forwarded a quiz
     question the task answered, «only the person confirms», and the element stopped);
   - a neighbour's request in its intake that its role covers → «Да, делай»; one its role does not cover → ask the architect;
   - a substep or step is closed with evidence → «Дальше по плану» or the next part of the task;
   - the task is done → report to the architect and `npm run supervise -- <id> off`.
3. Report one or two lines to the architect: what the element did, what you answered. `npm run person` tells where — Telegram
   when a bot is connected to you, otherwise this terminal.

## When the hand cannot finish (686)

`npm run where` names it: a turn cut off or stopped by a limit. A stop by the limit already has its resume — the clock wakes you at the
reset (686-5); then wake it «continue from your record». The element runs on its own person's subscription (689) and that one ran out
before the work ended — finish through the same hand on lent fuel: `npm run lend -- <id> --cost <% of the node's window you expect>
--reason "<the work>"`; it refuses when the forecast leaves you less than 15 % (every running lending counted). Then `npm run close`
and `npm run task`; the end of that session gives the fuel back by itself, `npm run lend` shows the debt. Only the work YOU handed
out — the architect's own work, led by you; the element's person's Telegram stays off during the loan, and their own wishes never run
on the owner's subscription, nor one person's two subscriptions around the limits — skill `provider-rules`.

## Never

- leave an element's permission question to the person: since 2026-11-09 (the owner: «агент ядра принимает решение о том что
  делать», core step 704) it comes to you as its own line `⟦node · permission⟧` and you decide it — skill `element-permission`;
- build, change or test the element's code yourself;
- go on after the last cycle: the node removes the record, you report and stop.
