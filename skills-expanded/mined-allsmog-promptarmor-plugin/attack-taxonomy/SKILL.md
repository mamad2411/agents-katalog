---
name: Attack Taxonomy
description: Complete taxonomy of 80+ attack plugins organized by category, technique, and OWASP mapping
version: 1.0.0
---

# Attack Taxonomy

## Purpose

Provides a structured classification of all PromptArmor attack plugins. Used by agents to understand what attacks are available, how they work, and which vulnerabilities they target.

## When to Use

- When planning which attacks to run
- When explaining findings to users
- When mapping attacks to OWASP or compliance frameworks
- When selecting mutation strategies

## Attack Categories

| Category | Count | Techniques |
|----------|-------|------------|
| **Jailbreak** | 13 | Direct instruction bypass, persona switching, encoding, delimiter injection, context manipulation |
| **Injection** | 5 | Direct prompt injection, indirect injection via content, context compliance, system override |
| **Tool Abuse** | 12 | SQL injection, SSRF, file access, code execution, privilege escalation, data exfiltration |
| **Harmful** | 18 | Violence, crime, hate speech, self-harm, drugs, weapons, cybercrime, misinformation |
| **Bias** | 5 | Age, gender, race, disability, religion discrimination |
| **PII** | 4 | Direct disclosure, session leaks, social engineering, database leaks |
| **Compliance** | 4 | HIPAA, COPPA, FERPA, GDPR violations |
| **Agentic** | 3 | Memory poisoning, cross-session leaks, goal misalignment |
| **RAG** | 3 | Document exfiltration, source attribution, context poisoning |
| **Other** | 13+ | Hallucination, imitation, contracts, competitors, debug access, DoS |

## Reference Files

- [Jailbreak Techniques](references/jailbreak-techniques.md)
- [Injection Patterns](references/injection-patterns.md)
- [Tool Abuse Vectors](references/tool-abuse-vectors.md)
- [Encoding Mutations](references/encoding-mutations.md)
