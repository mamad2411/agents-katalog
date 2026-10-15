---
name: cog-axiom
description: AxiomOS cognitive principles library providing eight immutable engineering principles, security kernel, compliance constraints, deliverable standards, and thinking protocols. Use as a reference domain to ground architecture decisions and enforce delivery standards; contains no operational workflow.
---

# AxiomOS Cognitive Principles Library

A reference-only cognitive asset. This skill provides principles, guardrails, and standards that other workflows consume. It deliberately contains **no operational modes or pipelines**: routing lives in `eng-router`, execution flows live in the Autopilot lifecycle orchestrators, and review lenses live in the dedicated audit skills.

---

## Reference Domains

### 1. Foundations
- Role & Mission: [`foundation/role.md`](foundation/role.md)
- Core Architectural Principles: [`foundation/principles.md`](foundation/principles.md)
- Context Architecture: [`foundation/context.md`](foundation/context.md)

### 2. Configuration & Safety
- System Constants: [`config/system.md`](config/system.md)
- Security Kernel: [`config/security.md`](config/security.md)
- Compliance Constraints: [`config/compliance.md`](config/compliance.md)

### 3. Standards
- Deliverable Standards: [`standards/deliverable.md`](standards/deliverable.md)
- Artifact Standards: [`standards/artifact.md`](standards/artifact.md)

### 4. Tool & Interaction Protocols
- Tool Governance: [`protocols/tools.md`](protocols/tools.md)
- Interaction Protocol: [`protocols/interaction.md`](protocols/interaction.md)

### 5. Cognitive Protocols
- Session Lifecycle: [`cognitive/session.md`](cognitive/session.md)
- UltraThink Deep-Reasoning Protocol: [`cognitive/ultrathink.md`](cognitive/ultrathink.md)

---

## 8 Immutable Core Principles

1. **Domain-Driven Priority**: Model real-world business domains explicitly before writing implementation logic.
2. **Specification-Driven Development**: Define contracts, schemas, and acceptance criteria upfront.
3. **Strategic Alignment**: Code changes must align with long-term architecture rather than quick hacks.
4. **Active Guardrails**: Enforce automated validation, type safety, and linting gates.
5. **Full Traceability**: Maintain clear commit logs, execution reports, and decision records.
6. **Zero-Trust Security**: Treat all inputs as untrusted; avoid secret leaks and unsafe execution.
7. **Quality-First Mindset**: Tests and documentation are first-class deliverables.
8. **Platform Agnosticism**: Ensure scripts and commands run cross-platform without platform-locked assumptions.

---

## Where Operational Capabilities Live Now

| Former Mode | Replaced By |
|---|---|
| triage (intent routing) | `eng-router` |
| sdm (standard development) | `eng-enterprise-lifecycle` |
| sfam (full automation) | Autopilot orchestrators |
| debug | `eng-defect-lifecycle`, `eng-hotfix-emergency-lifecycle` |
| audit + review | `eng-code-review`, `eng-multidimensional-audit` |
| security | `eng-adversarial-audit`, `eng-destructive-safety-gate` |
| micro-task | Fast-path rule in `eng-enterprise-lifecycle` |
| onboarding | `eng-prime-context`, `eng-onboarding-audit-lifecycle` |
| enhancement (prompt optimization) | Migrated to standalone skill `prod-prompt-enhancer` |

---

## Checkable Completion Criteria

- [ ] Principles consulted before architectural decisions when this skill is active.
- [ ] No operational workflow executed from within this reference library.
- [ ] All referenced files resolve correctly.