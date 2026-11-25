---

## name: biochemistry
description: >
  Expert biochemistry assistant for researchers and students. Use this skill whenever the user needs:
  understanding enzyme kinetics, metabolic pathways, protein structure, biomolecule characterization, biochemical techniques,
  or any rigorous academic treatment of biochemistry. Covers metabolism, enzyme mechanisms, and laboratory methods.
license: MIT
compatibility: opencode
metadata:
  audience: biochemists, molecular biologists, researchers
  category: biology

# Biochemistry — Academic Research Assistant

Covers: **Metabolic Pathways · Enzyme Kinetics · Protein Structure · Biomolecule Characterization · Biochemical Techniques · Metabolism Regulation**

---

## Enzyme Kinetics

### Michaelis-Menten Equation

```
v = (Vmax × [S]) / (Km + [S])

Where:
- v = reaction velocity
- Vmax = maximum velocity
- [S] = substrate concentration
- Km = Michaelis constant (substrate at half Vmax)
```

### Enzyme Inhibition Types

|Inhibition|Km|Vmax|Characteristic|
|----------|---|---|--------------|
|Competitive|↑|No change|Vmax unchanged, competes with substrate|
|Non-competitive|No change|↓|Binds enzyme not substrate|
|Mixed|Both change|Both change|Binds both ES and E|
|Uncompetitive|Both ↓|↓|Binds only ES complex|

```python
import numpy as np

class EnzymeKinetics:
    """Enzyme kinetics calculations"""
    
    def michaelis_menten(self, S, Vmax, Km):
        """
        Calculate reaction velocity
        S: Substrate concentration
        Vmax: Maximum velocity  
        Km: Michaelis constant
        """
        return (Vmax * S) / (Km + S)
    
    def lineweaver_burk(self, S, v):
        """
        Linearize: 1/v = (Km/Vmax)(1/S) + 1/Vmax
        Plot: x = 1/S, y = 1/v
        - Slope = Km/Vmax
        - y-intercept = 1/Vmax
        - x-intercept = -1/Km
        """
        return 1/v, 1/S
    
    def inhibition_effect(self, S, Vmax, Km, Ki, I, inhibitor_type):
        """
        Calculate velocity with inhibitor
        """
        if inhibitor_type == 'competitive':
            Km_app = Km * (1 + I/Ki)
            return self.michaelis_menten(S, Vmax, Km_app)
        
        elif inhibitor_type == 'non-competitive':
            Vmax_app = Vmax / (1 + I/Ki)
            return self.michaelis_menten(S, Vmax_app, Km)
        
        elif inhibitor_type == 'uncompetitive':
            Vmax_app = Vmax / (1 + I/Ki)
            Km_app = Km / (1 + I/Ki)
            return self.michaelis_menten(S, Vmax_app, Km_app)
        
        elif inhibitor_type == 'mixed':
            alpha = 1 + I/Ki
            alpha_prime = 1 + I/Ki  # Simplified
            Vmax_app = Vmax / alpha
            Km_app = Km * alpha_prime / alpha
            return self.michaelis_menten(S, Vmax_app, Km_app)
    
    def catalytic_efficiency(self, kcat, Km):
        """
        kcat/Km - specificity constant
        Upper limit: 10^8-10^9 M^-1 s^-1 (diffusion limit)
        """
        return kcat / Km
```

---

## Metabolic Pathways

### Glycolysis

```
Glucose → Glucose-6-P → Fructose-6-P → Fructose-1,6-BP
                            ↓
                    [Payoff phase]
                    1,3-BPG → 3-PG → 2-PG → PEP → Pyruvate

Net: Glucose + 2 NAD+ + 2 ADP + 2 Pi → 2 Pyruvate + 2 NADH + 2 ATP
```

### Citric Acid Cycle (Krebs Cycle)

```
Acetyl-CoA + Oxaloacetate → Citrate → Isocitrate → α-Ketoglutarate
                                                    ↓
                                          Succinyl-CoA → Succinate
                                                    ↓
                                          Fumarate → Malate → Oxaloacetate

Products per acetyl-CoA:
- 3 NADH
- 1 FADH₂
- 1 GTP (ATP)
- 2 CO₂
```

### Oxidative Phosphorylation

```python
class OxidativePhosphorylation:
    """ETC and ATP synthesis"""
    
    # P/O ratios (ATP per electron pair)
    P_TO_O = {
        "NADH": 2.5,  # Complex I
        "FADH2": 1.5,  # Complex II
        "QH2": 1.5     # Complex III
    }
    
    # Electron transport chain complexes
    COMPLEXES = {
        "I": {
            "name": "NADH:ubiquinone oxidoreductase",
            "substrates": ["NADH"],
            "inhibitors": ["rotenone", "amytal"]
        },
        "II": {
            "name": "Succinate dehydrogenase",
            "substrates": ["succinate", "FADH2"],
            "inhibitors": ["thenoyltrifluoroacetone"]
        },
        "III": {
            "name": "Cytochrome bc1",
            "substrates": ["QH2"],
            "inhibitors": ["antimycin A", "myxothiazol"]
        },
        "IV": {
            "name": "Cytochrome c oxidase",
            "substrates": ["cytochrome c"],
            "inhibitors": ["cyanide", "CO", "azide"]
        }
    }
    
    def calculate_atp(self, nadh_input, fadh2_input):
        """Calculate ATP yield from glucose"""
        # Glycolysis: 2 NADH (cytosolic - requires shuttle)
        glycolytic_nadh = 2 * 1.5  # ~1.5 or 2.5 depending on shuttle
        
        # Pyruvate dehydrogenase: 2 NADH
        pdh_nadh = 2 * 2.5
        
        # Krebs cycle: 6 NADH + 2 FADH2
        krebs_nadh = 6 * 2.5
        krebs_fadh2 = 2 * 1.5
        
        total_nadh = glycolytic_nadh + pdh_nadh + krebs_nadh
        total_fadh2 = krebs_fadh2 + fadh2_input
        
        return (total_nadh * 2.5) + (total_fadh2 * 1.5) + 2  # +2 GTP
```

---

## Protein Structure

### Hierarchical Organization

|Level|Features|
|-----|--------|
|Primary|Amino acid sequence|
|Secondary|α-helices, β-sheets (hydrogen bonds)|
|Tertiary|3D fold (disulfide, hydrophobic)|
|Quaternary|Subunit assembly|

```python
class ProteinStructure:
    """Protein structure concepts"""
    
    # Secondary structure prediction (simplified)
    CHOU_FASMAN = {
        "alpha_helix": {
            "residues": ["A", "C", "L", "M", "E", "H", "Q"],
            "Pα": 1.42
        },
        "beta_sheet": {
            "residues": ["V", "Y", "I", "F", "W"],
            "Pβ": 1.70
        }
    }
    
    def predict_secondary(self, sequence):
        """
        Chou-Fasman method
        Calculate Pα and Pβ for windows
        """
        predictions = []
        
        for i in range(len(sequence) - 6):
            window = sequence[i:i+6]
            
            p_alpha = sum(self.CHOU_FASMAN["alpha_helix"]["Pα"] 
                         for aa in window if aa in self.CHOU_FASMAN["alpha_helix"]["residues"])
            p_beta = sum(self.CHOU_FASMAN["beta_sheet"]["Pβ"]
                        for aa in window if aa in self.CHOU_FASMAN["beta_sheet"]["residues"])
            
            if p_alpha > p_beta and p_alpha > 1.0:
                predictions.append("H")  # Helix
            elif p_beta > p_alpha and p_beta > 1.0:
                predictions.append("E")  # Sheet
            else:
                predictions.append("C")  # Coil
        
        return predictions
```

---

## Biochemical Techniques

### Spectroscopy

|Technique|Information|Application|
|---------|-----------|------------|
|UV-Vis|Absorption at 280 nm|Protein concentration|
|Fluorescence|Intrinsic (Trp) or extrinsic|Structure, binding|
|Circular dichroism|Secondary structure|α/β content|
|IR Spectroscopy|Bond vibrations|Functional groups|

### Chromatography

|Method|Principle|Use|
|-----|--------|---|
|Ion exchange|Charge|Protein purification|
|Affinity|Tag/protein binding|His-tag, antibody|
|Size exclusion|Molecular size|Buffer exchange|
|HPLC|Various|Small molecule analysis|

### Electrophoresis

|Technique|Application|
|---------|-----------|
|SDS-PAGE|Molecular weight|
|Native PAGE|Native conformation|
|2D gel|pI + MW|
|Western blot|Protein identification|

```python
class ProteinPurification:
    """Protein purification calculations"""
    
    def calculate_ion_exchange(self, protein_pI, buffer_pH):
        """
        Determine if cation or anion exchange
        pI < pH → net negative → anion exchange
        pI > pH → net positive → cation exchange
        """
        if protein_pI < buffer_pH:
            return "Anion exchange (negatively charged)"
        else:
            return "Cation exchange (positively charged)"
    
    def est_sds_page_mw(self, migration_distance, standard_distances):
        """
        Estimate MW from migration
        log(MW) = log(MW_std) - K × (migration - migration_std)
        """
        pass
```

---

## Metabolic Regulation

### Allosteric Regulation

|Allosteric Effector|Metabolic Pathway|
|-------------------|-----------------|
|ATP|Citrate synthase (−), PFK (−)|
|ADP/AMP|PFK (+), Pyruvate kinase (+)|
|Citrate|PFK (−)|
|Fructose-2,6-bisphosphate|PFK (+)|
|NADH|Citrate synthase (−)|

### Covalent Modification

|Modification|Effect|Example|
|------------|------|-------|
|Phosphorylation|Activate/inhibit| glycogen phosphorylase|
|Ubiquitination|Proteasomal degradation|Cyclins|
|Methylation|Activity, localization|Histones|
|Acetylation|Activity|Histones, enzymes|

---

## Signaling Pathways

### Major Pathways

|Pathway|Receptor|Key Components|
|-------|---------|--------------|
|PKC|RTK, GPCR|DAG, IP₃, Ca²⁺|
|PKA|GPCR|cAMP, PKA|
|PI3K/AKT|RTK|PIP3, AKT|
|MAPK|RTK|Ras-Raf-MEK-ERK|
|JAK-STAT|Cytokine receptor|JAK, STAT|

---

## Common Errors to Avoid

1. **Ignoring enzyme saturation** — Michaelis-Menten applies at low [S]
2. **Not accounting for product inhibition** — Real systems are more complex
3. **Confusing Km with affinity** — Lower Km ≠ higher affinity always
4. **Oversimplifying metabolism** — Regulation is multi-level
5. **Ignoring cellular context** — In vitro ≠ in vivo
6. **Forgetting cofactor requirements** — NAD+, ATP, Mg²⁺ etc.
7. **Incorrect protein concentration** — Dilute solutions absorbances
8. **Not validating structure predictions** — Computational only

