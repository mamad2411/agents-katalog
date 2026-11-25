---
name: hkdata
description: >
  Use when the user asks about Hong Kong government open data, statistics, or
  datasets — e.g. transport, weather, population, employment, finance, health,
  education, housing, crime, tourism, facilities, etc. — in English or Chinese.
  Queries data.gov.hk and returns sourced, live answers, or an honest "no dataset".
compatibility: Requires python3 + chromadb for search/embed (see SETUP.md); needs a reachable embedding backend — Ollama by default, or any backend via the Embedder interface (see SETUP.md "Integrating a new backend").
license: MIT
---

# 港數通 · hkdata — Hong Kong Open Data Library

**Scope: Hong Kong data.gov.hk datasets only.** General web search, non-HK data,
or non-government sources are handled by the agent's native web search tools, not
this skill.

## Resolve the skill root once

The commands below use `$SKILL_DIR`; resolve it before the first call (the docs
never assume a runtime's install directory):

```bash
: "${SKILL_DIR:=$(for d in "${HKDATA_SKILL_DIR:-}" "$HOME/.agents/skills/hkdata" \
    "$PWD/.agents/skills/hkdata" "$HOME/.claude/skills/hkdata" \
    "$HOME/.config/agents/skills/hkdata" "$PWD"; do [ -f "$d/hk.sh" ] && { echo "$d"; break; }; done)}"
[ -n "$SKILL_DIR" ] || { echo "hkdata: set HKDATA_SKILL_DIR to the dir containing hk.sh" >&2; exit 1; }
```

The wrapper is cwd-safe (it resolves its own root) and picks the venv
interpreter when present, else `python3`. From the skill directory itself,
`bash ./hk.sh <subcommand> …` works the same way.

## You are a coding agent with a library of reusable programs

This skill gives you a growing library of **runnable, docstring-documented
functions** under `programs/` — each one a **reusable capability over one
data.gov.hk API/dataset**, grouped by department/org. Each function returns
JSON-serializable data (it never prints); its docstring says what data it
provides, its dataset ID, endpoints, and quirks.

**A program answers a *class* of questions, not one specific question.**
`address_lookup(q)` is the reusable capability; "where is the Housing Authority
headquarters?" is a query you answer *with* it. Write a program only when you
find a dataset/API that a whole family of future questions will need — never for
a single concrete fact.

### Think in programs before you search

When a question arrives, first decompose it: **what program / function / API /
dataset would produce this answer?** Then retrieve those primitives and compose
them, rather than reaching for web search or a one-off:

```text
"what's the Housing Authority HQ address, and the bus from Un Chau Estate?"
    → address_lookup("Housing Authority Headquarters")   # geocode → 33 Fat Kwong St
    → kmb_routes()                                        # find Cheung Sha Wan → Ho Man Tin (route 18)
```

A specific fact (an address, a coordinate, a route) is usually *retrievable
through an existing primitive* — compose your programs first. Only fall through
to exploration (Path B) when no program or catalog dataset can produce it.

Answer a question in **two paths**, not a fixed set of steps:

### Path A — a program already covers it (fast, repeatable)

```bash
bash "$SKILL_DIR/hk.sh" programs-search "<user query>"
```

Retrieve the top-k functions (bilingual semantic + keyword). If one covers the
question, **run its source in the skill venv** — no file I/O:

```bash
bash "$SKILL_DIR/hk.sh" python - <<'EOF'
<paste the returned source, then call it>
EOF
```

`hk.sh python` is the venv interpreter (`requests` / `pandas` / `lxml` /
`feedparser` live there), so the same paste runs a 4-line CSV fetcher and a
workbook reader alike. Compose when needed: `function_a(...) +
new_function_b(...)`, all in that throwaway heredoc.

### Path B — nothing covers it (discover → answer → remember)

```bash
bash "$SKILL_DIR/hk.sh" catalog-search "<query>"    # discovery over all ~3,822 datasets
bash "$SKILL_DIR/hk.sh" info "<dataset-id>"          # metadata + endpoint URLs
bash "$SKILL_DIR/hk.sh" test "<endpoint-url>"        # fetch + detect JSON/XML/CSV
```

Three steps, in this order:

1. **Discover** — `catalog-search` → `info` → `test`. Seconds.
2. **Answer now** — fetch the data and answer, per the answer contract.
3. **Remember** — write the working recipe as a reusable function (a whole
   class of questions, not this one instance) under `programs/<org>/<file>.py`
   (copy `programs/_template.py` for the docstring contract), then index it:
   ```bash
   bash "$SKILL_DIR/hk.sh" reindex
   ```
   That makes the *next* similar question a Path-A hit — the learning loop.

**The answer never waits for step 3.** The program is a *memory* for the next
question, not a prerequisite for this one: step 3 only pays off later, while
the user is waiting for the answer now. Fetch the data for step 2 with `test`
or a throwaway snippet — don't delay the answer by writing the function first.
Do step 3 in the same turn, after the answer, and close with one line naming
the file and that it was indexed.

## Write efficient programs — don't reinvent the wheel

Programs run in the skill venv (Python 3.11+), not a restricted sandbox. Use the
mainstream library for the job instead of hand-rolling the parser or the client:

| Task | Use | Don't |
|---|---|---|
| HTTP (one call or many) | `requests` (`timeout=`, `.raise_for_status()`) | `urllib.request` + hand-built headers |
| CSV / XLSX / joins / groupby | `pandas` (`read_csv`, `read_excel`, `merge`, `groupby`) | `csv.DictReader` loops, unzipping XLSX by hand |
| HTML tables / scraped pages | `lxml.html` (or `pandas.read_html`) | `re.findall(r"<td>…")` |
| RSS / Atom feeds | `feedparser` (incl. RFC-822 dates) | regex over `<item>` + `strptime` |
| JSON APIs | `resp.json()` | `json.loads(resp.read().decode())` |

Rules that keep a program reusable:

- **Imports go inside the function.** The source is pasted verbatim, so it must
  import everything it uses.
- **Helpers in the same file are fine.** `reindex` inlines the module-level
  private functions/constants a program references, so the stored source stays
  runnable. Never import from another `programs/` module — that cannot be
  inlined; duplicate the few lines instead.
- **Return JSON-serializable data** — `.to_dict("records")`, empty cells as
  `None` (not `NaN`), never a DataFrame, never `print()`.
- **One function = one capability** — a family of future questions, not one fact.

Spreadsheet resources (`xlsx`/`xls`, ~1,400 datasets) have no JSON endpoint:
call `xlsx_preview(url)` to find the header row, then `xlsx_rows(url, header=n)`.

## Program docstring contract

Every function's docstring is both the retrieval surface and the reading surface.
Lead with **what the data provides**, then coverage, then the mechanics. The full
contract with a copyable example is in [`programs/_template.py`](programs/_template.py).
Required sections: `Provides`, `Coverage`, `Datasets`, `Department`, `Endpoint`,
`Usage`, `Questions`, `Quirks`. `Questions` lists example natural-language queries
and is the main retrieval aid — a reworded query should still hit the right
function.

## Command summary

| Command | Purpose |
|---------|---------|
| `programs-search "<query>" [--source] [--json]` | Semantic search over runnable functions; `--source` prints full source (Path A) |
| `python [args…]` | Run the skill venv interpreter — `bash hk.sh python - <<'EOF'` runs pasted program source |
| `reindex` | Extract + embed functions from `programs/`, render the registry |
| `programs-status` | Program file/function count + vector-store state |
| `catalog-search "<query>"` | ChromaDB search over the full catalog (Path B discovery) |
| `info "<id>"` | CKAN `package_show` metadata (Path B) |
| `test "<url>"` | Test endpoint and detect format (Path B) |
| `embed-status` | Active embedding backend + store match (catalog, programs) |

Full CLI list (catalog build/refresh) in [`README.md`](README.md).

## Auto-fallback and no-dataset contract

When `programs-search` and `catalog-search` both return nothing useful, web search
`site:data.gov.hk <topic>`. If Path B reveals **no dataset answers the query**,
your answer MUST:

1. State clearly: "No suitable dataset found on data.gov.hk"
2. Include an exploration log listing each dataset examined and why it didn't fit
3. If a proxy exists, use it with an explicit caveat

**A department's own web app is not a dataset miss.** If no dataset exists but
the department publishes the data on its site (an RSS feed, a JSON endpoint, a
catalogue page), use that source — and label it as scraped, with the URL and
the reason there is no dataset. Example: the HKPL catalogue's per-branch
loan status is not an open dataset, but it is the authoritative answer.

## Answer contract (when a program answers)

Every successful answer MUST include, alongside the direct answer:

1. **Dataset ID** (and the source department) — so the claim is re-checkable.
   If the figures come from a department's **web app rather than an open
   dataset** (scraped HTML, an undocumented feed), say so explicitly:
   *"no open dataset — scraped from the <department> catalogue"* and give the
   URL. A scraped figure is weaker evidence than a published one, and the
   user needs to know which they are getting.
2. **Endpoint** actually queried (URL).
3. **Data timestamp** of the figures themselves, in **HKT**, distinct from
   "retrieved at" — e.g. "figures are as at 2026-03-13 (HKT)".

When Path B also wrote a program, close with one line naming the file and
that it was indexed — the user should see the loop close without re-reading.

The program's docstring carries the dataset ID and endpoint; the data's own
timestamp comes from the returned records. Presentation: multiple rows → a table;
a trend → a chart (with the source dataset and its temporality labelled). A
procedural/form question ("how do I apply …") is rarely a dataset — data.gov.hk
holds statistics/fee tables, not application steps; redirect to the department's
site and say so rather than reporting a "dataset miss".

## Deeper guidance

- [`references/workflow-guides.md`](references/workflow-guides.md) — response templates, cross-dataset joins, proxy indicators, temporality, error handling, known broken endpoints.
- [`programs/_template.py`](programs/_template.py) — the program docstring contract.
- [`SETUP.md`](SETUP.md) — install, build, and refresh the catalog and vector stores.
