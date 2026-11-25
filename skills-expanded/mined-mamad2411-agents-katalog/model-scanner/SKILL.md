---
name: model-scanner
description: ML supply chain security scanner. Scans model files, scores risk (0-100), maps to 5 global compliance frameworks (ISM-2072, EU AI Act, OWASP LLM, MITRE ATLAS, NIST AI RMF), and provides remediation steps. Zero-config, auto-installs scanners. Use when the user asks to scan a model, check if a model is safe, audit ML security posture, check compliance, inspect pickle/safetensors/pytorch files, or mentions model supply chain security. Also trigger on ISM-2072, EU AI Act, OWASP LLM06, model risk score, "is this model safe", "scan my models", "check compliance".
---

# Model Scanner — ML Supply Chain Security

Multi-scanner security analysis with risk scoring and global compliance mapping. Zero configuration.

## How You Should Behave

When this skill triggers, you assess ML model security posture. Not just "scan files" but "inventory, score, map to compliance, and tell them what to fix."

### Step 1: Discover What's Here

Before scanning, explore the workspace for model files and HuggingFace configs:

```bash
find . -type f \( -name "*.pkl" -o -name "*.pt" -o -name "*.pth" -o -name "*.bin" -o -name "*.safetensors" -o -name "*.onnx" -o -name "*.gguf" -o -name "*.joblib" -o -name "*.h5" -o -name "*.npy" \) 2>/dev/null
```

Check `config.json` files for HuggingFace metadata (`_name_or_path`, `trust_remote_code`, `auto_map`).

### Step 2: Run the Scanner

```bash
uv run scripts/scan.py <path-or-hf-model-id> [--verbose] [--json]
```

The script handles everything: auto-installs scanners, discovers files, runs 4 scanners with format-aware routing, calculates risk score, maps to compliance frameworks, and suggests remediation.

### Step 3: Present Results

The scanner output has 5 sections. Present them in order:

1. **Inventory** — what models exist, what formats, which are HuggingFace models
2. **Assessment** — per-file verdicts (MALICIOUS/SUSPICIOUS/SAFE/FORMAT_SAFE)
3. **Risk Score** — 0-100 with breakdown of what caused deductions
4. **Compliance** — PASS/FAIL/WARN against ISM-2072, EU AI Act, OWASP, MITRE, NIST
5. **Remediation** — ordered list of what to fix, most urgent first

Lead with the worst findings. If something is MALICIOUS, say so immediately.

### Step 4: HuggingFace-Specific Advice

When you detect HF models, offer options:
- Scan local files only
- Check HuggingFace for the full model (may have SafeTensors version)
- Compare formats available on HF vs locally

Always flag `trust_remote_code` and `auto_map` — these load arbitrary Python that model scanners don't analyze.

### Step 5: Compliance Questions

When the user asks "are we ISM-2072 compliant" or "EU AI Act" or "OWASP LLM06", read `references/compliance-frameworks.md` for detailed control text and how-to-comply guidance.

## Scanners (4 independent approaches)

| Scanner | Approach | Strength |
|---------|----------|----------|
| **Fickling** | Allowlist + decompiler | Blocks unknown imports by default |
| **ModelScan** | Denylist static | Broadest ML format support |
| **PickleScan** | Denylist static | HuggingFace parity |
| **ModelAudit** | Multi-format static | 42+ formats, config analysis |

Format routing prevents false positives: pickle scanners only run on pickle files, ModelAudit handles configs/safetensors.

## Risk Score

Starts at 100, deducts for risk factors. Bands: 90-100 GOOD, 70-89 MODERATE, 50-69 POOR, 0-49 CRITICAL. Breakdown shows exactly what caused each deduction.

## Compliance Frameworks

Maps every finding to controls across 5 frameworks:
- **ISM** (Australia): ISM-2072, ISM-2086, ISM-2087, ISM-2092
- **EU AI Act**: Article 15 (robustness against model poisoning)
- **OWASP LLM Top 10**: LLM06 (Supply Chain Vulnerabilities)
- **MITRE ATLAS**: AML.T0010 (ML Supply Chain Compromise)
- **NIST AI RMF**: MAP 3.4, MANAGE 2.4, MANAGE 4.1

## Caveats to Always Communicate

1. **No scanner is perfect.** 133 known bypass techniques. Clean scan does not mean safe.
2. **SafeTensors is not complete.** `trust_remote_code` + `auto_map` loads arbitrary Python alongside safe weights.
3. **Compliance requires format change, not just scanning.** ISM-2072 mandates non-executable formats.
4. **Dynamic analysis catches more.** For critical models, recommend [Dyana](https://github.com/dreadnode/dyana).

## References

- `references/scanner-landscape.md` — scanner comparison, bypass techniques, CVE data
- `references/compliance-frameworks.md` — detailed control text, how to comply per framework
