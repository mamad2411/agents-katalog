# Drug Response

Dose-response modeling and drug sensitivity prediction in cancer cell lines. Covers IC50 and AUC estimation from viability curves, retrieval and harmonization of GDSC, CTRP, and PRISM data through PharmacoGx, DepMap dependency and drug data, sensitivity prediction with regularized regression, and pharmacogenomic biomarker discovery.

## When to Use This Skill

Activate when the user requests:
- IC50, EC50, or AUC estimation from dose-response data
- Four-parameter logistic (4PL) curve fitting
- GDSC, CTRP, PRISM, or CCLE drug sensitivity retrieval
- DepMap dependency or drug screen data
- Cross-dataset harmonization of drug response
- Drug sensitivity prediction from expression or mutation
- Pharmacogenomic biomarker discovery
- Distinguishing IC50 from AUC as a response metric

## Inputs

| Data Type | Format | Source |
|-----------|--------|--------|
| Dose-response | Concentration, viability per well | Screening plates, published curves |
| Curated sensitivity | PharmacoSet (`.rds`) | PharmacoGx, ORCESTRA |
| Cell line molecular | Expression, mutation, CNV matrices | DepMap, CCLE |
| Drug annotation | SMILES, target, mechanism | DepMap, ChEMBL |

---

## Environment

Versions verified 2026-08.

```r
# Curated drug response, the practical entry point
BiocManager::install("PharmacoGx")      # 3.16.0 (Bioconductor)
#   NOT the CRAN PharmacoGx, which is frozen at 1.1.6 from 2016.
#   install.packages("PharmacoGx") gets a decade-old package. Use Bioconductor.

# Dose-response curve fitting
install.packages("drc")                 # 3.0-1 (2016). Stale but standard.
install.packages("nplr")                # 0.1-8 (2025). Maintained alternative.

# GDSC's own fitting pipeline
# remotes::install_github("CancerRxGene/gdscIC50")   # not on CRAN

# DepMap data in R
BiocManager::install("depmap")          # ExperimentHub interface to releases
```

```
Data source status, checked 2026-08:

  DepMap            depmap.org/portal — up. Distributes CCLE molecular data,
                    CRISPR dependency (Chronos), and the PRISM drug repurposing
                    screen. The practical download host.
  cancerrxgene.org  the GDSC website is currently returning HTTP 410 Gone,
                    on every path. Do not hardcode a download URL against it.
                    GDSC processed data is mirrored through DepMap and wrapped
                    by PharmacoGx, which is how to obtain it reliably now.
  PharmacoDB        pharmacodb.ca — up. Cross-dataset query interface.
  ORCESTRA          orcestra.ca — versioned, citable PharmacoSet objects.

Because the primary GDSC portal is unstable, prefer the curated PharmacoSet
route over scraping raw files. It also fixes the harmonization problems below.
```

---

## Dose-Response Curves

### IC50 is the wrong default metric

```
IC50   the concentration giving 50% of maximum inhibition.
AUC    the area under the dose-response curve, or its complement.

IC50 fails in common, important cases:
  - A drug that plateaus at 60% viability never reaches 50% inhibition.
    Its IC50 is undefined, and pipelines report it as the max tested
    concentration, which is not a measurement.
  - IC50 ignores the shape of the curve. Two drugs with the same IC50 can
    have very different efficacy at every other concentration.
  - It sits at one point, so it is sensitive to noise there.

AUC integrates the whole curve, is always defined, and correlates better
with clinical response. GDSC, CTRP and DepMap all report AUC for this reason.
Prefer AUC. Report IC50 only when a specific downstream method requires it,
and note when it was extrapolated rather than observed.
```

### Fitting a 4PL curve

```r
library(drc)   # v3.0-1

# Four-parameter log-logistic: lower asymptote, upper asymptote, slope, EC50
fit <- drm(viability ~ concentration, data = dr,
           fct = LL.4(names = c("slope", "lower", "upper", "ec50")))

ic50 <- ED(fit, 50, interval = "delta")   # 50% effective dose, with CI
```

```
LL.4 vs LL2.4: LL2.4 parameterizes ec50 on the log scale, which is far more
numerically stable when concentrations span several orders of magnitude, as
drug screens always do. Prefer LL2.4 for real data.

Constrain the asymptotes. Unconstrained, drm() can fit a lower asymptote of
-40% viability or an upper asymptote of 130%, which are not biological. Fix
the upper asymptote near 100% (untreated) and bound the lower at 0:
  drm(..., fct = LL.4(), lowerl = c(-Inf, 0, -Inf, -Inf),
                         upperl = c( Inf, Inf, 110, Inf))

Convergence failures are common and SILENT-ish. drm() may return a fit that
did not converge with only a warning. drc stores convergence as a LOGICAL in
fit$fit$convergence, where TRUE means it converged (this is not the optim()
integer convention where 0 means success). Check isTRUE(fit$fit$convergence),
and refit failures with different starting values rather than trusting the
returned parameters.
```

### The maintained alternative

```r
library(nplr)   # v0.1-8, actively maintained

# nplr chooses the number of parameters by goodness of fit and is more robust
# to the convergence problems above
np <- nplr(x = dr$concentration, y = dr$viability / 100, useLog = TRUE)
getAUC(np)             # AUC directly
getEstimates(np, 0.5)  # IC50 with confidence bounds
```

`nplr` weights points by a Poisson-like scheme (`LPweight`) that downweights the noisy extremes of the curve, which is usually what you want for screening data.

### GDSC's own pipeline

GDSC does not fit each curve independently. `gdscIC50` fits a **single joint model** across a drug's cell lines with a shared shape, which stabilizes IC50 estimates for cell lines with few informative points. If you are reproducing GDSC IC50 values, per-curve `drm()` will not match them; use `gdscIC50`.

---

## Retrieving Curated Data

```r
library(PharmacoGx)   # Bioconductor 3.16.0

availablePSets()                          # what can be downloaded
pset <- downloadPSet("GDSC_2020")         # a curated PharmacoSet

# Sensitivity as a drug x cell-line matrix
auc <- summarizeSensitivityProfiles(pset, sensitivity.measure = "aac_recomputed")
ic50 <- summarizeSensitivityProfiles(pset, sensitivity.measure = "ic50_recomputed")

# Matched molecular data from the same object
expr <- summarizeMolecularProfiles(pset, mDataType = "rna")
```

```
Use the *_recomputed measures, not the published ones.

PharmacoGx refits every curve with one consistent method. The published IC50
and AUC in each source used that source's own fitting pipeline, so published
values are NOT comparable across GDSC, CTRP and PRISM. The recomputed values
are, which is the entire point of the curated object.

aac_recomputed is the "activity area" (1 - AUC). Higher means more sensitive.
Confirm the direction before correlating with anything: half the confusion in
this field is a sign flip between AUC and AAC.
```

## Cross-Dataset Concordance

```
Drug response measured on the same cell line and drug in two datasets agrees
only moderately. Reported Spearman correlations between GDSC and CTRP are
often in the 0.5-0.7 range for the same drug, and lower for drugs with a
narrow response range.

Why it disagrees:
  Different assays (CellTiter-Glo vs Syto60), incubation times, seeding
  densities, and concentration ranges. A drug tested to 10 uM in one study
  and 1 uM in another cannot yield the same AUC.
  Cell line identity drift and misidentification between panels.

Consequence: a biomarker discovered in one dataset must be validated in
another before it means anything. Do not train and test on the same panel and
report the cross-validation as external validation.
```

```r
# PharmacoGx computes concordance directly
common <- intersectPSet(list(gdsc, ctrp), intersectOn = c("cell.lines", "drugs"))
```

## Sensitivity Prediction

### The task and its baseline

```
Predict a continuous response (AUC or IC50) for a cell line from its molecular
features (expression, mutation, CNV).

Baseline that is hard to beat: ridge or elastic-net regression on expression.
Deep models rarely improve on it for this task at cell-line scale, for the
same reason they struggle in single-cell (the sample count is small relative
to the feature count). Always report the linear baseline.
```

```r
library(glmnet)

# Expression as predictors, drug AUC as response
x <- t(expr)                       # cell lines x genes
y <- auc["Erlotinib", rownames(x)]
keep <- !is.na(y)

cv <- cv.glmnet(x[keep, ], y[keep], alpha = 0.5)   # elastic net
coef(cv, s = "lambda.min")                          # selected biomarker genes
```

```
Two failures that inflate reported accuracy:

  Feature leakage: selecting the top genes by correlation with response on the
  FULL dataset, then cross-validating. The selection has already seen the test
  fold. Put feature selection inside the CV loop.

  Tissue confounding: cell lines from the same lineage share both expression
  and response. A model can predict response by predicting lineage and looking
  up its average sensitivity, learning nothing drug-specific. Test across
  lineages, or stratify by lineage and report within-lineage performance.
```

### Pharmacogenomic biomarkers

```r
# Univariate association across all drugs, corrected for tissue
sig <- drugSensitivitySig(pset, mDataType = "rna",
                          sensitivity.measure = "aac_recomputed",
                          features = c("EGFR", "BRAF", "KRAS"))
```

```
A biomarker association is a hypothesis, not a mechanism. The established
positive controls are the ones to sanity-check any pipeline against:
  BRAF mutation      -> sensitivity to BRAF inhibitors
  EGFR mutation      -> sensitivity to EGFR inhibitors (in the right context)
  MDM2 amplification -> sensitivity to MDM2 inhibitors
If these do not surface as top hits, the pipeline has a problem before any
novel biomarker is worth reporting.

Correct for tissue of origin. Without it, an association is often just a
lineage that happens to be both mutation-enriched and drug-sensitive.
```

## Output Specification

| Output | Format | Description |
|--------|--------|-------------|
| `fitted_curves.rds` | RDS | Per-curve model objects with convergence status |
| `sensitivity_matrix.csv` | CSV | Drug x cell-line AUC (or AAC), recomputed |
| `ic50_estimates.csv` | CSV | IC50 with CI, and a flag when extrapolated |
| `concordance.csv` | CSV | Cross-dataset correlation per drug |
| `biomarker_associations.csv` | CSV | Feature, drug, effect, tissue-corrected p |
| `prediction_model.rds` | RDS | Fitted glmnet with the CV scheme recorded |
| `held_out_performance.csv` | CSV | Cross-lineage performance, not within-panel CV |

## Validation Checks

```
Curve fitting
  Convergence checked per curve; non-converged fits flagged, not silently kept.
  Asymptotes constrained to a biological range.
  IC50 values that equal the max tested concentration marked as extrapolated,
  not reported as measurements.
  AUC reported as the primary metric.

Data retrieval
  PharmacoGx *_recomputed measures used for any cross-dataset comparison.
  AUC vs AAC direction confirmed before correlating.
  Cell line identifiers harmonized (the same line has different names across
  panels).

Prediction
  Feature selection is inside the cross-validation loop.
  Performance reported across lineages, not only within-panel CV.
  Linear baseline (ridge/elastic net) reported alongside any complex model.

Biomarkers
  Known positive controls (BRAF, EGFR, MDM2) recovered as top hits.
  Associations corrected for tissue of origin.
```

## Common Pitfalls

### Curve fitting
1. **Reporting IC50 for a curve that never reaches 50% inhibition**: a drug plateauing at 60% viability has no IC50. Pipelines substitute the max concentration, which is not a measurement. Use AUC, and flag extrapolated IC50 values.
2. **Trusting a `drm()` fit without checking convergence**: it can return non-converged parameters with only a warning. Check `isTRUE(fit$fit$convergence)` — drc uses a logical where `TRUE` means converged, not the optim `== 0` convention — and refit failures with new starting values.
3. **Fitting on a linear concentration scale**: use `LL2.4` (log EC50) for concentrations spanning orders of magnitude, which every drug screen does.
4. **Leaving asymptotes unconstrained**: unconstrained fits produce negative viability or 130% upper asymptotes. Bound them to biology.
5. **Per-curve fitting when reproducing GDSC**: GDSC uses a joint model across cell lines (`gdscIC50`). Independent `drm()` fits will not reproduce its IC50 values.

### Data
6. **Installing PharmacoGx from CRAN**: the CRAN version is 1.1.6 from 2016. The maintained package is on Bioconductor. `install.packages("PharmacoGx")` silently gets the old one.
7. **Hardcoding a cancerrxgene.org download URL**: the GDSC site currently returns HTTP 410. Retrieve GDSC data through PharmacoGx or DepMap instead.
8. **Comparing published IC50/AUC across datasets**: each source fit curves its own way, so published values are not comparable. Use the recomputed measures.
9. **Confusing AUC and AAC direction**: AAC = 1 - AUC. Higher AAC means more sensitive; higher AUC means more resistant. A sign flip here silently inverts every result.

### Prediction
10. **Feature selection outside the CV loop**: selecting biomarker genes on the full dataset before cross-validating leaks the test fold and inflates accuracy. Select inside each fold.
11. **Ignoring tissue confounding**: a model can predict drug response by predicting lineage. Test across lineages, and report within-lineage performance.
12. **Omitting the linear baseline**: ridge and elastic net are hard to beat for cell-line sensitivity prediction. A complex model that does not beat them is not worth its cost.
13. **Reporting within-panel cross-validation as external validation**: cross-dataset concordance is only moderate, so a biomarker must be validated on an independent panel to mean anything.

## Related Skills

- [`cancer-multiomics`](../cancer-multiomics/SKILL.md): the expression and mutation features that predict drug response
- [`variant-annotation`](../variant-annotation/SKILL.md): classifying the variants used as pharmacogenomic biomarkers
- [`foundation-models`](../foundation-models/SKILL.md): the same "report the linear baseline" discipline applies to response prediction

## Public Datasets for Testing

| Dataset | Content | Access |
|---------|---------|--------|
| GDSC (via PharmacoGx) | ~700 lines, ~140 drugs, IC50/AUC | `downloadPSet("GDSC_2020")` |
| CTRPv2 | ~860 lines, ~500 compounds | `downloadPSet("CTRPv2_2015")` |
| PRISM (DepMap) | Repurposing screen, ~4500 compounds | DepMap portal |
| CCLE | Molecular profiles for the cell lines | `depmap` package, DepMap portal |
| GDSC1000 curve example | Small dose-response set for fitting | `gdscIC50` package |
