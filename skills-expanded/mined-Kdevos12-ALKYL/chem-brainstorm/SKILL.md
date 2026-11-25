---
name: chem-brainstorm
description: Use at the start of any computational chemistry task to structure thinking, map available tools, and generate concrete hypotheses. Covers molecule evaluation, hypothesis building, reaction assessment, and pipeline design. Flexible guide — adapt depth to problem complexity.
---

# Chem-Brainstorm — Computational Chemistry Thinking Guide

A flexible brainstorming framework for comp chem problems. Not a rigid checklist — activate only the steps relevant to the problem at hand. For complex/recurring workflows, load the appropriate `references/protocol-*.md`.

---

## Step 1 — Classify the Problem

Identify which mode(s) apply (can be multiple):

| Mode | Keywords | Protocol |
|------|----------|---------|
| **MOL** | "evaluate this molecule", "properties of X", "is this drug-like?" | `references/protocol-mol-evaluation.md` |
| **HYP** | "why does X work?", "what target?", "generate hypotheses", "SAR" | `references/protocol-hypothesis.md` |
| **RXN** | "will this reaction work?", "retrosynthesis", "conditions", "mechanism" | `references/protocol-reaction.md` |
| **PIPE** | "screen a library", "build a workflow", "automate", "batch" | `references/protocol-pipeline.md` |

For simple one-off questions (e.g. "LogP of aspirin"), skip to Step 3 directly.

---

## Step 2 — Audit Inputs

What is available?

| Input type | Examples |
|-----------|---------|
| **Structure** | SMILES, SDF, MOL, InChI, name |
| **Library** | `.smi`, `.sdf`, CSV with SMILES column |
| **Target** | Gene name, UniProt ID, PDB ID |
| **Reaction** | Reaction SMILES, SMARTS, conditions |
| **Data** | IC50/EC50 table, experimental results |
| **None** | Starting from a concept only |

Missing inputs → note what to fetch (Step 3 MCPs).

---

## Step 3 — Tool Map

Match inputs and goal to available tools. Order = cost (⚡ fast → ⚡⚡⚡ expensive).

### ALKYL Scripts (local, instant)
| Goal | Script | Cost |
|------|--------|------|
| Properties, Lipinski, PAINS | `chem_props.py` | ⚡ |
| Drug-likeness filters (Ro5/Veber/Egan/PAINS) | `chem_filter.py` | ⚡ |
| Full structural analysis (FG, stereo, QED, SA) | `chem_analyze.py` | ⚡ |
| Protonation state at pH | `chem_pka.py --ph 7.4` | ⚡ |
| CYP450 metabolic soft spots | `chem_metabolism.py` | ⚡ |
| Scaffold, BRICS fragments | `chem_scaffold.py` | ⚡ |
| Tautomers, stereoisomers | `chem_tautomers.py` / `chem_enum.py` | ⚡ |
| Substructure / similarity search | `chem_search.py` | ⚡ |
| Compare two molecules (MCS, Δprop) | `chem_compare.py` | ⚡ |
| Apply reaction SMARTS | `chem_react.py` | ⚡ |
| Batch process a library | `chem_batch.py` | ⚡ |
| Diverse subset selection | `chem_diversity.py` | ⚡ |
| 3D conformer generation | `chem_3d.py` | ⚡⚡ |
| QM input (ORCA/Gaussian) | `chem_qm.py` | ⚡⚡⚡ |

### ALKYL Skills (conceptual / coding help)
| Goal | Skill |
|------|-------|
| SMILES / SMARTS / SMIRKS writing | `daylight-theory` |
| RDKit code (any cheminformatics) | `rdkit` |
| ML on molecules (GCN, QSAR, MoleculeNet) | `deepchem` |
| Retrosynthesis, generative ML | `torchdrug` |
| Reaction graph analysis, ITS/DPO | `synkit` |
| HPC/cloud pipeline | `nextflow` |

### MCPs (external data, use when local data insufficient)
| Goal | MCP | Key functions |
|------|-----|--------------|
| Bioactivity, known targets, similar drugs | `ChEMBL` | `compound_search`, `get_bioactivity`, `target_search`, `get_mechanism` |
| Target-disease associations, tractability | `OpenTargets` | `search_entities`, `query_open_targets_graphql` |
| Recent methods, preprints, benchmarks | `bioRxiv` | `search_preprints`, `get_preprint` |
| Clinical context, indications, endpoints | `ClinicalTrials` | `search_trials`, `analyze_endpoints` |

### Marketplace Skills (specialized)
| Goal | Skill |
|------|-------|
| ADME/tox datasets, ML oracles | `scientific-skills:pytdc` |
| Protein structure (AlphaFold, PDB) | `scientific-skills:pdb-database` |
| Purchasable compounds | `scientific-skills:zinc-database` |
| Approved drugs + interactions | `scientific-skills:drugbank-database` |
| DiffDock virtual screening | `scientific-skills:diffdock` |
| Cloud QM (DFT, pKa, Boltz) | `scientific-skills:rowan` |

---

## Step 4 — Propose Directions

Generate **2–3 concrete directions**, each annotated with:
- Cost estimate (⚡/⚡⚡/⚡⚡⚡)
- First concrete action (script call or MCP query)
- What the result will tell us

**Format:**
```
Direction 1 — [name] ⚡
→ Action: python chem_filter.py --smiles "..."
→ Tells us: drug-likeness baseline before investing further

Direction 2 — [name] ⚡⚡
→ Action: ChEMBL compound_search + get_bioactivity
→ Tells us: known activity landscape for this scaffold

Direction 3 — [name] ⚡⚡⚡
→ Action: chem_3d.py → diffdock against PDB:XXXX
→ Tells us: predicted binding pose and affinity
```

---

## Step 5 — Sanity Checks (auto-activate if SMILES available)

Always run before investing in expensive steps:
```
chem_filter.py  → Lipinski, Veber, PAINS alerts
chem_analyze.py → SA score (> 6 = hard to synthesize), QED
chem_pka.py     → dominant form at physiological pH 7.4
chem_metabolism.py → CYP450 liabilities
```

Red flags that change the plan:
- SA score > 6 → consider simpler analog or retrosynthesis first
- PAINS alert → flag as assay interference risk
- net_charge ≠ 0 at pH 7.4 → affects permeability/docking

---

## Step 6 — Literature Anchor (activate for HYP mode or novel targets)

```
bioRxiv.search_preprints(query="[target/method]", date_range="2024-2026")
→ find recent methods, negative results, benchmark conditions

ChEMBL.target_search(query="[gene]")
→ confirm target is druggable, find reference ligands

OpenTargets.search_entities(query="[target]")
→ genetic evidence, disease associations, tractability score
```

---

## Decision Tree

```
Got SMILES?
  └─ Yes → run sanity checks (Step 5) first
  └─ No  → fetch from ChEMBL/PubChem or start from concept

Simple property question?
  └─ Yes → Step 3 scripts directly, no need for full workflow

Need external data?
  └─ Yes → MCPs before running expensive local tools

Complex / reproducible workflow?
  └─ Yes → load references/protocol-*.md
```

---

## Related Skills
- `daylight-theory` — write correct SMARTS/SMIRKS for queries and transforms
- `rdkit` — implement any cheminformatics step in Python
- `synkit` — if the problem involves reaction mechanisms or networks
