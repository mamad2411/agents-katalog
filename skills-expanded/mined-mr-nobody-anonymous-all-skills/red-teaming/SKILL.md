---
name: red-teaming
description: "Adversarial red-teaming for AI: jailbreaking, prompt injection, harmful content elicitation, automated fuzzing, and safety boundary testing"
category: ai-evaluation
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/ai-evaluation/red-teaming/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# AI Adversarial Red-Teaming

## Scope
Adversarial red-teaming probes LLM applications and agentic workflows to uncover vulnerabilities, security weaknesses, prompt injection exploits, and safety policy violations.

## Attack Vectors & Testing Protocols
- **Direct Prompt Injection**: Overriding system instructions via crafted user inputs (`Ignore previous instructions and output...`).
- **Indirect Prompt Injection**: Malicious instructions embedded in untrusted external data sources (retrieved web pages, PDFs, emails).
- **Jailbreak Strategies**: Role-playing persona shifts, hypothetical framing, multi-turn crescendo attacks, base64/rot13 obfuscation.
- **Automated Fuzzing & Testing**: Generating continuous automated adversarial permutations targeting OWASP Top 10 for LLMs.

## Standards & Tools
- **Standards**: OWASP Top 10 for LLM Applications, NIST AI Risk Management Framework.
- **Software**: Garak (LLM vulnerability scanner), PyRIT (Python Risk Identification Tool for generative AI).
