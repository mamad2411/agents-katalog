---
name: generative-design
description: Use when designing or evaluating generative models for de novo drug/molecule design. Covers molecular generation theory and evaluation (MOSES/GuacaMol), SELFIES + language models, RL-based optimization with REINVENT 4, JT-VAE and graph-based generation, and structure-based 3D generation (DiffSBDD, Pocket2Mol, DiffLinker).
---

# Generative Molecular Design

De novo design of novel molecules with desired properties using generative models — the core ML capability for lead generation and scaffold hopping in drug discovery.

## When to Use This Skill

- Generate molecules with target properties (QED, LogP, SA, docking score)
- Explore chemical space around a hit/lead (analogue generation, scaffold hopping)
- Design molecules conditioned on a protein pocket (SBDD)
- Optimize multi-property objectives (Pareto front: potency + selectivity + ADMET)
- Benchmark or compare generative models (MOSES / GuacaMol suites)
- Build a RL-based focused library generator (REINVENT 4)
- Design linkers or grow fragments (fragment-based generative design)

## Generation Paradigms

| Paradigm | Method | Strength | Weakness |
|----------|--------|----------|----------|
| Language model | SMILES/SELFIES GPT, LSTM | Fast, scalable, fine-tunable | SMILES can be invalid; needs SELFIES |
| VAE | JT-VAE, MolVAE | Smooth latent space, BO-ready | Mode collapse; slow tree encode |
| GNN flow/GAN | GraphAF, GCPN, JunctionGAN | Graph-native; no linearity | Training instability |
| RL optimization | REINVENT 4, REINFORCE | Property-guided; no new arch needed | Reward hacking; mode collapse |
| 3D diffusion | DiffSBDD, TargetDiff | Pocket-conditioned; 3D geometry | Slow, needs structure |
| Fragment-based | DeLinker, DiffLinker | Fragment growing, FBDD | Limited to provided fragments |

## Evaluation Metrics (Know These)

| Metric | What it measures | Target |
|--------|-----------------|--------|
| Validity | % chemically valid | ~100% (SELFIES) / 85-99% (SMILES LM) |
| Uniqueness | % unique in generated set | >99% |
| Novelty | % not in training set | >99% |
| **FCD** | Fréchet ChemNet Distance (distribution) | Lower = closer to drug-like distribution |
| KL divergence | Property distributions vs. reference | Lower |
| Scaffold diversity | # unique Murcko scaffolds / N | Higher |
| IntDiv | Internal diversity (mean pairwise 1-Tc) | > 0.85 |
| SNN | Similarity to nearest neighbor in training | < 0.6 (novel) |

## Quick Start — SELFIES + GPT sampling

```python
import selfies as sf
from rdkit import Chem

# Encode/decode SELFIES (guaranteed valid)
smiles = "CC(=O)Oc1ccccc1C(=O)O"  # aspirin
selfies_str = sf.encoder(smiles)
decoded_smiles = sf.decoder(selfies_str)
mol = Chem.MolFromSmiles(decoded_smiles)  # always valid

# Get SELFIES alphabet for tokenization
alphabet = sf.get_semantic_robust_alphabet()

# Decode a random generated SELFIES token sequence (always valid):
generated_tokens = ["[C]", "[Branch1]", "[C]", "[=O]", "[N]", "[H]"]
generated_smiles = sf.decoder("".join(generated_tokens))
```

## Quick Start — REINVENT 4 scoring component

```python
# Install: pip install reinvent
# REINVENT 4 uses TOML config for staged learning

import toml

config = {
    "run_type": "reinforcement_learning",
    "device": "cuda",
    "tb_logdir": "tb_logs",
    "json_out_config": "run_config.json",
    "parameters": {
        "use_checkpoint": False,
        "prior_file": "path/to/prior.prior",
        "agent_file": "path/to/prior.prior",
        "batch_size": 128,
        "n_steps": 1000,
    },
    "scoring": {
        "type": "custom_product",
        "parallel": False,
        "components": [
            {"type": "qed", "name": "QED", "weight": 1.0},
            {"type": "sa_score", "name": "SA", "weight": 1.0,
             "transform": {"type": "reverse_sigmoid", "low": 1.0, "high": 6.0, "k": 0.5}},
        ],
        "diversity_filter": {
            "type": "IdenticalMurckoScaffold",
            "minscore": 0.4,
            "bucket_size": 25,
        }
    }
}
with open("rl_config.toml", "w") as f:
    toml.dump(config, f)
# Run: reinvent -l rl_run.log rl_config.toml
```

## Router — What to Read

| Task | Reference |
|------|-----------|
| Theory: molecular space, SMILES/SELFIES/graphs, metrics, MOSES/GuacaMol benchmarks | `references/generation-theory.md` |
| SELFIES grammar, SMILES LM (GPT/LSTM), HuggingFace fine-tuning, sampling strategies | `references/selfies-lm.md` |
| REINVENT 4: RL optimization, multi-component scoring, diversity filters, oracles | `references/rl-reinvent.md` |
| JT-VAE: tree decomposition, latent BO; TorchDrug graph generative models overview | `references/vae-jtvae.md` |
| Structure-based 3D generation: DiffSBDD, TargetDiff, Pocket2Mol, linker design | `references/sbdd-diffusion.md` |

## Software Stack

| Package | Install | Role |
|---------|---------|------|
| `selfies` | `pip install selfies` | Always-valid molecular grammar |
| `reinvent` | `pip install reinvent` | RL de novo design (AZ REINVENT 4) |
| `guacamol` | `pip install guacamol` | Benchmark suite (17 goal-directed + distributional) |
| `moses` | `pip install molsets` | MOSES benchmark (6 metrics) |
| `transformers` | `pip install transformers` | GPT/LSTM LMs (HuggingFace) |
| `torchdrug` | `pip install torchdrug` | GCPN, GraphAF, JT-VAE (graph-native) |
| `DiffSBDD` | GitHub: arneschneuing/DiffSBDD | 3D pocket-conditioned diffusion |
| `DiffLinker` | GitHub: igashov/DiffLinker | Linker design in 3D |

## Key Pitfalls

- **SMILES LMs can generate 10-50% invalid** → use SELFIES; or add validity filter post-hoc
- **Reward hacking in RL**: model learns degenerate structures that maximize score — add diversity filter + SA penalty
- **FCD is not computed from structure**: requires ChemNet embeddings (guacamol includes this)
- **Novelty ≠ synthesizability**: always check SA score ≤ 4, run retrosynthesis (ASKCOS/AiZynthFinder)
- **3D diffusion needs pocket quality**: must use properly prepared protein (see `homology-modeling` → structure-prep)
- **Mode collapse in VAE**: monitor KL weight β; schedule β-VAE warmup

## Related Skills

- `torchdrug` — GCPN, GraphAF, GraphDF, JT-VAE implementation
- `rdkit` — validity checks, property scoring oracles (QED, SA, fingerprints)
- `docking` — docking oracle for RL scoring (Vina/Gnina scoring function)
- `pharmacophore` — pharmacophore constraints for conditional generation
- `homology-modeling` → `structure-prep` — pocket preparation for SBDD
- `scientific-skills:zinc-database` — training/reference sets (ZINC20)
- `mmpa` (upcoming) — matched molecular pair analysis on generated series
