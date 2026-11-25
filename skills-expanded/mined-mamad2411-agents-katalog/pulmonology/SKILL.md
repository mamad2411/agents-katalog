---

## name: pulmonology
description: >
  Expert pulmonology assistant for medical students and researchers. Use this skill whenever the user needs:
  understanding of respiratory diseases, pulmonary function testing, respiratory physiology, diagnostic approaches
  for lung disorders, treatment protocols, or any rigorous academic treatment of pulmonary medicine. Covers 
  obstructive, restrictive, and interstitial lung diseases, along with respiratory diagnostics and therapeutics.
license: MIT
compatibility: opencode
metadata:
  audience: medical-students
  category: medicine

# Pulmonology — Academic Research Assistant

Covers: **Obstructive Lung Disease · Restrictive Lung Disease · Pulmonary Function Testing · Respiratory Physiology · Interstitial Lung Disease · Sleep Medicine · Respiratory Failure · Pulmonary Imaging**

---

## Respiratory Anatomy & Physiology

### Pulmonary Ventilation

|Parameter|Definition|Normal Value|
|---------|-----------|-------------|
|Tidal volume (TV)|Volume of each breath at rest|500 mL|
|Inspiratory reserve volume (IRV)|Maximal inspiratory effort|3000 mL|
|Expiratory reserve volume (ERV)|Maximal expiratory effort|1200 mL|
|Residual volume (RV)|Volume remaining after max expiration|1200 mL|
|Total lung capacity (TLC)|Maximal lung volume|6000 mL|
|Vital capacity (VC)|Maximal voluntary ventilation|4800 mL|

### Gas Exchange

```
Alveolar Gas Equation:
PAO₂ = FiO₂ × (Patm - PH₂O) - (PaCO₂ / RQ)

Where:
- FiO₂ = Fraction inspired O₂ (0.21 at sea level)
- Patm = Atmospheric pressure (760 mmHg at sea level)
- PH₂O = Water vapor pressure (47 mmHg at 37°C)
- RQ = Respiratory quotient (~0.8)

Normal PAO₂: ~100 mmHg
Normal PaO₂: 80-100 mmHg (declines with age)
```

### Ventilation-Perfusion (V/Q) Matching

|Region|V/Q Ratio|Implication|
|------|---------|-----------|
|Normal lung base|~0.8|Optimal matching|
|Lung apex|>3.0|Wasted ventilation (high V/Q)|
|Lung base|<0.8|Wasted perfusion (low V/Q)|
|Shunt|V/Q = 0|No gas exchange (e.g., ARDS)|

---

## Pulmonary Function Testing

### Spirometry

```
Flow-Volume Loop Interpretation:

      Inspiratory    ┌──────┐   ┌──────────┐
      limb           │      │   │          │
                     │      │   │          │
                     │      │   │          │
                     │      │   │          │
                     └──────┴───┘          │
                    └──────────────────────┘
                         Expiratory limb

Obstructive:  Scooped ("festoons"), reduced FEV1/FVC
Restrictive:  Tall/narrow, preserved FEV1/FVC, reduced volumes
```

|Parameter|Obstructive|Restrictive|
|---------|------------|-----------|
|FVC|Normal or ↓|↓ Markedly|
|FEV₁|↓ Markedly|↓ Proportionally|
|FEV₁/FVC|↓ (<70%)|Normal (>70%)|
|TLC|Normal or ↑|↓|
|RV|Normal or ↑|↓|
|DLCO|Normal or ↓|Normal or ↓|

### Lung Volumes

|Volume|Definition|Clinical Significance|
|-------|-----------|---------------------|
|Functional residual capacity (FRC)|RV + ERV|Body pletysmography measures|
|Total lung capacity (TLC)|All volumes|Serial measurements track disease|
|Diffusing capacity (DLCO)|Gas transfer|Interstitial vs. obstructive|

---

## Obstructive Lung Diseases

### Chronic Obstructive Pulmonary Disease (COPD)

**Definition**: Progressive airflow limitation, not fully reversible, usually progressive, associated with enhanced inflammatory response to noxious particles/gases.

#### GOLD Classification

|GROUP|Symptoms|Spirometry|FEV₁ (% predicted)|
|-----|---------|----------|------------------|
|A|Low risk, few symptoms|FEV₁ ≥ 80%|≥ 80|
|B|Low risk, more symptoms|FEV₁ ≥ 50-79%|50-79|
|C|High risk, few symptoms|FEV₁ 30-49%|30-49|
|D|High risk, more symptoms|FEV₁ < 30%|< 30|

#### Pharmacologic Management

```python
COPD_TREATMENT = {
    "short-acting_bronchodilators": {
        "SABA": ["albuterol", "salbutamol"],
        "SAMA": ["ipratropium"],
        "use": "Rescue therapy"
    },
    "long-acting_bronchodilators": {
        "LABA": ["salmeterol", "formoterol", "indacaterol"],
        "LAMA": ["tiotropium", "umeclidinium", "glycopyrronium"],
        "use": "Maintenance therapy"
    },
    "inhaled_corticosteroids": {
        "indications": ["History of ≥2 exacerbations/yr", "Elevated eosinophils"],
        "examples": ["fluticasone", "budesonide"]
    },
    "triple_therapy": {
        "components": ["LABA + LAMA + ICS"],
        "indications": ["Group D COPD", "Frequent exacerbations"]
    }
}
```

### Asthma

**Definition**: Chronic inflammatory disorder of airways, reversible airflow obstruction, airway hyperresponsiveness.

#### Asthma Control Test (ACT)

|Score|Control Level|Action|
|-----|-------------|------|
|25|Well-controlled|Maintain therapy|
|20-24|Well-controlled|May step down|
|15-19|Not well-controlled|Step up therapy|
|<15|Very poorly controlled|Urgent action|

#### Stepwise Asthma Management

|Step|Treatment|Notes|
|-----|---------|-----|
|1|SABA PRN|Low-dose ICS PRN as needed|
|2|Low-dose ICS|Or LTRA|
|3|Medium-dose ICS + LABA|Consider adding LAMA|
|4|High-dose ICS + LABA|Add LAMA|
|5|Add oral montelukast|Refer for OCS, consider biologics|
|6|Add oral corticosteroids|Biologic therapy|

---

## Restrictive Lung Diseases

### Interstitial Lung Diseases (ILD)

|Category|Examples|Key Features|
|---------|--------|-------------|
|Idiopathic pulmonary fibrosis (IPF)|Usual interstitial pneumonia (UIP)|Honeycombing, basilar|
|Sarcoidosis|Non-caseating granulomas|Lymphadenopathy, upper lobe|
|Hypersensitivity pneumonitis|Bird fancier's lung|Exposure history|
|Connective tissue disease-associated|RA-ILD, SSc-ILD|Underlying autoimmune disease|
|Drug-induced|Bleomycin, methotrexate|Medication history|

### Pulmonary Function in Restriction

```
Pattern: ↓ TLC, ↓ FVC, ↓ FEV₁, Normal FEV₁/FVC ratio

Severity (TLC % predicted):
- Mild: 65-80%
- Moderate: 50-64%
- Severe: <50%
```

### High-Resolution CT (HRCT) Patterns

|Pattern|Characteristics|Differential|
|-------|---------------|-----------|
|UIP/IPF|Honeycombing, reticulation, traction bronchiectasis|Idiopathic pulmonary fibrosis|
|COP|Cryptogenic organizing pneumonia|Bilateral consolidations|
|NSIP|Ground-glass, reticulation, relatively preserved|Symmetric, lower lobe|
|LIP|Lung cysts, ground-glass|Diffuse, thin-walled cysts|

---

## Respiratory Failure

### Type I vs. Type II

|Type|pO₂|pCO₂|Examples|
|----|----|-----|--------|
|I (hypoxemic)|< 60 mmHg|Normal or ↓|PE, ARDS, pneumonia, edema|
|II (hypercapnic)|< 60|> 50|COPD exacerbation, obesity hypoventilation|

### Acute Respiratory Distress Syndrome (ARDS)

**Berlin Definition**:

|P|O₂ Requirement|
|---|---|
|Mild|PaO₂/FiO₂ 200-300 mmHg with PEEP ≥ 5|
|Moderate|PaO₂/FiO₂ 100-200 mmHg with PEEP ≥ 5|
|Severe|PaO₂/FiO₂ < 100 mmHg with PEEP ≥ 5|

**Etiology**:
- Direct: Pneumonia, aspiration, near-drowning, inhalation injury
- Indirect: Sepsis, transfusion, pancreatitis, trauma

---

## Sleep-Related Breathing Disorders

### Obstructive Sleep Apnea (OSA)

**Diagnosis**: AHI ≥ 5 events/hour with symptoms, or AHI ≥ 15 events/hour regardless of symptoms

|Event|Type|Definition|
|------|-----|----------|
|Apnea|Cessation|≥ 10 seconds|
|Hypopnea|Decrease|≥ 30% + 3% desaturation or arousal|
|RDI|Apnea + hypopnea|Events per hour|

### Treatment Options

|Treatment|Indication|Notes|
|---------|-----------|-----|
|CPAP|First-line OSA|Standard pressure 5-20 cmH₂O|
|BiPAP|Ventilatory failure|CPAP failure, overlap syndrome|
|MAD|Dental|OAS mild-moderate|
|Surgery|UPPP|Palatal surgery|
|Weight loss|All overweight|5-10% improvement|

---

## Pulmonary Imaging

### Chest X-Ray Patterns

|Pattern|Radiographic Appearance|Clinical Correlation|
|-------|------------------------|---------------------|
|Consolidation|Airspace opacity, air bronchograms|Pneumonia, edema, hemorrhage|
|Interstitial|Reticular, nodular|ILD, heart failure|
|Cavitation|Central lucency|Lung abscess, TB, tumor|
|Pleural effusion|Blunted costophrenic angle|Transudate vs. exudate|
|Pneumothorax|Visceral pleural line, no lung markings|Trauma, spontaneous|

### CT Pulmonary Angiography (CTPA)

**Indication**: Suspected pulmonary embolism

|Finding|Sensitivity|Specificity|
|--------|------------|------------|
|Central PE|83-100%|89-97%|

---

## Common Errors to Avoid

1. **Confusing obstructive vs. restrictive patterns** — Always look at FEV₁/FVC ratio and TLC
2. **Ignoring DLCO** — Essential for differentiating emphysema vs. chronic bronchitis
3. **Missing hypoxemia triggers** — Consider altitude, V/Q mismatch, shunt
4. **Inadequate rescue inhaler technique** — Check technique at each visit
5. **Underestimating sleep apnea** — Screen all snorers, especially with hypertension
6. **Delayed biopsy in ILD** — Consider multidisciplinary discussion
7. **Oxygen prescription errors** — Target SpO₂ 88-92% for COPD, 94-98% for others
8. **Ignoring vaccination status** — Influenza annually, pneumococcal per guidelines

