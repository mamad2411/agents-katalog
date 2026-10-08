---
name: stg-sizing-markets
description: Calculates market opportunity with TAM/SAM/SOM using dual methods and timing analysis. Use when researching market size during BUILD phase 1 or refreshing market data during CHALLENGE.
serves: strategist
domain: market-analysis
affects: problem-hypothesis, segment-hypothesis
depends-on: none
produces: tier-labeled market sizing evidence for hypothesis register
---

# Market Sizing

Calculate market opportunity with TAM/SAM/SOM and timing analysis. All figures are range-based, tier-labeled, and source-cited.

## Procedure

### Step 1: Load Context [S]

Read governor input: business mode (VENTURE/BOOTSTRAP/HYBRID), constraints (budget, team, timeline), problem space description.

Produce: research parameters (industry, geography, segment filters).

**Gate:** `context_loaded: bool` -- mode identified, problem space described.
- Pass: Step 2.
- Fail: Cannot proceed without mode and problem space. Report missing inputs.

### Step 2: Calculate TAM Using Both Methods [S]

Read: research parameters.

WebSearch for industry reports (Gartner, Forrester, IBISWorld, Statista, Grand View Research).

**Top-down:** Industry size x relevant segment percentage. Cite specific report, publisher, date, figure.

**Bottom-up:** Total potential customers x average revenue per customer. Cite customer count source and revenue assumption separately.

If methods differ >50%, investigate the discrepancy and report both with reconciliation attempt.

Produce: TAM range [low, high] with sources. Each figure labeled T1 (from published report) or T2 (calculated from multiple sources).

**Gate:** `tam_calculated: bool` -- two methods attempted, range produced, sources cited with dates.
- Pass: Step 3.
- Fail: If no reports found, widen search terms (adjacent industry, broader category). If still nothing, report: "TAM data insufficient -- mark as T3 assumption" and provide best available estimate.

### Step 3: Calculate SAM [S]

Read: TAM range, segment filters from context.

Apply filters sequentially to TAM:
- Geographic filter: reduce by geography relevance (cite source for geographic distribution)
- Segment filter: reduce by target segment proportion (cite source)
- Technical filter: reduce by technology compatibility requirements
- Vertical filter: reduce by industry vertical if applicable

Document each filter: what it is, reduction percentage, source, tier label.

Produce: SAM range with filter chain documented. Label T2 (derived through filtering).

**Gate:** `sam_calculated: bool` -- at least 2 filters applied, each with documented rationale and reduction ratio.
- Pass: Step 4.
- Fail: If SAM reduction is <20% of TAM, review filters. At minimum geographic, segment, and technical filters should apply. If genuinely broad, document why.

### Step 4: Calculate SOM [S]

Read: SAM range, constraints (resources, timeline, team size).

SOM = SAM x realistic capture rate in 12-24 months.

Capture rate justified by: analogous company benchmarks, channel capacity constraints, team size limitations. Most startups capture <1% of SAM in year 1.

Produce: SOM range. Label T2-T3 (capture rate is hypothesis).

**Gate:** `som_calculated: bool` -- capture rate justified with benchmark or analogy, not asserted.
- Pass: Step 5.
- Fail: If capture rate >5% of SAM in year 1 without evidence of existing traction, reduce or justify with specific precedent.

### Step 5: Assess Market Timing [K-grounded]

**Grounded in:** industry data from Step 2, competitive landscape signals.

Evaluate timing signals:
- Technology readiness: is enabling technology mature or emerging?
- Regulatory shifts: new regulations creating demand or removing barriers?
- Behavioral changes: shifts in how the segment works that create openings?
- Competitive density: crowded (late), sparse (early or no market), moderate (potentially right)?

Score: early, right time, late, too late. Each assessment cites specific evidence.

Produce: timing assessment with evidence. Label T2.

**Gate:** `timing_assessed: bool` -- at least 2 timing signals evaluated with cited evidence.
- Pass: Step 6.
- Fail: If no timing signals found, note: "Timing assessment inconclusive -- no strong signals in either direction."

### Step 6: Mode-Specific Validation [R]

Read: all calculations, business mode.

| Mode | Check | Threshold |
|------|-------|-----------|
| VENTURE | TAM size | >$1B |
| VENTURE | Growth rate | >15% annually |
| VENTURE | Timing | Not "too late" |
| BOOTSTRAP | SOM x estimated ARPU | > operating costs within 6 months |
| BOOTSTRAP | Niche viability | SOM supports sustainable business even if small |

Flag violations explicitly: which threshold failed, by how much, what it means.

Produce: mode validation result with specific concerns if any.

**Gate:** `validation_complete: bool` -- all mode-relevant thresholds checked, results documented.
- Pass: Done. Market sizing notes ready for register integration.
- Fail: If a threshold fails, report it as a finding (not a blocker). The strategist decides how to handle threshold violations.

## Quality Criteria

- TAM calculated using both top-down and bottom-up methods
- Every figure cites a specific source with date (not "industry reports say")
- All figures presented as ranges, not points
- Every figure carries a tier label (T1/T2/T3)
- SAM filters are enumerated with individual reduction ratios
- SOM capture rate is justified (not asserted)
- Mode-specific threshold check is explicit (pass/fail with numbers)

## Failure Modes

| Mode | Signal | Recovery |
|------|--------|----------|
| Fabricated market size | Figure has no source citation or cites a source that cannot be verified | Remove figure. Replace with "insufficient data -- requires [specific search]" or widen search terms |
| False precision | TAM stated as single number ($2.3B) rather than range | Convert to range. If only one source, range = source figure +/- 20%. If multiple sources, range = min to max of sources |
| SAM = TAM (no real filtering) | SAM reduction is <20% of TAM without extraordinary justification | Review filters. At minimum: geographic, segment, and technical filters should apply. If genuinely broad, document why |
| SOM wishful thinking | SOM capture rate >5% of SAM in first year without evidence of existing traction or analogous precedent | Justify or reduce. Most startups capture <1% of SAM in year 1 |

## Boundaries

**In scope:** TAM/SAM/SOM calculation, market timing assessment, mode-specific threshold validation, source citation, tier labeling, range estimation.

**Out of scope:** Competitive analysis (stg-analyzing-competition), segment definition (stg-segmenting-customers), pricing estimation (stg-designing-pricing), customer validation.
