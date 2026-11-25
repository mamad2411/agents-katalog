---
name: pipeline-assessment
description: "Use when assessing a pharmaceutical pipeline asset, drug candidate, biotech license-in opportunity, BD asset, clinical-stage therapy, or investment feasibility brief. Produces reproducible MNC-style BD/License-in evaluation with ClinicalTrials.gov/PubMed evidence, 0-10 quantitative scoring, competitive landscape, risk flags, and Markdown plus JSON outputs."
license: MIT
compatibility: "Requires web access for ClinicalTrials.gov, PubMed, regulatory, patent, and market-source retrieval. Optional bundled Python helper uses only the Python standard library."
metadata:
  version: "1.0.0"
  author: "Perplexity Computer"
---

# Pipeline Assessment

## When to Use This Skill

Use this skill when the user asks to evaluate a pharmaceutical or biotech pipeline asset using MNC-style BD, license-in, partnering, or investment feasibility logic. Typical trigger phrases include:

- "assess this pipeline asset"
- "license-in evaluation"
- "BD assessment"
- "drug pipeline investment brief"
- "clinical asset scoring"
- "compare this molecule against competitors"
- "generate a standardized investment feasibility brief"

Do not use this skill for general company valuation, public-equity stock analysis, personal medical advice, or non-drug product-market research unless the task is specifically about a pipeline asset.

## Required Inputs

Collect or infer the following inputs before starting. If a required field is missing, ask the user for it unless the user explicitly asks for a best-effort quick assessment.

```json
{
  "asset_name": "Target drug or pipeline name, INN or development code",
  "target_indication": "Primary indication",
  "mechanism_of_action": "Optional mechanism or target, used for competitor search",
  "developer": "Current developer or sponsor",
  "assessment_depth": "quick | standard | deep",
  "weights": {
    "clinical_efficacy": 0.3,
    "safety": 0.2,
    "market_potential": 0.3,
    "competitive_differentiation": 0.2
  }
}
```

Default `assessment_depth` to `standard` if omitted. Default `weights` to 0.3 / 0.2 / 0.3 / 0.2 unless the user provides custom weights. If custom weights do not sum to 1.0, normalize them and disclose the normalized values.

## Operating Principles

1. **Evidence first**: Every quantified conclusion must cite a ClinicalTrials.gov NCT ID, DOI, regulatory document URL, patent URL, or market-source URL. Never present a numerical claim without a source.
2. **No unsupported inference**: If a metric is missing, write `Data Not Available`. Do not impute ORR, PFS, OS, adverse-event rates, market size, patent life, or phase gap without source data.
3. **English retrieval terms**: Use English asset names, indications, mechanisms, endpoints, and sponsor names for database search consistency. The final brief may be bilingual if useful.
4. **Reproducibility**: Record search queries, APIs used, source URLs, NCT IDs, DOIs, access timestamps, and any scoring assumptions.
5. **Separation of fact and judgment**: Keep extracted evidence, scoring logic, and analyst interpretation in separate fields or paragraphs.

## Assessment Depth

- **quick**: Use ClinicalTrials.gov and 1-3 web/PubMed searches. Produce a concise brief focused on the target asset, key trials, top competitors, and major risks.
- **standard**: Use ClinicalTrials.gov, PubMed, regulatory sources where available, patent search, and market/epidemiology sources. Produce the full Markdown and JSON brief.
- **deep**: Add broader competitor mapping, conference abstract search, regulatory history, safety database signals where accessible, payer/access discussion, and explicit sensitivity analysis. Use deep research workflows if more than five entities or multiple paid-data substitutes are required.

## Workflow

### Data Retrieval Layer

1. Query ClinicalTrials.gov API v2 by `intervention` and `condition`:
   - Primary target query: `asset_name` + `target_indication`.
   - Sponsor query: `developer` + `asset_name`.
   - Mechanism competitor query: `mechanism_of_action` + `target_indication`, if mechanism is provided.
2. If using the bundled helper, run:

   ```bash
   python scripts/clinicaltrials_fetch.py \
     --asset-name "<asset_name>" \
     --condition "<target_indication>" \
     --developer "<developer>" \
     --mechanism "<mechanism_of_action>" \
     --depth "<quick|standard|deep>" \
     --out "<output.json>"
   ```

3. Search PubMed, conference abstracts, regulatory documents, and patent sources according to depth:
   - PubMed: asset name, mechanism, target indication, ORR/PFS/OS/safety keywords.
   - Conferences: ASCO, AACR, ESMO, ASH, AAN, ACR, or indication-specific venues.
   - Regulatory: FDA labels, FDA briefing documents, FDA AdCom documents, EMA EPAR, MHRA/PMDA documents where relevant.
   - Patents: Google Patents, Lens, WIPO Patentscope, or official patent office pages.
4. For market potential, prefer named market or epidemiology sources. If EvaluatePharma, GlobalData, Cortellis, Citeline, or Pharmaprojects access is unavailable, use transparent substitutes such as peer-reviewed epidemiology, regulatory labels, company filings, investor presentations, and reputable analyst summaries. Mark source limitations.

### Data Normalization Layer

Normalize each trial into JSON with these fields where available:

```json
{
  "nct_id": "NCT identifier",
  "brief_title": "Trial title",
  "official_title": "Official title",
  "asset_name": "Intervention name",
  "condition": "Indication/condition",
  "sponsor": "Lead sponsor",
  "phase": "EARLY_PHASE1 | PHASE1 | PHASE2 | PHASE3 | PHASE4 | NA",
  "phase_numeric": 0,
  "status": "Recruiting/Completed/etc.",
  "enrollment": 0,
  "primary_endpoints": [],
  "secondary_endpoints": [],
  "start_date": "YYYY-MM-DD or Data Not Available",
  "primary_completion_date": "YYYY-MM-DD or Data Not Available",
  "last_update_posted": "YYYY-MM-DD or Data Not Available",
  "has_results": false,
  "results_url": "ClinicalTrials.gov URL",
  "reported_metrics": {
    "orr": "Data Not Available",
    "pfs": "Data Not Available",
    "os": "Data Not Available",
    "hr": "Data Not Available",
    "p_value": "Data Not Available",
    "grade_3_plus_ae_rate": "Data Not Available",
    "sae_rate": "Data Not Available",
    "discontinuation_rate": "Data Not Available"
  },
  "sources": []
}
```

Use the phase mapping in `references/scoring-framework.md`. If phase is ambiguous or not supplied by the registry, use `Data Not Available` and exclude it from phase-gap arithmetic.

### Scoring Layer

Score each dimension from 0 to 10 using the rules in `references/scoring-framework.md`. Always show:

- raw evidence extracted
- comparator or benchmark used
- calculation or rule applied
- confidence level: `High`, `Medium`, or `Low`
- sources supporting the score

Default weighted score:

```text
total_score =
  0.30 * clinical_efficacy_score +
  0.20 * safety_score +
  0.30 * market_potential_score +
  0.20 * competitive_differentiation_score
```

If any dimension has insufficient evidence, assign `Data Not Available` for the dimension and provide two views:

- **Evidence-complete score**: weighted average over available dimensions, with weights renormalized.
- **Conservative score**: missing dimensions set to 0, clearly labeled as conservative.

### Competitive Gap Analysis Layer

Create a `Competitive Landscape Table` with the top five comparable assets by mechanism, target, indication, or standard-of-care relevance. Include:

- asset name
- mechanism / target
- sponsor
- phase
- phase numeric
- status
- latest readout, primary completion, or last update date
- key efficacy and safety signal, if available
- NCT IDs and DOI/source links

Calculate:

```text
Phase Gap = target_asset_phase_numeric - fastest_comparator_phase_numeric
```

If the target asset is the fastest or tied for fastest, phase gap is 0. If phase data is missing, report `Data Not Available`.

### Risk Identification Layer

Apply the rules in `references/risk-rules.md` and tag risks under four categories:

- `Regulatory`: FDA AdCom negative precedent, accelerated approval scrutiny, endpoint acceptability, single-arm trial reliance, unresolved CMC risk.
- `Access`: payer restrictions, price pressure, reimbursement uncertainty, health technology assessment risk,医保谈判降价压力.
- `IP`: weak composition-of-matter patent, short patent runway, freedom-to-operate ambiguity, formulation-only moat.
- `Geopolitical`: export controls, sanctions, China/US/EU data transfer, trial geography acceptability, supply-chain restrictions.

Each risk flag must include severity (`Low`, `Medium`, `High`), rationale, source, and mitigation.

## Output Requirements

Produce both a Markdown brief and a machine-readable JSON brief. Use the templates in `references/output-templates.md`.

### Markdown Brief Sections

1. **Executive Summary**: exactly three conclusion sentences plus total score.
2. **Scoring Dashboard**: radar-chart-ready data and dimension score table.
3. **Clinical Evidence Snapshot**: key trial summary table.
4. **Competitive Gap Analysis**: phase gap, top five landscape table, and timeline commentary.
5. **Access Risk Flags**: regulatory, payment/access, IP, and geopolitical risk tags.
6. **Data Sources**: all cited links, NCT IDs, DOIs, search queries, and retrieval timestamps.

### JSON Brief Requirements

The JSON output must include:

- `metadata`
- `input`
- `normalized_trials`
- `scoring`
- `competitive_landscape`
- `risk_flags`
- `data_sources`
- `limitations`

Use explicit `Data Not Available` strings for missing values. Do not use `null` for data that was searched but not found; reserve `null` only for fields that are structurally not applicable.

## Quality Checklist

Before finalizing, verify:

- All numerical clinical claims have NCT IDs or DOI/source URLs.
- Missing data is marked `Data Not Available`.
- The scoring dashboard ties exactly to the evidence table.
- Weighted total math is correct and weights are disclosed.
- Competitor phase gap is calculated only from sourced phase values.
- Risk flags are sourced and include mitigations.
- Markdown and JSON outputs are internally consistent.

## Example Invocation

```json
{
  "asset_name": "datopotamab deruxtecan",
  "target_indication": "non-small cell lung cancer",
  "mechanism_of_action": "TROP2-directed antibody-drug conjugate",
  "developer": "Daiichi Sankyo AstraZeneca",
  "assessment_depth": "standard"
}
```

Expected result: a sourced MNC-style license-in assessment brief with quantitative dimension scores, top competing TROP2/ADC/NSCLC assets, clinical evidence tables, risk flags, and both Markdown and JSON deliverables.
