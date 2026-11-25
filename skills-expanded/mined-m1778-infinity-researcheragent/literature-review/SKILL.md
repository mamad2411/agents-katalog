---
name: literature-review
description: Systematic literature review methodology. Search, screen, classify, and synthesize academic papers with rigorous evidence tracking.
license: MIT
---

# Literature Review Skill

Use this skill when conducting a literature search, meta-analysis, or technical survey on academic topics (AI/ML or Biology/Cancer).

## Operational Workflow

### 1. Query Decomposition (Mandatory Initial Step)
- Break the topic into 3-5 distinct sub-questions (e.g., architecture, scaling behavior, loss formulation, empirical evaluation).
- Extract domain terminology, author names, canonical benchmark datasets, and standard baseline methods.

### 2. Multi-Engine Sourcing Priority
- **AI/ML & Deep Learning**: Search arXiv and Semantic Scholar first.
- **Biomedical & Oncology**: Search PubMed / NCBI E-Utilities, Europe PMC, bioRxiv, and CrossRef.
- **Code & Implementations**: Query GitHub repository search.
- **General Concepts / Broad Meta-Search**: Query DuckDuckGo or SearXNG.

### 3. Systematic Screening & Categorization
Classify discovered papers into 3 operational buckets:
1. **Foundational / Canonical**: First paper to introduce the core architecture or concept.
2. **State-of-the-Art / SOTA**: Papers holding current Pareto frontiers on standard benchmarks.
3. **Contrarian / Critical Evidence**: Papers documenting failure modes, scaling bottlenecks, or negative results.

### 4. Deterministic Extraction Protocol
For every selected paper, extract:
- Exact primary identifier (arXiv ID, DOI, PMID).
- Model parameters / capacity / dataset token count.
- Baseline models compared against and evaluation conditions.
- Primary quantitative metrics (loss reduction, latency, memory footprint).
- Explicit limitations, caveats, and stated failure modes.

### 5. Synthesis Output Matrix
Format synthesis into a markdown matrix:
| Paper / Work | Primary Identifier | Key Architectural Idea | Quantitative Results | Limitations / Failure Modes |
|---|---|---|---|---|

