---
name: atag
description: >-
  Authoring Tool Accessibility Guidelines (ATAG): The Authoring Tool Accessibility Guidelines (ATAG) 2.0 provides guidelines for designing web content authoring tools that are both more accessible to authors with disabilities (Part A) and designed to enable, support, and promote the production of more accessible web content by all authors (Part B). Covers Authoring Tool Accessibility Guidelines (ATAG) 2.0. Use when building or reviewing an authoring tool for accessibility. Triggers: ATAG, ATAG 2.0, authoring tool accessibility.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Authoring Tool Accessibility Guidelines (ATAG)

The Authoring Tool Accessibility Guidelines (ATAG) 2.0 provides guidelines for designing web content authoring tools that are both more accessible to authors with disabilities (Part A) and designed to enable, support, and promote the production of more accessible web content by all authors (Part B). See Authoring Tool Accessibility Guidelines (ATAG) Overview for an introduction and links to ATAG technical and educational material.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when building or reviewing an authoring tool for accessibility.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Authoring Tool Accessibility Guidelines (ATAG) 2.0 (default); Authoring Tool Accessibility Guidelines 1.0 (legacy: read and upgrade, never author). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **ATAG 2.0 Layers of Guidance.** "The guidelines provide the basic goals that authoring tool developers should work toward in order to make authoring tools more accessible to both authors and end users of web content with different disabilities."
2. **Integration of Accessibility Features.** "When implementing ATAG 2.0, authoring tool developers should carefully integrate features that support more accessible authoring into the same "look-and-feel" as other features of the authoring tool ."
3. **Part A Conformance Applicability Notes:.** "Conformance claims are optional, but any claim that is made must record the user agent(s) ."
4. **A.1.2.1 Accessibility Guidelines:.** "( Level A ) Note: The (optional) explanation of conformance claim results should record the user interface accessibility guidelines that were followed."
5. **A.1.2.2 Platform Accessibility Services:.** "( Level A ) Note: The (optional) explanation of conformance claim results should record the platform accessibility service(s) that were implemented."
6. **A.3.1.1 Keyboard Access (Minimum):.** "Note 3: This success criterion does not forbid and should not discourage other input methods (e.g."
7. **Part B Conformance Applicability Notes:.** "Accessibility of features provided to meet Part B: The Part A success criteria apply to the entire authoring tool user interface , including any features that must be present to meet the success criteria in Part B (e.g."
8. **Part B Conformance Applicability Notes:.** "Accessible content support features should be made available to any authoring role where it would be useful."

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

- `wcag`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill wcag`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Authoring Tool Accessibility Guidelines (ATAG) 2.0](https://www.w3.org/TR/ATAG20/): Recommendation, ATAG20 NOTE-IMPLEMENTING-ATAG20-20150924 (Recommendation, 2015-09-24), checked 2026-10-06.
- [Authoring Tool Accessibility Guidelines 1.0](https://www.w3.org/TR/ATAG10/): Recommendation, ATAG10 REC-ATAG10-20000203 (Recommendation, 2000-02-03), checked 2026-10-06.
