---
name: image-forensics
description: Use when checking whether an image is a real camera capture or synthetic/generated, when tagging media provenance before ingestion, when verifying visual evidence for fact-check, or when validating that ai3d-gen source photos are real captures before splatting. Covers PRNU noise-residual forensics, EXIF/XMP/C2PA first pass, and PCE scoring via extensions/image-forensics.
---

# Image Forensics

Cheap image provenance: real-vs-synthetic plus "which camera took this".
Route: `extensions/image-forensics/verdict.py` — JSON contract
`{ok, verdict, pce, metadata_flags, notes}`.

## Evidence ordering (always in this order)

1. **Metadata first pass** — `metadata.py`: EXIF/XMP/C2PA report.
   Generator tags (`stable diffusion`, `dall-e`, ...) or a C2PA manifest
   are fast signals. Absence of EXIF is NOT evidence of synthesis:
   metadata dies on screenshot/re-upload; pixel noise does not.
2. **Noise residual** — `prnu.residual`: denoise (wavelet via PyWavelets
   when installed, Gaussian fallback) and subtract; the remainder is the
   fingerprint candidate.
3. **Reference pattern** — `verdict.py --build-ref dir/ --out ref.npy`
   averages residuals of N flat-ish real photos from one device.
4. **PCE score** — `prnu.pce`: peak-to-correlation-energy of residual vs
   reference. Goljan's empirical band ~50-60 discriminates; calibrate on
   the local dataset, never treat thresholds as universal.
5. **Verdict**: `real_capture` / `synthetic` / `inconclusive` /
   `no_reference` + flags + notes.

## Abstain rules

- Residual energy below the denoiser floor (flat or heavily recompressed
  input) -> `inconclusive`, note `low_residual_energy`.
- Heavy crop/resize/recompression weakens the signal; say so in notes.
- Never claim provenance from a single signal: combine metadata flags +
  residual + PCE. For publication, pair with `fact-check`.
- No camera reference available -> `no_reference`; build one or abstain.

## Commands

```bash
python extensions/image-forensics/verdict.py shot.jpg --ref ref.npy
python extensions/image-forensics/verdict.py --build-ref known_phone/ --out ref.npy
python extensions/image-forensics/metadata.py shot.jpg
```

## Integrations

- `ai3d-gen` preflight: source images should verify as real captures
  before the splat pipeline (synthetic inputs break PRNU assumptions).
- `fact-check`: visual-evidence tagging.
- PPISP (`extensions/ppisp-prep`) models complementary per-camera
  photometrics (exposure/vignette/CRF) — provenance vs correction answer
  different questions; do not conflate.
