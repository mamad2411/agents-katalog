# Single-Cell Foundation Models

When to use scGPT, Geneformer, UCE, and the perturbation models, and when a linear baseline beats them. Covers zero-shot embedding extraction, fine-tuning for annotation, in-silico perturbation, and the benchmark evidence behind each recommendation.

## When to Use This Skill

Activate when the user requests:
- scGPT or Geneformer embeddings, fine-tuning, or in-silico perturbation
- Zero-shot cell type annotation with a pretrained transformer
- Cross-species or reference-free cell embedding (UCE, TranscriptFormer)
- Perturbation effect prediction (STATE, Tahoe-x1, GEARS)
- Advice on whether a foundation model is worth it for a given task

## The Short Answer

**Default: do not use one.**

For human cell type annotation, CellTypist with a matching pretrained model, or scANVI/scVI for joint integration and label transfer, gives an answer in minutes on a CPU or small GPU, with a failure mode you can inspect. Three independent 2026 benchmarks put scVI or plain PCA at or above every foundation model on integration and representation.

The evidence base has converged: **single-cell foundation models are representation-strong and prediction-weak.**

```
Where they reliably lose to simple baselines:
  Zero-shot clustering and annotation      vs HVG + PCA, scVI
  Batch integration                        vs scVI, Harmony
  Trajectory inference from embeddings     vs HVG (temporal compression)
  Gene expression reconstruction           vs predicting the mean
  Single-gene perturbation prediction      vs additive / linear models
  GRN inference from attention weights     vs trivial co-expression baselines
```

That is not a reason to never use one. It is a reason to know which situation you are in.

## When to Reach for One

| Situation | Model | Why |
|-----------|-------|-----|
| <500-1000 labeled cells, large unlabeled target | Fine-tuned scGPT whole-human or Geneformer V2-104M | The one setting where the pretraining advantage is documented to *grow* as labels shrink |
| Query cell types absent from any CellTypist/Azimuth reference | scFM embedding + clustering, or UCE zero-shot | Reference-free by construction |
| Non-human or multi-species | TranscriptFormer or UCE | Shared cross-species latent space |
| Spatial and dissociated data jointly | Nicheformer | The only mature spatial foundation model |
| Combinatorial perturbations, cross-context transfer | Arc STATE or Tahoe-x1 | The one place deep models beat linear |
| Cancer / drug response | Tahoe-x1, Geneformer-V2-104M_CLcancer, or scGPT pan-cancer | Domain-matched pretraining |
| Bulk RNA-seq to prognosis | scFoundation embeddings as extra features | Documented C-index gains, low redundancy with expression |

Everything else: use CellTypist, scVI, or HVG+PCA.

---

## Environment

```
scGPT        install from git main, NOT PyPI
Geneformer   install from HuggingFace, NOT PyPI (not published there)
UCE          git clone, single script
Helical 3.1.1  one API over most of the above (AGPL-3.0 - check your policy)
```

```
scGPT PyPI 0.2.4 (2025-03-31) pins scvi-tools<1.0, datasets<3.0.0, orbax<0.1.8
and still depends on torchtext, whose development stopped at 0.18.0.
Those pins are irreconcilable with a current stack and cause most of the
"cannot install scGPT" reports.

git main (0.2.5, unreleased) drops torchtext for a pure-Python Vocab, adds
CUDA 12.8 and flash-attn >= 2.8.0 support, and moves to PEP 621 packaging.

  pip install git+https://github.com/bowang-lab/scGPT.git
```

```bash
# Geneformer
git lfs install
git clone https://huggingface.co/ctheodoris/Geneformer
cd Geneformer && pip install .
```

The Geneformer package version string is permanently `0.1.0`. **Version the checkpoint and the git commit, not the package.**

---

## scGPT

### Checkpoints

| Checkpoint | Pretraining |
|------------|-------------|
| whole-human (default) | 33M normal human cells |
| scGPT_CP (continual pretrained) | derived from whole-human; best scGPT variant for zero-shot embeddings |
| pan-cancer | 5.7M |
| blood (blood + bone marrow) | 10.3M |
| brain / lung / heart / kidney | 13.2M / 2.1M / 1.8M / 814K |

Counter-intuitive but measured: **scGPT-human (33M cells) underperforms scGPT-blood (10.3M cells)** on several benchmarks, including tissues outside blood and bone marrow. Bigger pretraining is not better here.

### Zero-shot embeddings

```python
import scgpt as scg

adata = scg.tasks.embed_data(
    adata,
    model_dir,                  # contains vocab.json, args.json, best_model.pt
    gene_col="feature_name",    # column in adata.var holding gene SYMBOLS
    max_length=1200,
    batch_size=64,
    device="cuda",
    return_new_adata=False,     # writes adata.obsm["X_scGPT"]
)
```

```
Input contract, read from the source rather than the tutorial:

  Binning is applied INSIDE the collator (do_binning=True is hard-coded on
  this path). Do not pre-bin.

  Genes not in the vocab are silently dropped. The log reports the match rate.
  CHECK IT. Symbol-vs-Ensembl mismatch is the single most common silent failure.

  The cell embedding is the <cls> token, not a mean-pool.

  With max_length=1200 and sampling=True, cells with more than 1199 detected
  genes have their gene set RANDOMLY SUBSAMPLED. Zero-shot embeddings are
  therefore mildly stochastic. Fix the seed.

  Whether .X should hold raw counts or normalized values is genuinely
  ambiguous in the codebase, and is a documented source of irreproducibility
  across benchmark papers. Record what you fed it.
```

### Fine-tuning for annotation

```python
hyperparameter_defaults = dict(
    seed=0, epochs=10, n_bins=51, lr=1e-4, batch_size=32,
    layer_size=128, nlayers=4, nhead=4, dropout=0.2,
    amp=True, freeze=False,     # freeze=True gives linear-probe behaviour
    DSBN=False,                 # domain-specific batch norm for batch correction
)
# max_seq_len = 3001 for fine-tuning, larger than the 1200 used at inference
```

Fine-tuning is seed- and hyperparameter-sensitive. Run several seeds and report the variance.

---

## Geneformer

### Checkpoints

| Checkpoint | Corpus | Params | Input size | Vocab |
|------------|--------|--------|-----------|-------|
| V1-10M | ~30M human cells | 10M | 2048 | 25,426 |
| V2-104M | ~104M non-cancer human | 104M | 4096 | 20,275 |
| V2-316M | ~104M | 316M | 4096 | 20,275 |
| V2-104M_CLcancer | V2 + ~14M cancer cells | 104M | 4096 | 20,275 |

```
The repo root now holds Geneformer-V2-316M.

  from_pretrained("ctheodoris/Geneformer")

silently loads the 316M model, NOT the 10M model from the 2023 Nature paper.
Most published criticism evaluated V1. Name the checkpoint explicitly.

V1 and V2 token IDs are NOT interchangeable (25,426 all-gene vocab vs 20,275
protein-coding). Dictionaries must match the checkpoint, which is why the API
objects carry model_version.
```

### Tokenization is the whole game

```python
from geneformer import TranscriptomeTokenizer

tk = TranscriptomeTokenizer(
    model_input_size=4096, special_token=True, model_version="V2",  # V1: 2048, False
)
```

```
Rank-value encoding:
  raw counts
    -> divide by cell total, x 10,000
    -> divide by the MEDIAN NON-ZERO expression of that gene ACROSS THE
       PRETRAINING CORPUS
    -> rank genes descending, truncate to model_input_size
  Zeros are dropped, not ranked.

Consequences you cannot ignore:
  RAW COUNTS ARE MANDATORY. No log1p. No HVG selection. No per-dataset
  normalization. Feeding log-normalized data produces valid-looking but
  wrong rankings, silently.

  Requires ensembl_id in .var and n_counts in .obs.

  The corpus-median divisor is what deprioritizes housekeeping genes. It also
  makes tokenization corpus-dependent, which is why V1/V2 dictionaries and
  checkpoints must be paired.
```

### In-silico perturbation

```python
from geneformer import InSilicoPerturber

isp = InSilicoPerturber(
    perturb_type="delete",        # only "delete" and "overexpress" are implemented
    genes_to_perturb="all",
    model_type="Pretrained",      # "Pretrained-Quantized" runs V2-316M on a consumer GPU
    emb_mode="cls",
    cell_states_to_model={"state_key": ..., "start_state": ..., "goal_state": ...},
    forward_batch_size=100, nproc=4, model_version="V2",
)
```

```
"inhibit" and "activate" appear in the docstring marked (TBA). They are NOT
implemented. Only delete and overexpress work today.

emb_layer accepts ONLY {-1, 0}, and the convention is INVERTED:
  0  = last layer
  -1 = second-to-last layer
You cannot sweep arbitrary depths through this API.

Mechanism: delete removes the token from the rank sequence; overexpress moves
the gene to the front of it. Effect = cosine shift of the cell embedding
toward the goal state.
```

Treat in-silico perturbation output as a **hypothesis ranker, not evidence**. Two independent 2026 papers found attention-derived edges capture co-expression rather than regulatory signal, with trivial gene-level baselines outperforming them (AUROC 0.81-0.88 vs 0.70), and causal ablation of "regulatory heads" producing no degradation.

---

## The Rest of the Field

| Model | Status | Use it? |
|-------|--------|---------|
| UCE | *Nature* 2026; code unchanged since Nov 2024 | Yes, easiest zero-shot. `.X` = counts, `.var_names` = gene **names**, not Ensembl. 4-layer and 33-layer embeddings are **not comparable** |
| TranscriptFormer | CZI, v0.6.1, active | Best cross-species option. Wins RNA to protein in VCBench |
| Nicheformer | *Nature Methods* 2025 | The only mature spatial foundation model. Strongest under linear probing, not zero-shot |
| Tahoe-x1 | Tx1-70M / 1.3B / 3B, Apache-2.0 | Cancer-focused, perturbation-pretrained, permissive license. Most relevant new entrant for oncology |
| Arc STATE | `arc-state` on PyPI, active | Perturbation prediction. **Non-commercial license** blocks industry use |
| C2S-Scale | Gemma-2 backbone, CC-BY-4.0 | Natural-language interface over cells. Start with the 2B, not the 27B |
| scFoundation | *Nat Methods* 2024 | High friction, thin docs. Still the choice for the bulk-to-prognosis recipe |
| scGenePT | dormant since Jan 2025 | Low priority; its task is the one where linear baselines win |
| Helical 3.1.1 | active, fast releases | One API over most of the above. **AGPL-3.0** and Python >=3.12,<3.13 |

---

## What the Evidence Says

Cite these when someone asks why you used PCA.

```
Kedzierska et al., Genome Biology 2025;26:101
  "HVG outperforms Geneformer and scGPT across all metrics" for cell-type
  separation. Geneformer ranked last consistently. scGPT beat scVI/Harmony
  on exactly one dataset. Caveat the authors raise themselves: the datasets
  where scGPT improved were in its pretraining set.

Boiarsky et al., Nature Machine Intelligence 2024;6:1443
  More nuanced than it is usually quoted. L1 logistic regression matches or
  beats scBERT. BUT scGPT beat logistic regression on the MS dataset at every
  training-set size, with the advantage GROWING as labels shrank. On pancreas
  the direction reversed. Anyone quoting "logistic regression beats foundation
  models" as a flat statement is misreading this paper.

Ahlmann-Eltze, Huber & Anders, Nature Methods 2025;22:1657
  Five foundation models plus two deep models vs deliberately simple baselines
  for perturbation prediction: "None outperformed the baselines."

DenAdel et al., Nature Methods 2026;23:1447
  400 models pretrained, 6,400 experiments. Performance plateaus with corpora
  "only a fraction of the size of current training corpora", and
  "unlike large language models, single-cell foundation models show no clear
  data scaling laws."

Han et al., bioRxiv 2026 (J&J), >1.5M clinical/preclinical cells
  Fine-tuned scGPT_CP was the best foundation model. scVI was the best
  performer overall.

Liu T. et al., bioRxiv 2026: 20 methods, 1,607 datasets, ~21.8M cells
  No single method wins across tasks. High utility does not imply robustness.
  "Greater computational cost did not consistently correspond to better
   performance."
```

Where they genuinely win, supported rather than marketed: fine-tuned annotation in label-scarce settings; representation tasks when fine-tuned; combinatorial perturbations and cross-context transfer; cross-modal prediction; bulk RNA-seq features for clinical modeling (mean C-index 0.724 across 25 TCGA cancers, >0.8 in seven); and in-silico perturbation as hypothesis generation followed by experiments.

---

## Non-Negotiable Protocol

```
1. Run HVG+PCA and scVI as baselines IN THE SAME SCRIPT.
   Every benchmark above exists because people did not.

2. Check pretraining contamination.
   If your dataset is in CELLxGENE, it is probably in the pretraining corpus.
   No foundation model publishes a cell-level training manifest, so you
   cannot verify this. Report it as a limitation.

3. Sweep the embedding-extraction layer where the API allows it.
   Optimal layer is task-dependent; trajectory performance peaks around 60%
   model depth. Geneformer does NOT allow a free sweep.

4. For perturbation, report DE-based and discrimination metrics.
   Never all-genes Pearson alone: a model that predicts NO CHANGE maximizes it.

5. Fix seeds and report variance. Fine-tuning is seed-sensitive.
```

## Compute Cost

For a 100k-cell dataset. Baselines included so the comparison is visible.

| Approach | GPU floor | Wall clock |
|----------|-----------|-----------|
| HVG + PCA | none (CPU) | 1-2 min |
| scVI | 8 GB | 10-20 min incl. training |
| scGPT whole-human | 16 GB | 15-40 min |
| Geneformer V2-104M | 16 GB | 30-60 min |
| Geneformer V2-316M | 24 GB | 1.5-3 h |
| UCE 33-layer | 80 GB (batch 25) | several hours |
| Tahoe-x1 Tx1-3B | 40 GB | 2-4 h |

Wall-clock figures beyond the baselines are planning estimates, not measured guarantees. CellTypist annotates 100k cells in seconds on a laptop CPU.

## Common Pitfalls

1. **Installing scGPT from PyPI**: 0.2.4 pins `scvi-tools<1.0` and needs `torchtext`, which is discontinued. Install from git main.
2. **`from_pretrained("ctheodoris/Geneformer")`**: silently loads V2-316M, not the 10M model the original paper describes. Name the checkpoint.
3. **Log-normalizing before Geneformer**: it needs raw counts. Rank-value encoding divides by a corpus median, so normalized input produces plausible but wrong rankings with no error.
4. **Mixing V1 and V2 Geneformer dictionaries**: token IDs differ (25,426 vs 20,275 vs). Pair `model_version`, `model_input_size`, `special_token`, and the checkpoint.
5. **Not checking scGPT's gene-vocabulary match rate**: unmatched genes are dropped silently. A symbol-vs-Ensembl mismatch can drop most of your panel.
6. **Treating zero-shot embeddings as batch-corrected**: batch signal persists in pretrained embeddings; post-hoc centering only partly fixes it. Foundation models do not give free batch correction.
7. **Running trajectory inference on zero-shot embeddings**: architectures over-compress temporal signal and artificially linearize branched structures, hiding divergence points. Use HVG-based embeddings.
8. **Comparing UCE 4-layer and 33-layer embeddings**: they are different spaces.
9. **Reporting all-genes Pearson for perturbation**: a no-change predictor maximizes it. It barely separates good models from useless ones.
10. **Benchmarking on a dataset that is in the pretraining corpus**: the most common way published foundation-model wins evaporate on re-evaluation.
11. **Reading in-silico perturbation output as regulatory evidence**: attention captures co-expression. Treat it as a ranked hypothesis list to test experimentally.
12. **Assuming a bigger checkpoint is better**: there are no clear data scaling laws here, and scGPT-human underperforms scGPT-blood on several tasks.

## Related Skills

- `single-cell-atlas`: the baseline pipeline these models must beat
- `spatial-transcriptomics`: Nicheformer covers the spatial case
- `cancer-multiomics`: bulk expression input for the prognosis recipe

## Public Datasets for Testing

| Dataset | Use |
|---------|-----|
| PBMC 3k | Fast smoke test for embedding extraction |
| Pancreas (scIB) | Standard integration benchmark, 9 technologies |
| Immune atlas (scIB) | Cross-tissue integration |
| Tabula Sapiens | Note: in the scGPT pretraining corpus |
| Norman / Replogle Perturb-seq | Perturbation prediction benchmarks |
