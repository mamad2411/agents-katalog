---
name: ryai-build
description: Build the pages in a PROJECT.md plan by pulling real components and prompts from the RYAI library instead of writing every block from scratch. Use after ryai-plan has written a PROJECT.md, or when someone says "build the plan", "start building", "/ryai-build". Also use when a project already has a PROJECT.md with an unchecked block list.
---

# RYAI Build

Work through `PROJECT.md` one block at a time, sourcing each from the library.

**Speak the user's language.** Identifiers and filenames stay as they are.

## Before starting

Read `PROJECT.md`. No plan file → run `ryai-plan` first, do not improvise a page list.

Every block line carries `(code)` or `(prompt)`. That tag decides the route, and the two
routes are not interchangeable:

| Tag | Route | Why |
|---|---|---|
| `(code)` | `fetch_blocks` → download → write files | Ships real component code |
| `(prompt)` | `get_prompt` → generate from the body | No prebuilt code exists |

## Route A — blocks that ship code

Batch every `(code)` slug for one page into a single `fetch_blocks` call.

```
fetch_blocks({ slugs: ["hero-x", "pricing-y", "faq-z"] })
→ { downloadUrl, files: [{filename, bytes}], dependencies: [...] }
```

Then download and unpack with the shell — `curl -fsSL "<downloadUrl>" | tar -xz -C <dir>`.

**Do not read the downloaded files.** They are already on disk and correct. A single
component runs ~10,000 characters and a multi-file template ~124,000; reading them back
burns the context this route exists to protect. Read one only if something actually
fails — a build error, a missing import — and then only that file.

Install the union of `dependencies` across all blocks in one command, not per block.

## Route B — blocks with no code

One `get_prompt` per block, generate, move on. Do not fetch several bodies up front:
each is ~8,000 characters, and they pile up in context while you work through them.

```
get_prompt({ slug: "hero-x" }) → { content, dependencies }
```

Follow the body's structure and intent. Match the project's existing conventions —
styling approach, file layout, component patterns — over anything the body assumes.

## Starting from an empty folder

If `PROJECT.md` names a scaffold, call `get_scaffold({ slug })` before anything else.
It returns git clone URLs and your Gitea username; the password is issued separately in
the browser, so if you do not have it, send them to the link the tool gives back rather
than guessing. Clone, then follow `setupSteps`.

Adding to an existing project? Skip this entirely — go straight to the routes above.

## Order of work

1. Scaffold first if `PROJECT.md` names one and the project is empty
2. Route A for the whole page — files land on disk
3. Install dependencies once
4. Route B block by block
5. Wire the blocks into the page in the order `PROJECT.md` lists
6. Run the dev server and confirm the page renders

Tick each `- [ ]` to `- [x]` in `PROJECT.md` as you finish it. That checklist is the
resume point if the session ends midway — keep it accurate, not optimistic.

## When a block is locked

`fetch_blocks` and `get_prompt` return `unlocked: false` with the tier required.

Say plainly which tier that block needs and let them decide. Never silently substitute a
different block to dodge the paywall — they planned around that one. Keep building the
blocks that are available and list the skipped ones at the end.

## Reporting

When the page renders, say which blocks came from real code, which were generated, and
which were skipped as locked. If something is half-wired or a block did not fit the
layout, say so — an unfinished page reported as done costs more to untangle later.
