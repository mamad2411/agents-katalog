---
name: homology-modeling
description: Use when building a 3D protein structure from sequence (no experimental structure available). Covers comparative homology modeling (MODELLER), AI-based prediction (AlphaFold2/ColabFold/ESMFold), model quality assessment (DOPE, pLDDT, Ramachandran), template search (HHblits, BLAST, Biopython), and structure preparation for MD or docking.
---

# Homology Modeling — Protein Structure Prediction

MODELLER 10.x · ColabFold · ESMFold · Biopython · pdbfixer · ProDy. For building protein 3D models from sequence when no experimental structure is available.

## When to Use This Skill

- No X-ray/CryoEM structure for your target protein (or coverage is partial)
- Building a receptor model for docking or MD when AlphaFold DB lacks your variant/mutant
- Constructing chimeric or engineered proteins not in existing databases
- Validating or improving an AI-predicted structure with experimental template data
- Generating a starting conformation for free-energy calculations (→ `force-fields` skill)

## Decision Tree — Which Method to Use

```
Target sequence available?
  NO → retrieve from UniProt / NCBI first

Do you have a homologous template (sequence identity > 25%)?
  YES + identity > 50%  → MODELLER (comparative, references/modeller-basics.md)
  YES + identity 25–50% → MODELLER multi-template or AlphaFold2 with template
  NO / < 25%             → AlphaFold2 / ColabFold (references/alphafold-esm.md)

Throughput?
  Single target           → ColabFold interactive / MODELLER script
  Batch (>10 proteins)    → ColabFold batch CLI or ESMFold API
  No MSA / fast screen    → ESMFold (references/alphafold-esm.md)

After modeling:
  → Validate model        → references/structure-quality.md
  → Prepare for MD        → references/structure-prep.md
  → Prepare for docking   → references/structure-prep.md + docking skill
```

## Quick Start

```python
# --- Option A: MODELLER comparative modeling (single template) ---
from modeller import Environ
from modeller.automodel import AutoModel

env = Environ()
env.io.atom_files_directory = ['.', '../templates']

a = AutoModel(env,
              alnfile  = 'alignment.pir',   # PIR format — see modeller-basics.md
              knowns   = '5HT2A_template',  # template code (PDB ID, no extension)
              sequence = 'TARGET_SEQ')      # target sequence ID in .pir file

a.starting_model = 1
a.ending_model   = 5    # generate 5 models, pick best by DOPE score

a.make()

# Select best model
results = [(m.molpdf, m.name) for m in a.outputs
           if m['failure'] is None]
results.sort()
print(f"Best model: {results[0][1]}  DOPE: {results[0][0]:.1f}")
```

```bash
# --- Option B: ColabFold (AlphaFold2 engine, local CLI) ---
colabfold_batch target.fasta output_dir/ \
    --num-models 5 \
    --num-recycle 3 \
    --amber \
    --use-gpu-relax

# Best model: output_dir/target_relaxed_rank_001_*.pdb
# Scores:     output_dir/target_scores_rank_001_*.json
```

```python
# --- Option C: ESMFold (single-sequence, no MSA, fastest) ---
import torch, esm

model = esm.pretrained.esmfold_v1()
model = model.eval().cuda()

sequence = "MKTAYIAKQRQISFVKSHFSRQ..."   # full amino acid sequence

with torch.no_grad():
    output = model.infer_pdb(sequence)

with open("esmfold_model.pdb", "w") as f:
    f.write(output)
print("Model saved to esmfold_model.pdb")
```

## Router — What to Read

| Task | Reference |
|------|-----------|
| MODELLER automodel, PIR format, loop refinement, multi-template, DOPE ranking | `references/modeller-basics.md` |
| ColabFold CLI, AlphaFold2 output parsing, ESMFold API, pLDDT/PAE interpretation | `references/alphafold-esm.md` |
| DOPE scores, Ramachandran analysis, MolProbity, ProDy, RMSD to experiment | `references/structure-quality.md` |
| pdbfixer, propka3, disulfide bonds, protonation states, ACE/NME capping | `references/structure-prep.md` |
| HHblits/HHpred template search, BLAST, Biopython alignments, multi-template selection | `references/template-search.md` |

## Method Comparison

| Method | Best for | Seq. ID required | Speed | Accuracy |
|--------|----------|-----------------|-------|----------|
| MODELLER (automodel) | Close homologs, custom restraints | > 30% | Medium | ★★★★ (with good template) |
| MODELLER (multi-template) | Coverage gaps, divergent regions | > 25% | Medium | ★★★★ |
| ColabFold / AlphaFold2 | Any target, captures remote homologs | None | Slow (GPU) | ★★★★★ |
| ESMFold | Fast screen, no MSA, single sequence | None | Fast (GPU) | ★★★ |

## Key Tools

| Tool | Install | Role |
|------|---------|------|
| `modeller` | `conda install -c salilab modeller` (requires license key) | Comparative modeling |
| `colabfold` | `pip install colabfold[alphafold]` or conda | AF2-based prediction |
| `esm` | `pip install fair-esm` | ESMFold single-sequence prediction |
| `biopython` | `pip install biopython` | PDB I/O, BLAST, alignments, Ramachandran |
| `pdbfixer` | `conda install -c conda-forge pdbfixer` | Missing residues, H addition |
| `propka` | `pip install propka` | pKa prediction, protonation states |
| `prody` | `pip install prody` | Structural analysis, NMA, chain alignment |

## Installation

```bash
# MODELLER (requires free academic license from https://salilab.org/modeller/)
conda install -c salilab modeller
# Set MODELLER license key:
export KEY_MODELLER="XXXXXXXX"  # add to ~/.bashrc

# ColabFold (local, GPU recommended)
pip install "colabfold[alphafold]"
# OR via conda (recommended for reproducibility):
conda install -c conda-forge -c bioconda colabfold

# ESMFold
pip install fair-esm
# ESMFold also requires torch >= 2.0 and ~15 GB VRAM for full model

# Biopython + ProDy
pip install biopython prody

# pdbfixer + propka (structure prep)
conda install -c conda-forge pdbfixer
pip install propka

# Verify
python -c "from modeller import Environ; print('MODELLER OK')"
colabfold_batch --help
python -c "import esm; print('ESM OK')"
```

## Related Skills

- `docking` → use homology model as receptor for virtual screening (check pLDDT > 80 in pocket)
- `force-fields` → MD simulation of the built model (OpenMM, AMBER, GROMACS)
- `mdanalysis` → trajectory analysis after MD equilibration of the model
- `qm-dft` → QM refinement of active-site geometry (xTB/ORCA)
- `free-energy` → FEP/TI relative binding free energies using model receptor
- `ase` → QM/MM or GFN2-xTB optimization of small binding-site models
- PDB: use `PDB MCP` or `pdb_database` skill → download template PDB
