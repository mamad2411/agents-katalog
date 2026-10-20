---
name: ask-ai-to-audit-itself
description: "Review a draft answer for logical errors, missing requirements, edge cases, and claims needing external verification."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["self-audit", "reflexion", "critic-actor", "verification", "code-review", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Ask AI to Audit Its Own Output (AI Skill)

## Overview
When an AI generates a long response in a single generation pass, it cannot "look ahead" to revise earlier sentences based on later logical deductions. As a result, drafts often contain subtle internal contradictions, forgotten constraints, or code bugs that the model would easily catch if asked to review them as a third party.

This skill implements the **Reflexion / Critic-Actor Prompting Protocol** - a technique that separates *generation* from *critique* to dramatically elevate accuracy and quality.

---

## The 3-Stage Reflexion Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 The Critic-Actor Pipeline                   │
│                                                             │
│  Step 1: ACTOR       ──► Draft initial solution             │
│            │                                                │
│  Step 2: CRITIC      ──► Adversarial audit against strict   │
│            │             rubric (find 3 flaws/edge cases)   │
│            │                                                │
│  Step 3: SYNTHESIZER ──► Output final refined version with  │
│                          all audited flaws resolved         │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Audit Prompts

### Pattern 1: The "Adversarial Code & Logic Audit"
Use this prompt immediately after an AI provides a code snippet or architectural plan:

```markdown
Now, switch personas. Act as a Principal Security and Performance Reviewer.

Critically audit your code/solution above against these 4 criteria:
1. **Edge Cases**: Where will this fail (null values, concurrency race conditions, unexpected formats)?
2. **Performance & Scalability**: Is there any O(N^2) bottleneck, memory leak, or redundant compute?
3. **Security Vulnerabilities**: Are there injection risks, unsafe inputs, or missing validations?
4. **Constraint Adherence**: Did the draft violate any original prompt requirements?

List any flaws found. If flaws exist, provide the corrected, production-ready version.
```

---

### Pattern 2: The "Editorial & Consistency Audit"
Use this for articles, contracts, reports, and documentation:

```markdown
Read through the text you just drafted. Audit it strictly for:
1. Internal factual or mathematical contradictions between sections.
2. Passive, repetitive, or vague statements.
3. Unanswered questions or vague hand-waving (e.g., "implement appropriate logic here").

Output a bulleted "Changelog of Fixes" followed by the finalized, corrected text.
```

---

## Real-World Examples

### Example 1: Auditing an Ingestion Script

#### Initial Generation (Actor Pass)
```python
def process_user_records(records):
    results = []
    for r in records:
        data = r['profile']
        results.append(data['email'].lower())
    return results
```

#### The Audit Prompt & Self-Correction
> **User**: *"Audit the function above for runtime exceptions in production."*
>
> **AI Self-Audit**:
> **Flaws Identified**:
> 1. `KeyError`: Will crash if `r` lacks `'profile'` or `'profile'` lacks `'email'`.
> 2. `AttributeError`: Will crash if `email` is `None`.
> 3. `TypeError`: Will fail if `records` is `None` or not iterable.
>
> **Corrected Production Version**:
```python
from typing import List, Dict, Any

def process_user_records(records: List[Dict[str, Any]] | None) -> List[str]:
    if not records:
        return []
    
    valid_emails = []
    for r in records:
        if not isinstance(r, dict):
            continue
        profile = r.get('profile')
        if isinstance(profile, dict):
            email = profile.get('email')
            if isinstance(email, str) and email.strip():
                valid_emails.append(email.strip().lower())
                
    return valid_emails
```

---

### Example 2: One-Turn Multi-Pass Audit (Self-Correction Prompt)
You don't always need two separate chat turns. You can instruct the model to perform the audit internally:

```markdown
Solve the following logic problem: [INSERT PROBLEM]

Follow this multi-pass structure in your response:
### Pass 1: Initial Solution & Reasoning
[Work through the problem step-by-step]

### Pass 2: Adversarial Self-Audit
[Test the solution with extreme boundary inputs and double-check all arithmetic]

### Pass 3: Final Verified Answer
[State the confirmed solution]
```

---

## Critical Rules & Anti-Patterns

| Don't Do (Weak Habit) | Do Instead (Master Skill) | Why |
| :--- | :--- | :--- |
| Asking *"Is this correct?"* | Asking *"Find 3 hidden edge cases or bugs in your solution."* | Models tend to be sycophantic and will agree with themselves if asked passively. |
| Auditing in a giant single block | Separating critique from the final output draft | Forcing the critique step into the context window ensures the final tokens incorporate the fixes. |
| Skipping domain rubrics | Supplying explicit checklists (Security, Nulls, Math) | Directed rubrics activate targeted safety and verification paths in the LLM. |
