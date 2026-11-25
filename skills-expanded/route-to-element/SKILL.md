---
name: route-to-element
description: "Both natures. Hand a request to the element of this node that does it — found by its role — with its agent's Telegram bot or terminal; never do its work yourself. Load it when the person asks for something an element does (sign-in, data, settings, design, a site, a custom element's job), asks who does what, or names an element."
---

# Route a request to its element

**Process: both** — you change nothing yourself and answer in two or three lines; the first line names the process of the request you pass on.

A hint, not a law: models of late 2026 work worse under rigid step-by-step instructions.

## Why

Every element has its own agent with its own instruction, skills and code. That agent knows its element; you know the node.
Doing an element's job from here means loading what its agent already has — the person pays twice and the element's code
changes without its agent knowing.

## How

1. `npm run find -- <the job in plain English words>` — the registry's candidates, at most five, each with its role and how to reach
   its agent (`npm run contacts -- <id>` — one element again). Never list the whole node: it grows.
2. Pick the element whose role covers the job — each candidate says why it matched (670-4): **does it now — skill X** (route the job
   there); **nearest by its AREA** (its card confirms → a route its own agent builds there; then `npm run role -- <id> --grows "<the
   job>"`); **matches only its description** (read its card — usually it does not do this job: nobody). Two fit — ask the person one
   question about how they differ, then record one role for each (`npm run role`).
3. Answer with the element and how to reach its agent, as `find` prints it:
   > «Это делает элемент **auth** — вход и роли для всех элементов. Его агент: Telegram t.me/<bot>, терминал <link>. Там его
   > среда разработки — напишите ему.»
4. The element has no bot — give its terminal and say a bot can be connected on its page «Messenger → H2A → Telegram».

## Not here

- Nobody in the node fits → skill `create-element` (the network first, then a new element).
- The person wants you to do it anyway — say once why the element's agent should do it, then pass it on and tell the person it went
  there. **A job** (the element's work, only data changes) → `npm run task -- <id> --work [--skill <one of its skills from npm run card>]
  "<the person's words>"`: its worker does it, not its builder, and its «done» wakes you with the report (`npm run state -- <id>`).
  **A change of its code** → `npm run task -- <id> "<the person's words>"` (its builder). `--dry` shows what would be sent.
