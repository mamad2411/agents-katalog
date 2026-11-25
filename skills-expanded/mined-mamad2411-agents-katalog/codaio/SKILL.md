---
name: codaio
description: >-
  Interact with Coda documents, tables, rows, pages, and formulas using the
  codaio CLI. Use this skill whenever the user mentions Coda, coda.io, a Coda
  doc, Coda table, or wants to read/write/export data from Coda — even if they
  don't explicitly say "codaio". Do not call the Coda REST API directly with
  curl or fetch; codaio handles authentication, pagination, rate limiting, and
  error formatting automatically. Use this skill for: reading rows from a Coda
  table, writing or upserting data, exporting pages to markdown, listing docs,
  discovering table schemas, and any other Coda-related data task.
---

# codaio CLI

Interact with Coda via the `codaio` CLI. Output is JSON by default — pipe to
`jq` or use directly in agent workflows.

## Installation

Run directly without installing (recommended for agents — always gets latest):

```bash
npx codaio@latest <command>
```

Or install globally:

```bash
npm install -g codaio
codaio <command>
```

Both forms work identically. Use `npx codaio@latest` unless you've already
confirmed a global install is present and up to date.

---

## Authentication

`CODA_API_TOKEN` environment variable is checked first and is the clearest
choice for automation. If it is not set, the CLI also falls back to the token
saved by `codaio login` in `~/.config/codaio/config.json`, so `codaio`
commands can authenticate even when raw `curl` or other shell tools do not see
`CODA_API_TOKEN`. Generate a token at https://coda.io/account.

```bash
export CODA_API_TOKEN=your_token_here
npx codaio@latest whoami   # verify it works
```

`codaio login` is available for interactive (human) use — it prompts for a
token and stores it at `~/.config/codaio/config.json`. Don't use it from agent
scripts; it requires a TTY. Reusing config that a human already created is
fine.

---

## Workflow: Discover Doc Structure

Before reading or writing, you usually need to find the right IDs. Start broad
and narrow down:

```bash
# 1. List all accessible docs
npx codaio@latest docs list --all

# 2. Find tables in a doc (use the doc ID from step 1, or extract from URL)
#    URL: https://coda.io/d/My-Doc_dAbCdEf123  →  API docId = AbCdEf123
#    Full browser URLs also work anywhere the CLI accepts a docId.
npx codaio@latest tables list <docId> --all

# 3. See columns in a table
npx codaio@latest columns list <docId> <tableIdOrName> --all --visible-only
```

**Always use `--use-column-names`** when reading rows — without it, row data
comes back with opaque column IDs like `c-abc123` instead of `Name`.

---

## Workflow: Read Data

```bash
# List all rows (with human-readable column names)
npx codaio@latest rows list <docId> <tableIdOrName> --all --use-column-names

# Filter rows by column value
npx codaio@latest rows list <docId> <tableIdOrName> --all --use-column-names \
  --query "Status:In Progress"

# Get simplified values (strips formula details, returns plain scalars)
npx codaio@latest rows list <docId> <tableIdOrName> --all --use-column-names \
  --value-format simple

# Get a single row by ID or name
npx codaio@latest rows get <docId> <tableIdOrName> <rowIdOrName> --use-column-names

# Sort options: createdAt, updatedAt, natural
npx codaio@latest rows list <docId> <tableIdOrName> --sort-by createdAt --all \
  --use-column-names
```

---

## Workflow: Write Data

### Insert or upsert rows

`--cells` takes a JSON array of `{column, value}` objects. Pass `--key-columns`
to enable upsert behavior — if an existing row matches on those columns, it gets
updated instead of a new row being created.

```bash
# Insert a single row
npx codaio@latest rows upsert <docId> <tableIdOrName> \
  --cells '[{"column":"Name","value":"Alice"},{"column":"Status","value":"Active"}]'

# Upsert: update if Name matches, insert if not
npx codaio@latest rows upsert <docId> <tableIdOrName> \
  --cells '[{"column":"Name","value":"Alice"},{"column":"Score","value":42}]' \
  --key-columns Name

# Insert multiple rows at once (array of arrays)
npx codaio@latest rows upsert <docId> <tableIdOrName> \
  --cells '[[{"column":"Name","value":"Alice"}],[{"column":"Name","value":"Bob"}]]'
```

### Update a specific row

```bash
npx codaio@latest rows update <docId> <tableIdOrName> <rowIdOrName> \
  --cells '[{"column":"Status","value":"Done"}]'
```

### Delete rows

```bash
# Delete by row IDs (comma-separated)
npx codaio@latest rows delete <docId> <tableIdOrName> \
  --row-ids i-abc123,i-def456
```

---

## Workflow: Pages & Export

```bash
# List pages in a doc
npx codaio@latest pages list <docId> --all

# Get a page
npx codaio@latest pages get <docId> <pageIdOrName>

# Update page metadata
npx codaio@latest pages update <docId> <pageIdOrName> \
  --name "New Title" --subtitle "A subtitle"

# Export to Markdown (async — CLI polls until done)
npx codaio@latest pages export <docId> <pageIdOrName> \
  --output-format markdown

# Export to HTML
npx codaio@latest pages export <docId> <pageIdOrName> \
  --output-format html
```

Export is async under the hood; the CLI handles polling with a default 60s
timeout (override with `--timeout <seconds>`).

---

## Workflow: Formulas & Controls

```bash
# List formulas (named calculated values)
npx codaio@latest formulas list <docId> --all
npx codaio@latest formulas get <docId> <formulaIdOrName>

# List controls (buttons, sliders, etc.)
npx codaio@latest controls list <docId> --all
npx codaio@latest controls get <docId> <controlIdOrName>
```

---

## Command Quick Reference

| Command | Args | Key Options |
|---------|------|-------------|
| `docs list` | — | `--query`, `--is-owner`, `--is-starred`, `--all` |
| `docs get` | `<docId>` | — |
| `docs create` | — | `--title` (required), `--source-doc`, `--folder-id` |
| `docs delete` | `<docId>` | — |
| `tables list` | `<docId>` | `--all`, `--table-types` |
| `tables get` | `<docId> <tableIdOrName>` | — |
| `columns list` | `<docId> <tableIdOrName>` | `--visible-only`, `--all` |
| `rows list` | `<docId> <tableIdOrName>` | `--query`, `--use-column-names`, `--value-format`, `--sort-by`, `--all` |
| `rows get` | `<docId> <tableIdOrName> <rowIdOrName>` | `--use-column-names`, `--value-format` |
| `rows upsert` | `<docId> <tableIdOrName>` | `--cells` (required), `--key-columns`, `--disable-parsing` |
| `rows update` | `<docId> <tableIdOrName> <rowIdOrName>` | `--cells` (required) |
| `rows delete` | `<docId> <tableIdOrName>` | `--row-ids` (required) |
| `pages list` | `<docId>` | `--all` |
| `pages get` | `<docId> <pageIdOrName>` | — |
| `pages update` | `<docId> <pageIdOrName>` | `--name`, `--subtitle`, `--icon-name`, `--image-url`, `--is-hidden` |
| `pages export` | `<docId> <pageIdOrName>` | `--output-format` (required: `html`\|`markdown`), `--timeout` |
| `formulas list` | `<docId>` | `--all` |
| `formulas get` | `<docId> <formulaIdOrName>` | — |
| `controls list` | `<docId>` | `--all` |
| `controls get` | `<docId> <controlIdOrName>` | — |

---

## Output Format

All commands default to JSON — ideal for agents and `jq` piping:

```bash
npx codaio@latest docs list | jq '.[].name'
```

For human-readable output:

```bash
npx codaio@latest docs list --format table
```

`--format` is a global option; it can go before or after the subcommand:

```bash
# Both work:
npx codaio@latest --format table docs list
npx codaio@latest docs list --format table
```

---

## Error Handling

| Status | Meaning | What to do |
|--------|---------|------------|
| 401 | Token missing or invalid | Check `CODA_API_TOKEN`; run `codaio whoami` to verify |
| 403 | Token lacks permission | Token owner doesn't have access to this doc/table |
| 404 | Wrong ID, browser-prefixed doc ID, or name | Re-run `list` to find the correct API ID/name |
| 429 | Rate limited | Wait before retrying — CLI retries automatically (3 attempts) |

---

## Common Mistakes

**Forgetting `--use-column-names`** — without it, rows come back with `c-abc123`
style column IDs. Always add this flag when reading row data.

**Wrong `--cells` format** — cells must be a JSON array of objects, not an
object or a string:
```bash
# Wrong
--cells '{"Name":"Alice"}'

# Right
--cells '[{"column":"Name","value":"Alice"}]'
```

**Missing `--all`** — list commands default to 25 results per page. If you need
all rows, always pass `--all`.

**Quoting names with spaces** — table and column names with spaces must be
quoted:
```bash
npx codaio@latest rows list dAbCdEf "My Table" --all --use-column-names
```

**`--key-columns` enables upsert** — if you pass `--key-columns`, rows matching
on those columns will be updated, not inserted. Omit it if you always want new
rows.

**Extracting doc IDs from URLs** — a Coda URL like
`https://coda.io/d/My-Doc_dAbCdEf123` contains a browser doc segment
`_dAbCdEf123`, but the API doc ID is `AbCdEf123` (without the leading `d`).

**Bare `d...` strings are ambiguous** — the CLI normalizes full browser URLs,
but a raw `dAbCdEf123` input is treated literally. If `docs get dAbCdEf123`
returns 404, use the API doc ID from `docs list --all` (`AbCdEf123`) or pass
the full browser URL instead.
