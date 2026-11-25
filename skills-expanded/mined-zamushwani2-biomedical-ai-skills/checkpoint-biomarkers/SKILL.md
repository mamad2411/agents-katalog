# Checkpoint Biomarkers

Predictive biomarkers for immune checkpoint blockade: what PD-L1 IHC scores are and why expression data cannot produce them, tumour mutational burden, microsatellite instability, and the expression signatures (IFN-gamma, TIS, TIDE) that are computable from RNA. Written to keep the assay-derived biomarkers and the expression-derived ones apart, because conflating them is the common failure.

## When to Use This Skill

Activate when the user requests:
- PD-L1 status, CPS, TPS, or IC/TC scoring
- TMB-high classification for checkpoint inhibitor eligibility
- MSI-high or dMMR determination
- IFN-gamma, Tumour Inflammation Signature, or TIDE scoring
- Predicting or stratifying response to anti-PD-1, anti-PD-L1, or anti-CTLA-4
- Combining several checkpoint biomarkers into one call

## Inputs

| Data Type | Form | Produces |
|-----------|------|----------|
| Stained slide | PD-L1 IHC, a named antibody clone | CPS, TPS, IC/TC — **only** from here |
| Somatic variants | VCF or MAF plus panel definition | TMB |
| Reads or variants | BAM, or MSI marker loci | MSI status |
| Bulk expression | genes x samples, TPM or normalized counts | IFN-gamma, TIS, TIDE |
| Clinical | response, PFS, OS | evaluation, never input to the score |

---

## The Division That Matters

```
Two families of checkpoint biomarker, and they are not interchangeable.

ASSAY-DERIVED, from a slide or a sequencer
  PD-L1 CPS / TPS      IHC. Requires counting stained cells.
  TMB                  mutations per megabase. Panel-dependent.
  MSI / dMMR           marker instability or MMR protein loss.

EXPRESSION-DERIVED, computable from RNA
  IFN-gamma signature  mean of a small gene set
  TIS / GEP            18-gene inflammation signature
  TIDE                 dysfunction and exclusion modelling

Most confusion in this area comes from treating a member of the first group
as though it belonged to the second.
```

## CPS and TPS Cannot Be Computed From Expression

```
This is the correction worth stating first, because the request arrives
often and sounds reasonable.

  TPS = (PD-L1-stained viable TUMOUR cells / total viable tumour cells) x 100
  CPS = (PD-L1-stained tumour cells + lymphocytes + macrophages
         / total viable tumour cells) x 100

Both are counts of individual stained cells on an IHC slide, and CPS
requires telling a stained tumour cell apart from a stained lymphocyte or
macrophage. That is a morphological judgement at cellular resolution.

Bulk RNA gives you one CD274 value per sample. It has no cells in it, so it
cannot enumerate them and cannot assign them to a compartment. CD274 mRNA
does correlate with PD-L1 IHC, and reasonably well, but a correlation is not
a score: you cannot recover CPS from it, and a "CPS estimated from
expression" is a number with no regulatory or clinical meaning.

What you CAN honestly do with expression:
  - report CD274 (PD-L1) expression as its own continuous variable
  - test its association with outcome
  - state that it is a correlate of, not a substitute for, IHC

If the analysis requires CPS or TPS, it requires a stained slide scored by a
pathologist. Say so rather than approximating.
```

### The antibody clone is part of the biomarker

```
PD-L1 assays are not interchangeable. Different antibody clones, platforms,
scoring systems and cutoffs were each validated with a specific drug and
indication:

  22C3    pharmDx, widely used for pembrolizumab indications (TPS or CPS)
  28-8    pharmDx, nivolumab
  SP142   Ventana, atezolizumab, scores tumour and immune cells separately
  SP263   Ventana, durvalumab among others

SP142 in particular stains a smaller fraction of cells than the others, so a
sample can be "positive" on one assay and negative on another. Always record
which clone, which scoring system, and which cutoff. "PD-L1 positive" with
none of those three is not a reportable result.
```

## TMB and MSI

Both are assay-derived and both are covered in depth by [`variant-annotation`](../variant-annotation/SKILL.md). What matters here is how they behave as checkpoint biomarkers.

```
TMB
  The 10 mut/Mb cutoff comes from a specific assay. Numerator rules
  (synonymous included or not), the denominator (panel capture size), and
  germline filtering all differ by vendor, so a TMB from one panel is not
  comparable to another without harmonization. Report the assay and the
  captured megabases beside the number.

  Panel size drives variance. A 0.8 Mb panel estimating 10 mut/Mb rests on
  roughly 8 observed mutations; the confidence interval is wide and rarely
  shown. Small panels dichotomize noisily around the cutoff.

MSI
  MSI-high and dMMR are tissue-agnostic indications, which makes MSI unusual
  among these biomarkers: the call itself is the eligibility criterion.
  Report the number of unstable loci and the total examined - 20% of 15 loci
  is not 20% of 2,000.

  MSI-high and TMB-high overlap heavily but are not the same set. Mismatch
  repair deficiency raises mutation count, so most MSI-high tumours are
  TMB-high; the converse does not hold, and tumours can be TMB-high through
  smoking or UV exposure with intact MMR.
```

## Expression Signatures

These are the biomarkers you can compute from RNA, and they are the reason to have this skill at all.

### IFN-gamma and the Tumour Inflammation Signature

```
Both are small gene sets summarised per sample. The IFN-gamma signature
captures interferon-driven adaptive immunity; the 18-gene TIS/GEP extends it
with antigen presentation and cytolytic markers. They are correlated, and
reporting both as independent evidence overstates the case.

Summarisation choice changes the answer:
  mean of z-scores    simple, transparent, cohort-dependent
  ssGSEA / GSVA       rank-based within a sample
  singscore           rank-based, explicitly single-sample

Rank-based single-sample scores are the safer default when samples arrive
over time, because a mean-of-z-scores is defined relative to whatever cohort
you happened to have when you computed it. Recomputing after adding samples
changes every earlier score.
```

```r
library(GSVA)   # 2.6.6

# GSVA 2.x takes a PARAMETER OBJECT. The 1.x call is gone.
#   1.x:  gsva(expr, gene_sets, method = "ssgsea")          # no longer works
#   2.x:  gsva(ssgseaParam(expr, gene_sets))
param  <- ssgseaParam(expr_matrix, list(IFNG = ifng_genes, TIS = tis_genes))
scores <- gsva(param)
```

```
GSVA moved to a parameter-object API in 2.x: gsvaParam(), ssgseaParam(),
zscoreParam(), plageParam(). Code written against gsva(expr, gsets,
method=...) fails on 2.x. Pin the version in anything you intend to
reproduce, and check packageVersion("GSVA") before debugging a call that
"used to work".
```

### TIDE

```
TIDE models two escape routes separately - T-cell dysfunction in tumours
with infiltration, and T-cell exclusion in tumours without - and combines
them. That structure is the point: a low score can mean two different
biologies, and the subscores are more informative than the composite.

Access:
  tide.dfci.harvard.edu returns HTTP 403 to programmatic requests, so it is
  a browser tool, not an API.
  tidepy 1.3.9 on PyPI is the programmatic route.

TIDE expects expression normalized relative to a control cohort, typically
by subtracting the per-gene average of the cohort. Feeding raw TPM produces
scores that look plausible and mean nothing. Confirm the normalization the
version you installed expects, rather than assuming.
```

## Combining Biomarkers

```
No single checkpoint biomarker is sufficient, and they disagree by design.

  PD-L1 high, TMB low     inflamed tumour, few neoantigens
  PD-L1 low, TMB high     antigenic but not inflamed
  MSI-high                usually both, and eligible regardless

Reporting them as a panel with each result and its assay is honest.
Collapsing them into a single "immunotherapy score" is not, unless that
composite was itself validated against outcome in an independent cohort -
and almost none have been.

If you build a composite, hold out the cohort you evaluate it on. Fitting
weights on the same patients whose response you then predict is the
leakage pattern from drug-response, wearing different clothes.
```

## Output Specification

| Output | Format | Description |
|--------|--------|-------------|
| `pdl1.csv` | CSV | score, **antibody clone, scoring system, cutoff** — never a bare "positive" |
| `tmb.csv` | CSV | mut/Mb, assay, captured Mb, numerator rule |
| `msi.csv` | CSV | status, unstable loci, loci examined |
| `signatures.csv` | CSV | IFN-gamma, TIS, TIDE with the scoring method named |
| `biomarker_panel.csv` | CSV | all of the above per sample, kept separate |
| `versions.json` | JSON | GSVA, tidepy and gene-set versions |

Keep the assay-derived and expression-derived columns visibly distinct, so no downstream consumer mistakes a signature score for an IHC result.

## Validation Checks

```
PD-L1
  CPS/TPS come from IHC only; no expression-derived approximation reported.
  Antibody clone, scoring system and cutoff recorded with every result.
  CD274 expression, if used, labelled as a correlate rather than a score.

TMB and MSI
  TMB reported with assay and captured megabases; cutoff provenance stated.
  MSI reported as unstable loci over loci examined, not a bare percentage.
  TMB-high and MSI-high not treated as the same set.

Signatures
  Scoring method named (mean-z, ssGSEA, singscore) and version pinned.
  GSVA calls use the 2.x parameter-object API.
  Rank-based single-sample scoring used when samples accrue over time.
  TIDE input normalized as the installed version expects.
  IFN-gamma and TIS not presented as independent evidence.

Composite
  Any combined score validated on a held-out cohort, or not reported as
  predictive.
```

## Common Pitfalls

### PD-L1
1. **Computing CPS or TPS from expression**: they are counts of individual stained cells, and CPS requires distinguishing stained tumour cells from stained immune cells. Bulk RNA has no cells in it. Report CD274 expression as its own variable, or obtain a scored slide.
2. **Reporting "PD-L1 positive" without the clone, scoring system and cutoff**: 22C3, 28-8, SP142 and SP263 are not interchangeable, and SP142 stains a smaller fraction, so the same sample can be positive on one assay and negative on another.
3. **Treating CD274 mRNA as a validated substitute for IHC**: the correlation is real but the score is not recoverable, and no regulatory cutoff is defined on mRNA.

### TMB and MSI
4. **Comparing TMB across assays**: numerator rules, capture size and germline filtering differ by vendor. Harmonize or report separately, with the captured megabases.
5. **Dichotomizing TMB at 10 mut/Mb from a small panel**: a 0.8 Mb panel rests on roughly 8 observed mutations at that cutoff, so the interval is wide. Report the uncertainty rather than a hard call.
6. **Reporting MSI as a bare percentage**: 20% of 15 loci is not 20% of 2,000. Give the numerator and denominator.
7. **Treating MSI-high and TMB-high as the same set**: most MSI-high tumours are TMB-high, but tumours reach TMB-high through smoking or UV with intact MMR.

### Signatures
8. **Using the GSVA 1.x call**: `gsva(expr, gene_sets, method = "ssgsea")` does not exist in 2.x, which dispatches on parameter objects such as `ssgseaParam()`. Check `packageVersion("GSVA")` first.
9. **Scoring with a mean of z-scores when samples accrue over time**: the score is defined relative to the cohort present when it was computed, so adding samples silently changes every earlier value. Use a rank-based single-sample method.
10. **Feeding raw TPM to TIDE**: it expects expression normalized against a control cohort. Raw input yields plausible, meaningless scores.
11. **Expecting a TIDE API**: the web tool returns HTTP 403 to programmatic requests. Use `tidepy` for scripted work.
12. **Reporting IFN-gamma and TIS as independent evidence**: they overlap by construction and are strongly correlated.

### Interpretation
13. **Collapsing biomarkers into one immunotherapy score**: they disagree by design, and almost no composite has been validated against outcome externally. Report the panel with each assay named.
14. **Fitting a composite and evaluating it on the same patients**: the same leakage that inflates drug-response prediction. Hold out a cohort.

## Related Skills

- [`variant-annotation`](../variant-annotation/SKILL.md): TMB and MSI computation, and the assay dependence behind both
- [`immune-deconvolution`](../immune-deconvolution/SKILL.md): the infiltration estimates that contextualise an inflamed-versus-excluded call
- [`cancer-multiomics`](../cancer-multiomics/SKILL.md): the expression matrices the signatures are computed from
- [`survival-analysis`](../survival-analysis/SKILL.md): evaluating a biomarker against outcome
- [`drug-response`](../drug-response/SKILL.md): the held-out-evaluation discipline a composite score needs

## Public Datasets for Testing

| Dataset | Content | Access |
|---------|---------|--------|
| TCGA (any project) | Expression for signature scoring, MAF for TMB | GDC, open |
| MSI-annotated TCGA | MSI status per sample | published supplements |
| Hugo 2016 (melanoma) | Pre-treatment RNA with anti-PD-1 response | GEO |
| Riaz 2017 (melanoma) | Pre- and on-treatment RNA with response | GEO |
| Mariathasan 2018 (bladder) | Expression with atezolizumab response | `IMvigor210CoreBiologies` |
