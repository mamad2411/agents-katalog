---
name: uaag
description: >-
  User Agent Accessibility Guidelines (UAAG): UAAG 2.0 guides developers in designing user agents that make the web more accessible to people with disabilities. Covers User Agent Accessibility Guidelines (UAAG) 2.0 (track), User Agent Accessibility Guidelines 1.0. Use when reviewing a user agent against UAAG. Triggers: UAAG, UAAG 2.0, user agent accessibility.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# User Agent Accessibility Guidelines (UAAG)

UAAG 2.0 guides developers in designing user agents that make the web more accessible to people with disabilities. User agents include browsers, browser extensions, media players, readers and other applications that render web content . A user agent that follows UAAG 2.0 will improve accessibility through its own user interface and its ability to communicate with other technologies, including assistive technologies . UAAG and supporting resources are also intended to meet the needs of different audiences, including developers, policy makers, and managers. All users, not just users with disabilities, will benefit from user agents that follow UAAG 2.0. In addition to helping developers of brow

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when reviewing a user agent against UAAG.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: User Agent Accessibility Guidelines (UAAG) 2.0 (default, posture track); User Agent Accessibility Guidelines 1.0 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Appendix A: Glossary.** "The key words are "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" ."
2. **W3C Working Group Note of UAAG 2.0.** "Changed term "Content Specifications" in 5.1.2 Implement Accessibility Features of Content Specifications to "Web Content Technology Specifications" Comments on the Note should be sent to public-uaag2-comments@w3.org ( Public Archive )."
3. **Relationship to the Web Content Accessibility Guidelines (WCAG) 2.0.** "If the finished application is used to retrieve, render, and facilitate end-user interaction with web content of the end-users choosing, then the application should be considered a stand-alone user agent."
4. **UAAG 2.0 Conformance Applicability Notes:.** "RFC 2119 language not used: UAAG 2.0 does not use RFC 2119 language (must, may, should) as it is not an interoperable specifications."
5. **UAAG 2.0 Conformance Applicability Notes:.** "Mongolian, Han), success criteria normally relating to horizontal rendering should be applied to vertical rendering instead."
6. **1.5.1 Global Volume:.** "Note : If browsers provide speech output for mainstream users, they should make the speech configurable enough to be usable by a wide range of individuals."
7. **1.5.1 Global Volume:.** "When an add-on adds speech output to the user agent, it becomes part of the user agent, and therefore should meet the requirements of 1.6."
8. **1.6.2 Speech Pitch and Range:.** "A user agent should expose the availability of pitch and pitch range control if the currently selected or installed text to speech engine offers this capability."

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

- [User Agent Accessibility Guidelines (UAAG) 2.0](https://www.w3.org/TR/UAAG20/): Note, UAAG20 NOTE-UAAG20-Reference-20151215 (Note, 2015-12-15), checked 2026-10-06.
- [User Agent Accessibility Guidelines 1.0](https://www.w3.org/TR/UAAG10/): Recommendation, UAAG10 REC-UAAG10-20021217 (Recommendation, 2002-12-17), checked 2026-10-06.
