---
name: biochemistry
description: "Enzymes, metabolic pathways, protein structure, nucleic acids, bioenergetics, and cellular signaling"
category: chemistry
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/chemistry/biochemistry/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Biochemistry

## Scope
Biochemistry explores the molecular mechanisms of biological systems, examining macromolecules (proteins, nucleic acids, lipids, carbohydrates), enzymatic catalysis, bioenergetics, and metabolic networks.

## Core Mechanisms

### 1. Protein Structure & Folding
- **Primary**: Amino acid sequence linked by peptide bonds (trans configuration).
- **Secondary**: $\alpha$-helices (3.6 residues/turn, $i \to i+4$ H-bonding) and $\beta$-sheets (parallel/antiparallel).
- **Ramachandran Plot**: Conformationally allowed $\phi$ and $\psi$ dihedral angles.
- **Tertiary & Quaternary**: Hydrophobic collapse, salt bridges, disulfide bonds ($Cys-S-S-Cys$).

### 2. Enzyme Kinetics
- **Michaelis-Menten Equation**:
  $$v_0 = \frac{V_{\max}[S]}{K_m + [S]}$$
  where $K_m = (k_{-1} + k_2)/k_1$ is the substrate concentration at $v_0 = V_{\max}/2$.
- **Turnover Number**: $k_{\text{cat}} = V_{\max} / [E]_T$; catalytic efficiency = $k_{\text{cat}} / K_m$.
- **Lineweaver-Burk Double Reciprocal**:
  $$\frac{1}{v_0} = \frac{K_m}{V_{\max}}\frac{1}{[S]} + \frac{1}{V_{\max}}$$
- **Inhibition Mechanisms**:
  - *Competitive*: $V_{\max}$ unchanged, $K_m$ increases ($K_m' = \alpha K_m$).
  - *Uncompetitive*: Both $V_{\max}$ and $K_m$ decrease by $\alpha'$.
  - *Noncompetitive (Mixed)*: $V_{\max}$ decreases, $K_m$ may increase or decrease.

### 3. Metabolic Pathways & Bioenergetics
- **ATP Free Energy**: $\Delta G^{\circ\prime} = -30.5\text{ kJ/mol}$ for ATP hydrolysis.
- **Glycolysis**: Glucose $\to$ 2 Pyruvate + 2 NADH + 2 ATP (net).
- **Citric Acid (TCA) Cycle**: Acetyl-CoA oxidized to $2 CO_2$, yielding $3 NADH, 1 FADH_2, 1 GTP$.
- **Oxidative Phosphorylation**: Chemiosmotic proton gradient driving ATP synthase ($F_0F_1$).

## Tools & Standards
- **Databases**: Protein Data Bank (PDB), KEGG Pathway, UniProt, BRENDA (Enzyme database).
- **Software**: PyMOL, ChimeraX, AlphaFold, BioPython.
- **Canonical References**: Nelson & Cox — *Lehninger Principles of Biochemistry*; Berg, Tymoczko & Stryer — *Biochemistry*.
