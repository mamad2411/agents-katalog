---
name: cubest
description: >-
  USE WHEN you need a structured OLAP slice of a large codebase, log
  stream (including multi-GB `.gz`), CSV export, sitemap or HTML crawl,
  or an SDD artefact catalog — WITHOUT reading raw file bodies into the
  context window. Single-pass aggregator: streams input, folds records
  into an in-memory cube by user-picked dimensions × measures (count /
  sum / avg / min / max / reservoir-sampled p50/p90/p95/p99), then
  prints one compact artefact in 13 formats: tree / flat (breadcrumb) /
  compact / CSV / md_table / YAML / JSON / XML / GraphViz DOT / Mermaid
  / PlantUML / draw.io XML / interactive ECharts HTML (sunburst,
  treemap, tree, sankey, graph, bar). **Measured 7-22× fewer tokens per
  tool response** across 7 reproducible scenarios (see `examples/`).
  Ships 31 built-in profiles, inline JSON/YAML, `--files-from` for
  `git diff` MR/PR preflight, and `--diff` for CI regression checks
  against a baseline cube. Streaming holds constant memory
  (ΔRSS <200 KiB per 500k lines) — 10 TB of logs is I/O-bound, not RAM.

  Concrete jobs it solves in one call:
  - Onboard a monorepo: file tree × extension × LOC, function inventory
    and approximate call graph across 15 languages
    (`file_tree`, `code_atlas`, `loc_counter`, `call_graph`).
  - PR/MR preflight from `git diff --name-only`: impact map, LOC delta,
    TODO diff; `--diff BEFORE AFTER` compares two cubest JSON dumps and
    emits a Markdown table of leaves that changed — drop-in CI gate
    (`mr_impact`, `tech_debt`, see `examples/ci/`).
  - SRE / on-call log rollup: nginx `access.log` by URL section ×
    status × method × p95 latency, gz-streamed at constant memory
    (`nginx_access`, `nginx_cdn_covers`, `frontend_geoip`,
    `jsonl_events`).
  - SEO / content audit: HTML `title/desc/H1/canonical/schema.org`
    coverage, H1–H6 semantic tree, sitemap.xml URL taxonomy → ECharts
    treemap or sunburst
    (`seo_audit`, `seo_semantic_tree`, `sitemap_map`).
  - CSV / analytics pivot: GA4, Yandex Metrica, Google Ads, Meta Ads
    exports rolled up by campaign × device × p90 (`csv_analytics`).
  - Docs & SDD catalog: markdown headings, checklists (done vs todo),
    YAML frontmatter, spec / PRD / ADR inventory, phase × status ×
    owner (`doc_structure`, `sdd_specs`, `sdd_checklist`,
    `spec_status`).
  - Infra & API surface: Kubernetes manifests by kind × namespace ×
    name, OpenAPI method × path, XML / YAML top-level keys
    (`k8s_resources`, `openapi_endpoints`, `xml_tags`, `yaml_keys`).
  - Codebase health: TODO / FIXME / HACK hotspots, disk usage by
    top-level folder, git-log activity by author × month, Python
    imports, React / Vue components, SQL functions
    (`tech_debt`, `disk_usage`, `git_log_activity`, `imports`,
    `react_components`, `sql_functions`, `api_routes`).
  - Claude Code catalog: subagents (`agents_inventory`) and skills
    (`skills_inventory`) inventory.

  NOT the right tool for: a single-file lookup (use `Read` / `Grep`),
  fetching source lines rather than aggregates, or trees under ~10
  files. Works with Claude Code, Cursor, Codex, Aider, Windsurf, Cline,
  Continue.dev — any AI coding agent billed per input token.

  Triggers: "map the codebase", "onboard this repo", "show project
  structure", "how many where", "all endpoints", "all TODOs", "count
  LOC", "call graph", "PR impact map", "MR preflight", "CI regression
  check", "diff two cubes", "nginx 5xx breakdown", "top endpoints by
  p95", "latency percentiles", "gzipped log rollup", "SEO audit",
  "sitemap taxonomy", "OpenGraph coverage", "H1-H6 semantic tree",
  "CSV pivot", "campaign × device rollup", "GA4 rollup", "K8s
  manifests inventory", "OpenAPI method × path", "SDD spec catalog",
  "checklist progress", "phase × status × owner", "ADR inventory",
  "disk usage by folder", "tech-debt hotspots", "git activity by
  author", "agents inventory", "skills inventory".
---

# cubest — Single-pass OLAP indexer

Scans a directory in one pass, extracts records via regex or presets,
aggregates them into an in-memory OLAP cube, and prints a compact tree.
**Does NOT pull raw file contents into the context** — only aggregates.

## When to call (token economy)

Use `cubest` **instead of**:

- chains of `grep -rn` + `cat` across 20+ files just to figure out what's
  where;
- manual `ls -R` + `wc -l` walks over big trees;
- opening a dozen files to "get a feel for how many endpoints / TODOs /
  components there are";
- "let me open every md just to build a table of contents".

Especially valuable when:

1. **Long refactor / audit loops** where holding context matters — keep
   a compact index in the window instead of raw files.
2. **Unfamiliar monorepo** — first move is `file_tree` + `code_stats`,
   getting the map in one shot.
3. **Recurring health checks** ("how many TODOs now?", "any new routes?")
   — 20-200 lines of output instead of thousands from `grep`.
4. **Planning changes** — before starting, learn the distribution: how
   many files affected, which directories, which extensions.

When **not** needed:

- Single lookup in a specific file — use `Read` / `Grep`.
- You need source lines, not an aggregate — use `Grep` / `Read`.
- Tree smaller than ~10 files — faster to read directly.

## Quick start

```bash
# Project tree: top dirs x extensions (no content read)
python .claude/skills/cubest/cubest.py --profile file_tree .

# FastAPI/Flask HTTP endpoints
python .claude/skills/cubest/cubest.py --profile api_routes ./src

# TODO/FIXME/HACK by kind and file
python .claude/skills/cubest/cubest.py --profile tech_debt .

# Markdown documentation table of contents
python .claude/skills/cubest/cubest.py --profile doc_structure ./docs
```

## Inline profiles

One-line JSON:

```bash
python .claude/skills/cubest/cubest.py \
  --profile '{"dimensions":["kind","file"],"measures":[{"name":"count","type":"count"}],"extract":[{"type":"preset","preset":"funcs"}],"scan":{"include":["*.py"]}}' \
  ./src
```

YAML via stdin:

```bash
cat <<'EOF' | python .claude/skills/cubest/cubest.py --profile - ./src
dimensions: [ext, file]
measures: [{name: count, type: count}]
extract: [{type: preset, preset: paths}]
output: {format: compact}
EOF
```

## Profile schema

```yaml
name: my_profile              # optional
description: "..."            # optional
scan:
  include: ["*.py", "docs/**/*.md"]
  exclude: [".git/", "node_modules/", "*.lock", "!keep.lock"]
dimensions:                   # order = tree hierarchy
  - kind
  - file
measures:
  - name: count
    type: count
  - name: bytes
    type: sum
    field: size
extract:
  - type: preset
    preset: paths | funcs | headers | lines | csv | tsv | md_checklist |
            md_frontmatter | html_meta | html_headings | sitemap | calls
  - type: regex
    pattern: '(?P<status>\d{3})\s+(?P<duration>[0-9.]+)'
    multiline: true
    ignorecase: false
filters:                      # safe eval with len/min/max/any/all
  - "status >= 200"
  - "'test' not in file.lower()"
output:
  format: tree | flat | compact | csv | md_table | yaml | json | xml |
          dot | mermaid | plantuml | drawio | echarts
  top_n: 15
  min_count: 2
```

## Presets (`type: preset`)

| Preset            | Fields on each record                                        | Reads file?     |
|-------------------|--------------------------------------------------------------|-----------------|
| `paths`           | `dir, basename, name, ext, depth, top, size, path_1..path_5` | no              |
| `funcs`           | `kind, name, parent, depth, lang` (15 languages)             | yes             |
| `calls`           | `caller, callee, lang` — approximate call graph              | yes             |
| `headers`         | `level, title` (Markdown)                                    | yes             |
| `lines`           | `line, length, ext, top, name, blank, comment`               | yes             |
| `md_checklist`    | `state` (done/todo), `title`                                 | yes (or stream) |
| `md_frontmatter`  | any `key: value` from YAML frontmatter                       | yes (batch)     |
| `csv` / `tsv`     | every column from header row (slugged names)                 | yes (batch)     |
| `html_meta`       | `title, description, canonical, og_*, h1_count, has_schema…` | yes             |
| `html_headings`   | `level, title` for each H1-H6                                | yes             |
| `sitemap`         | `url, host, path, section_1..3, priority, lastmod`           | yes             |

`paths` — one record per file, works even for empty/binary files; ideal
for tree maps without touching content. `path_1..path_5` are directory
prefixes up to depth N (`path_2 = "src/api"`), useful for disk-usage.

`md_checklist` / `md_frontmatter` — SDD artefacts (specs, PRDs, ADRs,
acceptance checklists, skill / agent catalogs).

## Path filters (`scan.include` / `scan.exclude`) — gitignore-like

Pattern matching rules:

- `*.py`, `README.*` — glob on file basename;
- `docs/**/*.md`, `src/*/api.py` — glob on relative path (`**` = any depth);
- `node_modules/`, `.git/`, `*cache*/` — **entire directory**, pruned at
  walk time (fast);
- `/README.md` — anchored to scan root;
- `!pattern` — negation: keep even if it matched exclude / drop even if it
  matched include.

Default `exclude` (if none specified):
`.git/ node_modules/ __pycache__/ .venv/ venv/ dist/ build/ .claude/ *.lock *.pyc`.

When you override `exclude` in a profile, defaults are **fully replaced**
— re-add the ones you still want.

## Measure types

| Type              | How it's computed                                | Rollup                          |
|-------------------|--------------------------------------------------|---------------------------------|
| `count`           | +1 per record                                    | sum over children               |
| `sum`             | +record[field] per record                        | sum over children               |
| `avg`             | mean of record[field] over records in the leaf   | weighted avg by child counts    |
| `min` / `max`     | leaf min/max of record[field]                    | recursive min/max               |
| `p50/p90/p95/p99` | reservoir-sampled percentile (default k=128)     | proportional-resample merge     |
| `percentile`      | user-defined q (e.g. `q: 0.75`)                  | same                            |

## Output formats

Text / tabular: `tree` (default), `flat` (breadcrumb), `compact`, `csv`,
`md_table` (`md`/`markdown`), `yaml` (`yml`), `json`, `xml`.

Diagrams (dimensions must be `[src, dst]` or deeper):

- `dot` / `graphviz` — DOT syntax, render with `dot -Tsvg`;
- `mermaid` / `mmd` — `flowchart LR`, renders on GitHub/GitLab/Notion/Obsidian;
- `plantuml` / `puml` — `@startuml` component diagram;
- `drawio` / `diagrams` — draw.io / diagrams.net XML (`File → Import`);
- `echarts` / `html` — standalone interactive HTML with 6 switchable
  chart types (sunburst / tree / treemap / sankey / graph / bar), CDN +
  inline data. Pick chart_type via `output.chart_type: auto|sunburst|...`.

Example — get a call graph as Mermaid in one command:
```
python .claude/skills/cubest/cubest.py -p call_graph src/ \
  -p '{"output":{"format":"mermaid","top_n":30}}'
```

## Content-based file filter

Beyond path globs you can require a file to CONTAIN (or NOT contain)
specific regexes — a pre-filter applied before the main extraction:

```yaml
scan:
  content_match: ["TODO", "@deprecated"]   # file must match both
  content_not:   ["generated by tool X"]   # and must not match this
  content_scan_bytes: 65536                # scan only first 64 KiB
```

Useful for disk-usage: "show size only for folders that contain TODO files".

## CLI flags

```
--profile / -p    built-in name | file path | inline JSON/YAML | '-' (stdin)
--files-from / -F stdin/file list of paths (MR/PR workflow with git diff)
--diff BEFORE AFTER  compare two cubest JSON dumps → md-table of changed
                     leaves (drop-in CI regression gate; see examples/ci/)
--verbose / -v    print "# scanned N files, M records" on stderr
path              scan root or a single file (auto-detects `.gz`)
```

## Install

The script needs only the standard library. `PyYAML` is optional (for YAML
profiles / YAML output). JSON profiles work with no dependencies.

```bash
pip install -r requirements.txt        # with pip
uv pip install -r requirements.txt     # with uv
uv run --with pyyaml cubest.py -p file_tree .   # ad-hoc via uv, no venv
```

## Tests

```bash
python3 .claude/skills/cubest/tests/run_tests.py     # 57 unit tests
python3 .claude/skills/cubest/tests/bench.py         # quick load test
HEAVY=1 python3 .claude/skills/cubest/tests/bench.py # heavy: 5M records
```

Bench targets: >100k rec/s on insert, gzip streaming keeps
**constant memory** (ΔRSS <200 KiB per 500k lines) — this is what lets
terabyte logs process without OOM.

See [README.md](README.md) for full use cases, cookbook and comparison
with related tools.
