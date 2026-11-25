---

name: quant-analysis

description: Use when the user needs quantitative social-science analysis, empirical modeling, causal inference, regression, panel models, DID, IV, RDD, PSM, SCM, DML, robustness checks, empirical tables, figure-ready model outputs, or replication-package preflight.

---



# Quant Analysis



This skill handles quantitative social-science analysis. It is not a generic statistics shortcut: it must keep research question, measurement, identification, diagnostics, robustness, interpretation, and reproducibility tied together.



## Required References



Before formal analysis or causal wording, read:



- `<VELA_RUNTIME_ROOT>\skills\catalog\empirical_quant_workflow.json`

- `<VELA_RUNTIME_ROOT>\skills\catalog\quality_gates.json`

- `<VELA_RUNTIME_ROOT>\skills\catalog\publication_style_rules.json`



## First Decision



Declare the task type before choosing a model:



- `descriptive`: distributions, rates, group differences, trends, or summary statistics.

- `associational`: relationships or correlations without a causal design.

- `predictive`: prediction, classification, scoring, or forecasting.

- `causal`: effect, impact, mechanism, policy effect, treatment effect, or counterfactual claim.



If the task is causal, do not run straight to regression. First select a design family and complete the causal-identification check.



## Minimum Inputs



Ask for or infer these, and mark missing items:



- research question;

- unit of analysis;

- sample, population, geography, and time window;

- outcome variable;

- main explanatory variable or treatment;

- control variables or covariate set;

- estimand, descriptive statistic, prediction target, or causal design;

- data path or model output path;

- preferred language or tool chain: Python, R, Stata, Excel, or supplied outputs.



## Design Families



Use `empirical_quant_workflow.json` as the design contract. Common families:



- descriptive or correlational analysis;

- panel fixed effects;

- difference-in-differences and event study;

- instrumental variables;

- regression discontinuity;

- matching, weighting, and balance designs;

- synthetic control and synthetic DID;

- machine-learning-assisted causal estimation;

- shift-share and Bartik designs;

- triple difference;

- randomized or field experiments;

- dose-response and continuous-treatment designs;

- mechanism, mediation, distributional effects, CATE, and causal forests.



Do not force economics or AER conventions onto every social-science task. Use these families only when the user's question, data, field expectation, reviewer request, or intended journal makes them relevant. Descriptive, qualitative, humanities, text-interpretive, and ordinary Chinese social-science writing can stay with the local workflow without importing applied-microeconometrics defaults.



Modern causal defaults matter. For example:



- Staggered DID cannot rely on naive TWFE as the only estimator.

- Modern DID must consider cohort, imputation, interaction-weighted, Bacon decomposition, or HonestDID checks when timing is staggered.

- IV needs exclusion logic, reduced form, first stage, and weak-IV-aware inference when relevant.

- Shift-share work must state whether identification comes from baseline shares or external shocks, then audit Rotemberg weights or shock-level inference.

- RDD should avoid high-order global polynomials and must check density/manipulation and covariate continuity.

- Matching and weighting need overlap, balance, and pre-treatment covariate discipline.

- Machine-learning causal estimates still need identification; prediction performance is not causal evidence.



## Stata Ecosystem



When a project uses Stata or asks for AER/AEJ-style applied microeconometrics output, treat Stata as an auditable tool chain rather than pasted results.



Do not switch a Python, R, Excel, or supplied-output project into Stata just because Stata support exists. Stata is enabled when the project already uses it, collaborators or reviewers require it, a replication package needs it, or the user asks for it.



Minimum Stata package and command map:



- FE and panel: `reghdfe`, `ftools`, `xtserial`, `xttest3`, `xtcsd`.

- IV and weak-IV checks: `ivreg2`, `ranktest`, `weakivtest`, `ivreghdfe`, Anderson-Rubin style inference when needed.

- DID and event study: `csdid`, `drdid`, `did_imputation`, `did_multiplegt`, `did_multiplegt_dyn`, `eventstudyinteract`, `bacondecomp`, `honestdid`.

- RDD: `rdrobust`, `rddensity`.

- Synthetic and matching: `synth`, `synth_runner`, `synth2`, `scul`, `psmatch2`, `teffects`, `ebalance`, `cem`.

- Robust inference and multiple testing: `boottest`, `ritest`, `rwolf`, `wyoung`, `psacalc`.

- Tables and figures: `esttab`, `estout`, `outreg2`, `asdoc`, `asdocx`, `coefplot`, `binscatter`, `heatplot`.



For formal delivery, require a traceable do-file structure: `run_all.do`, `00_globals.do`, `00_install_packages.do`, cleaning, descriptives, main models, robustness, heterogeneity/mechanism, tables, figures, logs, and a replication README. Reject Stata outputs that cannot be traced back to commands, logs, and output paths.



## Workflow



1. Build an empirical question card: question, unit, sample, variables, task type, and target output.

2. Lock the measurement map: construct definitions, proxy limitations, missingness, outliers, transformations, weights, clustering, and fixed effects.

3. If causal, run `causal_identification_checked`:

   - estimand or target parameter;

   - design family;

   - identifying assumption in plain language;

   - assignment or treatment process;

   - required diagnostics;

   - red flags and fallback language.

4. Build the analysis plan:

   - data cleaning and merge checks;

   - descriptive table or Table 1;

   - model family and inference rule;

   - robustness, heterogeneity, mechanism, placebo, and sensitivity checks;

   - figure/table output map;

   - replication artifact map.

5. Run or review the analysis.

6. Hand formal figures and tables to `figure-table-studio`.

7. Hand formal manuscript prose to `manuscript-writing-studio`, while preserving the empirical boundaries.

8. Hand final code/data/package work to `reproducibility-package` or `social-science-submission-packager` when the project is submission-bound.



## Academic De-AI Surface Audit



The local workflow adapts useful de-template writing checks from `Awesome-Agent-Skills-for-Empirical-Research`, but does not install those external humanizer skills as competing routes.



Use `academic-humanization-studio` only after claims, evidence, variables, estimates, uncertainty, and citations are locked:



- remove empty rhetoric, mechanical transitions, vague attribution, inflated novelty, and repetitive sentence rhythm;

- preserve all facts, sample definitions, variables, coefficients, p values, confidence intervals, model limits, citations, and uncertainty;

- for English journal prose, prefer precise claims, compact sentences, field-standard phrasing, and explicit limitations;

- for Chinese social-science prose, keep concept density, problem awareness, theoretical linkage, and PEEL closure;

- run detect-first, rewrite-second, and second-pass audit;

- never promise to bypass Turnitin, CNKI AMLC, GPTZero, or any detector, and never make a detector score the acceptance target.



If improving prose requires changing a claim, variable, result, citation, or limitation, stop and ask the user to approve a substantive revision.



## Required Outputs



For non-trivial quantitative work, provide:



- empirical question card;

- variable and sample map;

- design-family or descriptive-boundary note;

- diagnostics checklist;

- robustness matrix;

- table/figure output map;

- interpretation note separating estimate, inference, mechanism, and limitation;

- replication checklist or blocker list.



## Failure Rules



Stop or downgrade the output when:



- unit, sample, or variable definitions are ambiguous;

- the requested causal wording lacks a design and identifying assumptions;

- data or model outputs are missing but the user asks for concrete estimates;

- diagnostics fail and the text would overstate the result;

- the user asks for detector evasion rather than academic-quality cleanup.
