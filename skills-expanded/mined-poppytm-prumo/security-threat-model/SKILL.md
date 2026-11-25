---
name: security-threat-model
description: Map system assets, trust boundaries, attacker capabilities, STRIDE threat matrices, and mitigation requirements.
---
# Structured Threat Modeling & STRIDE

## Purpose & Rigor
Map system assets, trust boundaries, attacker capabilities, STRIDE threat matrices, and mitigation requirements.

## Operational Invariants
1. **Academic Rigor & First Principles:** Prioritize formal correctness, proof of termination, memory safety, and algorithmic complexity over convenience.
2. **Deterministic Evidence:** Never declare success without verifiable test, benchmark, or formal audit evidence.
3. **Fail-Closed Security:** In the presence of ambiguity or missing specifications, deny access and reject unsafe operations.
