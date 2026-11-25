---
name: cropland-out-of-production-agreements
description: Use when analyzing ongoing agricultural productivity impacts from transmission line, pipeline, or linear infrastructure right-of-way agreements, running three-model NPV comparisons (Ontario one-time vs Alberta SRB annual vs Farmer Required actual costs), quantifying operational inefficiencies (headlands loss, precision ag interference, aerial spray restrictions, weed control), or advocating for annual cropland compensation based on OFA guidance.
---

## What Constitutes "Cropland Out of Production"

### Complete Out of Production

**Tower/structure footprint**: Land physically occupied by structure where NO farming possible. Footprint scales with voltage class — from 15-20 m² for 69kV H-frames up to 80-120 m² for 500kV lattice towers. Per-voltage footprint sizes and headland calculation tables → see [`impact-quantification.md`](impact-quantification.md).

**Example**: 230kV transmission line, 12 towers across 100-acre farm → 12 × 50 m² = 600 m² = 0.15 acres of direct tower footprint (complete out of production).

### Partial Out of Production (Operational Inefficiency)

**Internal headlands**: Turning space required around each tower. Typical impact per tower: 20-30 meter diameter circle (300-700 m² lost productivity per structure).

**Example**: 100-acre farm, 12 towers, 25m diameter headlands per tower → 12 × 490 m² = 5,880 m² = 1.45 acres partial loss. Combined with 0.15-acre tower footprints, total impact = 1.6 acres (1.6% of farm).

### Right-of-Way Operational Restrictions

Activities restricted within ROW even where farming continues:

- **Aerial spraying**: Prohibited within 15-30m of conductors; must ground-spray ROW (10× cost, 3× time vs aerial). Cost differential roughly $450/ha annually for 500kV-class lines.
- **Irrigation**: Pivot irrigation cannot cross conductors (height clearance); forces linear move conversion ($120,000 capital + 15% efficiency loss).
- **Precision agriculture**: GPS signal distortion 10-20m either side of conductors; auto-steer malfunction requires manual steering with 5-10% input overlap (seed/fertilizer/pesticide waste).
- **Weed control**: Cannot spray within 2-3m of tower legs; manual control required at roughly $50/tower/year.
- **Equipment damage risk**: Guy wires, anchor points, tower legs as collision hazards. Expected annual cost typically 1-5% probability × $500-$50,000 damage per tower.

Full quantification methodology with dollar examples for each impact category → [`impact-quantification.md`](impact-quantification.md).

## Compensation Structures: One-Time vs. Annual

### Ontario Model (Hydro One — Current Practice)

**One-time easement payment**: Market value of easement (typically 10-25% of fee simple value).

**Theoretical potential profit loss** (6-year period only):
- Calculation: (Land value before − Land value after) + Crop costs + Ongoing impact injury
- Payment: Lump sum at easement grant
- **After year 6**: NO ongoing compensation despite 50+ year infrastructure lifespan

**Worked example**: 2 hectares agricultural land at $30,000/hectare fee simple value → easement value 15% × 2 × $30,000 = $9,000 one-time; theoretical profit loss 6 yrs × 2 ha × $500/ha = $6,000; total $15,000 paid once.

**Not covered**: Annual expenses after year 6 (internal headlands, labor, weed control), increased equipment operating costs over 50+ year structure lifespan, productivity loss from operational inefficiencies, equipment damage risk.

### Alberta Model (ATCO Electric — Surface Rights Board)

**Per-structure annual compensation** in addition to one-time easement, paid every year for life of structure (50-80 years), reviewed at 5-year intervals.

**2021 rates** (Hart v ATCO Electric Ltd):
- **$1,380/year** per structure on cultivated lands
- **$552/year** per structure on uncultivated lands
- **$690/year** per structure on headlands

**Additional Alberta one-time payments**: $1,300/acre easement, $7,500 quarter-section signing bonus, $10,000 Early Resolution Access Agreement (ERAA) incentive.

**Worked example**: 230kV line, 12 towers on 100-acre farm, 10 cultivated + 2 headlands → annual (10 × $1,380) + (2 × $690) = $15,180/year. NPV @ 5%, 50 years = $15,180 × 18.26 = **$277,187**. Compared to Ontario $15,000 single payment for similar farm: **18× higher**.

### OFA Advocacy Position (83% Member Support)

**OFA Resolution** (November 2024 AGM): Lobby Hydro One to provide **annual compensation** matching Alberta SRB per-structure model. Rationale: Alberta farmers receive annual for identical impacts; Ontario natural gas pipelines (Enbridge, TCPL) already pay annual ROW compensation; equity demands parity.

Full OFA factsheet inventory, negotiation playbook, common pitfalls, and pushback/counter scripts → [`ofa-guidance.md`](ofa-guidance.md).

## Automated Three-Model NPV Comparison (cropland_calculator.py)

For systematic, repeatable agricultural easement compensation analysis, use the bundled calculator located alongside this skill.

**Script path**: `${CLAUDE_PLUGIN_ROOT}/skills/cropland-out-of-production-agreements/cropland_calculator.py`

**Purpose**: Compare three compensation models side-by-side with full NPV math and sensitivity analysis:

1. **Ontario Hydro One (Current Practice)** — One-time easement + 6-year theoretical profit loss; NO annual ongoing compensation.
2. **Alberta Surface Rights Board (2021 Rates)** — One-time easement + per-structure annual compensation paid for life of structure with 5-year review intervals.
3. **Farmer Required (Documented Actual Costs)** — One-time easement + annual compensation calculated from farm-specific impact categories (headlands, aerial spray, precision ag, labor, weed control, equipment damage, irrigation).

### Invocation

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/cropland-out-of-production-agreements
python3 cropland_calculator.py /path/to/input.json --output results.json --verbose
```

Sample input: `sample_250acre_farm.json` (in same directory).

Full JSON input schema, validation rules, output structure, NPV convention, and annuity factor reference → [`calculator-reference.md`](calculator-reference.md).

### NPV Convention (CRITICAL — Common Misreading)

NPV in this skill represents **total cost to farmer over infrastructure lifespan**, NOT compensation paid.

- Higher NPV = more compensation REQUIRED to offset costs
- Lower NPV = less compensation required
- Ontario lower NPV is NOT "better" — it means Ontario compensates LESS and leaves more burden uncompensated

## Three-Tier Counter-Offer Strategy

When the calculator confirms an Ontario offer is inadequate, structure the counter-offer in three tiers:

### Tier 1 — IDEAL (Alberta Model Anchor)

**Ask**: One-time easement + Alberta per-structure annual compensation indexed to inflation, 5-year review intervals, transfers with land.

**Justification**: Hart v ATCO Electric Ltd (2021), Ontario gas pipeline precedent (Enbridge, TCPL), OFA November 2024 AGM resolution, interprovincial equity.

### Tier 2 — TARGET (Documented Actual Costs)

**Ask**: One-time easement + annual compensation equal to calculator-quantified ongoing impacts (typically $5,000-$15,000/year depending on farm size and tower count).

**Justification**: Calculator-quantified impacts backed by farm operational records.

### Tier 3 — ACCEPTABLE (Capitalized One-Time)

**Ask**: One-time payment = easement + 6-year theoretical profit + NPV of annual impacts over remaining lifespan, capitalized at 5%.

**Formula**: `one_time_easement + theoretical_profit_6yr + (annual_impacts × annuity_factor)`

### Walk-Away Threshold

Reject any offer below NPV of (one-time easement + capitalized actual ongoing impacts). Escalation paths: legal challenge, OFA advocacy, Surface Rights Board extension, collective action with other affected landowners.

Full tier-by-tier justifications, expected pushback scripts, and 90-day negotiation timeline → [`ofa-guidance.md`](ofa-guidance.md).

## Canonical Example

**Setup**: 250-acre cash crop farm (corn/soybeans), $35,000/acre land value, 500kV Hydro One line, 16 towers, 80m ROW, 2 km crossing, 50-year lifespan.

**Ontario offer**: $33,000 one-time ($21,000 easement + $12,000 6-year theoretical profit).

**Documented ongoing impacts**: $9,460/year (headlands $1,900 + aerial spray $3,600 + precision ag $560 + labor $1,000 + weed control $800 + equipment damage $1,600).

**NPV @ 5%, 50 years**: $9,460 × 18.26 = **$172,747** ongoing burden.

**Tier 3 capitalized counter**: $21,000 + $12,000 + $172,747 = **$205,747 minimum acceptable one-time payment**.

**Shortfall in Ontario offer**: $205,747 − $33,000 = **$172,747 uncompensated** (84% of true cost externalized to farmer).

Two additional worked case studies (Alberta ATCO farm and multi-generational succession scenario) → [`case-studies.md`](case-studies.md).

## Report Output Convention

Save compensation analyses to `$CLAUDE_PROJECT_DIR/Reports/` with ET timestamp prefix.

**Filename**: `YYYY-MM-DD_HHMMSS_[farm_name]_cropland_compensation_analysis.md`

**Timestamp**: `TZ='America/New_York' date '+%Y-%m-%d_%H%M%S'`

Standard 9-section structure (Executive Summary → Farm Summary → Three Models → Comparative Analysis → Sensitivity → Risk Assessment → Negotiation Strategy → Conclusion → Appendices) and full tone guidance → [`output-conventions.md`](output-conventions.md).

## Professional Tone (Summary)

This analysis ADVOCATES for the farmer — it is not neutral. Use evidence-backed advocacy language ("inadequate", "shortfall", "uncompensated burden", "cost externalization"). Every claim backed by a number, precedent, or documented operational data. Frame from farmer perspective; quantify everything; emphasize intergenerational impacts (perpetual easement = perpetual burden = requires perpetual compensation). Full tone guidance and language to avoid → [`output-conventions.md`](output-conventions.md).

## Key Terms

- **Easement**: Perpetual or long-term right of utility to occupy/access a strip of land; runs with title and binds future owners.
- **ROW (Right-of-Way)**: The corridor within which the utility has operational rights; wider than the tower footprint itself.
- **Headlands**: Turning space around towers where farming continues but is inefficient (30-50% productivity loss).
- **Complete out of production**: Tower footprint where NO farming is possible.
- **Partial out of production**: Headlands and operational-restriction zones where farming continues at reduced productivity.
- **Theoretical profit loss**: Ontario Hydro One concept — 6 years of presumed lost net income, paid as lump sum.
- **Surface Rights Board (SRB)**: Alberta tribunal that adjudicates landowner-utility compensation disputes; source of $1,380/$552/$690 per-structure annual rates.
- **ERAA (Early Resolution Access Agreement)**: $10,000 Alberta utility incentive to bypass SRB hearing — often trades short-term cash for hundreds of thousands in foregone annual compensation.
- **Annuity factor**: `(1 − (1+r)^−n) / r` — used to capitalize annual payments into one-time equivalent (50yr @ 5% = 18.26).
- **OFA**: Ontario Federation of Agriculture; 2024 AGM passed 83%-supported resolution lobbying Hydro One for annual compensation.
- **Hart v ATCO Electric Ltd (2021)**: SRB decision establishing current Alberta per-structure annual rates.
- **NPV convention here**: Total cost to farmer over lifespan (NOT compensation paid) — higher NPV = more compensation required.
