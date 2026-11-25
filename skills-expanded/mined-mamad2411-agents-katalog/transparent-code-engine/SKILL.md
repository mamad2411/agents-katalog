---
name: transparent-code-engine
description: "SBOM, SLSA provenance, Action pin, release integrity. Defense-only TC controls."
---

# GUARDRAIL AKTİF — savunma-only, secret-redakte, exploit-yok

# transparent-code-engine

## Trigger
SBOM, SLSA, provenance, Action SHA pin, supply chain, TC-xxx.

## Hybrid
`references/sbom-slsa.md` + `references/gha-pin-policy.md`

## MODE
ASSESS-ONLY. Supply-chain saldırı simülasyonu / exploit yok.

## Procedure
1. `SECURITY_RESEARCH/supply-chain.md` oku
2. Workflow bağımlılık envanteri
3. Pin/SBOM/provenance gap
4. TC kontrolleri
5. Matrix + tarama

## TODO
20k: CycloneDX örnek pipeline, Scorecard skor yorumu, attestation verify runbook.

## Depth status
Bu tur ~3816 karakter (SKILL+references). **Kalan ~20k hedefe:** ~16184. Sonraki: ek kanonik özet + holding örnekleri (padding yok).
