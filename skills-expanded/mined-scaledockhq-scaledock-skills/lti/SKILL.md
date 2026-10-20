---
name: lti
description: >-
  LTI: The IMS Learning Tools Interoperability (LTI)® specification allows Learning Management Systems (LMS) or platforms to integrate remote tools and content in a standard way. Covers LTI 1.3. Use when integrating a learning tool. Triggers: LTI.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# LTI

The IMS Learning Tools Interoperability (LTI)® specification allows Learning Management Systems (LMS) or platforms to integrate remote tools and content in a standard way. LTI™ v1.3 builds on LTI v1.1 by incorporating a new model for security for message and service authentication.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when integrating a learning tool.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: LTI 1.3 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **IPR and Distribution Notice.** "ANY USE OF THIS SPECIFICATION SHALL BE MADE ENTIRELY AT THE IMPLEMENTER'S OWN RISK, AND NEITHER THE CONSORTIUM, NOR ANY OF ITS MEMBERS OR SUBMITTERS, SHALL HAVE ANY LIABILITY WHATSOEVER TO ANY IMPLEMENTER OR THIRD PARTY FOR ANY DAMAGES OF ANY NATURE WHATSOEVER, DIRECTLY OR INDIRECTLY, ARISING FROM THE USE OF THIS SPECIFICATION."
2. **1.2 Conformance Statements.** "The key words MAY , MUST , MUST NOT , OPTIONAL , RECOMMENDED , REQUIRED , SHALL , SHALL NOT , SHOULD , and SHOULD NOT in this document are to be interpreted as described in [ RFC2119 ]."
3. **1.2 Conformance Statements.** "An implementation of this specification that fails to implement a MUST/REQUIRED/SHALL requirement or fails to abide by a MUST NOT/SHALL NOT prohibition is considered nonconformant."
4. **1.2 Conformance Statements.** "SHOULD/SHOULD NOT/RECOMMENDED statements constitute a best practice."
5. **3.1.3 Tool Deployment.** "When a user deploys a tool within their tool platform, the platform MUST generate an immutable deployment_id identifier to identify the integration."
6. **3.1.3 Tool Deployment.** "A platform MUST generate a unique deployment_id for each tool it integrates with."
7. **3.1.3 Tool Deployment.** "Every message between the platform and tool MUST include the deployment_id in addition to the client_id ."
8. **3.1.3 Tool Deployment.** "A tool MUST thus allow multiple deployments on a given platform to share the same client_id and the security contract attached to it."

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

- [LTI 1.3](https://www.imsglobal.org/spec/lti/v1p3): Specification, LTI 1.3, fetched 2026-10-06 (Specification, 2026-10-06), checked 2026-10-06.
