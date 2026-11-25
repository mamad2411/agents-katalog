---
name: ai-pii-redaction-review
description: "Privacy-review AI payloads with field-aware redaction, typed stable placeholders, leakage scans across prompts/logs/tools/RAG, and residual-risk reporting before external submission. Use before sending data to cloud LLMs or sharing traces."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-09-11"
tags: ["ai-workflows", "privacy", "pii", "redaction", "gdpr", "hipaa", "dlp", "pseudonymization"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# AI PII Redaction Review AI Skill Guide (Claude)

## Overview & Engine Architecture

Redaction is a **perimeter control**: sensitive data should not reach the provider, the trace store, or the ticket dump in the clear. Regex alone is not anonymization. Pseudonymization with a retained key remains personal data for the controller under GDPR-style regimes—describe outputs as **redacted/pseudonymized**, never “guaranteed anonymous.”

Claude operates as a Principal Privacy Engineer for AI pipelines, specializing in **destination/policy scoping**, **typed stable placeholders**, **reversal-map isolation**, **multi-surface leakage checks**, and **metadata-only audit logs**.

```
┌─────────────────────────────────────────────────────────────┐
│                 PII Redaction Review Stack                  │
│  Policy (allowed classes) → detect → minimize → placeholder │
│  → scan artifacts/meta/logs → restore only at auth boundary │
│  → report categories + residual risk (no raw secrets)       │
└─────────────────────────────────────────────────────────────┘
```

---

## When to use / when not to

**Use when** preparing prompts, RAG chunks, tool outputs, eval fixtures, or support packets for external LLMs or shared logs.  
**Do not use when** unauthorized to view the sample; never ship originals to an external redaction SaaS without approval (prefer **in-perimeter** detection).

---

## Operational Capabilities & Agent Directives

1. Establish **destination**, permitted data classes, task need-to-know, retention, and legal basis/owner before editing.  
2. Inventory: direct identifiers, credentials/secrets, quasi-identifiers in combination, sensitive free text (health, finance, biometrics).  
3. Prefer **local** detectors (e.g. Presidio-class NER + regex) + human field review.  
4. Drop fields not required; use **typed stable placeholders** (`<<EMAIL_1>>`) when relationships matter; keep reversal maps **out of** outgoing payloads and usually **out of disk logs**.  
5. Scan attachments, filenames, EXIF, headers, stack traces, and error messages—not only the main prompt.  
6. Do not put removed values in the deliverable report.

---

## Where to redact (compliance boundary)

| Surface | Action |
| :--- | :--- |
| Outbound LLM/tools | Redact **before** egress |
| RAG ingest | Redact/filter at index time or query time per policy |
| Agent hops | Re-check tool results before next model call |
| Observability | Prefer **metadata + content hash**; avoid raw prompt logs |
| Eval datasets | Redact before commit; `@ai-evaluation-dataset` |

---

## Procedure & checks

1. Minimize → placeholder/mask/hash/encrypt per entity policy (version the policy).  
2. Preserve types the task needs (dates may be generalized, not deleted, if required).  
3. Final scan for known identifiers, API keys, connection strings.  
4. Review false positives that would make the task impossible; document accepted residual risk.  
5. Canary-test detectors (plant synthetic PII; confirm catch rate).

---

## Production sketch

```python
"""Typed placeholder redaction with in-memory reversal map (never ship the map)."""
from __future__ import annotations
import re
from dataclasses import dataclass, field

EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)

@dataclass
class RedactionSession:
    mapping: dict[str, str] = field(default_factory=dict)  # placeholder -> original
    inverse: dict[str, str] = field(default_factory=dict)  # original -> placeholder

    def redact_email(self, text: str) -> str:
        def repl(m: re.Match[str]) -> str:
            val = m.group(0)
            if val not in self.inverse:
                ph = f"<<EMAIL_{len(self.mapping)+1}>>"
                self.inverse[val] = ph
                self.mapping[ph] = val
            return self.inverse[val]
        return EMAIL.sub(repl, text)

    def restore(self, text: str) -> str:
        out = text
        for ph, val in self.mapping.items():
            out = out.replace(ph, val)
        return out
```

Combine with NER for names/phones/addresses; treat credentials as **block**, not mask-and-send.

---

## Troubleshooting

| Signature | Fix |
| :--- | :--- |
| PII in Langfuse/raw logs | Metadata-only audit; hash payload |
| Same person → different placeholders | Stable map per session |
| “Anonymous” claim | Downgrade language; document key custody |
| Leak via filename/PDF metadata | Strip meta; rename files |
| External redact API | Requires explicit approval—prefer local |

---

## Deliverable

Redacted artifact + category-level change summary + residual risks + policy version. No removed values in the report.

## Related skills

`@ai-evaluation-dataset`, `@ai-human-handoff-contract`, `@never-paste-private-passwords`, `@keep-sensitive-financials-private`, `@agent-injection-boundary-test`

## Agent Operational Directive

> **MANDATORY**: Redact in-perimeter before egress. Use stable typed placeholders; isolate reversal maps. Scan all surfaces. Never claim perfect anonymity. Never include secrets in the review report.

## Sources

LLM-Redactor / Presidio-style placeholder restoration; GDPR pseudonymisation guidance; industry practice on metadata-only AI audit logs; self-hosted redaction before provider egress.
