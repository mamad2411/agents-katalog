---
name: canva-export-pipeline
description: Export workflow — format, quality, naming, VALIDATION.log.
---

# Canva Export Pipeline

## When to use
Onaylı design → final asset export.

## Steps
1. Export format (PNG/JPG/MP4) kanal spec'e göre
2. Naming: `{campaign}_{channel}_{ratio}_{version}.{ext}`
3. `CANVA_OPS/exports/`
4. `scripts/spec_validate.py` post-export
5. Registry status = exported

## References
- `CANVA_OPS/DESIGN_REGISTRY.csv`
