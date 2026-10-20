---
name: privacy-principles
description: >-
  Privacy Principles: Privacy is an essential part of the web. Covers Privacy Principles (track), Ethical Web Principles (track). Use when reviewing a web feature against the W3C privacy and ethical principles. Triggers: Privacy Principles, Ethical Web Principles.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Privacy Principles

Privacy is an essential part of the web. This document provides definitions for privacy and related concepts that are applicable worldwide as well as a set of privacy principles that should guide the development of the web as a trustworthy platform. People using the web would benefit from a stronger relationship between technology and policy, and this document is written to work with both.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when reviewing a web feature against the W3C privacy and ethical principles.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Privacy Principles (default, posture track); Ethical Web Principles (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **How This Document Fits In.** "This document elaborates on the privacy principle from the Ethical Web Principles : "Security and privacy are essential." While it focuses on privacy, this should not be taken as an indication that privacy is always more important than other ethical web principles, and this document doesn't address how to balance the different ethical web principles if they come into conflict."
2. **How This Document Fits In.** "These regulatory mechanisms are separate; a law in one country does not (and should not) change the architecture of the whole web, and likewise web specifications cannot override any given law (although they can affect how easy it is to create and enforce law)."
3. **Audiences for this Document.** "Because this document guides privacy reviews of new standards, authors of web specifications should consult it early in the design to make sure their feature passes the review smoothly."
4. **List of Principles.** "websites user agents API designers Principle 1.5.2 : If a service needs to collect extra data from its users in order to protect those or other users, it must take extra technical and legal measures to ensure that this data can't be then used for other purposes, like to grow the service."
5. **List of Principles.** "websites user agents Principle 2.1 : A user agent should help its user present the identity they want in each context they are in, and should prevent or support recognition as appropriate."
6. **List of Principles.** "user agents Principle 2.2.1 : Sites , user agents , and other actors should restrict the data they transfer to what's either necessary to achieve their users' goals or aligns with their users' wishes and interests."
7. **List of Principles.** "websites user agents Principle 2.2.2 : Web APIs should be designed to minimize the amount of data that sites need to request to carry out their users' goals."
8. **List of Principles.** "Web APIs should also provide granularity and user controls over personal data that is communicated to sites ."

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

- [Privacy Principles](https://www.w3.org/TR/privacy-principles/): Statement, privacy-principles privacy-principles (Statement, 2025-05-15), checked 2026-10-06.
- [Ethical Web Principles](https://www.w3.org/TR/ethical-web-principles/): Statement, ethical-web-principles ethical-web-principles (Statement, 2024-12-12), checked 2026-10-06.
