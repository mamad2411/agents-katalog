---
name: secondary-research
description: "When to activate: secondary research, desk research, industry reports, data sources, Statista, Gartner, IBISWorld, citation validation, source credibility, research methodology"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: research
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Secondary Research Patterns

## Source Categories and Quality Tiers

### Tier 1: Primary Sources (Highest credibility)
- Government data (census, BLS, SEC filings)
- Academic peer-reviewed journals
- Company's own financial filings (10-K, 10-Q)
- Regulatory filings and court records
- Raw datasets from research institutions

### Tier 2: Secondary Sources (High credibility)
- Established research firms (Gartner, Forrester, IDC, McKinsey)
- Industry associations and trade groups
- Central bank publications
- Major newspapers and wire services (FT, WSJ, Reuters)
- Think tanks (Brookings, Pew Research)

### Tier 3: Tertiary Sources (Use cautiously)
- Wikipedia (verify primary sources; good for overview)
- Industry blogs and analyst commentary
- Press releases (marketing language; verify claims)
- Social media (signal detection only, not citation)

## Data Sources by Domain

### Business and Market Data
| Source | Data Type | Cost |
|--------|-----------|------|
| Statista | Market stats, consumer data, charts | Paid ($600+/yr) |
| IBISWorld | Industry reports, NAICS codes | Paid (~$1,300/report) |
| Crunchbase | Startup funding, company data | Freemium |
| PitchBook | VC/PE data, M&A | Paid (institutional) |
| CB Insights | Market trends, funding | Freemium |
| FRED (Federal Reserve) | Macro economic data | Free |
| EDGAR (SEC) | Public company filings | Free |
| Bureau of Labor Statistics | Employment, wages | Free |
| Census Bureau | Demographics, business | Free |

### Technology and IT Research
| Source | Coverage |
|--------|---------|
| Gartner | Magic Quadrant, Hype Cycle, forecasts |
| Forrester | Wave reports, analyst opinions |
| IDC | Market share, spending forecasts |
| Stack Overflow Survey | Developer tools, languages |
| State of JS/CSS | Frontend ecosystem |
| JetBrains Developer Survey | Language popularity |

### Academic Sources
| Database | Coverage | Cost |
|----------|---------|------|
| Google Scholar | Academic papers, citations | Free |
| JSTOR | Journals and books | Institutional/Paid |
| PubMed | Biomedical and life sciences | Free |
| SSRN | Social sciences preprints | Free |
| arXiv | CS, physics, math preprints | Free |
| ResearchGate | Papers + author contact | Free |
| Semantic Scholar | AI-enhanced academic search | Free |

### Consumer and Demographic Data
| Source | Coverage |
|--------|---------|
| Pew Research | Attitudes, demographics, technology |
| Nielsen | Media consumption, retail |
| Kantar | Consumer panels, brand health |
| YouGov | Public opinion, surveys |
| Morning Consult | Real-time polling |
| Eurostat | European statistics |

## Research Process

### Systematic Desk Research Protocol
```
1. Define the question precisely
   - What specific claim or gap needs to be filled?
   - What level of certainty is required?

2. Identify likely source types
   - What type of data would answer this? (quantitative/qualitative)
   - Who would collect/publish this data?

3. Search sequence
   a. Government/regulatory (most authoritative)
   b. Academic journals (peer-reviewed evidence)
   c. Major research firms (market-specific)
   d. Quality news sources (recent developments)
   e. Industry sources (practitioner knowledge)

4. Triangulate
   - Find 3+ independent sources supporting key claims
   - Note when sources contradict — investigate why

5. Document sources meticulously
   - URL, publication date, author, methodology notes
   - Note when accessed (web content can change)
```

### Search Operators for Research
```
Google advanced search:
site:gartner.com "cloud market" 2024
filetype:pdf "market report" "SaaS" 2023
"market size" "$" billion "CAGR" "2024" -site:press-release.com

Google Scholar:
"machine learning" "fraud detection" after:2021

EDGAR full-text search:
EDGAR → Full-Text Search → search 10-K filings
```

## Source Credibility Assessment

### CRAAP Test
| Criteria | Questions |
|----------|----------|
| **Currency** | When was it published/updated? Is it recent enough? |
| **Relevance** | Does it answer your specific question? Right audience? |
| **Authority** | Who created it? What are their credentials? |
| **Accuracy** | Are claims supported? Peer reviewed? Citations present? |
| **Purpose** | Why was it created? Marketing, advocacy, or informing? |

### Red Flags
- No author or anonymous
- No publication date
- No citations or methodology
- Published by an organization with a financial stake
- Contradicted by multiple other sources
- Uses emotional language in factual claims
- URL ending in `.com` for statistical claims (prefer `.gov`, `.edu`, `.org`)

### Paywalled Content Access
```
Legitimate free options:
- Institutional library access (university alumni cards)
- Interlibrary loan
- Author's ResearchGate profile (often shares freely)
- Preprint on arXiv or SSRN
- Open Access version (Unpaywall browser extension)
- Google Scholar → "All X versions" for OA copy
- Email the corresponding author directly
```

## Citation Management

### Citation Formats
```
APA 7th (common in business and social science):
Smith, J. A., & Jones, B. (2023). Market dynamics in SaaS. 
Journal of Business Research, 45(2), 123–145.
https://doi.org/10.xxxx/xxx

Chicago (footnote style, common in humanities):
Smith, John A. "Market dynamics in SaaS." Journal of Business Research 
45, no. 2 (2023): 123–145.

For web sources (APA):
Gartner. (2024, March). Magic Quadrant for Cloud Infrastructure. 
Retrieved April 15, 2024, from https://www.gartner.com/...
```

### Research Log Template
```
Research Question: _______________
Date: ___

| Source | URL/DOI | Date Published | Key Finding | Credibility | Notes |
|--------|---------|---------------|-------------|-------------|-------|
| Gartner | [url] | 2024-01 | Cloud market $600B | Tier 2 | Subscription required |
| BLS | [url] | 2024-02 | Unemployment 3.9% | Tier 1 | — |
| TechCrunch | [url] | 2024-03 | X raises $50M | Tier 3 | Verify with Crunchbase |

Synthesis notes:
- Sources agree on: ___
- Sources conflict on: ___
- Gaps remaining: ___
```

## Working with Reports

### Extracting Value from Paid Reports
```
Gartner Magic Quadrant — read:
1. Criteria for inclusion (who was evaluated)
2. Your vendor's position and description
3. Competitors' positions and strengths/cautions
4. Gartner's market definition and size estimate

Forrester Wave — look for:
1. Score breakdowns (strategy vs. current offering)
2. Vendor-specific commentary
3. Market trend analysis in introduction

McKinsey/BCG Reports:
1. Executive summary first
2. Methodology appendix (sample size? scope?)
3. Headline stats + context around them
4. Check if commissioned by an industry group
```

### Chart and Statistic Verification
```
Before citing a statistic, verify:
□ Original source (not a chain of citations)
□ Sample size and methodology
□ Date of data collection (vs publication date)
□ Scope (geography, industry, company size)
□ Whether it's been updated since
□ Full context (sometimes headline contradicts detail)

Common misquotation pattern:
Report: "X% of companies that have implemented Y see benefit Z"
→ Often cited as "X% of companies use Y"
Always read original to confirm what was actually measured
```
