---
name: synkit
description: Use when working with SynKit for graph-based reaction informatics: ITS/MTG graph construction, reaction canonicalization, AAM validation, DPO rule extraction and composition, chemical reaction network (CRN) analysis, subgraph matching, and synthesis planning primitives.
---

# SynKit

Graph-based Python toolkit for reaction informatics: ITS graph construction, canonicalization, AAM validation, DPO rule extraction, CRN analysis, and synthesis planning.

**Paper:** doi:10.1021/acs.jcim.5c02123 | JCIM 2025

## When to Use This Skill

- Converting reaction SMILES → ITS graphs (NetworkX) → DPO rules (GML)
- Validating or comparing atom-to-atom mappings (AAMValidator)
- Canonicalizing reaction SMILES (CanonRSMI) or ITS graphs (GraphCanonicaliser)
- Clustering reactions by structural similarity (WL graph hash)
- Extracting and composing reaction rules (DPO formalism)
- Analyzing chemical reaction networks (Feinberg deficiency theory, Petri nets)
- Detecting autocatalysis, siphons, traps in reaction networks
- Planning synthetic routes via rule composition (SynReactor)
- Building reaction databases or curating USPTO/ChEMBL reaction data

## Core Concept: ITS Graph

The **Imaginary Transition State (ITS)** graph merges reactant and product graphs into a single labeled multigraph:
- Nodes: atoms with attributes (symbol, charge, radical, hybridization, H count)
- Edges: bonds with attributes (bond type, `change` flag: formed / broken / unchanged)

ITS ≡ CGR (Condensed Graph of Reaction) — same structure, different naming tradition.

## Quick Start

```python
from synkit.IO import load_reaction_smiles
from synkit.Graph import ITSConstruction
from synkit.Chem import CanonRSMI, AAMValidator

# 1. Parse reaction SMILES → ITS graph (NetworkX)
rxn_smiles = "[CH3:1][OH:2].[Na:3][H:4]>>[CH3:1][O:2][Na:3].[H:4][H:5]"
its = ITSConstruction.from_reaction_smiles(rxn_smiles)

# 2. Canonicalize the reaction SMILES
canon = CanonRSMI(rxn_smiles).canonicalize()

# 3. Validate atom-atom mapping
valid = AAMValidator(rxn_smiles).is_valid()
```

## Router — What to Read

| Task | Reference |
|------|-----------|
| Load reactions, format conversion (SMILES ↔ ITS ↔ GML), data I/O | `references/io-conversion.md` |
| Canonicalization (CanonRSMI), AAM validation, Reaction class | `references/chem-standardization.md` |
| ITS construction, MTG, graph canonicalization, WL hashing, subgraph search | `references/graph-its.md` |
| DPO rules, GML format, rule composition, SynReactor forward/retro | `references/rule-dpo.md` |
| CRN building, Feinberg deficiency theory, Petri nets, autocatalysis | `references/crn-analysis.md` |
| Synthesis planning, route construction, pathway analysis | `references/synthesis-planning.md` |

## Key Submodules

| Module | Role |
|--------|------|
| `synkit.IO` | Reaction SMILES parsing, SMILES ↔ ITS ↔ GML conversion |
| `synkit.Chem` | `CanonRSMI`, `AAMValidator`, `Reaction` standardization |
| `synkit.Graph` | `ITSConstruction`, `GraphCanonicaliser`, WL hash, subgraph search |
| `synkit.Rule` | DPO rules, GML handling, rule composition |
| `synkit.Synthesis` | Forward/retro prediction, route exploration |
| `synkit.CRN` | CRN construction, Feinberg theory, Petri-net analysis |
| `synkit.Vis` | Reaction and mechanism visualization |

## Conversion Pipeline

```
Reaction SMILES (atom-mapped)
    │
    ▼ IO / Graph.ITSConstruction
ITS Graph (NetworkX)         ← cluster, hash, validate
    │
    ▼ Graph.GraphCanonicaliser
Canonical ITS Graph          ← canonical form independent of atom ordering
    │
    ▼ Rule module
DPO Rule (GML format)        ← compose, apply, store
```

All conversions are **lossless** for balanced, atom-mapped reactions.
Caveats: stereochemistry is omitted; explicit H at reaction centers required for GML → SMILES reversion.

## Installation

```bash
pip install synkit          # core (RDKit + NetworkX)
pip install synkit[all]     # full (+ transformers for RXNMapper)
# Python ≥ 3.11 required
```

## Related Skills

- `rdkit` — molecule preprocessing before SynKit ingestion
- `torchdrug` — retrosynthesis with GNNs (complementary ML approach)
- `deepchem` — molecular ML when rule-based approach insufficient
