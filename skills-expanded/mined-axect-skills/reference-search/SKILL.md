---
name: reference-search
description: Search and curate academic references for a topic, claim, section, baseline, method, evaluation need, or report section using domain-aware routing across InspireHEP, OpenAlex, and Semantic Scholar, with markdown-ready summaries and optional save paths. Use when the user asks for papers, references, citations, related work, supporting literature, survey papers, background sources, baseline citations, evidence to support a report or research claim, or wants section-by-section citation help while drafting `report.md`.
---

# Reference Search

Use this skill to find and curate literature for research writing, report support, method comparison, or quick topic familiarization.

It is especially useful as a companion to `research-report` when a report section needs external literature support beyond local experiment artifacts.

## Sources and routing

The skill queries three sources via a single CLI:

| Source             | Best for                                                                 |
|--------------------|--------------------------------------------------------------------------|
| **InspireHEP**     | HEP / nuclear / gr-qc / cosmology-overlap papers. Highest precision.     |
| **OpenAlex**       | All other domains, with precision filters (title+abstract scope, topics).|
| **Semantic Scholar** | Supplementary; has TLDR summaries useful for screening.                |

**Default routing (`--source auto`)**:
- Domain is inferred from the query (or set explicitly with `--domain`).
- HEP family domain → InspireHEP first; if it returns less than half the requested limit, OpenAlex is queried to fill the gap.
- Non-HEP domain → OpenAlex first; falls back to Semantic Scholar if results are sparse.

Override with `--source inspire|openalex|semscholar|all`.

## Inputs to confirm

Ask only for what is missing:
- search target: topic, claim, section goal, or method name
- desired use mode: `background`, `survey`, `method`, `baseline`, `evaluation`, or `claim-support`
- if this is for a report, which section needs support and what kind of support is missing
- time window or recency preference
- preferred result count
- whether the user wants a file saved or inline output

If the user provides only a broad topic, default to `background` mode.

## Default behavior

- Infer domain automatically; route to the best source.
- Apply OpenAlex precision filters (`title_and_abstract.search`, `has_abstract`, `language:en`, `is_paratext:false`).
- Drop low-relevance results via `--min-score` and `--min-coverage` cutoffs (defaults: 0.05 and 0.10).
- Return concise, markdown-ready results with quoted matched sentences from each abstract.
- Do not fabricate claims about paper contents beyond title, metadata, and retrieved abstract text.

## Report-oriented workflow

When the user is drafting or revising a report:

1. Identify the target section and the citation role.
2. Choose one primary mode for that section:
   - `Research Background` → `background` or `survey`
   - `Methodology` → `method`
   - `Results & Visualization` comparison paragraphs → `baseline`
   - `Validation` benchmark or protocol discussion → `evaluation`
   - any isolated factual statement → `claim-support`
3. Turn the section need into a compact query rather than searching the whole paragraph verbatim.
4. Return only the strongest 2-5 references unless the user asks for a long list.
5. If saving notes for a report, prefer a section-scoped filename such as:
   - `references/background_references.md`
   - `references/method_references.md`
   - `references/validation_references.md`
6. Make the output easy to transplant into prose by emphasizing why each source matters.

## Recommended workflow

1. **Clarify the search intent**
   - Map the request into one of the supported modes.
   - If the user gives a sentence or claim, extract the core technical concepts before searching.
   - If the user mentions a report section, infer the citation role:
     - introduction or context → `background`
     - related work overview → `survey`
     - method justification → `method`
     - comparison target → `baseline`
     - benchmark or metrics discussion → `evaluation`
     - evidence for a specific statement → `claim-support`

2. **Choose a query**
   - Use the guidance in `references/query_patterns.md`.
   - Start with a narrow query that includes the main concepts.
   - Domain is inferred automatically; override with `--domain` only when the inference is wrong.
   - Sort defaults by mode: `survey`/`baseline` → citation count; otherwise relevance score.

3. **Run the search script**
   ```bash
   uv run reference-search/scripts/reference_search.py \
     "{query}" \
     --mode {mode} \
     --limit {limit} \
     --format md
   ```

   Common overrides:
   - `--domain {key}`: pin a domain. Known keys are listed in `references/domain_topics.md`.
   - `--source {auto|inspire|openalex|semscholar|all}`: force a source.
   - `--min-coverage 0`: disable the noise filter (useful when query is very short).
   - `--topic-id Txxxx`: pass an OpenAlex topic ID directly (repeatable).
   - `--email you@example.com`: polite-pool User-Agent for OpenAlex / Semantic Scholar.
   - `--format json`: structured output for downstream tools (see `bibtex-gen` below).

4. **Broaden when results are sparse**
   - If fewer than 3 relevant results appear:
     - simplify the query to the main nouns
     - lower `--min-coverage` (try 0.05 or 0)
     - try `--source all` to merge across sources
     - relax mode (`background` rather than `claim-support`)
   - State when the search had to be broadened.

5. **Curate, do not just dump results**
   - The script already drops low-relevance results and reranks. Still inspect each result before presenting.
   - For each selected paper, the output provides:
     - title, year, citation count, final score
     - first author or short author string
     - DOI or OpenAlex/arXiv URL
     - matched query terms and a quoted abstract sentence proving relevance
   - Then a short synthesis: dominant themes, recommended starting paper, caveat.

6. **Format for the user's context**
   - For a general literature request, return a numbered shortlist.
   - For report-writing support, group results under headings like `Background References`, `Baseline References`, or `Evidence for Claim`.
   - For claim support, explicitly say whether the retrieved references look like strong, partial, or weak support based on the matched-terms count and the quoted sentence.
   - For section support, end with a short `How to use in the report` note describing where the references belong and what they can support.

## Output template

The CLI produces this structure (markdown mode):

```markdown
## Reference Search: "{query}"

**Mode**: {mode}
**Domain**: {domain}
**Sources**: {sources used}
**Results**: {count}

### Recommended references
1. **Paper title** ({year}, cited: {N}, score: {0.XX})
   - Authors: {authors}
   - Source: {openalex|inspire|semscholar} / {venue}
   - DOI/URL: {identifier}
   - Why it matters: {mode-prefix}. Matched {k}/{T} key terms ({matched_terms}). Source: ...
     From abstract: "{quoted matched sentence}"

### Synthesis
- Dominant themes: ...
- Best starting point: ...
- Caveat: ...
```

## Save behavior

If the user asks to save the results, write the formatted markdown to the requested path after reviewing the results. If the path is relative, resolve it from the current working directory.

## Downstream: producing bibtex from results

When the user wants a real `.bib` file (not just a curated markdown shortlist), pair this skill with the **`bibtex-gen`** companion. The flow is:

1. Run this skill with `--format json` and save the output:
   ```bash
   uv run reference-search/scripts/reference_search.py \
     "{query}" --mode {mode} --limit {limit} --format json \
     > /tmp/{slug}.json
   ```
2. Pipe that JSON into `bibtex-gen`:
   ```bash
   uv run bibtex-gen/scripts/bibtex_gen.py \
     --from-search /tmp/{slug}.json \
     --output paper/refs.bib --verbose
   ```

`bibtex-gen` extracts each result's DOI from `identifier` and routes it through HEP (InspireHEP) → non-HEP (Google Scholar → CrossRef) so that HEP papers land with `Author:YYYYabc` keys and non-HEP papers land with Scholar / CrossRef keys. This skill is **discovery only**; canonical bibtex always comes from the field-appropriate authoritative source.

The JSON output preserves `results[].identifier` and `results[].title` for backward compatibility with `bibtex-gen --from-search`.

If the user asks for `references` *and* a `.bib` in the same step, run both skills back-to-back rather than fabricating bibtex from the discovery metadata directly.

## Resources

- `scripts/reference_search.py`: main entry. Domain-aware multi-source router.
- `scripts/source_openalex.py`, `scripts/source_inspirehep.py`, `scripts/source_semantic_scholar.py`: source adapters.
- `scripts/domain.py`: domain inference + topic ID mapping.
- `scripts/relevance.py`: query-coverage scoring + matched-sentence extraction + dedup.
- `scripts/_common.py`: shared `WorkSummary` dataclass and HTTP helper.
- `references/query_patterns.md`: query construction heuristics and mode examples.
- `references/domain_topics.md`: domain key reference and OpenAlex topic ID hints.
- `research-report`: companion reporting skill that can consume section-level reference support from this skill.
- `bibtex-gen`: companion skill that turns this skill's JSON output into a real `.bib` file (`bibtex-gen --from-search <file>.json`). Use it whenever the user wants citations materialized, not just curated.

After creating or updating this skill, suggest starting a new session so the new skill is discoverable from session start.
