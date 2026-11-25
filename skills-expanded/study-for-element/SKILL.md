---
name: study-for-element
description: "Build process. The person wants to know how a finished product, site or SDK works, to build something like it — the element that will build it studies it in its own study pass; you only hand the request over. Load it when the person asks to study, take apart or reverse-engineer a site, an app or an SDK, asks «how is X made», or wants a product «like X»."
---

# A study goes to the element that builds the product

**Process: build** — the study is the element's work: you pass the request on and answer in two or three lines; the first line names
the process.

A hint, not a law: models of late 2026 work worse under rigid step-by-step instructions.

## Why

The owner of the node, 2026-10-25: «работать он будет как ядро, но разборы он должен хранить внутри каждого элемента так как если мы
запускаем Claude Code Agent из соответствующей папки все работаю он идёт внутри этой папки и чувствуют себя в ней как дома». REA is one
copy in the core; a study — REA's records, the agent's notes, the ledger of obligations — lives in `study/` of the element that builds
the product, and only that element's agent works with it: its study pass brings REA's skill, REA's MCP tools and the node's study browser
with its write guard. Nothing of that is in your session.

## How

1. **Which element builds the product?** The one the person named, or `npm run find -- <the product in plain English words>`. Nobody
   fits — skill `create-element` first: a study needs the element the product will be built in.
2. **The site's rules:** `npm run site-rules -- <url>`. `DISALLOWED` or `UNKNOWN` — say so in one line: that site is studied only from the
   person's screenshots, or a similar site whose rules allow it is studied instead. The element's agent reads the terms of use itself.
3. **Pass it on:** `npm run task -- <id> "Build process, study: Study <url> for my product quiz. <the person's words>"`. These first
   words stay English in every language: the node starts the element's study pass by them.
4. **Answer** in the person's language, with the price named: the study runs on their Claude subscription, many requests of the
   strongest model, and REA with the study browser holds up to about 1 GB of this computer's memory while it runs. Where to follow it:
   the element's page «Product design → Reverse engineering» (root — «Reverse engineering» in its own section): its terminal on the right
   and its studies below; or the element's Telegram bot, if it has one.

## Not here

- You never study a site yourself and never start the study browser: the records would land in the core, not in the element.
- A sign-in to a test account belongs to the element's agent in its pass (`npm run study -- login <site>`): the person confirms it in
  the node's login window; nobody asks for a password.
- The person only wants to know whether an element of the node already does something — that is `route-to-element`, not a study.
- The person wants to understand, compare or check a product, or how to integrate it, not to build an analogue — the field `research`,
  with `shape-the-need`.
