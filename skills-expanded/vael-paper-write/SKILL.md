---
name: vael-paper-write
description: Write tomorrow's edition of the personal newspaper. Use when asked to produce, draft, assemble or fix an edition, section, or story for the Vael Paper — the nightly generator loop.
---

# Write an edition of the Vael Paper

You are the night editor of a personal newspaper that prints for one reader.
Your output is files in `editions/`, not prose in the chat.

## Read first

1. `../vael-paper/docs/WRITING.md` — the whole contract: fields, lengths,
   tables, pictures, voice. It is short. Read it.
2. `editions/paper.json` — the section ids and their order. Use only those ids.
3. The most recent edition's `articles/` for the house style, and so you do
   not repeat yesterday's story under a new headline.

## The desks — run them in order

**Data desks (no model).** Render the structured files in `inbox/` through the
scripts in `scripts/` (calendar, budget, steps, portfolio). These produce
correct tables every night by code. Do not improvise; do not have yourself
"improve" them.

The **weather desk** is a data desk that reads a live feed instead of a file:

```
python3 scripts/weather-desk.py <edition_dir> --place <name>
```

It fetches the 7-day forecast from Open-Meteo and writes a Weather story with
a chart and a board. It needs network; if the fetch fails, omit the weather
story — never invent a forecast. The `weather` section it uses is already in
`editions/paper.json`.

The **finance desk** is a live data desk for a Financial page:

```
python3 scripts/finance-desk.py <edition_dir>          # NVDA, AMZN, MU by default
python3 scripts/finance-desk.py <edition_dir> AAPL MSFT
```

It fetches Yahoo Finance quotes (no key) and writes a markets table with the
close, day change and percent for each ticker, plus a templated reading. It
needs network; if any ticker fails to resolve, omit the Financial story rather
than print a guessed price. Its `financial` section is already in
`editions/paper.json`.

**Prose desks (you).** One story per desk, from a handful of already-summarised
items in `inbox/`:

- three to five feed items (a paragraph each, with URLs);
- a photo or two from `inbox/photos/` the household desk may use;
- a page from your notes, for "this week last year".

Each desk has its own rules in its prompt: length, whether it needs sources,
its voice.

**The lead desk (last).** See everything produced and write the front page:
the reader's own day in the order it will happen, tying the data to the
stories. Exactly one story carries `priority: 1`; it is this one. An exemplar
front page — a target the edition must still check clean — is in
`../samples/lead-desk/`.

## Writing rules

- One markdown file per story in `articles/`, numbered in reading order.
- Only the headline is required. A leading `# Heading` works without
  frontmatter; a colon in the headline is fine; `title`, `author`, `photo`,
  `category` are all matched.
- A story that summarises something published elsewhere carries `sources:`.
  Only `http`/`https` URLs are ever linked.
- Charts are `chart: {kind: bars|line, values: [...]}` — never a hand-made
  image. Put the reading in the caption.
- Photographs only from `inbox/photos/`, copied into the edition's `images/`.
  Give a `focus:` (top/center/bottom) to any tall image.
- Tables: at most four columns, longest cell under 26 characters, day folded
  into the time (`Thu 9:30`), a `### Label` line directly above.
- Write in the paper's voice (see the AGENTS.md or WRITING.md).

## Finish

Run the check from the Vael Paper repo that this agent feeds:

```
cd server && uv run vael-paper-check ../editions/<date> --json
```

Fix by code — the codes and their fixes:

| code | do this |
|---|---|
| `yaml_parse` | Open file at line; usually an unquoted colon, bracket, or indent. Quote the value or rewrite the frontmatter. |
| `no_headline` | Add `headline:` or start with `# Heading`. |
| `unknown_section` | Use an id from `editions/paper.json`. |
| `missing_image` / `bad_image` | Remove `image:` or point at a file that exists in `images/`. |
| `bad_chart` | `values` needs 2+ numbers; `kind` is line/bars; `labels` short; `min` below `max`. |
| `unsafe_source` | Only http/https are printed. Drop or fix the link. |
| `table_wide` / `cell_long` | Drop a column, shorten the longest cells, fold day into time. |
| `cell_truncated` | Don't cut cells with `…` yourself; shorten in words. |
| `plate_aspect` | Add `focus:` or use a landscape image. |
| `story_short` / `story_long` | Fold into another / split. |
| `headline_long` / `deck_long` | Cut. |
| `no_lead` | Give the front-page story `priority: 1`. |

Repeat until `"ok": true`; stop at `"clean": true` when you can. Do not
declare the edition finished while `"ok"` is false — say which marks remain
and what blocked them.