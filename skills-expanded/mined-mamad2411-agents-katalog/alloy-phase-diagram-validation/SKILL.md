---
name: alloy-phase-diagram-validation
description: Evaluates a Wang-Landau sampling method combined with cluster expansion for predicting thermodynamic phase diagrams of binary alloys. It probes the method's ability to capture ordering and phase-separation tendencies, and accurately reproduce experimental phase boundaries and transition temperatures. Use when the user wants to benchmark on Cu-Au alloy, Pd-Rh alloy, or asks about evaluating this task. Reports cross-validation score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1609.05292
  bibtex_key: takeuchi2016wanglandau
  confidence: high
---

# alloy-phase-diagram-validation

> A new Wang-Landau approach to obtain phase diagrams for multicomponent alloys — Takeuchi et al. (2016) (arXiv:1609.05292, 2016)

## What this evaluates

Evaluates a Wang-Landau sampling method combined with cluster expansion for predicting thermodynamic phase diagrams of binary alloys. It probes the method's ability to capture ordering and phase-separation tendencies, and accurately reproduce experimental phase boundaries and transition temperatures.

## Datasets

- **Cu-Au alloy** — total 183; splits: train (183)
- **Pd-Rh alloy** — total 71; splits: train (71)

## Metrics

- `cross-validation score` **(primary)** — range: other
  - Mean absolute error between DFT-calculated formation energies and cluster expansion predictions for structures excluded from the ECI fitting set.
- `phase diagram fidelity` — range: other
  - Comparison of predicted temperature-composition (T-x) phase boundaries and transition temperatures against established experimental data (Okamoto et al.).

## Input / output format

**Input**: Atomic configurations on an fcc lattice (supercells up to 32 atoms), chemical potentials (μ), and temperature (T).

**Output**: Effective Cluster Interactions (ECI), Helmholtz free energy F(T,x), equilibrium composition x, and T-x phase diagrams.

## Scoring recipe

```python
def evaluate_eci(dft_energies, ce_energies):
    return mean(abs(dft_energies - ce_energies))

def evaluate_phase_diagram(predicted_Tx, experimental_Tx):
    temp_error = abs(predicted_Tx['T_trans'] - experimental_Tx['T_trans'])
    boundary_match = compare_curves(predicted_Tx['x'], experimental_Tx['x'])
    return temp_error, boundary_match
```

## Common pitfalls

- Neglecting non-configurational free energy (vibrational/electronic) shifts transition temperatures, though low-T phases remain qualitatively correct.
- Differential errors when converting T-μ diagrams to T-x diagrams, exacerbated by small simulation cell sizes.
- Phase-separation systems may lack clear heat capacity peaks, requiring common-tangent construction on Helmholtz free energy instead of peak detection.

## Evidence (verbatim from paper)

> We obtained 16 optimized ECI (see Fig.[1](#S3.F1 "Figure 1 ‣ III.1 Cu-Au ‣ III results and discussion ‣ A new Wang-Landau approach to obtain phase diagrams for multicomponent alloys")(a)) with the prediction accuracy, a cross-validation score, of 1.1 meV/atom, which gives sufficient accuracy to capture the thermodynamic characteristics for Cu-Au alloy. Compared with our result and the experimental one*Okamoto*et al.* ([a](#bib.bib30 ""))*, we confirmed that our method successfully describe the Cu-Au phase diagram that captures the thermodynamic characteristics of Cu-Au alloy.

## Citation

```bibtex
@misc{takeuchi2016wanglandau,
  title={A new Wang-Landau approach to obtain phase diagrams for multicomponent alloys},
  author={Takeuchi et al. (2016)},
  year={2016},
  note={arXiv:1609.05292}
}
```

- arXiv: 1609.05292
