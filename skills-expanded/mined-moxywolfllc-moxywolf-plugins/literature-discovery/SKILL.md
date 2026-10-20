---
name: literature-discovery
description: >
  Multi-source literature discovery across academic and non-academic sources. Can be the
  FIRST step in a research project — give it a topic and it creates the library from scratch.
  Searches OpenAlex, Semantic Scholar, arXiv, and the general web (blogs, whitepapers, NIST
  docs, vendor publications, industry reports). Use this skill whenever the user says "research
  this topic," "find papers on," "discover literature," "I want to research," "find sources
  about," "what's been written about," "build me a bibliography," "start researching," "find
  more papers," "expand my bibliography," "what am I missing," "find related work," "literature
  search," "fill research gaps," or any request to search for literature — academic or
  otherwise — on a topic. This is the recommended ENTRY POINT for new research projects.
  Also trigger when gap analysis results suggest missing coverage areas, or when the user
  gives a topic without specifying what to do with it.
version: 0.3.0
---

# Literature Discovery

The starting point for any research project. Give it a topic — it finds the literature,
creates the library, and loads everything into Supabase. Works with or without an existing
library.

## Discovery Engines

This skill has two discovery engines that work together:

1. **API Engine** — Direct calls to academic databases (OpenAlex, Semantic Scholar, arXiv)
   and web search. Fast, structured, returns metadata-rich results.

2. **Multi-Model Swarm** — Fans the same research query out to 2-3 LLMs via OpenRouter
   (Perplexity Sonar Pro + Gemini Flash or Claude Sonnet). Each model searches its own
   knowledge base and web-grounded sources, finding material the others miss. Results are
   merged, deduplicated, and synthesized by Claude.

By default, both engines run. The API engine catches the structured academic literature.
The swarm catches the practitioner content, niche reports, and sources that don't show up
in academic indexes.

## Two Modes

### Mode 1: Topic-First (New Research)

The user has a topic but no bibliography yet. This is the most common entry point.

Flow:
1. User says "I want to research STIG automation" (or any topic)
2. Create a new library in Supabase
3. Search academic AND non-academic sources
4. Present candidates for user review
5. Ingest approved sources into the library
6. Run gap analysis to identify what's still missing

### Mode 2: Library Expansion (Existing Research)

The user already has a library and wants to find what's missing.

Flow:
1. Assess current library state
2. Choose discovery strategy based on gaps
3. Search, deduplicate against existing citations
4. Present and ingest approved sources

## Prerequisites

- **Supabase MCP** — creating libraries, reading/writing citations
- **Built-in `WebSearch`** — for general web search across blogs, whitepapers, NIST/DISA docs
- **`WebFetch` and `Bash` (curl)** — for direct API calls (OpenAlex, Semantic Scholar, arXiv, CrossRef)
- **OpenRouter API key** + **Council plugin v0.7.0+** — the multi-model swarm reuses Council's `scripts/openrouter_dispatch.py` (and `scripts/openrouter_key.py`), which auto-resolves the key from the `OPENROUTER_API_KEY` env var or the team-shared vault file at `MoxyWolf Vault/_Shared Knowledge/Agents and Plugins/openrouter.env`

## Step 1: Understand the Research Need

Ask the user what they want to research. If they've given a clear topic, proceed.
If vague, ask a few sharpening questions:

- What specific aspect of this topic interests you?
- Are you looking for academic research, industry practices, both?
- Any particular time period? (last 5 years, historical, etc.)
- Any specific domains? (cybersecurity, compliance, AI, etc.)

## Step 2: Create or Select Library

**If no library exists for this topic:**

```sql
INSERT INTO research_libraries (name, description, metadata)
VALUES (
  '{topic_name}',
  '{user_description}',
  '{"topics": [...], "created_by": "dorian", "source_types": ["academic", "industry", "government"]}'::jsonb
)
RETURNING id, name
```

Tell the user: "Created library '[name]' — now searching for sources."

**If a library already exists:**

```sql
SELECT id, name FROM research_libraries ORDER BY created_at DESC
```

Ask which one, or auto-select if name matches.

## Step 3: Search Across All Source Types

### Academic Sources

#### OpenAlex (Primary — largest coverage, free, no auth)

```
GET https://api.openalex.org/works?search={query}&per_page=50&sort=relevance_score:desc
```

Add `&mailto=dorianc@moxywolf.com` for polite pool access (faster rate limits).

Filter options:
- By year: `&filter=from_publication_date:2020-01-01`
- By concept: `&filter=concepts.id:C41008148`
- By open access: `&filter=is_oa:true`

Key response fields: `doi`, `title`, `authorships`, `publication_year`,
`primary_location.source.display_name`, `abstract_inverted_index`, `cited_by_count`

Reconstruct abstracts from inverted index (see `references/api-response-formats.md`).

Rate limit: 10/sec without key, 100/sec with mailto.

#### Semantic Scholar (Strong for citation graphs)

```
GET https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=50&fields=title,authors,year,abstract,externalIds,citationCount
```

Rate limit: 100 requests/5 minutes.

#### arXiv (Preprints — CS, ML, Physics, Math)

```
GET https://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=50&sortBy=relevance
```

Rate limit: 1 request/3 seconds. Always respect this.

For cybersecurity/compliance topics, use category filter: `cat:cs.CR`

### Non-Academic Sources

These are just as important for practitioner-oriented research.

#### Web Search (built-in)

Use Claude's built-in `WebSearch` tool to search for:

Construct targeted queries for each source type:

- **Industry blogs/whitepapers**: `"{topic}" site:blog OR whitepaper OR "technical report"`
- **Government/standards docs**: `"{topic}" site:nist.gov OR site:disa.mil OR site:cyber.gov`
- **Vendor documentation**: `"{topic}" site:docs.* OR "technical documentation"`
- **Conference talks/slides**: `"{topic}" conference OR presentation OR "talk" filetype:pdf`
- **Reddit/forums**: `"{topic}" site:reddit.com OR site:stackoverflow.com`

#### NIST/Government Sources (direct)

For compliance and cybersecurity topics, search NIST directly:

```
WebFetch: https://csrc.nist.gov/publications?keywords={query}
```

Extract publication titles, abstracts, and PDF links.

#### DISA STIG Sources

For STIG-related research:

```
WebFetch: https://public.cyber.mil/stigs/
```

Search for relevant STIGs, SRGs, and related documentation.

### Source Classification

For each discovered source, classify it:

| Type | Entry Type | Example |
|------|-----------|---------|
| Journal article | `article` | IEEE, ACM papers |
| Conference paper | `inproceedings` | Black Hat, RSA talks |
| Preprint | `preprint` | arXiv papers |
| Government publication | `government` | NIST SP 800-series |
| Industry whitepaper | `whitepaper` | Vendor security reports |
| Blog post | `blog` | Practitioner insights |
| Standard/Framework | `standard` | DISA STIGs, CIS Benchmarks |
| Book/Chapter | `book` | Textbooks, reference guides |
| Other web source | `web` | Everything else |

## Step 3b: Multi-Model Research Swarm

After the API and web searches complete, run the multi-model swarm to catch what
structured APIs miss. This uses OpenRouter to query multiple LLMs in parallel,
each with different training data, web access, and knowledge bases.

### How It Works

Send the same research prompt to 2-3 models via Council's `scripts/openrouter_dispatch.py`
helper, which hits the OpenRouter chat completions endpoint in parallel. Each model
returns sources it knows about. Claude then merges, deduplicates, and validates the
combined results.

### Models and Their Strengths

| Model | OpenRouter ID | Strength | Notes |
|-------|--------------|----------|-------|
| Perplexity Sonar Pro | `perplexity/sonar-pro` | Web-grounded search, real-time citations with verified URLs | **Primary.** Always use. Best source of real, current URLs. |
| Google Gemini 2.5 Flash | `google/gemini-2.5-flash-preview-05-20` | Fast, strong on government/standards docs | Use Flash not Pro — Pro's reasoning burns the token budget before generating output. |
| Anthropic Claude Sonnet | `anthropic/claude-sonnet-5` | Deep reasoning, strong cross-domain connections | Good complement to Perplexity. Honest about what it doesn't know. |

### Models to Avoid

| Model | Why |
|-------|-----|
| `openai/gpt-4o` | Fabricates URLs. Every single URL it returned in testing was `example.com`. Cannot be trusted for source discovery. |
| `deepseek/deepseek-r1` | Usable — the dispatch helper's 180s default timeout covers R1's reasoning phase. Still slower than chat variants, so default to `deepseek/deepseek-chat` unless deep reasoning is worth the latency. |
| `google/gemini-2.5-pro-preview-05-06` | Spends most of its token budget on internal reasoning, then hits max_tokens before outputting results. Use Flash instead. |

### Execution Strategy

Run Perplexity + one or two other models as a parallel batch via Council's
`scripts/openrouter_dispatch.py` (see "Executing via the dispatch helper" below).
The 180s default timeout comfortably accommodates 3 models in one batch; only
split if you're chaining `deepseek-r1` with another reasoning model.

### The Swarm Prompt

Send this prompt (adapted per topic) to each model:

```
You are a research discovery agent. Your job is to find ALL significant sources
— academic papers, government publications, industry whitepapers, blog posts,
conference talks, and standards documents — on the following topic:

TOPIC: {topic}
CONTEXT: {library_description}

For each source you find, provide:
1. Title (exact)
2. Authors (if known)
3. Year of publication
4. Type: academic | government | industry | blog | standard | book
5. URL or DOI (if you have it — ONLY real ones, never fabricate)
6. A 2-3 sentence description of what the source covers
7. Why it's relevant to this research topic

Find at least 15 sources. Prioritize:
- Seminal/foundational works that everyone in this field cites
- Recent publications (last 3 years) showing current state of the art
- Government standards and guidance documents (NIST, DISA, DoD)
- Practitioner perspectives (blogs, conference talks, vendor whitepapers)
- Contrarian or critical viewpoints that challenge mainstream thinking

DO NOT fabricate citations. If you're unsure about a URL or DOI, say so.
It's better to give a title without a link than a fake link.

Format your response as a JSON array:
[
  {
    "title": "...",
    "authors": "...",
    "year": 2024,
    "type": "academic",
    "url": "https://...",
    "doi": "10.1234/...",
    "description": "...",
    "relevance": "..."
  }
]
```

### Executing via the dispatch helper

Reuse Council's `scripts/openrouter_dispatch.py` (resolves at
`${CLAUDE_PLUGIN_ROOT}/../council/scripts/openrouter_dispatch.py` when both plugins
are installed in the same marketplace, or copy it to this plugin if you prefer
no cross-plugin coupling).

Build a swarm jobs file at `${WORKSPACE_OUTPUTS}/lit-discovery-{run_id}/swarm-jobs.json`:

```json
[
  {
    "id": "perplexity",
    "model": "perplexity/sonar-pro",
    "messages": [{"role": "user", "content": "{swarm_prompt}"}],
    "temperature": 0.3,
    "max_tokens": 4000
  },
  {
    "id": "gemini",
    "model": "google/gemini-2.5-flash-preview-05-20",
    "messages": [{"role": "user", "content": "{swarm_prompt}"}],
    "temperature": 0.3,
    "max_tokens": 4000
  },
  {
    "id": "claude",
    "model": "anthropic/claude-sonnet-5",
    "messages": [{"role": "user", "content": "{swarm_prompt}"}],
    "temperature": 0.3,
    "max_tokens": 4000
  }
]
```

Then dispatch in parallel:

```bash
python3 "${COUNCIL_PLUGIN}/scripts/openrouter_dispatch.py" \
    --jobs "${WORKSPACE_OUTPUTS}/lit-discovery-${RUN_ID}/swarm-jobs.json" \
    --out  "${WORKSPACE_OUTPUTS}/lit-discovery-${RUN_ID}/swarm" \
    --timeout 180
```

The helper writes one `{id}.json` per model. Read each, extract `response.choices[0].message.content`, then process as below.

### Processing Swarm Results

After all models respond:

1. **Parse** each model's JSON response into source objects
2. **Tag** each source with the model that found it:
   `"discovered_by": ["perplexity", "gemini"]`
3. **Merge** by matching on title similarity (>85%) or exact DOI/URL match
4. **Score** by cross-model agreement:
   - Found by 3+ models = high confidence
   - Found by 2 models = medium confidence
   - Found by 1 model only = verify before including
5. **Validate URLs** — for sources found by only one model, attempt a HEAD
   request via WebFetch to confirm the URL is real. Discard 404s.
6. **Deduplicate against API results** — remove anything already found by
   OpenAlex, Semantic Scholar, or arXiv in Step 3

### What the Swarm Catches That APIs Miss

- Practitioner blog posts and opinion pieces
- Vendor-specific whitepapers and case studies
- DISA/DoD memos and policy documents not indexed in academic databases
- Conference presentations and webinar recordings
- Reddit/forum discussions with real-world implementation insights
- International equivalents and comparative standards
- Historical documents and foundational thinking pre-dating digital indexes
- Cross-domain connections (e.g., healthcare compliance mapped to defense)

### Cost Awareness

Actual costs from live testing (March 2026):
- Perplexity Sonar Pro: ~$0.024 per query (best ROI — most real sources per dollar)
- Gemini 2.5 Flash: ~$0.005-0.01 per query
- Claude Sonnet: ~$0.02-0.04 per query

Total per discovery run (2 models): ~$0.03-0.07. Negligible for the coverage improvement.

### Presenting Swarm Results

After merging with API results, flag swarm-only discoveries in the presentation:

```
🔍 Multi-Model Discovery ([count] unique sources not found by API search)

22. [Title] ([Year]) — found by Perplexity + Gemini Flash
    Type: whitepaper
    URL: [link]
    Why: [relevance explanation]

23. [Title] ([Year]) — found by Perplexity only (URL verified)
    Type: blog
    URL: [link]
    Why: [relevance explanation]
```

This makes it clear which sources came from the swarm vs. structured APIs,
so the user can weigh confidence accordingly.

## Step 3c: Deep Research (optional recursive expansion)

Steps 3 and 3b are one flat round — they search what the user asked for. Deep research is the bounded recursive version: each level distills what it found into a learnings digest, and that digest generates the next level's queries. The search follows the corpus instead of the opening guess, which is how it surfaces the literature the field files under a different name.

Run it when the user says "go deep," "be exhaustive," or "I don't know what I don't know," and when a flat round comes back thin on a topic that clearly has more to it. Skip it for a quick look or a tightly-bounded expansion — recursion costs real money and a flat round is usually enough.

Defaults: breadth 4, depth 2, concurrency 4. Declare the shape and the estimated spend before running anything, and get an explicit go. Record the actuals — rounds run, dry branches, sources added, wall time, spend — into the library metadata when it finishes, so `/research-status` can report what the corpus cost to build.

The full protocol lives in `references/deep-research-loop.md`: the three-bucket digest schema, child-query generation, dry-branch handling, upward propagation between siblings, termination conditions, and which substrate to run it on. Read it before running a deep pass. Do not improvise the recursion — an unbounded or undeduped version of this loop burns budget and inflates the source count without growing the corpus.

## Step 4: Deduplicate

If expanding an existing library:

```sql
SELECT doi, title, url FROM citations WHERE library_id = {id}
```

Remove matches on DOI, URL, or title similarity >90%.

For new libraries, deduplicate across search results (same paper found
by multiple APIs).

## Step 5: Present Candidates

Group results by source type for clarity:

```
Literature Discovery: "{topic}"
══════════════════════════════

Found [X] sources across academic and industry channels.

📄 Academic Papers ([count])
1. [Title] ([Year]) — [Journal]
   Authors: [...]  |  Citations: [count]
   DOI: [doi]

2. ...

🏛️ Government & Standards ([count])
3. [NIST SP 800-171 Rev 3] — NIST
   Published: [date]
   URL: [link]

4. ...

📝 Industry & Practitioner ([count])
5. [Blog Title] — [Site]
   Author: [...]  |  Published: [date]
   URL: [link]

6. ...

Which of these should I add to your library?
Say 'all', specific numbers, 'academic only', 'industry only', or 'none'.
```

## Step 6: Ingest Approved Sources

For each approved source:

```sql
INSERT INTO citations (
  library_id, citation_key, entry_type, title, authors, year,
  journal, abstract, doi, arxiv_id, url, bibtex_raw,
  verification_status, source
) VALUES (
  {library_id},
  '{generated_citation_key}',
  '{entry_type}',
  '{title}',
  '{authors}',
  {year},
  '{journal_or_publisher}',
  '{abstract_or_description}',
  '{doi}',
  '{arxiv_id}',
  '{url}',
  '{bibtex_raw_if_available}',
  CASE WHEN doi IS NOT NULL OR arxiv_id IS NOT NULL THEN 'verified' ELSE 'unverified' END,
  '{source_api}'
)
ON CONFLICT (library_id, citation_key) DO NOTHING
```

### Generating Citation Keys

For non-academic sources without a BibTeX key, generate one:
- `{first_author_surname}_{year}` for authored works
- `{org_acronym}_{year}_{short_title}` for org publications (e.g., `nist_2024_sp800171`)
- `{site}_{year}_{slug}` for blog posts (e.g., `krebs_2024_stig_automation`)

### Generating BibTeX for Non-Academic Sources

For web sources, generate a BibTeX entry so the library stays export-compatible:

```bibtex
@misc{krebs_2024_stig_automation,
  author = {Krebs, Brian},
  title = {Automating STIG Compliance at Scale},
  year = {2024},
  url = {https://example.com/article},
  note = {Blog post. Accessed: 2026-03-18},
  abstract = {Brief description of the content...}
}
```

## Step 7: Summary and Next Steps

```
Library Built: {name}
═══════════════════

Total sources added: [X]
  ├─ Academic papers:      [count]
  ├─ Government/standards: [count]
  ├─ Industry/practitioner: [count]
  └─ Other:                [count]

Verification status:
  ├─ Verified (DOI/arXiv): [count]
  └─ Unverified (web):     [count]

Next steps:
  → "Verify my citations" — validate DOIs and check for broken links
  → "Find more papers" — run another discovery round with refined terms
  → "Synthesize my research" — build thematic map + writing perspective
  → "Import my BibTeX" — add your own collected references on top
```

## Discovery Strategies (for Library Expansion)

When expanding an existing library, choose based on its state:

### Strategy 1: Keyword Expansion
Broaden search terms based on themes already in the library.

### Strategy 2: Citation Chain
Follow references and citations from the library's most-cited papers
via Semantic Scholar.

### Strategy 3: Gap-Driven
Target specific gaps identified in `research_gaps` table.

### Strategy 4: Temporal
Fill year-range gaps — find recent work or foundational papers.

### Strategy 5: Source-Type Diversification
If the library is all academic, find industry sources. If all industry,
find the academic backing.

## Scheduled Discovery

Weekly automated scan (configure via `/schedule`):

1. For each active library, search for sources published in the last 7 days
2. Filter by relevance to library topics
3. Stage candidates — do NOT auto-ingest
4. Summary for next session: "Found [X] new sources this week for [library name]."

## Reference

- **`references/api-response-formats.md`** — Parsing guides for OpenAlex, Semantic Scholar, arXiv, CrossRef, DataCite
- **`references/openrouter-swarm.md`** — Multi-model swarm configuration: model roster, prompt templates, merge algorithm, cost breakdown
- **`references/deep-research-loop.md`** — The recursive deep-research protocol behind Step 3c: breadth/depth/concurrency, the learnings digest, dry-branch termination, upward propagation, and the declared-budget gate
- For the Supabase schema, read the migration SQL in the research-pipeline skill.
