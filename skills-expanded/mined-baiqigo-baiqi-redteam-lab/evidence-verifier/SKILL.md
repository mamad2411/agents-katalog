---
name: evidence-verifier
description: Verify artifact integrity, provenance, reproduction, and proof links before graph promotion. Use when a supervisor assigns capabilities: evidence.verify.
license: project
compatibility: OpenTgtyLab Worker Protocol v1; manifest evidence.verifier@1.0.0.
metadata:
  open-tgtylab-id: evidence.verifier
  version: 1.0.0
  digest: 7aec5da2dca6619815584e206b8520e1f3e5bf4696c6c0bd3f666ac4190d2720
allowed-tools: artifact.read
---

# Evidence Verifier Procedure

1. Resolve every artifact inside the Case evidence boundary. Finish when path, size, and SHA-256 match or the artifact is rejected.
2. Trace each claim to its producing task, run, revision, and observation. Finish when every accepted claim has a complete provenance chain.
3. Apply redaction and reproducibility requirements. Finish when credential-bearing evidence is rejected or represented only by a redacted classification.
4. Return promotion decisions for each claimed graph edge and proof condition. Finish when no claim remains implicit.

## Contract

Return `schemas/worker-result-v1.schema.json`. Echo skill ID `evidence.verifier`, version `1.0.0`, and digest `7aec5da2dca6619815584e206b8520e1f3e5bf4696c6c0bd3f666ac4190d2720` through the assigned task anchors.
