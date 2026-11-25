---
name: measuring-section-entropy-to-detect-packing
description: 'Detects packing and encryption by measuring Shannon entropy across a binary''s
  sections and regions: flagging high-entropy executable sections, entropy spikes, and
  size/raw-vs-virtual anomalies that indicate compression or encryption. Activates for requests
  to measure entropy, detect packing, or assess whether a sample is compressed/encrypted.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - entropy
  - packing
  - static-analysis
  - pe
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027.002
  - T1027
d3fend:
  - D3-FCR
references:
  - 'Shannon, A Mathematical Theory of Communication (entropy) — https://doi.org/10.1002/j.1538-7305.1948.tb01338.x'
  - 'Microsoft PE/COFF specification — https://learn.microsoft.com/windows/win32/debug/pe-format'
---

# Measuring Section Entropy to Detect Packing

## When to Use

- You want a quick statistical signal of whether a sample is packed or encrypted.
- You are triaging a PE and need to flag suspicious high-entropy executable sections.
- You are deciding whether to route a sample to an unpacking workflow.

**Do not use** entropy as a verdict — legitimate compressed resources and installers also show
high entropy; combine with imports, section names, and raw/virtual size anomalies.

## Prerequisites

- Python (`math` stdlib); optionally `pefile` for per-section analysis.

## Safety & Handling

- Compute entropy on the inert file; never execute the sample.
- Keep the sample password-protected at rest and reference it by hash.

## Workflow

### Step 1: Compute whole-file and sliding-window entropy

Calculate Shannon entropy (0–8 bits/byte). Sliding-window entropy reveals localized
high-entropy regions even when the overall value is moderate.

```bash
python scripts/analyst.py entropy sample.exe
```

### Step 2: Compute per-section entropy (PE)

For each PE section, compute entropy and compare raw vs. virtual size. Executable sections with
entropy > ~7.0 are a packing indicator.

### Step 3: Correlate structural anomalies

Flag classic packer signs: high-entropy `.text`, unusual/renamed sections (`UPX0`, random
names), tiny raw size but large virtual size, and an entry point outside `.text`.

### Step 4: Decide routing

If indicators stack (high entropy + thin IAT + odd sections), route to unpacking; otherwise
proceed with normal static analysis.

## Validation

- High-entropy executable sections are corroborated by other packing signs before concluding.
- Benign high-entropy cases (compressed resources) are not misclassified as packers.
- The routing decision (unpack vs. proceed) is justified by combined indicators.

## Pitfalls

- Calling any high-entropy file "packed" without structural corroboration.
- Ignoring sliding-window entropy and missing a localized encrypted blob.
- Overlooking raw-vs-virtual size mismatch, a strong unpacking-at-runtime hint.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the entropy tool.
- Shannon entropy and the PE/COFF spec (linked in frontmatter).
