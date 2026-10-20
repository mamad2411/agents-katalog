---
name: web-platform-design-principles
description: >-
  Web Platform Design Principles: This document contains a set of design principles to be used when designing web platform technologies. Covers Web Platform Design Principles (track). Use when designing or reviewing a web platform feature. Triggers: Web Platform Design Principles, security and privacy questionnaire, fingerprinting.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Web Platform Design Principles

This document contains a set of design principles to be used when designing web platform technologies. These principles have been collected during the Technical Architecture Group’s discussions in reviewing developing specifications, and build upon the Ethical Web Principles [ethical-web-principles] . We encourage specification designers to read this document and use it as a resource when making design decisions.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when designing or reviewing a web platform feature.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Web Platform Design Principles (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **10.9. Do not expose new information through Client Hints.** "As it says in RFC 8942 §4.1 where client hints are defined: Therefore, features relying on this document to define Client Hint headers MUST NOT provide new information that is otherwise not made available to the application by the user agent, such as existing request headers, HTML, CSS, or JavaScript."
2. **1.1. Put user needs first (Priority of Constituencies).** "See also: The web should not cause harm to society The web must enhance individuals' control and power [RFC8890]"
3. **1.2. It should be safe to visit a web page.** "To work towards making sure the reality of safety on the web matches users' expectations, we can take complementary approaches when adding new features: We can improve the user interfaces through which the Web is used to make it clearer what users of the Web should (and should not) expect; We can change the technical foundations of the Web so that they match user expectations of privacy; We can…"
4. **1.3. Trusted user interface should be trustworthy.** "These trusted user interfaces must be able to be designed in a way that enables users to trust and verify that the information they provide is genuine, and hasn’t been spoofed or hijacked by the website."
5. **1.4. Design for user intent.** "Using such a feature should only be possible if the user’s expectation matches the feature’s consequences (e.g., the personal information it reveals or the state it changes)."
6. **1.4.1. Help users make good decisions.** "If users' decisions last longer than the current session, user agents should remind users that their past decision still applies."
7. **1.4.1. Help users make good decisions.** "APIs should include a way for sites to learn of the change in status."
8. **1.4.1. Help users make good decisions.** "When a typical user reads the question about a feature, they should immediately think of the associated risks."

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

- [Web Platform Design Principles](https://www.w3.org/TR/design-principles/): Note, design-principles NOTE-design-principles-20260914 (Note, 2026-09-14), checked 2026-10-06.
- [Self-Review Questionnaire: Security and Privacy](https://www.w3.org/TR/security-privacy-questionnaire/): Note, security-privacy-questionnaire (Note, 2025-04-18), checked 2026-10-06.
- [Self-Review Questionnaire: Societal Impact](https://www.w3.org/TR/societal-impact-questionnaire/): Draft Note, societal-impact-questionnaire (Draft Note, 2026-03-19), checked 2026-10-06.
- [Mitigating Browser Fingerprinting in Web Specifications](https://www.w3.org/TR/fingerprinting-guidance/): Note, fingerprinting-guidance (Note, 2025-09-25), checked 2026-10-06.
