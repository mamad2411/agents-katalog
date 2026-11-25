---
name: lit-rescue
description: Last-resort skill. Invoke when no obvious or coherent solution is available and hallucination risk is high. Searches peer-reviewed literature and validated sources (Perplexity, bioRxiv, PubMed) before attempting an answer. Generalist — applies to any domain.
---

# Lit-Rescue — Literature-Grounded Problem Solving

**When to invoke this skill:**
- No confident answer exists from training knowledge
- The problem involves a specific algorithm, parameter, protocol, or library behavior that could be misremembered
- Previous attempts at solving the problem have been inconsistent or failed
- The question is novel, niche, or at the edge of a domain
- The user is debugging something that "shouldn't happen"

**Rule:** If there is >20% chance the answer could be fabricated or outdated → invoke this skill first.

---

## Step 1 — Classify the Problem

Identify the query type before formulating search queries:

| Type | Keywords | Primary MCP |
|------|----------|-------------|
| **METHOD** | "which algorithm", "best approach for", "how to compute X" | Perplexity → bioRxiv |
| **PARAM** | "what value for", "typical hyperparameters", "threshold for" | Perplexity → PubMed |
| **BUG** | "why does X fail", "unexpected behavior", "error in library" | Perplexity only |
| **THEORY** | "physical basis of", "why does X work", "derivation" | PubMed → bioRxiv |
| **PROTOCOL** | "standard procedure", "step-by-step for", "pipeline for" | bioRxiv → PubMed |
| **BENCHMARK** | "comparison of methods", "state of the art for", "which is better" | bioRxiv → PubMed |
| **DOMAIN** | highly specialized jargon or niche subfield | Perplexity → PubMed |

Multiple types can apply — activate each relevant search.

---

## Step 2 — Formulate Queries

**Load `references/perplexity-prompts.md`** if Perplexity MCP is available.

Otherwise, construct queries following these principles:
1. **Be maximally specific** — include library name + version, domain, and exact task
2. **Ask for citations** — request DOIs, paper titles, or package documentation references
3. **Anchor to peer-reviewed content** — explicitly exclude opinion/blog content for scientific questions
4. **Specify recency** — for fast-moving fields, constrain to last 2–3 years

---

## Step 3 — Execute Search Waterfall

Run MCPs in this order (stop when sufficient evidence found):

### A — Perplexity (if available)

Check if `mcp__perplexity` tools are accessible. If yes, use the prompts from `references/perplexity-prompts.md`.

Perplexity covers: documentation, GitHub issues, StackOverflow, technical blogs, and papers. Best for BUG and METHOD types.

### B — bioRxiv / medRxiv MCP (always available)

```
bioRxiv.search_preprints(
  query="[core concept] [method/tool] [domain]",
  date_range="2022-2026",  # recency matters for methods
  limit=10
)
```

Use for: recent methods papers, benchmarks, protocols, negative results.

Refine with category filter if domain is clear (e.g., `category="bioinformatics"` or `"biochemistry"`).

For a promising hit, fetch full abstract + DOI:
```
bioRxiv.get_preprint(doi="10.1101/XXXX")
```

### C — PubMed MCP (always available)

```
PubMed.search_articles(
  query="[concept] [method] [organism/domain]",
  max_results=10,
  sort="relevance"   # or "date" for recent work
)
PubMed.get_article_metadata(pmid="XXXXXXXX")
```

Use for: established methods, clinical/biological protocols, theoretical foundations.

For methods specifically: add `"protocol" OR "method" OR "algorithm"` to the query.

For benchmarks: add `"comparison" OR "benchmark" OR "evaluation"` to the query.

---

## Step 4 — Synthesize Results

After collecting hits, apply this synthesis protocol:

### 4.1 — Extract method/answer
State the answer as found in literature. Do not infer beyond what the sources say.

### 4.2 — Cite properly
Every claim derived from literature must carry a citation:
```
[Author et al., YEAR] — DOI: 10.XXXX/XXXXX
or
[bioRxiv YEAR-MM-DD] — DOI: 10.1101/XXXX
```
Never cite URLs. Always use DOIs when available.

### 4.3 — Rate confidence
```
★★★ — Multiple independent peer-reviewed sources agree
★★☆ — One peer-reviewed source or multiple preprints
★☆☆ — Single preprint or indirect evidence
☆☆☆ — No direct source found (see Step 5)
```

### 4.4 — Flag limitations
Note explicitly:
- Whether the source is peer-reviewed or a preprint
- Recency (methods older than 5 years may have superseded alternatives)
- Whether the source matches the exact library version / domain in question

---

## Step 5 — Honest Reporting

**If evidence is found (★★☆ or better):** Present the answer with citations. Note any caveats.

**If evidence is partial (★☆☆):** Present what was found, state clearly that evidence is thin, and describe what would be needed to confirm.

**If no evidence found (☆☆☆):**
```
⚠️ LIT-RESCUE NEGATIVE RESULT

Searched: [list of queries and MCPs used]
Result: No peer-reviewed or preprint source found for [specific question].

Options:
1. Reformulate the question — the concept may use different terminology
2. Consult domain-specific documentation directly (package docs, official manual)
3. Run an empirical test (write a minimal script to probe the behavior)
4. Ask a domain expert or post to the relevant community forum

I will NOT speculate without a source.
```

This negative result is itself valuable — it tells the user that this is an open question or requires empirical investigation.

---

## Decision Tree

```
Problem encountered
  │
  ├─ Is the answer confidently known from verified knowledge?
  │    └─ Yes → answer directly (don't invoke this skill)
  │    └─ Uncertain → continue
  │
  ├─ Classify type (Step 1)
  │
  ├─ Is it a BUG/implementation question?
  │    └─ Yes → Perplexity first (broader web coverage)
  │    └─ No → bioRxiv + PubMed first
  │
  ├─ Is the field fast-moving (ML, comp bio, cheminformatics)?
  │    └─ Yes → bioRxiv (preprints = 6–18 months ahead of journals)
  │    └─ No → PubMed (peer-reviewed = more reliable for established fields)
  │
  └─ Synthesize (Step 4) → Report honestly (Step 5)
```

---

## Related Skills
- `chem-brainstorm` — for comp chem problems, run this before lit-rescue to check local tools
- `scientific-skills:literature-review` — for systematic multi-paper literature analysis
- `scientific-skills:pubmed-database` — for complex PubMed query strategies
- `scientific-skills:biorxiv-database` — for preprint-focused searches
