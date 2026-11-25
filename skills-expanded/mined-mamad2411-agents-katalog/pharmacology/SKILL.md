---

## name: pharmacology
description: >
  Expert pharmacology assistant for researchers and students. Use this skill whenever the user needs:
  understanding drug mechanisms, pharmacokinetics, pharmacodynamics, drug-receptor interactions, ADME properties,
  drug-drug interactions, toxicity, or any rigorous academic treatment of pharmacology. Covers receptor theory,
  dose-response relationships, drug metabolism, and clinical pharmacology.
license: MIT
compatibility: opencode
metadata:
  audience: researchers
  category: biology

# Pharmacology — Academic Research Assistant

Covers: **Pharmacokinetics · Pharmacodynamics · Drug-Receptor Interactions · Dose-Response · Drug Metabolism · Toxicity · Drug Interactions · Clinical Pharmacology**

---

## Pharmacokinetics (ADME)

### Absorption

|Route|Bioavailability|Factors Affecting|
|-----|--------------|-----------------|
|Oral|Variable (depends on drug)|First-pass metabolism, pH, transporters|
|IV|100%|None|
|IM|Good|Adequate perfusion|
|SC|Good to moderate|Rate of dissolution|
|Transdermal|Variable|Skin integrity, drug properties|
|Inhalation|Rapid|Vehicle, particle size|

```python
class Pharmacokinetics:
    """Pharmacokinetic modeling"""
    
    def calculate_clearance(self, dose, auc):
        """
        Clearance = Dose / AUC
        Units: L/hr or mL/min
        """
        return dose / auc
    
    def calculate_volume_of_distribution(self, dose, concentration):
        """
        Vd = Dose / C₀
        Volume in which drug would need to be distributed
        """
        return dose / concentration
    
    def half_life_calculation(self, Vd, Cl):
        """
        t½ = 0.693 × Vd / Cl
        """
        return 0.693 * Vd / Cl
    
    def loading_dose(self, target_conc, Vd, bioavailability=1):
        """
        Loading dose = (Target × Vd) / F
        """
        return (target_conc * Vd) / bioavailability
    
    def maintenance_dose(self, target_conc, Cl, dosing_interval, F=1):
        """
        Maintenance dose = Target × Cl × τ / F
        """
        return target_conc * Cl * dosing_interval / F
```

### Distribution

|Parameter|Definition|Clinical Significance|
|---------|-----------|---------------------|
|Vd < 20 L|Blood volume|Limited distribution|
|Vd 20-40 L|Extracellular water|Moderate distribution|
|Vd > 40 L|Total body water|Extensive distribution|
|Vd >> 100 L|Tissue binding|High tissue affinity|

### Protein Binding

```python
# Free drug hypothesis
# Only free drug is pharmacologically active

def free_drug_concentration(total_conc, fu):
    """
    fu = fraction unbound
    C_free = C_total × fu
    """
    return total_conc * fu

def adjust_total_for_protein_binding(total_conc, fu_new, fu_old):
    """
    Adjust dose when protein binding changes
    """
    free_old = total_conc * fu_old
    total_new = free_old / fu_new
    return total_new
```

---

## Pharmacodynamics

### Drug-Receptor Interactions

|Receptor Type|G-Protein|Example|
|-------------|---------|-------|
|GPCR|Most common|β-blockers, antihistamines|
|Ion channel|N/A|Anesthetics, CCBs|
|Nuclear receptor|Direct|Dexamethasone|
|Enzyme inhibition|N/A|ACE inhibitors|

```python
class ReceptorTheory:
    """Drug-receptor interaction models"""
    
    # Hill equation (Emax model)
    def emax_model(self, E_max, C, EC50):
        """
        E = E_max × C / (EC50 + C)
        """
        return E_max * C / (EC50 + C)
    
    def hill_equation(self, E_max, C, EC50, n):
        """
        E = E_max × Cⁿ / (EC50ⁿ + Cⁿ)
        n = Hill coefficient (cooperativity)
        """
        return E_max * (C ** n) / (EC50 ** n + C ** n)
    
    def competitive_antagonism(self, agonist_conc, antagonist_conc, pA2):
        """
        Schild analysis for competitive antagonism
        pA2 = -log(Kb)
        Dose ratio = 1 + [Ant]/Kb
        """
        dose_ratio = 1 + antagonist_conc / (10 ** (-pA2))
        return dose_ratio
```

### Dose-Response Relationships

|Parameter|Definition|Interpretation|
|---------|-----------|--------------|
|EC₅₀|50% maximal effect|Concentration for half-maximal response|
|Efficacy|Maximal effect possible|What the drug can achieve|
|Potency|EC₅₀|Lower EC₅₀ = more potent|
|Therapeutic index|Safety margin|LD₅₀/ED₅₀|

---

## Drug Metabolism

### Phase I Reactions

|Reaction|Enzyme|Example Drug|
|--------|------|------------|
|Oxidation|CYP450|Cortisol, phenytoin|
|Reduction|Aldo-keto reductases|Morphine|
|Hydrolysis|Esterases|Procaine|

### Phase II Reactions

|Reaction|Enzyme|Substrate|Example|
|--------|------|----------|--------|
|Glucuronidation|UGT|Bilirubin|Tramadol|
|Sulfation|SULT|Phenol|Acetaminophen|
|Acetylation|NAT|Isoniazid|
|Glutathione conjugation|GST|N-acetyl-p-benzoquinone|

```python
class DrugMetabolism:
    """Drug metabolism prediction"""
    
    # Common CYP450 substrates, inducers, inhibitors
    CYP450_PROPERTIES = {
        "CYP3A4": {
            "substrates": ["atorvastatin", "clarithromycin", "simvastatin"],
            "inducers": ["rifampin", "carbamazepine", "phenytoin"],
            "inhibitors": ["ketoconazole", "erythromycin", "grapefruit"]
        },
        "CYP2D6": {
            "substrates": ["metoprolol", "tramadol", "codeine"],
            "inhibitors": ["fluoxetine", "paroxetine", "quinidine"]
        },
        "CYP2C9": {
            "substrates": ["warfarin", "phenytoin"],
            "inhibitors": ["fluconazole", "amiodarone"]
        },
        "CYP2C19": {
            "substrates": ["omeprazole", "clopidogrel"],
            "inhibitors": ["fluoxetine", "omeprazole"]
        }
    }
    
    # Drug-drug interactions
    def predict_interaction(self, drug1, drug2, mechanism):
        """
        Mechanisms: competitive inhibition, induction,
        substrate competition, displacement
        """
        interactions = {
            "competitive_inhibition": "Increase substrate levels",
            "induction": "Decrease substrate levels",
            "displacement": "Increase free drug (if highly bound)"
        }
        return interactions.get(mechanism, "Unknown")
```

---

## Drug Interactions

### Interaction Types

|Category|Mechanism|Example|
|--------|---------|-------|
|Pharmacokinetic|Absorption, distribution, metabolism, excretion|Warfarin + metronidazole|
|Pharmacodynamic|Additive, synergistic, antagonistic|ACEI + potassium-sparing diuretic|
|Idiosyncratic|Unpredictable|Hepatic necrosis with valproate|

```python
# Common clinically significant interactions
CLINICALLY_SIGNIFICANT = {
    "warfarin + NSAIDs": "Increased bleeding risk",
    "warfarin + metronidazole": "Increased INR",
    "digoxin + amiodarone": "Increased digoxin levels",
    "clarithromycin + simvastatin": "Rhabdomyolysis risk",
    "methotrexate + NSAIDs": "Increased toxicity",
    "ACEI + potassium": "Hyperkalemia",
    "SSRI + tramadol": "Serotonin syndrome",
    "QT prolonging drugs + other QT drugs": "Torsades"
}
```

---

## Toxicology

### Dose-Response Curves

```
Response
    ▲
100%│───────────────────────────────────────►
    │          ┌────── Toxicity
    │        ╱ 
    │      ╱ 
    │    ╱
    │  ╱
    │╱────────────── Therapeutic effect
    └──────────────────────────────────────►
              Dose
```

### Triage and Management

|Toxin|Antidote|
|-----|--------|
|Opioids|Naloxone|
|Benzodiazepines|Flumazenil|
|Acetaminophen|N-acetylcysteine|
|Warsfarin|Vitamin K, PCC|
|Cyanide|Hydroxocobalamin, nitrites|
|Organophosphates|Atropine, pralidoxime|
|Iron|Deferoxamine|
|Methemoglobinemia|Methylene blue|

---

## Clinical Pharmacology

### Therapeutic Drug Monitoring

|Drug|Therapeutic Range|Notes|
|-----|-----------------|-----|
|Digoxin|0.5-0.9 ng/mL|Check levels 6-8h post-dose|
|Warfarin|INR 2-3 (mechanical valve 2.5-3.5)|Check before next dose|
|Phenytoin|10-20 μg/mL|Non-linear kinetics|
|Lithium|0.6-1.2 mEq/L|Best 12h post-dose|
|Vancomycin|Trough 10-15, Peak 20-40 μg/mL|Trough only for most|
|Aminoglycosides|Trough < 2, Peak depends on drug|Once-daily dosing|

### Drug Dosing in Special Populations

|Renal Impairment|Cockcroft-Gault Equation|
|----------------|-------------------------|
|CrCl =|((140 - age) × weight) / (72 × SCr)|
|Female|× 0.85|

|Hepatic Impairment|Child-Pugh Score|Adjustment|
|------------------|----------------|----------|
|A (mild)|5-6|No change|
|B (moderate)|7-9|Decrease 25-50%|
|C (severe)|10-15|Decrease >50%|

---

## Common Errors to Avoid

1. **Ignoring drug half-life** — Affects dosing interval and time to steady state
2. **Forgetting first-pass metabolism** — Oral vs. IV dosing can differ dramatically
3. **Not checking protein binding** — Free drug determines effect in displacement
4. **Missing drug-drug interactions** — Review all medications at each visit
5. **Inappropriate TDM timing** — Trough vs. peak matters
6. **Not adjusting for organ dysfunction** — Renal/hepatic impairment
7. **Ignoring pharmacogenomics** — CYP2D6, CYP2C19 polymorphism affects many drugs
8. **Confusing potency with efficacy** — EC₅₀ vs. E_max

