---
name: map-web-app
description: Reverse-engineer an unknown web app through a real browser until its data model and CRUD operations are fully mapped, then codify that into a reusable CLI plus a skill so the next session starts from a contract instead of re-exploring. Use when the user wants to automate, script, or build a CLI for a website that has no usable API - "automate X for me", "build me a CLI for X", "can you script X", "I want to do CRUD on X programmatically", "figure out how X works so we can automate it". Also use before any long browser-automation task on an unfamiliar site, so the mapping is captured instead of thrown away.
compatibility: Needs a browser automation tool. Prefers `playwriter` (drives the user's real logged-in Chrome). Falls back to agent-browser or playwright-cli. Produces a bash or Node CLI plus a skill directory.
---

# map-web-app

Turn an unknown web app into a scriptable interface.

The output is **not** a one-off automation run. It is a CLI plus a written DOM contract, so the next session and the next agent start from a mapped system instead of re-deriving it by clicking around.

**The core discipline: explore exhaustively before writing anything.** Map every entity, every CRUD operation, and every field's widget type first. Scripts written mid-exploration encode wrong assumptions, and those assumptions fail silently.

## Phase 0: do not scrape if you do not have to

**Always spend the first five minutes here.** Scraping is the expensive path; take it only after ruling out the cheap ones, in this order:

1. **An official REST/GraphQL API.** Check `/api`, `/settings?developer`, the docs site, and the footer.
2. **Is it paywalled?** A documented API you cannot use is not an option. Verify the account can actually mint a key, do not just confirm the endpoint exists.
3. **A published CLI, SDK, or MCP server.** Search before building.
4. **A bulk export.** Even read-only export beats scraping reads.
5. **The app's own XHR calls.** Intercept the network while clicking. Sometimes an internal JSON API is usable with session cookies, which is far more stable than the DOM.

Only when all five fail do you scrape the DOM.

> Record the outcome of this check in the skill you write. "The API is Pro-only" is the single most useful sentence in the artifact, because it stops the next agent re-investigating for an hour.

## Phase 1: enumerate the data model

Before touching any control, answer on paper:

- **What are the entities?** (routines, workouts, invoices, contacts)
- **How do they nest?** (routine has exercises has sets)
- **What is the URL for each?** List, detail, create, edit. Note when the edit URL uses a *different* id from the detail URL.
- **What identifies a record?** Slug, uuid, or only its title.

Use `snapshot()` over screenshots. It is text, searchable, and gives ready-made locators. Screenshot only when spatial layout genuinely matters, such as a menu with no accessible name.

## Phase 2: map CRUD per entity

For each entity, find and record the exact path for **all five**, including the ones you do not need yet:

| Op | What to capture |
|---|---|
| List | URL, and the selector yielding ids and titles |
| Read | URL pattern, and which fields it actually renders |
| Create | Entry point, the form, the save control |
| Update | How to reach edit mode; often a hidden menu |
| Delete | The control, plus any confirmation dialog |

**Read is not the inverse of write.** A detail page routinely omits fields the editor holds. Find the view that shows a field before you claim you can verify it.

**Watch for limits.** Free-tier caps, rate limits and quotas surface as modals mid-flow. Find them deliberately rather than being surprised at 3am: create records until something stops you.

## Phase 3: map every field's widget

This is where silent failures are manufactured. For each field, record its **widget type**, because the interaction differs:

| Widget | Tell | How to set |
|---|---|---|
| Text input | `<input>` | `.fill()` |
| Multi-line | **`<textarea>`** | `.fill()`, but a selector saying `input[...]` matches nothing |
| Native select | `<select>` | `.selectOption()` |
| Custom select | `div[class*="-control"]`, react-select | click control, then click the option |
| Toggle/checkbox | `role=checkbox` | `.check()` |
| Conditional column | present only for some records | detect before indexing |

Two traps that cost real time:

- **Placeholder-based filters exclude labelled fields.** `input:not([placeholder])` skips the note field that carries a placeholder. Enumerate all inputs with their tag, placeholder, aria-label and value before choosing a filter.
- **Index arithmetic breaks on conditional columns.** A row may be `[weight, reps]` or just `[reps]` depending on the record. Detect the column set per record (`(await block.innerText()).includes('KG')`) rather than assuming a fixed stride.

Dump the full field inventory once, and keep it:

```js
await page.evaluate(() => Array.from(document.querySelectorAll('input,textarea,select'))
  .map(e => ({ tag: e.tagName, type: e.type, ph: e.placeholder, aria: e.getAttribute('aria-label'), name: e.name, val: e.value })));
```

## Phase 4: assume every write failed silently

**This is the doctrine that matters most.** In browser automation the dominant failure is not an exception, it is a write that reports success and did nothing:

- `.fill()` on a locator matching zero elements
- Writing to a real element that is not the one you meant
- A framework overlay (1Password, cookie banners) eating focus
- A value set but discarded because the form was not committed

So: **verify every write by reading it back through a different path than you wrote it.** Write via the form, verify via the edit view or the API or a fresh page load. Never trust the save handler's own response, and never trust an exit code.

When a value must round-trip, the acceptance test is: **create → read back → assert → delete.**

## Phase 5: codify

Two artifacts. Both are required; a CLI without the reference rots silently.

### The CLI

- One verb per operation, mirroring the entities: `<tool> <entity> <list|show|create|delete>`
- **Reads from a bulk export or cached data where possible**, writes through the browser. Reads should not need a browser at all.
- Accept declarative input for creates, a JSON spec rather than positional flags. Specs are diffable, reviewable and re-runnable.
- Print a machine-readable line (`TOOL_OK`, `TOOL_ERR`) that the wrapper greps, so failures are loud.
- Detect known limits and report them rather than hanging.

### The DOM reference

The recovery kit for when the site redesigns. It must contain:

1. **Stable anchors** (URLs, `role=` locators, accessible names) in one table.
2. **Fragile anchors** flagged as fragile, with **how to re-derive them**. A hashed class like `div.sc-421920c7-0` is styled-components output and *will* rotate. Write down the symptom of staleness and the derivation snippet, not just the current value.
3. **Every trap you hit**, with its symptom. Traps are the expensive knowledge; the selectors are cheap.
4. **The Phase 0 finding**: which cheaper paths were ruled out and why.

## Phase 6: prove it end to end

Before declaring done, run a full round trip on a **throwaway record**, never on real data:

```
create  -> verify every field through an independent view -> delete -> confirm gone
```

If a field cannot be verified, say so explicitly rather than assuming. "Notes are set but I could not confirm them" is an honest and useful statement; silence is not.

## Anti-patterns

- **Writing the script during exploration.** You encode assumptions before you know the shape, then debug the script instead of the site.
- **Trusting a summary count.** "8 exercises, 25 sets" can be true while every note is empty.
- **Hardcoding a hashed class without documenting derivation.** Guarantees a future agent starts from zero.
- **Substring matching a name.** `getByText('Overhead Press')` also matches `Seated Overhead Press`. Use `{ exact: true }`.
- **Coordinate clicks without a fallback.** Fine for a menu with no accessible name; record what it is and why.
- **Foreground timeouts on long writes.** A UI write loop can exceed two minutes and a kill mid-flow leaves corrupted records. Background it.
- **Optimising before mapping.** Batch and parallelise after the contract is known, not during.

## Where the artifacts go

| Scope | Location |
|---|---|
| Personal data tied to the user's own accounts | the vault's `.agents/skills/<name>/` |
| A general tool anyone could use | `~/dotfiles/.claude/skills/<name>/` |

Name the skill `<service>-<domain>` so it is callable and triggers precisely. Put the trigger vocabulary in the description, including the user's other languages, not in the name.

See `reference/worked-example.md` for a full mapping that followed this process.
