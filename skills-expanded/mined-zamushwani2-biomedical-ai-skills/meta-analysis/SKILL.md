# Meta-Analysis

Systematic review and meta-analysis for clinical and preclinical evidence. Covers protocol registration, search strategy, screening, PRISMA 2020 flow diagrams, risk of bias, pooling with fixed and random effects models, small-study effects, sensitivity diagnostics, network meta-analysis, and GRADE/CINeMA certainty rating. Uses metafor, netmeta, PRISMA2020, synthesisr, and robvis.

## When to Use This Skill

Activate when the user requests:
- A systematic review or meta-analysis protocol
- Search strategy construction for PubMed, Embase, or Cochrane CENTRAL
- PRISMA 2020 flow diagram generation
- Deduplication of records across databases
- Title/abstract or full-text screening workflows
- Inter-rater agreement between screeners
- Risk of bias assessment (RoB 2, ROBINS-I, ROBINS-E, QUADAS-2, Newcastle-Ottawa)
- Risk of bias visualization (traffic light or summary plots)
- Data extraction templates for RCTs or observational studies
- Effect size computation (OR, RR, RD, SMD, MD, ROM, HR)
- Pooling with equal-effects or random-effects models
- Heterogeneity quantification (tau^2, I^2, Q) and prediction intervals
- Subgroup analysis and meta-regression
- Hazard ratio reconstruction from published Kaplan-Meier curves
- Forest and funnel plots
- Publication bias or small-study effect assessment
- Leave-one-out, influence, or cumulative sensitivity analysis
- Network meta-analysis, transitivity, inconsistency, or treatment ranking
- GRADE or CINeMA certainty rating

## Inputs

| Data Type | Format | Source |
|-----------|--------|--------|
| Search results | RIS, BibTeX, NBIB, CSV | PubMed, Embase, CENTRAL, Web of Science |
| Record counts | Integers per PRISMA stage | Search logs, screening software |
| Extracted outcomes | Tabular (study, n, effect, variance) | Full-text data extraction |
| Risk of bias judgements | Tabular (study, domain 1..k, overall) | RoB 2 / ROBINS-I Excel or manual |

---

## Environment

```r
# Core, all actively maintained (versions verified 2026-08)
install.packages(c("metafor", "meta", "PRISMA2020", "robvis", "synthesisr", "irr"))
#   metafor     5.0-1    effect sizes and models
#   meta        8.5-0    alternative interface, GRADE-friendly output
#   PRISMA2020  1.1.4    flow diagrams
#   robvis      0.3.1    risk of bias plots
#   synthesisr  0.4.1    bibliographic import and deduplication
#   irr         0.85     Cohen's and Fleiss' kappa

# Network meta-analysis and bias sensitivity
install.packages(c("netmeta", "metasens", "gemtc", "multinma"))
#   netmeta     3.6-1    frequentist NMA. NOTE: pairwise() is in `meta`
#   metasens    1.5-3    Copas selection model, limit meta-analysis
#   gemtc       1.1-1    Bayesian NMA, JAGS backend
#   multinma    0.9.1    Bayesian NMA, Stan; aggregate + individual patient data

# Programmatic search
install.packages(c("rentrez", "easyPubMed"))
#   rentrez     1.2.4
#   easyPubMed  3.1.6
```

```
Packages to avoid, and why:

  revtools    0.4.1, last released 2019-12. Superseded by synthesisr, which is
              by the same authors and actively maintained.
  metagear    0.7, last released 2021-02.
  metaviz     0.3.1, last released 2020-04. metafor and meta cover the plots.
  esc         0.5.1, last released 2019-12. Use metafor::escalc().
  pcnetmeta   2.8, last released 2022-08.
  nmadb       1.2.0, last released 2019-12.

Not an R package at all:
  CINeMA      web application for certainty in network meta-analysis.
              Do not search CRAN for it.

Not on CRAN, install from source if needed:
  ASySD       deduplication, higher sensitivity than reference-manager dedup
  litsearchr  search term discovery from a naive search
  dmetar      companion package to the Doing Meta-Analysis book
```

---

## Protocol and Registration

Register before screening starts. A protocol written after seeing results is not a protocol.

```
Where to register:
  PROSPERO        health-related reviews with a health outcome. Free.
                  Registration before data extraction begins.
  OSF Registries  anything PROSPERO will not take (preclinical, methods,
                  animal studies, scoping reviews).
  INPLASY         alternative when PROSPERO turnaround is too slow.

What must be pre-specified, because changing it later is a protocol deviation
that has to be reported:
  - PICO elements and the review question
  - Eligibility criteria, including study designs and language limits
  - Databases and the planned search date range
  - Primary and secondary outcomes, defined precisely
  - Effect measure (OR, RR, HR, MD, SMD)
  - Synthesis model (fixed vs random effects) and heterogeneity handling
  - Subgroup and sensitivity analyses, declared in advance
  - Risk of bias tool
```

Report the PROSPERO ID in the manuscript. Reviewers check it, and deviations between the registration and the paper are a common reason for rejection.

## Search Strategy

### Translating PICO into a query

```
PICO -> query blocks, combined with AND across blocks and OR within blocks:

  P (Population)    disease terms, controlled vocabulary + free text
  I (Intervention)  drug/exposure names, including synonyms and brand names
  C (Comparator)    usually omitted from the search; it over-restricts
  O (Outcome)       usually omitted; outcomes are poorly indexed and
                    including them loses relevant records

Standard practice is to search P AND I only, and apply C and O at screening.
Searching all four is the most common cause of a search that misses studies.
```

### Controlled vocabulary and free text

Every block needs both. MeSH alone misses recent records that have not been indexed yet; free text alone misses records where the concept is only in the MeSH.

```
PubMed
  "Carcinoma, Non-Small-Cell Lung"[Mesh] OR nsclc[tiab] OR
  "non small cell lung"[tiab]

  [Mesh]        controlled vocabulary, auto-explodes to narrower terms
  [Mesh:NoExp]  suppress explosion
  [tiab]        title/abstract
  [tw]          text word, broader than tiab
  [pt]          publication type

Embase (Ovid syntax)
  exp Carcinoma, Non-Small Cell Lung/ OR nsclc.ti,ab,kw.

  exp   explode the Emtree term
  /     Emtree term marker
  .ti,ab,kw.  title, abstract, keyword

Cochrane CENTRAL
  [mh "Carcinoma, Non-Small-Cell Lung"] OR nsclc:ti,ab,kw
```

Truncation differs by platform. PubMed uses `*` and requires at least four characters before it; Ovid uses `$` or `*`. PubMed does not support left truncation.

### Validated study design filters

Do not write your own RCT filter. Use a validated one and cite it.

```
Cochrane Highly Sensitive Search Strategy (CHSSS), sensitivity-maximizing
version for PubMed. Published in the Cochrane Handbook, chapter 4.

  (randomized controlled trial[pt] OR controlled clinical trial[pt] OR
   randomized[tiab] OR placebo[tiab] OR clinical trials as topic[mesh:noexp] OR
   randomly[tiab] OR trial[ti]) NOT (animals[mh] NOT humans[mh])

Note the animal exclusion is written as NOT (animals NOT humans), not
NOT animals[mh]. The latter drops human studies that also used animal models.
```

For observational designs there is no equivalent gold standard. Filters exist but lose sensitivity, so most reviews search without a design filter and exclude at screening.

### Programmatic PubMed search

```r
library(rentrez)   # v1.2.4

query <- paste(
  '("Carcinoma, Non-Small-Cell Lung"[Mesh] OR nsclc[tiab])',
  'AND ("Immunotherapy"[Mesh] OR pembrolizumab[tiab] OR nivolumab[tiab])',
  'AND ("2015/01/01"[PDAT] : "2026/12/31"[PDAT])'
)

# use_history keeps results server-side; required above ~10k records
res <- entrez_search(db = "pubmed", term = query, use_history = TRUE, retmax = 0)
res$count

# Fetch in batches. NCBI throttles to 3 requests/second without an API key,
# 10/second with one. Set it via ENTREZ_KEY or set_entrez_key().
recs <- character()
for (start in seq(0, res$count - 1, by = 200)) {
  recs <- c(recs, entrez_fetch(
    db = "pubmed", web_history = res$web_history,
    rettype = "medline", retmode = "text",
    retstart = start, retmax = 200
  ))
  Sys.sleep(0.34)
}
writeLines(recs, "pubmed_records.nbib")
```

The search string, the database, the platform, the date run, and the number of hits must all be recorded per database. PRISMA 2020 requires the full strategy for at least one database in the manuscript or supplement.

## Deduplication

Records overlap heavily across databases. PubMed and Embase alone typically overlap 40-60%.

```r
library(synthesisr)   # v0.4.1

files <- c("pubmed.nbib", "embase.ris", "central.ris")
refs <- read_refs(files, tag_naming = "best_guess", return_df = TRUE)

# Exact match on DOI first: fast and safe
refs <- refs[!duplicated(refs$doi) | is.na(refs$doi), ]

# Then fuzzy match on title for records lacking a DOI
dups <- find_duplicates(
  refs$title,
  method = "string_osa",
  to_lower = TRUE, rm_punctuation = TRUE,
  threshold = 7          # max edit distance; raise to catch more, at the
)                        # cost of false merges
deduped <- extract_unique_references(refs, matches = dups)

nrow(refs) - nrow(deduped)   # duplicates removed, needed for PRISMA
```

```
Deduplication is not a solved problem. Two failure modes, opposite directions:

  Under-merging   the same trial published as a conference abstract and a
                  full paper has different titles and no shared DOI. These
                  are duplicate STUDIES, not duplicate RECORDS, and must be
                  linked at data extraction, not here.

  Over-merging    companion papers reporting different outcomes of one trial
                  have near-identical titles. Merging them loses an outcome.

Always eyeball the merged pairs before accepting. A threshold that removes
"too many" duplicates is worse than one that removes too few, because the
lost records are invisible downstream.
```

Reference-manager deduplication (EndNote, Zotero) has lower sensitivity than dedicated tools. If dedup accuracy matters, ASySD reports sensitivity 0.95-0.99 with specificity above 0.99.

## Screening

### Two reviewers, independently

```
Title/abstract screening
  Two reviewers screen all records independently against the eligibility
  criteria. Liberal inclusion: if either reviewer says maybe, it advances.
  Reconcile disagreements by discussion, with a third reviewer to break ties.

Full-text screening
  Same two-reviewer process. This is the stage where every exclusion needs a
  recorded REASON, because PRISMA 2020 requires reporting them with counts.

Pilot first
  Both reviewers screen the same 50-100 records, compare, and refine the
  criteria before screening the rest. Most criteria ambiguity surfaces here.
```

### Measuring agreement

```r
library(irr)   # v0.85

# screening: data.frame with one column per reviewer, one row per record
kappa2(screening[, c("reviewer_1", "reviewer_2")])       # two reviewers
kappam.fleiss(screening[, c("r1", "r2", "r3")])          # three or more
```

```
Interpreting kappa for screening:
  < 0.40   poor. The criteria are ambiguous. Stop and rewrite them.
  0.40-0.60  moderate. Usually fixable with a calibration round.
  0.60-0.80  substantial. Acceptable.
  > 0.80   almost perfect.

Kappa is deflated when inclusion is rare, which it always is at title/abstract
(typical inclusion 2-5%). A low kappa with high raw agreement is the expected
pattern, not necessarily a problem. Report both.
```

### Screening automation

Active-learning tools rank records by predicted relevance so screening can stop early. They are decision aids, not replacements for a second reviewer.

```
ASReview    open source, active learning. Screens in relevance order and
            plateaus once the recall curve flattens.
Rayyan      web based, free tier, supports blinded two-reviewer workflow.

If you use one, report it: the tool, the model, the stopping rule, and
whether a human screened every record or only until the stopping rule fired.
An unreported stopping rule is a reproducibility gap.
```

## PRISMA 2020 Flow Diagram

PRISMA 2020 replaced the 2009 statement and changed the diagram structure. The current version separates records identified from databases and registers, and distinguishes reports from studies.

```r
library(PRISMA2020)   # v1.1.4

# The package expects a specific set of row names. Start from the template
# shipped with the package rather than building the data frame by hand.
template <- system.file("extdata", "PRISMA.csv", package = "PRISMA2020")
counts <- read.csv(template)

# Key fields, all as integers:
#   database_results, register_results       identification
#   duplicates, excluded_automatic, excluded_other
#   records_screened, records_excluded       screening
#   dbr_sought_reports, dbr_notretrieved_reports
#   dbr_assessed, dbr_excluded               eligibility, with reasons
#   new_studies, new_reports                 included

data <- PRISMA_data(counts)

plot <- PRISMA_flowdiagram(
  data,
  interactive = FALSE,
  previous = FALSE,        # TRUE only for a review update with prior studies
  other = TRUE,            # records found outside database searching
  detail_databases = TRUE, # break identification down per database
  side_boxes = TRUE
)

PRISMA_save(plot, filename = "prisma_flow.pdf", filetype = "PDF", overwrite = TRUE)
```

```
The arithmetic must reconcile, and reviewers check it:

  records_screened = (database_results + register_results)
                     - duplicates - excluded_automatic - excluded_other

  dbr_assessed = dbr_sought_reports - dbr_notretrieved_reports

  new_studies <= dbr_assessed - dbr_excluded

Studies vs reports: one study can produce several reports. The included box
reports both counts, and they are usually different. Conflating them is the
most common PRISMA diagram error.

previous = TRUE is only for review updates. Leaving it at the default on a
new review produces boxes for prior studies that do not exist.
```

## Data Extraction

### Extract in duplicate

Two extractors, independently, into the same template, then reconcile. Single extraction has a documented error rate high enough to change pooled estimates.

### What to capture

```
Study level
  citation, PROSPERO/trial registration ID, country, funding source,
  conflicts of interest, design, follow-up duration

Population
  n randomized, n analysed, age, sex, disease stage, line of therapy,
  key prognostic factors

Intervention and comparator
  agent, dose, schedule, duration, co-interventions

Outcomes, per outcome and per timepoint
  definition as reported, timepoint, n analysed
  binary        events and total, per arm
  continuous    mean, SD, n, per arm
  time-to-event HR with CI, or the numbers needed to derive one

Always record what was NOT reported. "Not reported" and "zero" are different
and are handled differently downstream.
```

### Deriving what is missing

Trials frequently report the wrong summary statistic. Convert rather than dropping the study, and record every conversion.

```
Median and IQR -> mean and SD        Wan et al. 2014, Luo et al. 2018
SE -> SD                            SD = SE * sqrt(n)
95% CI -> SD                        SD = sqrt(n) * (upper - lower) / 3.92
                                    3.92 = 2 * 1.96; use the t quantile if n < 60
p value -> SE                       back-calculate from the test statistic

Every derived value is an assumption. Flag them and test them in a
sensitivity analysis that excludes derived data.
```

## Risk of Bias

### Choosing the tool

```
What design are you assessing?

  Randomized trial
    -> RoB 2. Five domains, signalling questions, per-outcome not per-study.
       Assess each outcome separately; a trial can be low risk for mortality
       and high risk for a subjective outcome.

  Non-randomized study of an INTERVENTION
    -> ROBINS-I (2016). Seven domains, judged against a target trial.
       ROBINS-I V2 was posted 2025-11-20 but is still a DRAFT and is
       "subject to change". Use the 2016 version for work you intend to
       publish, and state which version you used.

  Non-randomized study of an EXPOSURE
    -> ROBINS-E. Same logic as ROBINS-I, adapted for exposures.

  Diagnostic accuracy study
    -> QUADAS-2.

  Prognostic factor study
    -> QUIPS.

  Missing evidence in the synthesis itself
    -> ROB ME.

  Newcastle-Ottawa Scale
    -> Widely used for cohort and case-control studies and often demanded by
       journals, but it produces a numeric score, and Cochrane recommends
       against collapsing risk of bias into a score. If a journal requires
       NOS, report it alongside ROBINS-I rather than instead of it.
```

RoB 2 and ROBINS-I are domain-judgement tools, not checklists. Each domain resolves to Low / Some concerns (or Moderate) / High / Critical via an algorithm from the signalling questions. Do not average domains: the overall judgement is driven by the worst domain.

### Visualization

```r
library(robvis)   # v0.3.1

# One row per study. Columns: Study, D1..Dk, Overall, and optionally Weight.
# Judgement strings must match the tool's expected levels exactly.
rob_traffic_light(data = rob_data, tool = "ROB2", psize = 10)

rob_summary(data = rob_data, tool = "ROB2", overall = TRUE,
            weighted = TRUE)   # weight bars by study weight from the model

# Supported: "ROB2", "ROB2-Cluster", "ROBINS-I", "ROBINS-E",
#            "QUADAS-2", "QUIPS", "Generic"
rob_tools()   # confirms the list for the installed version
```

Use `tool = "Generic"` for anything else, including the Newcastle-Ottawa Scale, which robvis does not model directly.

```
The robvis CRAN package is maintained (0.3.1, June 2026), but riskofbias.info
states they are no longer able to support the robvis web app or the Excel tool
implementations. Use the R package rather than the hosted app.
```

Risk of bias feeds the synthesis. Studies at high risk are not silently dropped: they are either excluded in a pre-specified sensitivity analysis, or retained with the sensitivity analysis reported alongside.

## Effect Measures

Choose the measure before extraction, because it determines what has to be extracted.

```
Binary outcome
  OR   odds ratio. Symmetric, works with case-control, but is misread as a
       risk ratio whenever the event is common (> ~10%).
  RR   risk ratio. Interpretable, preferred for cohort and trial data.
       Not estimable from case-control designs.
  RD   risk difference. Absolute scale, so it transports poorly across
       populations with different baseline risk. Usually more heterogeneous.
  PETO one-step OR. Only for rare events with balanced arms. Biased when
       arms are unbalanced or effects are large.

Continuous outcome
  MD   mean difference. Use when every study measured the SAME instrument
       on the same scale.
  SMD  standardised mean difference (Hedges' g in metafor). Use when studies
       used DIFFERENT instruments for the same construct.
  ROM  ratio of means. Use for ratio-scale outcomes where a proportional
       change is more natural than an absolute one.

Time-to-event
  HR   hazard ratio, pooled on the log scale.
```

Pick one and keep it. Switching measure after seeing the pooled result is a form of analytic flexibility that inflates false positives.

## Computing Effect Sizes

`escalc()` computes the effect size `yi` and its sampling variance `vi`, which is what every model consumes.

```r
library(metafor)   # v5.0-1
data(dat.bcg, package = "metadat")

# Binary: 2x2 table per study
dat <- escalc(measure = "RR", data = dat.bcg,
              ai = tpos, bi = tneg,     # events / non-events, treatment
              ci = cpos, di = cneg)     # events / non-events, control

# Continuous
# escalc(measure = "SMD", m1i =, sd1i =, n1i =, m2i =, sd2i =, n2i =, data = )

# Time-to-event: supply log(HR) and its standard error directly
# dat$yi <- log(dat$hr);  dat$vi <- ((log(dat$hr_upper) - log(dat$hr_lower)) / 3.92)^2
```

```
metafor 5.0 changed two escalc() defaults. Code written for 4.x runs without
error and returns DIFFERENT numbers.

  correct = TRUE is now the default for "ROM", "ROMC", "CVR" and "CVRC".
  The second-order Taylor bias correction is applied unless you pass
  correct = FALSE. Any ROM or CVR meta-analysis run on 4.x will not reproduce
  on 5.x at the default.

  The default `add` value changed to 0 for eight measures where bias
  corrections are now applied.

  pi.type was renamed predtype. The old name still works but is deprecated.

If you are reproducing a published analysis, pin the metafor version and say
which one you used.
```

### Zero cells

```r
# add = 1/2, to = "only0" is the default: add 0.5 only to studies with a zero cell
dat <- escalc(measure = "OR", ai = ai, bi = bi, ci = ci, di = di, data = dat)

# Double-zero studies contribute nothing and are dropped by default
# drop00 = TRUE removes them explicitly
```

```
The 0.5 continuity correction is a convenience, not a solution. It biases the
estimate toward the null and the bias grows as arms become unbalanced.

For rare events, prefer a method that does not need it:
  - Peto OR, when events are rare AND arms are roughly balanced
  - a beta-binomial or exact model via rma.glmm()

Never "fix" zero cells by deleting the studies. That is informative deletion.
```

## Fitting the Model

### The terminology trap

```r
rma(yi, vi, data = dat, method = "EE")   # equal-effects
rma(yi, vi, data = dat, method = "FE")   # fixed-effects
```

```
"EE" and "FE" produce IDENTICAL numbers and mean different things.

  EE (equal-effects)  assumes one single true effect underlies every study.
                      Differences between studies are sampling error only.
                      This is what most people mean when they write
                      "fixed-effect meta-analysis".

  FE (fixed-effects)  makes no such assumption. Inference is conditional on
                      the studies actually included: it estimates the average
                      effect IN THIS SET, and does not generalize beyond it.

Older metafor used "FE" for what is now "EE". Papers saying "fixed effect"
almost always mean EE. State which model you fitted and what you claim from it.
```

### Random-effects, the default

```r
res <- rma(yi, vi, data = dat,
           method = "REML",   # tau^2 estimator; the default
           test = "knha")     # Knapp-Hartung; NOT the default, must be asked for
summary(res)
```

```
Two choices carry most of the weight.

tau^2 estimator: REML
  metafor's default and its author's recommendation, because REML gives
  approximately unbiased estimates of heterogeneity. DerSimonian-Laird is
  the historical default in older software and underestimates tau^2, which
  makes confidence intervals too narrow. Use REML unless reproducing an
  older analysis, and then say so.
  Available: "REML", "ML", "DL", "PM", "EB", "SJ", "HS", "HSk", "HE", "GENQ".

Knapp-Hartung: test = "knha"
  Default is test = "z", which uses a normal distribution and produces
  intervals that are too narrow when the number of studies is small.
  test = "knha" uses a t-distribution with k - p degrees of freedom.
  metafor's author calls it "highly recommended".

  Honest caveat: simulation work (IntHout 2014, Jackson 2017) shows coverage
  is slightly BELOW nominal when heterogeneity is low (I^2 < 30%) and study
  sizes are very uneven. It still beats DerSimonian-Laird across most of the
  parameter space. Report that you used it.
```

## Heterogeneity

```r
res                  # prints Q, its p-value, tau^2, I^2, H^2
confint(res)         # confidence interval for tau^2 and I^2 — report it
predict(res, digits = 3)   # pooled estimate with a PREDICTION interval
```

```
What each quantity actually tells you:

  Q       a test of whether heterogeneity exceeds sampling error. Badly
          underpowered with few studies, and trivially significant with many.
          A non-significant Q does NOT establish homogeneity.

  tau^2   the variance of true effects, on the analysis scale. The only one
          of these that is a magnitude rather than a proportion.

  I^2     the PERCENTAGE OF VARIABILITY due to heterogeneity rather than
          chance. It is NOT the amount of heterogeneity. I^2 rises as studies
          get larger even when tau^2 is unchanged, because sampling error
          shrinks. Two meta-analyses with identical tau^2 can have I^2 of 25%
          and 90%.

  The 25/50/75% "low/moderate/high" thresholds are explicitly described in the
  Cochrane Handbook as rough and context-dependent. Do not treat them as rules.

Prediction interval
  The confidence interval describes the AVERAGE effect. The prediction
  interval describes where the effect of a NEW study would fall. With
  substantial tau^2 the prediction interval routinely crosses the null while
  the confidence interval does not. Report both, or the review overstates
  what is known.
```

## Subgroup Analysis

```r
# Subgroups are a moderator, not separate meta-analyses
res_sub <- rma(yi, vi, mods = ~ factor(alloc), data = dat, test = "knha")
res_sub          # QM = omnibus test of the moderator; this is the test that matters

# Pooled estimate within each level, with a shared tau^2
predict(res_sub, newmods = rbind(c(0,0), c(1,0), c(0,1)))
```

```
The mistake that shows up in most published subgroup analyses:

  Running a separate meta-analysis in each subgroup and comparing whether one
  is significant and the other is not. That is not a comparison. A subgroup
  can be significant purely because it has more studies.

  The correct question is whether the SUBGROUP DIFFERENCE is non-zero, which
  is the QM test above.

Subgroup analyses are observational even in a review of randomized trials.
Studies were not randomized to subgroups, so a subgroup difference is a
hypothesis, not an effect. Pre-specify them, keep them few, and report how
many you ran.
```

## Meta-Regression

```r
res_mr <- rma(yi, vi, mods = ~ ablat + year, data = dat, test = "knha")
res_mr
# R^2 in the output = proportion of tau^2 explained by the moderators

regplot(res_mr, mod = "ablat", xlab = "Absolute latitude", las = 1)
```

```
Power rule of thumb: at least 10 studies per moderator, and that is a floor,
not a target. Meta-regression on 8 studies with 2 moderators is curve-fitting.

Aggregation bias: a study-level covariate is not a patient-level covariate.
A relationship between mean age and effect size across studies does not imply
the same relationship across patients. This is ecological inference, and it
is the single most over-claimed result in meta-regression.
```

## Hazard Ratios from Published Curves

When a trial reports a Kaplan-Meier curve but no hazard ratio, the HR can be reconstructed.

```
Preferred order:

  1. HR and CI reported directly            use them
  2. Reconstruct from reported statistics   Parmar/Tierney methods, using
                                            O-E and variance, or the log-rank
                                            p-value with events per arm
  3. Digitize the KM curve                  Guyot algorithm reconstructs
                                            individual patient data from the
                                            curve plus numbers at risk

Digitizing is a last resort. It requires the numbers-at-risk table to be
printed; without it the reconstruction is unreliable. The R implementation
(IPDfromKM) was last released in 2020, so validate its output against any
reported median survival before pooling.

Whatever you use, record the method per study and run a sensitivity analysis
excluding reconstructed estimates.
```

## Forest Plots

```r
forest(res,
       slab = paste(dat$author, dat$year, sep = ", "),
       atransf = exp,               # display on the ratio scale, model fitted on log
       at = log(c(0.05, 0.25, 1, 4)),
       xlab = "Risk Ratio (log scale)",
       header = "Author(s) and Year",
       mlab = "")
addpoly(res, row = -1, atransf = exp, mlab = "RE Model (REML, KNHA)")
```

Fit ratio measures on the log scale and transform only for display. Pooling raw ratios is wrong: the sampling distribution is skewed and the variance formula assumes the log scale.

## Publication Bias and Small-Study Effects

"Publication bias" is one explanation for funnel plot asymmetry. It is not the only one, and the tests cannot distinguish between them.

```
Why a funnel plot can be asymmetric, all producing the same picture:

  Publication bias      small negative studies never published
  True heterogeneity    small studies done in higher-risk populations with
                        genuinely larger effects
  Poorer methods        small studies less likely to be blinded or allocation
                        concealed, inflating their effects
  Outcome reporting     the significant outcome reported, the others not
  Chance                with 10 studies, asymmetry happens

The Cochrane Handbook's term for this family is SMALL-STUDY EFFECTS, which is
the honest label. Use it in the manuscript rather than asserting publication
bias you cannot demonstrate.
```

### Funnel plot and Egger's test

```r
funnel(res, level = c(90, 95, 99), shade = c("white", "gray55", "gray75"),
       refline = 0, legend = TRUE)

regtest(res, model = "lm")   # Egger's regression test
ranktest(res)                # Begg's rank correlation, low power
```

```
Do not run Egger's test with fewer than 10 studies. The Cochrane Handbook is
explicit, and running it anyway is one of the most common errors in published
reviews: with k < 10 the test cannot distinguish asymmetry from chance.

A significant Egger's test does not establish publication bias. It establishes
asymmetry. The five causes above all produce it.

Agreement between Begg's test, Egger's test and trim-and-fill is empirically
only weak to moderate, so a "negative" result from one is not reassurance.

For ratio measures use the log scale, and prefer a funnel plot against the
standard error rather than the sample size.
```

### Trim-and-fill, and why to be careful with it

```r
tf <- trimfill(res)
tf              # imputed studies and the "adjusted" estimate
funnel(tf)
```

```
Cochrane Handbook, on trim-and-fill:

  it is "built on the strong assumption that there should be a symmetric
  funnel plot", it "does not take into account reasons for funnel plot
  asymmetry other than publication bias", and "'corrected' intervention
  effect estimates from this method should be interpreted with great caution".

Practical reading: use trim-and-fill as a SENSITIVITY ANALYSIS, to ask whether
the conclusion survives a pessimistic scenario. Do not report the filled
estimate as the result, and do not report the number of imputed studies as if
it were a count of suppressed trials. It is not.
```

### Selection models, the principled alternative

```r
# Model the publication process explicitly rather than assuming symmetry
sel <- selmodel(res, type = "step", steps = c(0.025, 0.5))
sel
```

```r
library(metasens)   # v1.5-3
limitmeta(m)        # limit meta-analysis: estimate as study size -> infinity
copas(m)            # Copas selection model, sensitivity across selection strengths
```

Selection models state their assumption about how publication depends on the p-value, which makes the assumption arguable. Trim-and-fill hides its assumption inside a symmetry requirement. Prefer the former when you have enough studies to fit it.

## Sensitivity and Influence Diagnostics

```r
leave1out(res)                 # refit dropping each study in turn
inf <- influence(res); plot(inf)   # Cook's distance, DFFITS, hat, tau^2 delete-1
baujat(res)                    # heterogeneity contribution vs influence on the pooled effect
cumul(res, order = year)       # cumulative meta-analysis, in time order
```

```
What each answers:

  leave1out   does any single study drive the result? Report the range of
              pooled estimates, not just the full-data one.
  influence   which studies are outliers AND influential. Being an outlier
              is not enough; a small outlier changes nothing.
  baujat      separates "inflates heterogeneity" from "moves the estimate".
              The top-right quadrant is what to investigate.
  cumul       shows whether the effect stabilized or is still moving. An
              estimate that shifts with each new trial is not settled.

Pre-specify sensitivity analyses. Running leave-one-out and reporting only the
version that reaches significance is p-hacking with extra steps.
```

## Network Meta-Analysis

NMA compares three or more treatments by combining direct and indirect evidence. It answers questions no single trial asked.

### Transitivity, the assumption everything rests on

```
Indirect evidence for A vs C comes from A vs B and B vs C trials.

That is valid ONLY if the A-vs-B and B-vs-C trials are similar enough that a
patient in one could plausibly have been enrolled in the other. Formally:
effect modifiers must be distributed similarly across comparisons.

Check it BEFORE fitting anything, and check it with clinical data, not
statistics: tabulate age, disease severity, line of therapy, year, and dose
by comparison. If early trials used a lower dose of B than later ones, the
network is not transitive and no amount of modelling repairs it.

Statistical inconsistency tests have low power. A non-significant
inconsistency test is not evidence of transitivity.
```

### Fitting

```r
library(netmeta)   # v3.6-1
library(meta)      # pairwise() lives HERE, not in netmeta

# Long arm-based data -> contrast-based pairwise comparisons,
# with correlated multi-arm trials handled correctly
p <- pairwise(treat = treatment, event = events, n = total,
              studlab = study, data = dat, sm = "OR")

net <- netmeta(p, common = FALSE, random = TRUE,
               reference.group = "placebo",
               small.values = "desirable",   # do lower values mean benefit?
               prediction = TRUE)
summary(net)
```

```
Multi-arm trials are the trap. A three-arm trial contributes three pairwise
comparisons that are CORRELATED, because they share an arm. Feeding those in
as if independent double-counts patients and understates the standard error.

pairwise() constructs the correct correlation structure. Building the
comparison table by hand in a spreadsheet does not.
```

### Network geometry

```r
netgraph(net, plastic = FALSE, thickness = "number.of.studies",
         number.of.studies = TRUE)
```

Look at it before interpreting anything. A comparison supported by one small trial can sit between two well-studied nodes and carry the entire indirect estimate.

### Inconsistency

```r
netsplit(net)        # direct vs indirect per comparison, with a p-value
decomp.design(net)   # design-by-treatment interaction, the global test
netheat(net)         # which designs contribute the inconsistency
```

```
netsplit is local: it asks whether direct and indirect disagree for each
comparison. decomp.design is global.

Both are underpowered. Report them, and treat a disagreement as a reason to
re-examine transitivity rather than as a number to correct.

If direct and indirect genuinely conflict, the network estimate is a weighted
average of two incompatible things. Do not report it as if the conflict were
resolved.
```

### Ranking, and its limits

```r
netrank(net, small.values = "desirable")   # P-scores, frequentist analogue of SUCRA
```

```
P-scores and SUCRA are the most over-interpreted output in the whole field.

  A treatment can rank first on a single small trial. The ranking metric does
  not encode uncertainty in a way readers perceive.

  Rankings are unstable: adding one study can reorder the top three.

  "Ranked first" is not "better than second". Report the effect estimates with
  confidence intervals alongside any ranking, and never report a league table
  of ranks without them.

Report certainty too. A first-ranked treatment supported by very-low-certainty
evidence should be described that way.
```

### Bayesian NMA

```r
library(gemtc)     # v1.1-1, JAGS backend
# mtc.network() -> mtc.model() -> mtc.run(), then gelman.diag() for convergence

library(multinma)  # v0.9.1, Stan backend; supports individual patient data
```

Use Bayesian NMA when you need full posterior distributions, want to incorporate prior information on heterogeneity, or need to combine aggregate and individual patient data. Check convergence (R-hat, trace plots) before reading any estimate.

## Certainty of Evidence

```
Pairwise meta-analysis -> GRADE
  Start high for RCTs, low for observational studies, then rate down for:
    risk of bias, inconsistency, indirectness, imprecision, publication bias
  and up (observational only) for:
    large effect, dose-response, plausible confounding working against the effect

  Produce a Summary of Findings table. GRADEpro is the standard tool.

Network meta-analysis -> CINeMA
  GRADE does not extend cleanly to networks, because each estimate mixes
  direct and indirect evidence in different proportions. CINeMA
  (Confidence In Network Meta-Analysis) handles this across six domains:
  within-study bias, reporting bias, indirectness, imprecision, heterogeneity,
  and incoherence.

  CINeMA is a WEB APPLICATION, not an R package. Do not look for it on CRAN.
  netmeta can export the data it needs.
```

Certainty is assessed per outcome and per comparison, not once for the review. A review with high certainty for the primary outcome and very low certainty for harms must say so.

## Output Specification

| Output | Format | Description |
|--------|--------|-------------|
| `search_strategy.txt` | Text | Full query per database, platform, date run, hits |
| `records_raw.ris` | RIS | Combined export before deduplication |
| `records_deduped.csv` | CSV | Unique records with a duplicate-removal count |
| `screening_decisions.csv` | CSV | Per-record decision per reviewer, plus reconciliation |
| `exclusion_reasons.csv` | CSV | Full-text exclusions with a reason per record |
| `prisma_counts.csv` | CSV | Integer counts per PRISMA 2020 stage |
| `prisma_flow.pdf` | PDF | PRISMA 2020 flow diagram |
| `extraction.csv` | CSV | One row per study-outcome-timepoint |
| `rob_assessments.csv` | CSV | Study, per-domain judgements, overall |
| `rob_traffic_light.pdf` | PDF | Per-study per-domain risk of bias |
| `rob_summary.pdf` | PDF | Stacked bar of judgements per domain |
| `effect_sizes.csv` | CSV | Per-study `yi` and `vi` from `escalc()`, plus the measure used |
| `model_results.txt` | Text | `rma()` output: estimate, CI, prediction interval, tau^2, I^2, Q |
| `subgroup_results.csv` | CSV | Per-subgroup estimates and the QM test of the difference |
| `metaregression.txt` | Text | Coefficients, omnibus test, R^2 |
| `forest_plot.pdf` | PDF | Forest plot on the analysis scale, transformed for display |
| `sessionInfo.txt` | Text | Package versions. metafor 4.x and 5.x give different ROM/CVR results |
| `funnel_plot.pdf` | PDF | Contour-enhanced funnel plot, with k reported |
| `bias_tests.txt` | Text | Egger's regression and rank test, with k and the k >= 10 check |
| `sensitivity.csv` | CSV | Leave-one-out estimates, influence diagnostics, cumulative analysis |
| `netgraph.pdf` | PDF | Network geometry with edge thickness by number of studies |
| `nma_results.csv` | CSV | League table of pairwise estimates with confidence intervals |
| `netsplit.csv` | CSV | Direct vs indirect per comparison, with the inconsistency p-value |
| `netrank.csv` | CSV | P-scores, reported alongside effect estimates and certainty |
| `transitivity_table.csv` | CSV | Effect modifiers tabulated by comparison, the pre-fit check |
| `certainty.csv` | CSV | GRADE (pairwise) or CINeMA (network) rating per outcome per comparison |

## Validation Checks

```
Search
  Every known-relevant "seed" study is retrieved by the final search.
  Build a seed set of 5-10 papers you already know qualify, and confirm the
  search finds all of them. A search that misses a seed is incomplete.

  Hit counts per database are recorded and sum to the identification box.

Deduplication
  Removed count is plausible: 30-60% overlap across 3+ biomedical databases.
  Under 10% suggests dedup failed. Over 70% suggests over-merging.
  Spot-check 20 merged pairs manually.

Screening
  Kappa reported for both title/abstract and full text.
  Every full-text exclusion has exactly one recorded primary reason.
  Reasons collapse to a small set: PRISMA expects grouped counts, not 40
  distinct one-off reasons.

PRISMA diagram
  records_screened reconciles with identification minus removals.
  dbr_assessed reconciles with sought minus not-retrieved.
  Studies and reports counted separately in the included box.

Risk of bias
  RoB 2 applied per outcome, not once per study.
  Domain levels match the tool's expected strings exactly, or robvis silently
  drops rows.
  Overall judgement equals the worst domain, never an average.
  Two assessors, with disagreements recorded and reconciled.

Effect sizes
  yi and vi exist for every included study; no NA passed silently into rma().
  Ratio measures are on the log scale in yi, exponentiated only for display.
  Direction is consistent: a value below 0 (log scale) means the same thing
  in every study. Flipped arms are the most common extraction error.
  Sanity-check 2-3 studies by hand against the paper's reported effect.

Model
  method and test are stated explicitly, not left implicit.
  tau^2 reported with a confidence interval, not just a point estimate.
  Prediction interval reported alongside the confidence interval.
  k (number of studies) matches the PRISMA included count.

  Reproducibility: record metafor's version. Bias correction defaults for
  ROM, ROMC, CVR and CVRC changed in 5.0, so the same code gives different
  numbers across that boundary.

Subgroups and meta-regression
  Subgroup claims rest on the QM test of the difference, not on comparing
  which subgroup reached significance.
  At least 10 studies per moderator, and the count reported.
  Number of subgroup analyses run is reported, including the ones that
  produced nothing.

Publication bias
  k >= 10 before any asymmetry test is run, and k stated next to the result.
  Findings described as "small-study effects", not asserted as publication bias.
  Trim-and-fill reported as a sensitivity analysis, never as the headline estimate.

Sensitivity
  Leave-one-out range reported, not just the full-data estimate.
  Sensitivity analyses were pre-specified, and all of them are reported.

Network meta-analysis
  Transitivity assessed with a table of effect modifiers by comparison,
  BEFORE the model was fitted.
  pairwise() used to build comparisons, so multi-arm trials are correlated
  correctly. Patients are not double-counted.
  Network plot inspected: no comparison carrying the network on one small trial.
  netsplit and decomp.design both reported, with their low power acknowledged.
  Rankings never reported without effect estimates, confidence intervals and
  certainty alongside.
  Bayesian fits: convergence checked (R-hat, trace plots) before interpretation.

Certainty
  Rated per outcome and per comparison, not once for the whole review.
  GRADE for pairwise, CINeMA for networks.
```

## Common Pitfalls

### Protocol and search
1. **Registering after screening**: PROSPERO registration exists to fix the criteria before the results are visible. Registering late, or amending criteria after seeing which studies qualify, is a deviation that must be declared and undermines the review.
2. **Putting outcomes in the search string**: outcomes are inconsistently reported in titles and abstracts and poorly indexed. Adding an outcome block silently drops eligible studies. Search P AND I, filter for O at screening.
3. **Using MeSH without free-text terms**: records indexed in the last 6-12 months may have no MeSH assigned. A MeSH-only search systematically misses the most recent literature, which is usually the literature that motivated the review.
4. **Writing your own RCT filter**: validated filters exist and are cited. A hand-rolled filter has unknown sensitivity. Use the Cochrane Highly Sensitive Search Strategy and cite it.
5. **`NOT animals[mh]` to exclude animal studies**: this also removes human studies that included animal work. The validated form is `NOT (animals[mh] NOT humans[mh])`.
6. **Searching one database**: PubMed alone misses a substantial fraction of trials, particularly European and conference records. Minimum for a Cochrane-style review is PubMed, Embase, and CENTRAL.

### Screening and extraction
7. **Single-reviewer screening**: doubles the miss rate relative to duplicate screening. If resources force it, use two reviewers for a random 20% and report the agreement on that subset.
8. **Reading kappa without raw agreement**: at 2-5% inclusion rates kappa is deflated by design. A kappa of 0.5 with 97% raw agreement is not the same problem as a kappa of 0.5 with 70% raw agreement.
9. **Not recording exclusion reasons at full text**: PRISMA 2020 requires exclusions with reasons and counts. Reconstructing them afterwards from memory is not possible.
10. **Treating reports as studies**: a trial with a primary paper, a long-term follow-up, and a conference abstract is one study and three reports. Counting it three times inflates the evidence base and double-counts patients in the pooled estimate.
11. **Dropping studies that report medians**: median and IQR convert to mean and SD with published formulae. Dropping them biases the review toward studies with normally distributed outcomes.

### Risk of bias
12. **Assessing RoB 2 once per study**: RoB 2 is per outcome by design. A trial can be low risk for overall survival and high risk for an investigator-assessed response endpoint measured unblinded.
13. **Using ROBINS-I V2 for publication now**: it was posted 2025-11-20 as a draft and the authors state it is subject to change. Use the 2016 version and state which you used.
14. **Averaging domain judgements**: the overall judgement is the worst domain, not a mean. Averaging turns one critical flaw into a moderate score.
15. **Scoring instead of judging with the Newcastle-Ottawa Scale**: a numeric star score implies domains are interchangeable and that a threshold separates good from bad studies. Report domain-level judgements, and pair NOS with ROBINS-I when a journal insists on it.
16. **Excluding high-risk studies without pre-specification**: deciding to drop studies after seeing that they change the result is a post-hoc choice. Pre-specify it as a sensitivity analysis, and report both the full and restricted syntheses.

### Effect estimation
17. **Assuming metafor 4.x code reproduces on 5.x**: bias corrections for `ROM`, `ROMC`, `CVR` and `CVRC` became the `escalc()` default in 5.0, and the default `add` changed for eight measures. The code runs without error and returns different numbers. Record the version, and pass `correct = FALSE` if you are reproducing an older analysis.
18. **Leaving `test = "z"` on a random-effects model**: the default gives normal-based intervals that are too narrow with few studies. `test = "knha"` uses a t-distribution and is the maintainer's own recommendation. It is not the default, so it has to be requested.
19. **Using DerSimonian-Laird because it is familiar**: it underestimates tau^2, which narrows every downstream interval. REML is metafor's default and the current recommendation. If you use DL to match an older analysis, say so.
20. **Confusing `method = "EE"` with `method = "FE"`**: they produce identical numbers and support different claims. EE assumes one true effect; FE restricts inference to the included studies only. Most papers writing "fixed effect" mean EE.
21. **Reading I² as the amount of heterogeneity**: it is the proportion of variability attributable to heterogeneity, and it increases with study size at constant tau². Report tau² with its confidence interval for magnitude, and treat the 25/50/75% bands as the rough guide the Cochrane Handbook says they are.
22. **Reporting only the confidence interval**: it describes the average effect. With real heterogeneity the prediction interval, which describes the next study, often crosses the null when the confidence interval does not. Omitting it overstates certainty.
23. **Comparing subgroups by their separate p-values**: significance in one subgroup and not another is not evidence of a difference; the subgroup with more studies simply has more power. Test the interaction with the QM statistic.
24. **Meta-regression with too few studies**: fewer than about 10 studies per moderator is curve-fitting. And a study-level covariate is not a patient-level one, so a moderator relationship across studies does not transfer to patients.
25. **Pooling ratio measures on the raw scale**: odds ratios, risk ratios and hazard ratios are pooled on the log scale, where the sampling distribution is approximately normal, and back-transformed only for display.
26. **Relying on the 0.5 continuity correction for rare events**: it biases estimates toward the null, and worse as arms become more unbalanced. Use Peto OR for rare balanced events, or a model that handles zeros directly.

### Publication bias and sensitivity
27. **Running Egger's test with fewer than 10 studies**: the Cochrane Handbook says not to, and it remains one of the most common errors in published reviews. Below k = 10 the test cannot separate asymmetry from chance.
28. **Reporting funnel plot asymmetry as publication bias**: asymmetry is equally consistent with genuine heterogeneity, worse methods in small studies, selective outcome reporting, or chance. The defensible term is "small-study effects".
29. **Presenting the trim-and-fill estimate as the result**: it assumes the funnel should be symmetric and ignores every other cause of asymmetry. Cochrane says to interpret its corrected estimates "with great caution". Use it as a sensitivity analysis.
30. **Treating the number of imputed studies as a count of suppressed trials**: they are a mathematical construction that restores symmetry, not evidence that those trials exist.
31. **Reporting leave-one-out only when it helps**: dropping the one study that removes significance, and reporting that version, is p-hacking. Pre-specify sensitivity analyses and report all of them.

### Network meta-analysis
32. **Fitting an NMA without assessing transitivity**: indirect comparison is only valid when effect modifiers are distributed similarly across comparisons. That is a clinical judgement made from a table of study characteristics, before modelling, and no statistical test substitutes for it.
33. **Reading a non-significant inconsistency test as evidence of consistency**: `netsplit` and `decomp.design` are both underpowered. Absence of detected inconsistency is not evidence of transitivity.
34. **Building the comparison table by hand**: multi-arm trials produce correlated comparisons that share an arm. Entering them as independent double-counts patients and understates standard errors. Use `pairwise()` from **meta**, which is where it lives, not netmeta.
35. **Reporting SUCRA or P-score rankings without effect estimates**: a treatment can rank first on one small trial, and rankings reorder when a single study is added. Always report the estimate, its interval, and the certainty next to the rank.
36. **Applying GRADE directly to network estimates**: each network estimate blends direct and indirect evidence in different proportions, which GRADE does not handle. Use CINeMA, and note it is a web application rather than an R package.
37. **Rating certainty once for the whole review**: certainty is per outcome and per comparison. High certainty for the primary outcome says nothing about the harms.

## Related Skills

- [`survival-analysis`](../survival-analysis/SKILL.md): interpreting the hazard ratios and Kaplan-Meier curves that time-to-event meta-analyses pool
- [`cancer-multiomics`](../cancer-multiomics/SKILL.md): primary analysis of the trials and cohorts a review synthesizes

## Public Datasets for Testing

| Dataset | Source | Use Case |
|---------|--------|----------|
| `dat.bcg` | `metadat` | 13 BCG vaccine trials, the canonical binary-outcome example |
| `dat.normand1999` | `metadat` | 9 trials, continuous outcome, length of stay |
| `dat.colditz1994` | `metadat` | Same BCG trials with alternative coding |
| `dat.hine1989` | `metadat` | 6 trials, risk difference, small counts |
| `data_rob2` | `robvis` | Example RoB 2 assessments in the expected column format |
| `data_robins_i` | `robvis` | ROBINS-I example, seven domains |
| `data_robins_e` | `robvis` | ROBINS-E example |
| `data_quadas` / `data_quips` | `robvis` | QUADAS-2 and QUIPS examples |
| `PRISMA.csv` | `PRISMA2020` | Template flow diagram counts, correct field names |
| `Senn2013` | `netmeta` | 26 diabetes trials, 10 treatments — the standard NMA teaching network |
| `Woods2010` | `netmeta` | COPD, binary outcome, includes multi-arm trials |
| `Linde2015` | `netmeta` | Depression, larger network with sparse comparisons |
| `dat.hasselblad1998` | `metadat` | Smoking cessation, the classic Bayesian NMA example |

Load the template with `system.file("extdata", "PRISMA.csv", package = "PRISMA2020")` rather than transcribing the field names, which is where most flow-diagram errors start.
