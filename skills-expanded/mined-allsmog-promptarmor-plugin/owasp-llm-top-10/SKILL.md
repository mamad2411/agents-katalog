---
name: OWASP LLM Top 10
description: Comprehensive knowledge of the OWASP Top 10 for LLM Applications (2025), including attack mappings, detection methodology, and remediation checklists
version: 1.0.0
---

# OWASP LLM Top 10 Reference

## Purpose

Provides expert knowledge of the OWASP Top 10 for Large Language Model Applications. Used by agents to understand vulnerability categories, map attacks to standards, and produce standards-aligned reports.

## When to Use

- When mapping scan findings to industry standards
- When producing compliance reports
- When prioritizing vulnerabilities
- When the user asks about OWASP LLM categories
- During attack planning to ensure coverage

## Categories

| ID | Name | PromptArmor Coverage |
|----|------|---------------------|
| LLM01 | Prompt Injection | jailbreak (13), injection (5) |
| LLM02 | Insecure Output Handling | other:hijacking, tool-abuse |
| LLM03 | Training Data Poisoning | rag:poisoning |
| LLM04 | Model Denial of Service | other:reasoning-dos, other:divergent-repetition |
| LLM05 | Supply Chain Vulnerabilities | — (out of scope for red teaming) |
| LLM06 | Sensitive Information Disclosure | pii (4), harmful:privacy-violation |
| LLM07 | Insecure Plugin Design | tool-abuse (12), agentic (3) |
| LLM08 | Excessive Agency | agentic:goal-misalignment, tool-abuse:privilege-escalation |
| LLM09 | Overreliance | other:hallucination, other:overreliance |
| LLM10 | Model Theft | — (infrastructure concern, not red team testable) |

## Reference Files

- [LLM01 - Prompt Injection](references/llm01-prompt-injection.md)
- [LLM02 - Insecure Output Handling](references/llm02-insecure-output.md)
- [LLM03 - Training Data Poisoning](references/llm03-training-data-poisoning.md)
- [LLM04 - Model Denial of Service](references/llm04-model-dos.md)
- [LLM05 - Supply Chain Vulnerabilities](references/llm05-supply-chain.md)
- [LLM06 - Sensitive Information Disclosure](references/llm06-sensitive-info.md)
- [LLM07 - Insecure Plugin Design](references/llm07-insecure-plugin.md)
- [LLM08 - Excessive Agency](references/llm08-excessive-agency.md)
- [LLM09 - Overreliance](references/llm09-overreliance.md)
- [LLM10 - Model Theft](references/llm10-model-theft.md)
