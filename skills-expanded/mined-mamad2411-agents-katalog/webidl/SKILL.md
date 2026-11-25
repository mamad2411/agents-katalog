---
name: webidl
description: >-
  Web IDL: This standard defines an interface definition language, Web IDL, that can be used to describe interfaces that are intended to be implemented in web browsers. Covers Web IDL Living Standard. Use when writing or checking Web IDL. Triggers: Web IDL, interface.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Web IDL

This standard defines an interface definition language, Web IDL, that can be used to describe interfaces that are intended to be implemented in web browsers.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when writing or checking Web IDL.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Web IDL Living Standard (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Web IDL.** "Developers should refer to the Living Standard for the most current error corrections and other developments."
2. **2.1. Names.** "The identifier of any of the abovementioned IDL constructs (except operation arguments) must not be " constructor ", " toString ", or begin with a U+005F (_)."
3. **2.1. Names.** "Although the " toJSON " identifier is not a reserved identifier , it must only be used for regular operations that convert objects to JSON types , as described in § 2.5.3.1 toJSON ."
4. **2.1. Names.** "Within the set of IDL fragments that a given implementation supports, the identifier of every interface , namespace , dictionary , enumeration , callback function , callback interface and typedef must not be the same as the identifier of any other interface , namespace , dictionary , enumeration , callback function , callback interface or typedef ."
5. **2.2. Interfaces.** "An interface must not be declared such that its inheritance hierarchy has a cycle."
6. **2.2. Interfaces.** "The identifier of a partial interface definition must be the same as the identifier of an interface definition."
7. **2.2. Interfaces.** "Interfaces must be annotated with an [ Exposed ] extended attribute ."
8. **2.3. Interface mixins.** "The identifier of a partial interface mixin definition must be the same as the identifier of an interface mixin definition ."

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

- [Web IDL Living Standard](https://webidl.spec.whatwg.org/review-drafts/2026-09/): Review Draft, Review Draft 2026-09 (Review Draft, 2026-09), checked 2026-10-06.
