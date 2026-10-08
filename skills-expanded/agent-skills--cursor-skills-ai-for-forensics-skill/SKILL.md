# AI for Digital Forensics

## Description

Use ML to detect deepfakes and image forgeries, attribute authorship, and surface anomalies in digital and network forensic evidence.

## When to use

You are verifying digital evidence, detecting synthetic media, or attributing authorship.

## Usage

- Detect GAN- or diffusion-generated deepfakes in images, audio, and video evidence.
- Identify image forgeries such as copy-move, splicing, and compression artifacts.
- Attribute authorship of text, code, or behavioral patterns using stylometry and biometrics.
- Find anomalies in logs, network traffic, or device telemetry that indicate intrusion or tampering.

## Steps

1. Collect and preserve the digital evidence with documented chain of custody and hashing.
2. Extract forensic features (noise, EXIF, compression, artifacts) and run deepfake or forgery detectors.
3. Use source-camera identification and manipulation-localization maps to pinpoint altered regions.
4. Build stylometric or behavioral-biometric models to attribute authorship of suspicious content.
5. Apply anomaly detection to logs and network traffic, correlating events with the media under investigation.
6. Package findings with confidence scores and explainable evidence for legal review and chain-of-custody reporting.

## Code pattern

```python
from transformers import AutoModelForImageClassification, AutoImageProcessor

processor = AutoImageProcessor.from_pretrained("prithivMLmods/Deepfake-vs-Real-8000")
model = AutoModelForImageClassification.from_pretrained("prithivMLmods/Deepfake-vs-Real-8000")
```

## Tuning notes

- Adversarial generators evolve quickly; use ensemble and metadata checks.
- Report confidence and uncertainty; legal evidence needs transparency.
- Maintain chain of custody and avoid altering evidence.

## Verification

1. Build a deepfake detector and test on held-out generation methods.
2. Detect a copy-move forgery in an image.
3. Attribute authorship of a short text and evaluate robustness.

## References

- https://arxiv.org/abs/2404.11163
- https://github.com/grip-unina/TruFor
- https://github.com/polimi-ispl/icpr2020dfdc
- https://pages.nist.gov/frvt/
