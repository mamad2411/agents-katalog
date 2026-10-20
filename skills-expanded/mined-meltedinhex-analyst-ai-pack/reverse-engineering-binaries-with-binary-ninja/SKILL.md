---
name: reverse-engineering-binaries-with-binary-ninja
description: 'Reverse engineers binaries with Binary Ninja using its analysis stack and Python API
  to enumerate functions, navigate IL levels (LLIL/MLIL/HLIL), and automate annotation and
  extraction. Activates for requests to reverse a binary with Binary Ninja, script the Binary Ninja
  API, or work with its intermediate languages.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - binary-ninja
  - il
  - automation
  - static-analysis
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
  - T1059
  - T1587.001
d3fend:
  - D3-DA
  - D3-SDA
references:
  - 'Binary Ninja Python API documentation — https://api.binary.ninja/'
  - 'Binary Ninja IL (LLIL/MLIL/HLIL) guide — https://docs.binary.ninja/dev/bnil-llil.html'
---

# Reverse Engineering Binaries With Binary Ninja

## When to Use

- You want to reverse a binary with Binary Ninja and automate analysis via its Python API
  (function enumeration, IL traversal, annotation, extraction).
- You need to leverage MLIL/HLIL for cleaner analysis of obfuscated code.

**Do not use** the headless API to execute the sample — Binary Ninja performs static analysis. Run
in an isolated environment and treat inputs as malicious.

## Prerequisites

- Binary Ninja with the `binaryninja` Python API available (the script degrades gracefully and
  generates a script skeleton if the API is not importable).

## Safety & Handling

- Static analysis does not execute the sample; keep inputs isolated.

## Workflow

### Step 1: Generate an analysis script skeleton

```bash
python scripts/analyst.py skeleton --emit functions,strings --out bn_extract.py
```

Emits a Binary Ninja Python script that opens a view, iterates functions, and exports
functions/strings to JSON using the real API (`open_view`, `bv.functions`, `bv.get_strings`).

### Step 2: Choose the IL level

Use LLIL for close-to-assembly, MLIL for variable/SSA reasoning, and HLIL for readable
pseudo-code; traverse instructions and operands programmatically.

### Step 3: Automate annotation

Rename symbols (`func.name`), add comments (`bv.set_comment_at`), and create tags for findings.

### Step 4: Run and aggregate

Execute the script (headless or in the UI console) and aggregate the JSON output.

## Validation

- The skeleton uses real API calls (`binaryninja.open_view`, `bv.functions`).
- The chosen IL level matches the analysis goal.
- Exported JSON contains plausible functions/strings.

## Pitfalls

- Headless licensing differences (Commercial vs Personal) affecting `open_view` availability.
- Confusing IL levels and operand structures across LLIL/MLIL/HLIL.
- Long analysis times on large binaries — scope function ranges.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the skeleton generator.
- Binary Ninja API and IL docs (linked in frontmatter).
