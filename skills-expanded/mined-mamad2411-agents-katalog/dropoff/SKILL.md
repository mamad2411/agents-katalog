---
name: dropoff
description: >-
  Publish a doc, a diagram, a code snippet, a table, a diff or a small file from
  the terminal, which answers with an unlisted URL. Use when the user asks to
  publish, post or put something online ("publiceer dit plan op dropoff.sh", "zet
  dit diagram online"), to update something published earlier, to upload a small
  image, to show a code change as a rich diff ("publiceer deze diff"), or wants a
  diagram of a process, flow, pipeline or architecture ("maak een diagram van het
  inlogproces", "teken deze pipeline").
license: MIT
---

# Publishing to dropoff

`publish.ts` takes a file and hands back a link. It is the whole interface: run
it, read what it prints, report that. Everything it refuses or warns about it
says in words, so there is no need to open the script or guess at the host.

## Setup

The script runs on [Bun](https://bun.sh), and the skill is installed with
`npx skills add basmilius/skills --skill dropoff`, updated with
`npx skills update dropoff`.

| Variable | Holds |
| --- | --- |
| `DROPOFF_TOKEN` | The bearer token the host issued |
| `DROPOFF_ENDPOINT` | Optional. Another host to publish to, when not `https://dropoff.sh` |

The variable has to reach a non-interactive shell, so on macOS it belongs in
`~/.zshenv` or in the `env` block of `~/.claude/settings.json`, never in a
project's `.claude/settings.json`, which is committed. If the token is missing,
or the account still has to confirm its email address, the script says so and
stops. Report that rather than inventing a value or writing a config file: there
is no config file to write.

## Choosing a type

- **doc** for prose: a plan, a summary, notes, a proposal. Markdown.
- **diagram** for a process, a flow, a pipeline or an architecture, drawn from
  markup you write. A picture that already exists, an exported SVG or a
  screenshot of one, is a **file** instead.
- **code** for one snippet, highlighted server-side. Needs `--language`, a shiki
  name such as `ts` or `python`.
- **table** for tabular data, rendered sortable and filterable. CSV or a JSON
  array.
- **diff** for one file's unified diff, exactly as `git diff` printed it, the
  `diff --git` and `index` lines included and no fence around it. A patch
  touching two files is refused, so pass one path at a time.
- **file** for raw bytes: a screenshot, a small photo, a PDF. The extension has
  to be one of avif, csv, gif, ico, jpeg, jpg, json, md, pdf, png, svg, txt,
  webp or zip.

## Publishing

Write the content to a temporary file first, outside the repository unless it
already belongs there, and hand that file over; never pass long content as a
shell argument. Run the script from the project the page is about, since that is
where the project tag comes from.

```shell
bun ~/.claude/skills/dropoff/publish.ts \
    --type doc \
    --title "Login flow" \
    --description "How a session is issued, end to end." \
    --tags auth,review \
    --file /path/to/content.md
```

That is the usual skill path; if this skill lives elsewhere, run the
`publish.ts` that sits next to this file.

| Argument | Required | Notes |
| --- | --- | --- |
| `--type` | yes | `doc`, `diagram`, `file`, `code`, `table` or `diff` |
| `--title` | yes | The page heading, and what the slug comes from. At most 200 characters |
| `--file` | yes | Path to the source |
| `--description` | no | One sentence, for link previews. At most 300 characters |
| `--tags` | no | Comma separated, on top of the project tag |
| `--no-project-tag` | no | Leave the project out of the tags |
| `--language` | code | A shiki language name, such as `ts` or `python` |
| `--format` | no | A table's format, `csv` or `json`; auto-detected when left out |
| `--folder` | no | File the item under a folder, created on first use (Pro) |
| `--path` | no | Publish onto an existing page, as its `<code>/<slug>` path or its `/p/<code>` short link |
| `--new` | no | Force a fresh URL even when the title was published before |
| `--check` | no | Check a diagram's spacing and stop; publishes nothing |
| `--force` | no | Publish a diagram the spacing check objects to |

Reporting the link is the point of the operation. A page leads with a short
`/p/<code>` link and that is the one to hand back; a file leads with its long
URL instead, because only that one spells out the extension a markdown image
needs. Neither follows from the title, since the slug ends in a code of its own,
so take both from the output rather than assembling one.

The lines after it say whether a page was replaced, which tags it carries and,
on a plan that expires pages, when this one goes. No expiry line means it stays.
Mention one when it is there: a link that disappears in three days is a
different promise than one that does not.

How large a source may be, how many items may be live at once, whether folders
are available and how often you may publish all belong to the account's plan
rather than to the script. The host answers what it allows and the script prints
it, so relay that instead of retrying.

### Replacing a page

A page is keyed on its title and its type, so publishing the same title again
lands on the same URL and keeps its original date, while a doc and a diagram of
the same name stay two pages. Pick a title specific enough not to collide, and
if the output says `(replaced the existing page)` when you did not mean to
replace anything, say so and offer `--new`.

- The user gives a URL to update: pass everything after the domain as `--path`.
  The code is what lands it on the page it names, so the slug beside it need not
  match.
- The user wants a second page under the same title: pass `--new`.
- An upload always takes a fresh URL unless `--path` names one to replace, and
  the replacement has to carry the same extension. Its path carries that
  extension too, so it goes in whole:
  `--path 4hydssm/delivery-states-nyjvfg.svg`.

`--title` is required either way, and on a replacement it becomes the page's new
title while the URL stays exactly as it was. So a page can end up with a slug
that no longer reads like its title, which is fine: only the code resolves it.
There is no way to read a title or a set of tags back before overwriting them
(bar a doc's markdown, below), so when either matters, ask rather than guess.

Appending `.md` to a doc's long URL hands back the markdown it was published
from, so an earlier page can be read before it is rewritten rather than
republished from memory.

### Tags

Tags are what make something findable again. The script adds one for the
repository it runs in; add two or three of your own with `--tags` for the
subject or the kind of work, such as `auth`, `review` or `incident`. Publishing
replaces a page's tags rather than adding to them, so pass them again when
republishing something that carried tags worth keeping.

That project tag only helps while the page really is about the project you are
standing in. When it is not, a scratch demo or something written for someone
else, pass `--no-project-tag`: a tag naming the wrong project is worse than no
tag at all, since it files the page with work it has nothing to do with.

## Writing a doc

The page carries its own house style, so write none: no HTML, no inline styles,
no headings used for visual effect. Punctuate with hyphens, commas, colons or
parentheses, never en or em dashes.

Start the markdown at `##`, since `--title` is already rendered as the page
heading, and give the h2 and h3 headings meaning: they become the side
navigation. Write the whole document in one language, headings included, and let
the work decide which rather than the request. A repository whose code and
comments are English gets an English page even when the ask for it came in
another language.

GitHub-flavoured markdown works throughout: tables, task lists, footnotes,
strikethrough, and a code fence highlighted for every language shiki knows. On
top of that a doc may use components: cards, an embedded diagram, callouts,
collapsibles, progress bars, stat tiles, badges, file trees, steps, a facts
panel, tabbed code groups and rich diffs. **Read `references/doc-components.md`
before writing one**; the syntax is unforgiving about closing markers and
quoting.

A diagram is the only item a doc embeds, so publish it first as its own
`--type diagram` and embed the path it printed. Add one where a picture saves
the reader a paragraph, not to every doc. A code, table or diff item is linked
with a card instead; short code and small tables belong in the doc itself.

## Building a diagram

A diagram is one root element holding nodes you place yourself, at pixel
coordinates. Nothing lays it out for you, and a coordinate that leaves two nodes
too close only shows up once the page is live, which is what `--check` is for.

Everything is static: no state, no data, no event handlers, no `<script>` block
and no `<template>` wrapper. A template carrying any of those is refused rather
than published without them.

1. Write the flow out as steps first, in prose. One spine down the page and
   branches sideways: a reader follows a single line far more easily than a
   balanced tree.
2. Read `references/diagram-components.md` and pick a component per step.
3. Read `references/diagram-layout.md` and place the nodes from the top down.
   Each `y` is the previous node's `y` plus that node's height plus the space
   its connection needs. Never a fixed increment: a card is as tall as its text.
4. Line them up. A narrow node under a wide one goes at
   `x + (wide - narrow) / 2`, because both ends attach at their own middle.
5. Wire the connections. Markers off at either end that touches a junction or a
   gate, a short label or an icon on a branch, and that choice held across the
   whole diagram.
6. Run `--check --file <path>`, fix what it names, then publish.

Fix coordinates rather than reaching for `--force`. The check measures what the
viewer will actually draw, so what it objects to is what a reader would see: a
badge lying across two cards, a line with no visible stretch left in it. Every
number it asks for is in `references/diagram-layout.md`, and moving a node down
is a one-character edit.

What it measures is the room between two nodes and the markers where they meet a
junction. Where a connector lands is yours to get right: a junction belongs at
the middle of the node after it, and two nodes line up only when you line them
up. A silent check means nothing is crowded, not that the diagram reads well.

The viewer opens every diagram full screen, centred, on a dotted canvas, and
makes it draggable and zoomable, so leave those props out. It rejects a
component or an icon it cannot resolve, since both would render as nothing at
all and the warning never reaches a live page.
