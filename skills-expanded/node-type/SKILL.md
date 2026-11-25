---
name: node-type
description: Build process. The node type — a single project (one owner, every element under the core's CONFIG) or an app factory (hosting of projects of different owners). Load it when the person asks what kind of node this is, speaks about hosting other people's sites, an app factory, projects for clients, one owner or one wallet, or when you create an element and need to know how it will look.
---

# The node type: single project or app factory

**Process: build** — the type is written into the node's registry. Change it only after the person's «yes» to three lines: what
becomes different, for which elements, how to switch back.

A hint, not a law: models of late 2026 work worse under rigid step-by-step instructions.

## The two types

- **project — «Single project» (the default).** One owner. Every element lives under the core's CONFIG: one header and footer, one
  wallet (the node's — an element cannot add its own), no Messenger section in the elements (their Telegram bot is in Build). A new
  custom element is born «like the whole project».
- **factory — «App factory».** The core hosts projects of different owners. A new custom element is born on its own settings: its
  own header, footer and policy pages. Wallets and Messenger stay with each element. The core and the built-in elements stay under
  the core's CONFIG.
- **Both:** the first header tab of every element under CONFIG is «All projects» — the home pages of all running elements of the
  node; on a factory it lists the projects of every owner.

## Commands

- `npm run node-type -- get` — the type, its meaning, and the born custom elements that differ from its default.
- `npm run node-type -- set project|factory` — change the type (only after the person's «yes»).
- `npm run node-type -- look <id> own|project` — switch one element's links with CONFIG and Design (the same door as the cards on its
  page). Existing elements never switch by themselves: after `set`, read the list and ask the person about each element.

## Never

- Change the type on your own initiative.
- Touch wallet keys: on a single project the person removes an element's own wallet on its Settings → Payments → Web3 page.

## Known limit of the factory

Since node step 554 every custom element born on a factory is an application with its own people: the same email in two applications is
two accounts, and a person signs in on the application's own site. The node's architect is admitted to every application.
