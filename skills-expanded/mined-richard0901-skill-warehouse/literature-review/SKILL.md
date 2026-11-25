---
name: literature-review
description: Academic literature review workflow for research topic selection. Use when user asks to do literature survey, research topic exploration, or systematic review for a specific field. Triggers include: "literature review for [field]", "research topic selection", "help me design a search strategy", "systematic literature search", or when user describes a multi-step research workflow involving database searching, relevance assessment, journal filtering, and topic analysis.
---

# Literature Review Workflow

A systematic workflow for academic literature survey and research topic selection.

## Workflow Overview

```
1. Research Background -> Generate Search Query
2. Execute Search (PubMed/Scopus/Semantic Scholar)
3. Relevance Assessment (50% threshold)
4. Query Optimization (if needed)
5. Journal Stratification & Filtering
6. Deep Analysis & Topic Mining
```

## Step 1: Generate Search Query

### Prompt Template
```
I need to conduct a literature review for the "[RESEARCH_FIELD]" field to select a research direction. Please design an advanced search query for Scopus/PubMed.

Requirements:
- Include all naming variants
- Use TITLE-ABS-KEY (Scopus) or [Title/Abstract] (PubMed) for field-level search
- Exclude irrelevant literature using TITLE-level exclusion
```

### Naming Variant Discovery

Before generating query, identify all relevant terms:

| Source | Method |
|--------|--------|
| English full names | Standard terminology |
| Abbreviations | Common acronyms (caution: may cause false positives) |
| Variant spellings | Different spellings (e.g., "Crohn's" vs "Crohn") |
| Subtypes | Disease subtypes, related conditions |

### Query Templates

**Scopus:**
```
TITLE-ABS-KEY("term1" OR "term2" OR "term3") AND NOT TITLE("exclude1" OR "exclude2")
```

**PubMed:**
```
("term1"[Title/Abstract] OR "term2"[Title/Abstract]) NOT ("exclude1"[Title] OR "exclude2"[Title])
```

### Common Exclusions

| Exclusion | Reason |
|-----------|--------|
| `irritable bowel syndrome` / `IBS` | Common confusion |
| `case report` | Low evidence level |
| `case presentation` | Low evidence level |
| Field-specific: `gynecolog`, `oncolog` | Exclude non-target specialties |

## Step 2: Execute Search

### Database Selection

| Database | Best For |
|----------|----------|
| PubMed | Biomedical/clinical research |
| Scopus | Comprehensive coverage |
| Semantic Scholar | AI-powered, but API rate limited |

### Search Execution via Browser

1. Navigate to database URL with encoded query
2. Apply filters if needed (publication date, article type)
3. Capture total results and first 10-20 papers

### PubMed URL Template
```
https://pubmed.ncbi.nlm.nih.gov/?term=ENCODED_QUERY&sort=date
```

## Step 3: Relevance Assessment

### Assessment Criteria

For top 10-20 papers (sorted by date, newest first):

| Score | Criteria |
|-------|----------|
| Directly relevant | Core topic, primary focus |
| Relevant | Significant discussion of topic |
| Marginally relevant | Mentioned in passing |
| Not relevant | Different field, wrong context |

### Pass Threshold

- **50% match rate** (e.g., 5/10 or 10/20 relevant or higher)
- If failed, proceed to query optimization

### Assessment Prompt
```
Evaluate the following [N] papers for relevance to [RESEARCH_FIELD]:

[LIST OF TITLES]

Rate each as: Directly relevant / Relevant / Marginally relevant / Not relevant
Calculate match rate and recommend next steps.
```

## Step 4: Query Optimization

### If Match Rate < 50%

Analyze why irrelevant papers were retrieved:

| Problem | Solution |
|---------|----------|
| Term too broad | Remove or qualify the term |
| Missing exclusions | Add exclusion terms to TITLE filter |
| False positives from abbreviations | Remove abbreviation, use full terms only |
| Non-target fields appearing | Add field-specific exclusions |

### Optimization Prompt
```
The search query returned these papers but many are irrelevant:

[LIST OF IRRELEVANT PAPERS WITH TITLES]

Analyze why each irrelevant paper was retrieved and propose specific query modifications.
```

### Iterate

1. Modify query based on analysis
2. Re-run search
3. Re-assess match rate
4. Repeat until >= 50% match rate achieved

## Step 5: Journal Stratification & Filtering

### Journal Quality Tiers

| Tier | IF Range | Characteristics |
|------|----------|-----------------|
| Top | >10 | Field-leading, high impact |
| High | 5-10 | Strong reputation |
| Medium | 3-5 | Solid, specialized |
| Standard | <3 | General, regional |

### Field-Specific Top Journals

For each research field, identify the top journals:

**Example (Gastroenterology):**
- Lancet Gastroenterology & Hepatology (IF ~45)
- Gastroenterology (IF ~29)
- Gut (IF ~24)
- Journal of Crohn's and Colitis (IF ~10)

### Filtering Strategy

1. Identify top 5-10 journals in the field
2. Filter results to focus on high-quality sources
3. Use for subsequent deep analysis

## Step 6: Deep Analysis & Topic Mining

### Analysis Framework

#### 1. Dynamic Topic Evolution

| Category | Indicators |
|----------|------------|
| Evergreen (stable/growing) | 5-year consistent publication, steady citations |
| Emerging (1-2 years) | Rapid growth, new methodology/technology |
| Declining (saturated) | Decreasing publications, well-established knowledge |

#### 2. Journal Preferences

Analyze top journals' editorial preferences:

| Journal | Preference |
|---------|------------|
| Mechanism-focused | Basic research, pathways |
| Clinical-focused | RCTs, real-world evidence |
| Methods-focused | New techniques, AI applications |

#### 3. High-Frequency Keyword Combinations

Identify patterns:
- Method + Disease subtype
- Population + Intervention
- Biomarker + Outcome

#### 4. Research Opportunity Mining

**Overcrowded areas:** Avoid (high competition, limited novelty)

**Promising directions (by difficulty):**

| Level | Characteristics | Risk/Reward |
|-------|----------------|-------------|
| Basic | Survey, simple analysis | Low risk, modest contribution |
| Medium | Cohort study, method application | Moderate risk, good contribution |
| Advanced | Novel mechanism, new intervention | High risk, high impact potential |

### Analysis Output Format

```
## Topic Evolution Analysis
- Evergreen topics: [list with rationale]
- Emerging topics: [list with growth indicators]
- Declining topics: [list with saturation evidence]

## Journal Preferences
[journal-by-journal analysis]

## Keyword Combinations
[high-frequency patterns]

## Research Opportunities
- Overcrowded: [areas to avoid]
- Promising: [5 directions with difficulty levels]
```

## Quick Reference: Workflow Checklist

- [ ] Identify research field and background
- [ ] Discover naming variants and synonyms
- [ ] Generate initial search query
- [ ] Execute search on database
- [ ] Assess relevance (target: 50%+)
- [ ] Optimize query if needed
- [ ] Identify top journals in field
- [ ] Filter for high-quality sources
- [ ] Perform deep topic analysis
- [ ] Generate research direction recommendations

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Query too narrow | Include synonyms, check spelling variants |
| Query too broad | Add exclusions, use phrase searching |
| Missing key terms | Consult MeSH terms, field experts |
| Irrelevant results | Analyze false positives, add exclusions |
| Low-quality sources | Apply journal filters, check impact factors |