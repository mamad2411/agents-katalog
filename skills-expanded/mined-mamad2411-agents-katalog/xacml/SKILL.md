---
name: xacml
description: >-
  XACML 3.0: write and evaluate attribute-based access control policies, with the JSON profile. Covers XACML 3.0, XACML JSON Profile 1.1. Use when writing or evaluating attribute-based access policies. Triggers: XACML, attribute-based access control.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# XACML

http://www.oasis-open.org/committees/download.php/43799/xacml-3.0-core-spec-csprd03-en.zip

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when writing or evaluating attribute-based access policies.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: XACML 3.0 (default); XACML JSON Profile 1.1 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.2 Terminology.** "The key words �MUST�, �MUST NOT�, �REQUIRED�, �SHALL�, �SHALL NOT�, �SHOULD�, �SHOULD NOT�, �RECOMMENDED�, �MAY�, and �OPTIONAL� in this document are to be interpreted as described in [RFC2119] ."
2. **2.12 Actions performed in conjunction with enforcement.** "In many applications, policies specify actions that MUST be performed, either instead of, or in addition to, actions that MAY be performed.� This idea was described by Sloman [Sloman94] .� XACML provides facilities to specify actions that MUST be performed in conjunction with policy evaluation in the <Obligations> element.� This idea was described as a provisional action by Kudo [Kudo00] .� There…"
3. **5.1 Element <PolicySet>.** "A <PolicySet> element may be evaluated, in which case the evaluation procedure defined in Section 7.13 SHALL be used."
4. **5.1 Element <PolicySet>.** "If a <PolicySet> element contains references to other policy sets or policies in the form of URLs, then these references MAY be resolvable.� Policy sets and policies included in a <PolicySet> element MUST be combined using the algorithm identified by the PolicyCombiningAlgId attribute.� <PolicySet> is treated exactly like a <Policy> in all policy-combining algorithms ."
5. **5.1 Element <PolicySet>.** "The <ObligationExpressions> element contains a set of obligation expressions that MUST be evaluated into obligations by the PDP and the resulting obligations MUST be fulfilled by the PEP in conjunction with the authorization decision .� If the PEP does not understand or cannot fulfill any of the obligations , then it MUST act according to the PEP bias.� See Section 7.2 and 7.18."
6. **5.1 Element <PolicySet>.** "The <AdviceExpressions> element contains a set of advice expressions that MUST be evaluated into advice by the PDP ."
7. **5.1 Element <PolicySet>.** "PolicyCombiningAlgId [Required] The identifier of the policy-combining algorithm by which the <PolicySet> , <CombinerParameters> , <PolicyCombinerParameters> and <PolicySetCombinerParameters> components MUST be combined.� Standard policy-combining algorithms are listed in Appendix Appendix C.� Standard policy-combining algorithm identifiers are listed in Section B.9."
8. **5.1 Element <PolicySet>.** "<PolicySetDefaults> [Optional] A set of default values applicable to the policy set .� The scope of the <PolicySetDefaults> element SHALL be the enclosing policy set ."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
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

- [XACML 3.0](https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-os-en.html): OASIS Standard, XACML 3.0 core, fetched 2026-10-06 (OASIS Standard, 2026-10-06), checked 2026-10-06.
- [XACML JSON Profile 1.1](https://docs.oasis-open.org/xacml/xacml-json-http/v1.1/xacml-json-http-v1.1.html): OASIS Standard, XACML JSON and HTTP profile 1.1, fetched 2026-10-06 (OASIS Standard, 2026-10-06), checked 2026-10-06.
