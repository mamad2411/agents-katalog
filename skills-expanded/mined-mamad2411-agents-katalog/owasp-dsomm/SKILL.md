---
name: owasp-dsomm
description: >-
  OWASP DSOMM: assess and improve DevSecOps maturity by dimension and level. Covers OWASP DSOMM. Use when assessing DevSecOps maturity. Triggers: DSOMM.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# OWASP DSOMM

The OWASP DevSecOps Maturity Model (DSOMM): activities grouped by dimension (Build and Deployment, Culture and Organization, Implementation, Information Gathering, Test and Verification, Agentic AI) and sub-dimension, each with a maturity level from 1 to 5 and a measure. Read from the model's YAML data at a pinned release tag.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Owner or assessor of a DevSecOps program, team or pipeline, scoring or improving activities by level.
- Target version: OWASP DSOMM (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Build: Defined build process (level 1).** "Find a tool that suits your environment. Add your manual build steps, include steps for running tests, scanning and preparation for deployment."
2. **Identity and Access Management: MFA for admins (level 1).** "Two or more factor authentication for all privileged accounts on systems and applications."
3. **Consolidation: Treatment of defects with high or critical severity (level 1).** "Make it a rule that all _high_ or _critical_ security findings must be fixed before the software is approved for release or use."
4. **Static depth for infrastructure: Test for stored secrets in code (level 1).** "Test for secrets in code and git history"
5. **Logging: Centralized system logging (level 1).** "System logs must be stored in a central repository, protected from unauthorized access and modification."

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
- [ ] Each assessed activity is recorded with its dimension, sub-dimension, activity name and level, and level 1 activities are assessed before higher levels.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `owasp-samm`, `nist-ssdf`, `s2c2f`, `owasp-ci-cd-top-10`, `openssf-baseline`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [DSOMM Build and Deployment / Build](https://raw.githubusercontent.com/devsecopsmaturitymodel/DevSecOps-MaturityModel-data/v5.1.0/src/assets/YAML/default/BuildAndDeployment/Build.yaml): OWASP Project model data, Release v5.1.0 (2026-09-21), checked 2026-10-06.
- [DSOMM Build and Deployment / Deployment](https://raw.githubusercontent.com/devsecopsmaturitymodel/DevSecOps-MaturityModel-data/v5.1.0/src/assets/YAML/default/BuildAndDeployment/Deployment.yaml): OWASP Project model data, Release v5.1.0 (2026-09-21), checked 2026-10-06.
- [DSOMM Build and Deployment / Patch Management](https://raw.githubusercontent.com/devsecopsmaturitymodel/DevSecOps-MaturityModel-data/v5.1.0/src/assets/YAML/default/BuildAndDeployment/PatchManagement.yaml): OWASP Project model data, Release v5.1.0 (2026-09-21), checked 2026-10-06.
- [DSOMM Culture and Organization / Design](https://raw.githubusercontent.com/devsecopsmaturitymodel/DevSecOps-MaturityModel-data/v5.1.0/src/assets/YAML/default/CultureAndOrganization/Design.yaml): OWASP Project model data, Release v5.1.0 (2026-09-21), checked 2026-10-06.
- [DSOMM Culture and Organization / Education and Guidance](https://raw.githubusercontent.com/devsecopsmaturitymodel/DevSecOps-MaturityModel-data/v5.1.0/src/assets/YAML/default/CultureAndOrganization/EducationAndGuidance.yaml): OWASP Project model data, Release v5.1.0 (2026-09-21), checked 2026-10-06.
- [DSOMM Culture and Organization / Process](https://raw.githubusercontent.com/devsecopsmaturitymodel/DevSecOps-MaturityModel-data/v5.1.0/src/assets/YAML/default/CultureAndOrganization/Process.yaml): OWASP Project model data, Release v5.1.0 (2026-09-21), checked 2026-10-06.
- [DSOMM Implementation / Development and Source Control](https://raw.githubusercontent.com/devsecopsmaturitymodel/DevSecOps-MaturityModel-data/v5.1.0/src/assets/YAML/default/Implementation/DevelopmentAndSourceControl.yaml): OWASP Project model data, Release v5.1.0 (2026-09-21), checked 2026-10-06.
- [DSOMM Implementation / Application Hardening](https://raw.githubusercontent.com/devsecopsmaturitymodel/DevSecOps-MaturityModel-data/v5.1.0/src/assets/YAML/default/Implementation/ApplicationHardening.yaml): OWASP Project model data, Release v5.1.0 (2026-09-21), checked 2026-10-06.
- [DSOMM Implementation / Identity and Access Management](https://raw.githubusercontent.com/devsecopsmaturitymodel/DevSecOps-MaturityModel-data/v5.1.0/src/assets/YAML/default/Implementation/IdentityAndAccessManagement.yaml): OWASP Project model data, Release v5.1.0 (2026-09-21), checked 2026-10-06.
- [DSOMM Implementation / Infrastructure Hardening](https://raw.githubusercontent.com/devsecopsmaturitymodel/DevSecOps-MaturityModel-data/v5.1.0/src/assets/YAML/default/Implementation/InfrastructureHardening.yaml): OWASP Project model data, Release v5.1.0 (2026-09-21), checked 2026-10-06.
- [DSOMM Information Gathering / Logging](https://raw.githubusercontent.com/devsecopsmaturitymodel/DevSecOps-MaturityModel-data/v5.1.0/src/assets/YAML/default/InformationGathering/Logging.yaml): OWASP Project model data, Release v5.1.0 (2026-09-21), checked 2026-10-06.
- [DSOMM Information Gathering / Monitoring](https://raw.githubusercontent.com/devsecopsmaturitymodel/DevSecOps-MaturityModel-data/v5.1.0/src/assets/YAML/default/InformationGathering/Monitoring.yaml): OWASP Project model data, Release v5.1.0 (2026-09-21), checked 2026-10-06.
- [DSOMM Test and Verification / Consolidation](https://raw.githubusercontent.com/devsecopsmaturitymodel/DevSecOps-MaturityModel-data/v5.1.0/src/assets/YAML/default/TestAndVerification/Consolidation.yaml): OWASP Project model data, Release v5.1.0 (2026-09-21), checked 2026-10-06.
- [DSOMM Test and Verification / Static depth for infrastructure](https://raw.githubusercontent.com/devsecopsmaturitymodel/DevSecOps-MaturityModel-data/v5.1.0/src/assets/YAML/default/TestAndVerification/StaticDepthForInfrastructure.yaml): OWASP Project model data, Release v5.1.0 (2026-09-21), checked 2026-10-06.
- [DSOMM Agentic AI / Isolation](https://raw.githubusercontent.com/devsecopsmaturitymodel/DevSecOps-MaturityModel-data/v5.1.0/src/assets/YAML/default/AgenticAI/Isolation.yaml): OWASP Project model data, Release v5.1.0 (2026-09-21), checked 2026-10-06.
