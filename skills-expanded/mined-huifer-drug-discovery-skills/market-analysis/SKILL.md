---
name: market-analysis
description: |
  Market sizing, epidemiology, and commercial opportunity assessment for
  drug development. Use for market forecasts, opportunity evaluation, and
  investment decisions.

  Keywords: market, epidemiology, prevalence, forecast, sizing, opportunity
category: Market Analysis
tags: [market, epidemiology, forecast, sizing, commercial]
version: 1.0.0
author: Drug Discovery Team
dependencies:
  - gbd-database
  - ihme-database
  - who-database
---

# Market Analysis Skill

Epidemiology and market opportunity assessment for drug development.

## Quick Start

```
/market NSCLC
/market-forecast "EGFR inhibitor" --region China
/epi lung cancer --country US
Analyze market opportunity for KRAS G12C inhibitors
```

## What's Included

| Section | Description | Data Source |
|---------|-------------|-------------|
| Epidemiology | Prevalence, incidence, mortality | GBD, IHME, WHO |
| Patient Population | Diagnosed, treatable, addressable | Derived |
| Market Sizing | Current and forecasted market | Multi-source |
| Competitive Market | Branded/generic split | Claims data |
| Pricing Analysis | Price benchmarks | Payers, registries |
| Access & Reimbursement | Coverage by country | HTA agencies |

## Output Structure

```markdown
# Market Analysis: EGFR-Mutated NSCLC

## Executive Summary
**Total Addressable Market**: $12.3B globally (2024)
**Growth Rate**: 8.5% CAGR to 2030
**Key Drivers**: Increased testing, targeted therapies, emerging markets
**Barriers**: Generic competition, resistance mechanisms

## Epidemiology

### Global Burden
| Metric | Value | Source |
|--------|-------|--------|
| New Cases (2024) | 2.2M | GBD 2024 |
| Prevalence | 3.8M | IHME 2024 |
| Deaths | 1.8M | WHO 2024 |
| EGFR Mutation Rate | 15-20% | Literature |

### By Region
| Region | New Cases | EGFR+ | Treatable |
|--------|-----------|------|----------|
| China | 850K | 150K | 100K |
| US | 235K | 42K | 38K |
| EU | 320K | 55K | 48K |
| Japan | 95K | 18K | 17K |

## Patient Flow Funnel
```
New NSCLC Cases: 2,200,000
         ↓ (80% tested)
EGFR Tested: 1,760,000
         ↓ (17% positive)
EGFR Positive: 300,000
         ↓ (70% treatment-eligible)
Treatable Population: 210,000
         ↓ (80% access)
Addressable Market: 168,000
```

## Market Sizing

### Current Market (2024)
| Segment | Patients | Price/Patient | Market |
|---------|----------|---------------|--------|
| 1st-line TKI | 90K | $80,000 | $7.2B |
| 2nd-line TKI | 35K | $60,000 | $2.1B |
| 3rd-line TKI | 30K | $120,000 | $3.6B |
| Chemo + | 13K | $30,000 | $0.4B |
| **Total** | **168K** | - | **$13.3B** |

### Forecast to 2030
| Year | Addressable | Price/Patient | Market |
|------|-------------|---------------|--------|
| 2024 | 168K | $79K | $13.3B |
| 2025 | 178K | $78K | $13.9B |
| 2026 | 188K | $77K | $14.5B |
| 2027 | 198K | $76K | $15.0B |
| 2028 | 208K | $75K | $15.6B |
| 2029 | 218K | $74K | $16.1B |
| 2030 | 228K | $73K | $16.6B |

**CAGR**: 4.3% (volume), 3.8% (value)

## Competitive Market

### Market Share (2024)
| Drug | Share | Sales |
|------|-------|-------|
| Osimertinib | 65% | $8.6B |
| Erlotinib | 10% | $1.3B |
| Gefitinib | 8% | $1.1B |
| Afatinib | 5% | $0.7B |
| Others | 12% | $1.6B |

### Generic Impact
| Year | Generic Erosion | Market Impact |
|------|-----------------|---------------|
| 2024 | 5% | Erlotinib US |
| 2025 | 15% | Gefitinib EU |
| 2026 | 25% | 1st-gen overall |
| 2027+ | 40% | Significant |

## Pricing Analysis

### Price Benchmarks by Country
| Country | Annual Price | Relative to US |
|---------|--------------|-----------------|
| US | $120K | 100% |
| Germany | $85K | 71% |
| China | $45K | 38% |
| Japan | $70K | 58% |
| UK | $65K | 54% |

### Price Trend
**Direction:** Gradual decline due to:
- Generic competition
- HTA pressure
- Value-based pricing
- Emerging market discounts

## Access & Reimbursement

### Coverage by Major Markets
| Country | Public Coverage | Criteria | Restrictions |
|----------|-----------------|----------|-------------|
| US | Medicare/Medicaid | EGFR+ | Prior auth |
| Germany | Statutory | EGFR+ | Line-specific |
| China | Basic Insurance | EGFR+ | Local reimbursement |
| Japan | National | EGFR+ | D.I.N. approval |

## Key Opportunities
1. **Untested regions**: Africa, SE Asia testing <40%
2. **Resistance market**: 30-40% develop resistance
3. **Adjuvant setting**: Expanding indication
4. **Combination therapies**: Chemo +, anti-angiogenic

## Key Risks
1. **Generic erosion**: 1st-gen largely generic
2. **Resistance limits**: C797S challenges
3. **Pricing pressure**: HTA-driven discounts
4. **New competition**: 4th-gen in development
```

## Examples

### Disease Market
```
/market NSCLC
/market-forecast "colorectal cancer" --region global
```

### Drug Market
```
/market "EGFR inhibitors" --forecast 10years
Analyze market size for KRAS G12C drugs
```

### Epidemiology
```
/epi lung cancer --country China
/epi "solid tumors" --age 65+
```

### Pricing Analysis
```
/market oncology drugs --pricing --compare US,EU,CN
Analyze TKI pricing across Asia
```

## Running Scripts

```bash
# Market sizing
python scripts/market_analysis.py --condition "NSCLC" --target "EGFR" -o market.json

# Epidemiology data
python scripts/epi_fetch.py --cancer "lung" --demographics -o epi.json

# Price comparison
python scripts/price_analysis.py --drug "osimertinib" --countries US,CN,JP,EU

# Forecast model
python scripts/forecast.py --historical 2018-2024 --forecast 2025-2030
```

## Requirements

```bash
pip install requests pandas numpy
```

## Additional Resources

- [GBD Data](reference/gbd-api.md)
- [IHME Resources](reference/ihme-resources.md)
- [Market Sizing Methodology](reference/market-methodology.md)

## Best Practices

1. **Define funnel clearly**: incidence → tested → positive → treated
2. **Use multiple sources**: Cross-reference epidemiology
3. **Check testing rates**: Vary significantly by region
4. **Consider generics**: Impact on market size
5. **Validate pricing**: Use real-world price data

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Incidence ≠ prevalence | Distinguish clearly |
| Ignoring testing rates | Affects addressable market |
| Static pricing | Prices decline over time |
| Overestimating access | Real-world access <100% |
| Ignoring generics | Generic impact grows over time |
