---
name: openssf-baseline
description: >-
  OpenSSF OSPS Baseline v2026.08.28 and Scorecard v5: assess an open source repository against the Open Source Project Security Baseline controls (OSPS-AC, BR, DO, GV, LE, QA, SA, VM) at maturity levels 1 to 3, self-attest the result, and run OpenSSF Scorecard checks in CI. Use when auditing or hardening a project's security posture, filling in the Baseline checklist, writing a Baseline compliance statement, mapping Baseline controls to the EU CRA, NIST SSDF, CSF or SLSA via the published mappings, reading Scorecard results (Branch-Protection, Code-Review, Dangerous-Workflow, Token-Permissions, Pinned-Dependencies, SAST, Signed-Releases, Vulnerabilities), or setting up scorecard-action. Lines: OSPS Baseline v2026.08.28 is current and the OSPS Baseline in-development version is a tracked preview; OpenSSF Scorecard v5 (v5.5.0) is current. Baseline v2026.02.19, v2025.10.10 and v2025.02.25 and Scorecard v4 are legacy. Triggers: OSPS Baseline, OSPS-AC-01, maturity level, Security Insights, scorecard badge.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# OpenSSF OSPS Baseline and Scorecard

The Open Source Project Security (OSPS) Baseline, maintained by the OpenSSF Security Baseline SIG, is a catalog of MUST-only security controls for open source projects, organized in eight families and three maturity levels. OpenSSF Scorecard is a separately versioned OpenSSF tool that scores a repository on automated heuristic checks. With this skill the agent assesses a repository against a named Baseline version and level, records evidence and a point-in-time self-attestation, relates controls to other frameworks through the Baseline's own mappings, and runs and reads Scorecard.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: maintainer (assessing and improving your own project), assessor (reviewing someone else's project), or consumer (judging an upstream dependency).
- Target version: OSPS Baseline v2026.08.28 (default). OSPS Baseline v2026.02.19, OSPS Baseline v2025.10.10 and OSPS Baseline v2025.02.25 are legacy: read existing claims against them and upgrade, never start a new assessment on them. OSPS Baseline in-development is a preview (posture: track): never claim against it. For Scorecard: OpenSSF Scorecard v5 (default, v5.5.0); OpenSSF Scorecard v4 is legacy. See [`references/versions.md`](references/versions.md).
- Target level: Level 1, 2 or 3. Pick it from the level descriptions (step 2), not from what is easiest to pass.
- Scope: the repositories that make up the project, whether the project has made a release, its official channels and distribution channels, and where its project documentation lives.
- Access: whether you have admin access to the version control system and CI/CD settings. Several controls cannot be observed without it.
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the versions list on the Baseline home page and the Scorecard releases page for a newer line, and update the pins.

## Invariants

1. **Claim against one version and one level, at a point in time.** Consumers specify compliance against a specific Baseline version, and compliance is a point-in-time status, stated like "As of <date>, this project complies with OSPS Baseline version <version> level <n>" (Home, Versions; FAQ, Does OSPS Baseline compliance expire?).
2. **Only the current version for new work.** Only the version labeled current is used for new compliance efforts; previous versions are for historical reference (Home, Versions).
3. **Assess assessment requirements, not just controls.** A control (`OSPS-AC-03`) groups assessment requirements (`OSPS-AC-03.01`, `OSPS-AC-03.02`), and each requirement carries its own MUST text and level applicability (catalog `baseline/OSPS-*.yaml`). Controls only contain MUST entries (Home, Guiding principles).
4. **A level covers every requirement that applies at that level.** Each requirement lists the maturity levels it applies to; a Level N claim needs every requirement whose applicability includes N (catalog `applicability`; Controls Overview).
5. **Preconditions decide applicability.** Requirements that start with "When the project has made a release", "When an official release is created" or "When the package management system supports it" apply only when the condition holds. Record the condition and why it does not hold rather than marking the requirement met (requirement texts).
6. **Identifiers are stable.** Retired identifiers are never reused and stay in the catalog marked retired; a substantial change of meaning gets a new identifier; a level change keeps the identifier (Maintenance Process, Identifiers).
7. **Self-attestation, not a grade.** Projects self-attest; the Baseline is not a comparison, scoring or grading tool between projects, and tooling cannot discover every implementation (FAQ, How can I prove…; What should the Baseline not be used for?).
8. **Mappings relate, they do not certify.** Mappings to external frameworks are relates-to references, not 100% matches, and provide no claim of compliance with the external catalog and no substitute for audits (Overview; FAQ, How is the OSPS Baseline different…; mapping document metadata).
9. **Scorecard is heuristic.** Each check scores 0 to 10, the aggregate is a risk-weighted average (Critical 10, High 7.5, Medium 5, Low 2.5), and a low score is not a definitive indication of risk (Scorecard README, Scoring and Project Non-Goals; checks.md notes).
10. **A Scorecard score is not a Baseline result.** The Baseline maps only some controls to Scorecard checks, and Scorecard's own analysis finds most Baseline requirements only partly covered or not observable (mapping `osps-to-scorecard.yaml`; Scorecard OSPS Baseline coverage analysis).
11. **Publishing Scorecard results constrains the workflow.** With `publish_results: true`, the job needs `id-token: write`, the workflow has no top-level env or defaults and no workflow-level write permissions, and the job uses only the approved actions (scorecard-action README, Breaking changes in v2 and Workflow Restrictions).

## Workflow

1. **Pick the versions.** Use OSPS Baseline v2026.08.28 and Scorecard v5. If an existing claim names an older Baseline version, plan the upgrade (step 10).
   -> [`references/versions.md`](references/versions.md)
   ✓ The Baseline version, level and Scorecard version are recorded, and none is legacy or preview.
2. **Scope the project and pick the level.** List the repositories, the primary branch, official and distribution channels, whether a release exists, and the documentation location. Level 1 is for any code or non-code project; Level 2 for a code project with at least 2 maintainers and a small number of consistent users; Level 3 for a code project with a large number of consistent users (Controls Overview).
   -> [`references/assessment.md`](references/assessment.md)
   ✓ The scope and target level are written down with the reason for the level.
3. **Gather evidence.** Collect version control and CI/CD settings, files (LICENSE, SECURITY.md, CONTRIBUTING.md, dependency manifests, workflows), release assets, and the Security Insights file if one exists.
   -> [`references/assessment.md`](references/assessment.md)
   ✓ Each piece of evidence has a link or a captured setting, and settings you cannot see are marked unknown.
4. **Assess Level 1.** Walk every Level 1 requirement.
   -> [`references/controls-level-1.md`](references/controls-level-1.md)
   ✓ All 24 Level 1 requirements have a result, evidence and, if not applicable, the failed precondition.
5. **Assess Levels 2 and 3** (only up to the target level).
   -> [`references/controls-levels-2-3.md`](references/controls-levels-2-3.md)
   ✓ Every requirement whose applicability includes the target level has a result.
6. **Record the result.** Fill in the version's checklist, and write the dated statement from invariant 1 only when every applicable requirement is met.
   -> [`references/assessment.md`](references/assessment.md)
   ✓ The statement names the version, the level and the date, and the gaps list is empty or no statement is made.
7. **Relate to other frameworks** (when asked). Look up the published mapping document for the framework, and report relationships, not compliance.
   -> [`references/assessment.md`](references/assessment.md)
   ✓ Every mapped item cites the mapping document and version, and the report carries the no-compliance caveat.
8. **Run Scorecard.** Run the CLI or scorecard-action, read per-check scores and details, and add maintainer annotations where Scorecard cannot see an implementation.
   -> [`references/scorecard.md`](references/scorecard.md)
   ✓ The run names the Scorecard version; the workflow has read-all top-level permissions; the actions in it are pinned.
9. **Remediate.** Fix gaps using each requirement's recommendation and each check's remediation steps, then re-assess the changed requirements.
   -> [`references/controls-level-1.md`](references/controls-level-1.md), [`references/controls-levels-2-3.md`](references/controls-levels-2-3.md), [`references/scorecard.md`](references/scorecard.md)
   ✓ Every closed gap has new evidence.
10. **Upgrade** (only when asked). Move a claim from a legacy Baseline version to v2026.08.28, or a Scorecard v4 integration to v5.
    -> [`references/versions.md`](references/versions.md)
    ✓ The new claim covers the added requirements, drops the retired ones, and is re-dated.

## Verify before done

- [ ] The assessment names one Baseline version (v2026.08.28 unless the user named another) and one level (invariants 1, 2).
- [ ] Every assessment requirement whose applicability includes the target level has a result and evidence; retired OSPS-BR-01.02 is not assessed (Maintenance Process, Identifiers).
- [ ] Not-applicable results name the precondition that does not hold (invariant 5).
- [ ] Requirements that need admin access you did not have are marked unknown, not met (Scorecard coverage analysis, Notes).
- [ ] Any compliance statement is dated and lists version and level (FAQ).
- [ ] Mappings are reported as relates-to, with the mapping document and the "no claim of compliance" caveat (FAQ).
- [ ] Scorecard scores are reported per check with the Scorecard version, and never as a Baseline level (invariants 9, 10).
- [ ] A Scorecard workflow that publishes results meets the scorecard-action restrictions (invariant 11).
- [ ] Nothing is claimed against the in-development version.

## Reference index

- **`references/versions.md`**: every Baseline release and Scorecard major line with status, what changed between releases, upgrade steps, and the in-development preview. Load for steps 1 and 10.
- **`references/controls-level-1.md`**: the eight families and all Level 1 requirements with their text, recommendation and evidence to look for. Load for steps 4 and 9.
- **`references/controls-levels-2-3.md`**: the Level 2 and Level 3 requirements, grouped by family. Load for steps 5 and 9.
- **`references/assessment.md`**: scoping, evidence, recording results, the checklist and statement, Security Insights, assessment tooling, and the external framework mappings including Scorecard, CRA and SLSA. Load for steps 2, 3, 6 and 7.
- **`references/scorecard.md`**: every Scorecard check with risk and scoring, the aggregate score, CLI, scorecard-action in CI, annotations, probes, and the Baseline-to-Scorecard mapping. Load for steps 8 and 9.

## Related skills

- `slsa` for build provenance and levels behind OSPS-BR-06.01 and the Signed-Releases check: `npx skills add ScaleDockHQ/scaledock-skills --skill slsa`.
- `in-toto` for attestations and the `*.intoto.jsonl` provenance Scorecard looks for: `npx skills add ScaleDockHQ/scaledock-skills --skill in-toto`.
- `cyclonedx` for the SBOM behind OSPS-QA-02.02 and the SBOM check: `npx skills add ScaleDockHQ/scaledock-skills --skill cyclonedx`.
- `eu-cra` for the Cyber Resilience Act requirements the Baseline maps to: `npx skills add ScaleDockHQ/scaledock-skills --skill eu-cra`.
- `security-txt` for publishing security contacts (OSPS-VM-02.01, OSPS-VM-03.01): `npx skills add ScaleDockHQ/scaledock-skills --skill security-txt`.
- `openvex` for the VEX documents OSPS-VM-04.02 requires: `npx skills add ScaleDockHQ/scaledock-skills --skill openvex`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Open Source Project Security Baseline (home and versions index)](https://baseline.openssf.org/): Released, lists v2026.08.28 as current, checked 2026-10-05.
- [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28): Released (current), v2026.08.28, checked 2026-10-05.
- [OSPS Baseline v2026.08.28 checklist](https://baseline.openssf.org/versions/2026-08-28-checklist): Released (current), v2026.08.28, checked 2026-10-05.
- [OSPS Baseline v2026.08.28 external framework crosswalk](https://baseline.openssf.org/versions/2026-08-28-crosswalk): Released (current), v2026.08.28, checked 2026-10-05.
- [OSPS Baseline control catalog](https://github.com/ossf/security-baseline/tree/v2026.08.28/baseline): Released, tag v2026.08.28 (Gemara ControlCatalog), checked 2026-10-05.
- [OSPS Baseline mapping documents](https://github.com/ossf/security-baseline/tree/v2026.08.28/baseline/mappings): Released (mappings marked draft), tag v2026.08.28, checked 2026-10-05.
- [OSPS Baseline release v2026.08.28](https://github.com/ossf/security-baseline/releases/tag/v2026.08.28): Released, 2026-08-28, checked 2026-10-05.
- [OSPS Baseline release notes](https://baseline.openssf.org/release_notes): Released, entries 2025-02-25 to 2026-08-28, checked 2026-10-05.
- [OSPS Baseline v2026.02.19](https://baseline.openssf.org/versions/2026-02-19): Released (previous), checked 2026-10-05.
- [OSPS Baseline v2025.10.10](https://baseline.openssf.org/versions/2025-10-10): Released (previous), checked 2026-10-05.
- [OSPS Baseline v2025.02.25](https://baseline.openssf.org/versions/2025-02-25): Released (previous), checked 2026-10-05.
- [OSPS Baseline in-development version](https://baseline.openssf.org/versions/devel): In development, main at ca5dbf3, checked 2026-10-05.
- [OSPS Baseline Maintenance Process](https://baseline.openssf.org/maintenance): Process document, checked 2026-10-05.
- [OSPS Baseline FAQ](https://baseline.openssf.org/faq): Documentation, checked 2026-10-05.
- [OSPS Baseline Maintainer Guidance](https://baseline.openssf.org/maintainers): Documentation, checked 2026-10-05.
- [OpenSSF Scorecard check documentation](https://github.com/ossf/scorecard/blob/v5.5.0/docs/checks.md): Released, v5.5.0, checked 2026-10-05.
- [OpenSSF Scorecard README](https://github.com/ossf/scorecard/blob/v5.5.0/README.md): Released, v5.5.0, checked 2026-10-05.
- [OpenSSF Scorecard release v5.5.0](https://github.com/ossf/scorecard/releases/tag/v5.5.0): Released (latest), 2026-04-23, checked 2026-10-05.
- [OpenSSF Scorecard release v5.0.0](https://github.com/ossf/scorecard/releases/tag/v5.0.0): Released, 2024-07-19, checked 2026-10-05.
- [OpenSSF Scorecard v4 check documentation](https://github.com/ossf/scorecard/blob/v4.13.1/docs/checks.md): Released (superseded), v4.13.1, checked 2026-10-05.
- [OpenSSF Scorecard maintainer annotations](https://github.com/ossf/scorecard/blob/v5.5.0/config/README.md): Released, v5.5.0, checked 2026-10-05.
- [OpenSSF Scorecard OSPS Baseline coverage analysis](https://github.com/ossf/scorecard/blob/v5.5.0/docs/osps-baseline-coverage.md): Living document, analysed against Baseline v2026.02.19, checked 2026-10-05.
- [OpenSSF Scorecard roadmap](https://github.com/ossf/scorecard/blob/v5.5.0/docs/ROADMAP.md): Roadmap (Scorecard v6), checked 2026-10-05.
- [Scorecard GitHub Action](https://github.com/ossf/scorecard-action): Released, v2.4.4 (runs Scorecard v5.5.0), checked 2026-10-05.
- [scorecard.dev](https://scorecard.dev/): Project site, checked 2026-10-05.
