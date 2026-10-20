---
name: llm-text-section-parser-claims-causal-chain
description: Parse a free-form LLM response into structured fields (root cause, category, validated/non-validated claims, causal chain) by splitting on uppercase section headers and stripping bullet markers, with a category whitelist to defend against hallucinated values.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [llm, parsing, structured-output, sections, fallback]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/services/llm_client.py
imported_at: 2026-04-18T00:00:00Z
---

# Free-Form LLM Response Section Parser

## When to use
Your prompt asks the LLM to use a fixed set of `UPPERCASE_HEADER:` sections (e.g. `ROOT_CAUSE:`, `VALIDATED_CLAIMS:`, `CAUSAL_CHAIN:`). You want a deterministic parser that survives missing/reordered sections and small formatting drift, without forcing strict JSON-mode.

## How it works
- Split on `HEADER:` substrings; everything before the next known header belongs to the current section.
- Strip leading bullet markers (`*`, `-`, `•`) and whitespace per line; drop lines that look like another header.
- Validate enum-like fields (`ROOT_CAUSE_CATEGORY:`) against a frozen whitelist; defaults to `"unknown"` on miss.
- Always set safe defaults so a partial response doesn't crash downstream code.

## Example
```python
_VALID_ROOT_CAUSE_CATEGORIES = frozenset({
    "configuration_error", "code_defect", "data_quality",
    "resource_exhaustion", "dependency_failure", "infrastructure",
    "healthy", "unknown",
})

def parse_root_cause(response: str) -> RootCauseResult:
    root_cause = "Unable to determine root cause"
    root_cause_category = "unknown"
    validated_claims, non_validated_claims, causal_chain = [], [], []

    if "ROOT_CAUSE_CATEGORY:" in response:
        after = response.split("ROOT_CAUSE_CATEGORY:")[1]
        for line in after.split("\n"):
            cand = line.strip().lower()
            if cand in _VALID_ROOT_CAUSE_CATEGORIES:
                root_cause_category = cand
                break

    if "ROOT_CAUSE:" in response:
        parts = response.split("ROOT_CAUSE:")[1]
        for delim in ("ROOT_CAUSE_CATEGORY:", "VALIDATED_CLAIMS:",
                      "NON_VALIDATED_CLAIMS:", "CAUSAL_CHAIN:"):
            if delim in parts:
                root_cause = parts.split(delim)[0].strip(); break
        else:
            root_cause = parts.strip()

        if "VALIDATED_CLAIMS:" in parts:
            section = parts.split("VALIDATED_CLAIMS:")[1]
            for delim in ("NON_VALIDATED_CLAIMS:", "CAUSAL_CHAIN:"):
                if delim in section: section = section.split(delim)[0]; break
            for line in section.strip().split("\n"):
                line = line.strip().lstrip("*-• ").strip()
                if line and not any(line.startswith(h) for h in
                                    ("NON_", "CAUSAL_CHAIN", "CONFIDENCE", "ROOT_CAUSE")):
                    validated_claims.append(line)
        # ... same for non_validated_claims and causal_chain ...

    return RootCauseResult(root_cause=root_cause,
                           root_cause_category=root_cause_category,
                           validated_claims=validated_claims,
                           non_validated_claims=non_validated_claims,
                           causal_chain=causal_chain)
```

## Gotchas
- Always validate the category against a whitelist — LLMs love to invent new ones ("partial_failure", "unknown_root_cause").
- Use `frozenset` for the whitelist so it's immutable and the membership check is O(1).
- The line-skip filter ("don't append a line that starts with another header") prevents one section from absorbing another when the LLM omits a delimiter.
- For maximum robustness, prefer this parser as the final layer AFTER attempting JSON parsing — see `structured-output-json-fallback-extractor`.
