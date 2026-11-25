---
name: research-report-interpretation
description: Interpret sell-side, institutional, expert, or investor research by extracting claims, assumptions, valuation drivers, verification needs, and thesis impact.
---

# Research Report Interpretation Skill

这个 skill 用于解读券商、卖方、机构、专家或投资者研究报告。它的目标不是复述研报，而是把一份报告拆成可验证 claim、隐含假设、预期变量、估值驱动和对 Mira thesis 的增量影响。

研报在 Mira 中默认是 `sellside_and_expert_research`，通常是 `L3 secondary / signal`。它可以帮助识别框架、预期差、变量优先级、估值方法和叙事变化，但不能替代公司披露、监管文件、官方数据、市场数据或可复算模型。

## Use When

- 用户提供或指定一份券商研报、机构研报、rating change、target price update、initiation note、industry note、专家研究、投资者信或研究 PDF。
- 用户问“这篇研报怎么看 / 靠谱吗 / 有什么新东西 / 对 thesis 有什么影响”。
- 需要从研报中提取可复用方法、变量框架或预期差线索，但当前任务仍围绕某个研究对象，而不是纯方法论研究。
- 需要把研报结论与已有 Mira thesis、company filing、earnings package、consensus proxy 或市场定价做差异检查。

如果用户问的是“这个研究方法本身是否值得纳入 Mira”，优先进入 `loops/methodology-research-loop.md`。如果研报解读触发 thesis 状态变化，再 handoff 到 `loops/thesis-update-loop.md` 或 `loops/event-delta-loop.md`。

## Required Inputs

- `research_object`: ticker、company、industry、macro asset 或 methodology object。
- `market_scope`
- `time_boundary`
- `report_title`
- `provider_or_submitter`
- `author_or_team`，如可得
- `report_date` 或明确的 `source_gap`
- `report_type`: initiation、update、rating_change、target_price_update、industry_note、thematic_note、expert_research、investor_letter、other
- `access_route`: public_on_demand、user_material、authorized_provider 或 transient_only
- `license_scope`
- `storage_scope`
- `redistribution_allowed`
- `user_goal`: summarize、challenge、extract_claims、compare_to_thesis、update_thesis、reverse_engineer_method
- `completeness_status`: full_report、excerpt、screenshot、summary_only、metadata_only

## Required Source Types

- Report source or user material intake record.
- `restricted_source_note` when the report is paid, confidential, licensed, user-provided, expert-network, or otherwise restricted.
- At least one independent `L1` / `L2` / `L5` source when a report claim is used for a durable conclusion.
- Existing Mira thesis package, evidence log or expectation map when the user asks for thesis impact.
- Consensus or estimate source, or explicit `source_gap`, when the interpretation depends on market expectation baseline.

## Ingestion And Permission Gate

Before using a newly supplied report, run `data/ingestion-layer.md`.

Default treatment:

- Public report URL: `ingestion_route=public_on_demand`; cite metadata and short summaries only.
- User upload, screenshot, clipped PDF or exported note: `ingestion_route=user_material`; keep private unless user explicitly approves promotion.
- Licensed vendor or paid research: `ingestion_route=authorized_provider` or `user_material`; tracked artifacts may contain metadata, short compliant effect notes and claim categories, not raw report content.
- Unknown permission: `storage_scope=transient_only` or `private`; `public_case_use=blocked`.

Do not commit full paid reports, substantial excerpts, expert-network transcripts, or vendor raw data. Do not quote long passages. Extract claim-level summaries instead.

## Analysis Flow

### 1. Report Metadata And Source Posture

Record:

- report identity, date, provider, author/team and source URL/path
- permission and storage boundary
- whether the report is complete or only a fragment
- whether it is company-specific, industry-wide, macro, thematic or method-focused
- stale boundary: report date, event covered, next earnings, next data release or target price/rating update

If `report_date`, permission, completeness or object identity is missing, keep the output at `working_view` and mark the gap.

### 2. Thesis Of The Report

Separate:

- headline conclusion
- core variable the author believes matters most
- time horizon of the view
- catalyst or revision path
- base case, bull case and bear case
- rating / target price / valuation output
- evidence the report itself cites
- what the report asks the market to change its mind about

Never treat rating, target price or author conviction as evidence by itself.

### 3. Claim Extraction

Extract claim-level records into `report-claim-map.csv`.

Each row should identify:

- `claim_type`: fact, reported_metric, guidance, target, forecast, assumption, interpretation, opinion, market_pricing, sentiment or derived_calculation
- `source_speaker`: sellside, buyside, expert, company, market, media or mira
- `variable`: revenue, margin, pricing, volume, capex, cash flow, multiple, risk premium, market share, demand, supply, regulation or other
- `time_horizon`: current, next_quarter, FY1, FY2, long_term or unknown
- `evidence_cited_by_report`
- `independent_verification_status`
- `treatment`: use_normally, attribute, monitor, needs_cross_check, source_gap, exclude

Facts and reported metrics require independent verification before they can support a durable Mira conclusion. Forecasts, assumptions, interpretations and opinions remain attributed to the report.

### 4. Expectation And Variant-Perception Bridge

Ask:

- Is the report describing consensus, challenging consensus, or updating consensus?
- Which variable is the expectation baseline: revenue, EPS, margin, FCF, capex, TAM, unit volume, ASP, multiple or risk premium?
- Does the report cite consensus provider/data, or is it using author estimates?
- Is the claimed edge from better facts, better interpretation, different time horizon, or different risk weighting?
- What would prove the author right or wrong?

If no reliable consensus proxy exists, write `source_gap`; do not replace consensus with a single analyst view, media tone or price action.

### 5. Valuation And Model Decomposition

If the report includes target price, rating, valuation multiple, DCF, SOTP or scenario math, decompose:

- forecast driver: revenue, margin, EPS, FCF, capex, share count, net cash/debt
- valuation anchor: P/E, EV/Sales, EV/EBITDA, EV/FCF, DCF, SOTP, NAV, replacement cost or other
- terminal assumptions and discount rate if available
- multiple change versus estimate change
- sensitivity: which input moves the conclusion most
- hidden assumption: margin normalization, utilization, terminal growth, TAM share, customer concentration, dilution or cost of capital

If Mira relies on these numbers for a conclusion, run `skills/data-analysis-quality-gate/SKILL.md` and record formulas or `calculation_gap`.

### 6. Evidence Cross-Check

Cross-check the report's material claims against:

- issuer primary disclosure or filing
- current or recent earnings package
- transcript / management Q&A where relevant
- market price, valuation and estimate data
- peer disclosure or industry data
- previous Mira evidence log or expectation map

Classify each material claim:

- `confirmed`: independently supported by higher-weight evidence
- `plausible_unverified`: directionally plausible but not yet confirmed
- `contested`: contradicted or weakened by other evidence
- `opinion_only`: useful framing, not evidence
- `source_gap`: cannot be checked with available sources

### 7. Bias, Incentive And Framing Check

Check for:

- rating or target-price anchoring
- model-driven precision without source detail
- selective peer set or date window
- company-access bias
- event-chasing after price movement
- bull-case assumptions embedded in base case
- TAM-to-revenue leap
- channel-check anecdote presented as broad demand fact
- valuation multiple change without explicit risk-premium or growth rationale

Bias check does not reject the report automatically. It determines treatment and confidence.

### 8. Mira Thesis Impact

If an existing thesis or expectation map exists, classify the report impact:

- `no_new_evidence`: repeats known consensus or prior Mira view
- `new_variable`: introduces a variable Mira was not tracking
- `evidence_upgrade`: improves evidence quality for an existing variable
- `evidence_downgrade`: weakens or contradicts a current variable
- `expectation_delta`: changes consensus, author estimates or valuation-implied expectation
- `method_delta`: useful framework should enter methodology review
- `actionability_gap`: interesting but not enough for research action without more data

Then state whether to update:

- `evidence-log.csv`
- `expectation-map.csv`
- `thesis-ledger.md`
- `event-delta.md`
- `methodology-card.md`

When a research report contributes a reusable method for gold, precious metals
or macro-sensitive commodities, do not promote the method directly. Classify it
as `method_delta`, identify the existing Mira method it extends, and record
whether it should become a labeled lens. For example, a gold residual / MSE
framework should map to `memory/methodologies/gold-residual-regime-lens.md`
unless independent data reconstruction supports a stronger methodology review.

## Output Package

Default output package:

- `report-readout.md`
- `report-claim-map.csv`
- `evidence-log.csv`

Optional supporting artifacts:

- `restricted-source-note.md`
- `calculation-ledger.csv`
- thesis-system updates when impact is material
- methodology card when the main value is a reusable method

`quick_map` can output only a routing card, source posture, report thesis, key claim table, Mira impact and refresh triggers. `standard` should produce the package. `deep_dive` should add cross-checks, valuation decomposition and thesis-system updates where relevant.

## Required Sections In `report-readout.md`

- setup
- source and permission boundary
- report thesis
- claim map summary
- expectation / variant-perception bridge
- valuation and model decomposition
- independent cross-check
- bias and framing check
- Mira thesis impact
- facts / inferences / judgments
- refresh triggers
- follow-up prompts

## Scoring

Use scores only to force structure, not to replace judgment.

| dimension | score range | meaning |
| --- | --- | --- |
| source_posture | 1-5 | report identity, date, permission and completeness quality |
| claim_separation | 1-5 | facts, forecasts, assumptions and opinions are separable |
| evidence_traceability | 1-5 | report shows upstream evidence that can be checked |
| independent_verifiability | 1-5 | Mira can cross-check material claims |
| expectation_delta_quality | 1-5 | report improves consensus / expectation understanding |
| valuation_transparency | 1-5 | target price or model assumptions are decomposable |
| bias_risk | 1-5 | higher means more framing / incentive / selection risk |
| mira_incremental_value | 1-5 | value added versus existing Mira state |

## Red Flags

- report date or author/source unknown
- full conclusion rests on target price or rating language
- facts, forecasts and opinions are mixed without separation
- target price changes mainly from multiple expansion with no risk-premium explanation
- TAM narrative is treated as company revenue without share, timing and margin bridge
- channel checks lack sample, geography, timing or counter-evidence
- consensus is asserted but provider, date and metric definition are missing
- report relies on company access or management framing without external check
- model precision exceeds source quality
- report is stale relative to earnings, guidance, filing or material event

## Stop Rules

- If permission is unclear, do not retain raw report content in tracked artifacts.
- If the report is restricted, output only compliant metadata, short effect notes and claim-level summaries.
- If the report is fragmentary, do not infer omitted model assumptions as known.
- If independent verification is unavailable, keep conclusions at `working_view`, `monitor` or `source_gap`.
- If valuation math is central and cannot be reproduced, mark `calculation_gap` and avoid strong target-price conclusions.
- If the report only adds opinion and no new evidence, do not update the durable thesis; record `no_new_evidence` or `method_delta` only.
- If a report's main value is a reusable model or factor lens, keep report facts
  attributed to the report and route the method through methodology review before
  treating it as a Mira framework.
