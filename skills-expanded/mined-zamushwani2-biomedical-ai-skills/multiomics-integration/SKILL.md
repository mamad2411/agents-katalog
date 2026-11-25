# Multi-Omics Integration

Joint analysis of two or more molecular layers on the same samples. Covers method selection, the preprocessing that decides whether integration works at all, MOFA+ factor analysis, similarity network fusion, joint clustering for cancer subtyping, supervised integration, and survival models built on integrated features.

## When to Use This Skill

Activate when the user requests:
- Combining expression with methylation, mutation, CNV, or proteomics
- MOFA+, MOFA2, SNF, iClusterPlus, DIABLO, or mixOmics
- Cancer subtyping from more than one data type
- Latent factors or components shared across omics layers
- Survival modelling on integrated multi-omics features
- Deciding which integration method suits their design

## Inputs

| Data Type | Form | Note |
|-----------|------|------|
| Expression | genes x samples, log-CPM or VST | usually the largest view |
| Methylation | probes/regions x samples, M-values | beta-values are heteroscedastic |
| CNV | segments or gene-level x samples | discrete-ish, often bimodal |
| Proteomics | proteins x samples | far fewer features, more missingness |
| Clinical | samples x variables | outcome for supervised methods |

Every view must be indexed by the **same sample identifiers**. Integration is a join before it is a model.

---

## Environment

Versions verified 2026-08.

```r
BiocManager::install("MOFA2")           # 1.22.0  factor analysis
BiocManager::install("iClusterPlus")    # 1.48.0  joint clustering
BiocManager::install("mixOmics")        # 6.36.0  supervised (DIABLO)
install.packages("SNFtool")             # 2.3.1   similarity fusion
```

```
INSTALL mixOmics FROM BIOCONDUCTOR, NOT CRAN.

  CRAN         mixOmics 6.3.2, published 2018-06-01
  Bioconductor mixOmics 6.36.0

install.packages("mixOmics") silently gives you an eight-year-old build with
a different API. This is the same trap as PharmacoGx. Check which one you
actually loaded: packageVersion("mixOmics").

SNFtool 2.3.1 was last released 2021-06-11. It still works and the algorithm
is unchanged, but expect no fixes. Say so when you depend on it.
```

### MOFA2 in R is a Python package

```
MOFA2's R package is a front end. The solver is the Python package mofapy2,
called through reticulate. Two consequences that produce confusing failures:

  run_mofa(object, outfile = NULL, save_data = TRUE, use_basilisk = FALSE)

use_basilisk defaults to FALSE, so by default MOFA2 uses whatever Python
reticulate happens to find. If mofapy2 is not installed there, training
fails at run_mofa() with a Python import error, long after the R-side setup
looked fine. Pass use_basilisk = TRUE to get the managed, pinned environment.

That managed environment pins python=3.12.10 and numpy=1.26.4 - numpy 1.x.
If you are also driving a numpy 2.x stack from the same session, keep them
apart. Confirm what you got:

    reticulate::py_config()
    reticulate::py_module_available("mofapy2")
```

---

## Choosing the Method

The question decides the method. Picking by popularity is how people end up reporting factors they cannot interpret.

```
Do you have an outcome you want the integration to predict?
  YES -> supervised: DIABLO (mixOmics). Components are chosen to
         discriminate the outcome AND correlate across views.
  NO  -> unsupervised, then ask what you want out:

         interpretable FACTORS, tolerant of missing views
           -> MOFA+ (MOFA2). Variance decomposition per factor per view
              tells you which layer drives what.

         patient CLUSTERS from fused similarity
           -> SNF. Fuses per-view patient-similarity networks, then
              spectral-clusters the fused network.

         joint clusters with FEATURE SELECTION built in
           -> iClusterPlus. Latent variable model with lasso penalties;
              slow, and you must tune the penalties.
```

```
A supervised method fitted and then evaluated on the same samples will
report excellent discrimination whatever the data. DIABLO in particular
selects features using the outcome. If you report its training performance
as evidence, you have reported nothing. Hold out samples, or cross-validate
with the selection inside the fold.
```

## Preprocessing Decides Everything

More integrations fail here than in the model.

### Sample intersection

```r
common <- Reduce(intersect, lapply(views, colnames))
views  <- lapply(views, function(v) v[, common, drop = FALSE])
```

```
Report how many samples survived the intersection and how many each view
started with. A cohort of 500 with expression, 480 with methylation and 90
with proteomics integrates to 90. That is the study you actually ran, and it
is often a surprise to everyone including the analyst.

MOFA+ tolerates missing views for a sample, which is a real advantage: you
can keep the 500 and let the model use what exists per sample. SNF and
iClusterPlus need complete cases. Choosing MOFA+ for this reason is
legitimate; pretending SNF used 500 samples when it used 90 is not.
```

### Scale and feature-count imbalance

```
Two problems that both let one view dominate:

  SCALE     expression in log-CPM (range ~0-15), methylation M-values
            (range ~-6 to 6), CNV log-ratios (~-2 to 2). A method that
            works on variance will follow whichever view has the largest
            numbers. Centre and scale each view.

  DIMENSION 20,000 genes against 100 proteins. Even after scaling, the
            20,000-feature view contributes far more total variance simply
            by having more features. Feature-select per view first
            (top-N most variable is the usual choice) and report N.

MOFA2 has scale_views in its data options for the first problem. It does
nothing about the second. A 2,000-gene view against a 100-protein view is a
20:1 imbalance, not the 200:1 you started with, and it is worth saying which
you used.
```

### Methylation is not expression

```
Use M-values, not beta-values, for anything variance-based. Beta is bounded
in [0,1] and strongly heteroscedastic: variance collapses near 0 and 1, so
a variance-ranked feature selection preferentially picks intermediate-
methylation probes regardless of biology. M = log2(beta/(1-beta)).

Convert back to beta only for reporting, because M-values are not
interpretable as a percentage.
```

## MOFA+

```r
library(MOFA2)

object <- create_mofa(list(rna = rna_mat, meth = meth_mat, prot = prot_mat))

data_opts  <- get_default_data_options(object)
data_opts$scale_views <- TRUE          # equalise variance across views

model_opts <- get_default_model_options(object)
model_opts$num_factors <- 15           # an upper bound, not a target

train_opts <- get_default_training_options(object)
train_opts$seed <- 42                  # MOFA is stochastic; fix and report it

object <- prepare_mofa(object, data_options = data_opts,
                       model_options = model_opts,
                       training_options = train_opts)
model  <- run_mofa(object, use_basilisk = TRUE)
```

```
num_factors is an UPPER BOUND. MOFA prunes factors that explain less
variance than a threshold, so asking for 15 and getting 8 is the model
working, not failing. Report how many survived.

Read the variance decomposition before interpreting any factor:

    plot_variance_explained(model, x = "view", y = "factor")

A factor loading almost entirely on one view is that view's internal
structure, not integration. The factors worth the name are the ones with
substantial variance in two or more views. Say which is which rather than
presenting all factors as "multi-omics factors".

MOFA factors are UNSUPERVISED and unordered by importance to your question.
Factor 1 is the largest source of variance, which in tumour data is very
often tumour purity, sex, or batch. Correlate every factor against known
covariates before claiming biology.
```

## Similarity Network Fusion

```r
library(SNFtool)   # 2.3.1

Ws <- lapply(views, function(v) {
  x <- standardNormalization(t(v))          # samples x features
  affinityMatrix(dist2(x, x), K = 20, sigma = 0.5)
})
W <- SNF(Ws, K = 20, t = 20)
groups <- spectralClustering(W, K = 3)
```

```
Defaults, from the source: affinityMatrix(diff, K = 20, sigma = 0.5) and
SNF(Wall, K = 20, t = 20). K is the number of neighbours, sigma the kernel
width, t the fusion iterations.

K = 20 is a neighbourhood size, so it is only sensible when the cohort is
much larger than 20. On 60 samples, K = 20 makes a third of the cohort every
patient's neighbour and the fused network approaches a single blob. Scale K
to the cohort and state it.

SNF returns a similarity matrix, not clusters. The number of clusters is
YOUR choice, made afterwards. Estimating it from eigengaps
(estimateNumberOfClustersGivenGraph) is standard, but it is an estimate, and
different K and sigma give different answers. Report the stability of the
cluster count under those settings, not a single number.
```

## Joint Clustering with iClusterPlus

```
iClusterPlus fits a joint latent variable model with lasso penalties, so it
selects features while clustering. That is its appeal and its cost:

  - you must tune the penalty per view (tune.iClusterPlus), which is a grid
    search over a slow model. Budget hours, not minutes.
  - it wants data-type declarations per view (gaussian, binomial, poisson,
    multinomial). Passing binary mutation data as gaussian runs fine and
    fits nonsense.
  - k is the number of latent variables and gives k+1 clusters.

For a first pass, MOFA+ or SNF answers the same question faster. Reach for
iClusterPlus when built-in feature selection is the point.
```

## Supervised Integration: DIABLO

```r
library(mixOmics)   # Bioconductor 6.36.0, NOT CRAN 6.3.2

design <- matrix(0.1, nrow = length(views), ncol = length(views))
diag(design) <- 0
result <- block.splsda(X = views, Y = outcome, ncomp = 2, design = design)
```

```
The design matrix sets how hard the model tries to make views correlate with
each other, against how hard it tries to predict Y. Values near 0 favour
prediction; near 1 favour cross-view correlation. It is a modelling choice
that changes the answer, so state the value and why.

DIABLO selects features using Y. Every performance number must therefore
come from held-out samples, with the selection repeated inside each fold.
perf() and tune.block.splsda() do this correctly; a manual fit on all
samples does not.
```

## Survival on Integrated Features

```
Integrated features go into survival models the same way any high-dimensional
features do, and inherit the same failure modes:

  p >> n, always. Even 15 MOFA factors against 90 patients with 30 events is
  3 events per parameter, below the usual 10-events-per-variable guidance.
  Regularize (glmnet with family = "cox") or preselect on a principled basis.

  Cluster membership from SNF or iClusterPlus is not a covariate you may
  test on the same samples that defined it. The clustering saw the data; a
  log-rank test across those clusters is circular. Validate the assignment
  on an independent cohort, or report it as a descriptive finding.

  MOFA factors are unsupervised, so testing them against survival is
  legitimate. Correct for the number of factors tested.
```

```r
library(glmnet)   # 5.0
fit <- cv.glmnet(factor_matrix, Surv(time, status), family = "cox", alpha = 0.5)
```

```
glmnet moved to 5.0 (2026-05). Pin it in any analysis you intend to
reproduce, and re-check results if you are moving from 4.x, because a
solver change alters which features survive at a given lambda even when the
API does not change.
```

## Output Specification

| Output | Format | Description |
|--------|--------|-------------|
| `sample_intersection.csv` | CSV | samples per view, and the integrated set |
| `preprocessing.json` | JSON | per-view scaling, transform, features retained |
| `mofa_model.hdf5` | HDF5 | trained model with its seed |
| `variance_explained.csv` | CSV | variance per factor per view |
| `factor_covariates.csv` | CSV | each factor correlated against purity, sex, batch |
| `clusters.csv` | CSV | assignment, method, K and sigma used |
| `survival_model.rds` | RDS | fitted model with the CV scheme recorded |

## Validation Checks

```
Data preparation
  Sample intersection reported per view and for the integrated set.
  Each view centred and scaled; scaling stated.
  Per-view feature selection stated with N, and the resulting imbalance.
  Methylation as M-values, not beta, for variance-based methods.

Model
  MOFA num_factors treated as an upper bound; surviving count reported.
  Variance decomposition inspected; single-view factors labelled as such.
  Every factor correlated against purity, sex and batch before interpretation.
  Seed fixed and reported for stochastic methods.
  SNF K scaled to the cohort, not left at 20 on a small one.
  Cluster count reported with its stability across settings.

Supervised and survival
  DIABLO performance from held-out samples with selection inside the fold.
  Cluster-based survival tests not run on the samples that defined them.
  Events-per-parameter reported; regularization used when p >> n.
  mixOmics version confirmed to be the Bioconductor build.
```

## Common Pitfalls

### Setup
1. **Installing mixOmics from CRAN**: CRAN carries 6.3.2 from 2018 while Bioconductor has 6.36.0. `install.packages()` silently gives an eight-year-old API. Check `packageVersion("mixOmics")`.
2. **Calling `run_mofa()` without `use_basilisk = TRUE`**: it defaults to `FALSE` and uses whatever Python reticulate finds. If `mofapy2` is not there, training fails with a Python import error after the R setup looked fine.
3. **Mixing MOFA2's pinned environment with a numpy 2.x stack**: its basilisk environment pins `numpy=1.26.4`. Keep them in separate sessions.
4. **Depending on SNFtool without saying so**: last released 2021-06-11. The algorithm is stable but unmaintained; state it.

### Preprocessing
5. **Not reporting the sample intersection**: 500 expression + 480 methylation + 90 proteomics integrates to 90 complete cases. That is the study, and it should be stated up front.
6. **Leaving views on their native scales**: log-CPM, M-values and log-ratios have different ranges, so a variance-based method follows the largest numbers. Centre and scale per view.
7. **Ignoring feature-count imbalance**: 20,000 genes against 100 proteins lets the big view dominate even after scaling. Feature-select per view and report N.
8. **Using beta-values for variance-based selection**: beta is bounded and heteroscedastic, so ranking by variance picks intermediate-methylation probes regardless of biology. Use M-values.

### Interpretation
9. **Treating `num_factors` as a target**: it is an upper bound. MOFA prunes uninformative factors; asking for 15 and getting 8 is correct behaviour.
10. **Calling every MOFA factor a multi-omics factor**: a factor loading almost entirely on one view is that view's internal structure. Read the variance decomposition and label single-view factors as such.
11. **Interpreting Factor 1 as biology without checking**: the largest variance component in tumour data is very often purity, sex or batch. Correlate every factor against known covariates first.
12. **Leaving SNF at `K = 20` on a small cohort**: with 60 samples that makes a third of the cohort every patient's neighbour and the fused network collapses toward one blob. Scale K.
13. **Reporting a single cluster count from SNF**: it returns a similarity matrix, not clusters. The count is your choice and moves with K and sigma; report its stability.
14. **Declaring binary mutation data as gaussian in iClusterPlus**: it runs and fits nonsense. Declare the distribution per view.

### Evaluation
15. **Reporting DIABLO training performance**: it selects features using the outcome, so training performance is not evidence. Use held-out samples with selection inside each fold.
16. **Testing survival across clusters on the samples that defined them**: the clustering already saw the data, so the log-rank test is circular. Validate externally or report descriptively.
17. **Fitting an unregularized Cox model on integrated features**: 15 factors against 30 events is far below ten events per variable. Regularize and report events-per-parameter.

## Related Skills

- [`cancer-multiomics`](../cancer-multiomics/SKILL.md): producing the per-layer matrices that feed integration
- [`survival-analysis`](../survival-analysis/SKILL.md): the time-to-event models that consume integrated features
- [`drug-response`](../drug-response/SKILL.md): the same leakage and confounding discipline for prediction
- [`single-cell-atlas`](../single-cell-atlas/SKILL.md): integration at the cell rather than the patient level

## Public Datasets for Testing

| Dataset | Layers | Access |
|---------|--------|--------|
| TCGA (any project) | expression, methylation, CNV, mutation | GDC, open |
| CPTAC | proteomics matched to TCGA-style genomics | open |
| MOFA2 CLL example | expression, methylation, mutation, drug response | ships with MOFA2 |
| SNFtool example data | two synthetic views with known clusters | ships with SNFtool |
