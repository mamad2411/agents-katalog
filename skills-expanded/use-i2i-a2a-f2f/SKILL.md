---
name: use-i2i-a2a-f2f
description: >
  Where a task about elements talking, agents, deals, prices, ratings, Lagrix or exchanging elements belongs: i2i (inside the node),
  a2a (work for outside agents through Lagrix) or f2f (whole elements exchanged with other Fractera projects through Lagrix). Load it
  before touching the element menu (`lib/web4-items/item-tree.ts`: «Build» with its groups «Inside the node (i2i)» and «Exchange with
  Fractera (f2f)», the section «A2A»), the Deals page, the Lagrix rating card, a deal summary, a connector between elements, an F2F
  card, or anything that mentions payment between agents, a token, escrow, a wallet or reputation; and whenever a person asks «where
  does this go?». The rule that changes behaviour: inside the node aim at a connector over the API so that no model is needed; to the
  outside a Fractera element is an agent like any other — no advantage, no handicap; the element itself changing hands is f2f.
---

# use-i2i-a2a-f2f

> Informational, not binding. **Know a better way for the case in front of you — do it your way and say so.** You are trusted
> with the creative work on this project. Written 2026-10-11 (step 451) before any i2i or f2f code exists.

## Three protocols, one question each

| Protocol | What changes hands | Process | Where it lives in the node |
|---|---|---|---|
| **i2i** | a connector between two elements of THIS node: they meet as in A2A, then agree on an API call, so that next time no model is needed | build | «Build → Inside the node (i2i)»: `build/catalog`, `build/api`, `build/mcp` |
| **a2a** | a result of the element's work for an outside agent (a text, a picture, an answer), free or paid; paid → Lagrix settles it | working | section «A2A»: showcase `connectors/a2a`, **Deals** `connectors/deals`, Lagrix rating card on `connectors` |
| **f2f** | **the element itself** (its code, a copy, the right to run it) exchanged with another Fractera project, found through Lagrix with a technical card | build | «Build → Exchange with Fractera (f2f)»: `build/find`, `build/publish` |

**The questions that sort any task, in this order:**
1. Is the other side an element of **this node**? → **i2i**. The aim is a connector, not a conversation.
2. Is the thing changing hands **a result of work**? → **a2a**.
3. Is it **the element itself**? → **f2f**.

Old addresses `connectors/{catalog,api,mcp}`, `build/{api,mcp,catalog}` and `web3-store/*`, `build/{find,publish}` redirect to `build/i2i/*` and `build/f2f/*`; a2a lives in «Working process» (`workflow/a2a-work`, `workflow/a2a-orders`) — `movedPage()` in `item-tree.ts` (step 528).

## Rules that hold

- **i2i: models are the exception.** Two elements that talk over A2A more than once about the same thing should end with an agreed
  API call; the agent writes the connector, the next request goes without a model.
- **a2a: neutrality.** Lagrix sees a Fractera element exactly as an agent of any other framework, a site or an agent without a UI.
  Never build a Fractera-only shortcut into a2a; never expect one from Lagrix.
- **f2f goes through Lagrix** (owner 2026-10-11): the same discovery as a2a, plus the technical card of Lagrix document 20 — template,
  framework, `consumes`, `provides`, environment variable **names**, storage, licence, source. 🪦 «M2M never calls Lagrix»
  (2026-10-09) is cancelled.
- **Never in an F2F card or a deal:** keys, tokens, passwords, personal data, storage contents; a counterparty is an agent's address,
  never a person's name, e-mail or phone.
- **The node works without Lagrix.** i2i never needs it; only paid a2a deals and f2f exchanges go through it.
- **i2i works today; a2a is a plan** (owner 2026-11-07: «i2i we can use just now , but a2a it must discribed for feature»). A neighbour's
  job → `npm run task -- <id> --work [--skill <id>]` (670-2). An outside order → `new-steps/672-…` (not built): the element's door
  serves it, never a Claude session on the owner's subscription (skill `provider-rules`). The Lagrix search answers a2a and f2f in one
  contract (`npm run lagrix`, simulated; guard `check:lagrix-contract`) — called only when nobody in the node does it and the person
  decides to buy or build (a live search will cost $0.01 a list, doc 17 §17.8).
- **No invented numbers.** Until an element is connected to Lagrix the rating card shows «—» for every value
  (`components/element-docs/lagrix-rating.tsx`, words `_i18n/lagrix-rating.i18n.ts`).
- **Core change = question first.** The menu is shared by every element; moving or renaming a page changes all of them — name it to
  the person before the edit.

## Where to read more

- Instruction: `CLAUDE.md`, «Three protocols: i2i · a2a · f2f».
- Sections: `app/[lang]/(architectLayer)/architect/[item]/_sections/a2a/README.md` (the deal fields Lagrix will need) and
  `…/_sections/m2m/README.md` (where the f2f tabs went).
- Lagrix: `https://github.com/lagrix-dev/lagrix` — README «Two protocols at the start», escrow (doc 04), API (12), discovery and
  reputation (17), governance (18), F2F draft (20), the life of a deal (27).
- Element side: template `CLAUDE.md` «4. Process» and the element's skill `a2a-conversation` (i2i first).
