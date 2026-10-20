---
name: openmed
description: "Production-ready medical NLP toolkit (maziyarpanahi/openmed). Entity extraction, assertion detection, PII de-identification, batch processing, REST API, and multilingual support. Covers installation, all model families, configuration, and deployment."
tags: [medical-nlp, clinical-text, entity-extraction, deidentification, pii, icd10, healthcare, zorai, openmed]
---

# OpenMed

**OpenMed** transforms clinical text into structured insights. It bundles curated biomedical NER models, HIPAA-compliant de-identification, batch processing, a Dockerized REST API, and Apple Silicon acceleration — all behind a single `analyze_text()` call.

## When to Use

| Scenario | Start with |
|---|---|
| Extract diseases, drugs, anatomy from clinical notes | `references/entity-extraction` |
| Remove PHI/PII before sharing or storing data | `references/pii-deidentification` |
| Run NER on hundreds of clinical documents | `references/batch-processing` |
| Serve OpenMed behind a REST API | `references/rest-service` |
| Set up on Apple Silicon, Docker, or Swift | `references/installation` |
| Configure profiles, pick the right model | `references/configuration` |
| PII in French, German, Spanish, Portuguese, etc. | `references/multilingual-pii` |
| Privacy Filter (OpenAI / Nemotron) families | `references/privacy-filter` |

## Quick Start

```bash
git clone https://github.com/maziyarpanahi/openmed.git
cd openmed
uv pip install -e ".[hf]"
```

```python
from openmed import analyze_text

result = analyze_text(
    "Patient started imatinib for chronic myeloid leukemia.",
    model_name="disease_detection_superclinical",
)
for entity in result.entities:
    print(f"{entity.label:<12} {entity.text:<35} {entity.confidence:.2f}")
# DISEASE      chronic myeloid leukemia          0.98
# DRUG         imatinib                           0.95
```

## Model Registry (12+ Models)

| Model | Entity Types |
|---|---|
| `disease_detection_superclinical` | DISEASE, CONDITION, DIAGNOSIS |
| `pharma_detection_superclinical` | DRUG, MEDICATION, TREATMENT |
| `pii_detection_superclinical` | NAME, DATE, SSN, PHONE, EMAIL, ADDRESS |
| `anatomy_detection_electramed` | ANATOMY, ORGAN, BODY_PART |
| `gene_detection_genecorpus` | GENE, PROTEIN |

Browse the full catalog: `openmed.life/docs/model-registry`

## Key Concepts

- **analyze_text()** — single-call inference with configurable model, aggregation, format, and confidence threshold
- **BatchProcessor** — multi-text and multi-file workflows with progress tracking
- **extract_pii()** / **deidentify()** — HIPAA-compliant PII detection and redaction
- **Configuration Profiles** — `dev`, `prod`, `test`, `fast` presets via YAML or env vars
- **REST API** — FastAPI endpoints: `/health`, `/analyze`, `/pii/extract`, `/pii/deidentify`

## References

- [OpenMed docs](https://openmed.life/docs/)
- [OpenMed arXiv paper](https://arxiv.org/abs/2508.01630)
- [OpenMed GitHub](https://github.com/maziyarpanahi/openmed)
- `references/installation.md` — cross-platform install, Docker, Swift
- `references/entity-extraction.md` — disease, drug, anatomy, gene models
- `references/pii-deidentification.md` — HIPAA compliance, smart merging, anonymization
- `references/batch-processing.md` — BatchProcessor API
- `references/rest-service.md` — FastAPI endpoints, Docker
- `references/configuration.md` — profiles, model registry, profiling
- `references/multilingual-pii.md` — 9-language PII support
- `references/privacy-filter.md` — OpenAI Privacy Filter, Nemotron, MLX
