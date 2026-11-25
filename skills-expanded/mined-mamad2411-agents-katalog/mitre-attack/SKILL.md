---
name: mitre-attack
description: >-
  MITRE ATT&CK: versioned adversary behavior knowledge base. Covers ATT&CK v19.2. Use when mapping adversary behavior. Triggers: ATT&CK.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.2.0"
  kind: standard
---

# MITRE ATT&CK

MITRE ATT&CK, a knowledge base of adversary tactics, techniques, sub-techniques and procedures: the model from the ATT&CK Design and Philosophy paper, and how the v19.2 release is published as STIX 2.1 data in the mitre-attack/attack-stix-data repository at the v19.2 tag.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Threat intelligence analyst, detection engineer, red teamer, or a tool that maps findings to ATT&CK or reads the ATT&CK STIX data.
- Target version: ATT&CK v19.2 (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **§ 3.3.** "Tactics represent the “why” of an ATT&CK technique or sub-technique. It is the adversary’s tactical objective: the reason for performing an action."
2. **§ 3.4.** "Techniques represent “how” an adversary achieves a tactical objective by performing an action."
3. **§ 2.1.** "Anyone mapping to ATT&CK should be able to explain the procedures they cover."
4. **x_mitre_deprecated, revoked.** "Objects that are deemed no longer beneficial to track as part of the knowledge base are marked as deprecated, and objects which are replaced by a different object are revoked."
5. **x_mitre_deprecated, revoked.** "We recommend you filter out revoked and deprecated objects from your views whenever possible since they are no longer maintained by ATT&CK."

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
- [ ] Every mapping cites the ATT&CK version and the technique or sub-technique id (T#### or T####.###), and no mapping points to a revoked or deprecated object.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `mitre-atlas`, `stix-taxii`, `cwe`, `cve-json`, `ocsf`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [MITRE ATT&CK: Design and Philosophy](https://attack.mitre.org/docs/ATTACK_Design_and_Philosophy_March_2020.pdf): MITRE Product, MP180360R1, revised March 2020, checked 2026-10-06.
- [ATT&CK STIX Data: README](https://raw.githubusercontent.com/mitre-attack/attack-stix-data/v19.2/README.md): Data repository documentation, Tag v19.2, commit 6cda5ad8462c (2026-08-05), checked 2026-10-06.
- [ATT&CK STIX Data: USAGE](https://raw.githubusercontent.com/mitre-attack/attack-stix-data/v19.2/USAGE.md): Data repository documentation, Tag v19.2, commit 6cda5ad8462c (2026-08-05), checked 2026-10-06.
