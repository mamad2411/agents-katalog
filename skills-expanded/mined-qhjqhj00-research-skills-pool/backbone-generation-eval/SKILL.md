---
name: backbone-generation-eval
description: This benchmark evaluates the designability, structural diversity, and novelty of generated protein backbones across varying lengths. It measures how well diffusion models can produce foldable and structurally distinct protein scaffolds. Use when the user wants to benchmark on Protein Backbone Generation Benchmark, or asks about evaluating this task. Reports scRMSD.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2406.01622
  bibtex_key: norton2024sifting
  confidence: high
---

# backbone-generation-eval

> Sifting through the Noise: A Survey of Diffusion Probabilistic Models and Their Applications to Biomolecules — Norton et al. (2024) (arXiv:2406.01622, 2024)

## What this evaluates

This benchmark evaluates the designability, structural diversity, and novelty of generated protein backbones across varying lengths. It measures how well diffusion models can produce foldable and structurally distinct protein scaffolds.

## Datasets

- **Protein Backbone Generation Benchmark** — total 250; splits: test (250)

## Metrics

- `scRMSD` **(primary)** — range: Å
  - Minimum difference between the RMSD of the folded Cα backbones and the corresponding sample. A protein is considered designable if scRMSD < 2.0Å.

## Input / output format

**Input**: Target protein backbone structures of specified lengths (50, 100, 150, 200, 250 amino acids).

**Output**: Generated protein backbone structures (Cα coordinates).

## Scoring recipe

```python
designable_proteins = []
for backbone in generated_backbones:
    seqs = ProteinMPNN.generate(backbone, temp=0.1)
    folded = ESMFold.fold(seqs[0])
    rmsd = compute_rmsd(folded.Ca, backbone.Ca)
    if rmsd < 2.0:
        designable_proteins.append(backbone)
avg_tm = mean(TMAlign.score(p1, p2) for p1, p2 in combinations(designable_proteins))
max_pdb = max(FoldSeek.score(p, pdb_db) for p in designable_proteins)
novelty_pct = sum(1 for p in designable_proteins if FoldSeek.score(p, pdb_db) < 0.5) / len(designable_proteins)
```

## Common pitfalls

- Using raw RMSD instead of the minimum difference after sequence folding (scRMSD).
- Comparing TM-Scores without normalizing by the length of the longer protein.
- Ignoring structural similarity filtering when assessing novelty against the PDB.

## Evidence (verbatim from paper)

> To test designability, we used ProteinMPNN [70] at a temperature of 0.1 to create 8 possible sequences, which were then folded using ESMFold [69]. The minimum difference between the RMSD of the folded Cα backbones and the corresponding sample was recorded as the scRMSD for the structure. A protein is considered designable if scRMSD is less than 2.0Å, and the percentage of designable proteins is reported for each method.

## Citation

```bibtex
@misc{norton2024sifting,
  title={Sifting through the Noise: A Survey of Diffusion Probabilistic Models and Their Applications to Biomolecules},
  author={Norton et al. (2024)},
  year={2024},
  note={arXiv:2406.01622}
}
```

- arXiv: 2406.01622
