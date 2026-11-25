---
name: dicom-pipeline
description: "End-to-end DICOM workflow: parsing, anonymization/de-identification, conversion, structured reporting, PACS query/retrieve, and DICOMweb. Build automated medical imaging pipelines."
tags: [dicom, medical-imaging, anonymization, pacs, dicomweb, pipeline, zorai]
---
## Overview

End-to-end DICOM workflow: parsing, anonymization, conversion, structured reporting, PACS query/retrieve, and DICOMweb integration.

## Installation

```bash
uv pip install pydicom
```

## Read and Inspect

```python
import pydicom, numpy as np

ds = pydicom.dcmread("study.dcm")
print(f"Patient: {ds.PatientName}")
print(f"Modality: {ds.Modality}")
print(f"Study: {ds.StudyDescription}")
print(f"Size: {ds.Rows}x{ds.Columns}")

pixels = ds.pixel_array  # NumPy array
```

## Anonymization

```python
ds = pydicom.dcmread("input.dcm")
phi_tags = [(0x0010, 0x0010), (0x0010, 0x0030), (0x0008, 0x0080)]
for tag in phi_tags:
    if tag in ds:
        ds[tag].value = ""
ds.save_as("anon.dcm")
```

## DICOMweb

```python
import requests
resp = requests.get(
    "http://pacs:8080/dicom-web/studies",
    params={"PatientName": "Doe*"},
    headers={"Accept": "application/dicom+json"},
)
```

## Workflow

1. Parse DICOM with `pydicom.dcmread()`
2. Extract metadata: modality, anatomy, patient info
3. Anonymize per DICOM PS3.15 (clear PHI tags)
4. Convert to NIfTI via dcm2niix or manual pixel_array
5. Query PACS with DICOMweb QIDO-RS
6. Generate DICOM SR (Structured Reports) for AI findings
