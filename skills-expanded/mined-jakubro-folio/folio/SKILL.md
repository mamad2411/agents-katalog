---
name: folio
description: Folio serves a folder of markdown and data files to its reader's browser as live pages, and keeps a model of the whole folder that agents query too. Write documents there that use what Folio adds, so numbers and shared text follow their sources where copies go stale - includes of files, sections and blocks; links to any block; data files and SQL results embedded as tables, values and Vega-Lite charts; figures checked against their data; results saved into the markdown; FOLIO.md kinds, fields and rules; components drawing data with scripts - and check them against Folio's health. Use whenever a FOLIO.md sits at or above the working folder, Folio's MCP tools (folio_health, folio_query) are connected, documents are linked at a Folio address such as http://localhost:8640/, or the user names Folio - before writing or editing markdown or a component there, before quoting a number from a data file, before moving or renaming a file, and when asked which page the reader has open, what they have read or what changed.
---

# Writing for Folio

**Where Folio serves a folder, write documents that include, embed and check rather than copy.** Folio is a command that serves one folder of markdown and data files to a browser, every page live, and keeps a model of the whole folder: every block of every document, the data files they read, what links to and includes what, what is broken and what the reader has read. The person you work for reads the folder through it. A number copied out of a CSV goes stale the day the CSV changes, and nobody notices; an embedded one redraws, and a figure tied to its data turns red when the data disagrees. A pasted paragraph drifts from the document that owns it; an included one follows it. The files stay plain markdown, and how they read outside Folio is never a reason to hold back from its syntax:

- **Never copy a number out of data.** Embed it with `{value: ...}`, or tie the figure you type to its data with `<data value="...">`.
- **Never paste text another document owns.** Include its file, section or block.
- **Never keep a list by hand that a query can produce.** Query the data files, or the documents themselves.
- **Never describe in prose what a chart or a map can show.** Draw it from the data.
- **Link to the exact block**, not to the page around it.
- **Give every recurring kind of document its fields and rules** in a `FOLIO.md`, so the folder checks itself.
- **Ask Folio what the folder knows** - what uses a file, what is broken and, when the user asks, which page they have open and what they have read - rather than working it out from the files.
- **Check the folder after every edit.** A broken include, link, query or figure shows to the reader in red.

Where nothing marks the folder as Folio's - no `FOLIO.md` at or above it, no Folio tools, no Folio serving it or a folder above it (*Find Folio*) - write plain markdown: Folio's includes, embeds and queries render nowhere else.

In the raw text of this skill every include example carries a backslash before its brace, so Folio does not resolve the examples when it serves these files. Write includes without the backslash.

Declaring a folder's conventions in `FOLIO.md`: [references/conventions.md](references/conventions.md). Writing a component: [references/components.md](references/components.md). Every limit and edge case is in Folio's reference: [Command line](https://jakubro.github.io/folio/reference/command-line/), [Addresses](https://jakubro.github.io/folio/reference/addresses/), [Model API](https://jakubro.github.io/folio/reference/model-api/), [Data files](https://jakubro.github.io/folio/reference/data-files/), [Embedded data](https://jakubro.github.io/folio/reference/embedded-data/), [Components](https://jakubro.github.io/folio/reference/components/), [Queries](https://jakubro.github.io/folio/reference/queries/), [Reading](https://jakubro.github.io/folio/reference/reading/), [History](https://jakubro.github.io/folio/reference/history/), [Digests](https://jakubro.github.io/folio/reference/digests/), [Conventions](https://jakubro.github.io/folio/reference/conventions/), [Saved views](https://jakubro.github.io/folio/reference/saved-views/), [Markdown](https://jakubro.github.io/folio/reference/markdown/) and [Security and limits](https://jakubro.github.io/folio/reference/security-and-limits/).

## Find Folio

Ask a running Folio what it serves. It answers `root`, the folder it serves, and lists every resource:

```sh
curl -s 'http://localhost:8640/?api'
```

- **Which Folio** - each Folio serves one folder, on port 8640 or, when another Folio holds that port, the next free one above it, unless it was started with `--port`. Use the one whose `root` is the folder you work in or a folder above it; when 8640 serves another folder, ask 8641 and up.
- **Paths are relative to `root`, or absolute under it**, and `root` may lie above the folder you work in: with `root` `/srv/notes`, the file `/srv/notes/reports/weekly.md` is `reports/weekly.md` or `/srv/notes/reports/weekly.md` in every `?api=` address, tool argument and path a tool's query quotes, and `reports/weekly.md` in every result. A path relative to the folder you work in is not one of them; a refusal of a path names `root`. With only the tools, find a file you know in `folio.documents`: `select path from folio.documents where filename = 'weekly.md'`.
- **A socket** - a Folio started with `--socket PATH`, as one shared with a container is, answers on it too: `curl -s --unix-socket PATH 'http://localhost/?api'`.
- **No Folio** - the user starts Folio, as `folio FOLDER`; never start one yourself, since a running Folio writes into the folder what its `FOLIO.md` declares. When none answers, ask the user to start it - or, when one already serves the folder on another port or a socket, to start `folio mcp` with `--port` or `--socket` to match, or, with the folio plugin in Claude Code, to set the plugin's Folio setting, in `/config`, to that Folio's address or socket.
- **Tools** - Folio's MCP server gives the same answers as read-only tools; when `folio_*` tools are connected, use them. Otherwise the agent's MCP client starts the server as a command, from its configuration. It reads the Folio serving the agent's folder, wherever that Folio serves; `"args": ["mcp", "localhost:N"]` or `["mcp", "PATH"]` for a socket names one outright:

```json
{ "mcpServers": { "folio": { "command": "folio", "args": ["mcp"] } } }
```

In Claude Code, the folio plugin installs the server and this skill, `/folio:folio`, running the Folio release it pins through `npx`:

```sh
claude plugin marketplace add jakubro/folio
claude plugin install folio@folio
```

Before writing into a folder, read what it declares: every `FOLIO.md` in the folder and the folders above it. `?conventions` on an existing document names its kind and the fields it reads; for a document not written yet, `?api=kinds` on its path lists the kinds, rules and health entries applying there, each kind with the `where` patterns that place a document in it.

```sh
curl -s 'http://localhost:8640/stations/north.md?conventions'
curl -s 'http://localhost:8640/stations/west.md?api=kinds'
```

## Assemble from other documents

````markdown
\{include: parts/intro.md}

\{include: design.md#retry-policy}

\{include: design.md#^3f9a1c2e}
````

- A whole file, the section under a heading by its anchor - up to the next heading of the same or a higher level - or one block by its id.
- The path resolves against the including file's folder, or the served folder when it starts with `/`. It holds no brackets, braces, quotes or commas.
- Includes expand everywhere - prose, inline code, code blocks and diagram fences - and at any depth. A `mermaid` fence holding only `\{include: network.mmd}` draws that file's diagram, and a document may include a section of itself.
- The page updates when an included file is saved. An include that finds nothing stays as written, marked red, and is listed in health.
- `\\{include: path}` shows the include as text, never resolved.

## Link to headings and blocks

- Headings take GitHub's anchors: `[retry policy](design.md#retry-policy)`, or GitHub's `#user-content-retry-policy` form.
- Every block has an id, the ¶ in its margin: `[the threshold](design.md#^3f9a1c2e)`. A block link keeps landing on its block while the block is reworded or moved. A block id is 8 hex characters Folio derives - never invent one. Save the file, then read the ids from its blocks; a document Folio has not read yet answers 503, so ask again:

```sh
curl -s 'http://localhost:8640/design.md?api=document'
```

- Backlinks are automatic: every page lists the documents linking to it, with the words around each link. Never keep a list of the pages pointing back.
- Link straight to data files and query files - each opens as a page - and to one table of a database: `[readings](data/archive.sqlite?table=readings)`.

## Put data in the document

CSV, TSV, JSON Lines, Parquet, JSON, YAML, SQLite and DuckDB files open as pages and embed into documents. A reference names what to read:

| Reference | Reads |
|---|---|
| `data/daily.csv` | The whole file; a tabular file's data is its list of rows |
| `data/daily.csv#0.rain_mm` | A part: keys, and row or list positions from 0, joined by dots |
| `data/stations.json#north.elevation_m` | A key path into nested data |
| `data/archive.sqlite#readings` | A database's table |
| `queries/wettest.sql` | A query file's result |
| `#totals` | The result of the query named `totals` in the same document |
| `#totals#0.rain_mm` | A part of that result |

A path resolves against the folder of the file it is written in - a document's, or a `.sql` file's own - or against the served folder when it starts with `/`.

````markdown
{table: queries/wettest.sql}

The network logged {value: #totals#0.rain_mm | ,.1f} mm of rain, <data value="#totals#0.wet_days">9</data> days of it wet.

```vega-lite
mark: line
data: {url: data/daily.csv}
encoding:
  x: {field: day, type: temporal}
  y: {field: rain_mm, type: quantitative}
```
````

- **Table** - `{table: ref}` alone in a paragraph or list item, at any depth. The reader sorts, filters, hides columns and folds it.
- **Value** - `{value: ref}` anywhere in a paragraph, heading, list item or table cell, outside code. A space, `|`, a space and a [d3-format](https://d3js.org/d3-format) specifier format a number: `{value: ref | .1%}`, `{value: ref | ,.0f}`.
- **Figure** - `<data value="ref">48.2</data>` keeps the typed figure in the text and checks it against the data. A number matches within half a unit of its last typed digit; thousands separators, a sign, a currency mark and `k`, `K`, `M`, `B` or `bn` are allowed, and a figure ending in `%` reads a data value between -1 and 1 as a fraction. A date matches on the parts typed. A range such as `29-56%` is not checked, and health never lists it. Keep units outside the tag. A contradicted figure is underlined red with the data's value beside it and listed in health.
- **Chart** - a `vega-lite` fence holding a Vega-Lite description in JSON or YAML; every `data.url`, at any depth, is a reference. In YAML, quote a reference starting with `#` - unquoted, it is a comment.
- **Component** - a `component <name>` fence holding YAML: `data` maps each entry name to a reference, every other key is an option. A Folio started with `--components PATH` draws it with `<name>.js` from that folder; `curl -s 'http://localhost:8640/?components'` lists the components it has, and a fence naming none of them is listed in health. The folder holds built `.js` files only, each compiled from its sources in that folder's own build; writing one, in plain JavaScript or in TypeScript and React: [references/components.md](references/components.md).

````markdown
```component levels
data:
  readings: data/daily.csv
  totals: '#totals'
title: Rain by station
```
````

Use a value where the sentence should always carry the data's current number, and a figure where the number belongs to the prose and must stay true. Every embed, chart, component and query result redraws on each open page when a file it reads changes. One whose file or part is missing shows the reference and why, marked red, and the rest of the page draws.

## Query the folder

A `sql query` fence runs one DuckDB `SELECT` from the document's folder and shows its result below the fence; a plain `sql` fence stays code. A name after `query` makes the result a reference, `#name`, for embeds, charts, figures and saved views of the same document - not for another query, which reads a shared query from its `.sql` file instead:

````markdown
```sql query totals
select round(sum(rain_mm), 1) as rain_mm, count(*) filter (where rain_mm > 0) as wet_days
from 'data/daily.csv'
```
````

- **Files** - a path in quotes is a table: `'data/daily.csv'`, `'data/archive.sqlite#readings'`, or `'queries/wettest.sql'` for another query's result. `read_csv`, `read_json`, `read_ndjson`, `read_parquet` and their variants read the folder's files named in quotes.
- **Patterns** - `*` and `?` match within one folder, `**` across folders: `'logs/**/*.jsonl'` reads every match, thousands as readily as two, stacked by column name, with each row's file in a `filename` column. A pattern matching nothing is an empty table, and a file matching later is picked up. A matched JSON, JSON Lines or YAML file that cannot be read - half-saved, or holding merge-conflict markers - is left out and the rows come from the others, health names it where a document or a rule reads the pattern, and `?api=query` lists it in `leftOut`; a key one file holds as text and another as a record reads as JSON in every row.
- **Query files** - a `.sql` file holds one query, opens as a page showing its text and result, and is used by its path wherever a reference goes.
- **Documents** - the folder's documents are tables too, with nothing to declare. Content an include brings in counts in the file holding it.

| Table | Columns |
|---|---|
| `folio.documents` | `path`, `filename` (the file's name without its folder), `title` (the one h1 outside `<details>`; null with none, an empty one or several), `kind` |
| `folio.headings` | `path`, `line`, `level`, `text`, `anchor` |
| `folio.links` | `path`, `line`, `url` (as written), `target`, `fragment`, `context` |
| `folio.tasks` | `path`, `line`, `done`, `text` |
| `folio.frontmatter` | `path`, `key`, `value` |
| `folio.tables` | `path`, `line`, `row`, `header`, `cells` |
| `kind.<name>` | `path` and a column per field the kind declares |

````markdown
```sql query open
select t.path, t.line, t.text
from folio.tasks t
where not t.done
order by t.path, t.line
```
````

- **Limits** - one `SELECT`. `PIVOT`, `COPY`, `ATTACH`, anything writing a file, a path outside the served folder and a web address are refused; among table functions only the readers above, `range`, `generate_series` and `unnest` run. A query stops after 10 seconds, and a result keeps its first 10,000 rows and 16 MB.

Run a query or resolve a reference before writing it into a document:

```sh
curl -sG 'http://localhost:8640/reports/?api=query' --data-urlencode "sql=select count(*) from '../data/daily.csv'"
curl -sG 'http://localhost:8640/reports/weekly.md?api=embed' --data-urlencode 'reference=#totals#0.rain_mm'
```

## Save a result into the markdown

Where a `FOLIO.md`'s `save` section places the document, Folio writes a result into a marked region as plain markdown and rewrites it whenever the result changes, so the result also reads on GitHub and in any editor:

````markdown
<!-- folio view: #active -->
<!-- /folio view -->

```sql query active
select s.id, s.owner, s.calibrated from kind.station s where s.status = 'active' order by s.id
```
````

- The reference after `folio view:` is any reference: a data file or a part of one, a `.sql` file, or `#name`.
- Folio writes a table, or a single value as text, and never changes a byte outside the region. Never edit inside a region: the next write replaces a hand edit, and health reports it.
- Each marker stands on a line of its own; markers inside a code fence are examples, and Folio never writes into them.
- Folio writes a view only into a document a `save` entry places; declare one as [references/conventions.md](references/conventions.md) shows.

## Markdown Folio renders

- GitHub-flavoured markdown - tables, task lists, strikethrough, footnotes and bare links - plus `$...$` and `$$...$$` math, inline math also as GitHub's ``$`...`$``, and fenced code highlighted by the language named after the fence.
- Alerts: a quote at the top level of the page whose first line is only `[!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]` or `[!CAUTION]` shows as a callout.
- Colours: inline code holding exactly one colour - `#RRGGBB`, `rgb(R, G, B)` or `hsl(H, S%, L%)` - shows a swatch of it. Short hex, names and alpha forms stay plain code.
- Diagrams: a `mermaid` fence, or a whole `.mmd` or `.mermaid` file as a page. The reader opens any diagram over the whole window to zoom and pan, and a chart, map, model or image not inside a link the same way.
- Maps: a `geojson` fence holding GeoJSON, or a `topojson` fence holding a TopoJSON topology, draws its shapes as a map, without fetching anything until the reader loads map tiles. Draw a map from a file the folder keeps with a fence holding only `\{include: data/stations.geojson}`.
- 3D models: an `stl` fence holding an ASCII STL model, `solid ... endsolid`, draws as a model the reader turns by dragging.
- HTML elements: `<details>`, `<kbd>`, `<mark>`, `<sub>`, `<sup>`, `<abbr>`, `<u>`, `<small>`, `<cite>`, `<dfn>`, definition lists, figures and tables with merged cells, each of them taking `class` and `style`. Scripts, event handlers and `javascript:` links are stripped.
- YAML frontmatter shows as a table at the page's end, under *Metadata*. A markdown link in a value - quoted when the value starts with it, as YAML reads a leading `[` as a list - is a link like one in the page: it opens its target, counts under Linked from and in `folio.links`, and health lists it when broken.
- Loose tables: rows with extra or missing cells, and pipe lines without a divider line, still render as tables.
- Every table but the frontmatter's - written, embedded or queried - sorts, filters, hides columns and folds in the reader's view. Write a table in its natural order.

## Edit so the reader can catch up

Folio remembers which blocks the reader has read, and marks each block added (green), changed (amber, the text as read a click away) or removed (a red tick) since - a table by its rows, a list by its items, code by its lines; the tree puts a dot after each document holding a mark. A block showing an embed, chart, component or query result is marked when its data changes, and a block an include brings in when its file changes.

- Change only the blocks whose content changes. Rewrapping a paragraph, repadding a table, line endings and moving a block whole count for nothing; rewording a block, or reordering the items or rows inside it, marks it.
- A moved or reworded block keeps its identity, its links and its history.
- Never write change notes into a document: Folio keeps every committed version and the saves it saw - all of them for 30 days, then the last of each day - compares any two block by block, and builds a digest of any period.
- Link every new document from another one. A document unchanged for a year, never read and linked from nowhere surfaces as outlived.
- Before editing, moving, renaming or deleting a file, ask what uses it - `?api=used-by` on its path lists every document including it, or embedding or querying its data, and `select path, line from folio.links where target = 'design.md'` every link to it - and update every link, include, embed and figure naming it.

## Check the work

While Folio runs, `/?api=health` - `folio_health` among the tools - lists everything wrong in the folder, each problem with its document, line and block, and `/<path>?api=health` - `folio_health` given `path` - only the problems of that document or of the documents under that folder, once what changed there is checked; while it answers `"ready": false`, Folio is still reading the folder or has never checked it, so ask again. While Folio reads the folder after starting, `folio_health`, `folio_needs` and `folio_changes` answer as last worked out with `"ready": false`, and what has nothing to answer from - `folio_stale`, `folio_kinds`, `folio_digest`, `folio_used_by`, a query over the documents, and the three above on a first start - answers 503, Folio is still reading the folder: ask again shortly. The whole folder answers at once with the problems as last checked, and `"checking": true` while Folio is still checking changes: give the path of what you edited for its current problems; `folio_needs` answers the same way. Read every problem in a file you touched. A tool's answer too long for one has its lists cut to fit and says, in `omitted` and `narrow`, how many entries each list left out and how to ask for less. Without a running Folio, or to gate a commit:

```sh
folio check ROOT
```

- **Components** - `folio check ROOT --components PATH`, the folders the user's Folio starts with, checks component fences against their scripts when no Folio serves the folder; a check working alone without the option lists every component fence as missing.
- **Check the folder Folio serves, never one inside it.** `folio check` takes the folder it is given as the served folder: a folder inside it is checked without the `FOLIO.md` declarations above it, so their rules and health entries never run and it can report a clean folder over their violations. It asks the Folio serving exactly that folder - wherever it serves, or on `--port N` or `--socket PATH` when given - and otherwise works the health out itself.
- It prints one problem a line - `path:line`, the severity (`error`, `warning` for a rule's warning, `-` for any other problem), the kind and what is wrong - then a count. It exits 1 only when a problem is an error: frontmatter that is not YAML, a violation of a rule whose severity is `error`, or a problem of a kind of check a `health` entry declares an error. Contradicted figures, broken links, missing includes, failing queries and diagrams, charts or components that do not draw are listed but do not fail it unless declared, so read every line naming a file you touched - exit 0 is not a clean folder. It exits 2 when no health can be worked out.
- **A draft in a dot-folder**, such as `.drafts/`, or under `node_modules` is left out of health, `folio check`, the folder's lists and digests, yet `?api=document`, `?api=provenance`, `?api=embed` and `?api=reads` - `folio_document`, `folio_provenance`, `folio_embed` and `folio_reads` - read it when asked and answer as for any document: read its block ids and resolve its references there, then check its problems once it moves into place.

While Folio runs, the same answers come per resource:

| Address | Answers |
|---|---|
| `/?api` | The folder Folio serves as `root`, and every resource |
| `/?api=health`, `<path>?api=health` | Everything wrong in the folder as last checked, with `checking`, or in a document or under a folder once checked, each problem with its document, line and block; `/?api=health&wait` once every change heard is checked |
| `<path>?raw` | A document's text with its includes expanded |
| `<path>?api=document` | A document's blocks with their ids, its kind and fields, and the data it reads |
| `<path>?api=embed&reference=<ref>` | What a reference written in the document reads |
| `<folder>/?api=query&sql=<select>` | A query's columns, first 5,000 rows, the files it read and, as `leftOut`, the files a pattern left out |
| `<path>?conventions` | The declarations applying to a document, its kind and its fields |
| `<path>?api=provenance&block=<id>` | Where a block came from: its lines, last change, data files and queries, and the state of each figure |
| `<path>?api=related&block=<id>`, `?api=related&question=<text>` | The blocks of other documents closest in meaning to a block or a question, where a `FOLIO.md`'s `related` asks for it; a block the page does not hold is refused |
| `<path>?api=used-by` | The documents including a file, or embedding or querying its data |

## Tools for agents

`folio mcp` serves the model as read-only tools, each answering as its `?api=` resource does, every time in ISO 8601:

| Tool | Answers |
|---|---|
| `folio_documents` | Every document under a folder, with its kind |
| `folio_document` | A document's blocks with their ids, its kind and fields, and the data it reads |
| `folio_query` | One `SELECT`, run from a folder |
| `folio_embed` | What a reference written in a document reads |
| `folio_kinds` | The declarations applying at a path, and the kinds, rules and health entries they layer to |
| `folio_health` | Everything wrong in the folder, or with `path` in a document or under a folder |
| `folio_used_by` | The documents including a file, or reading its data |
| `folio_provenance` | Where one block came from |
| `folio_related` | What other documents say the same as a block, or answer a question, by meaning; a block the page does not hold is refused |
| `folio_history` | A document's versions; a version's text, each text a block has had, or each result an embed has shown |
| `folio_digest` | Every document created, changed or removed in a period, and every value that moved; `from` and `to` are ISO 8601 dates or times, a date alone starting at midnight UTC |
| `folio_needs` | What needs the reader: errors, problems in documents they read, attention rows and changes; with `path`, what lies there |
| `folio_presence` | The page in each open tab and the block under the reader's pointer |
| `folio_reads` | What the reader has read, per document or per block |
| `folio_changes` | The documents the reader read that changed since; with `path`, those there |
| `folio_stale` | Documents that have probably outlived their use; with `path`, those there |

The reader is the person reading the folder in their browser, usually the user you work for. Call `folio_presence`, `folio_reads`, `folio_changes`, `folio_needs` and `folio_stale` only when the user's request is about what they see, have read or must catch up on, or to fit a report to what they have not read yet - never for anything else. While the reader has paused sharing, these five answer only that sharing is paused.
