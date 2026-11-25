---
name: ai-science-zero-shot-mutation
description: Score protein point mutations zero-shot with ESM-1v/ESM-2 masked-LM log-odds, ensembled, benchmarked on ProteinGym DMS. Use when predicting mutation effects, ranking missense variants, scoring VUS fitness with no labels.
tool_type: python
primary_tool: esm
---

# Zero-Shot Mutation Effect Prediction

## When to Use

- Ranking candidate point mutations (protein engineering, saturation mutagenesis) with no experimental fitness data.
- Prioritizing missense variants of uncertain significance (VUS) from ClinVar/gnomAD by predicted deleteriousness.
- Comparing predicted effects against deep mutational scanning (DMS) assays, e.g. validating on ProteinGym.
- Building a stability/fitness proxy to feed into variant triage alongside allele frequency and structural confidence.

## Version Compatibility

- `fair-esm` ≥ 2.0.0 (ESM-1v, ESM-2), PyTorch ≥ 2.0, Python ≥ 3.10.
- GPU strongly recommended for ESM-1v/ESM-2 (650M+ params); CPU inference is slow but works for short sequences.
- ProteinGym benchmark CSVs (no fixed version — download current release from proteingym.org).

## Prerequisites

- `pip install fair-esm torch pandas numpy`
- Familiarity with masked language models (BERT-style masking) and Spearman correlation.
- A wild-type protein sequence (FASTA) and a list of positions/substitutions to score.

## Key Distinctions

- **Masked vs autoregressive**: ESM-1v/ESM-2 use MLM — mask position i, compare log-probs at that position. Autoregressive models (ProtGPT2) instead compare full-sequence log-likelihoods.
- **Single-site vs epistatic**: ESM-1v computes single-site marginals independently, ignoring mutation-mutation interactions. For epistatic/multi-mutant effects use ESM-IF1 (inverse folding) or a DMS-fine-tuned model.
- **ΔlogP vs ΔΔG**: ESM scores track evolutionary fitness (how tolerated a substitution is across homologs), not thermodynamic stability directly — correlated but not identical.
- **Benchmark first**: always check Spearman ρ against ProteinGym DMS assays for a protein family similar to your target before trusting raw scores.

**Goal:** compute, for each candidate substitution, the zero-shot log-odds score
`Δ = logP(mutant | masked context) - logP(wildtype | masked context)` under a masked protein language model. Negative Δ signals the mutant is less likely under the model's evolutionary prior (candidate deleterious).

**Approach:** mask each queried position once, run one forward pass, read off log-probabilities for wildtype and every mutant amino acid at that position, then average across the 5 ESM-1v ensemble checkpoints for robustness.

```python
import esm
import torch
import torch.nn.functional as F

AA = list('ACDEFGHIKLMNPQRSTVWY')

model, alphabet = esm.pretrained.esm1v_t33_650M_UR90S_1()  # one of 5 ensemble members (UR90S_1..5)
batch_converter = alphabet.get_batch_converter()
model.eval()


def score_mutations(sequence: str, positions: list[int]) -> dict[str, float]:
    """Compute ESM-1v zero-shot log-odds for all single-AA substitutions at given positions.

    sequence: wild-type protein sequence (no gaps)
    positions: 1-indexed residue positions to score
    returns: dict mapping "{wt}{pos}{mut}" -> delta log-prob (mutant vs wildtype)
    """
    _, _, tokens = batch_converter([("seq", sequence)])
    # tokens layout: [<cls>, res_1, res_2, ..., res_L, <eos>] -> token index i holds
    # residue at 1-indexed sequence position i, so `pos` indexes directly into tokens.

    scores = {}
    with torch.no_grad():
        for pos in positions:
            masked_tokens = tokens.clone()
            masked_tokens[0, pos] = alphabet.mask_idx

            logits = model(masked_tokens, repr_layers=[])["logits"]  # (1, L+2, vocab)
            log_probs = F.log_softmax(logits[0, pos], dim=-1)

            wt_aa = sequence[pos - 1]
            wt_idx = alphabet.get_idx(wt_aa)

            for mut_aa in AA:
                if mut_aa == wt_aa:
                    continue
                mut_idx = alphabet.get_idx(mut_aa)
                delta = (log_probs[mut_idx] - log_probs[wt_idx]).item()
                scores[f"{wt_aa}{pos}{mut_aa}"] = delta
    return scores
```

**Goal:** improve correlation with experimental fitness by averaging the 5 independently-trained ESM-1v checkpoints (published to reduce single-model variance on ProteinGym).

**Approach:** score the same mutations with each checkpoint and average the deltas.

```python
import numpy as np

CHECKPOINTS = [
    esm.pretrained.esm1v_t33_650M_UR90S_1,
    esm.pretrained.esm1v_t33_650M_UR90S_2,
    esm.pretrained.esm1v_t33_650M_UR90S_3,
    esm.pretrained.esm1v_t33_650M_UR90S_4,
    esm.pretrained.esm1v_t33_650M_UR90S_5,
]


def ensemble_score(sequence: str, positions: list[int]) -> dict[str, float]:
    """Average zero-shot log-odds across all 5 ESM-1v ensemble members."""
    per_model = []
    for load_fn in CHECKPOINTS:
        m, alpha = load_fn()
        m.eval()
        bc = alpha.get_batch_converter()
        _, _, tokens = bc([("seq", sequence)])
        model_scores = {}
        with torch.no_grad():
            for pos in positions:
                masked = tokens.clone()
                masked[0, pos] = alpha.mask_idx
                logits = m(masked, repr_layers=[])["logits"]
                log_probs = F.log_softmax(logits[0, pos], dim=-1)
                wt_aa = sequence[pos - 1]
                wt_idx = alpha.get_idx(wt_aa)
                for mut_aa in AA:
                    if mut_aa == wt_aa:
                        continue
                    delta = (log_probs[alpha.get_idx(mut_aa)] - log_probs[wt_idx]).item()
                    model_scores[f"{wt_aa}{pos}{mut_aa}"] = delta
        per_model.append(model_scores)

    keys = per_model[0].keys()
    return {k: float(np.mean([d[k] for d in per_model])) for k in keys}
```

**Goal:** validate zero-shot scores against a fitness proxy (or real ProteinGym DMS data) before using them for triage, and produce a rarity/stability-aware priority ranking — this pattern works identically with real ESM scores or the toy proxy below (no GPU needed for smoke-testing the pipeline).

```python
import numpy as np
import pandas as pd

np.random.seed(13)
AA = list('ACDEFGHIKLMNPQRSTVWY')
HYDRO, POLAR, CHARGED = set('AILMFWVY'), set('STNQ'), set('KRHDE')


def aa_group(a: str) -> str:
    """Classify an amino acid into a coarse physicochemical group."""
    if a in HYDRO:
        return 'hydro'
    if a in POLAR:
        return 'polar'
    if a in CHARGED:
        return 'charged'
    return 'other'


def toy_zero_shot_delta(wt: str, mut: str) -> float:
    """CPU-only stand-in for a real ESM delta: penalize physicochemical group switches."""
    return 0.25 if aa_group(wt) == aa_group(mut) else -0.55


wt_seq = 'MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQ'
records = []
for i, wt in enumerate(wt_seq):
    for mut in AA:
        if mut == wt:
            continue
        records.append({'pos': i + 1, 'wt': wt, 'mut': mut, 'delta_ll': toy_zero_shot_delta(wt, mut)})

df = pd.DataFrame(records)

noise = np.random.normal(0, 0.08, size=len(df))  # benchmark: correlate delta vs pseudo-fitness (Spearman rho, as on ProteinGym)
df['fitness'] = 0.6 + 0.5 * df['delta_ll'] + noise
corr = df[['delta_ll', 'fitness']].corr(method='spearman').iloc[0, 1]
print('Spearman correlation (delta vs fitness):', round(float(corr), 3))

subset = df.sample(12, random_state=1).copy()  # triage: combine effect score with rarity + structural confidence
subset['rarity'] = np.random.uniform(0.2, 1.0, size=len(subset))
subset['plddt_proxy'] = np.random.uniform(55, 95, size=len(subset))
subset['priority'] = (
    0.5 * (-subset['delta_ll']) +
    0.3 * subset['rarity'] +
    0.2 * (subset['plddt_proxy'] / 100.0)
)
print(subset.sort_values('priority', ascending=False)[
    ['pos', 'wt', 'mut', 'delta_ll', 'rarity', 'plddt_proxy', 'priority']
])
```

## Pitfalls

- **Confusing evolutionary fitness with stability**: a mutation can score well on ESM (evolutionarily tolerated) yet destabilize the fold (high ΔΔG), or vice versa — don't substitute one for the other without checking.
- **No benchmark, no trust**: run the toy/real pipeline against ProteinGym DMS assays for a related protein family first; Spearman ρ varies widely (0.2–0.7+) by protein family and model.
- **Position indexing off-by-one**: ESM batch-converter output has `<cls>` at index 0, so a 1-indexed residue position maps directly to that token index — do not add or subtract an extra offset.
- **Single checkpoint variance**: a single ESM-1v member is noisier than the 5-model ensemble; prefer ensembling when ranking close-call mutations.
- **Epistasis blindness**: single-site marginals assume mutations are independent — for double/triple mutants or designed variants, epistatic effects can dominate and require ESM-IF1 or structure-based scoring instead.

## See Also

- `esm` — embeddings, contact prediction, and general ESM-2 usage.
- `bio-clinical-databases-variant-prioritization` — combining zero-shot scores with population frequency and clinical annotations.
- `bio-structural-biology-alphafold-predictions` — structural confidence (pLDDT) proxies used in triage.
- `bio-machine-learning-biomarker-discovery` — downstream use of variant-effect scores as model features.
