---
name: literature-review
version: 1.3.5
description: Conduct comprehensive, systematic literature reviews using multiple academic databases (PubMed, arXiv, bioRxiv, Semantic Scholar, etc.). This skill should be used when conducting systematic literature reviews, meta-analyses, research synthesis, or comprehensive literature searches across biomedical, scientific, and technical domains. Creates professionally formatted markdown documents and PDFs with verified citations in multiple citation styles (APA, Nature, Vancouver, etc.).
allowed-tools: [Read, Write, Edit, Bash]
---

# Literature Review

## Overview

Conduct systematic, comprehensive literature reviews following rigorous academic methodology. Search multiple literature databases, synthesize findings thematically, verify all citations for accuracy, and generate professional output documents in markdown and PDF formats.

This locally maintained skill uses direct scholarly APIs for retrieval and provides tools for citation verification, result aggregation, and document generation. See the database routing below before choosing a search tool.

## When to Use This Skill

Use this skill when:
- Conducting a systematic literature review for research or publication
- Synthesizing current knowledge on a specific topic across multiple sources
- Performing meta-analysis or scoping reviews
- Writing the literature review section of a research paper or thesis
- Investigating the state of the art in a research domain
- Identifying research gaps and future directions
- Requiring verified citations and professional formatting

## Database Access and Local Customizations

Use the local `scripts/lit_search.py` for bounded searches in PubMed (`pm`),
Europe PMC (`epmc`), OpenAlex (`oa`), Crossref (`cr`), and Semantic Scholar (`s2`).
Run commands from this skill's directory; select each database explicitly:

```bash
python3 scripts/lit_search.py search 'CRISPR gene editing' --source pm --limit 100
```

Use the separately installed `paper-lookup` skill for additional scholarly APIs,
identifier resolution, citation links, and open-access discovery. Consult its
provider references and translate queries for each database. Keep this skill's
custom API implementation; do not replace it during upstream documentation updates.

For systematic retrieval, use the database's direct API (for PubMed, NCBI
E-Utilities or the `ncbi-entrez-skill`) with pagination/history and recorded query,
search date, total hits, and retrieved count. `lit_search.py` currently retrieves
only a bounded first page: `--limit` and `--source all` do not establish exhaustive
coverage. Its combined-source output can hide individual source errors; inspect
sources separately. PubMed MeSH and field tags must not be forwarded unchanged to
other providers. `scripts/search_databases.py` processes records already retrieved;
it does not perform live searches.

These workflows use scholarly APIs directly. Do not require commercial search
services or AI image services to complete a literature review.

## Figures When Useful

Use figures when they help communicate the review. For systematic reviews, report
the selection flow with a PRISMA diagram based on recorded screening counts.
Generate data figures and flow diagrams with reproducible plotting or diagram
tools. AI-generated illustrations are optional and require a relevant user request;
there is no mandatory number of AI figures or image-service dependency.

---

## Read the Relevant Guide Before Acting

For MeSH terms, keyword trees, query construction, query repair or search-only tasks,
use the locally maintained `systematic-search-strategy` skill. It selects the relevant
steps from the seven-step framework. Ordinary retrieval still covers relevant
multiple databases and keeps a concise persistent search log (including zero hits,
failures, progress and gaps); it does not require a formal review report. Expand the
full review workflow below only when the task calls for review methodology or synthesis.

- For a full review, read [core_workflow.md](references/core_workflow.md) before
  planning. It contains all seven phases, screening, quality assessment, synthesis,
  verification, reporting, and common pitfalls.
- Before systematic retrieval, read [search_audit.md](references/search_audit.md)
  and complete the [audit record](assets/search_audit_template.md). Check MeSH,
  free text, fields and independent seed retrieval; report unresolved gaps.
- Before constructing searches or formatting citations, read
  [search_and_citation.md](references/search_and_citation.md). Consult
  [database_strategies.md](references/database_strategies.md) for additional database
  guidance and [citation_styles.md](references/citation_styles.md) for style details.
- For an end-to-end command example, read
  [example_workflow.md](references/example_workflow.md). Example topics and dates
  are illustrative; adapt them to the review protocol.

For a search-only task, follow `systematic-search-strategy` and consult the database
references needed for execution. For a full review, also read the example when
executing the pipeline. Do not treat this short entry point as the complete methodology.

## Essential Rules

- Search as many relevant scholarly databases as practicable; do not reduce the
  source set merely because some sources return no results. Keep the existing
  multi-database emphasis. Record every attempted source, including successful
  zero-hit searches, failures, inaccessible sources and reasons for omissions.
- Prefer maintained upstream retrieval utilities where supported; read
  [upstream_retrieval.md](references/upstream_retrieval.md) before pagination or
  result reconciliation. Do not describe deferred capabilities as implemented.

- Define the review question and inclusion/exclusion criteria before screening.
- Record each database's exact query, search date, total hits and retrieved count.
  Translate syntax per provider and check retrieval completeness explicitly.
- Preserve source provenance, deduplicate, and record screening exclusion reasons.
- Assess study quality and synthesize evidence across studies; citation counts are
  not evidence quality or an eligibility criterion.
- Verify bibliographic metadata and whether each cited paper supports its claim.
  Automated DOI verification does not replace checking the article itself.
- Report limitations, reproducible methods and selection counts. For systematic
  reviews, prepare the PRISMA selection flow from actual screening records.

## Supporting Skills

Use `paper-lookup` for additional scholarly providers and `ncbi-entrez-skill` for
NCBI retrieval. Use domain-specific database skills only when the research question
needs them. Use reproducible plotting tools for data figures. No commercial search,
internal-company writing, or AI image service is required.

## Resources

### Bundled Resources

**Scripts:**
- `scripts/lit_search.py`: Bounded searches through the five custom scholarly API adapters
- `scripts/verify_citations.py`: Verify DOIs and generate formatted citations
- `scripts/generate_pdf.py`: Convert markdown to professional PDF
- `scripts/search_databases.py`: Process, deduplicate, and format search results

**References:**
- `references/citation_styles.md`: Detailed citation formatting guide (APA, Nature, Vancouver, Chicago, IEEE)
- `references/database_strategies.md`: Comprehensive database search strategies

**Assets:**
- `assets/review_template.md`: Complete literature review template with all sections

### External Resources

**Guidelines:**
- PRISMA (Systematic Reviews): http://www.prisma-statement.org/
- Cochrane Handbook: https://training.cochrane.org/handbook
- AMSTAR 2 (Review Quality): https://amstar.ca/

**Tools:**
- MeSH Browser: https://meshb.nlm.nih.gov/search
- PubMed Advanced Search: https://pubmed.ncbi.nlm.nih.gov/advanced/
- Boolean Search Guide: https://www.ncbi.nlm.nih.gov/books/NBK3827/

**Citation Styles:**
- APA Style: https://apastyle.apa.org/
- Nature Portfolio: https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards
- NLM/Vancouver: https://www.nlm.nih.gov/bsd/uniform_requirements.html

## Dependencies

### Required Python Packages
```bash
pip install requests  # For citation verification
```

### Required System Tools
```bash
# For PDF generation
brew install pandoc  # macOS
apt-get install pandoc  # Linux

# For LaTeX (PDF generation)
brew install --cask mactex  # macOS
apt-get install texlive-xetex  # Linux
```

Check dependencies:
```bash
python scripts/generate_pdf.py --check-deps
```

## Maintenance

This is a locally maintained skill. See [UPSTREAM-MERGES.md](UPSTREAM-MERGES.md)
for selective upstream integration and [tests/README.md](tests/README.md) for the
offline regression suite. Preserve the custom retrieval implementation during updates.
