---
name: permissions
description: >-
  Permissions: This specification defines common infrastructure that other specifications can use to interact with browser permissions. Covers Permissions (track), Permissions Policy Level 1 (track). Use when querying, requesting or specifying a powerful feature permission. Triggers: Permissions API, navigator.permissions, Permissions-Policy.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Permissions

This specification defines common infrastructure that other specifications can use to interact with browser permissions. These permissions represent a user's choice to allow or deny access to "powerful features" of the platform. For developers, the specification standardizes an API to query the permission state of a powerful feature, and be notified if a permission to use a powerful feature changes state.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when querying, requesting or specifying a powerful feature permission.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Permissions (default, posture track); Permissions Policy Level 1 (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **4..** "Specifying a powerful feature When a conforming specification specifies a powerful feature it: MUST give the powerful feature a name in the form of a ascii lowercase string."
2. **4..** "MUST register the powerful feature in the Permissions Registry ."
3. **4..** "A feature that specifies a custom permission key type MUST also specify a permission key generation algorithm ."
4. **4..** "A feature that specifies a custom permission key generation algorithm MUST also specify a permission key comparison algorithm ."
5. **4..** "A permission lifetime : Specifications that define one or more powerful features SHOULD suggest a permission lifetime that is best suited for the particular feature."
6. **6.2.1.** "query() method When the query() method is invoked, the user agent MUST run the following query a permission algorithm, passing the parameter permissionDesc : If this 's relevant global object is a Window object, then: If the current settings object 's associated Document is not fully active , return a promise rejected with an " InvalidStateError " DOMException ."
7. **6.3.5.** "Garbage collection A PermissionStatus object MUST NOT be garbage collected if it has an event listener whose type is change ."
8. **7. Conformance.** "The key words MAY , MUST , MUST NOT , OPTIONAL , and SHOULD in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."

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

- [Permissions](https://www.w3.org/TR/permissions/): Working Draft, permissions WD-permissions-20251006 (Working Draft, 2025-10-06), checked 2026-10-06.
- [Permissions Policy](https://www.w3.org/TR/permissions-policy-1/): Working Draft, permissions-policy-1 WD-permissions-policy-1-20260922 (Working Draft, 2026-09-22), checked 2026-10-06.
