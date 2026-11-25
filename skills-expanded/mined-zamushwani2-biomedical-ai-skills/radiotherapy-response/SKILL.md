# Radiotherapy Response

Genomic predictors of radiation response: DNA damage repair pathway profiling, the Radiosensitivity Index and the Genomic-Adjusted Radiation Dose built on it, post-irradiation immune activation signatures, and an honest account of what the abscopal effect can and cannot be predicted from.

## When to Use This Skill

Activate when the user requests:
- Radiosensitivity Index (RSI) or Genomic-Adjusted Radiation Dose (GARD)
- DNA damage repair gene or pathway profiling
- Predicting response to radiotherapy from expression data
- Immune activation signatures after irradiation
- Abscopal effect biomarkers
- Combining radiotherapy dose with a genomic covariate

## Inputs

| Data Type | Form | Note |
|-----------|------|------|
| Expression | genes x samples | RSI needs **ranks**, not raw values |
| Dose / fractionation | total dose, dose per fraction | required for GARD, not RSI |
| Somatic variants | VCF or MAF | DDR gene alterations |
| Clinical | local control, PFS, OS, site irradiated | evaluation only |

---

## Environment

Versions verified 2026-08.

```r
BiocManager::install("RadioGx")    # 2.16.0  radiation pharmacogenomics
install.packages("msigdbr")        # 26.1.1  gene set collections
```

```
NO PACKAGE IMPLEMENTS RSI OR GARD.

Checked CRAN, Bioconductor and PyPI: there is no maintained implementation.
You write the model yourself from the publication, which means the gene list,
the coefficients and the rank transform are your responsibility to get right.
That is the main risk in this skill, so the exact model is written out below.

RadioGx (2.16.0) is the sibling of PharmacoGx for radiation response and
holds curated radiogenomic datasets. It is where to get training or
validation data, not an RSI implementation.
```

```
msigdbr changed its version scheme. The history runs 10.0.2 -> 24.1.0 ->
25.1.x -> 26.1.1: it is now CALENDAR versioned against the MSigDB release
year, not semantic. A dependency pinned as ">= 7.5.1" or logic that compares
major versions numerically will behave oddly. Pin an exact version and
record which MSigDB release it carries.
```

## The Radiosensitivity Index

RSI is a 10-gene linear model trained in 48 cancer cell lines to predict survival fraction at 2 Gy (SF2).

```
Genes:  AR, JUN, STAT1, PRRT2, RELA, ABL1, SUMO1, CDK1, HDAC9, IRF1

RSI = -0.0098009 * AR
      +0.0128283 * JUN
      +0.0254552 * STAT1
      -0.0017589 * PRRT2
      -0.0038171 * RELA
      +0.1070213 * ABL1
      -0.0002509 * SUMO1
      -0.0092431 * CDK1
      -0.0204469 * HDAC9
      -0.0441683 * IRF1
```

### Two things that invert the answer

```
1. THE INPUTS ARE RANKS, NOT EXPRESSION VALUES.

Each gene's expression is converted to its rank within the sample before the
coefficients are applied. The rank transform is what makes the score portable
across platforms, which was the point of building it that way. Feeding
log-TPM or z-scores into those coefficients produces a number on a different
scale that is not RSI.

2. HIGHER RSI MEANS MORE RADIO-RESISTANT.

The name says "radiosensitivity index" and the direction is the opposite of
what the name suggests. RSI predicts SF2, the surviving fraction at 2 Gy, so
a high value means more cells survive: resistant. Low RSI is the radio-
sensitive tumour.

This is the same class of error as reading AAC for AUC. Write the direction
into the column name (rsi_higher_is_resistant) rather than trusting a
reader to remember it.
```

```r
rank_within_sample <- function(expr, genes) {
  # ranks across ALL genes in the sample, then subset - not ranks among the 10
  apply(expr, 2, function(col) rank(col, ties.method = "average"))[genes, , drop = FALSE]
}
```

```
Rank across the whole transcriptome, then take the 10 genes. Ranking only
within the 10 gives each sample the values 1..10 and destroys the signal.
This is the single easiest way to implement RSI incorrectly and still get
plausible-looking output.
```

## GARD

```
GARD combines RSI with the linear-quadratic model to give a dose-adjusted,
patient-specific estimate of radiation effect. RSI alone says how sensitive
the tumour is; GARD says how much biological effect the delivered dose
achieves in that tumour.

  RSI   genomic, dose-independent
  GARD  genomic AND dose-dependent: needs total dose and dose per fraction

Reporting GARD without stating the dose and fractionation it was computed
for is meaningless, because the same tumour has a different GARD under
60 Gy in 30 fractions than under 50 Gy in 5.

The alpha/beta ratio is an assumption, not a measurement. It is usually
taken as 10 for tumours and 3 for late-responding normal tissue. State the
value you used; the comparison between arms can move with it.
```

### State the controversy

```
GARD-guided dose adjustment is an active research question, not settled
practice. A pan-cancer analysis has argued directly that RSI is not fit to
be used for dose adjustment, and that critique is in the literature
alongside the validation studies.

Present RSI and GARD as research biomarkers with contested evidence. Do not
generate a dose recommendation from them. If the user's goal is clinical
dose adjustment, say plainly that this is investigational and belongs in a
trial.
```

## DNA Damage Repair Profiling

```
DDR is not one pathway. Grouping all "DNA repair genes" together and calling
the result a DDR score mixes pathways whose deficiencies have opposite
therapeutic implications:

  HR        homologous recombination (BRCA1/2, RAD51, PALB2)
  NHEJ      non-homologous end joining (PRKDC, XRCC4, LIG4)
  MMR       mismatch repair (MLH1, MSH2, MSH6, PMS2)
  BER       base excision repair (PARP1, OGG1, APEX1)
  NER       nucleotide excision repair (ERCC1-5, XPA, XPC)
  FA        Fanconi anaemia crosslink repair

HR deficiency sensitizes to radiation and to PARP inhibition. MMR deficiency
drives MSI and checkpoint response but does not confer the same
radiosensitivity. Score the pathways separately and say which you mean.
```

```r
library(msigdbr)   # 26.1.1
hallmark_ddr <- msigdbr(species = "Homo sapiens",
                        collection = "H")           # then filter to DNA repair
```

```
The `category`/`subcategory` arguments were renamed to `collection` and
`subcollection` in the newer msigdbr. Old code using category = "H" errors
or warns depending on version. Check the signature against the version you
installed rather than copying a tutorial.

For a curated DDR gene list, the TCGA pan-cancer DDR resource is the usual
reference and is larger and better organised by pathway than the Hallmark
DNA repair set, which is a single 150-gene block with no pathway structure.
```

## Post-Irradiation Immune Signatures

```
Radiation is immunomodulatory: it releases antigen, induces type I
interferon through the cGAS-STING axis, and can increase MHC-I. Expression
signatures capturing that are the same family used for checkpoint response,
so read the checkpoint-biomarkers skill for how to score them.

The measurement problem specific to radiotherapy is TIMING. The immune
signal after irradiation is transient and its direction depends on when you
biopsy: early lymphocyte depletion within the field, later infiltration.
A pre- versus post-treatment comparison without a stated interval is not
interpretable, and intervals differ across published studies.

Also: irradiated tissue is not the same tissue. A post-radiation biopsy of
the treated site contains fibrosis, necrosis and treatment effect, so an
expression change may be composition rather than regulation. Deconvolve or
say you did not.
```

## The Abscopal Effect

```
Be honest about the state of the evidence here.

The abscopal effect - regression of a non-irradiated lesion after local
radiotherapy - is real but RARE, and most of the literature is case reports
and small series, often with concurrent immunotherapy. There is no validated
biomarker panel that predicts it, and a skill that offers one would be
inventing it.

What can be done defensibly:
  - measure the mechanistic correlates (type I interferon signalling,
    cGAS-STING, antigen presentation, T-cell infiltration at the distant
    site) and describe them as mechanistic, not predictive
  - require a distant, NON-irradiated lesion with its own measurement,
    because an abscopal claim rests entirely on that lesion
  - report the interval and concurrent systemic therapy, since most reported
    cases involve checkpoint blockade

What should not be done:
  - presenting a signature score as an abscopal predictor
  - inferring abscopal response from a single-lesion response
```

## Output Specification

| Output | Format | Description |
|--------|--------|-------------|
| `rsi.csv` | CSV | score with the direction in the column name, and the rank basis stated |
| `gard.csv` | CSV | GARD **with total dose, dose per fraction and alpha/beta** |
| `ddr_scores.csv` | CSV | one column per DDR pathway, never a single merged score |
| `immune_signatures.csv` | CSV | signature scores with the biopsy interval |
| `versions.json` | JSON | msigdbr version and the MSigDB release it carries |

## Validation Checks

```
RSI
  Ranks computed across the whole transcriptome, then the 10 genes taken.
  All ten genes present; missing genes reported rather than dropped silently.
  Direction stated: higher RSI = more resistant.
  Not presented as clinically actionable.

GARD
  Total dose, dose per fraction and alpha/beta recorded with every value.
  Assumption values stated, not left implicit.
  No dose recommendation generated.

DDR
  Pathways scored separately; no single merged DDR score.
  Gene set source and version recorded.
  msigdbr called with collection/subcollection matching the installed version.

Immune and abscopal
  Biopsy interval stated for any pre/post comparison.
  Composition change considered before calling a change regulatory.
  Abscopal correlates labelled mechanistic, not predictive.
  Distant non-irradiated lesion measured separately for any abscopal claim.
```

## Common Pitfalls

### RSI
1. **Feeding expression values instead of ranks**: the coefficients were fitted on within-sample ranks, which is what makes the score platform-portable. Log-TPM in produces a number that is not RSI.
2. **Ranking within the 10 genes instead of the transcriptome**: every sample then gets the values 1 to 10 and the signal is gone, while the output still looks reasonable.
3. **Reading high RSI as radiosensitive**: it predicts SF2, so high means more cells survive, meaning resistant. The name misleads. Put the direction in the column name.
4. **Dropping a missing gene silently**: the model has ten terms and no defined behaviour with nine. Report absences rather than computing a partial score.

### GARD
5. **Reporting GARD without dose and fractionation**: it is dose-dependent by construction, so the same tumour has different GARD under different schedules.
6. **Leaving alpha/beta implicit**: it is an assumption, conventionally 10 for tumour and 3 for late-responding normal tissue, and comparisons can move with it.
7. **Generating a dose recommendation**: dose adjustment from RSI/GARD is investigational and directly contested in the literature. Report the score, not a prescription.

### DDR
8. **Collapsing all DDR genes into one score**: HR, NHEJ, MMR, BER, NER and FA deficiencies have different and sometimes opposite implications. Score them separately.
9. **Treating MMR deficiency as radiosensitizing**: it drives MSI and checkpoint response; HR deficiency is the one tied to radiation and PARP sensitivity.
10. **Using `category =` with a newer msigdbr**: the argument is now `collection`/`subcollection`. Check the installed signature.
11. **Assuming msigdbr uses semantic versions**: it moved to calendar versioning (10.0.2 → 24.1.0 → 26.1.1). Pin exactly and record the MSigDB release.

### Immune and abscopal
12. **Comparing pre- and post-irradiation expression without stating the interval**: the immune response is transient and its direction depends on timing.
13. **Reading a post-radiation expression change as regulation**: the irradiated field contains fibrosis, necrosis and treatment effect, so composition may have changed instead.
14. **Presenting any signature as an abscopal predictor**: no validated panel exists. Report mechanistic correlates as mechanistic.
15. **Claiming an abscopal response without measuring a distant non-irradiated lesion**: that lesion is the entire basis of the claim.

## Related Skills

- [`checkpoint-biomarkers`](../checkpoint-biomarkers/SKILL.md): scoring the immune signatures radiation modulates, and the same signature-scoring traps
- [`variant-annotation`](../variant-annotation/SKILL.md): calling the DDR gene alterations profiled here
- [`survival-analysis`](../survival-analysis/SKILL.md): evaluating RSI or GARD against local control and survival
- [`cancer-multiomics`](../cancer-multiomics/SKILL.md): the expression matrices these scores are computed from
- [`immune-deconvolution`](../immune-deconvolution/SKILL.md): separating composition change from regulation in irradiated tissue

## Public Datasets for Testing

| Dataset | Content | Access |
|---------|---------|--------|
| RadioGx datasets | Curated radiogenomic cell-line data with survival fractions | Bioconductor |
| TCGA (any project) | Expression plus radiotherapy fields in clinical data | GDC, open |
| MSigDB Hallmark | DNA repair gene set (one block, no pathway structure) | `msigdbr` |
| TCGA pan-cancer DDR resource | DDR genes organised by pathway | published supplement |
