---
name: oss-vetting
audience: team
description: >
  OSS library vetting and SBOM analysis for federal contractor environments (national labs / DOE / CUI).
  Use this skill when evaluating any open-source or third-party package for use in a federal
  contractor project — including NuGet packages, npm, PyPI, or any OSS library. Triggers include:
  vet this library, can we use X on a national-lab project, is X approved for CUI systems, evaluate this NuGet
  package, generate an SBOM, supply chain risk, check this dependency, OSS assessment,
  800-171 compliance for this package, C-SCRM review. Also trigger for any question about
  whether a library is safe, compliant, or appropriate for use on a government contract or
  CUI-adjacent system.
---

# OSS Vetting Skill

> "On a federal contract, a dependency is not a convenience — it is an attack surface you
> inherited and a compliance liability you signed for. Vet it like both."

## Core Philosophy

Producing an OSS Vetting Assessment Report for federal contractor use is a compliance act, not a
checkbox. Every assessment is evaluated against four frameworks — understanding *why* each matters
prevents shallow checkbox compliance:

| Framework | Role |
|---|---|
| **EO 14028** | Creates the legal obligation — software on federal systems must be verifiably secure |
| **NIST SP 800-218 (SSDF)** | Defines the process — how maintainers should build and respond to vulnerabilities |
| **NIST SP 800-171 Rev 2** | Sets the data-protection stakes — 110 controls for CUI systems; a vulnerable dep is a direct compliance liability |
| **NIST SP 800-161 (C-SCRM)** | Governs provenance — where the software came from, who maintains it, whether the supply chain is auditable |

**Non-Negotiable Constraints:**
1. SCOPE FIRST — never assess without package, version, ecosystem, and target system (CUI? restricted network? air-gapped?). A vague request produces a shallow report; ask.
2. EVIDENCE, NOT CLAIMS — every dimension score cites a finding (CVE ID, repo signal, license SPDX), never an impression.
3. AIR-GAP SAFE — for restricted network artifacts, no live-connectivity URLs, no cloud scanners (Snyk/Dependabot), offline-capable SBOM tooling only.
4. RED FLAGS ESCALATE — a disqualifying finding (see `references/assessment-dimensions.md`) halts approval pending waiver, regardless of other scores.

Plain-language framework explanations for stakeholder briefings live in `references/framework-glossary.md`.

## Workflow

```
DETECT    Gather inputs: package, version, ecosystem; target system + classification;
          intended use; constraints. Missing context → ask. No report written yet.

RESEARCH  Investigate the four dimension groups — identity/provenance, security posture,
          development health (SSDF), supply chain (C-SCRM). Web search if available;
          note limitations if air-gapped. Detail: references/assessment-dimensions.md.

SCORE     Rate each dimension 1–5 (5 = lowest risk): security posture, supply chain
          integrity, maintainership health, license compatibility, CUI suitability.
          Each score cites evidence. Scale + dimensions: references/assessment-dimensions.md.

LICENSE   Resolve SPDX identifier → risk tier (acceptable / review / disqualifying) and
          note attribution + patent clauses. Full matrix: references/license-matrix.md.

SBOM      Note SBOM availability and pick offline-capable tooling for the deployment context.
          Tooling table + air-gap rules: references/assessment-dimensions.md.

REPORT    Write the Confluence-ready report from references/report-template.md with a
          clear recommendation: Approve / Approve with conditions / Reject.
```

**Exit criteria:** every dimension scored with cited evidence; license tier resolved; SBOM posture
noted; a single explicit recommendation rendered; red flags surfaced and escalated if present.

## State Block

```
<oss-vetting-state>
phase: DETECT | RESEARCH | SCORE | LICENSE | SBOM | REPORT | COMPLETE
package: [name@version]
ecosystem: nuget | pypi | npm | other
target_system: [name] (cui: true|false, yellow_network: true|false, air_gapped: true|false)
license_spdx: [id] | unknown
license_tier: acceptable | review | disqualifying | unresolved
dimension_scores: security=_ supply=_ maintainer=_ license=_ cui=_ (1–5, blank = not-yet-scored)
red_flags: [count] | none
recommendation: approve | approve-with-conditions | reject | pending
last_action: [description]
next_action: [description]
</oss-vetting-state>
```

## Output Template

- **Full report** — `references/report-template.md` (Confluence-ready: header + classification marking,
  executive summary, dimension scores, findings, license analysis, supply-chain/SBOM notes, mitigations, references).
- **License analysis** — risk tiers, attribution, and patent notes from `references/license-matrix.md`.
- **Stakeholder framework briefings** — plain-language explanations from `references/framework-glossary.md`.

Render as Confluence-ready Markdown: `##` section headers, tables for scores and license data, inline
code for package names / CVE IDs / SPDX identifiers, a blockquote for the executive-summary callout,
and the classification marking as a bold header line at the top.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `supply-chain-audit` | Run to scan the consuming project's full dependency tree once a package is approved. |
| `dependency-mapper` | Map where the vetted package sits in the project's dependency graph and its blast radius. |
| `security-review-federal` | Pairs the package assessment with a federal security review of the consuming system. |
| `nuget-package-scaffold` / `pypi-package-scaffold` | Apply vetting standards when authoring first-party packages, not just consuming third-party ones. |
