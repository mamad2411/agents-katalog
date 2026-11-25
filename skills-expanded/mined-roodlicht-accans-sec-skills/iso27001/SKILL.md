---
name: iso27001
description: ISO/IEC 27001:2022 ISMS implementation and certification prep — clauses 4-10 (context, leadership, planning, support, operation, evaluation, improvement), Annex A 93 controls across four themes, Statement of Applicability, Stage 1/Stage 2 audit prep, and the certification cycle.
---

# ISO 27001 Mapper

> **Disclaimer**: this skill supports technical and organizational implementation, not legal or certification advice. Final certification is an independent auditor's judgement; this skill helps you prepare but does not replace an accredited auditor.

## When to use

ISO/IEC 27001:2022 is the international certifiable standard for an Information Security Management System (ISMS). The 2022 revision replaces 2013 with a revised Annex A (113 → 93 controls, regrouped into four themes). This skill helps with ISMS setup, control mapping, and Stage 1/Stage 2 audit preparation.

Triggers on:

- A question like "set up an ISO 27001 trajectory", "what goes in the SoA", "which controls for our scope", "prepare for Stage 2 audit", "gap against the 2022 revision".
- An organization considering certification or already in a certification cycle (annual surveillance, 3-yearly recertification).
- A handoff from `nis2` or `dora`: both demand an ISMS and Annex A covers their technical-measures layer.
- A question from a `soc2` context about mapping or dual-attestation strategy.
- A customer contract requirement: "you must be ISO 27001".

### When NOT (handoff)

- EU regulatory compliance (NIS2, DORA, AVG) → the relevant skills. ISO 27001 helps but is not legally required.
- SOC 2 Type II → `soc2`. Lots of overlap in controls, different audit model.
- Risk-assessment methodology → `risk-register`. ISO 27001 demands risk management (Cl 6.1, 8.2-8.3); the methodology lives in that skill.
- Policy drafting → `policy-drafter`.
- Evidence packaging for audits → `audit-evidence`.
- Technical implementation of controls (e.g. encryption, access control) → the relevant security skills.
- Privacy-specific ISO 27701 (privacy extension of 27001) is out of scope; refer to a dedicated PIMS skill if one is set up.

## Approach

Six phases. Phase 1 (scope) is the heaviest strategically; phases 3-4 (controls + risk) the heaviest operationally.

### 1. Scope and ISMS boundary

ISO 27001 Cl 4.3 demands a deliberately chosen ISMS scope. What sits inside the ISMS is audited and certified; what sits outside is not.

- **Organizational scope**: whole entity, business unit, specific product line, or specific service. Often you start with the SaaS service or B2B product and expand later.
- **Geographic scope**: one location, several, all. Remote workers explicitly in scope or out?
- **Technological scope**: which systems, networks, applications, clouds. Shadow IT and undocumented systems cause audit findings.
- **Interfaces and dependencies** (Cl 4.3): which out-of-scope systems feed input into what is in scope? Those interfaces must be documented and managed.

The out-of-scope argument must be defensible against an auditor. "Our R&D environment is out of scope because ..." — with a reason that is not Swiss-cheese.

Lock the scope down in a scope statement (documented information, Cl 4.3). One paragraph, publishable on your certificate.

### 2. ISMS clauses 4–10

The numbered chapters of the standard form the management system. Every clause demands documented information plus evidence of implementation.

- **Cl 4 Context**: external/internal issues (PESTLE-style), interested parties plus their requirements, ISMS scope.
- **Cl 5 Leadership**: top-management commitment, policy (Cl 5.2), roles and responsibilities. At audit: management-review agendas, accountability identified per role.
- **Cl 6 Planning**: risk-assessment method, risk treatment (see phase 4), infosec objectives with measurability.
- **Cl 7 Support**: resources, competence, awareness, communication, documented information (doc control).
- **Cl 8 Operation**: actual risk-assessment runs and treatment-plan execution.
- **Cl 9 Performance evaluation**: monitoring/measurement, internal audit (see phase 5), management review.
- **Cl 10 Improvement**: nonconformities plus corrective action, continuous improvement.

Common gaps at Stage 2 audits: Cl 5.2 policy not visibly committed by top management, Cl 9.3 management review without evidence of the input items required, Cl 10 nonconformities register thin or missing.

### 3. Annex A — 93 controls across four themes

ISO 27001:2022 Annex A groups controls into four themes:

- **A.5 Organizational controls** (37 controls): policies, roles, threat intelligence, supplier relationships, compliance, etc.
- **A.6 People controls** (8 controls): screening, terms, awareness, disciplinary, remote working, confidentiality.
- **A.7 Physical controls** (14 controls): secure areas, physical entry, office/room/facilities, working in secure areas, clear desk/screen, equipment siting, security of assets off-premises, storage media, supporting utilities, cabling, maintenance, removal of assets, disposal, unattended user equipment.
- **A.8 Technological controls** (34 controls): user endpoint, privileged access, authentication, identity management, information access, source code, secure development, test data, configuration, info deletion, data masking, DLP, backup, redundancy, logging, monitoring, clock sync, separation of networks, web filtering, cryptography, secure system engineering, outsourced dev, separation of dev/test/prod, vulnerability management, secure coding, testing, installation, change management, development lifecycle, configuration, capacity, ...

Every control in A.5-A.8 has a **control statement** (what), **purpose** (why), and **guidance** (how). Guidance is not normative but strongly recommended for audit.

### 4. Risk assessment and Statement of Applicability

**Risk assessment** (Cl 6.1.2) requires:

- A risk-assessment methodology that is consistently executable (reproducible).
- Asset identification or another recognized model (scenario-based, threat-based).
- Likelihood + impact judgement with written criteria.
- Risk-acceptance criteria explicit.

See `risk-register` for methodology; ISO 27005 is the ISO-specific infosec risk-management standard that pairs with 27001.

**Statement of Applicability (SoA)** (Cl 6.1.3.d) is the central document: a list of all 93 Annex A controls with, per control:

- Applicable: yes / no.
- If no: rationale for exclusion (e.g. "A.7.14 Secure disposal of storage media — not applicable, we host in cloud, disposal is a provider responsibility"). Rationale must be auditor-convincing.
- If yes: implementation status (implemented / partial / planned) with a pointer to where the evidence lives.

The SoA is a living document. It changes on risk re-assessment, scope change, new threats. Versioning required.

**Risk-treatment plan** (Cl 6.1.3.e): per identified risk: chosen treatment (avoid/modify/share/retain — the ISO terms for avoid/mitigate/transfer/accept), Annex A controls applied, owner, deadline, status.

### 5. Audit preparation: Stage 1 and Stage 2

The external certification audit has two stages:

- **Stage 1 (documentation review)**: the auditor reads the ISMS documents plus SoA, judges completeness and design adequacy. Produces major/minor findings plus recommendations. Output: "go to Stage 2" or "improve and retry". Lasts 1-3 days on-site or remote.
- **Stage 2 (implementation audit)**: the auditor tests evidence that the ISMS works. Interviews, documentation sampling, walk-throughs, evidence verification. Lasts 2-5+ days depending on scope. Findings are nonconformities (major/minor/observation). Major = certificate held until closed, minor = corrective action within 90 days.

After certification:

- **Surveillance audit** annually, lighter than Stage 2, focused on changes and previously found issues.
- **Recertification audit** every 3 years, comparable to Stage 2.

Preparation discipline: an internal audit programme (Cl 9.2) plus management review (Cl 9.3) at least one cycle before Stage 2. Resolve internal-audit findings up front.

See `audit-evidence` for evidence packaging per control.

### 6. Mapping to other frameworks and verification-loop

ISO 27001 is the foundation other frameworks build on:

- **NIS2 Art 21 ↔ Annex A**: publicly available mappings (ENISA) — 27001 covers all 10 NIS2 measures.
- **DORA ↔ 27001**: the ICT-risk-management framework requirement is implicitly 27001-compatible.
- **SOC 2 ↔ 27001**: large overlap in controls, different audit model. Dual attestation possible from one ISMS.
- **NIST CSF 2.0 ↔ 27001**: cross-walks available.

Layer 1: scope statement unambiguous?, all 93 Annex A controls addressed in the SoA (yes/no)?, risk-treatment plan covers all above-tolerance risks?, internal-audit log complete for the cycle?. Layer 2: Annex A control numbers verified against the 2022 version (not 2013!), ISO clause references correct, NIS2/DORA mapping claims supported by ENISA documents or your own cross-walk, not improvised.

## Output

```
ISO 27001:2022 assessment — <entity/scope>
Goal: <certification Stage 1 | Stage 2 | surveillance | recertification | gap analysis without audit>

ISMS scope:
  Organizational:   <entity/unit/product>
  Geographic:       <locations>
  Technological:    <systems/clouds>
  Interfaces:       <mapped | gap>

Clauses 4-10 status:
  Cl 4 Context:           <complete | gaps: ...>
  Cl 5 Leadership:        ...
  Cl 6 Planning:          ...
  Cl 7 Support:           ...
  Cl 8 Operation:         ...
  Cl 9 Performance:       ...
  Cl 10 Improvement:      ...

Annex A 93 controls (SoA status):
  A.5 Organizational:    <N/37 implemented, N/37 partial, N/37 gap>
  A.6 People:            ...
  A.7 Physical:          ...
  A.8 Technological:     ...
  Exclusions (not applicable): <N, rationale quality: strong/weak>

Risk management:
  Methodology:            <used + source>
  Risk-treatment plan:    <coverage, owners>
  SoA version + date:     <...>

Audit readiness:
  Stage 1 ready:          <yes/no with gaps>
  Stage 2 ready:          <yes/no with gaps>
  Internal audit run:     <date>
  Management review:      <date>

Mapping (optional):
  NIS2 Art 21 coverage:   <%>
  SOC 2 TSC overlap:      <summary>

Priorities:
  <fix-now / fix-sprint / fix-quarter>

Verification-loop: ...
```

## References

- **ISO/IEC 27001:2022** — [https://www.iso.org/standard/27001](https://www.iso.org/standard/27001). Official standard (paid). NEN sells the NL version.
- **ISO/IEC 27002:2022** — [https://www.iso.org/standard/75652.html](https://www.iso.org/standard/75652.html). Guidance companion for Annex A controls, not a certification requirement but practically indispensable.
- **ISO/IEC 27005:2022** — [https://www.iso.org/standard/80585.html](https://www.iso.org/standard/80585.html). Infosec risk management, pairs with 27001.
- **ENISA — NIS2 mapping** — [https://www.enisa.europa.eu/topics/nis-directive](https://www.enisa.europa.eu/topics/nis-directive). For cross-walks to NIS2 Art 21.
- **IAF — International Accreditation Forum** — [https://iaf.nu/](https://iaf.nu/). For accredited certification bodies.
- **Raad voor Accreditatie (RvA)** — [https://www.rva.nl/](https://www.rva.nl/). NL accreditation body for certifying institutions.
- **NEN** — [https://www.nen.nl/](https://www.nen.nl/). Dutch distributor of ISO standards, including NL translations.
- **BSI 27001 toolkit docs** (vendor docs with reasonable quality) — examples of SoA templates.

## Categories

- grc
