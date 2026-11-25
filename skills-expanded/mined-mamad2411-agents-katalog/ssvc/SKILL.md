---
name: ssvc
description: >-
  SSVC: prioritize vulnerability responses with Stakeholder-Specific Vulnerability Categorization decision trees. Covers SSVC. Use when prioritizing vulnerabilities with SSVC. Triggers: SSVC.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# SSVC

Stakeholder-Specific Vulnerability Categorization (SSVC) from the CERT Coordination Center: decision points such as Exploitation, Automatable, Technical Impact, System Exposure and Human Impact, and the outcomes they lead to (Defer, Scheduled, Out-of-Cycle, Immediate for deployers; Track, Track*, Attend, Act for CISA). Read from the decision point JSON data and the deployer documentation in the CERTCC/SSVC repository at a pinned release.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Deployer, Supplier, Coordinator or CISA-style analyst deciding the response priority for a vulnerability.
- Target version: SSVC (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Exploitation.** "Shared, observable, reliable evidence that the exploit is being used in the wild by real attackers; there is credible public reporting."
2. **Automatable.** "Can an attacker reliably automate creating exploitation events for this vulnerability?"
3. **Technical Impact.** "The exploit gives the adversary total control over the behavior of the software, or it gives total disclosure of all information on the system that contains the vulnerability."
4. **Human Impact.** "Human Impact is a combination of Safety and Mission impacts."
5. **Immediate.** "Act immediately; focus all resources on applying the fix as quickly as possible, including, if necessary, pausing regular organization operations."

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
- [ ] Each decision records the stakeholder, the decision point values chosen (with each decision point's version) and the resulting outcome.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `cvss`, `epss`, `cisa-kev`, `cve-json`, `csaf`, `openvex`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [SSVC decision point: Exploitation 1.1.0](https://raw.githubusercontent.com/CERTCC/SSVC/2026.7.0/data/json/decision_points/ssvc/exploitation_1_1_0.json): CERT/CC decision point, Release 2026.7.0, commit e3b00a256158 (2026-07-20), checked 2026-10-06.
- [SSVC decision point: Automatable 2.0.0](https://raw.githubusercontent.com/CERTCC/SSVC/2026.7.0/data/json/decision_points/ssvc/automatable_2_0_0.json): CERT/CC decision point, Release 2026.7.0, commit e3b00a256158 (2026-07-20), checked 2026-10-06.
- [SSVC decision point: Technical Impact 1.0.0](https://raw.githubusercontent.com/CERTCC/SSVC/2026.7.0/data/json/decision_points/ssvc/technical_impact_1_0_0.json): CERT/CC decision point, Release 2026.7.0, commit e3b00a256158 (2026-07-20), checked 2026-10-06.
- [SSVC decision point: System Exposure 1.0.1](https://raw.githubusercontent.com/CERTCC/SSVC/2026.7.0/data/json/decision_points/ssvc/system_exposure_1_0_1.json): CERT/CC decision point, Release 2026.7.0, commit e3b00a256158 (2026-07-20), checked 2026-10-06.
- [SSVC decision point: Mission Impact 2.0.0](https://raw.githubusercontent.com/CERTCC/SSVC/2026.7.0/data/json/decision_points/ssvc/mission_impact_2_0_0.json): CERT/CC decision point, Release 2026.7.0, commit e3b00a256158 (2026-07-20), checked 2026-10-06.
- [SSVC decision point: Human Impact 2.0.2](https://raw.githubusercontent.com/CERTCC/SSVC/2026.7.0/data/json/decision_points/ssvc/human_impact_2_0_2.json): CERT/CC decision point, Release 2026.7.0, commit e3b00a256158 (2026-07-20), checked 2026-10-06.
- [SSVC decision point: Value Density 1.0.0](https://raw.githubusercontent.com/CERTCC/SSVC/2026.7.0/data/json/decision_points/ssvc/value_density_1_0_0.json): CERT/CC decision point, Release 2026.7.0, commit e3b00a256158 (2026-07-20), checked 2026-10-06.
- [SSVC decision point: CISA Levels 1.1.0](https://raw.githubusercontent.com/CERTCC/SSVC/2026.7.0/data/json/decision_points/cisa/cisa_levels_1_1_0.json): CERT/CC decision point, Release 2026.7.0, commit e3b00a256158 (2026-07-20), checked 2026-10-06.
- [SSVC: Prioritizing Patch Deployment (Deployer decision model)](https://raw.githubusercontent.com/CERTCC/SSVC/2026.7.0/docs/howto/deployer_tree.md): CERT/CC documentation, Release 2026.7.0, commit e3b00a256158 (2026-07-20), checked 2026-10-06.
