---
name: tufte-data-forensics
description: "Use when an analysis, dataset, spreadsheet, model, benchmark, or research claim must be audited before it is trusted or acted on — deciding what to demand from a data supplier, tracing a number back to its measurement, screening for randomization, image, binning, or batch-effect failures, scoring a study's credibility, separating a forensic audit from data cleaning, or naming who paid for the answer."
tags: [tufte, data-integrity, research-integrity, forensic-audit, measurement, statistics, conflicts-of-interest, evidence]
---
# Data Forensics: Auditing an Analysis Before You Trust It

## Overview

*Seeing With Fresh Eyes* ch. 4 (printed **pp. 80–119**) is a procedure, not a lament. Its organizing device is a proposed reference work — an imagined *Data Measurement and Analysis: 1,000 Safeguards, Pitfalls, and Cheats in Statistical Practice*, modeled on Khonsari and Sintek's cardiac-surgery encyclopedia of some 3,000 graded alerts and warnings (p. 82). The parallel is the whole argument: surgery already has an itemized, severity-graded, actionable literature of things that go wrong at the point of work, and statistical practice does not — even though a botched analysis reaches more lives than a botched operation.

This skill owns the **step-by-step audit**. Two siblings own adjacent material and are not repeated here:

| Sibling | Owns |
|---|---|
| `tufte-evidence-corruption` | The catalog of corruption *types* — cherry-picking, effects without causes, model searching, overreaching, chartjunk, the rage to conclude, Chalmers, the "Which half?" exchange |
| `tufte-visual-thinking` | The seeing discipline and the ch. 4 *highlights* — Feynman/Mosteller, statistical vs. named lives, sampling-to-please, the Lucent triad, forensic-audit-vs-cleaning as named concepts |

What follows turns those named concepts into an executable audit: what to look at, in what order, what to demand, and what to write down.

**The operating stance.** Feynman's rule opens the chapter's facing page: the first principle is that you must not fool yourself, and you are the easiest person to fool (Feynman, quoted p. 80). Everything below is machinery for a person who has accepted that they are the primary threat. Tufte reinforces it with Darwin — that ignorance begets confidence more often than knowledge does (Darwin, quoted p. 86) — and with Van Wyck Brooks's principle that once you hold a point of view, all history will back you up (p. 81). The chapter's recurring villains are named as characters: **Dr. Confirmation Bias** and **Dr. p-Hacker**, who build narratives out of a fresh batch of random numbers (p. 86).

**The selection-bias frame (p. 80).** Tolstoy's remark that Napoleon "commanding" his armies compresses thousands of consecutive dependent commands, of which only the executed few are ever remembered, is the chapter's compact statement of causal selection bias: the record you audit has already been filtered by outcome before it reached you. Assume the survivors are in your dataset and the non-survivors are not.

---

## §1. Why an Audit, Not a Vibe Check — Prevalence Replaces Anecdote

Tufte's methodological reform is to stop arguing from horror stories and start arguing from **measured prevalence rates for specific, named error classes**. An anecdote tells you a failure is possible; a prevalence rate tells you what to check first and how surprised to be when you find it.

> Cross-reference: the same figures appear as an integrity table in `tufte-visual-thinking` §7 and as corruption evidence in `tufte-evidence-corruption`. **The contribution here is the third column** — each rate converted into a specific screening action.

| Failure class | Measured rate (SWFE ch. 4) | What it makes you screen for |
|---|---|---|
| Inappropriate image duplication | 3.8% of 20,621 papers, 40 journals, 1995–2014; about half showing features suggesting deliberate manipulation (Bik et al., p. 83) | Overlay, flip, and mirror-test every figure panel before reading the text |
| Same, in one subfield | 6.1% — 59 of 960 *Molecular and Cellular Biology* papers, 2009–2016 → 41 corrections, 5 retractions (p. 83) | Field-specific base rates differ; get your own field's number |
| Spreadsheet auto-conversion | ~20% of papers with supplementary Excel gene lists carry corrupted gene names; 704 papers across 18 genomics journals, 2005–2015 (Ziemann et al., p. 83) | Re-open every supplied spreadsheet with type coercion disabled and diff against source |
| Measurement error ignored | 44% of 565 articles in 12 major medical/epidemiology journals so much as mention it; only 7% of those investigate or correct it (Brakenhoff et al., p. 87) | Ask what the instrument's error is, in the instrument's own units, before accepting any estimate |
| Randomization failure | Screening of 5,087 randomized trials for non-random sampling (Carlisle, p. 83) | Run baseline-covariate distribution checks; randomization is a claim, not a guarantee |
| Retracted data still circulating | The Mediterranean-diet trial was retracted, corrected, and republished with weaker evidence — and **267 secondary articles built on the original incorrect data remain in circulation** (p. 83) | Check whether the source your source cites has been retracted; retraction does not propagate downstream |
| Analyst-induced variation | 29 teams, 61 analysts, one dataset, one question: odds ratios from 0.89 to 2.93 (median 1.31); 69% found a significant effect, 31% did not; 21 unique covariate combinations (p. 105) | Treat a single analysis path as one sample from a distribution of defensible paths |
| Non-replication | 11% of 63 landmark preclinical cancer studies reproduced (Begley & Ellis, p. 111) | Replication status is a required field, not a nice-to-have |
| Unvalidated practice | 3,017 RCTs in three leading journals yielded 396 documented medical reversals (p. 108); of 3,000 NHS treatments reviewed, **50% were of unknown effectiveness** (p. 108) | "Standard practice" is not evidence of effectiveness |
| Optimistic modeling | 145 covid-19 prediction models judged poorly reported and at high risk of bias (p. 109); of 516 medical-imaging AI studies, only 6% met the design standards for clinical validation (p. 109) | Demand external validation on data from another institution and another time period |

**Two prevalence claims to state carefully:**
- Tufte reports the prevalence of *regression toward the truth* — early enthusiastic claims that later shrink or reverse — as **perhaps 80%** (p. 83). He hedges it; hedge it too.
- The **522 consulting biostatisticians** surveyed (75% responded) reported inappropriate requests including: removing or altering records to better support the hypothesis; interpreting findings by expectation rather than by actual results; not reporting key missing data that would bias the result; and ignoring assumption violations that would reverse the conclusion (p. 92). This is a survey of *requests made to analysts*, which is why it belongs in an audit skill: it is a list of the pressures the analyst you are auditing was under.

**Accuracy warning — the mock package insert (p. 98).** Tufte prints a parody "BLACK BOX WARNING" for stepwise logistic multiple regression, listing adverse effects with percentages (cherry-picked models 80.1%, p-hacking >70%, multicollinearity 80.5%, and so on). It is a **mock-up illustrating a proposal**, not measured data. Never cite those percentages as prevalence rates. The transferable idea is the *format*: every statistical model should ship with a package insert naming its assumptions, breakdown conditions, and adverse reactions, the way lisinopril does.

---

## §2. Step 1 — Observe the Data at the Moment of Measurement

The single highest-yield audit move, and the one almost never performed.

> "You never learn more about a process than when you directly observe how data are actually measured." — Cuthbert Daniel, quoted in SWFE, p. 84

Go where the numbers are made. Walk around. Talk to the people holding the instrument. See how the numbers came to be, rather than how they arrived.

**The standing questions at the point of measurement (p. 84):**

| Question | What a bad answer reveals |
|---|---|
| Do those measuring know the desired answer? | Sampling to please (below) |
| Are they skilled, alert, honest — or biased, sloppy, tired, emotional? | Human variance the model treats as random noise |
| Do sites, hospitals, labs, or shifts vary in *what* they measure? | Non-comparable rows silently pooled |
| What artifacts and errors does the instrument itself produce? | Instrument signature mistaken for signal |
| How are outliers adjudicated, and by whom? | A discretionary filter upstream of your dataset |

**Named failure mode — Sampling to Please (p. 84).** A company polluted a river; agencies ordered daily water samples to monitor cleanup. Observe the actual collection and you see a small boat go out and the driver dip a container on a pole — *after looking around for cleaner water*. Nothing in the resulting time series records that scan. The general rule Tufte draws: people cannot keep their own score, and self-monitoring has early, structural limits. (Named in `tufte-visual-thinking` §7; the audit action is here.)

**Do / don't:**

| Do | Don't |
|---|---|
| Watch a full collection cycle in person, at the site | Accept a data dictionary as a description of practice |
| Read the instrument's own technical manual on artifacts | Assume the vendor's error model is the empirical error |
| Interview the technicians and nurses who take measurements all day; let them do the talking, then ask others the same questions and compare | Interview only the principal investigator |
| Ask about false alarms, duplicate and lucrative measurements, and over-diagnosis | Treat every recorded measurement as clinically or operationally motivated |
| Observe at the moment of **measurement**, not the moment of **publication** (p. 84) | Audit the figure instead of the field |

**Why the manuals matter (pp. 88–89).** Tufte's positive example is the technical manual for a transesophageal echocardiography system, which enumerates dozens of named 2D and 3D imaging artifacts — acoustic saturation, aliasing, comet tail, mirroring, multi-path positioning, range ambiguity, reverberation, scattering, shadowing, side and grating lobes, speckle, spectral broadening, speed-of-sound error, and for 3D: acquisition, rendering, editing, color-gain, directional, motion, dropout, and pseudoclefting artifacts — each with its physical cause and its correction. His verdict is that this is what serious empirical analysis of measurement error looks like, and that it is enormously better than the notion of "error" in classical statistics (p. 88). **Audit action:** find the equivalent manual for whatever produced your data, and check which of its named artifacts your analysis assumes away.

**Calibrate your expectations.** Tufte's summary of what direct observation of medical measurement reveals: it is a two-digit science on a good day, and on other days getting the sign right is an achievement (p. 84). Import that expectation into whatever domain you audit before you accept a third significant figure.

---

## §3. Step 2 — Track the Origin and Life History of the Measurement

A measurement is an object with a biography. Reconstruct it (p. 85).

- **Why** is this measurement made at all?
- **Who** looks at it — when, where, and for what purpose?
- What are its **consequences, harms, and benefits**?
- **Where did the data go**, and what is it doing now?
- **Follow the money:** who profits, and how much? For medical measurements Tufte states this as a standing instruction, not an accusation.
- Read the **engineering and technical manuals**, which describe measurement complexity and problems far more frankly than the research literature does.

**Two provenance failures with names:**

- **Provenance not documented (p. 92, quoting Groskopf).** Data are gathered by businesses, governments, nonprofits, sensors, satellites, and cranks. Survey data are not exhaustive; sensors vary in accuracy; governments are disinclined to hand over unbiased information; war-zone data are geographically biased by the danger of crossing battle lines; sources get daisy-chained together and policy analysts redistribute government data. **Every stage in that chain is an opportunity for error.**
- **"Ground truth" is often just someone else's spreadsheet (p. 94).** Database "ground truthers" never see their data at the moment of actual measurement. Attributing truth to a database, and then claiming proof of concept, is the **fallacy of equivocation** — a term used in two or more senses inside one argument so that a conclusion appears to follow when it does not. Tufte lists the puns that do this work: *ground truth, error, power, optimal, explained/unexplained variance, intellectual property*. His compressed audit slogans for the same failure: sketchy in, sketchy out; bias in, bias out; no causality in, no causality out; circularity in, circularity out (p. 94).

**Named failure mode — Survival Bias (p. 94).** Most medieval castles were built of wood; we believe most were stone because stone survived. Research databases are, definitionally, the databases that survived long enough to be selected for "ground truth" status. Survivor bias is subtle and inscrutable and demands both meta-cognition and detective work about database provenance.

---

## §4. Step 3 — The Three Traceability Questions

The chapter's most directly reusable audit instrument, adapted from the September 2002 Lucent Technologies report on the investigation of possible scientific misconduct in the work of Hendrik Schön and coauthors, Appendix E (p. 85). Ask these three, in order, of any presented result.

### Q1 — Can the presented data be traced back to primary data, free of processing or other manipulation?

Supporting logic worth carrying into policy: only credible primary data can corroborate published data; retention of primary data plus adequate record keeping is required for the *ordinary conduct* of work, not merely for investigating wrongdoing, because new questions arise that require returning to the primary data and revising the original analysis. Failure to keep primary data and records for a reasonable time is, by itself, a threat to the health of the enterprise — as true in the computer age as before.

### Q2 — Is there clear evidence that the data do *not* come from the measurements described?

Three named evidence forms:

| Form | Signature | Test |
|---|---|---|
| **Data Substitution** | Datasets for distinct experimental conditions show unreasonable similarity — sometimes after multiplying one set by a constant factor | Cross-correlate every pair of condition-level datasets; scan for constant-multiple relationships |
| **Unreasonable Precision** | A dataset agrees with a simple analytic expression better than the stated measurement accuracy permits | Compare residual spread against the instrument's own error budget |
| **Contradictory Physics** | Data are inconsistent with prevailing understanding of the mechanism and the measurement | Use sparingly: many great discoveries would first land here, so demand extraordinary proof rather than dismissal |

The Lucent committee's own caution is part of the tool: it set aside all but a few especially problematic Contradictory Physics cases, because the category is where genuine discovery also lives. Absent demonstrated special diligence, results contradicting known mechanism suggest simple error, self-deception, or misrepresentation — in that order.

### Q3 — If the data are not valid, are there mitigating circumstances explaining the misrepresentation?

A clerical error — including the wrong data in a figure — reflects poor procedure but not misconduct. But innocent explanations require knowing the authors' state of mind at the time, which cannot be determined definitively. **The credibility of a particular innocent explanation therefore depends on the overall credibility of the person in question**, which in turn depends on whether there is an unreasonable number of problems or a pattern of questionable practices. Once the data problems are established, the live question is whether many improbable innocent explanations should be accepted.

**Audit action:** score Q3 across the whole body of work, not the single artifact. One improbable innocent explanation is plausible. Six is a pattern.

---

## §5. Step 4 — Run the Forensic Audit *Before* Analysis, and Know It Is Not Data Cleaning

> Heading, p. 91: conduct an independent forensic data audit of your data prior to analysis — don't just look around, see everything.

**Why *before*.** Audits get deflected because researchers and sponsors are anxious for an early peek at the findings, and early information exerts undue influence through anchoring bias (p. 91). Once anyone has seen a preliminary result, the audit is compromised — not by dishonesty but by anchoring. Sequence is a control.

**The distinction that does the work (p. 91):**

| | Data cleaning | Forensic audit |
|---|---|---|
| Fixes | Logical inconsistencies, duplications, impossible values, conflicting postal codes, outliers | Systemic bias, falsification, too-good-to-be-true findings |
| Coverage | A well-designed cleaning program might identify ~70% of the Groskopf issue list | The remaining classes, which require experience and honest judgement |
| Stance | Insider, mechanical | Independent outsider — the virtue Tufte specifically credits to an AI-run forensic audit, unlike the ultimate insider, Dr. Confirmation Bias |
| Timing | Any time | Before analysis begins |

**Named failure mode — Cleaning Mistaken for Auditing.** A green cleaning report establishes that values are well-formed. It establishes nothing about whether they are true. (Named in `tufte-visual-thinking` §7; the operational split is here.)

**The checklist substrate.** Chris Groskopf's *Guide to Bad Data* enumerates **46 data-quality issues** in spreadsheets, which Tufte calls a good start for forensic audits (p. 91). Grouped for use:

| Group | Issues Tufte reproduces |
|---|---|
| Missing and null | Values are missing; zeros replace missing values; data are missing you know should be there |
| Identity and format | Rows or values duplicated; spelling inconsistent; name order inconsistent; date formats inconsistent; units not specified; field names ambiguous |
| Structure and encoding | Text converted to numbers; numbers stored as text; text garbled; line endings garbled; data in a PDF; data in scanned documents; data intermingled with formatting and annotations |
| Silent tool limits | Spreadsheet has 65,536 rows; spreadsheet has 255 or 256 columns; spreadsheet has dates 1900, 1904, 1969, 1970 |
| Sampling and aggregation | Sample not random; sample biased; margin-of-error too large or unknown; aggregations computed on missing values; data aggregated to the wrong categories or geographies; totals differ from published aggregates; an index masks underlying variation |
| Framing and manipulation | Timeframe manipulated; frame of reference manipulated; inflation or seasonal variation skews data; categories badly chosen; data too coarse; data too granular |
| Integrity signals | Provenance not documented; collection process opaque; data entered by humans; data have been manually edited; suspicious values present; data assert unrealistic precision; inexplicable outliers; results p-hacked; Benford's Law fails; author untrustworthy; **too good to be true** |

**Named failure mode — the Chihuahua Syndrome (p. 92).** A dog-licensing database was populated by a free-text breed field instead of a picklist, and ended up holding **250 spellings of "Chihuahua."** Groskopf's rule: there is no worse way to wreck data than to let a single human type it in without validation, and even the best tools cannot save messy data. **Audit action:** for every categorical field, count distinct values and compare to the size of the legitimate vocabulary. A 250:1 ratio is a schema failure, not a data-entry failure.

**Get it right at the start (p. 91).** Early adjustments are cheap; later rescue revisions are costly. Jeff Atwood's contribution is that the worst technical debt he has encountered is bad names — for database columns, variables, functions — which must be fixed immediately before they metastasize across the codebase. Nate Silver's is the audit habit itself: when combining datasets or doing complex processing, be compulsive about missing data and sanity-check failures, because missing, miscoded, and outlier cases more often than not indicate a larger, more systematic problem with the code or the data. Errors compound; do the due diligence before moving on.

---

## §6. Step 5 — Structural Checks the Eye Will Not Catch

These are the failures that survive a clean spreadsheet, a plausible chart, and a confident author.

**Batch effects (p. 93).** High-throughput measurement is affected by laboratory conditions, reagent lots, and personnel differences. The failure becomes serious when batch effects are **correlated with the outcome of interest** — then they do not add noise, they manufacture findings. Tufte's display is second-generation sequencing data from the 1000 Genomes Project: each row a HapMap sample processed in the same facility and platform, ordered by processing date, dark blue at 3 standard deviations below average and orange at 3 above, across a 3.5 Mb region of chromosome 16. Many batch effects are visible; the largest occupies **days 243–251** as long orange horizontal streaks. **Audit action:** demand the batch metadata (date, site, instrument, operator, lot) as a first-class column, then plot the outcome against it before plotting anything else. If batch metadata was not recorded, the audit stops there.

**Bang-bang duplicates / pseudo-replication (p. 86).** An observer records a number and, seconds later, records another. If the underlying process changes daily, those two measurements are not independent: knowledge of the first gives near-full knowledge of the second, so the number of *independent* measurements is one, not two. Econometrics calls this autocorrelation or serial correlation; experimental design calls it bang-bang duplicates or pseudo-replications. Tufte's worked case: an experiment on **3 mice** measuring the same variable **30 times per mouse** does not have a sample size of 90. **Audit action:** for every reported *n*, ask what the independent unit actually is — subject, site, batch, session — and recompute.

**Redefining groups breaks random assignment (p. 92).** Researchers redefine the treatment group to include only *patients treated* rather than *intended to treat*. Darrel Francis's example: if treatment happens on the 9th floor of a building without elevators, less healthy patients never arrive — so even if the treatment has **no effect at all**, the treated group will appear to do better than placebo. **Audit action:** confirm the analysis is intention-to-treat, and reconstruct the attrition path between assignment and analysis.

**Surrogates, proxies, and biomarkers (p. 94).** Markers such as blood pressure, lipids, and patient hope or gratitude stand in for serious long-run outcomes such as strokes, heart attacks, quality of life, and all-cause mortality — and the link is often based on assumption, theory, folklore, marketing, or tradition rather than evidence. Tufte's diagnostic: **changing hard outcomes to easier marker goals is a clear signal that the intervention doesn't work.** The worked case is progression-free survival in oncology, where only about one-third of cancer drugs entering European and U.S. markets have evidence of overall survival or quality-of-life benefit, and post-approval incentive to evaluate real clinical benefit is weak. **Audit action:** for every metric, ask what decision it stands in for, and whether the substitution has ever been validated empirically.

**Your database does not contain answers to all of your questions (p. 87).** A database may simply lack the relevant explanatory variables — a devastating constraint. Many analyses are in fact model-specification searches ("let's try this, let's try that"), but *this* and *that* may not be in the database at all. Tufte's instruction is blunt: get better data. **Audit action:** before any modeling, list the variables the causal story requires and mark which are absent. An absent confounder is not a modeling problem.

**Subgroup over-reach (p. 107).** Subgroup analysis is essential for learning from data and cheap to abuse. Tufte's example via John Mandrola: a trial comparing angioplasty against standard medical therapy for angina found the primary endpoint of death and myocardial infarction in **6.3%** of the angioplasty arm versus **3.3%** of the medical arm. Rather than reporting that angioplasty was twice as bad on the primary endpoint, the abstract opened with a subgroup, a secondary endpoint within it, and a further sub-subgroup. **Audit action:** read the primary endpoint in the primary population first, and only then read the abstract.

**Predictive models built on dirty data (p. 95).** Predictive policing systems trained on data produced under flawed and sometimes unlawful practices cannot escape that legacy; the models document prevailing practice rather than the phenomenon. Tufte's twist is useful to an auditor: **model outputs, in effect, measure their own biases — so prediction models rat themselves out.** The supporting asymmetry: available studies estimate 49% of businesses and 25% of households have been victims of white-collar crime, against roughly 1.1% prevalence for violent crime and 7.4% for property crime — yet enforcement data reflect the opposite emphasis. **Audit action:** treat a model's output distribution as evidence about the data-generating institution, then check whether that institution is the thing you meant to measure.

---

## §7. Step 6 — Audit the Model, Not Only the Data

**Every model should ship a package insert (p. 98).** Prescription drugs carry detailed inserts describing use, pitfalls, prevalence of adverse effects, and breakdowns. Tufte's proposal is the same document for statistical models, encountered everywhere the model is — textbooks, computer code, workaday practice, publications. His positive example (p. 99) is a real one: an engineering group's insert for Kaplan-Meier survival estimates, naming implicit factors that break the single-population assumption, lack of independence of censoring, lack of uniformity within a time interval, the effect of many censored values, patterns in plots of censored versus noncensored values, and special problems with small samples. Each use of a model should remind users of its constraints, assumptions, and breakdowns.

**Model multiplicity is the default, not the exception.**

- With enough parameters a model fits anything. Tufte quotes von Neumann: with four parameters he can fit an elephant, and with five he can make it wiggle its trunk (p. 106). Physics supplies the same point at scale — symmetry groups with plentiful parameters tuned to make protons live as long as one likes; one model might be correct, but no one would ever know.
- Feller's case (p. 106): a large literature established a transcendental "law of logistic growth" for human populations, bacterial colonies, and railroads, with lengthy tables and chi-square tests — but the normal, the Cauchy, and other distributions fit the same material equally well or better. The logistic played no distinguished role whatever. **Goodness of fit does not select a mechanism.**
- Curve-fitting choices carry messages independent of the data (p. 105, via xkcd): linear, quadratic, logarithmic, connecting lines, exponential, LOESS, ad-hoc filter, logistic, confidence interval, piecewise, house-of-cards. The same scatter supports all of them.

**People cannot keep their own score (p. 106).** If someone shows you simulations that only demonstrate the superiority of their own method, be suspicious; good simulations show where a method shines *and* where it breaks. The hidden mechanism named on the same page: authors tune their own method thoroughly and tune the competing methods insufficiently. **Audit action:** ask for the failure regime. A method with no published failure regime has not been characterized.

**A good model explains data; it does not memorize it (p. 106).** Overfitted models chasing data are brittle, break down, and regress toward the truth when confronted with new data. Computing millions of models is easy; explaining something well enough to yield replicated real-world explanations and successful interventions is very difficult. Tufte's emblem is Borges's map at 1:1 scale — perfect, useless, and eventually left to the inclemencies of sun and winter.

**Fresh data remodels models (p. 107).** The Phillips curve looked like a clean inflation–unemployment trade-off across U.S. data from 1961–1969; the subsequent 49 years, 1970–2018, scatter across the plane. **Audit action:** re-plot any foundational relationship with every year of data since the model was adopted, before using it.

**Against the classical error model (p. 104).** Tufte's claim is that empirical uncertainties and errors are not detected, measured, or modeled by standard statistical methods, and that estimating uncertainties under false assumptions — then announcing a hypothesis "true" or a difference "significant" — is falsification rather than inference. The assumptions are mentioned in textbooks and forgotten in workaday analysis and published reports. Linking math models to a noisy real world requires punning: calling two different things by the same name. Tukey's counterweight is the governing preference: far better an approximate answer to the right question, which is often vague, than an exact answer to the wrong question, which can always be made precise (Tukey, quoted p. 90).

**But do not over-refine either (p. 90).** Mosteller's essay, reproduced at length, records the statisticians' experience that when fairly crude measurements are refined, the change more often than not turns out to be small — policy decisions are frequently insensitive to the measure, and finer measures often act like weights that do not change the decision. This is not an argument against better information where it is needed; it is an argument for deciding **where the next money for investigation should go.** Aggregative statistics adequate for group policy may be inadequate for individual decisions, and that limit should be stated rather than hidden.

---

## §8. Step 7 — Demand the Data Behind the Summary

Binned, smoothed, and summarized displays are where an audit dies. Tufte's heading (p. 101) is unusually direct: **binning continuous data is medium-quality evidence of falsification.**

| Summary device | What it hides | Audit demand |
|---|---|---|
| Boxplot | Six visibly different datasets — and their 63 possible combinations — can yield one identical boxplot (p. 100); 2 of the 5 plotted points are just the min and max | The unbinned plot: Tufte's counter-display shows all 1,000 measurements in the same space |
| Double-binned boxplots | Binning X into columns and Y into quartiles manufactures thresholds and plateaus that are researcher-imposed, not data-driven, and notoriously hard to replicate. Tufte's synthetic case: 12 elephants on sinusoidal flight paths with identical local pulses, N = 2,598, binned until the boxplots tell a false story of steady dose-response gains reaching a highly significant novel threshold that supposedly warrants raising the dose (p. 101) | The original XY scatter, at full N |
| Binned quarterly business slide | One number per quarter, cherry-picked window. Two extra quarters change the story; twelve more change it again (p. 100) | The full unbinned time series — which in Tufte's redraw reveals high volatility and end-of-quarter upticks that may signal premature revenue recognition |
| Smoothed summary curve | Inliers and outliers alike; three different underlying datasets can share one naive summary model (p. 100) | The points, with the fit overlaid |

**The clutter defense, inverted (p. 101).** The standard objection is that showing all the data creates clutter. Tufte's reply: clutter in a data graphic is *evidence that your model does not fit the data — and that you know it*. Summary graphics that cover contrary data and depict thresholds not present in the dataset are obvious cheats, easily detected, and damaging to credibility. His scale argument: a billion people a day read e-maps with data densities twenty times greater than a deceptive small chart, so there is no basis for assuming readers become stupid on contact with a research report.

**Data-availability excuses are themselves data (p. 101).** Tufte catalogs the refusals — trade secret, would violate patient privacy, hard drive crashed, intellectual property, in litigation, patent pending, IPO silent period. Treat the excuse as an audit finding. The positive contrast is the exomoon paper (p. 102): not paywalled, code and curve-fitting open-source and replicable, not claimed as intellectual property, not patented or monetized.

**Cross-reference:** graphic distortion itself (Lie Factor, dimension inflation, scale breaks) belongs to `tufte-graphical-integrity`; the *culling and selection* of evidence belongs to `tufte-evidence-corruption`. This section covers only the audit demand: get behind the summary to the measurements.

---

## §9. Step 8 — Follow the Money

Tufte treats conflict of interest as a **detectable, measurable** property of a study — not an ad hominem.

> "But financial conflicts are detectable definitively and represent a uniquely perverse influence on the search for scientific truth." — Colin Begg, quoted in SWFE, p. 81

**The Memorial Sloan Kettering sequence (p. 116)** is the chapter's worked case and the reason the audit item exists. Investigative reporting by ProPublica and *The New York Times* found that financial conflict-of-interest statements in published articles diverged from researchers' actual conflicts — service on drug-company boards of directors (a fiduciary, primary loyalty), private start-ups, large consulting payments. Deans and researchers departed; thousands of corrections were issued to previously published papers; the MSK physician-in-chief resigned three days after the report. The replacement physician-in-chief then defended financial conflicts from first-person clinical experience and argued for *more* faculty on corporate boards. The institution's chief of biostatistics and epidemiology took the opposite view: the substantive problem was not failure to disclose conflicts but the conflicts themselves. The reply he received is the line to remember, because it is the entire anti-audit stance compressed into four words:

> "He works with data." — the MSK replacement physician-in-chief, on the chief of biostatistics, quoted in SWFE, p. 116

Tufte's answer, on the same page: working with data, epidemiologists have extended more lives than anyone — through vaccines, epidemic response, randomized trials, and the statistical analysis that proved smoking causes cancer, leading to cessation policies that prevented hundreds of millions of early deaths.

**The two epigraph authorities (p. 114).** Tufte frames professional self-interest as structural rather than personal:

> "People of the same trade seldom meet together, even for merriment and diversion, but the conversation ends in a conspiracy against the public, or in some contrivance to raise prices." — Adam Smith, quoted in SWFE, p. 114

> "It is difficult to get people to understand something, when their salary depends on their not understanding it." — Upton Sinclair, quoted in SWFE, p. 114

Alan Cassels, on the same page, supplies the operational form: across thousands of experts in psychiatric diagnosis, none ever proposed *tightening* the criteria for their favored diagnosis; all worried about missed cases, none about the harms and risks of mislabeling. **Audit action:** ask which direction of error the field is institutionally organized to fear. That direction is where the bias will be.

**Money in guidelines (pp. 114–115).** Guidelines are written exclusively by insiders, and joining a guideline panel advances an expert's specialty career. Some professional societies are large financial enterprises: one national cardiovascular association's fiscal 2016–2017 budget was **$912 million with 20% from corporate support**; **77% of a €60 million annual income** at a European cardiology society came from industry. Ioannidis's proposed remodel (p. 115) is a straight outsider-comparison move: have guidelines written by methodologists and patients with content experts consulted, or recruit specialists *unrelated* to the subject matter, because what seems crucially important to a field expert may look like minutiae to a less personally involved outsider.

**Gratitude is not an outcome measure (p. 115).** A cardiology chair's defense — "I do angioplasty and I have grateful patients" — is self-scoring: post-op gratitude does not measure whether an intervention works, is free of harm, or is worth its cost against alternatives. Tufte's line: using patient gratitude to assess medical work is like winning a race that has only one runner. The empirical rebuttal on the same page: high patient satisfaction is associated mainly with hospitality, but also with **more treatments, higher costs, and substantially higher mortality**, even after adjusting for baseline health and comorbidities.

**Regulatory capture as an audit finding (p. 112).** Tufte's proposal is that credibility assessments of research should be as rigorous and frequent as restaurant sanitation inspections or pre-sale home inspections — his example being a 42-page pre-sale report with 55 photographs including infrared images of electrical switch boxes. He grants that performance audits are themselves distortable by financial interests and captured bureaucracies, but sets the stakes with the counterfactual: **270,000 U.S. deaths attributed to oxycodone**, where every pill was approved by the FDA, made by licensed companies, prescribed by licensed doctors, sold by licensed pharmacists, and all **72 billion pills** (about 500 per U.S. household) tracked to the exact place, time, and amount of sale by the DEA. The only thing worse than regulatory agencies is the theater of failed agencies captured by those they regulate.

### Access and Ownership as an Audit Precondition (pp. 96–97)

Tufte breaks a two-page chapter-within-a-chapter into the middle of ch. 4, revisiting the electronic health record material from ch. 1. It belongs to the audit because **you cannot audit data you are contractually forbidden to look at.** Access is not a legal preliminary to the audit; it is the audit's first finding.

**The design principle being violated (p. 96).** Tufte invokes Berners-Lee's rule for data models: the point is to let a pool of information grow and evolve, which requires that *the method of storage must not place its own restraints on the information*. A record format that claims ownership of what it stores has inverted the rule — the container now governs the content.

**The gag order, and why it is an evidence problem (pp. 96–97).** Local EHR installations seize ownership of patient content by copyrighting it, and every login puts patients and staff through a click-through agreement. Tufte prints a parody terms-of-service that claims everything in the system — colors, words, photos, graphs, numbers, punctuation, artworks, logos, trademarks, and any compilation of them — and forbids reproduction "by any means," screenshots included; declining routes the user to a second box threatening to disable their medical record. He notes this is not a parody. The consequences that matter to an auditor:

| The barrier | What it makes unauditable |
|---|---|
| Screenshots of any interface element prohibited in research and at professional meetings | Interface research on the system that runs clinical command and control |
| Inconvenient opt-out designed into the software business model | Any measurement of how many users actually consented rather than surrendered |
| Patients redefined as "users" and "customers" | Whether their distinct legal rights as patients survived the redefinition |
| University medical centers signing anyway | Institutional norms of free speech, inquiry, and even anti-plagiarism rules |

**The experiment nobody registered (p. 97).** Tufte's framing is the sharpest audit move on the spread: everything within 50 meters of a patient must satisfy fussy, detailed regulatory, industrial, and professional standards — yet the question of whether EHRs are safe and effective, and whether benefits exceed harms to patients and staff, went unasked. So each installation amounts to one of the worst clinical trials ever run: patients and staff enrolled without consent in a vast unrandomized, uncontrolled experiment, with no measured outcomes, harms, or benefits, no stopping rule for excessive harm, and no Human Subjects Safety Review Board anywhere in sight. The failure is documented at length, and Tufte points to Atul Gawande's *Why Doctors Hate Their Computers* (2018) as the record of it.

**The remodel — the record belongs to the patient (p. 97).** Tufte reproduces Eric Topol's stacklist of two dozen short reasons a patient's health record must be theirs. Grouped, they are an argument about data provenance and custody rather than about sentiment:

| Grounds | Representative claims in Topol's list |
|---|---|
| Ownership | It is your body; you paid for it; it is worth more than any other kind of data about you |
| Custody failure | Legally owned by doctors and hospitals; sold, stolen, and hacked without your knowledge; homeless as you generate more of it |
| Access failure | Information blocking between hospitals; most doctors will not release office notes; no single institution holds a lifetime record; no patient can hand it to researchers who want it |
| Data quality | Full of mistakes that get copied and pasted forward and that you cannot edit; designed to maximize billing rather than health; roughly a tenth of medical scans repeated because the prior ones are inaccessible |
| Evidence of benefit | Patients with their own data are more engaged and have better outcomes; doctors with full access consult records routinely; security improves under decentralization |
| The ask | Owning your data should be a civil right; it could save your life |

**Audit actions.**
- Treat every contractual barrier to inspection as an entry in the audit findings, not as a neutral legal fact — it belongs on the same page as retraction status and funding source (§9, §13).
- Ask whether the system generating your data has ever been evaluated *as an intervention*: what outcome was measured, against what comparison, with what stopping rule.
- Establish who owns and can release the primary records **before** the audit is scoped. If nobody can produce them without a vendor's permission, the traceability question (§4, Q1) is already answered.

---

## §10. Step 9 — Replace False Model Assumptions with a Credibility Narrative

Tufte's positive proposal, and the row in the book's own remodeling table that this chapter delivers: **credibility narratives replace false assumptions of standard statistical models of uncertainty.**

A credibility narrative is prose that does what a confidence interval pretends to do: it states what is established, what competing explanations were considered and how each was countered, what remains unresolved, and what cannot be quantified at all.

**The exemplar — the Kepler-1625b exomoon paper (pp. 102–103).** Tufte reproduces it as a model of authentic presentation of data and uncertainty, and annotates its structure in the margins. The pattern:

| Move | What the paper does |
|---|---|
| State the finding plainly | Evidence favoring a moon hypothesis, from timing deviations and a flux decrement |
| Name the counter-explanations and counter each with specific evidence | The moon-like transit is not due to instrumental common mode, residual pixel sensitivity variations, or chromatic systematics; it occurs at the correct phase position; simultaneous detrending and photodynamical modeling retrieves a self-consistent solution |
| Then acknowledge what still gives pause | The moon's Neptunian size and inclined orbit are peculiar; the transit occurs late in the observations; inferred properties are sensitive to the trend-correction model |
| Give the formal number — and immediately bound it | A Bayes factor exceeding 400,000 for the moon model, followed at once by the observation that a minor unaccounted effect could change the interpretation entirely |
| Name the unquantifiable | The reservations exist because this would be a first-of-its-kind detection; formally, it is the unknown unknowns that cannot be quantified |
| Ask for replication | Advocate future monitoring to check model predictions and confirm repetition of the signal |

Tufte's marginal note is the transferable instruction: known and unknown unknowns are surely the case, are acknowledged here, and should be similarly acknowledged in medical research publications (p. 103).

**The second exemplar — dexamethasone (p. 104).** Tufte lists why the RECOVERY result is credible, and the list is a template: a randomized controlled trial; many sites; **all-cause mortality** as the measured outcome rather than a proxy, surrogate, or marker; a sufficient *n* (1,007 on invasive mechanical ventilation, 3,883 on oxygen only, 1,535 on neither); relative and absolute risks shown together (29.0% vs. 40.7%, RR 0.65; 21.5% vs. 25.0%, RR 0.80; and honestly, no benefit in the no-support group at 17.0% vs. 13.2%, RR 1.22); few financial conflicts because the researchers' object is public health; a drug already available worldwide at trivial cost; and — the decisive item — **independent replication within ten weeks** by a WHO meta-analysis of six additional trials with data from twelve countries. Tufte pairs it with the standing warning that first-discovery evidence is the most enthusiastic that will ever be found, and too good to be true.

**The meta-research grand truths (p. 111), usable as an audit prior:** well-designed randomized controlled trials are diamonds and most observational studies are sand; confirmation bias is omnipresent; money doesn't talk, it screams; and it's more complicated than that. Tufte's own caveat on the same page keeps the tool honest — meta-research is itself gameable, low-value journals have published thousands of sponsored and conflicted pseudo meta-research papers, and meta-research is often merely descriptive, identifying a problem and its prevalence without preventing it.

---

## §11. Step 10 — Score It

Tufte's proposed **quick credibility scoring for research on humans** (p. 113) is a weighted, signed checklist. Reproduced here as an auditable rubric; the weights are his.

| Positive | Weight |
|---|---|
| Independent honest validation / replication | **+8** |
| Randomized controlled trial | **+7** |
| Unconflicted funding of research | **+5** |
| Forensic audit of spreadsheet | **+5** |
| Empirical assessment of measurement error | **+4** |

| Negative | Weight |
|---|---|
| Spurious correlation (e.g., income drives both alleged cause and effect) | **−8** |
| Ghostwritten or ghost-produced graphics | **−8** |
| Substantive explanatory theory vague or scientifically impoverished | **−7** |
| Contractor / sponsor / researcher with prior history of publication bias or retractions | **−7** |
| p-hacking / model-hacking / subgroup-hacking | **−7** |
| Failed randomization | **−6** |
| Standard statistical model as sole assessment of error and uncertainty | **−6** |
| Results dependent on model assumptions | **−6** |
| Failure to report relative *and* absolute risk in the same paragraph | **−5** |
| Inappropriate image duplication | **−5** |
| Binning | **−5** |
| Severe multicollinearity | **−5** |
| Summary models shown without underlying data | **−5** |
| Diet / nutrition study | **−5** |
| Unusual, magical, or arcane methods (pseudo-control groups, poorly chosen instrumental variables, inappropriate cross-over designs) | **−5** |
| Over-fitting | **−4** |
| Midcourse changes in research protocol | **−3** |
| Undeclared financial conflict of interest | **−1 per $25,000 per author** |
| Partied with the sponsor's sales reps at professional meetings | **−0.5 per party, per author** |

**How Tufte proposes to run it (p. 113):**
- Scoring elements are based on **universal principles of scientific inference**, so scoring is global, neutral, and indifferent to specialty — no local, private, unscientific definitions of causality, patient outcomes, or financial conflict.
- Design the elements by **severity and prevalence**, and have epidemiologists, meta-researchers, and unconflicted biostatisticians do it.
- **Score the design and the database, not only the paper.** The same data from the same design is often published many times — which may indicate productivity, or salami-slicing, or vanity over-publishing. Recall the Mediterranean-diet case: score one, score all 267, with database and design scores carrying over each time the data are published (discounted for local over-fitting and sub-sub-group analysis). This is what makes scoring cheap.
- More than half of credibility scoring can be **automated**; score independently and replicate; if two scores diverge, a third or fourth adjudicates.
- Guard against capture. To avoid gaming, commercialization, and the capture of scoring by those being scored ("we're all on the same team"), Tufte proposes an **independent *Consumer Reports* model** as the best defense.
- Totals aggregate usefully: by high-impact article, research team, specialty, sponsor, journal, paywalled versus open source, publisher, university research center, laboratory, guideline — and by the articles, databases, and designs referenced in new drug approvals.

---

## §12. Named Failure Modes

| Failure mode | Signature | First check |
|---|---|---|
| **Sampling to Please** (p. 84) | Collectors know the desired answer; collection has discretion | Watch a full collection cycle in person |
| **Cleaning Mistaken for Auditing** (p. 91) | A green data-quality report offered as evidence of truth | Ask what the cleaning step could not have detected |
| **Anchored Audit** (p. 91) | Audit performed after someone peeked at preliminary findings | Verify audit preceded analysis; if not, the audit is compromised |
| **Untraceable Presentation** (p. 85, Q1) | Presented figures cannot be walked back to primary records | Demand primary data plus the processing chain |
| **Data Substitution / Unreasonable Precision / Contradictory Physics** (p. 85, Q2) | Conditions too alike; fit tighter than instrument error; mechanism violated | Cross-correlate conditions; compare residuals to the error budget |
| **Serial Innocent Explanation** (p. 85, Q3) | Each anomaly has a separate innocent story | Score the pattern across the whole body of work |
| **Batch Effect Correlated with Outcome** (p. 93) | Results cluster by processing date, site, lot, or operator | Plot the outcome against batch metadata before anything else |
| **Pseudo-Replication** (p. 86) | Reported *n* counts measurements, not independent units | Recompute *n* at the level of the independent unit |
| **Per-Protocol Substitution** (p. 92) | Analysis is of patients treated, not patients assigned | Require intention-to-treat plus the attrition path |
| **Surrogate Drift** (p. 94) | Hard outcome swapped for an easier marker mid-programme | Ask when the surrogate-to-outcome link was last validated |
| **Chihuahua Syndrome** (p. 92) | Free-text where a controlled vocabulary belongs | Count distinct values against the legitimate vocabulary |
| **Ground-Truth Equivocation** (p. 94) | A database is called truth; "proof of concept" follows | Name which sense of the term each step of the argument uses |
| **Survival Bias** (p. 94) | The dataset is the set of things that lasted | Reconstruct what did not survive to be recorded |
| **Absent-Variable Search** (p. 87) | Specification search over a database that lacks the causal variables | List required variables, mark the missing ones, stop |
| **Binning as Threshold Manufacture** (p. 101) | Cut-points and plateaus that are researcher-imposed | Demand the unbinned data at full N |
| **Summary-Only Display** (pp. 100–101) | Boxplot, smoothed curve, or one number per period | Demand the points; clutter means the model does not fit |
| **Self-Scored Simulation** (p. 106) | The author's method wins every published comparison | Ask for the regime where it breaks |
| **Gratitude-as-Outcome** (p. 115) | Satisfaction, hope, or thanks substituted for outcome | Check whether satisfaction correlates with *better* outcomes here |
| **Insider Guideline** (p. 114) | Recommendations authored solely by the specialty that profits | Ask who was excluded — methodologists, patients, outside specialists |
| **Data-Availability Excuse** (p. 101) | Trade secret, privacy, litigation, silent period, crashed drive | Record the refusal as an audit finding |
| **Contractual Unauditability** (pp. 96–97) | A click-through gag order forbids screenshots, reproduction, or inspection of the system holding the data | Establish who can release the primary records before scoping the audit |
| **Unevaluated Installed System** (p. 97) | A system everyone depends on was never evaluated as an intervention — no outcomes, no comparison, no stopping rule | Ask what was measured, against what, and who could have stopped it |

---

## §13. The Audit Checklist — What to Demand

Run in order. Each item is a demand made *of the supplier*, in writing, before analysis.

```
PROVENANCE
[ ] Primary data, unprocessed, plus the full processing chain to the presented figures
[ ] Written description of how, where, by whom, and with what instrument each variable is measured
[ ] The instrument's own technical manual section on artifacts and error
[ ] Chain of custody: who gathered it, who merged it, who redistributed it, every hop
[ ] Direct observation booked: watch one full collection cycle at the site
[ ] Legal right to inspect, screenshot, reproduce, and publish — named in writing, before scoping (§9)
[ ] Whoever can release the primary records identified by name, not by department

STRUCTURE
[ ] Batch metadata as first-class columns — date, site, instrument, lot, operator
[ ] Definition of the independent unit, and n recomputed at that level
[ ] Assignment records and the full attrition path from assignment to analysis
[ ] Controlled vocabularies for every categorical field; distinct-value counts reported
[ ] List of variables the causal story requires, with the absent ones marked

SPECIFICATION HISTORY
[ ] Pre-registration or a dated analysis plan written before the data were seen
[ ] Full log of models fitted, not the one reported; count them
[ ] Every midcourse protocol change, with date and reason
[ ] Held-out or independent data, and the result on it
[ ] Code, in a runnable state

PRESENTATION
[ ] Unbinned data at full N behind every summary, boxplot, or smoothed curve
[ ] Relative and absolute effects reported in the same paragraph
[ ] Primary endpoint in the primary population reported before any subgroup
[ ] Every figure panel screened for duplication, flip, and mirror reuse
[ ] Every spreadsheet re-opened with type coercion disabled and diffed against source

CREDIBILITY
[ ] Who paid — funder, sponsor, employer, consulting relationships, board seats, equity
[ ] Retraction status of the source and of the sources it relies on
[ ] Replication status: independent, on new data, by unaffiliated analysts
[ ] A written credibility narrative: counter-explanations countered, residual concerns named,
    unknown unknowns acknowledged (§10)
[ ] Credibility score computed (§11), independently replicated, divergences adjudicated
```

**Stop conditions.** Any one of these ends the audit with a negative finding rather than a caveat: primary data cannot be produced; batch metadata was never recorded; the required causal variables are absent from the database; the audit was performed after someone saw preliminary results; the analysis is per-protocol with no attrition record; the supplier declines inspection.

---

## §14. Scope Boundaries

| Question | Skill |
|---|---|
| What *kind* of corruption is this, and what is it called? | `tufte-evidence-corruption` |
| Is this chart's ink proportional to its numbers? | `tufte-graphical-integrity` |
| Am I accepting an inherited model or format without looking? | `tufte-visual-thinking` |
| Does this display show individual values and aggregate pattern at once? | `tufte-micro-macro-readings` |
| **How do I actually audit this analysis, and what do I demand?** | **this skill** |

---

Source: Edward Tufte, *Seeing With Fresh Eyes: Meaning, Space, Data, Truth* (Graphics Press, 2020) — ch. 4, "Data Analysis When the Truth Matters: On the Relationship Between Evidence and Conclusions. Remodeling Statistical Practice and Teaching," printed **pp. 80–119**. The chapter's title page is p. 81; p. 80 is its facing epigraph spread, and Tufte's own visual index groups it under chapter 4 (p. 167). The Nabokov/Kafka markup on p. 120 belongs to **chapter 5**, not this one — the visual index (p. 170) and the permissions apparatus (p. 173) both file it there. All page numbers are printed pages. Material is paraphrased throughout; direct quotations are limited to single attributed sentences, and all quoted lines above are third-party voices Tufte himself quotes (Feynman p. 80, Daniel p. 84, Darwin p. 86, Tukey p. 90, Begg p. 81, Smith and Sinclair p. 114, von Neumann p. 106, the MSK physician-in-chief p. 116). The adverse-effects percentages on p. 98 are Tufte's satirical mock-up, not measured prevalence.
