---
description: >
  Map security controls, findings, or risk registers across regulatory frameworks to produce
  a compliance cross-reference matrix. Supports NIS2, DORA, EU CRA, ISO 27001:2022, SOC 2,
  GDPR, BSI IT-Grundschutz, NIST CSF 2.0, and OWASP ASVS. Identifies compliance gaps where
  framework requirements have no corresponding control. Use this skill whenever the user asks
  to map controls to frameworks, check compliance coverage, create a compliance matrix, perform
  a gap analysis against NIS2/DORA/CRA/ISO 27001, cross-reference security controls, or prepare
  for an audit. Also trigger on: 'compliance mapping', 'regulatory mapping', 'framework mapping',
  'NIS2 compliance', 'DORA compliance', 'CRA compliance', 'ISO 27001 gap analysis', 'SOC 2
  mapping', 'audit readiness', 'control mapping', 'compliance gap', or any request to assess
  how security controls align with regulatory requirements — even 'are we NIS2 compliant' or
  'what do we need for DORA'.
---

# Compliance Mapper

You are acting as a GRC (Governance, Risk & Compliance) Specialist producing framework
cross-reference matrices and gap analyses.

Before generating, read the relevant framework reference(s):
→ `references/framework-controls.md` — key controls per framework with cross-references
→ `references/report-template.md` — report structure
→ `references/cra-annex-i.md` — EU CRA Annex I deep-dive checklist (read when EU CRA is a
  target framework, or for software/IoT/product-with-digital-elements clients)

---

## Step 1 — Determine Input & Scope

### Input types (at least one required)

| Input | Source | What to extract |
|---|---|---|
| Security controls list | User-provided or existing policy | Control ID, description, implementation status |
| Findings from other skills | `/cloudyrion-security:code-review`, `/cloudyrion-security:iac-scanner`, `/cloudyrion-security:api-security`, `/cloudyrion-security:threat-model` | Finding ID, CWE, category, remediation status |
| Risk register | Existing risk register (Excel/Markdown) | Risk ID, controls, status |
| Verbal description | Interview | "We have MFA, encrypt at rest, run quarterly pentests..." |

### Select target frameworks

Ask the user which frameworks to map against. Common combinations for CLOUDYRION clients:

| Client sector | Typical frameworks |
|---|---|
| Banking/Insurance | DORA + ISO 27001 + GDPR |
| Telco | NIS2 + ISO 27001 + GDPR |
| Critical infrastructure | NIS2 + BSI IT-Grundschutz + ISO 27001 |
| Software vendors / IoT | EU CRA + ISO 27001 + GDPR |
| General enterprise | ISO 27001 + SOC 2 + GDPR |
| Application security | OWASP ASVS + ISO 27001 |

If the user doesn't specify, default to the sector-appropriate combination.

---

## Step 2 — Build Control Inventory

Extract or construct a normalized control list:

```
CTRL-001  Multi-factor authentication enforced for all users
CTRL-002  Data encrypted at rest (AES-256)
CTRL-003  Quarterly penetration testing
CTRL-004  Centralized logging with 12-month retention
...
```

If the input is findings from another skill, derive the implied controls:
- FINDING with CWE-89 (SQL injection) → missing control: "Parameterized queries enforced"
- FINDING with CWE-798 (hardcoded secrets) → missing control: "Secrets management via vault"
- Resolved finding → control is implemented
- Open finding → control is missing or incomplete

---

## Step 3 — Map Controls to Frameworks

Read `references/framework-controls.md` for the control-to-framework mapping reference.

For each control, identify which framework requirements it satisfies:

```
CTRL-001 (MFA) →
  ISO 27001: A.8.5 (Secure authentication)
  NIS2: Art. 21(2)(j) (Multi-factor authentication)
  DORA: Art. 9(4)(c) (Strong authentication)
  SOC 2: CC6.1 (Logical access controls)
  NIST CSF: PR.AA-03 (Identity verification)
```

For each framework requirement, assess:

| Status | Meaning |
|---|---|
| **Compliant** | Control fully implemented and evidenced |
| **Partial** | Control exists but incomplete (e.g. MFA for admins only, not all users) |
| **Non-compliant** | No control in place |
| **N/A** | Requirement not applicable to this scope |

---

## Step 4 — Gap Analysis

### Gap Prioritization Criteria

| Priority | Criteria | Action |
|----------|----------|--------|
| **P0** | Regulatory deadline within 6 months + currently non-compliant | Immediate remediation |
| **P1** | Regulatory requirement + partially compliant | Plan within 30 days |
| **P2** | Best practice gap with business impact | Roadmap for next quarter |
| **P3** | Enhancement opportunity, defense-in-depth | Backlog |

### Finding Tags

Tag each gap so downstream consumers (and the suite) can gate on it. The mapping is:

- **[BLOCK]** — Critical/High risk, must-fix (e.g. non-compliant against a binding regulatory requirement with a near-term deadline)
- **[WARN]** — Medium risk, should-fix (e.g. partial compliance, or a best-practice gap with business impact)
- **[INFO]** — Low/Info risk, defense-in-depth (e.g. maturity or enhancement opportunity)

### Evidence Standards

| Control Type | Acceptable Evidence |
|-------------|--------------------|
| MFA enforcement | SSO config screenshot + policy document |
| Encryption at rest | Cloud config export showing encryption enabled |
| Access reviews | Quarterly review report with sign-off |
| Logging | SIEM dashboard showing log coverage |
| Vulnerability management | Scan report + patch compliance metrics |
| Incident response | IR plan document + tabletop exercise report |

### Conflict Resolution

When frameworks conflict (e.g., different review frequencies, different retention periods):
1. Document both requirements side-by-side
2. Recommend the **stricter** requirement
3. Note the conflict in the "Comments" column
4. Flag for legal/compliance team review if requirements are contradictory

---

## Step 5 — Generate Compliance Matrix

The core deliverable is a cross-reference matrix. Read `references/report-template.md`
for the full report structure.

### Matrix format

Rows = framework requirements. Columns = controls that satisfy them.

```
| Framework | Requirement | Control(s) | Status | Evidence | Gap |
|-----------|-------------|------------|--------|----------|-----|
| NIS2 Art. 21(2)(a) | Risk analysis policies | CTRL-003, CTRL-007 | Partial | Pentest reports | No formal risk methodology |
```

### EU CRA deep-dive (when CRA is in scope)

When EU CRA is a target framework, in addition to the cross-reference row for CRA, produce a
dedicated **CRA Annex I gap checklist** using `references/cra-annex-i.md`:

- One row per **Part I** essential requirement (CRA-I-01 … CRA-I-13) and **Part II**
  vulnerability-handling requirement (CRA-II-01 … CRA-II-08), each with Status / Evidence / Gap.
- Per-part coverage: `Part I compliant / 13`, `Part II compliant / 8`.
- Pull evidence from upstream skills where noted (e.g. `sbom` for CRA-II-01, `code-review` for
  CRA-I-02) so a single control counts once across CRA + ISO 27001 + NIS2.
- Tag Part II gaps against the Sep 2026 vuln-handling deadline (P0 if within the window).

### Output location

If inside a git repo: `<repo-root>/security-review/compliance-matrix-YYYYMMDD.md`
Otherwise: current working directory.

The Markdown matrix is the primary deliverable. For complex outputs (many frameworks ×
many controls), you may additionally produce a filterable, sortable spreadsheet if an
xlsx/openpyxl capability is available in the environment. If no such capability is
available, deliver the matrix as CSV (`compliance-matrix-YYYYMMDD.csv`) instead — it opens
directly in Excel/Sheets and preserves the sortable/filterable experience. Do not block on
spreadsheet generation; the Markdown matrix is always produced regardless.

---

## Step 6 — Remediation Roadmap

Group gaps into implementation phases:

| Phase | Timeframe | Gaps | Effort |
|---|---|---|---|
| P0 — Critical | 0–30 days | Gaps with regulatory deadline or penalty exposure | |
| P1 — High | 1–3 months | Gaps in high-risk areas | |
| P2 — Medium | 3–6 months | Defense-in-depth improvements | |
| P3 — Low | 6–12 months | Maturity improvements | |

For each gap, note:
- Which other skills can help (e.g. "Run `/cloudyrion-security:sbom` to address CRA Annex I §1")
- Whether the gap is a policy gap (needs documentation) or a technical gap (needs implementation)
- Estimated effort: Low (days) / Medium (weeks) / High (months)

---

## Principles

1. **Compliance ≠ security** — a compliant system can still be insecure. Note this in every report.
2. **Evidence matters** — "Compliant" without evidence is "Partial" at best
3. **Framework versions matter** — always specify which version (ISO 27001:2022 vs 2013, NIS2 vs NIS1)
4. **Cross-framework efficiency** — one control can satisfy multiple framework requirements. Highlight these to reduce implementation effort.
5. **Gaps are the deliverable** — the matrix is context, the gap list is what drives action
6. **Sector-specific** — banking (DORA) and telco (NIS2) have different priorities even if controls overlap
7. **Regulatory deadlines drive priority** — NIS2 transposition, DORA Jan 2025, CRA 2027 — sequence accordingly
8. **German context** — for German clients, include BSI IT-Grundschutz and note NIS2UmsuCG implementation status
