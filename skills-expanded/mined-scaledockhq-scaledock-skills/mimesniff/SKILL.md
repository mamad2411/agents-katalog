---
name: mimesniff
description: >-
  MIME Sniffing: The MIME Sniffing standard defines sniffing resources. Covers MIME Sniffing Living Standard. Use when sniffing a MIME type. Triggers: MIME sniffing.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# MIME Sniffing

The MIME Sniffing standard defines sniffing resources.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when sniffing a MIME type.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: MIME Sniffing Living Standard (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2. Conformance requirements.** "The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119."
2. **MIME Sniffing.** "Developers should refer to the Living Standard for the most current error corrections and other developments."
3. **5. Handling a resource.** "For each resource it handles, the user agent must keep track of the following associated metadata: A supplied MIME type , the MIME type determined by the supplied MIME type detection algorithm ."
4. **5.1. Interpreting the resource metadata.** "To determine the supplied MIME type of a resource , user agents must use the following supplied MIME type detection algorithm : Let supplied-type be null."
5. **7. Determining the computed MIME type of a resource.** "To determine the computed MIME type of a resource , user agents must use the following MIME type sniffing algorithm : If the supplied MIME type is an XML MIME type or HTML MIME type , the computed MIME type is the supplied MIME type ."
6. **7.1. Identifying a resource with an unknown MIME type.** "If the setting of the sniff-scriptable flag is not specified when calling the rules for identifying an unknown MIME type , the sniff-scriptable flag must default to unset."
7. **7.1. Identifying a resource with an unknown MIME type.** "However, user agents should not implicitly extend this table to include additional byte patterns for any computed MIME type already present in this table, as doing so could introduce privilege escalation vulnerabilities."
8. **7.1. Identifying a resource with an unknown MIME type.** "User agents must not introduce any privilege escalation vulnerabilities when extending this table."

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

- [MIME Sniffing Living Standard](https://mimesniff.spec.whatwg.org/review-drafts/2026-07/): Review Draft, Review Draft 2026-07 (Review Draft, 2026-07), checked 2026-10-06.
