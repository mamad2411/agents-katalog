---
name: open-badges
description: >-
  Open Badges: This specification is a new version of the 1EdTech Open Badges Specification that aligns with the conventions of the Verifiable Credentials Data Model v2.0 for the use cases of Defined Achievement Claim and a Skill Claim . Covers Open Badges 3.0. Use when issuing an Open Badge. Triggers: Open Badges.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Open Badges

This specification is a new version of the 1EdTech Open Badges Specification that aligns with the conventions of the Verifiable Credentials Data Model v2.0 for the use cases of Defined Achievement Claim and a Skill Claim . The credentials that are produced are easily be bundled into Comprehensive Learner Records and Verifiable Presentations . Portability and learner data privacy are improved by expanding the usage of cryptographic proofs/signatures, because this format will be compatible with a growing array of proof schemas that are developed for the Verifiable Credentials Data Model.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when issuing an Open Badge.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Open Badges 3.0 (default). See `references/versions.md`.
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **IPR and Distribution Notice.** "ANY USE OF THIS SPECIFICATION SHALL BE MADE ENTIRELY AT THE IMPLEMENTER'S OWN RISK, AND NEITHER THE CONSORTIUM, NOR ANY OF ITS MEMBERS OR SUBMITTERS, SHALL HAVE ANY LIABILITY WHATSOEVER TO ANY IMPLEMENTER OR THIRD PARTY FOR ANY DAMAGES OF ANY NATURE WHATSOEVER, DIRECTLY OR INDIRECTLY, ARISING FROM THE USE OF THIS SPECIFICATION."
2. **1.3 Conformance Statements.** "The key words MAY , MUST , MUST NOT , NOT RECOMMENDED , NOT REQUIRED , OPTIONAL , RECOMMENDED , REQUIRED , SHALL , SHALL NOT , SHOULD , and SHOULD NOT in this document are to be interpreted as described in [ RFC2119 ]."
3. **1.3 Conformance Statements.** "An implementation of this specification that fails to implement a MUST/REQUIRED/SHALL requirement or fails to abide by a MUST NOT/SHALL NOT prohibition is considered nonconformant."
4. **1.3 Conformance Statements.** "SHOULD/SHOULD NOT/RECOMMENDED statements constitute a best practice."
5. **2.4 Achievement Credentials.** "Verifiers of AchievementCredentials that are aware of a specific defined achievement SHOULD ensure that the issued AchievementCredential is issued by an issuer they trust to recognize this achievement, usually the creator of the achievement."
6. **2.4.1 Differentiating Issuers and Achievement Creators.** "When an Achievement does not include a reference to its creator, verifiers SHOULD interpret it as an entity associated with the credential issuer."
7. **2.4.1 Differentiating Issuers and Achievement Creators.** "Verifiers SHOULD ensure that they trust a particular credential's issuer to recognize the accomplishments described by the Achievement it contains."
8. **2.4.1 Differentiating Issuers and Achievement Creators.** "Verifiers SHOULD NOT trust that an issuer has accurately represented the creator or data of an achievement definition within a credential when that entity is authored by another party, but SHOULD understand that the data within the credential is the data the issuer wished to recognize, even if the verifier encounters a different representation of that data elsewhere."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> `references/versions.md`
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in `references/requirements.md` and implement each one that applies to the role.
   -> `references/requirements.md`
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> `references/versions.md`
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in `references/requirements.md` holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Open Badges 3.0](https://www.imsglobal.org/spec/ob/v3p0/): Specification, Open Badges 3.0 (Specification, 2026-10-06), checked 2026-10-06.
