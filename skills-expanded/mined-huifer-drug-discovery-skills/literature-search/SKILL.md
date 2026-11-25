---
name: literature-search
description: |
  Comprehensive literature search with automatic summarization,
  trend analysis, and key paper identification from PubMed and preprints.

  Use this skill for literature review, trend identification, key paper
  discovery, and staying current with research developments.

  Keywords: literature, pubmed, papers, search, bibliography, review
category: Literature & Intelligence
tags: [literature, pubmed, papers, search]
version: 1.0.0
author: Drug Discovery Team
dependencies:
  - pubmed-e-utilities
  - biorxiv-api
---

# Literature Search Skill

Search and analyze scientific literature for drug discovery insights.

## Quick Start

```
/pubmed EGFR resistance
/literature-search "KRAS G12C" --year 2023-2024
Find recent papers on PROTAC technology
What are the key publications on ADC toxicity?
```

## What's Included

| Feature | Description |
|---------|-------------|
| **Smart Search** | Automatic query optimization and expansion |
| **Summarization** | Key findings extraction from abstracts |
| **Trend Analysis** | Publication trends over time, hot topics |
| **Key Papers** | High-impact identification by citations |
| **Preprints** | bioRxiv/arXiv integration for early access |
| **Related Work** | Citation network exploration |

## Data Sources

| Source | Coverage | API |
|--------|----------|-----|
| PubMed | 35M+ citations | E-utilities |
| PubMed Central | 9M+ full-text | E-utilities |
| bioRxiv | 200K+ preprints | API |
| medRxiv | 80K+ preprints | API |
| arXiv | 2M+ preprints | API |

## Output Structure

```markdown
# Literature Search: EGFR Resistance

## Summary
Found **847 papers** (2020-2024). Key trends: 3rd-gen TKI resistance mechanisms,
C797S mutation targeting, combination strategies, and 4th-generation TKIs.

## Publication Trend
```
2020: 127 papers
2021: 156 papers  ↑23%
2022: 183 papers  ↑17%
2023: 198 papers  ↑8%
2024 (YTD): 183 papers
```
**Growth Rate**: +13% CAGR
**Hot Topic Alert**: C797S mutation papers up 340% (2022-2024)

## Key Papers (Top 10)

### 1. Osimertinib resistance mechanisms (Nature Medicine, 2023)
- **Citation**: 234
- **Journal Impact Factor**: 82.9
- **Key Finding**: C797S mutation accounts for 40% of 3rd-gen resistance;
  MET amplification 35%, HER2 amplification 15%
- **Authors**: Wang et al. (Memorial Sloan Kettering)

### 2. Fourth-generation EGFR TKIs (Cancer Cell, 2024)
- **Citation**: 89
- **Key Finding**: BLU-945 shows activity against C797S in xenograft models;
  clinical data promising

[... 8 more key papers ...]

## Research Themes

### Theme 1: Resistance Mechanisms (45% of papers)
| Sub-theme | Paper Count | Growth |
|-----------|-------------|--------|
| C797S mutation | 127 | +340% |
| MET amplification | 98 | +180% |
| Phenotypic transformation | 67 | +120% |

### Theme 2: Combination Strategies (25% of papers)
| Combination | Evidence Level |
|-------------|----------------|
| EGFR + MET TKI | Phase III positive |
| EGFR + Chemotherapy | Standard of care |
| EGFR + Anti-angiogenic | Mixed results |

### Theme 3: Novel Modalities (15% of papers)
| Modality | Paper Count | Status |
|----------|-------------|--------|
| 4th-gen TKI | 43 | 5 in clinic |
| Bispecific antibodies | 28 | 3 in clinic |
| ADC approaches | 34 | Early |
| PROTAC | 19 | Preclinical |

### Theme 4: Biomarker Discovery (10% of papers)
- ctDNA monitoring
- Early detection of resistance
- Patient stratification

### Theme 5: CNS Metastases (5% of papers)
- Brain penetration strategies
- Intracranial efficacy

## Top Journals

| Journal | Papers | % | Avg IF |
|---------|--------|---|--------|
| Clinical Cancer Research | 78 | 9% | 10.2 |
| J Thorac Oncol | 67 | 8% | 20.1 |
| Nat Commun | 54 | 6% | 16.6 |
| Ann Oncol | 45 | 5% | 50.5 |

## Leading Institutions

| Institution | Papers | Key Collaborators |
|-------------|--------|-------------------|
| Memorial Sloan Kettering | 67 | Dana-Farber, Mass General |
| Dana-Farber Cancer Institute | 54 | MSK, MD Anderson |
| MD Anderson | 48 | DFCI, MSK |
| AstraZeneca | 43 | Academic partners |

## Key Clinical Trials Referenced

| Trial | Phase | Finding | Citation |
|-------|-------|---------|----------|
| FLAURA2 | III | Chemo combo superior | 234 papers |
| MARIPOSA | III | Lazertinib vs osimertinib | 156 papers |
| SAVANNAH | II | MET combo resistance | 89 papers |

## Emerging Keywords (2023-2024)
| Keyword | Frequency | Growth |
|---------|-----------|--------|
| C797S | 234 | +450% |
| Fourth-generation | 189 | +380% |
| Bispecific | 156 | +220% |
| Neoantigen | 98 | +180% |
| Liquid biopsy | 87 | +150% |

## Knowledge Gaps Identified
1. Long-term resistance beyond C797S
2. Optimal combination sequencing
3. Biomarkers for patient selection
4. Quality of life endpoints
```

## Examples

### Basic Search
```
/pubmed EGFR resistance
/literature KRAS inhibitors
Search for ADC toxicity papers
```

### Time-Bounded Search
```
/pubmed "KRAS G12C" --year 2023-2024
/literature PROTAC --since 2022-06
Papers from last 6 months on GLP-1
```

### Focused Search
```
/pubmed EGFR --focus clinical
/literature "bispecific antibodies" --focus preclinical
Search reviews only on CAR-T toxicity
```

### Comparison Search
```
Compare literature on 1st vs 2nd gen EGFR TKIs
/pubmem KRAS vs NRAS vs HRAS clinical data
```

### Trend Analysis
```
What are the emerging trends in ADC research?
/literature trends obesity drugs --last 5years
```

## Search Operators

| Operator | Usage | Example |
|----------|-------|---------|
| `AND` | Combine terms | `EGFR AND resistance` |
| `OR` | Either term | `TKI OR antibody` |
| `NOT` | Exclude | `EGFR NOT lung` |
| `*` | Wildcard | `resist*` |
| `""` | Phrase | `"C797S mutation"` |
| `[]` | MeSH terms | `EGFR[MeSH]` |

## Running Scripts

```bash
# Basic search
python scripts/pubmed_search.py "EGFR resistance" --output results.json

# With date range
python scripts/pubmed_search.py "KRAS G12C" --start 2023-01-01 --end 2024-12-31

# Include full-text
python scripts/pubmed_search.py "PROTAC" --full-text --max 50

# Trend analysis
python scripts/pubmed_search.py "ADC toxicity" --trend --years 5

# Preprints only
python/scripts/pubmed_search.py "mRNA vaccines" --preprints
```

## Requirements

```bash
pip install requests pandas biopython
```

## Additional Resources

- [PubMed E-utilities API](reference/pubmed-api.md)
- [Search Strategy Guide](reference/search-strategies.md)
- [Data Extraction Scripts](reference/extraction-scripts.md)

## Best Practices

1. **Start broad, then narrow**: Search broad terms first
2. **Use quotes for phrases**: `"C797S mutation"` not `C797S mutation`
3. **Check recent first**: Sort by publication date for current research
4. **Review high-impact**: Check citation count for key papers
5. **Include preprints**: For cutting-edge developments

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Too many results | Add specific terms, date range |
| Too few results | Use synonyms, expand search |
| Missing recent | Check preprint servers |
| Not specific enough | Use MeSH terms |
| Overlap | Remove duplicates before analysis |

## Output Options

| Format | Description |
|--------|-------------|
| Summary (default) | Key insights, trends, top papers |
| Full | All papers with abstracts |
| BibTeX | Citation export |
| CSV | Data analysis ready |
| Markdown | Report format |
