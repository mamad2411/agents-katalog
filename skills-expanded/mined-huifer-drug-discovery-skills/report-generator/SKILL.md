---
name: report-generator
description: |
  Generate professional drug discovery reports including target dossiers,
  competitive briefs, and Go/No-Go decision summaries.

  Use this skill when you need formatted reports for presentations,
  decision meetings, or documentation. Supports multiple output formats.

  Keywords: report, dossier, decision, go-no-go, brief, presentation
category: Report Generation
tags: [report, dossier, decision, go-no-go]
version: 1.0.0
author: Drug Discovery Team
dependencies: []
---

# Report Generator Skill

Generate professional drug discovery intelligence reports.

## Quick Start

```
/dossier EGFR --format pdf
/brief EGFR competitors --format ppt
/gng project-KRAS --full
/report --template competitor-brief
Generate a Go/No-Go report for HER2 inhibitor project
```

## What's Included

| Report Type | Description | Use Case |
|-------------|-------------|----------|
| **Target Dossier** | Comprehensive target analysis | Target validation meetings |
| **Competitor Brief** | Competitive intelligence summary | Portfolio reviews |
| **Go/No-Go** | Decision support with scoring | Investment decisions |
| **Weekly Update** | Weekly intelligence summary | Team updates |
| **Project Overview** | Full project analysis | Stakeholder reports |

## Report Types

### 1. Target Dossier (`/dossier`)

Comprehensive target analysis for validation decisions.

**Sections:**
- Executive Summary (1 page)
- Target Overview
- Druggability Assessment
- Disease Associations
- Competitive Landscape
- Safety Assessment
- Opportunities & Risks
- Recommendations

**Output:** PDF (10-15 pages)

```
/dossier EGFR
/target-dossier KRAS G12C --format pdf
Generate dossier for BRAF V600E
```

### 2. Competitor Brief (`/brief`)

Competitive intelligence summary for portfolio reviews.

**Sections:**
- Market Overview
- Approved Products
- Pipeline Analysis
- Company Landscape
- Key Differentiators
- White Space

**Output:** PPT (8-12 slides)

```
/brief EGFR inhibitors
/competitor-brief GLP-1 agonists --format ppt
Create competitor brief for obesity market
```

### 3. Go/No-Go Analysis (`/gng`)

Decision support with multi-dimensional scoring.

**Scoring Dimensions:**

| Dimension | Weight | Assessment Criteria |
|-----------|--------|---------------------|
| Scientific Rationale | 25% | Target validation, disease linkage strength |
| Differentiation | 20% | Competitive advantage, novelty |
| Feasibility | 20% | Technical feasibility, developability |
| Commercial | 20% | Market size, unmet need, pricing |
| IP/Safety | 15% | Patentability, safety risk |

**Score Interpretation:**
- **80-100**: Strong Go - Proceed with confidence
- **60-79**: Go with conditions - Address specific concerns
- **40-59**: Caution - Significant concerns, re-evaluate
- **0-39**: No-Go - Do not proceed

**Output:** PDF with scorecard (5-8 pages)

```
/gng project-EGFR-4thgen
/go-no-go KRAS inhibitor --full
Generate Go/No-Go analysis for ADC program
```

### 4. Weekly Update (`/weekly`)

Weekly intelligence summary for team alignment.

**Sections:**
- Key Developments
- Literature Highlights
- Pipeline Updates
- Conference Abstracts
- Deals & News

**Output:** Email/Markdown (1-2 pages)

```
/weekly --targets EGFR,KRAS,HER2
/weekly-update --diseases NSCLC,CRC
Generate weekly report for oncology portfolio
```

### 5. Project Overview (`/report --full`)

Complete analysis combining all above sections.

**Output:** Full report (30-50 pages)

```
/report --full EGFR program
/generate full project report for KRAS G12C
```

## Output Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| **Markdown** | Default, fully formatted | Quick review, version control |
| **PDF** | Professional report | Meetings, archives |
| **PPT** | Slide deck | Presentations |
| **One-pager** | Single page summary | Executive updates |

## Go/No-Go Scoring Example

```markdown
# Go/No-Go Analysis: KRAS G12C Inhibitor Project

## Overall Score: 72/100 (Go with Conditions)

### Dimension Scores

| Dimension | Score | Weight | Weighted | Status |
|-----------|-------|--------|----------|--------|
| Scientific Rationale | 85/100 | 25% | 21.25 | ✅ Strong |
| Differentiation | 65/100 | 20% | 13.00 | ⚠️ Moderate |
| Feasibility | 75/100 | 20% | 15.00 | ✅ Good |
| Commercial | 80/100 | 20% | 16.00 | ✅ Strong |
| IP/Safety | 50/100 | 15% | 7.50 | ⚠️ Concern |

### Detailed Assessment

#### Scientific Rationale (85/100) ✅
**Strengths:**
- KRAS G12C validated in NSCLC, CRC
- Strong genetic association
- Clear mechanism of action

**Score:** 85/100

#### Differentiation (65/100) ⚠️
**Strengths:**
- First-in-class opportunity
- Novel covalent binding

**Concerns:**
- 4 competitors in Phase II/III
- Amgen and Mirati ahead

**Score:** 65/100

#### Feasibility (75/100) ✅
**Strengths:**
- Proven chemistry platform
- Clear PK/PD biomarkers

**Concerns:**
- Resistance mutations observed
- Combination complexity

**Score:** 75/100

#### Commercial (80/100) ✅
**Strengths:**
- Large NSCLC market
- Premium pricing potential
- Expansion to CRC, pancreatic

**Score:** 80/100

#### IP/Safety (50/100) ⚠️
**Concerns:**
- Patent landscape crowded
- Off-target toxicity risks
- Sotorasib safety signals

**Score:** 50/100

### Conditions to Proceed

1. **IP:** Conduct FTO analysis, explore novel binding pocket
2. **Safety:** Early toxicity profiling, off-target screening
3. **Differentiation:** Focus on combination strategies, CNS penetration

### Recommendation
**PROCEED with Conditions** - Strong scientific and commercial rationale,
but address IP position and safety profile before major investment.
```

## Examples

### Target Dossier
```
/dossier EGFR
Generate a target dossier for HER2
/target-dossier KRAS --focus safety
```

### Competitor Brief
```
/brief EGFR TKIs
Create competitor brief for obesity drugs
/competitor-brief GLP-1 --format ppt --include-privates
```

### Go/No-Go
```
/gng my-project-name
/go-no-go KRAS G12C --full
Generate decision report for ADC platform
```

### Weekly Update
```
/weekly
/weekly-update --targets EGFR,KRAS --format email
```

### Custom Report
```
/report --template custom --sections exec-sum,market,competition
/generate report using template project-overview
```

## Running Scripts

```bash
# Generate dossier
python scripts/generate_dossier.py EGFR --format pdf --output reports/

# Generate brief
python scripts/generate_brief.py "EGFR inhibitors" --format ppt

# Go/No-Go with custom weights
python scripts/generate_gng.py project-name --weights science=30,diff=15

# Weekly report
python scripts/weekly_report.py --targets EGFR,KRAS,HER2 --format email
```

## Requirements

For PDF/PPT generation:
```bash
pip install weasyprint python-pptx jinja2 pandas
```

## Additional Resources

- [Template Reference](reference/templates.md)
- [Customization Guide](reference/customization.md)
- [Script Usage](reference/scripts.md)

## Best Practices

1. **Specify format**: Always include output format
2. **Use templates**: Reference existing templates for consistency
3. **Include context**: Add project-specific considerations
4. **Review scores**: Validate Go/No-Go assumptions
5. **Version control**: Track report iterations

## Report Templates

Templates are in `templates/` directory:

```
templates/
├── target-dossier.md      # Target validation report
├── competitor-brief.md    # Competitive intelligence
├── go-no-go.md            # Decision support
├── weekly-update.md       # Weekly intelligence
└── project-overview.md    # Full project analysis
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Missing context | Include project background |
| Generic scores | Customize weights by project |
| Outdated data | Always refresh data before report |
| Too long | Use executive summary |
| Wrong format | Verify format before generation |
