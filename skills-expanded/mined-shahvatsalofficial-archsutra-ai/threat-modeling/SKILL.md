---
name: threat-modeling
description: Threat model a system, feature or change. Covers assets, actors, data flows, trust boundaries, STRIDE threats, LLM and agent threats (prompt injection, excessive agency, insecure output handling), mitigations with verification tests, and residual risk. Use this skill whenever the user asks for a security design review, attack surface, "what could go wrong", abuse cases, or is adding an AI agent or tool access, a new public endpoint, or a third-party integration, even if they never say "threat model". Do not use it as a penetration test, vulnerability scan or compliance audit.
license: Apache-2.0
compatibility: Works with file read and search tools and conversation. Diagrams are Mermaid text. No network or scanner needed.
---
# Threat Modeling

Produce a short, specific threat model that engineers will actually use: what is at stake, how it could be attacked here, what stops it, and what is left over.

## Why this skill is built the way it is

- Generic STRIDE tables get ignored. Threats tied to this system's data flows, with a control and a test, get fixed.
- Teams under-model the boundaries between components and between humans and models. Most real incidents cross a trust boundary.
- AI features add a new boundary: text that a model reads can steer what it does. Anything the model can call becomes part of the attack surface.

## Workflow

1. **Scope and assets.** What is the system, what is in and out of scope, and what is protected (data, money, availability, safety, reputation)? Who are the actors, including a malicious insider, a compromised dependency and a curious customer?
2. **Draw the data flow** in Mermaid: processes, stores, external entities, and the trust boundaries between them. Mark where untrusted data enters.
3. **Enumerate threats per element and per boundary crossing** with [references/stride-checklist.md](references/stride-checklist.md). For models, agents or tools also use [references/llm-agent-threats.md](references/llm-agent-threats.md).
4. **Rate each threat** by likelihood and impact with one line of reasoning. Use ordinal ratings (low, medium, high). Do not state a CVE, exploit or statistic you did not verify.
5. **Mitigate concretely.** Each threat gets a control, an owner type and a test that would fail if the control were missing. Prefer removing the capability over guarding it.
6. **Record residual risk** and who must accept it. A risk nobody owns is a risk nobody has accepted.
7. **Emit tracked items** using [references/threat-register-template.md](references/threat-register-template.md). Evidence is `observed` when you saw it in code or config, `proposed` when it is a recommended control.

## Rules that keep the model honest

- **Be specific to this system.** Name the endpoint, table, queue or tool. "Attacker tampers with data" is not a threat; "a customer edits `orderId` in `PUT /orders/{id}` to modify another tenant's order" is.
- **Treat model input as hostile.** Retrieved documents, web pages, tickets and tool outputs can contain instructions. They never gain authority over tools.
- **Irreversible or external actions need a human.** Sending money, deleting data, emailing customers and running shell commands require approval by default.
- **Active secrets or exploitable flaws found along the way come first.** Stop and report them with the rotation or fix step before continuing.
- **Frameworks are references.** OWASP ASVS, OWASP Top 10, the OWASP Top 10 for LLM Applications and NIST SSDF guide the review; the result is not a certification or a compliance statement.

## Files the reader gets

Write the threat model as both `docs/architecture/threat-model.md` and `docs/architecture/threat-model.html`. Save the Markdown, then run `archsutra html docs/architecture/threat-model.md`. Do not hand-write HTML. Do not leave the model only in chat.

## Hand-offs

Use architecture-audit for a broader review of existing code. Run architecture-verification on the finished model before it is shared.
