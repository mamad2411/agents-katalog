---
name: odrl
description: >-
  ODRL: The Open Digital Rights Language (ODRL) is a policy expression language that provides a flexible and interoperable information model, vocabulary, and encoding mechanisms for representing statements about the usage of content and services. Covers ODRL Information Model 2.2, ODRL Vocabulary & Expression 2.2. Use when expressing permissions and obligations. Triggers: ODRL, Open Digital Rights Language.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# ODRL

The Open Digital Rights Language (ODRL) is a policy expression language that provides a flexible and interoperable information model, vocabulary, and encoding mechanisms for representing statements about the usage of content and services. The ODRL Information Model describes the underlying concepts, entities, and relationships that form the foundational basis for the semantics of the ODRL policies. Policies are used to represent permitted and prohibited actions over a certain asset, as well as the obligations required to be meet by stakeholders. In addition, policies may be limited by constraints (e.g., temporal or spatial constraints) and duties (e.g. payments) may be imposed on permissions

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when expressing permissions and obligations.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: ODRL Information Model 2.2 (default); ODRL Vocabulary & Expression 2.2 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **§ 2.1.** "A Policy MUST have one uid property value (of type IRI [rfc3987]) to identify the Policy."
2. **§ 2.1.** "A Policy MUST have at least one permission, prohibition, or obligation property values of type Rule."
3. **§ 2.5.** "When multiple Constraints apply to the same Rule, Action, Party/Asset Collection, then they are interpreted as conjunction and all MUST be satisfied."
4. **§ 2.5.1.** "Only one of rightOperand or rightOperandReference MUST appear in the Constraint."
5. **§ 2.6.** "A Rule MUST have one action property value of type Action."
6. **§ 2.6.1.** "A Permission MUST have one target property value of type Asset."
7. **§ 2.8.** "If a Policy has the dc:isReplacedBy property, then a processor MUST consider the first Policy void and MUST retrieve and process the identified Policy."
8. **§ 2.10.** "If a Policy has multiple conflict property values (for example, after a Policy merge or inheritance) and there are conflicting Rules then the entire Policy MUST be void."
9. **§ 3.2.** "If the ODRL Processing system does not recognise the ODRL Profile identifier(s) then it MUST stop processing the policy."
10. **§ 3.2.1.** "An Agreement Policy MUST contain at least one Permission or Prohibition rule, a Party with Assigner function, and a Party with Assignee function (in the same Permission or Prohibition)."
11. **§ 5.** "Implementations of ODRL expressions must be serialised using the UTF-8 character encoding."

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
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [ODRL Information Model 2.2](https://www.w3.org/TR/odrl-model/): Recommendation, odrl-model REC-odrl-model-20180215 (Recommendation, 2018-02-15), checked 2026-10-06.
- [ODRL Vocabulary & Expression 2.2](https://www.w3.org/TR/odrl-vocab/): Recommendation, odrl-vocab REC-odrl-vocab-20180215 (Recommendation, 2018-02-15), checked 2026-10-06.
