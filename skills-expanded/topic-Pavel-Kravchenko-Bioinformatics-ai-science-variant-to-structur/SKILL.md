---
name: ai-science-variant-to-structure-models
description: "Triage variant scores for structural follow-up; pick AlphaFold2 vs AlphaFold3 vs RoseTTAFold2 and gate results on pLDDT/PAE. Use for monomer/complex/ligand model choice or ranking variants by structural confidence."
tool_type: python
primary_tool: pandas
---

# From DNA Variants to Protein Structure: AlphaFold2, AlphaFold3, RoseTTAFold

## When to Use

- A variant-effect pipeline (splice/expression/missense scores) produced candidates and you need to decide which ones justify running a structure predictor.
- You must choose between AlphaFold2, AlphaFold3, and RoseTTAFold2 for a monomer, a protein-nucleic-acid/ligand complex, or a Rosetta-design workflow.
- You need to combine a variant priority score with structural confidence (pLDDT, interface PAE) into one ranked list instead of trusting either signal alone.
- You're building the last stage of a genomics-to-structure triage: variant calling → genomic model scores → structural follow-up.

## Version Compatibility

- AlphaFold2 (ColabFold ≥1.5, or DeepMind `alphafold` ≥2.3) — monomer/complex, no ligands/nucleic acids.
- AlphaFold3 — via AlphaFold Server (alphafoldserver.com, rate-limited) or the open-source non-commercial weights/code (no `pip install`; run via the provided `run_alphafold.py`).
- RoseTTAFold2 / RoseTTAFold-All-Atom — via RosettaCommons GitHub, run via `run_e2e_ver.sh`.
- pandas ≥2.0, numpy ≥1.24, Python ≥3.10 for the triage/scoring logic below.

## Prerequisites

- `pip install pandas numpy` for the scoring/decision code.
- A prior variant-effect scoring step (splice score, expression delta, missense probability, population rarity) — see `bio-applied-variant-calling-and-snp-analysis` / `bio-applied-clinical-genomics`.
- Access to one of: ColabFold/AlphaFold2 install, AlphaFold Server or AF3 source, or a RoseTTAFold2 checkout with GPU.

**Confidence thresholds for decision-making:** require pLDDT ≥ 70 AND interface PAE ≤ 15 Å before using a structural prediction to guide hypothesis generation. Non-coding variants (splice, regulatory) rarely benefit from structure modeling — reserve it for missense variants whose mechanism plausibly depends on protein conformation or an interface.

**Goal:** rank variants by how much they'd benefit from structural follow-up.

**Approach:** combine coding status, missense probability, expression impact, and rarity into one composite score; non-coding variants score zero regardless of other signals.

```python
import numpy as np
import pandas as pd

np.random.seed(23)

variants = pd.DataFrame([
    {"var": "v1", "gene": "GENE1", "coding": 1, "max_ds": 0.12, "expr_delta": 0.45, "missense_prob": 0.80, "rarity_score": 0.90},
    {"var": "v2", "gene": "GENE2", "coding": 0, "max_ds": 0.91, "expr_delta": 0.15, "missense_prob": 0.05, "rarity_score": 0.70},
    {"var": "v3", "gene": "GENE3", "coding": 1, "max_ds": 0.20, "expr_delta": 0.30, "missense_prob": 0.65, "rarity_score": 0.85},
    {"var": "v4", "gene": "GENE4", "coding": 1, "max_ds": 0.05, "expr_delta": 0.10, "missense_prob": 0.40, "rarity_score": 0.60},
])

def structure_priority(row: pd.Series) -> float:
    """Composite score for whether a variant deserves structural follow-up.

    Non-coding variants (coding == 0) are zeroed out: splice/regulatory
    mechanisms rarely need a 3D structure to interpret. Coding variants
    are weighted toward missense impact, with expression, rarity, and
    splice disruption as secondary evidence.
    """
    if row["coding"] == 0:
        return 0.0
    return (
        0.45 * row["missense_prob"] +
        0.25 * abs(row["expr_delta"]) +
        0.20 * row["rarity_score"] +
        0.10 * row["max_ds"]
    )

variants["structure_priority"] = variants.apply(structure_priority, axis=1)
variants.sort_values("structure_priority", ascending=False)
```

## Model Selection

| Scenario | Prefer |
|---|---|
| Single-chain monomer, fast baseline | **AlphaFold2** |
| Complex with nucleic acids / ligands / modified residues | **AlphaFold3** |
| Rosetta-centric workflows and interface exploration | **RoseTTAFold2** |

**Goal:** pick a structure predictor from the biological context, not benchmark averages.

**Approach:** encode the decision as an explicit function so the choice is reproducible across a batch of variants/genes.

```python
def choose_structure_model(
    has_complex: bool,
    has_ligand_or_nucleic: bool,
    need_open_rosetta_workflow: bool,
) -> str:
    """Pick AF2 / AF3 / RoseTTAFold2 for one target.

    Order matters: ligand/nucleic-acid content forces AF3 regardless of
    other flags, since AF2 cannot model them at all.
    """
    if has_ligand_or_nucleic:
        return "AlphaFold3"
    if need_open_rosetta_workflow:
        return "RoseTTAFold2"
    if has_complex:
        return "AlphaFold3"
    return "AlphaFold2"

print(choose_structure_model(False, False, False))  # AlphaFold2 (simple monomer)
print(choose_structure_model(True, False, False))   # AlphaFold3 (protein complex)
print(choose_structure_model(False, True, False))   # AlphaFold3 (ligand/nucleic acid)
print(choose_structure_model(False, False, True))   # RoseTTAFold2 (Rosetta workflow)
```

Actual invocations once a model is chosen (adjust paths/flags per install):

```bash
# AlphaFold2 via ColabFold (local or notebook)
colabfold_batch input.fasta out_dir/ --num-recycle 3

# AlphaFold3 (open-source, non-commercial weights required)
python run_alphafold.py --json_path=input.json --output_dir=out_dir/

# RoseTTAFold2
bash RoseTTAFold2/run_e2e_ver.sh input.fa out_dir/
```

## Integrating Confidence with Variant Priority

**Goal:** avoid letting a high variant-priority score drive conclusions from a low-confidence structural model.

**Approach:** merge structural confidence metrics onto the variant table and multiply, so a confident-but-low-priority variant and a high-priority-but-unreliable-model variant both get penalized appropriately.

```python
structure_results = pd.DataFrame([
    {"var": "v1", "mean_plddt": 84, "interface_pae": 6.0},
    {"var": "v3", "mean_plddt": 72, "interface_pae": 14.0},
    {"var": "v4", "mean_plddt": 58, "interface_pae": 22.0},
])

merged = variants.merge(structure_results, on="var", how="left")
merged["confidence_factor"] = (
    0.6 * (merged["mean_plddt"].fillna(50) / 100.0) +
    0.4 * (1.0 - np.clip(merged["interface_pae"].fillna(30) / 30.0, 0, 1))
)
merged["final_priority"] = merged["structure_priority"] * merged["confidence_factor"]
merged.sort_values("final_priority", ascending=False)[
    ["var", "gene", "structure_priority", "confidence_factor", "final_priority"]
]
```

## Pitfalls

- Structure prediction generates hypotheses, not final proof — pair it with orthogonal evidence (functional assays, literature, patient/phenotype context).
- Low-confidence regions (pLDDT < 70, interface PAE > 15 Å) must not drive high-stakes decisions; a missing row in `structure_results` gets `fillna(50)`/`fillna(30)` defaults above, which read as low confidence by design — don't silently treat a missing prediction as "unknown/neutral".
- AF2 cannot model ligands, nucleic acids, or covalent modifications — routing a ligand-bound complex through AF2 instead of AF3 silently drops that chemistry.
- AF3 has no `pip install`; it's accessed via alphafoldserver.com (rate-limited) or the open-source non-commercial release run through its own scripts.
- Non-coding (splice/regulatory) variants rarely benefit from structural modeling — spending compute on structure for a `coding == 0` variant is usually wasted effort.

## See Also

- `alphafold-structure-prediction` — running AlphaFold2/ColabFold and reading pLDDT/PAE outputs
- `ai-science-alphafold-protein-design` — AlphaFold3-style complex/design workflows
- `structural-bioinformatics` — general structure file handling and geometric analysis
- `bio-applied-clinical-genomics` — upstream variant scoring and clinical prioritization
