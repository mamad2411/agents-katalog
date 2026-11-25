---

## name: organic
description: >
  Expert organic chemistry assistant for academic researchers and students. Use this skill whenever the user 
  needs: understanding of organic reaction mechanisms, functional group chemistry, stereochemistry, molecular 
  orbital theory applied to organic systems, synthesis planning, or any rigorous academic treatment of organic 
  chemistry. Covers reaction mechanisms, synthesis strategies, and structural analysis.
license: MIT
compatibility: opencode
metadata:
  audience: chemists, students, researchers
  category: chemistry

# Organic Chemistry — Academic Research Assistant

Covers: **Functional Groups · Reaction Mechanisms · Stereochemistry · Synthesis · Molecular Orbital Theory · Named Reactions · Nomenclature**

---

## Functional Groups & Reactivity

### Priority in Nomenclature (Highest to Lowest)

| priority | Functional Group | Suffix | Example |
|----------|------------------|--------|---------|
| 1 | Carboxylic acid | -oic acid | Acetic acid |
| 2 | Ester | -oate | Ethyl acetate |
| 3 | Amide | -amide | Acetamide |
| 4 | Nitrile | -nitrile | Acetonitrile |
| 5 | Aldehyde | -al | Acetaldehyde |
| 6 | Ketone | -one | Acetone |
| 7 | Alcohol | -ol | Ethanol |
| 8 | Thiol | -thiol | Ethanethiol |
| 9 | Amine | -amine | Ethylamine |
| 10 | Alkene | -ene | Ethene |
| 11 | Alkyne | -yne | Ethyne |
| 12 | Ether | ether | Diethyl ether |
| 13 | Halide | halide | Chloroethane |

### Hydrocarbon Chemistry

#### Alkanes (Saturated Hydrocarbons)

- **General formula**: CₙH₂ₙ₊₂
- **Hybridization**: sp³
- **Bond angle**: 109.5°
- **Reactions**: Halogenation (radical), combustion

```
CH₄ + Cl₂ → CH₃Cl + HCl (monochlorination)
           ↓ (excess Cl₂)
    CHCl₃ → CCl₄
```

#### Alkenes (Unsaturated - C=C)

- **General formula**: CₙH₂ₙ
- **Hybridization**: sp²
- **Bond angle**: 120°
- **Reactions**: Addition, polymerization, oxidation

```
Addition Reactions:
┌─────────────────────────────────────────────────┐
│ Electrophilic Addition:                        │
│                                                 │
│   H₂C=CH₂ + HCl → CH₃-CH₂Cl                   │
│   (Markovnikov: H adds to less-substituted C)  │
│                                                 │
│   H₂C=CH₂ + H₂O → CH₃-CH₂OH (acid-catalyzed)  │
│                                                 │
│ Halogen Addition:                               │
│                                                 │
│   H₂C=CH₂ + Br₂ → Br-CH₂-CH₂-Br                │
│   (Anti addition - stereospecific)             │
│                                                 │
│ Hydroboration:                                  │
│                                                 │
│   H₂C=CH₂ + BH₃ → CH₃-CH₂-BH₂                  │
│   → H₂O₂ → CH₃-CH₂OH (Anti-Markovnikov)        │
└─────────────────────────────────────────────────┘
```

#### Alkynes (Unsaturated - C≡C)

- **General formula**: CₙH₂ₙ₊₂
- **Hybridization**: sp
- **Bond angle**: 180°
- **Reactions**: Addition, oxidation, acid-base

---

## Reaction Mechanisms

### Nucleophilic Substitution (SN1 and SN2)

|Feature|SN2|SN1|
|-------|----|----|
|**Mechanism**|Concerted, backside attack|Two-step, carbocation intermediate|
|**Stereochemistry**|Inversion (Walden inversion)|Racemization|
|**Rate law**|2nd order (depends on both)|1st order (depends on substrate)|
|**Substrate preference**|Primary > Secondary|Secondary > Tertiary|
|**Nucleophile strength**|Strong nucleophiles favored|Weak nucleophiles okay|
|**Solvent polar protic favors**|No|Yes|

```python
# Reaction kinetics conceptual model
class NucleophilicSubstitution:
    """Analyze SN1 vs SN2 reaction factors"""
    
    def predict_mechanism(self, substrate_type, nucleophile, solvent):
        """
        Predict whether SN1 or SN2 is favored
        """
        factors = {
            "substrate": {
                "methyl": "SN2 only",
                "primary": "SN2 favored",
                "secondary": "depends on conditions",
                "tertiary": "SN1 only"
            },
            "nucleophile": {
                "strong": "SN2 (if substrate allows)",
                "weak": "SN1 (if substrate allows)"
            },
            "solvent": {
                "polar_protic": "SN1 favored (solvates nucleophile)",
                "polar_aprolic": "SN2 favored (nucleophile free)"
            }
        }
        
        if substrate_type == "tertiary":
            return "SN1"
        elif substrate_type == "primary":
            return "SN2"
        else:
            return "depends on nucleophile and solvent"
    
    # Steric hindrance calculation
    def steric_hindrance_score(self, substituents):
        """Estimate relative steric hindrance"""
        hindrance = {
            "H": 0,
            "CH3": 1,
            "C2H5": 1.5,
            "iPr": 2,
            "tBu": 3
        }
        return sum(hindrance.get(s, 2) for s in substituents)
```

### Elimination Reactions (E1 and E2)

|Feature|E2|E1|
|-------|----|----|
|**Mechanism**|Concerted, anti-periplanar|Two-step, carbocation|
|**Stereochemistry**|Anti-elimination required|Racemization|
|**Base requirement**|Strong base required|Weak base okay|
|**Substrate preference**|Secondary/tertiary|Secondary/tertiary|

---

## Stereochemistry

### Chirality and Enantiomers

- **Chiral center**: Tetrahedral carbon with 4 different substituents
- **Enantiomers**: Non-superimposable mirror images
- **Optical activity**: Rotate plane-polarized light in opposite directions

### R/S Configuration Determination

```
Priority rules (Cahn-Ingold-Prelog):
1. Higher atomic number = higher priority
2. If tie, check next atoms (I > Br > Cl > S > P > F > O > N > C > H)
3. Double/triple bonds count as multiple atoms

Determination steps:
┌────────────────────────────────────────────────┐
│ 1. Assign priorities (1=highest, 4=lowest)   │
│ 2. View from side opposite lowest priority   │
│ 3. 1→2→3 clockwise = R (Rectus)              │
│ 4. 1→2→3 counterclockwise = S (Sinister)    │
└────────────────────────────────────────────────┘
```

### Geometric Isomers (E/Z)

|E|Z|
|---|---|
|Ethyl > Ethyl (trans)|Same side (cis)|
|Higher priority groups on opposite sides|Higher priority groups on same side|

### Conformational Analysis

```
Butane (CH₃-CH₂-CH₂-CH₃) Newman projections:

Anti (staggered)      Gauche (staggered)     Eclipsed
    H                    CH₃                  H
  /   \                /   \                /   \
 H     H              H     H               H     CH₃
  \   /                \   /                \   /
   C-C                  C-C                   C-C
  /   \                /   \                /   \
CH₃    H              CH₃    H              CH₃    H

Energy: 0 kcal/mol      ~0.9 kcal/mol       ~3.6 kcal/mol
```

---

## Synthesis Planning

### Retrosynthetic Analysis

```python
class Retrosynthesis:
    """Simplified retrosynthetic analysis framework"""
    
    # Common transformations
    TRANSFORMATIONS = {
        "alcohol": {
            "from_alkene": ["hydroboration", "oxymercuration", "acid-catalyzed hydration"],
            "from_carbonyl": ["reduction (NaBH₄, LiAlH₄)", "Grignard addition"],
            "from_ester": ["reduction (DIBAL-H)"]
        },
        "alkene": {
            "from_alkyl_halide": ["elimination (E2/E1)"],
            "from_diol": ["pinacol rearrangement"],
            "from_alkyne": ["partial reduction (H₂/Pd, Lindlar)"]
        },
        "carbonyl": {
            "from_alcohol": ["oxidation (PCC, Jones)"],
            "from_alkene": ["ozonolysis"],
            "from_alkyne": ["hydration (HgSO₄)"]
        },
        "carboxylic_acid": {
            "from_alcohol": ["strong oxidation"],
            "from_ester": ["hydrolysis (acid or base)"],
            "from_nitrile": ["hydrolysis"]
        }
    }
    
    # Synthesis planning
    def plan_synthesis(self, target_functional_group, available_starting_materials):
        """Suggest synthetic route"""
        return self.TRANSFORMATIONS.get(target_functional_group, {})
```

### Common Named Reactions

|Reaction|Name|Key Feature|
|--------|-----|-----------|
|Oxidation|Jones oxidation|PCC for primary → aldehyde|
|Reduction|NaBH₄ reduction|Selective for aldehydes/ketones|
|Grignard|Grignard reaction|Forms C-C bonds|
|Wittig|Wittig reaction|Alkenes from carbonyls|
|Diels-Alder|[4+2] cycloaddition|Stereospecific|
|Heck|Heck coupling|Pd-catalyzed vinylation|
|Suzuki|Suzuki coupling|Boron-carbon coupling|

---

## Molecular Orbital Theory

### Frontier Molecular Orbital (FMO) Analysis

```
HOMO-LUMO Interactions:

Nucleophile (HOMO) → Electrophile (LUMO)
        or
Electrophile (HOMO) → Nucleophile (LUMO)

Orbital symmetry rules govern reaction feasibility:
- Thermally allowed: Symmetry-allowed reactions
- Photochemical: Different symmetry requirements

Conjugation effects:
- Allylic system: 3 p-orbitals → 3 MOs
  - ψ1 (bonding): Both electrons
  - ψ2 (nonbonding): 1 electron
  - ψ3 (antibonding): Empty
  
- Diene: 4 p-orbitals → 4 MOs
  - ψ1, ψ2 (bonding): Filled
  - ψ3*, ψ4* (antibonding): Empty
```

### Pericyclic Reactions

|Reaction|Type|Mechanism|
|--------|-----|--------|
|Diels-Alder|[4+2] cycloaddition|Thermally allowed|
|Electrocyclic ring closure|(4n) electrons, conrotatory|Thermally allowed|
|Electrocyclic ring closure|(4n+2) electrons, disrotatory|Thermally allowed|
|Claisen rearrangement|[3,3]-sigmatropic|Thermally allowed|

---

## Spectroscopic Methods

### IR Spectroscopy (Functional Group Identification)

|Region (cm⁻¹)|Bond|Functional Group|
|-------------|-----|-----------------|
|3600-3200|O-H stretch|Alcohol (broad), carboxylic acid (very broad)|
|3300-2500|O-H stretch|Carboxylic acid (very broad)|
|3300-2100|C≡N stretch|Nitrile|
|3000-2850|C-H stretch (sp³)|Alkanes|
|3100-3000|C-H stretch (sp²)|Alkenes, aromatics|
|3300|C-H stretch (sp)|Alkyne|
|1750-1700|C=O stretch|Carbonyl compounds|
|1700-1650|C=C stretch|Alkenes|

### NMR Chemical Shifts (¹H)

|Protons|δ (ppm)|Notes|
|--------|--------|------|
|CH₃-|~0.9|Aliphatic methyl|
|-CH₂-|~1.3|Methylene|
|CH-|~1.5|Methine|
|=CH-|~5-6|Vinyl|
|≡CH-|~2-3|Acetylenic|
|Ar-H~|7-8|Aromatic|
|-OH|variable (1-5)|Exchangeable|
|-NH|variable (1-3)|Exchangeable|
|R-CHO|~9-10|Aldehyde|

---

## Common Errors to Avoid

1. **Confusing SN1/SN2 mechanisms** — Always consider substrate structure, nucleophile, and solvent together
2. **Ignoring stereochemistry** — Label chiral centers and specify R/S in products
3. **Forgetting regiochemistry** — Markovnikov vs. anti-Markovnikov matters
4. **Incorrect IUPAC naming** — Follow latest nomenclature rules systematically
5. **Over-relying on memorization** — Understand mechanisms to predict products
6. **Skipping protonation states** — Consider pKa in acid-base reactions
7. **Ignoring steric effects** — Bulky groups affect reactivity significantly
8. **Not considering competing reactions** — Elimination vs. substitution, etc.

