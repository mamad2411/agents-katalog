---
name: bio-target-prioritization
version: 1.0.0
description: Rank candidate drug targets by genetic evidence, tractability, safety, and novelty into a transparent, weighted, sensitivity-tested shortlist.
author: matrixx0070
tags: [drug-discovery, target-id, tractability, genetics, prioritization, scoring]
capabilities: []
---

## When to use

Use this when the user has a set of candidate genes or proteins for a disease and needs a transparent, weighted ranking to decide which to pursue. Apply before committing screening or chemistry resources.

**Not for:** summarizing the evidence base for one gene (use bio-literature-review), deciding whether a whole program is worth starting (use bio-problem-selection), or designing the validation assay itself (use bio-experiment-design).

## Method

1. Assemble the candidate set and fix the disease context: indication, mechanism hypothesis, patient population.
2. Score each target across weighted dimensions:
   - Genetic/causal evidence — GWAS, Mendelian, Open Targets association, direction of effect.
   - Biological rationale — pathway centrality, tissue expression (GTEx/HPA), model validation.
   - Tractability — small-molecule pockets, antibody accessibility (surface/secreted), existing chemical matter, structures.
   - Safety liabilities — essentiality (DepMap), broad expression, known on-target tox, knockout phenotypes.
   - Novelty & competition — patent/clinical landscape, precedented vs first-in-class.
3. Normalize each dimension to 0–1. Apply explicit, user-tunable weights and show the arithmetic.
4. **Decision:** run a sensitivity check. If the ranking flips under a plausible ±20% weight change, report it as unstable rather than as a firm order.
5. **Decision:** flag any target that ranks only via a single dimension; a lone high genetics score with zero tractability is a research target, not a drug target.
6. Recommend a top tier with go/no-go rationale and the single biggest de-risking experiment per target.

## Example

Five candidates for a fibrosis program. Target A scores genetics 0.9 but tractability 0.1 (intrinsically disordered, no pocket) — flagged single-dimension, demoted to tool-compound track. Target C scores 0.6/0.7/0.8/0.7/0.5; weighted total 0.66 tops the list and survives the sensitivity sweep. The de-risking experiment for C: a knockdown in primary lung fibroblasts measuring collagen deposition.

## Pitfalls

- Hiding the weights so the ranking looks objective when it encodes your priors.
- Scoring novelty as "high" without actually checking the clinical/patent landscape.
- Ignoring DepMap essentiality — a pan-essential gene is a toxicity trap.
- Reporting a single ordered list with no sensitivity note, implying false precision.

## Output format

```
# Target Prioritization — <Indication>
Weights: genetics=_, biology=_, tractability=_, safety=_, novelty=_

## Scoring table
| Target | Genetics | Biology | Tractability | Safety | Novelty | Weighted |

## Ranked shortlist
1. <Target> — <two-line rationale> | de-risking exp: <one line>

## Risk flags & missing data
- <target>: <single-dimension flag / key gap>

Sensitivity: <stable | flips under weight change X>
```
Cite sources; mark low-confidence scores UNVERIFIED.

## Reference

### Weighted scoring rubric

Score every target 0–1 on each dimension, multiply by the weight, sum to a weighted total. Default weights below reflect that human genetic causality is the strongest predictor of clinical success (Nelson 2015 / King 2019: genetically supported targets roughly double the odds of approval). Tune weights to the program and always publish them.

| Dimension | Default weight | 0.0 anchor | 0.5 anchor | 1.0 anchor |
|-----------|:-:|-----------|-----------|-----------|
| Genetic / causal evidence | 0.30 | No association | GWAS hit, no fine-mapping/direction | Coding Mendelian or MR-supported causal allele, direction matches therapeutic hypothesis |
| Tractability | 0.20 | Undruggable (disordered, no pocket, intracellular for a biologic) | Ligandable pocket predicted, no chemical matter | Precedented modality: known pocket + tool cpds, or surface/secreted for antibody |
| Safety / tolerability | 0.20 | Pan-essential (DepMap CERES < −0.5 broadly), severe KO phenotype | Some broad expression, manageable | Restricted expression, benign LoF humans (pLoF carriers healthy) |
| Biological rationale | 0.15 | Peripheral to mechanism | Pathway-adjacent, model-supported | Node is causal driver, disease-tissue expressed, model-validated |
| Novelty / competition | 0.15 | Approved drug already on target | Multiple clinical programs | First-in-class, clear IP space |

**Worked example — fibrosis, 3 candidates (default weights):**

| Target | Gen (0.30) | Tract (0.20) | Safety (0.20) | Bio (0.15) | Novel (0.15) | Weighted |
|--------|:-:|:-:|:-:|:-:|:-:|:-:|
| A | 0.90 | 0.10 | 0.60 | 0.80 | 0.70 | **0.605** |
| B | 0.50 | 0.80 | 0.70 | 0.60 | 0.40 | **0.595** |
| C | 0.60 | 0.70 | 0.80 | 0.70 | 0.50 | **0.660** |

C leads. A is a *single-dimension* case (genetics 0.9, tractability 0.1) → demote to tool-compound / genetic-validation track, not a drug program. A and B are within 0.01 → report the top as a tie pending the sensitivity sweep.

### Key data sources per dimension

- **Genetics/causality:** Open Targets Genetics (L2G score, colocalization), GWAS Catalog, ClinVar/OMIM (Mendelian), gnomAD (pLoF constraint: pLI, LOEUF — LOEUF < 0.35 = constrained/essential-like; pLoF-tolerant genes with healthy homozygous carriers are safer knockdown targets), Mendelian randomization studies.
- **Tractability:** Open Targets tractability buckets (SM / AB / PROTAC / other modalities, buckets 1–10), canSAR, structural coverage (PDB / AlphaFold pLDDT), DrugBank/ChEMBL for existing chemical matter, and DGIdb.
- **Safety/essentiality:** DepMap (Chronos/CERES gene-effect: strongly negative = fitness-essential = tox risk), GTEx/Human Protein Atlas tissue specificity (τ score — high τ = restricted = safer), mouse KO phenotypes (IMPC/MGI), known on-target adverse effects.
- **Novelty/competition:** patents (SureChEMBL/Espacenet), ClinicalTrials.gov, Pharmaprojects/Cortellis, company pipelines.

### Sensitivity & decision rules

Run a ±20% weight perturbation and a leave-one-dimension-out check. If the top rank changes under either, report the ranking as **unstable** and widen the top tier. Treat a target scoring high on only one axis as a research question, not a drug target. Never present a single ordered list without the sensitivity note — it implies false precision the underlying data does not support.
