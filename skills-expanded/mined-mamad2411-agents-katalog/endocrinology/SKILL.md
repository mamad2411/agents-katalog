---

## name: endocrinology
description: >
  Endocrinology expert for hormonal systems, endocrine disorders, and metabolic
  research. Use this skill whenever the user needs: understanding hormone signaling
  pathways, diagnosing endocrine disorders, analyzing metabolic conditions, working
  with hormone replacement therapies, studying diabetes and thyroid disorders, analyzing
  adrenal and pituitary function, or any task involving the endocrine system and
  metabolic disorders. This skill covers clinical endocrinology, molecular endocrinology,
  and metabolic research.
license: MIT
compatibility: opencode
metadata:
  audience: medical-students
  category: medicine

# Endocrinology — Hormonal Systems and Metabolic Disorders

Covers: **Hormone Signaling · Endocrine Glands · Metabolic Disorders · Diabetes · Thyroid · Adrenal · Pituitary · Calcium Metabolism · Reproductive Endocrinology**

-----

## Hormone Classification and Signaling

### Types of Hormones

Hormones can be classified by their chemical structure and mechanism of action:

| Type | Examples | Mechanism | Solubility |
|------|----------|-----------|------------|
| **Peptide/Protein** | Insulin, GH, TSH | Surface receptor, cAMP/IP3 | Water-soluble |
| **Steroid** | Cortisol, estrogen, testosterone | Intracellular receptor | Lipid-soluble |
| **Amino Acid Derivative** | Epinephrine, thyroid hormone | Surface + intracellular | Mixed |
| **Fatty Acid Derivative** | Prostaglandins, leukotrienes | Surface receptor | Lipid-soluble |

### Hormone Signaling Pathways

```python
# Second messenger systems
second_messengers = {
    'cAMP': {
        'activator': 'Gs protein-coupled receptors',
        'effectors': ['PKA', 'CREB'],
        'cascade': 'Adenylyl cyclase → cAMP → PKA → Phosphorylation'
    },
    'IP3/DAG': {
        'activator': 'Gq protein-coupled receptors',
        'effectors': ['PKC', 'Ca²⁺ release'],
        'cascade': 'PLC → IP3 + DAG → Ca²⁺/PKC activation'
    },
    'cGMP': {
        'activator': 'Natriuretic peptides, NO',
        'effectors': ['PKG'],
        'cascade': 'Guanylyl cyclase → cGMP → PKG'
    }
}

# Nuclear receptor signaling
nuclear_receptors = {
    'Type I': {
        'location': 'Cytoplasm',
        'examples': ['GR', 'MR', 'AR', 'ER', 'PR'],
        'mechanism': 'Bind hormone in cytoplasm, translocate to nucleus'
    },
    'Type II': {
        'location': 'Nucleus',
        'examples': ['TR', 'RAR', 'VDR', 'PPAR'],
        'mechanism': 'Pre-bound to DNA, recruit co-activators on hormone binding'
    }
}
```

### Feedback Loops

Endocrine systems use sophisticated feedback mechanisms:

**Negative Feedback (most common):**
- HPA axis: Cortisol suppresses CRH and ACTH
- HPT axis: Thyroid hormone suppresses TSH
- Glucose-insulin: High glucose stimulates insulin, which lowers glucose

**Positive Feedback (rare):**
- Oxytocin during labor: Contractions stimulate more oxytocin
- LH surge: Estrogen stimulates LH release

-----

## Major Endocrine Glands

### Pituitary Gland

The pituitary has anterior (adenohypophysis) and posterior (neurohypophysis) portions:

```python
# Pituitary hormones
anterior_pituitary = {
    'GH': {
        'name': 'Growth Hormone',
        'target': 'Liver, bone, muscle',
        'action': 'Growth, metabolism, IGF-1 production',
        'dysfunction': 'Acromegaly (excess), dwarfism (deficiency)'
    },
    'PRL': {
        'name': 'Prolactin',
        'target': 'Mammary gland',
        'action': 'Milk production',
        'dysfunction': 'Galactorrhea, infertility'
    },
    'ACTH': {
        'name': 'Adrenocorticotropic Hormone',
        'target': 'Adrenal cortex',
        'action': 'Cortisol synthesis',
        'dysfunction': 'Cushing disease (excess), Addison (deficiency)'
    },
    'TSH': {
        'name': 'Thyroid Stimulating Hormone',
        'target': 'Thyroid',
        'action': 'Thyroid hormone synthesis',
        'dysfunction': 'Hyper/hypothyroidism'
    },
    'LH/FSH': {
        'name': 'Gonadotropins',
        'target': 'Gonads',
        'action': 'Sex steroid production, gametogenesis',
        'dysfunction': 'Infertility'
    }
}

posterior_pituitary = {
    'ADH/vasopressin': {
        'action': 'Water retention, vasoconstriction',
        'dysfunction': 'DI (deficiency), SIADH (excess)'
    },
    'Oxytocin': {
        'action': 'Uterine contraction, milk ejection',
        'dysfunction': 'Impaired labor, bonding issues'
    }
}
```

### Thyroid Gland

```python
# Thyroid hormone synthesis
thyroid_hormones = {
    'T4 (thyroxine)': {
        'full_name': '3,5,3\',5\'-tetraiodothyronine',
        'binding': '99.97% protein-bound (TBG)',
        'half_life': '7 days',
        'activity': 'Prohormone, converted to T3'
    },
    'T3 (triiodothyronine)': {
        'full_name': '3,5,3\'-triiodothyronine',
        'binding': '99.5% protein-bound (TBG)',
        'half_life': '1 day',
        'activity': 'Active form'
    },
    'rT3 (reverse T3)': {
        'binding': 'Low',
        'activity': 'Inactive, increased in illness'
    }
}

# Synthesis pathway
synthesis_steps = [
    '1. Iodide uptake via NIS (sodium-iodide symporter)',
    '2. Oxidation of iodide by thyroid peroxidase (TPO)',
    '3. Organification:iodination of tyrosine residues on thyroglobulin',
    '4. Coupling of MIT and DIT to form T3 and T4',
    '5. Storage in colloid',
    '6. Proteolysis and release'
]
```

### Adrenal Gland

```python
# Adrenal cortex zones and hormones
adrenal_zones = {
    'Zona glomerulosa': {
        'hormones': ['Aldosterone'],
        'regulator': 'Renin-angiotensin system, K⁺',
        'function': 'Mineralocorticoid: Na⁺ retention, K⁺ excretion'
    },
    'Zona fasciculata': {
        'hormones': ['Cortisol'],
        'regulator': 'ACTH',
        'function': 'Glucocorticoid: metabolism, stress response'
    },
    'Zona reticularis': {
        'hormones': ['Androgens (DHEA, androstenedione)'],
        'regulator': 'ACTH',
        'function': 'Precursors to sex steroids'
    }
}

adrenal_medulla = {
    'hormones': ['Epinephrine', 'Norepinephrine'],
    'regulator': 'Sympathetic preganglionic neurons',
    'function': 'Fight-or-flight response'
}
```

-----

## Metabolic Disorders

### Diabetes Mellitus

```python
# Diabetes classification and diagnosis
diabetes_diagnosis = {
    'Type 1 Diabetes': {
        'cause': 'Autoimmune destruction of β-cells',
        'insulin': 'Absolute deficiency',
        'age_onset': 'Usually < 30 years',
        'ketosis': 'Prone to DKA',
        'c_peptide': 'Low/undetectable',
        'treatment': 'Insulin therapy'
    },
    'Type 2 Diabetes': {
        'cause': 'Insulin resistance + relative insulin deficiency',
        'insulin': 'Relative deficiency',
        'age_onset': 'Usually > 40 years',
        'ketosis': 'Usually not',
        'c_peptide': 'Normal or high',
        'treatment': 'Lifestyle, OHA, insulin'
    },
    'Gestational Diabetes': {
        'cause': 'Pregnancy-induced insulin resistance',
        'timing': '24-28 weeks gestation',
        'risk_factors': ['Obesity', 'PCOS', 'Family history'],
        'treatment': 'Diet, insulin if needed'
    },
    'MODY': {
        'cause': 'Genetic defects in β-cell function',
        'inheritance': 'Autosomal dominant',
        'subtypes': ['HNF1α', 'GCK', 'HNF4α', etc.]
    }
}

# Diagnostic criteria
diagnostic_criteria = {
    'FPG': '≥126 mg/dL (7.0 mmol/L)',
    '2h OGTT': '≥200 mg/dL (11.1 mmol/L)',
    'HbA1c': '≥6.5% (48 mmol/mol)',
    'RPG': '≥200 mg/dL with classic symptoms',
    'Prediabetes FPG': '100-125 mg/dL',
    'Prediabetes 2h': '140-199 mg/dL',
    'Prediabetes HbA1c': '5.7-6.4%'
}
```

### Thyroid Disorders

```python
# Hypothyroidism
hypothyroidism = {
    'Primary': {
        'cause': 'Thyroid gland failure',
        'TSH': 'High',
        'FT4': 'Low',
        'causes': ['Hashimoto\'s', 'post-thyroidectomy', 'radiation']
    },
    'Secondary': {
        'cause': 'Pituitary failure',
        'TSH': 'Low/normal',
        'FT4': 'Low',
        'causes': ['Pituitary tumor', 'Sheehan syndrome']
    },
    'Tertiary': {
        'cause': 'Hypothalamic failure',
        'TSH': 'Low',
        'FT4': 'Low',
        'causes': ['Hypothalamic disease']
    }
}

# Hyperthyroidism
hyperthyroidism = {
    'Graves\'': {
        'cause': 'TSH receptor antibodies (TRAb)',
        'TSH': 'Suppressed',
        'FT4/FT3': 'Elevated',
        'features': ['Graves ophthalmopathy', 'pretibial myxedema']
    },
    'Toxic multinodular': {
        'cause': 'Autonomous thyroid nodules',
        'TSH': 'Suppressed',
        'FT4/FT3': 'Elevated',
        'features': ['Multiple hot nodules on scan']
    },
    'Thyroiditis': {
        'cause': 'Inflammation releasing stored hormone',
        'TSH': 'Suppressed initially',
        'FT4/FT3': 'Elevated initially',
        'types': ['Subacute', 'Hashimoto\'s', 'Postpartum']
    }
}
```

### Adrenal Disorders

```python
# Cushing syndrome
cushing = {
    'Etiology': {
        'ACTH-producing pituitary': '70% (Cushing disease)',
        'Ectopic ACTH': '15%',
        'Adrenal adenoma/carcinoma': '15%'
    },
    'Diagnosis': {
        'screening_tests': ['24h UFC', 'Late-night saliva cortisol', 'DST'],
        'localization': ['ACTH level', 'High-dose DST', 'Imaging']
    },
    'clinical_features': [
        'Central obesity', 'Moon face', 'Buffalo hump',
        'Purple striae', 'Hypertension', 'Hyperglycemia',
        'Osteoporosis', 'Psychiatric changes'
    ]
}

# Addison disease
addison = {
    'cause': 'Primary adrenal insufficiency',
    'autoimmune': '70-90% in developed countries',
    'diagnostic_tests': {
        'baseline_cortisol': 'Low',
        'ACTH': 'High',
        'aldosterone': 'Low',
        'adrenal_autoantibodies': 'Often positive'
    },
    'clinical_features': [
        'Fatigue', 'Hyperpigmentation', 'Hypotension',
        'Salt craving', 'Weight loss', 'Nausea'
    ],
    'adrenal_crisis': 'Life-threatening, need stress steroids'
}
```

-----

## Metabolic Syndrome

```python
# Metabolic syndrome criteria (NCEP ATP III)
metabolic_syndrome = {
    'criteria': {
        'waist_circumference': {
            'male': '>102 cm (>40 in)',
            'female': '>88 cm (>35 in)'
        },
        'triglycerides': '≥150 mg/dL',
        'HDL cholesterol': {
            'male': '<40 mg/dL',
            'female': '<50 mg/dL'
        },
        'blood_pressure': '≥130/85 mmHg',
        'fasting_glucose': '≥100 mg/dL'
    },
    'diagnosis': '3 or more criteria',
    'components': [
        'Central obesity',
        'Dyslipidemia',
        'Hypertension',
        'Insulin resistance'
    ],
    'treatment': {
        'lifestyle': 'Weight loss, exercise, diet',
        'pharmacologic': 'Metformin, statins, antihypertensives'
    }
}
```

### Calcium Metabolism

```python
# Calcium regulation
calcium_regulation = {
    'normal_range': '8.5-10.5 mg/dL (2.12-2.62 mmol/L)',
    'ionized_ca': '4.5-5.3 mg/dL (1.12-1.32 mmol/L)',
    
    'parathyroid_hormone': {
        'secretion_trigger': 'Low ionized Ca²⁺',
        'actions': [
            'Increase bone resorption',
            'Increase kidney Ca²⁺ reabsorption',
            'Increase vitamin D activation',
            'Decrease phosphate reabsorption'
        ]
    },
    'calcitonin': {
        'secretion_trigger': 'High Ca²⁺',
        'actions': ['Inhibit bone resorption', 'Increase Ca²⁺ excretion']
    },
    'vitamin_D': {
        'forms': ['D2 (ergocalciferol)', 'D3 (cholecalciferol)'],
        'activation': 'Liver → Kidney (1,25(OH)₂D)',
        'actions': [
            'Increase intestinal Ca²⁺ absorption',
            'Increase bone resorption',
            'Increase kidney Ca²⁺ reabsorption'
        ]
    }
}

# Disorders
hypercalcemia = {
    'causes': ['Primary hyperparathyroidism', 'Malignancy', 'Vitamin D excess'],
    'symptoms': ['Stones', 'Bones', 'Moans', 'Psychiatric'],
    'treatment': ['IV fluids', 'Bisphosphonates', 'Calcitonin', 'Surgery']
}

hypocalcemia = {
    'causes': ['Hypoparathyroidism', 'Vitamin D deficiency', 'Chronic kidney disease'],
    'symptoms': ['Tetany', 'Seizures', 'Arrhythmias', 'Paresthesias'],
    'treatment': ['IV calcium gluconate', 'Vitamin D', 'Calcium supplements']
}
```

-----

## Hormone Replacement Therapy

### Types of HRT

| Type | Indications | Components | Considerations |
|------|------------|------------|----------------|
| **Menopausal** | Menopausal symptoms | Estrogen ± Progesterone | Duration, bleeding |
| **Testosterone** | Hypogonadism | Testosterone | Hematocrit, PSA |
| **Thyroid** | Hypothyroidism | T4 (levothyroxine) | Take on empty stomach |
| **Adrenal** | Addison's | Hydrocortisone + Fludrocortisone | Stress dosing |
| **Growth Hormone** | GHD | Recombinant GH | Monitor IGF-1 |

### Glucocorticoid Replacement

```python
# Glucocorticoid dosing
glucocorticoid_equivalencies = {
    'hydrocortisone': '20 mg',
    'prednisone': '5 mg',
    'prednisolone': '5 mg',
    'dexamethasone': '0.5 mg',
    'methylprednisolone': '4 mg'
}

# Stress dosing protocol
stress_dosing = {
    'minor_illness': 'Double usual dose for 2-3 days',
    'major_stress': '50-100 mg hydrocortisone IV q6h',
    'surgery': '100 mg hydrocortisone IV pre-op, then 50 mg q8h',
    'diarrhea/vomiting': 'IV hydrocortisone, not oral'
}
```

-----

## Laboratory Evaluation

### Endocrine Testing

```python
# Dynamic function tests
dynamic_tests = {
    'ACTH_stimulation_test': {
        'purpose': 'Assess adrenal reserve',
        'method': '250 μg cosyntropin IV',
        'normal': 'Cortisol >18 μg/dL at 30-60 min',
        'interpretation': 'Peak <18 = adrenal insufficiency'
    },
    'CRH_stimulation_test': {
        'purpose': 'Differentiate Cushing causes',
        'method': '1 μg/kg CRH IV',
        'pituitary': 'ACTH and cortisol rise',
        'ectopic': 'No response',
        'adrenal': 'Cortisol rise, no ACTH'
    },
    'Insulin_tolerance_test': {
        'purpose': 'Assess GH and cortisol axis',
        'method': '0.1-0.15 U/kg insulin IV',
        'normal': 'GH >5 μg/L, cortisol >18 μg/dL',
        'contraindications': 'Seizures, heart disease'
    },
    'Oral_glucose_tolerance_test': {
        'purpose': 'Diagnose diabetes, assess insulin resistance',
        'method': '75g glucose PO',
        'diabetes': '2h glucose >200 mg/dL',
        'prediabetes': '140-199 mg/dL'
    }
}

# Hormone reference ranges
reference_ranges = {
    'cortisol': {
        'morning': '5-25 μg/dL',
        'evening': '<10 μg/dL'
    },
    'TSH': '0.4-4.0 mIU/L',
    'free_T4': '0.8-1.8 ng/dL',
    'free_T3': '2.3-4.2 pg/mL',
    'insulin': '2-25 μIU/mL',
    'HbA1c': '<5.6% (normal), 5.7-6.4% (prediabetes), ≥6.5% (diabetes)'
}
```

-----

## Common Errors to Avoid

- **Ignoring feedback loops**: Endocrine systems are tightly regulated; understand the axis
- **Treating lab values in isolation**: Always interpret in clinical context
- **Missing secondary/tertiary causes**: Don't assume primary pathology without testing
- **Overtreating subclinical disease**: Not all abnormal values require intervention
- **Ignoring diurnal variation**: Cortisol, ACTH have circadian rhythms
- **Forgetting drug interactions**: Many medications affect hormone levels
- **Neglecting stress doses**: Patients on chronic steroids need stress coverage
- **Using total instead of free hormones**: Protein binding affects interpretation
- **Assuming thyroid antibodies are always significant**: Context matters
- **Not considering assay limitations**: Different assays have different reference ranges
