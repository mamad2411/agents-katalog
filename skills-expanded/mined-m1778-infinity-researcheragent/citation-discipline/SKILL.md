---
name: citation-discipline
description: Strict citation verification and attribution standards. Enforces that every factual claim has an unambiguous, resolvable academic reference.
license: MIT
---

# Citation Discipline Standards

This skill governs the citation integrity of all research outputs produced by Infinity-ResearcherAgent.

## Core Directives

### 1. No Phantom Numbers (Zero-Tolerance Policy)
- Every benchmark number, hyperparameter value, sample size, or empirical metric (e.g., "recovered 85% CE loss", "achieved 3.2x speedup", "L0 = 42") **MUST** be paired with an identifiable source citation.
- If a calculation or estimate is made by the agent rather than quoted from a paper, label it unambiguously: `[Agent Calculation - unverified empirically]`.
- If an exact number is unknown or unstated in the literature, state "Unspecified in primary paper" rather than inventing a plausible value.

### 2. Format Requirements for Resolvable Identifiers
Every citation bracket must include at least one permanent, machine-resolvable identifier:
1. **arXiv**: `[Author et al., Year, arXiv:YYMM.NNNNN]` or `[arXiv:YYMM.NNNNN]`
2. **DOI**: `[Author et al., Year, 10.xxxx/yyyy]` or `[doi:10.xxxx/yyyy]`
3. **PubMed**: `[Author et al., Year, PMID: NNNNNNNN]`
4. **Code / Repo**: `[Author/Repo, GitHub: https://github.com/org/repo]`

### 3. Separation of Knowledge Layers
Distinguish between three separate knowledge categories in all technical reports:
- **Established Academic Consensus**: Validated across multiple independent publications.
- **Single-Source Empirical Claim**: Reported by one author group, awaiting independent reproduction.
- **Architectural Recommendation / Agent Inference**: Deduced logically by the agent from reported evidence.

### 4. Bibliography Closure
Every document ending must contain a `## References` section listing every cited work with its title, authors, publication venue, year, and primary resolvable link.

