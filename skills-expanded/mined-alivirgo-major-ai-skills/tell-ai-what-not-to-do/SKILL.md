---
name: tell-ai-what-not-to-do
description: "State relevant exclusions and forbidden approaches when they materially constrain the deliverable."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["negative-constraints", "guardrails", "prompt-engineering", "pruning", "precision", "safety"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Tell AI What NOT to Do (Negative Constraint Engineering) (AI Skill)

## Overview
Defining only what you *want* (*"Write a login script"*) leaves 90% of the possibility space undefined - inviting the AI to import unnecessary third-party libraries, write 50 lines of boilerplate, or invent complex dependencies.

**Negative Constraint Engineering** prunes the model's search space by explicitly outlawing forbidden libraries, cliché words, unneeded complexity, and structural anti-patterns.

---

## Positive Directives vs. Negative Boundary Pruning

```
┌─────────────────────────────────────────────────────────────┐
│                 Negative Boundary Pruning                   │
│                                                             │
│  Positive Command Only ("Write a sorting algorithm"):       │
│  • AI might import external libraries, write O(N^2) bubblesort,│
│    or wrap it in an unnecessary class.                      │
│                                                             │
│  Positive + Negative Guardrails:                            │
│  "Write a sorting function in Python.                       │
│   ❌ DO NOT import external packages (standard lib only)    │
│   ❌ DO NOT use recursion (must be iterative)               │
│   ❌ DO NOT modify the original input array in-place"       │
│  • Result: Laser-targeted, exact implementation on Turn 1   │
└─────────────────────────────────────────────────────────────┘
```

---

## The 4-Category Negative Constraint Matrix

| Category | High-Yield Negative Constraint Example | Why It Prevents Failure |
| :--- | :--- | :--- |
| **1. Vocabulary & Style** | *"Do NOT use 'delve', 'tapestry', 'testament', or 'in today's world'."* | Eliminates tell-tale synthetic AI voice. |
| **2. Technical Dependencies**| *"Do NOT use external NPM/PyPI packages; use standard library only."* | Prevents dependency bloat & supply chain bloat. |
| **3. Architecture / Logic** | *"Do NOT use recursion, global variables, or mutable default arguments."* | Prevents stack overflows and race conditions. |
| **4. Formatting & Chat** | *"Do NOT include conversational preambles or sign-offs."* | Eliminates manual copy-paste cleanup. |

---

## Master Negative Constraint Prompt Templates

### Pattern 1: The Zero-Bloat Technical Directive

```markdown
Write a [FUNCTION / SCRIPT] in [LANGUAGE] to [TASK].

Negative Constraints (Strictly Prohibited):
- ❌ Do NOT use external third-party dependencies.
- ❌ Do NOT use deprecated APIs or syntax.
- ❌ Do NOT hardcode file paths or API credentials.
- ❌ Do NOT leave placeholder comments (e.g. `# TODO: add error handling here`). Write the complete error handling.
```

---

### Pattern 2: The Executive Communication Guardrail

```markdown
Draft a response to [CLIENT / EXECUTIVE].

Prohibited Elements:
- ❌ No apologies or self-deprecating phrasing ("Sorry for the delay").
- ❌ No corporate filler ("Hope you are having a wonderful quarter").
- ❌ No vague commitments ("We will look into this soon"). State exact dates.
```

---

## Real-World Case Study

### Scenario: Parsing JSON in a Lightweight AWS Lambda Function

#### Without Negative Constraints (Bloated Output)
> **Prompt**: *"Write a Python script to parse a nested JSON config and validate required keys."*
> ❌ *Model imports `pydantic` and `pandas` - requiring you to build and upload a 50MB Lambda layer for a simple 10-line task.*

#### With Negative Constraints (Zero-Dependency Perfection)
> **Prompt**: *"Write a Python script to validate required keys in a JSON config. **Do NOT import pydantic, pandas, or any third-party package; use native Python 3.12 standard library only.**"*

**AI Output**:
```python
from typing import Dict, Any, List

REQUIRED_KEYS = {"user_id", "email", "subscription_tier"}

def validate_config(payload: Dict[str, Any]) -> List[str]:
    """Validates required keys using pure standard library with zero external packages."""
    if not isinstance(payload, dict):
        return ["Payload must be a valid dictionary"]
        
    missing_keys = [key for key in REQUIRED_KEYS if key not in payload or payload[key] is None]
    return [f"Missing required key: '{k}'" for k in missing_keys]
```

---

## Summary Best Practices
- **Use the "❌ DO NOT" bullet pattern**: Visual negation symbols (`❌`, `DO NOT`) receive strong attention weights in modern LLMs.
- **Pair positive intent with negative guardrails**: *"Build X, but do NOT do Y."*
