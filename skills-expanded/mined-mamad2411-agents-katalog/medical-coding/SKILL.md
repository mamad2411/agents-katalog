---
name: medical-coding
description: "Medical code mapping and classification tools. ICD-10-CM/PCS, CPT, SNOMED CT, HCPCS, LOINC, RxNorm. Code validation, mapping between terminologies, HCC risk adjustment, and reimbursement modeling."
tags: [icd10, cpt, snomed, loinc, medical-coding, hcc, reimbursement, zorai]
---
## Overview

Medical code mapping and classification: ICD-10-CM/PCS, CPT, SNOMED CT, HCPCS, LOINC, RxNorm. Covers code validation, cross-terminology mapping, HCC risk adjustment, and reimbursement modeling used in healthcare billing and clinical research.

## ICD-10 to HCC Mapping

```python
hcc_map = {
    "E11.9": "HCC 19",   # Diabetes without complications
    "I10": "HCC 134",    # Essential hypertension
    "N18.3": "HCC 138",  # CKD stage 3
}

def calc_hcc(codes):
    hccs = set()
    for c in codes:
        if c in hcc_map:
            hccs.add(hcc_map[c])
    return list(hccs)

print(calc_hcc(["E11.9", "I10"]))
```

## Code Validation

```python
valid_icd10 = set()  # from official CMS file or lookup

def validate_code(code):
    if code in valid_icd10:
        return True, "Valid"
    if code[:3] in valid_icd10:
        return True, "Valid (category)"
    return False, "Unknown code"
```

## References
- [CMS ICD-10](https://www.cms.gov/medicare/coding/icd10)
- [SNOMED CT](https://www.snomed.org/)
- [HCC coding](https://www.cms.gov/medicare/health-plans/medicareadvtgspecratestats/risk-adjustors)