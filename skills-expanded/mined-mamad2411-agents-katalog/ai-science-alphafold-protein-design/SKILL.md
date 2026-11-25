---
name: ai-science-alphafold-protein-design
description: "Interpret AlphaFold2/AF3 pLDDT/PAE scores, fetch AlphaFold DB models by UniProt ID, and rank RFdiffusion/ProteinMPNN designs. Use when asked about pLDDT, PAE, AF2 vs AF3, AlphaFold DB fetch, or design triage."
tool_type: python
primary_tool: biopython
---

# AlphaFold and Protein Design

## When to Use

- Explaining AF2 vs AF3 architecture (Evoformer/Structure Module vs Diffusion Module)
- Interpreting pLDDT or PAE output to decide whether a predicted structure is trustworthy
- Fetching a precomputed model from the AlphaFold Protein Structure Database by UniProt accession
- Comparing two predicted structures (e.g., paralogs, design iterations) via Cα RMSD
- Ranking de novo design candidates from an RFdiffusion → ProteinMPNN → AF2/AF3 pipeline

## Version Compatibility

- AlphaFold2 (DeepMind/ColabFold weights, model_v4 files); AlphaFold3 (2024 release, non-commercial license, DNA/RNA/ligand support)
- AlphaFold DB REST files: `https://alphafold.ebi.ac.uk/files/AF-{UNIPROT}-F1-model_v4.pdb`
- biopython ≥1.81, numpy ≥1.24, requests ≥2.28, matplotlib ≥3.7, Python ≥3.9

## Prerequisites

```bash
pip install biopython numpy requests matplotlib
```

Familiarity with PDB/mmCIF format and basic structure concepts (see `bio-core-protein-structure`).

## Key Gotchas

- **AF2 does not predict dynamics** — it outputs one static conformation, typically the most stable one
- **High pLDDT ≠ biologically correct** — disordered regions can score high pLDDT if they resemble folded training examples
- **PAE is directional, not symmetric**: `PAE[i, j]` asks "if residue i is placed correctly, how confident are we about j's position?"
- **AF2 vs AF3**: AF2 handles single proteins/homomers only. AF3 adds protein-DNA, protein-RNA, protein-ligand, and modified-residue complexes

## Architecture

**AF2 inputs**: MSA representation (N_seq × L × 256) + pair representation (L × L × 128)

**Evoformer** (48 blocks): row-wise gated self-attention → column-wise attention → outer product mean (MSA→pair) → triangular multiplicative updates → triangular attention (pair→pair)

**Structure Module** (8 iterations): Invariant Point Attention (IPA) — attention over scalar pair features plus local 3D point attention within each residue's rigid frame; equivariant to global rotation/translation

**Outputs**: all-atom 3D coordinates, per-residue pLDDT, distogram/PAE

**AF3 change**: replaces the Structure Module with a **Diffusion Module** that generates all-atom coordinates jointly for proteins, nucleic acids, small molecules, and ions

## Confidence Metrics

**Goal:** decide whether a predicted region can be trusted before using it downstream.
**Approach:** AF2 writes per-residue pLDDT (0-100) into the B-factor column of the output PDB instead of a real B-factor — extract it per residue and bin it against the standard thresholds (>90 very high, 70-90 confident, 50-70 low, <50 likely disordered).

```python
import numpy as np
from Bio.PDB import PDBParser


def per_residue_plddt(pdb_path: str) -> np.ndarray:
    """Extract per-residue pLDDT from an AlphaFold PDB (stored in the B-factor column)."""
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure('model', pdb_path)
    plddt = []
    for residue in structure.get_residues():
        atoms = list(residue.get_atoms())
        if not atoms:
            continue
        ca = next((a for a in atoms if a.name == 'CA'), atoms[0])
        plddt.append(ca.get_bfactor())
    return np.array(plddt)


def confidence_bands(plddt: np.ndarray) -> dict:
    """Bin residues into AF2's standard confidence bands (fraction of residues in each)."""
    return {
        'very_high (>90)': float(np.mean(plddt > 90)),
        'confident (70-90)': float(np.mean((plddt > 70) & (plddt <= 90))),
        'low (50-70)': float(np.mean((plddt > 50) & (plddt <= 70))),
        'very_low (<50)': float(np.mean(plddt <= 50)),
    }
```

## Fetching from AlphaFold DB and Comparing Structures

**Goal:** pull a precomputed model for a UniProt accession and compare it to another structure (e.g., a paralog or an experimental reference).
**Approach:** download the `model_v4` PDB directly (no GPU or local model needed), then superimpose Cα atoms to get a global RMSD.

```python
import requests
from pathlib import Path
from Bio.PDB import PDBParser, Superimposer


def fetch_alphafold_pdb(uniprot_id: str, out_dir: str = 'pdb_files') -> str:
    """Download a precomputed AlphaFold DB model (model_v4) for a UniProt accession."""
    out = Path(out_dir)
    out.mkdir(exist_ok=True)
    url = f'https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb'
    r = requests.get(url, timeout=30)
    if r.status_code != 200:
        raise RuntimeError(f'Fetch failed: {uniprot_id} ({r.status_code})')
    path = out / f'{uniprot_id}.pdb'
    path.write_text(r.text)
    return str(path)


def ca_rmsd(pdb_a: str, pdb_b: str) -> float:
    """Superimpose Cα atoms of two structures and return the RMSD in angstroms."""
    parser = PDBParser(QUIET=True)
    s1 = parser.get_structure('a', pdb_a)
    s2 = parser.get_structure('b', pdb_b)
    ca1 = [a for a in s1.get_atoms() if a.name == 'CA']
    ca2 = [a for a in s2.get_atoms() if a.name == 'CA']
    n = min(len(ca1), len(ca2))
    if n == 0:
        raise ValueError('No CA atoms found')
    sup = Superimposer()
    sup.set_atoms(ca1[:n], ca2[:n])
    return float(sup.rms)


# Example: compare HRAS (P01112) and KRAS (P01116) G-domains
# hras = fetch_alphafold_pdb('P01112')
# kras = fetch_alphafold_pdb('P01116')
# print(ca_rmsd(hras, kras))
```

## Design Candidate Ranking

**Goal:** triage a batch of de novo design candidates coming out of an RFdiffusion (backbone) → ProteinMPNN (sequence) → AF2/AF3 (validation) pipeline.
**Approach:** combine mean pLDDT, interface PAE, and sequence novelty into a single priority score, weighting confidence over novelty (novel-but-unconfident designs are cheap to generate but expensive to validate in the wet lab).

```python
import numpy as np


def design_priority(mean_plddt: float, interface_pae: float, seq_novelty: float) -> float:
    """Score a design candidate: higher is better. seq_novelty in [0, 1] from e.g. edit distance to nearest known sequence."""
    conf = 0.7 * (mean_plddt / 100.0) + 0.3 * (1.0 - np.clip(interface_pae / 30.0, 0, 1))
    return float(0.8 * conf + 0.2 * seq_novelty)


candidates = [
    {'id': 'd1', 'plddt': 86, 'pae': 7.5, 'novelty': 0.40},
    {'id': 'd2', 'plddt': 74, 'pae': 15.0, 'novelty': 0.70},
    {'id': 'd3', 'plddt': 91, 'pae': 5.0, 'novelty': 0.20},
]
for c in candidates:
    c['priority'] = design_priority(c['plddt'], c['pae'], c['novelty'])
ranked = sorted(candidates, key=lambda x: x['priority'], reverse=True)
```

## Pitfalls

- Don't compare PAE across two independently predicted monomers as if it were a real interface PAE — that requires a joint (multimer) prediction
- Low pLDDT in a C-terminal tail or linker usually reflects genuine intrinsic disorder, not a bad prediction — don't discard the whole model over it
- `ca_rmsd` above truncates to `min(len(ca1), len(ca2))` in sequence order — only valid when the two chains are the same protein/paralog with aligned numbering; for divergent sequences, align first
- AlphaFold DB confidence stats are proteome-wide averages (Varadi et al. 2022: ~58% of residues >70 pLDDT, ~36% >90) — don't expect any single protein pair to match them exactly

## See Also

- `bio-core-protein-structure` — PDB/mmCIF parsing and structural biology fundamentals
- `alphafold-structure-prediction` — running AF2/ESMFold prediction jobs
- `ai-science-esm2-embeddings` / `protein-language-models` — sequence-based embeddings as an alternative/complement to structure prediction
- `alphafold-database` — bulk querying and browsing the AlphaFold DB

## Sources

- [Jumper et al. 2021, AlphaFold2 (Nature)](https://www.nature.com/articles/s41586-021-03819-2)
- [Abramson et al. 2024, AlphaFold3 (Nature)](https://www.nature.com/articles/s41586-024-07487-w)
- [Varadi et al. 2022, AlphaFold DB (NAR)](https://doi.org/10.1093/nar/gkab1061)
- [AlphaFold repo](https://github.com/google-deepmind/alphafold) / [AF3 repo](https://github.com/google-deepmind/alphafold3)
