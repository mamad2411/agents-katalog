---
name: scholar-lab-radar
description: >-
  Profile a research lab (a professor, or a school/department) over the last N years
  by collecting every paper from OpenAlex, structuring it into a temporal knowledge
  graph (ontology) — Papers, Researchers, Topics, Themes, Methods, Venues, Citations —
  and synthesizing a grounded report of the lab's year-by-year output and shift in
  focus ("기조 변화"). Resolve → collect → build graph → metrics → tag themes →
  synthesize. Use when the user wants to understand a lab/PI's body of work, its
  evolution, its members, or to vet/compare labs. Triggers: "profile this lab",
  "research group analysis", "what does <professor>'s lab work on", "lab trend report",
  "연구실 분석", "이 교수 연구실 논문 흐름", "지도교수/랩 비교". Localized phrases map
  to the same intent.
---

# scholar-lab-radar

Turns one lab (a PI, or a school/department) into a **temporal knowledge graph** of its
output and a grounded evolution report. Sibling to `scholar-megasearch`: free structured
scholarly APIs (**OpenAlex**-first) + LLM only on the semantic layer. The data layer is
deterministic Python (reproducible); the LLM names research themes/methods and writes the
narrative — always grounded in the graph's counts, never invented.

Default install locations:

- Claude Code: `~/.claude/skills/scholar-lab-radar`, venv not required (scripts are stdlib).
- Codex: `~/.agents/skills/scholar-lab-radar`.

Use the skill directory from the loaded skill path for bundled scripts (`<skill-dir>/scripts`).
The full ontology schema is in `references/ontology.md`; the data sources and exact
OpenAlex queries are in `references/sources.md`.

## Modes

- **professor** *(default, cleanest)* — corpus = the confirmed PI's authored works.
- **lab** — PI + inferred members' works (co-author expansion).
- **department** — an institution + topic scoping (broad; noisier).
- **compare** — two labs side by side (e.g. an applicant comparing advisors).
- **applicant** — a lab + the user's interests → alignment + who to contact.

All modes reuse the same pipeline (resolve → collect → graph → tag → infer → analyze → synthesize).

### Mode recipes
- **lab** — run professor mode first, then take the `likely_member` ids from `data/roster.csv`
  and re-collect with the PI **and** members in one corpus, then rebuild:
  `collect.py --author <PI> --author <M1> --author <M2> … -o ./labs/<slug>-lab`.
- **compare** — profile two labs into separate dirs, then
  `compare.py ./labs/<a> ./labs/<b> -o ./labs/<a>-vs-<b>.md` (productivity, shared vs
  distinctive topics, each lab's focus shift, overlapping collaborators).
- **applicant** — profile the lab, then match the user's stated interests against the lab's
  Themes/Topics (`metrics.json`) and recommend **which member to contact** — the recent
  first-author or `advised_by`/theme owner of the matching thread.
- **department** — collect by institution + topic instead of author
  (`/works?filter=authorships.institutions.id:<I>,topics.id:<T>,from/to_publication_date`);
  broader and noisier, so scope tightly and caveat heavily.

## Workflow

### 1. Resolve the lab — the make-or-break step
Author disambiguation decides whether the report is about the right person, so **confirm
the OpenAlex id with the user** before collecting. Prefer ORCID.
```bash
python3 <skill-dir>/scripts/resolve.py institution "<school>" --mailto <email>
python3 <skill-dir>/scripts/resolve.py author "<name>" --institution <instId> --mailto <email>
python3 <skill-dir>/scripts/resolve.py author "<name>" --orcid 0000-... --mailto <email>
```
Present the candidates (name, ORCID, institution, works/cites, recent titles) and ask the
user to pick the id — **merge several ids** if OpenAlex split the person. Also confirm the
**year range** (default: last 5 years) and **mode**.

### 2. Collect the corpus
```bash
python3 <skill-dir>/scripts/collect.py --author <id> [--author <id2>] \
  --from <Y1> --to <Y2> -o ./labs/<slug> --mailto <email>
```
Fetches every work in range via cursor paging, reconstructs abstracts, dedupes by
DOI → OpenAlex id → normalized title, and writes `labs/<slug>/works.jsonl` + `meta.json`.
Use `--institution <id>` to scope to works produced while at that institution; `--max N`
to cap a very prolific PI. The sweep **checkpoints after every page**, so an interrupted
run (dropped network, exhausted retries, Ctrl-C) resumes from the last saved cursor when
you rerun the same command — no re-fetching what's already on disk. Pass `--fresh` to
ignore the checkpoint and re-sweep from scratch.

### 3. Build the knowledge graph (ontology)
```bash
python3 <skill-dir>/scripts/build_graph.py ./labs/<slug>
```
Emits `graph/entities.jsonl` + `graph/relations.jsonl` — typed, time-stamped: Paper /
Researcher / Topic / Venue / Institution / Funder nodes, and `authored_by · has_topic ·
published_in · funded_by · cites(internal) · collaborates_with(PI ego)` edges. Member
roster (role, active span, first-author count) is computed here. No LLM.

### 4. Compute metrics + structured report
```bash
python3 <skill-dir>/scripts/analyze.py ./labs/<slug>
```
Writes `metrics.json`, `data/{topics_by_year.csv, roster.csv}`, `index.md` (dashboard),
and `report.md` (structured draft): papers/citations per year, topic×year matrix,
**focus-shift detection** (early vs late primary-topic share, with counts), roster,
rising members, collaboration growth, top venues, notable papers. Every number is
grounded — the narrative must cite these counts.

### 5. Semantic layer — tag Themes / Methods / Datasets (LLM, fan-out)
Fan out over `works.jsonl` (megasearch-style) and, from each paper's title+abstract,
extract lab-specific **Themes** (finer threads on top of OpenAlex Topics), **Methods**,
and **Datasets**, plus a one-line summary. **Canonicalize across the whole corpus** before
writing — reuse one `slug` per concept so "CNN" and "convolutional neural network" collapse
to the same Method, and cluster near-duplicate themes. Write one record per paper to
`labs/<slug>/tags.jsonl`:
```json
{"id":"W123","themes":[{"slug":"contrastive-ssl","label":"Contrastive self-supervised learning"}],
 "methods":[{"slug":"transformer","label":"Transformer","aliases":["self-attention"]}],
 "datasets":[{"slug":"imagenet","label":"ImageNet"}],"summary":"one-line takeaway"}
```
Then merge it into the ontology and emit the per-paper cards + JSON-LD, and re-run analyze
so themes fold into the metrics/report:
```bash
python3 <skill-dir>/scripts/tag_ingest.py   ./labs/<slug>   # +Theme/Method/Dataset, papers/*.md
python3 <skill-dir>/scripts/infer.py        ./labs/<slug>   # structural advised_by + method diffusion
python3 <skill-dir>/scripts/export_jsonld.py ./labs/<slug>   # graph/ontology.jsonld
python3 <skill-dir>/scripts/analyze.py       ./labs/<slug>   # theme×year + theme focus-shift
```
`infer.py` adds the structural inferred edges (`advised_by` from recurring member-first /
PI-last co-authorship + shared institution; `diffused_to` from Method×Theme co-occurrence).
Theme lineage (`evolved_from`) is LLM-judged — append it to `graph/relations.jsonl` with
`confidence: llm` (see `references/ontology.md`).

### 6. Synthesize the report
Rewrite `report.md` into the final narrative grounded in `metrics.json` + the graph:
exec summary, year-by-year flow, **기조 변화** (cite the emerging/declining counts),
Theme lineage + which members carried each thread, method/dataset evolution, member
dynamics (rising first-authors, departures), notable papers, collaboration evolution,
and an honest **Caveats** section (disambiguation confidence, coverage gaps, small-N).
Never assert a trend without the count behind it.

### 7. (optional) Visualize the graph
```bash
python3 <skill-dir>/scripts/viz.py ./labs/<slug>   # -> labs/<slug>/graph.html
```
Self-contained interactive `graph.html` (vis-network, opens in any browser): nodes colored
by type, sized by degree, with node-type filters and an edge-label toggle. **Click any node**
for a detail panel (attributes, DOI/links, summary, connections). A **year slider + ▶ play**
grows the graph year by year — drag it (or press play) and nodes/edges appear as their
relations come into being, so you watch the lab assemble over time. External one-off
co-authors are hidden by default (`--include-external` to show); `--max-nodes N` caps the
most-connected nodes to avoid a hairball.

## Outputs
Everything lands under `./labs/<slug>/` in the working directory:
```
labs/<slug>/
├── works.jsonl              normalized corpus (one work per line)
├── meta.json               run params + counts
├── graph/{entities,relations}.jsonl   the temporal knowledge graph (ontology)
├── data/{topics_by_year,roster}.csv   spreadsheet-ready matrices
├── papers/<year>-<slug>.md  per-paper tagged metadata (semantic layer)
├── index.md                structured dashboard
├── report.md               synthesized lab report
└── graph.html              interactive node-link viewer (open in a browser)
```

## Honesty
Report what was actually collected and the disambiguation choice. `likely_member` /
`collaborator` / `advised_by` are **inferred** — label them so. Do not invent trends:
small per-year samples are noisy and the counts are shown so a reader can judge. See
memory `feedback_honest_writing`.
