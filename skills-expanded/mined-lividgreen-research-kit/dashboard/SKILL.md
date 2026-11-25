---
name: dashboard
description: One read-only browser dashboard over the flow's records, the reference library's cards and any other component installed beside it and bound in the project — every page the component's own command-line answer, rendered. Use when the owner wants to browse the records or the cards, when asked to start or stop the dashboard, and when writing a new component that should add its pages to it. Reads no record or card file itself and writes nothing.
license: Apache-2.0
compatibility: Python 3.11 or later, standard library only; a browser. Optional - the `markdown` package for rendered bodies (paragraphs otherwise). Renders only components that answer `--json pages`, today the `flow` and `library` skills' CLIs.
metadata:
  version: "0.12.1"
  script: scripts/dashboard.py
---

# The dashboard

`python3 scripts/dashboard.py`, run by its path from the project root (`${CLAUDE_PLUGIN_ROOT}/skills/dashboard/scripts/dashboard.py` under Claude Code), serves one site on localhost, port 8765 by default, with one section per mounted component.
The flow's records are a card table: `/` opens on the table, each owner's hand, the open goals and the open directions face up, each owner's deck behind a stack of card backs, the common deck and the two piles, every card a face with its title, its summary, its value and effort, its standing and its place; the lists lay the same faces, a record is its card at the left with its panel beside it, and the directions, the artifacts, the tags, the index and the validator's verdict are pages of their own.
The library's works are cards too, with a ranked search, each work with our notes, extracts and citing sites, and the candidates, the watches and the check as tables.
It is a renderer and nothing else.
Every page is the answer of the component's command with `--json`, so the command line and the dashboard cannot disagree; no work is shown and no path into the library's store is served.
It re-asks on every request, so a transition run in another terminal shows on the next reload.
It answers only a request addressed to it by name: `--host 0.0.0.0` serves other devices under this machine's names and its addresses, and `--allow-host NAME` adds a name a proxy or a tunnel uses; a page of another site never loads one of its pages in the background.

## What it mounts

Components are found in this order, the first mount of a name winning: a `--component CMD…` on the command line; `dashboard.toml` at the project root, with `[[component]]` tables naming a `command` list; the skill directories beside this one whose `component.toml` names a `command` and a `bindings` file, mounted when the bindings file exists at the project root; the `flow` and `library` commands on PATH when their bindings file exists.
So a skill adds its pages to the one dashboard by being installed beside it — in the same skills directory, or as a sibling plugin of the same marketplace, each plugin read at its newest version — and bound in the project, and `dashboard --list` prints what would be mounted.

## Writing a component

A component is any command that answers `<command> --json pages` with a page manifest and every other page as `<command> --json <subcommand> …`; `references/protocol.md` is the manifest's shape — the mount, the navigation entries, the link patterns that turn an id in any text into a link across components, and the home page, the `card` key that lays a record on a card's face, and the routes with their views: `markdown`, `lines`, `list`, `table`, `record`, `tables`, `check`.
A component ships a `component.toml` beside its `SKILL.md` naming its command relative to the skill directory and the project's bindings file.
`scripts/dashboard.py --selftest` mounts stub components, one with a `card` and one with none, and renders every view.
