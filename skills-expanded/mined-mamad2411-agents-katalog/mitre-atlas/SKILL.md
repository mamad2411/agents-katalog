---
name: mitre-atlas
description: >-
  MITRE ATLAS 2026.09: map AI threats to ATLAS tactics, techniques,
  sub-techniques, mitigations and case studies, and parse the ATLAS YAML data.
  Use when threat-modeling an AI, LLM or agentic system, planning or reporting
  an AI red team exercise, tagging detections or incidents with ATLAS IDs, or
  loading atlas-data files. Covers the 16-tactic matrix (AML.TA*), techniques
  and sub-techniques (AML.T*) with maturity (Feasible, Demonstrated, Realized)
  and platforms (Predictive AI, Generative AI, Agentic AI, Enterprise),
  mitigations (AML.M*), case studies (AML.CS*), the agentic techniques in
  2026.09, the link to MITRE ATT&CK through attack-reference, and the
  STIX and Navigator outputs. Targets content release ATLAS 2026.09 in ATLAS
  YAML format 6.0.0 (dist/ATLAS-latest.yaml); upgrades from 2026.06 and earlier
  (retired AML.T0019, AML.T0058, AML.T0104, AML.T0045) and from the deprecated
  ATLAS.yaml legacy format. Triggers: ATLAS matrix, adversarial ML, prompt
  injection AML.T0051, AI agent tool poisoning, AI red team.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# MITRE ATLAS

MITRE ATLAS (Adversarial Threat Landscape for Artificial-Intelligence Systems) is MITRE's knowledge base of adversary tactics and techniques against AI-enabled systems, built from real-world attacks and red team demonstrations and published as monthly data releases in `mitre-atlas/atlas-data`. With this skill the agent produces ATLAS-mapped threat models, red team plans and findings, detection tags, and code that reads the ATLAS data.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the file, section or object ID it cites. ATLAS has no numbered sections, so rules cite the README section, the schema model, the changelog release or the ATLAS object (for example AML.M0035). When a rule and the pinned source disagree, the source wins; when the source has a newer release than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: threat modeler, red team, detection engineer, incident responder, or developer of a tool that reads ATLAS data.
- System in scope: the AI components (predictive model, LLM feature, agent with tools or memory) and the surrounding IT. This decides the platforms.
- Target version: ATLAS 2026.09 content (current, the default) in ATLAS YAML format 6.0.0 (current). ATLAS 2026.06 and ATLAS 2021.10 are legacy content lines, and the ATLAS legacy YAML format is legacy: read them and upgrade from them, never author new work against them. No preview exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned release in [Sources](#sources) (tag `v2026.09`, released 2026-09-15), unless the user names another.
- Output: threat model table, red team plan or report, detection mapping, or parsed data.
- Sources: when refreshing this skill or when a rule looks out of date, check the latest release of `mitre-atlas/atlas-data` and the "Data" version on the ATLAS General Information page, read the changelog entries since the pin for retired or renamed IDs, re-read every URL in [Sources](#sources), regenerate the tables in `references/`, and update the pins.

## Invariants

1. **Cite IDs with the release.** Tactics are `AML.TA####`, techniques `AML.T####`, sub-techniques `AML.T####.###`, mitigations `AML.M####`, case studies `AML.CS####` (README, ID conventions; `atlas/schemas.py`). Names change between releases, for example AML.TA0001 became "AI Attack Adaptation" in 2026.08 (CHANGELOG 2026.08), so every artifact records the ATLAS release it maps to.
2. **Never use a retired ID in new work.** Retired IDs are removed from later data files, not marked: AML.T0019, AML.T0058 and AML.T0104 became AML.T0115.000 to `.002` (CHANGELOG 2026.07), and AML.T0045 became AML.T0048.004 (CHANGELOG 4.5.0).
3. **Tactics come from `achieves` relationships.** A technique can achieve several tactics (AML.T0053 achieves Execution, Privilege Escalation and Lateral Movement), so a mapped step names its tactic as well; case study `employs` relationships require `tactic` (`EmploysRelationshipFields`).
4. **Sub-techniques belong to one parent.** Each has exactly one `specializes` relationship to an `AML.T####` parent (`SpecializesRelationshipFields`).
5. **Maturity is evidence of use.** Feasible means shown in research, Demonstrated means shown in a red team or demonstration on a realistic system, Realized means used by a threat actor in a real incident (CHANGELOG 5.0.0). Every technique has a maturity and one or more platforms (`Technique`, `TechniqueFields`).
6. **ATLAS and ATT&CK are separate namespaces.** An adapted tactic, technique or mitigation links to ATT&CK only through `attack-reference` (`TacticFields`, `TechniqueFields`, `MitigationFields`); the matrix page marks these with `&`. AML.TA0000 and AML.TA0001 have no ATT&CK counterpart.
7. **Mitigations prevent; they are not detections.** A mitigation reaches techniques only through `mitigates` relationships, each with a description of how it applies (README, Relationship types; Mitigations page). ATLAS 2026.09 has no detection or data source objects (`atlas/schemas.py`).
8. **Parse format 6.0.0, not `dist/ATLAS.yaml`.** `dist/ATLAS.yaml` is deprecated and no longer updated; `dist/ATLAS-latest.yaml` is the latest content in the latest format (README, Distributed Versions).
9. **UUIDs are derived, not invented.** `uuid` is UUIDv5 of the object ID in the `atlas.mitre.org.` namespace, and the validator rejects a mismatch (`AtlasObject.uuid`).
10. **Only published techniques.** Agentic and other techniques are cited only as they appear in the release you read; anything else is mapped to the nearest existing technique, not given a made-up ID.

## Workflow

1. **Pick the version.** Use ATLAS 2026.09 and format 6.0.0. If the input cites an older release or uses the legacy YAML, plan the upgrade (step 8).
   -> [`references/versions.md`](references/versions.md)
   ✓ The artifact names ATLAS v2026.09, and no legacy line is the target.
2. **Load the data** (tooling only). Read `dist/v6/ATLAS-2026.09.yaml` or `dist/ATLAS-latest.yaml`, validate it, and build indexes from `relationships`.
   -> [`references/data-format.md`](references/data-format.md)
   ✓ `format-version` is `6.0.0`, `collection.version` is `2026.09`, and every relationship endpoint exists.
3. **Scope the system.** Describe components, trust boundaries, data flows and access points, pick the platforms, and define the adversary (AML.M0035, Plan and Scope).
   -> [`references/threat-modeling.md`](references/threat-modeling.md)
   ✓ Each component maps to at least one platform, and the adversary's objectives, access and capabilities are written down.
4. **Select tactics and techniques.** Walk the matrix in order and keep techniques the components expose; use sub-techniques when one fits; use case studies as attack paths.
   -> [`references/tactics-and-techniques.md`](references/tactics-and-techniques.md)
   ✓ Every threat vector has a tactic ID and a technique or sub-technique ID that exist in 2026.09.
5. **Attach mitigations.** List mitigations per technique from `mitigates` edges, with their descriptions and status.
   -> [`references/mitigations.md`](references/mitigations.md)
   ✓ Every in-scope technique has mitigations marked in place, planned or not applicable, and gaps are listed.
6. **Plan or report the red team.** Follow the three AML.M0035 phases, tag each test and finding with tactic and technique IDs, and clean up exercise artifacts.
   -> [`references/threat-modeling.md`](references/threat-modeling.md)
   ✓ Rules of engagement and stop conditions exist, and every finding has an owner and a retest.
7. **Map detections.** Log what AML.M0024 lists, tag each rule with ATLAS and, where `attack-reference` exists, ATT&CK IDs, and report coverage per tactic.
   -> [`references/threat-modeling.md`](references/threat-modeling.md)
   ✓ Every detection names the technique and tactic it covers, and coverage gaps are visible.
8. **Upgrade** (only when asked). Apply each step from the source release to 2026.09: replace retired IDs, update renamed names, and convert legacy YAML to format 6.0.0.
   -> [`references/versions.md`](references/versions.md)
   ✓ Every ID resolves in `dist/v6/ATLAS-2026.09.yaml`, and the mappings mean what they meant before.

## Verify before done

- [ ] Every ATLAS ID matches its pattern and exists in `dist/v6/ATLAS-2026.09.yaml`.
- [ ] The artifact states the ATLAS release (v2026.09).
- [ ] No retired ID (AML.T0019, AML.T0058, AML.T0104, AML.T0045) appears in new work.
- [ ] Every mapped step names a tactic that its technique `achieves`.
- [ ] ATT&CK IDs appear only where the ATLAS object has an `attack-reference`, and they are labelled as ATT&CK.
- [ ] Mitigations are cited with the per-technique `mitigates` description; detections are listed separately.
- [ ] Code reads format 6.0.0 and checks `format-version`; it does not read `dist/ATLAS.yaml`.
- [ ] No agentic or other technique is cited that the release does not contain.

## Reference index

- **`references/versions.md`**: the content and format lines, what each release changed, retired and renamed IDs, and upgrade steps. Load for steps 1 and 8.
- **`references/tactics-and-techniques.md`**: the model (tactics, techniques, sub-techniques, maturity, platforms), the ATT&CK relationship, multi-tactic techniques, the agentic techniques, and the full 2026.09 matrix. Load for step 4.
- **`references/mitigations.md`**: categories, lifecycle phases, coverage queries, every 2026.09 mitigation, and the agent-specific ones. Load for step 5.
- **`references/data-format.md`**: files and manifest, format 6.0.0 fields, ID patterns, relationships, validation, STIX and Navigator output, and the legacy format. Load for steps 2 and 8.
- **`references/threat-modeling.md`**: threat modeling, the AML.M0035 red team phases, detection mapping, and common mistakes. Load for steps 3, 6 and 7.

## Related skills

- `owasp-llm` for the OWASP Top 10 for LLM Applications, a risk list to cross-reference with ATLAS techniques: `npx skills add ScaleDockHQ/scaledock-skills --skill owasp-llm`.
- `owasp-agentic` for OWASP's agentic AI threats and mitigations: `npx skills add ScaleDockHQ/scaledock-skills --skill owasp-agentic`.
- `nist-ai-rmf` for the NIST AI Risk Management Framework that an ATLAS threat model can feed: `npx skills add ScaleDockHQ/scaledock-skills --skill nist-ai-rmf`.
- `ocsf` for carrying ATLAS IDs on security findings and detection events: `npx skills add ScaleDockHQ/scaledock-skills --skill ocsf`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [MITRE ATLAS website](https://atlas.mitre.org/): released, Data v2026.09 (Website v5.4.1), checked 2026-10-05.
- [mitre-atlas/atlas-data README](https://github.com/mitre-atlas/atlas-data/blob/v2026.09/README.md): released, tag v2026.09 (commit 3259f38), checked 2026-10-05.
- [ATLAS release v2026.09](https://github.com/mitre-atlas/atlas-data/releases/tag/v2026.09): released, latest release 2026-09-15 (not a pre-release), checked 2026-10-05.
- [ATLAS-2026.09.yaml (format 6.0.0)](https://github.com/mitre-atlas/atlas-data/blob/v2026.09/dist/v6/ATLAS-2026.09.yaml): released, content 2026.09, checked 2026-10-05.
- [ATLAS Data CHANGELOG](https://github.com/mitre-atlas/atlas-data/blob/v2026.09/CHANGELOG.md): released, 1.0.0 to 2026.09, checked 2026-10-05.
- [ATLAS release manifest](https://github.com/mitre-atlas/atlas-data/blob/v2026.09/dist/manifest.yaml): released, 2021.05 to 2026.09, checked 2026-10-05.
- [ATLAS format 6.0.0 schema (atlas/schemas.py)](https://github.com/mitre-atlas/atlas-data/blob/v2026.09/atlas/schemas.py): released, format 6.0.0, checked 2026-10-05.
- [ATLAS enums (atlas/enums.py)](https://github.com/mitre-atlas/atlas-data/blob/v2026.09/atlas/enums.py): released, format 6.0.0, checked 2026-10-05.
- [ATLAS to STIX tool (tools/atlas_to_stix.py)](https://github.com/mitre-atlas/atlas-data/blob/v2026.09/tools/atlas_to_stix.py): released, tag v2026.09, checked 2026-10-05.
- [Deprecated ATLAS.yaml (legacy format)](https://github.com/mitre-atlas/atlas-data/blob/v2026.09/dist/ATLAS.yaml): deprecated, 5.6.0, checked 2026-10-05.
- [mitre-atlas/atlas-navigator-data](https://github.com/mitre-atlas/atlas-navigator-data): deprecated, last pushed 2026-06-24 (outputs moved to atlas-data releases), checked 2026-10-05.
