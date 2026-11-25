---
name: owasp-scvs
description: >-
  OWASP SCVS: verify software components, SBOMs and supply chain controls by level. Covers OWASP SCVS. Use when verifying software components. Triggers: SCVS.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# OWASP SCVS

The OWASP Software Component Verification Standard (SCVS) 1.0: verification requirements V1 to V6 (inventory, SBOM, build environment, package management, component analysis, pedigree and provenance), read from the project's Markdown source at the 1.0 release tag.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Owner or assessor of a software supply chain: build pipeline, package repository, SBOM producer or consumer.
- Target version: OWASP SCVS (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **V1.1.** "All direct and transitive components and their versions are known at completion of a build"
2. **V2.9.** "SBOM contains a complete and accurate inventory of all components the SBOM describes"
3. **V3.1.** "Application uses a repeatable build"
4. **V4.13.** "Package manager verifies the integrity of packages when they are retrieved from remote repository"

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] The assessment names its target level (L1, L2 or L3), and every finding names its requirement id.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `cyclonedx`, `spdx`, `slsa`, `s2c2f`, `purl`, `owasp-ci-cd-top-10`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [V1: Inventory](https://raw.githubusercontent.com/OWASP/Software-Component-Verification-Standard/1.0/en/0x10-V1-Inventory.md): OWASP Standard, Tag 1.0 (2020-06-25), checked 2026-10-06.
- [V2: Software Bill of Materials](https://raw.githubusercontent.com/OWASP/Software-Component-Verification-Standard/1.0/en/0x11-V2-Software_Bill_of_Materials.md): OWASP Standard, Tag 1.0 (2020-06-25), checked 2026-10-06.
- [V3: Build Environment](https://raw.githubusercontent.com/OWASP/Software-Component-Verification-Standard/1.0/en/0x12-V3-Build_Environment.md): OWASP Standard, Tag 1.0 (2020-06-25), checked 2026-10-06.
- [V4: Package Management](https://raw.githubusercontent.com/OWASP/Software-Component-Verification-Standard/1.0/en/0x13-V4-Package_Management.md): OWASP Standard, Tag 1.0 (2020-06-25), checked 2026-10-06.
- [V5: Component Analysis](https://raw.githubusercontent.com/OWASP/Software-Component-Verification-Standard/1.0/en/0x14-V5-Component_Analysis.md): OWASP Standard, Tag 1.0 (2020-06-25), checked 2026-10-06.
- [V6: Pedigree and Provenance](https://raw.githubusercontent.com/OWASP/Software-Component-Verification-Standard/1.0/en/0x15-V6-Pedigree_and_Provenance.md): OWASP Standard, Tag 1.0 (2020-06-25), checked 2026-10-06.
