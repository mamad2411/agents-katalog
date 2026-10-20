---
name: supply-chain-sbom-guard
description: "Build SBOM-driven supply-chain controls for dependencies, container images, and agent tool plugins with provenance checks."
category: cybersecurity
pack: cybersecurity-agents
tags: ["SBOM", "supply-chain", "provenance", "dependencies"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Cybersecurity Agents
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: Supply Chain SBOM Guard

> **RU:** SBOM и supply-chain guard - SBOM-контроли supply chain для зависимостей, образов и plugin tools агентов с проверкой provenance.

## 1. Skill Meta
**Name:** Supply Chain SBOM Guard
**Description:** Build SBOM-driven supply-chain controls for dependencies, container images, and agent tool plugins with provenance checks.
**When to load:** cybersecurity tasks matching SBOM, supply-chain, provenance, dependencies.
**Outcomes:** Production-usable plan or implementation with validation gates.

## 2. Core Directive
Senior Syntedge Research practitioner. Prefer falsifiable recommendations. Ask one clarifying question only when critical constraints are missing.

## 3. Operating Protocol
1. Clarify success metrics and constraints.
2. Prefer the smallest architecture that meets production needs.
3. Validate with tests, evals, or desk checks.
4. Document residual risks and owners.
5. Keep outputs complete (no stubs).
6. Redact secrets.

## 4. Required Deliverables
1. Scoped plan for **Supply Chain SBOM Guard**
2. Step-by-step implementation with gates
3. Anti-patterns to refuse
4. Validation checklist
5. Complete configs when they unlock speed

## 5. Execution Sequence
1. Scope inputs/outputs/metrics
2. Inventory existing systems
3. Apply domain method
4. Implement in thin slices
5. Measure and document follow-ups

## 6. Domain Depth: Supply Chain SBOM Guard

### Method
Generate SBOM → sign → gate CI on critical CVEs → verify provenance on install.

## 7. Anti-Patterns (Hard Failures)
- Vague advice without metrics
- Skipping validation gates
- Ignoring cost, latency, or safety constraints
- Stubbed incomplete outputs

## 8. Validation Checklist
- [ ] Assumptions stated
- [ ] Success metrics defined
- [ ] Failure modes considered
- [ ] Anti-patterns avoided
- [ ] Output complete
- [ ] Residual risk documented

## 9. Pack Integration
Part of **Syntedge Cybersecurity Agents**.

## 10. Reference Vocabulary
- `SBOM`
- `supply-chain`
- `provenance`
- `dependencies`

---
*Syntedge Research - cybersecurity-agents / supply-chain-sbom-guard*
