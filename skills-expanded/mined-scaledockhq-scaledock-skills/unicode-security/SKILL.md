---
name: unicode-security
description: >-
  Unicode Security Mechanisms (UTS #39): detect confusable and mixed-script text and restrict identifiers. Covers UTS #39. Use when detecting confusable or restricted Unicode text. Triggers: UTS 39, confusables.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Unicode Security Mechanisms (UTS #39)

the General Profile for Identifiers shall do so by conforming to either UTS-39-C1-1 or UTS-39-C1-2 .

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when detecting confusable or restricted Unicode text.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: UTS #39 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Unicode Security Mechanisms.** "Readers should be familiar with [ UTR36 ] before continuing."
2. **Unicode Security Mechanisms.** "2 Conformance An implementation claiming conformance to this specification must do so in conformance to the following clauses: UTS-39-C1 ."
3. **Unicode Security Mechanisms.** "Unicode Standard Annex #31, "Unicode Identifiers and Syntax" [ UAX31 ] provides a recommended method of determining which strings should qualify as identifiers."
4. **Unicode Security Mechanisms.** "Implementations of the General Profile for Identifiers that wish to retain ZWJ and ZWNJ should declare that they use a modification of the profile per Section 2, Conformance , and should ensure that they implement the restrictions described in Section 3.1.1, Joining Controls ."
5. **Unicode Security Mechanisms.** "The default Identifier_Type property value should be Uncommon_Use if no other categories apply."
6. **Unicode Security Mechanisms.** "Thus users of this data should be prepared for changes in successive versions, such as by having a backward compatibility policy in place for previously supported characters or registrations."
7. **Unicode Security Mechanisms.** "Restricted characters should be treated with caution when considering possible use in identifiers, and should be disallowed unless there is good reason to allow them in the environment in question."
8. **3.1.1 Joining Controls.** "Identifier systems that attempt to provide more natural representations of terms in "modern, customary usage" should allow these characters in input and display, but limit them to contexts in which they are necessary."

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

- [UTS #39](https://www.unicode.org/reports/tr39/): Unicode Technical Standard, UTS #39 (Unicode Technical Standard, 2026-10-06), checked 2026-10-06.
