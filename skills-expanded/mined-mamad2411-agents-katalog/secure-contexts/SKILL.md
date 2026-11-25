---
name: secure-contexts
description: >-
  Secure Contexts: This specification defines "secure contexts", thereby allowing user agent implementers and specification authors to enable certain features only when certain minimum standards of authentication and confidentiality are met. Covers Secure Contexts (build), Mixed Content (build), Upgrade Insecure Requests (build). Use when deciding whether a context is secure, blocking mixed content, or upgrading insecure requests. Triggers: secure context, isSecureContext, mixed content, upgrade-insecure-requests.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Secure Contexts

This specification defines "secure contexts", thereby allowing user agent implementers and specification authors to enable certain features only when certain minimum standards of authentication and confidentiality are met.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when deciding whether a context is secure, blocking mixed content, or upgrading insecure requests.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Secure Contexts (default, posture build); Mixed Content (default, posture build); Upgrade Insecure Requests (default, posture build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **3.1. Is origin potentially trustworthy?.** "In particular, the user agent SHOULD treat file URLs as potentially trustworthy."
2. **5.2. localhost.** "as special, and suggests that local resolvers SHOULD/MAY treat them specially."
3. **1. Introduction.** "As an extension of the TAG’s recommendations in [SECURING-WEB] , this document describes threat models for feature abuse on the web (see § 4.1 Threat Models ) and outlines normative requirements which should be incorporated into documents specifying new features (see § 7 Implementation Considerations )."
4. **2.1. Integration with WebIDL.** "The following example should help: interface ExampleFeature { // This call will succeed in all contexts."
5. **4.1. Threat Models.** "The state of the Internet is such that we must indeed assume that a network attacker is present."
6. **4.3. Risks associated with non-secure contexts.** "Certain web platform features that have a distinct impact on a user’s security or privacy should be available for use only in secure contexts in order to defend against the threats above."
7. **4.3. Risks associated with non-secure contexts.** "This list is non-exhaustive, but should give you a feel for the types of risks we should consider when writing or implementing specifications."
8. **7.4. Restricting Legacy Features.** "If such a feature is in wide use, we recommend that the existing functionality be deprecated; the specification should be modified to note that it does not conform to the restrictions outlined in this document, and a plan should be developed to both offer a conformant version of the feature and to migrate existing users into that new version."

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

- [Secure Contexts](https://www.w3.org/TR/secure-contexts/): Candidate Recommendation Draft, secure-contexts CRD-secure-contexts-20231110 (Candidate Recommendation Draft, 2023-11-10), checked 2026-10-06.
- [Mixed Content](https://www.w3.org/TR/mixed-content/): Candidate Recommendation Draft, mixed-content CRD-mixed-content-20230223 (Candidate Recommendation Draft, 2023-02-23), checked 2026-10-06.
- [Upgrade Insecure Requests](https://www.w3.org/TR/upgrade-insecure-requests/): Candidate Recommendation Snapshot, upgrade-insecure-requests CR-upgrade-insecure-requests-20151008 (Candidate Recommendation Snapshot, 2015-10-08), checked 2026-10-06.
