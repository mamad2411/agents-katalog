---
name: lit-capture
description: Capture scholarly papers met in research conversations into this project's .lit corpus, triage the capture inbox, and answer literature questions from the local corpus before re-searching. Use when a paper with a DOI, arXiv id, OpenAlex W-id, or exact title plus author or year comes up and looks worth keeping, when the user asks to capture, save, or file a paper, or when a literature question may already be answered by the corpus. Not for casual mentions the user has not asked to keep. After capture, drain the paper-brief enrichment queue with --enrich-pending.
---

<!-- Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-lit-memory. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# lit-capture

Run this as a procedure. The corpus lives in `.lit/` at the root of the current
project repo and is git-tracked there. The script `lit_fetch.py` is the only
component that touches the network. It requests `api.openalex.org` over HTTPS
and rejects a response whose final host is not that host.
Everything else is agent reading and writing.

Invoke the script by its installed path so no PATH setup is needed:

```bash
python "$HOME/.zcode/skills/lit-capture/lit_fetch.py" --status
```

Common flags: `--dir <path>` (corpus root, default `.lit`; always run from the
repo root), `--api-key <key>` (default env `OPENALEX_API_KEY`).

## Prerequisites

- Python 3.9+ (standard library only; no pip packages) reachable as `python`.
- Network access to `api.openalex.org`. Singleton DOI and W-id lookups are
  free; title searches, batches, and inbox triage draw on a daily budget, so
  set `OPENALEX_API_KEY` (from OpenAlex) for the full budget.
- The script ships inside this skill folder. The default install is ZCode
  (`~/.zcode/skills/lit-capture/lit_fetch.py`); on other hosts substitute
  that host's installed path (for example
  `~/.claude/skills/jgs/lit-capture/lit_fetch.py` or
  `~/.gemini/extensions/jgs-lit-capture/lit_fetch.py`).

## When to use

A paper enters the conversation with enough identity to fetch (DOI, arXiv id,
W-id, or exact title plus author and/or year) and looks worth keeping. Capture
takes under a minute and never leaves the chat.

## Extract, do not fetch blindly

Scan the conversation for DOIs (`10.xxxx/...`), arXiv ids, OpenAlex W-ids, and
full titles. This is agent-driven reading, not code-based NLP; the script never
parses prose. Dedupe against the corpus before capture: read the generated
`.lit/SKILL.md` for counts and last-synced, then grep `papers/` for the
identifiers you found.

## Capture offline first

Append one JSONL line per item to `.lit/inbox.jsonl`. The `ref` grammar is
exactly one of:

```json
{"ref": "doi:10.1038/nature12373"}
{"ref": "W2741809807"}
{"ref": "arxiv:2401.12345", "title": "<verbatim title>"}
{"ref": "title:<verbatim title>"}
```

Title-form and arxiv-form entries also carry `"title"` (verbatim), plus
optional `"author"` (surname) and `"year"`. Every entry carries `"note"` (why
it came up) and `"added_at"` (ISO timestamp). This works with no network and
survives the session.

## Fetch now when online

With user consent or standing habit, run the script per item, or as one batch:

```bash
python "$HOME/.zcode/skills/lit-capture/lit_fetch.py" --ids "W2741809807|W2100837265"
python "$HOME/.zcode/skills/lit-capture/lit_fetch.py" --doi 10.1038/nature12373
python "$HOME/.zcode/skills/lit-capture/lit_fetch.py" --title "Exact Title" --author Surname --year 2024
```

Report the `written=N skipped=M failed=K` summary block to the user. Then stage
the capture: `git add .lit`.

Title searches and batches are budgeted calls; without an API key the script
warns and draws on the small keyless daily budget. Singleton DOI and W-id
lookups are free.

## When OpenAlex is unavailable

Failure signs: `--check` exits non-zero, the summary reads "budget
exhausted", or a failure reason reads "backoff exhausted after 5 attempts".
Causes are the spent keyless daily budget, an OpenAlex outage, or no
network. Completed writes always stand; nothing half-written needs cleanup.

The script never falls back to another metadata source by design: the
corpus is keyed on canonical OpenAlex W-ids. The fallback is agent work,
in this order:

1. Run `--check` to separate "OpenAlex is down" from "today's budget is
   spent".
2. Tell the user what failed and suggest the fix: get a free OpenAlex API
   key and set `OPENALEX_API_KEY` (or pass `--api-key`). The key lifts the
   budget on title searches, batches, and inbox triage; singleton DOI and
   W-id lookups stay free either way.
3. If the user wants the paper now, fetch it directly from the open web and
   leave the corpus write for later: download the PDF from arXiv
   (`https://arxiv.org/pdf/<arxiv-id>`), resolve the DOI landing page
   (`https://doi.org/<doi>`), or take metadata from the arXiv Atom API
   (`https://export.arxiv.org/api/query?id_list=<arxiv-id>`) or Crossref
   (`https://api.crossref.org/works/<doi>`), then read the paper in-chat.
   An optional `findings/<YYYY>-<slug>.md` entry can hold what was learned.
4. Never hand-write `papers/<W-id>.json` or a brief with an invented id;
   made-up ids break dedupe, the citation graph, and brief writes. Queue
   the paper offline in `.lit/inbox.jsonl` instead (Capture offline first).
5. When OpenAlex answers again (key set, budget reset, outage over), run
   `--inbox`, then `--enrich-pending` as usual. Re-runs are idempotent
   through skip-if-exists.

## Paper briefs

Every captured paper gets an analysis brief sidecar at
`.lit/briefs/<W-id>.json`. The script creates a `pending` stub automatically
when a paper is first written. Briefs are the rationale layer: what the paper
claims, how it was tested, its limits, and why it matters here. Bib metadata
stays in `papers/`; the script owns stubs, validation, and stamps; the agent
authors brief content. The Python script never calls an LLM.

Drain the enrichment queue after every successful capture, and at the start
of any lit work:

```bash
python "$HOME/.zcode/skills/lit-capture/lit_fetch.py" --enrich-pending
```

For each listed id (keep it to about three per turn; the rest stay queued):

1. Read `.lit/papers/<id>.json`.
2. Use fulltext when clearly available (a local file or a readable OA URL in
   the paper record); otherwise the abstract. Set each claim's `basis`
   honestly; the script derives the brief's top-level `basis`.
3. Draft the full brief JSON per the schema in the stub: overview, claims
   (in-paper argument graph only: `supports` / `contradicts` point at claim
   ids inside this same brief), methods_tests, limits, why_it_matters,
   related_in_corpus, open_questions. Unknown `page` / `section` stay null.
4. Write it through the script, never a hand edit:

```bash
python "$HOME/.zcode/skills/lit-capture/lit_fetch.py" --brief-write --id W123 --file brief.json
```

   Add `--human` only when the user dictated human notes this turn, and
   include a `human` block in the payload then. Every other write replaces
   the `agent` block and preserves `human`.

5. Check what you wrote and fix failures before finishing the turn:

```bash
python "$HOME/.zcode/skills/lit-capture/lit_fetch.py" --brief-check
```

6. Run the quality gate and fix every FAIL line before committing:

```bash
python "$HOME/.zcode/skills/lit-capture/lit_fetch.py" --audit
```

   The bar per paper: status `ready`; at least three claims; at least one
   open question; at least one `related_in_corpus` link to another paper
   in the corpus. When the paper record has an `oa_url`, read the full text.
   If that download fails, start `notes` with `fulltext-unavailable:` and
   name what failed; never edit or clear `oa_url` to get past the gate.
   Without an `oa_url`, abstract basis passes only with `notes` that say why
   full text was unavailable (paywalled, no preprint). A claim's basis is
   `fulltext` only when the claim was read in the full text. Two
   records with the same title are one work in two versions, such as a
   preprint and the published paper. Keep the published version and fold
   the other into it with
   `--merge W-old --into W-kept`. An inbox entry that cannot resolve must be
   fixed (DOI or W-id) or deleted; the gate fails while the inbox holds
   anything.

7. `git add .lit` together with papers and edges as today.

Honesty constraints: do not invent pages, tests, or results absent from the
source basis; prefer claim `confidence` of `low` or `med` for abstract-only
fills; never mint cross-paper claim ids; do not clear `human.*` unless the
user dictated human notes this turn.

Reset an agent block for a fresh re-enrich (basis upgrade to fulltext is a
good reason):

```bash
python "$HOME/.zcode/skills/lit-capture/lit_fetch.py" --brief-restub --id W123
```

`findings/*.md` stays an optional human diary; briefs do not require one.

## Findings stub (optional)

For papers worth a note, write `findings/<YYYY>-<slug>.md` from this template:

```markdown
# <paper title>

- W-id: <W-id>
- Captured: <YYYY-MM-DD>, why: <one line on why it came up>
- Claim worth remembering: <one sentence>
```

Prose in findings follows the Written Prose Standard: lead with the finding,
no em dashes, no filler.

## Triage

Periodically run:

```bash
python "$HOME/.zcode/skills/lit-capture/lit_fetch.py" --inbox
```

Title-form and arxiv-form entries resolve through their `"title"` field
(arXiv entries get theirs from the paper as captured); supply `"author"` and
`"year"` to disambiguate. Drop entries no longer wanted by deleting their
lines. Failures stay queued with their reason in `last_error`; fix the entry
or delete it, then re-run.

## Query the corpus

Read `.lit/SKILL.md` first each session (counts, recipes, last-synced), then
answer literature questions from briefs, papers, and `graph/edges.jsonl`
before re-searching the web. For a paper already in scope, read its brief
first: prefer `human.*` when non-null, and the human claims array replaces
the agent claims array only when it holds at least one claim with text.
Then the paper record, then the edges. The index carries copy-pasteable
recipes: title grep, boundary ID extraction, edges per paper, papers citing
a given W-id.

## Limits

Abstracts are often null (OpenAlex stores them only as an inverted index and
only for roughly half of works). Use the corpus for identity, graph, and
retrieval, not as a full-text store. `referenced_works` is lossy relative to
printed reference lists; treat the graph as biased, not authoritative.
