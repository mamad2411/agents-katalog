---
name: pipeline-tracker
description: |
  Global drug development pipeline tracking by disease, target, mechanism, or company.
  Use for competitive intelligence, opportunity identification, and trend analysis.

  Keywords: pipeline, drug development, clinical trials, R&D tracking, competitive landscape
category: Competitive Intelligence
tags: [pipeline, fda, clinical-trials, drug-development, tracking]
version: 1.0.0
author: Drug Discovery Team
dependencies:
  - clinicaltrials-api
  - fda-api
  - pharma-projects
  - citeline
---

# Pipeline Tracker Skill

Track global drug development pipeline across diseases, targets, and companies.

## Quick Start

```
/pipeline --target "EGFR" --by-phase
/pipeline --disease "NSCLC" --phase 2,3
/pipeline --company "AstraZeneca" --oncology
/pipeline-trends --compare 2023 vs 2024
```

## Pipeline Overview

### By Development Phase

| Phase | Description | Count (2024) | Trend |
|-------|-------------|--------------|-------|
| Preclinical | Before IND | ~15,000 | ↑ 5% |
| Phase 1 | First-in-human | ~2,500 | ↑ 8% |
| Phase 2 | Efficacy | ~1,800 | ↑ 6% |
| Phase 3 | Confirmatory | ~900 | ↑ 10% |
| Registration | Under review | ~200 | → |
| Approved | Marketed | ~1,500 | ↑ 3% |

### By Therapeutic Area

| Area | Pipeline Share | Growth |
|------|----------------|-------|
| Oncology | 38% | ↑ 12% |
| Immunology | 12% | ↑ 8% |
| Neurology | 10% | ↑ 5% |
| Cardiovascular | 8% | ↓ 2% |
| Metabolic | 8% | ↑ 3% |
| Respiratory | 6% | ↑ 4% |
| Infectious | 6% | ↓ 15% |
| Other | 12% | → |

## Output Structure

```markdown
# Pipeline Analysis: EGFR Inhibitors (2024)

## Summary

| Metric | Value | vs 2023 |
|--------|-------|--------|
| Total Programs | 245 | ↑ 12% |
| Phase 3 | 18 | ↑ 20% |
| Phase 2 | 42 | ↑ 10% |
| Phase 1 | 67 | ↑ 15% |
| Preclinical | 118 | ↑ 8% |

## By Phase

### Phase 3 Programs

| Drug | Company | Indication | Status |
|------|---------|-----------|--------|
| Lazertinib | J&J | NSCLC 1L | Recruiting |
| Nazartinib | Novartis | NSCLC 2L | Active |
| Amivantamab | J&J | NSCLC | Accelerated |
| Patritumab | Daiichi Sankyo | NSCLC | Recruiting |
| Datopotamab | Merck | NSCLC | Active |
| ... | ... | ... | ... |

### Phase 2 Programs

| Drug | Company | Indication | Differentiation |
|------|---------|-----------|-----------------|
| JDQ443 | J&J | NSCLC | CNS-penetrant |
| BPI-301 | BridgeBio | CRC | Selective |
| ... | ... | ... | ... |

## By Company

### Top 10 Companies by EGFR Pipeline

| Rank | Company | Phase 3 | Phase 2 | Phase 1 | Total |
|------|---------|---------|---------|---------|-------|
| 1 | AstraZeneca | 2 | 3 | 5 | 10 |
| 2 | J&J | 3 | 4 | 3 | 10 |
| 3 | Merck | 2 | 2 | 4 | 8 |
| 4 | Roche | 1 | 3 | 3 | 7 |
| 5 | BeiGene | 1 | 2 | 4 | 7 |
| ... | ... | ... | ... | ... | ... |

## By Mechanism

| Mechanism | Count | Trend |
|-----------|-------|-------|
| 3rd-gen TKI | 45 | ↑ |
| 4th-gen TKI (C797S) | 12 | ↑↑ |
| Bi-specific | 8 | ↑↑ |
| ADC | 15 | ↑↑ |
| Allosteric | 5 | → |
| PROTAC | 3 | ↑ |

## Pipeline Trends

### 3-Year Evolution

| Year | Phase 3 | Phase 2 | Phase 1 | Total |
|------|---------|---------|---------|-------|
| 2022 | 12 | 35 | 52 | 198 |
| 2023 | 15 | 38 | 58 | 219 |
| 2024 | 18 | 42 | 67 | 245 |

**Growth Rate**: 11% CAGR

### Key Trends

1. **4th-generation expansion**: Targeting C797S resistance
2. **ADC surge**: Antibody-drug conjugates gaining
3. **CNS focus**: Brain metastasis programs
4. **Combination trials**: 40% in combinations

## Regional Distribution

| Region | Phase 3 | Phase 2 | Phase 1 |
|--------|---------|---------|---------|
| United States | 45% | 38% | 42% |
| China | 30% | 35% | 38% |
| Europe | 25% | 20% | 18% |
| Japan | 12% | 8% | 10% |
| Rest of World | 8% | 5% | 5% |

## Innovation Assessment

### Novel Mechanisms by Phase

| Mechanism | Phase 3 | Phase 2 | Phase 1 | Preclinical |
|-----------|---------|---------|---------|------------|
| 4th-gen TKI | 3 | 5 | 4 | 8 |
| ADC | 4 | 6 | 5 | 12 |
| Bispecific | 2 | 3 | 3 | 6 |
| PROTAC | 0 | 1 | 0 | 5 |
| Allosteric | 0 | 2 | 3 | 4 |

**Innovation Index**: 32% novel mechanisms

## Competitive Dynamics

### Success Rate by Phase

| Transition | Rate | Analysis |
|------------|------|----------|
| Preclinical → Phase 1 | 15% | High risk |
| Phase 1 → Phase 2 | 60% | Improved |
| Phase 2 → Phase 3 | 35% | Major hurdle |
| Phase 3 → Approval | 65% | Strong pipeline |

### Attrition Analysis

| Reason | Phase 2 | Phase 3 |
|--------|---------|---------|
| Efficacy | 45% | 40% |
| Safety | 25% | 35% |
| Commercial | 15% | 20% |
| Strategic | 10% | 5% |

## Opportunities

### White Space

| Area | Programs | Opportunity |
|------|----------|------------|
| C797S + S1278 double mutant | 0 | High |
| Brain metastasis focus | 3 | High |
| Oral 4th-gen | 2 | Medium |
| Adjuvant setting | 4 | Medium |

## Recommendations

### For New Entrants

**Avoid**: Crowded 3rd-gen space

**Consider**:
1. **CNS-penetrant 4th-gen**: 3 programs total
2. **Double mutant coverage**: Unmet need
3. **Combination-ready**: Biomarker-selected
4. **Neoadjuvant setting**: Earlier treatment

### For Investors

**Hot Areas**:
- 4th-gen TKI (resistance focus)
- ADC platforms (established targets)
- CNS programs (large unmet need)

**Rising Stars**:
- Revolution (RMC-4630)
- BridgeBio (BPI-301)
- Cullinan (PROTAC)
```

## Running Scripts

```bash
# Target pipeline
python scripts/pipeline_tracker.py --target EGFR --by-phase

# Disease pipeline
python scripts/pipeline_tracker.py --disease "NSCLC" --phase 2,3

# Company pipeline
python scripts/pipeline_tracker.py --company "AstraZeneca" --oncology

# Trend analysis
python scripts/pipeline_tracker.py --trends 2022-2024 --target "KRAS"

# Export
python scripts/pipeline_tracker.py --export --format csv --output pipeline.csv
```

## Requirements

```bash
pip install requests pandas numpy

# Optional for advanced features
pip install plotly seaborn
```

## Reference

- [reference/data-sources.md](reference/data-sources.md) - Pipeline data sources
- [reference/analysis-methods.md](reference/analysis-methods.md) - Analysis methodologies

## Best Practices

1. **Update regularly**: Pipeline changes weekly
2. **Verify status**: Check ClinicalTrials.gov
3. **Track discontinuations: Learn from failures
4. **Monitor conferences: ASCO, ESMO for pipeline updates
5. **Include China: Major contributor to pipeline

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Stale data | Regular refresh from source APIs |
| Missing inactive trials | Include suspended/terminated |
| Geographic bias | Include global programs |
| Company name variants | Standardize company names |
| Duplicate counting | Use unique trial IDs
