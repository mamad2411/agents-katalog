---
name: impact-measurement
description: >
  Measure social and environmental impact using theory of change, indicator selection, data collection
  frameworks, attribution analysis, and impact reporting.
  TRIGGER when: user says /impact-measurement, "measure impact", "impact assessment", "social impact", "impact report", "impact measurement".
argument-hint: "[program-or-initiative] [impact-area] [time-period]"
user-invocable: true
---

# Impact Measurement

Rigorously measure and communicate the social and environmental outcomes of programs, investments, and business activities to demonstrate real-world impact.

---

## Input Gathering

| Input                          | Description                                                   | Required |
|--------------------------------|---------------------------------------------------------------|----------|
| Program / initiative description| Goals, activities, target beneficiaries, geographic scope     | Yes      |
| Theory of change               | Logic model connecting inputs to outcomes (or draft one)      | Yes      |
| Baseline data                  | Pre-intervention metrics for target population                | Yes      |
| Impact area                    | Environmental, social, health, education, economic, etc.      | Yes      |
| Stakeholder input              | Beneficiary perspectives, partner expectations                | No       |
| Budget for measurement         | Resources available for data collection and analysis          | No       |
| Comparison data                | Control group, benchmark, or counterfactual information       | No       |

---

## Step-by-Step Process

### Step 1 — Theory of Change Development

Build or validate the causal logic chain:

```
Inputs -> Activities -> Outputs -> Outcomes -> Impact
```

| Element    | Definition                                    | Example (Clean Water Program)           |
|------------|-----------------------------------------------|-----------------------------------------|
| Inputs     | Resources invested                            | $500K funding, 20 staff, equipment      |
| Activities | What the program does                         | Install water purification systems      |
| Outputs    | Direct deliverables (countable)               | 50 systems installed, 200 people trained|
| Outcomes   | Short/medium-term changes in behavior/condition| 80% reduction in waterborne illness     |
| Impact     | Long-term systemic change                      | Improved community health and productivity|

Document critical assumptions at each link in the chain. Identify external factors that could influence outcomes independently of the program.

### Step 2 — Indicator Selection and Measurement Framework

Select indicators at each level of the theory of change:

| Level     | Indicator Type | Example Indicators                              | Data Source           |
|-----------|---------------|--------------------------------------------------|-----------------------|
| Output    | Quantitative   | Units delivered, people reached, events held     | Program records       |
| Outcome   | Quantitative   | % change in behavior, income increase, emissions reduced | Surveys, monitoring |
| Outcome   | Qualitative    | Beneficiary testimonials, case studies           | Interviews, FGDs      |
| Impact    | Quantitative   | DALY avoided, tCO2e abated, poverty rate change  | Secondary data, models|
| Impact    | Monetized      | Social Return on Investment (SROI) ratio          | Economic valuation    |

Apply the SMART+C framework:
- **S**pecific: Clearly defined, no ambiguity
- **M**easurable: Quantifiable with available methods
- **A**chievable: Realistic to collect within budget
- **R**elevant: Directly linked to the theory of change
- **T**ime-bound: Measured at defined intervals
- **C**omparable: Benchmarkable against standards or peers

Limit to 5-8 core indicators per program to ensure quality over quantity.

### Step 3 — Data Collection Design

Design the data collection strategy:

| Method                | Best For                          | Cost    | Rigor  | Sample Size |
|-----------------------|-----------------------------------|---------|--------|-------------|
| Administrative records| Outputs, enrollment, completion   | Low     | Medium | Full census |
| Surveys (quantitative)| Outcome measurement at scale      | Medium  | Medium | 200-1000+   |
| Interviews (qualitative)| Deep understanding, attribution | Medium  | High   | 15-30       |
| Focus group discussions| Community perspectives, nuance   | Low     | Medium | 4-8 groups  |
| Direct observation    | Behavioral change verification    | Medium  | High   | Varies      |
| Sensor / IoT data     | Environmental metrics (real-time) | High    | High   | Continuous  |
| Secondary / public data| Benchmarks, macro-level trends   | Low     | Varies | N/A         |

Design considerations:
- **Sampling**: Random or stratified sampling for survey populations; document selection criteria.
- **Frequency**: Baseline (pre-intervention), midline (during), endline (post), and follow-up (sustained impact).
- **Ethics**: Informed consent, data privacy (GDPR/local law), do-no-harm principles, IRB approval if applicable.
- **Bias mitigation**: Enumerator training, survey pre-testing, response validation, triangulation across methods.

### Step 4 — Attribution and Counterfactual Analysis

Determine how much of the observed change is attributable to the program:

| Method                          | Description                                          | Rigor Level | Cost    |
|---------------------------------|------------------------------------------------------|:-----------:|---------|
| Randomized Controlled Trial (RCT)| Random assignment to treatment/control              | Highest     | High    |
| Quasi-experimental (DiD, PSM)  | Statistical matching of treatment and comparison groups| High      | Medium  |
| Pre-post comparison             | Before/after measurement, same group                 | Medium      | Low     |
| Contribution analysis           | Assess contribution within a multi-factor context    | Medium      | Low     |
| Beneficiary self-attribution    | Ask beneficiaries what caused the change             | Low-Medium  | Low     |
| Expert judgment / Delphi        | Panel of experts estimates attribution %             | Low-Medium  | Low     |

Select the method appropriate to the program's scale, budget, and evidence needs:

| Program Investment | Recommended Method                | Justification                         |
|--------------------|------------------------------------|---------------------------------------|
| > $10M             | RCT or quasi-experimental          | High stakes require rigorous evidence |
| $1M - $10M         | Quasi-experimental or contribution | Balance of rigor and cost             |
| < $1M              | Pre-post with contribution analysis| Proportional to investment            |

Always acknowledge attribution limitations transparently in reporting.

### Step 5 — Data Analysis and Interpretation

Analyze collected data to quantify impact:

| Analysis Type          | Application                                     | Output                       |
|------------------------|-------------------------------------------------|------------------------------|
| Descriptive statistics | Summarize outputs and outcome metrics            | Means, distributions, counts |
| Trend analysis         | Track change over time (baseline to endline)     | % change, trajectory charts  |
| Comparative analysis   | Treatment vs. control group differences          | Effect size, significance    |
| Subgroup analysis      | Impact variation by gender, geography, income    | Equity insights              |
| Cost-effectiveness     | Cost per unit of outcome achieved                | $/outcome unit               |
| SROI calculation       | Monetized social value vs. investment            | Ratio (e.g., 3.5:1)         |
| Sensitivity analysis   | Test robustness under different assumptions      | Range of plausible estimates |

Key principles:
- Report both intended and unintended outcomes (positive and negative).
- Disaggregate data by relevant demographic dimensions.
- Present confidence intervals, not just point estimates.
- Conduct sensitivity analysis on key assumptions (discount rate, attribution %, deadweight).

### Step 6 — Impact Reporting and Communication

Tailor reporting to different audiences:

| Audience            | Format                                | Depth          | Key Content                        |
|---------------------|---------------------------------------|----------------|------------------------------------|
| Board / executives  | 2-page dashboard                      | Summary        | Headline metrics, ROI, decisions   |
| Investors / donors  | Full impact report (15-30 pages)     | Detailed       | Methodology, evidence, SROI        |
| Beneficiaries       | Visual summary, infographic           | Accessible     | What changed, what comes next      |
| Internal teams      | Learning brief (5-10 pages)          | Operational     | What worked, what to adjust        |
| Public              | Website, press release, social media  | Highlights     | Stories + data, transparent claims |
| Academic / sector   | White paper or journal article        | Technical       | Methodology, replicability         |

Follow the Impact Management Project (IMP) five dimensions in reporting:
1. **What**: What outcome occurred?
2. **Who**: Who experienced the outcome?
3. **How Much**: Scale, depth, and duration of the outcome.
4. **Contribution**: What was the program's role vs. other factors?
5. **Risk**: What is the risk that the impact is different than reported?

---

## Output Format

```
## Impact Measurement Report — [Program] — [Period]

### Executive Summary
- Program investment: [$X]
- Beneficiaries reached: [count]
- Key outcome: [headline metric and change]
- Social Return on Investment: [X:1]
- Attribution confidence: [high/medium/low]

### Theory of Change
Inputs -> Activities -> Outputs -> Outcomes -> Impact
[Summary with key assumptions]

### Indicator Dashboard
| Indicator               | Baseline | Target  | Actual  | % Achieved | Trend |
|-------------------------|----------|---------|---------|:----------:|:-----:|
| ...                     | ...      | ...     | ...     | ...        | ...   |

### Attribution Analysis
- Method used: [RCT / quasi-experimental / contribution analysis]
- Estimated attribution: [X%] of observed change attributable to program
- Counterfactual: [What would have happened without the program]
- Confidence level: [with explanation]

### Subgroup Analysis
| Subgroup          | Sample Size | Outcome Change | vs. Average |
|-------------------|:-----------:|:--------------:|:-----------:|
| Women             | ...         | ...            | ...         |
| Low-income        | ...         | ...            | ...         |
| Rural             | ...         | ...            | ...         |

### Cost-Effectiveness
- Cost per beneficiary: [$X]
- Cost per unit of outcome: [$X]
- SROI ratio: [X:1] (sensitivity range: [Y:1 to Z:1])

### Lessons Learned
1. [What worked well]
2. [What could be improved]
3. [Unexpected findings]

### Recommendations
1. [For program improvement]
2. [For scaling]
3. [For future measurement]
```

---

## Quality Checklist

- [ ] Theory of change articulated with clear assumptions at each link
- [ ] Indicators selected at output, outcome, and impact levels
- [ ] Baseline data collected before or at program start
- [ ] Data collection methods appropriate for budget and rigor needs
- [ ] Ethical considerations addressed (consent, privacy, do-no-harm)
- [ ] Attribution method proportional to investment and evidence needs
- [ ] Data disaggregated by relevant demographic dimensions
- [ ] Both intended and unintended outcomes reported
- [ ] Sensitivity analysis conducted on key assumptions
- [ ] Report tailored to audience with appropriate depth and format

---

## Edge Cases

- **No baseline data available (program already underway)**: Use recall-based surveys (with caution), proxy baselines from secondary data, or retrospective pre-post designs; document the limitation and adjust confidence levels accordingly.
- **Very small sample size (< 30 beneficiaries)**: Use qualitative-dominant mixed methods; report case studies rather than statistical generalizations; apply process tracing for attribution.
- **Long time lag between intervention and impact (5-10+ years)**: Measure intermediate outcomes as leading indicators; conduct periodic check-ins; use modeling to project long-term impact from short-term outcome data.
- **Multiple programs operating in the same context**: Use contribution analysis to assess relative influence; track unique program touchpoints; acknowledge shared attribution honestly.
- **Beneficiaries difficult to track (mobile populations, informal economy)**: Use community-level indicators as proxies; partner with local organizations for follow-up; design shorter measurement cycles.
- **Negative or null impact findings**: Report transparently; analyze why outcomes were not achieved; distinguish between program failure and measurement limitations; frame findings as learning for adaptive management.
