---
name: medicinal-chemistry
description: "Structure-activity relationships (SAR), drug design, pharmacokinetics, Lipinski rules, and hit-to-lead optimization"
category: chemistry
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/chemistry/medicinal-chemistry/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Medicinal Chemistry

## Scope
Medicinal chemistry combines organic chemistry, pharmacology, and molecular biology to discover, design, and optimize therapeutic drug candidates.

## Drug Design Principles

### 1. Lipinski's Rule of Five (Oral Bioavailability)
A drug-like small molecule typically has:
- Molecular weight $\le 500\text{ Da}$
- Octanol-water partition coefficient $\log P \le 5$
- Hydrogen bond donors $\le 5$ ($\sum OH + NH$)
- Hydrogen bond acceptors $\le 10$ ($\sum O + N$)
*(Veber extension: Topological Polar Surface Area $\text{TPSA} \le 140\text{ \AA}^2$, rotatable bonds $\le 10$)*.

### 2. Pharmacokinetics: ADMET Framework
- **Absorption**: Permeability assays (Caco-2, PAMPA).
- **Distribution**: Plasma protein binding (PPB), volume of distribution ($V_d$).
- **Metabolism**: Cytochrome P450 enzymes (CYP3A4, CYP2D6, CYP2C9); phase I (oxidation) and phase II (conjugation).
- **Excretion**: Renal clearance, biliary excretion, half-life ($t_{1/2} = 0.693 V_d / CL$).
- **Toxicity**: hERG cardiac channel inhibition, Ames mutagenicity, hepatotoxicity.

### 3. Structure-Activity Relationships (SAR) & Bioisosterism
- **Classical Bioisosteres**: Carboxylic acid bioisosteres (tetrazole, hydroxamic acid, acyl sulfonamide).
- **Fluorine Substitution**: Enhances metabolic stability (blocks CYP oxidation), modulates pKa and lipophilicity.

## Tools & Standards
- **Cheminformatics**: RDKit, Schrödinger Suite (Glide, Maestro), MOE, AutoDock Vina.
- **Databases**: ChEMBL, DrugBank, PubChem, BindingDB.
- **Canonical References**: Patrick — *An Introduction to Medicinal Chemistry*; Silverman & Holladay — *The Organic Chemistry of Drug Design and Drug Action*.
