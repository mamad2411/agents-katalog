---
name: patent-search
description: |
  Search and analyze patents including FTO (Freedom to Operate) analysis,
  patent landscape mapping, and competitive IP intelligence.

  Keywords: patent, FTO, freedom to operate, IP, intellectual property
category: Patent Analysis
tags: [patent, fto, ip, landscape, claims]
version: 1.0.0
author: Drug Discovery Team
dependencies:
  - uspto-database
  - epo-database
  - wipo-database
---

# Patent Search Skill

Comprehensive patent analysis for drug discovery and IP intelligence.

## Quick Start

```
/patent EGFR inhibitor
/fto "quinazoline EGFR kinase"
/patent-map KRAS G12C
Analyze patent landscape for osimertinib
```

## What's Included

| Section | Description | Data Source |
|---------|-------------|-------------|
| Patent Search | Find relevant patents | USPTO, EPO, WIPO |
| Patent Details | Claims, assignees, priority | Patent databases |
| FTO Analysis | Freedom to operate assessment | Claims analysis |
| Landscape Map | Patent clustering and gaps | Aggregated |
| Expiration | Patent expiry dates | Patent databases |
| Family Analysis | Patent family members | Global Dossier |

## Output Structure

```markdown
# Patent Analysis: EGFR Inhibitors

## Executive Summary
**Total Patents**: 3,247 EGFR inhibitor patents found
**Key Patent Families**: 89 unique families
**FTO Risk**: High - crowded landscape with broad claims

## Patent Landscape
| Time Period | Patents | Growth |
|-------------|---------|--------|
| 1990-1999 | 234 | Baseline |
| 2000-2009 | 892 | +281% |
| 2010-2019 | 1,456 | +63% |
| 2020-2024 | 665 | Declining |

## Key Patent Families

### US5747498 (Erlotinib)
| Field | Value |
|-------|-------|
| Assignee | OSI Pharmaceuticals |
| Priority Date | 1994-04-15 |
| Grant Date | 1998-05-05 |
| Expiry | 2018 (expired) |
| Claims | 47 claims |
| Scope | Quinazoline EGFR inhibitors |

### US8017621 (Gefitinib)
| Field | Value |
|-------|-------|
| Assignee | AstraZeneca |
| Priority Date | 1992-03-06 |
| Expiry | 2014 (expired) |
| Scope | Broad EGFR TKI claims |

## FTO Analysis

### High-Risk Patents
| Patent | Risk | Reason |
|--------|------|--------|
| US8772358 | ⚠️ High | 3rd-gen TKI, C797S active |
| US10363010 | ⚠️ High | Broad mutant-selective claims |
| US10588034 | ⚠️ High | Combination therapy claims |

### White Space
| Area | Opportunity | Rationale |
|------|-------------|----------|
| 4th-gen TKI | Low IP pressure | C797S+S1278 niche |
| Allosteric sites | Emerging | Fewer existing claims |
| Bispecific formats | Moderate | Combination IP possible |

## Patent Family Analysis
**Example: Osimertinib (AZD9291)**

| Jurisdiction | Patent | Status | Expiry |
|-------------|--------|--------|--------|
| US | US8772358 | Expired | 2033 |
| EP | EP2378967 | Granted | 2033 |
| JP | JP5958971 | Granted | 2033 |
| CN | CN102822420 | Granted | 2033 |

## Claim Analysis
**US8772358 Claim 1 (Representative):**
```
A compound of formula (I) or a pharmaceutically acceptable salt thereof,
for use in the treatment of a proliferative disease mediated by EGFR
having the T790M mutation...
```

**Breadth:** Broad - covers mutant-selective EGFR inhibitors
**Enforceability:** High - well-defined structure
**Workaround:** Difficult - covers core scaffold

## Competitive IP Map
| Company | Patent Families | Core Focus |
|----------|-----------------|-------------|
| AstraZeneca | 12 | 3rd-gen TKI, combinations |
| Johnson & Johnson | 8 | Bispecific antibodies |
| Daiichi Sankyo | 6 | ADC conjugates |
| Blueprint Medicines | 4 | 4th-gen TKI |
| Yuhan/Roche | 3 | Lazertinib combinations |
```

## Examples

### Patent Search
```
/patent EGFR quinazoline
/patent-search "KRAS G12C inhibitor"
Find all patents for sotorasib
```

### FTO Analysis
```
/fto "EGFR TKI scaffold"
/fto-analysis compound.smi
Can I make this compound without infringement?
```

### Landscape Mapping
```
/patent-map KRAS inhibitors
Map patent landscape for 4th-gen EGFR
Analyze IP gaps in PROTAC EGFR degraders
```

### Patent Family
```
/patent US8772358 --family
/patent WO2010130291 --global
Show all related patents for osimertinib
```

## Running Scripts

```bash
# Search patents by keyword
python scripts/patent_search.py "EGFR inhibitor" --output patents.json

# FTO analysis
python scripts/patent_search.py --fto "quinazoline scaffold" --claims

# Patent family lookup
python scripts/patent_search.py --family US8772358

# Landscape mapping
python scripts/patent_search.py --landscape "KRAS G12C" --cluster

# Expiration analysis
python scripts/patent_search.py --expiry "EGFR TKI" --sort-by-date
```

## Requirements

```bash
pip install requests pandas lxml
```

## Additional Resources

- [USPTO API Reference](reference/uspto-api.md)
- [EPO Register](reference/epo-resources.md)
- [FTO Methodology](reference/fto-methodology.md)

## Best Practices

1. **Start broad**: Cast wide net, then filter
2. **Check families**: Patents span multiple jurisdictions
3. **Read claims**: Scope determined by claims, not abstract
4. **Check expiry**: Many drug patents expired
5. **Consider licenses**: Blocked ≠ impossible (licensing possible)

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Narrow search | Use multiple terms/synonyms |
| Ignoring families | Check global coverage |
| Misreading claims | Claims define scope, not title |
| Overlooked continuations | Check continuation-in-part (CIP) |
| Publication vs. grant | Check granted patent status |
