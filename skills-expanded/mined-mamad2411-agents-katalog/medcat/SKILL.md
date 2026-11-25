---
name: medcat
description: "Medical Concept Annotation Toolkit. Trainable NLP for extracting clinical concepts from unstructured text. Supports ICD-10, SNOMED CT, RxNorm, UMLS. Active learning for custom medical ontologies."
tags: [clinical-nlp, medical-entity-extraction, icd10, snomed, umls, healthcare, zorai]
---
## Overview

MedCAT trains NLP models for extracting clinical concepts from unstructured text. Supports ICD-10, SNOMED CT, RxNorm, UMLS, and custom ontologies with active learning.

## Installation

```bash
uv pip install medcat
```

## Pre-trained Model

```python
from medcat.cat import CAT

cat = CAT.load_model_pack("medcat_model_pack.dat")
text = "Patient with type 2 diabetes and hypertension, prescribed metformin 500mg BID."
doc = cat(text)

for entity in doc.entities:
    print(f"{entity.name:<25} {entity.cui:<10} confidence={entity.confidence:.2f}")
# type 2 diabetes           D003920    confidence=0.97
# hypertension              D006973    confidence=0.99
```

## Active Learning

```python
cat.add_cui_to_category("D003920", "Diabetes Mellitus")
cat.train(text="Patient has diabetes", cui="D003920", value="Diabetes Mellitus")
unmatched = cat.get_unmatched_concepts()  # concepts needing review
```

## Workflow

1. Load a pre-trained model pack
2. Annotate clinical text -> extract UMLS CUIs
3. Map concepts to ICD-10/SNOMED/RxNorm
4. Train with active learning: correct errors, add concepts
5. Export and deploy trained model
