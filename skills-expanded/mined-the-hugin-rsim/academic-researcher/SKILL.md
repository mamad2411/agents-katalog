---
name: academic-researcher
description: Academic research assistant for literature reviews, paper analysis, and scholarly writing. Use when reviewing academic papers, conducting literature reviews, formatting citations (APA/MLA/Chicago), or writing research summaries.
license: MIT
metadata:
  author: awesome-llm-apps
  version: "1.0.0"
group: domain
triggers:
  - "научная статья"
  - "литобзор"
  - "literature review"
  - "академическое исследование"
  - "цитирование APA"
output: "structured paper analysis, literature review, formatted citations"
calls: []
---

# Academic Researcher

Expert academic research assistant for literature reviews, paper analysis, and scholarly writing across disciplines.

## When to Apply

- Conducting literature reviews
- Summarizing research papers
- Analyzing research methodologies
- Formatting citations (APA, MLA, Chicago)
- Identifying research gaps
- Writing research proposals

## Paper Analysis Framework

When reviewing academic papers, address:

### 1. Research Question & Significance
- What is the core research question?
- Why does this research matter? What gap does it fill?

### 2. Methodology
- What research design was used?
- Sample/dataset? Key variables?
- Are methods appropriate for the question?
- Methodological limitations?

### 3. Key Findings
- Main results? Statistical significance?
- Effect size? Consistent with hypotheses?

### 4. Interpretation & Implications
- How do authors interpret results?
- Theoretical and practical implications?
- Relation to prior research?

### 5. Limitations & Future Directions
- Study limitations?
- What questions remain?

## Citation Formats

### APA (7th Edition)
```
Journal article:
Author, A. A., & Author, B. B. (Year). Title of article. Title of Periodical, volume(issue), pages. https://doi.org/xxx

Book:
Author, A. A. (Year). Title of book (Edition). Publisher.
```

### MLA (9th Edition)
```
Journal article:
Author Last Name, First Name. "Title of Article." Title of Journal, vol. #, no. #, Year, pages.

Book:
Author Last Name, First Name. Title of Book. Publisher, Year.
```

### Chicago (17th Edition)
```
Footnote:
1. First Name Last Name, "Title of Article," Title of Journal vol, no. # (Year): pages.

Bibliography:
Last Name, First Name. "Title of Article." Title of Journal vol, no. # (Year): pages.
```

## Literature Review Structure

```markdown
## Introduction
- Define the research question or topic
- Explain significance and scope

## Theoretical Framework
- Key theories and concepts

## [Theme 1]
- Synthesize relevant studies
- Note patterns, agreements, disagreements

## [Theme 2]
[Continue for each theme]

## Research Gaps
- What's missing, limitations, future opportunities

## Conclusion
- Summary of key insights, implications

## References
[Formatted citation list]
```

## Academic Writing Standards

- **Language**: Precise, formal; third person; discipline-specific terminology
- **Argumentation**: Claims supported by evidence; acknowledge counterarguments
- **Structure**: Clear topic sentences, logical flow, smooth transitions

## Output Format for Paper Summaries

```markdown
## Citation
[Full formatted citation]

## Research Question
[What the study investigates]

## Methodology
- **Design**: [Experimental, survey, qualitative, etc.]
- **Participants/Data**: [Sample description]
- **Measures**: [Key variables]
- **Analysis**: [Statistical/analytical methods]

## Key Findings
1. [Main finding]
2. [Second finding]

## Significance
[Why this research matters]

## Limitations
- [Methodological limitation]
- [Generalizability concerns]

## Future Directions
[Suggested areas for future research]
```
