---
name: ai-security
description: "Covers securing AI/LLM systems: the AI-specific attack surface (prompt injection, RAG poisoning, agent tool abuse), model supply chain, controls that hold, and the governance anchors ISO 42001, NIST AI RMF and the OWASP LLM and Agentic Top 10. Use when the user asks how to secure an LLM app, chatbot, RAG pipeline or AI agent, about prompt injection or jailbreak risk, model/weights provenance, or AI security governance."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# AI/LLM Security

Two jobs, often confused: **securing AI systems you build or buy**, and
**governing AI use** so it is defensible. Regulatory obligations for the EU
market are a separate skill: `load_skill eu-ai-act`.

The governing intuition: an LLM **cannot reliably separate instructions from
data**. Everything it reads (a document, a web page, a tool result, another
agent's output) is potential instruction. Design as if the model will do the
worst thing its permissions allow, because a sufficiently clever input can make
it try.

## The attack surface

- **Prompt injection (direct)**: the user talks the model past its system
  prompt. **Indirect**: the payload rides in content the model _retrieves_: a
  web page, PDF, ticket, email, code comment. Indirect is the dangerous one; the
  attacker never touches your UI.
- **RAG / knowledge-base poisoning**: attacker-controlled content lands in the
  index and is later retrieved as trusted context. Whoever can write to the
  corpus can write to the prompt.
- **Tool / agent abuse**: the main blast radius. An agent with shell, HTTP, or
  DB tools turns a text exploit into an action. Consider the **lethal trifecta**:
  private data access + exposure to untrusted content + ability to exfiltrate.
  Any two are usually survivable; all three is an exfil channel by design.
- **Excessive agency**: over-broad tool scopes, standing credentials, no
  confirmation on irreversible actions.
- **Sensitive-information disclosure**: secrets in system prompts, PII in
  training data or logs, cross-tenant leakage via a shared vector store.
- **Model supply chain**: untrusted weights from a hub, pickle-deserialisation
  RCE in checkpoints, typosquatted model/package names, poisoned fine-tune data.
- **Output handling**: model output rendered as HTML, passed to `eval`, or run
  as SQL/shell. Classic injection with a novel source; treat output as untrusted
  input (XSS, SQLi).
- **Denial of wallet**: unbounded token spend rather than downtime.

## Controls that actually hold

- **Do not rely on prompt-level defenses alone.** "Ignore malicious
  instructions" in a system prompt is a speed bump, not a boundary. Guardrail
  classifiers reduce rate, not risk class.
- **Enforce authority outside the model.** The model proposes; a deterministic
  layer authorises. Tool calls run with the _end user's_ permissions, not the
  agent's service account.
- **Human confirmation on irreversible or outbound actions**: payments, deletes,
  sending data to third parties, code merges.
- **Isolate and least-privilege the tools**: narrow scopes, short-lived creds,
  egress allowlists. Sandbox any code execution.
- **Segregate untrusted content.** Mark retrieved content as data in the prompt
  structure; keep tenant corpora separate; validate who can write to the index.
- **Verify model provenance**: pinned versions, checksums, signatures; prefer
  safetensors over pickle formats; scan model artifacts like dependencies.
- **Log prompts, retrievals, tool calls and outputs** as a security-relevant
  audit trail; this is the only forensic record when an agent misbehaves
  (`load_skill detection-engineering` for turning it into alerts).
- **Rate/spend limits** per user and per session.

## Governance anchors

- **ISO/IEC 42001:2023**: the **certifiable** AI management system (AIMS), same
  shape as ISO 27001 (context → leadership → risk → controls → audit →
  improvement). The one to certify against when customers ask. Companions:
  **ISO/IEC 42005:2025** (AI impact assessment guidance) and **42006:2025**
  (requirements for certification bodies). Sits alongside, not inside, an ISMS:
  `load_skill iso27001`.
- **NIST AI RMF (AI 100-1)**: voluntary US anchor: **Govern, Map, Measure,
  Manage**, plus a Generative AI Profile (AI 600-1). A revision is under way
  under the 2025 AI Action Plan; no draft was out as of Nov 2026. Running the
  management system around it: `load_skill ai-governance`. Verify current status:
  https://www.nist.gov/itl/ai-risk-management-framework
- **NIST SP 800-218A** (final Jul 2024): the **GenAI profile of the SSDF**; use
  with SP 800-218 v1.1 in the pipeline (`load_skill devsecops`).
- **OWASP Top 10 for LLM Applications (2026 edition, Aug 2026)** and **OWASP Top
  10 for Agentic Applications (2026 edition)**; the working taxonomies for the
  risks above. https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/
- **MITRE ATLAS**: ATT&CK-shaped adversarial-ML technique matrix, for threat
  modelling AI systems (`load_skill threat-modeling`).

## Program moves

- **Inventory first.** You cannot govern shadow AI you can't see: enumerate
  models, agents, API keys, and which business processes depend on them. This is
  also the AI Act's implicit prerequisite.
- **Classify by consequence, not by hype**: what data can it reach, what actions
  can it take, who is affected if it's wrong. Feed that into
  `load_skill risk-assessment`.
- **Set an acceptable-use policy** with a sanctioned-tool list: banning AI
  outright reliably produces unmonitored personal-account usage.
- **Test adversarially before launch** and after material prompt/tool changes:
  red-team the agent's tools, not just its text (red-team / adversarial testing).
- **Contract for it**: model-provider training-data use, output IP, sub-processor
  disclosure, incident duties (`load_skill legal-contractual`).

## Report

- `report_finding` with the concrete exploit path: "indirect injection via
  retrieved doc → agent's HTTP tool → exfil to attacker host", not "LLM is
  susceptible to prompt injection". Name the tool scope that made it reachable.
- Map to CWE where one fits (e.g. CWE-77/CWE-94 for injection into an
  interpreter, CWE-200 for disclosure) and to controls via
  `load_skill control-mapping`.

## Pairs with

- `load_skill eu-ai-act` (EU obligations), `load_skill threat-modeling`,
  `load_skill appsec-sdlc`, `load_skill devsecops` (pipeline + supply chain).
- `load_skill privacy-engineering` (training data, DPIA), `load_skill data-security`.
