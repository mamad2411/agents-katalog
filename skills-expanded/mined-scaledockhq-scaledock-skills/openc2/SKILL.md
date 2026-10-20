---
name: openc2
description: >-
  OpenC2 1.0: send and answer standardized cybersecurity command and control messages. Covers OpenC2 Language 1.0. Use when sending cybersecurity commands. Triggers: OpenC2.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# OpenC2

https://docs.oasis-open.org/openc2/oc2ls/v1.0/cs02/oc2ls-v1.0-cs02.md (Authoritative)

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when sending cybersecurity commands.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: OpenC2 Language 1.0 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.2 Terminology.** "The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [ RFC2119 ] and [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
2. **3.1.4 Extensions.** "All extensions MUST be identified with a short namespace reference, called a namespace identifier (NSID)."
3. **3.1.4 Extensions.** "For example, the OASIS standard Stateless Packet Filtering actuator profile has: Unique Name : http://docs.oasis-open.org/openc2/oc2slpf/v1.0/oc2slpf-v1.0.md NSID : slpf The namespace identifier for non-standard extensions MUST be prefixed with "x-"."
4. **3.1.4 Extensions.** "For example, the fictional, non-standard Superwidget actuator profile has: Unique Name : http://www.acme.com/openc2/superwidget-v1.0.html NSID : x-acme The list of Actions in Section 3.3.1.1 SHALL NOT be extended."
5. **3.1.4 Extensions.** "Extended Target names MUST be prefixed with a namespace identifier followed by a colon (":")."
6. **3.1.4 Extensions.** "Extended Arguments MUST be defined within the extended Argument namespace."
7. **3.1.4 Extensions.** "} }, "args" : { "slpf" : { "direction" : "ingress" } } } The Actuator property of a Command, defined in Section 3.3.1.3 , MUST be extended using the namespace identifier as the Actuator name, called an extended Actuator namespace."
8. **3.1.4 Extensions.** "Actuator Specifiers MUST be defined within the extended Actuator namespace."

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

- [OpenC2 Language 1.0](https://docs.oasis-open.org/openc2/oc2ls/v1.0/oc2ls-v1.0.html): OASIS Standard, OpenC2 Language Specification 1.0, fetched 2026-10-06 (OASIS Standard, 2026-10-06), checked 2026-10-06.
