---
name: llm-security-review
description: Audit an LLM system for security — OWASP LLM Top 10, direct/indirect prompt injection, sensitive-data leakage, insecure output handling, RAG and agent-action risks.
---

# llm-security-review

> An LLM turns every input channel — user text, retrieved docs, tool output — into a potential instruction. Review the whole data path for where untrusted text becomes action or leaks data.

## When to use

- Auditing an LLM-backed feature, RAG system, or agent for security before/after launch.
- Reviewing whether `llm-guardrails` controls are sufficient against the actual threat surface.
- A workflow invokes `polymath-security:llm-security-review`.

Not this when: you are *designing* the controls — that is `polymath-ai:llm-guardrails` (this skill audits a system, that one builds the defenses). For agent loop/stop design, `polymath-ai:agent-design`. For classic app vulns, `owasp-review`.

## Inputs

- The LLM system's data flow: inputs, retrieval sources, tools/actions, outputs, and who/what consumes them.
- Privileges the model can exercise.

## Procedure

1. **Map the attack surface** against the OWASP Top 10 for LLM Applications, walking the data path end to end.
2. **Prompt injection — direct**: can user input override the system prompt or extract it? Test instruction-override, role-play escapes, and delimiter breaking.
3. **Prompt injection — indirect**: can retrieved documents, tool results, or third-party content carry instructions the model will follow? This is the most-missed class — treat all retrieved/tool content as untrusted.
4. **Sensitive-data disclosure**: can the model leak secrets, other users' data, PII, or its system prompt? Check what's in context and what retrieval can reach (tenant isolation).
5. **Insecure output handling**: is model output trusted downstream (rendered as HTML→XSS, run as SQL/shell, used as a URL→SSRF)? Output must be treated as untrusted and validated.
6. **Excessive agency**: what actions can the model trigger, and is any irreversible/high-impact action authorized by model output alone? Confirm privilege separation (model proposes, code authorizes).
7. **Supply chain & model**: provenance of models/plugins/training data; for RAG, poisoning of the knowledge base.
8. **DoS / cost abuse**: unbounded loops, token-flooding, recursive tool calls — confirm rate/cost limits.
9. **Cross-check the defenses** against `polymath-ai:llm-guardrails`; each finding names a mitigation + owner.

## Output

- A findings report keyed to the OWASP-LLM categories: each finding has the attack path, severity, a proof-of-concept sketch, and a mitigation + owner; plus an overall risk verdict.

## Quality bar

- Indirect prompt injection (via retrieval/tool content) is explicitly assessed, not just direct.
- Output-handling sinks (HTML/SQL/shell/URL) are checked for trusting model output.
- Every action the model can trigger is checked for the propose-vs-authorize split.
- Each finding has a severity, an attack path, and a named mitigation.
