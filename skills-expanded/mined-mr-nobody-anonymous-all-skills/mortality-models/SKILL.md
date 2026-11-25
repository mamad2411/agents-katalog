---
name: mortality-models
description: "Life tables, mortality laws, survival analysis, longevity risk modeling, and population projections"
category: actuarial
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/actuarial/mortality-models/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Mortality Models

## Scope
Mortality modeling is foundational to life insurance, pensions, and public health. This skill covers life table construction, parametric mortality laws, survival analysis, and longevity risk modeling.

## Life Tables

### Structure
| Column | Symbol | Description |
|--------|--------|-------------|
| Age | x | Exact age |
| Mortality rate | qₓ | P(death between age x and x+1 | alive at x) |
| Survival probability | pₓ | 1 - qₓ |
| Lives | lₓ | Number alive at exact age x (from radix l₀ = 100,000) |
| Deaths | dₓ | lₓ - lₓ₊₁ = lₓ · qₓ |
| Person-years lived | Lₓ | ∫₀¹ lₓ₊ₜ dt ≈ (lₓ + lₓ₊₁)/2 |
| Total future lifetime | Tₓ | Σ_{k=x}^ω Lₖ |
| Life expectancy | e̊ₓ | Tₓ/lₓ |

### Types
- **Period life table**: Cross-sectional mortality rates for a single year
- **Cohort life table**: Tracks actual birth cohort through time
- **Select life table**: Accounts for underwriting selection effect [x]+t notation

## Parametric Mortality Laws

### Classical Laws
- **Gompertz (1825)**: μₓ = Bcˣ (exponential increase with age)
  - Force of mortality increases geometrically — good fit for ages 20-90
- **Makeham (1860)**: μₓ = A + Bcˣ (adds age-independent component)
  - A captures accidents/background mortality
- **Weibull**: μₓ = kxⁿ

### Modern Models
- **Lee-Carter (1992)**: ln(mₓ,ₜ) = aₓ + bₓkₜ + εₓ,ₜ
  - aₓ = age-specific mortality pattern
  - bₓ = sensitivity of age x to mortality improvement
  - kₜ = mortality index (modeled as random walk with drift)
- **Cairns-Blake-Dowd (CBD)**: logit(qₓ,ₜ) = κₜ⁽¹⁾ + κₜ⁽²⁾(x - x̄)
  - Designed for older ages (pension modeling)
- **Renshaw-Haberman**: Lee-Carter with cohort effects

## Survival Analysis

### Key Functions
- **Survival function**: S(t) = P(T > t) = exp(-∫₀ᵗ μ(s)ds)
- **Hazard function**: h(t) = f(t)/S(t) = -d/dt ln S(t)
- **Cumulative hazard**: H(t) = ∫₀ᵗ h(s)ds = -ln S(t)

### Estimation
- **Kaplan-Meier**: Non-parametric, handles censoring: Ŝ(t) = Π_{tᵢ≤t} (1 - dᵢ/nᵢ)
- **Nelson-Aalen**: Ĥ(t) = Σ_{tᵢ≤t} dᵢ/nᵢ
- **Cox proportional hazards**: h(t|X) = h₀(t)exp(βᵀX) — semi-parametric

### Testing
- **Log-rank test**: Compare survival curves between groups
- **Likelihood ratio test**: Compare nested parametric models

## Longevity Risk
- **Basis risk**: Mismatch between hedging instrument and actual portfolio mortality
- **Longevity bonds/swaps**: Financial instruments transferring longevity risk
- **Value at Risk (VaR)**: Quantile-based risk measure for mortality uncertainty
- **Stochastic mortality projection**: Simulate future kₜ paths → distribution of liabilities

## Data Sources
- **Human Mortality Database (HMD)**: mortality.org — gold standard
- **SOA/CIA mortality tables**: Industry standard for North America
- **WHO Life Tables**: Global mortality data
- **National statistical offices**: Country-specific vital statistics

## Computational Tools
- **R**: `demography`, `StMoMo`, `survival`, `MortalityTables`
- **Python**: `lifelines` (survival analysis), `pymort`
- **Excel**: Actuarial spreadsheet models (common in practice)
- **Prophet/AXIS**: Commercial actuarial modeling software

## Professional Standards
- Actuarial Standards of Practice (ASOPs) — particularly ASOP 25 (Credibility)
- Institute and Faculty of Actuaries (IFoA) — CM1 Core Reading
- Society of Actuaries (SOA) — Exam LTAM syllabus

## References
- Dickson, Hardy & Waters — *Actuarial Mathematics for Life Contingent Risks*
- Pitacco et al. — *Modelling Longevity Dynamics for Pensions and Annuity Business*
- Cairns et al. (2009) — "A Quantitative Comparison of Stochastic Mortality Models"
