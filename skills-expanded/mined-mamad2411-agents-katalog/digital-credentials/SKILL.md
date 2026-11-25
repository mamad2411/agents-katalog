---
name: digital-credentials
description: >-
  Digital Credentials API: This document specifies an API enabling user agents to mediate the presentation and issuance of digital credentials , such as a driver's license, government-issued identification card, or other types of digital credential . Covers Digital Credentials (track). Use when a site requests or presents digital credentials in the browser. Triggers: Digital Credentials API, navigator.credentials, digital credential.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Digital Credentials API

This document specifies an API enabling user agents to mediate the presentation and issuance of digital credentials , such as a driver's license, government-issued identification card, or other types of digital credential . The API builds on Credential Management Level 1 and is designed to be agnostic to credential formats.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when a site requests or presents digital credentials in the browser.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Digital Credentials (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **5..** "A user agent MUST support all the presentation protocols listed in the table of supported presentation and issuance protocols ."
2. **7.7.** "To simplify the developer experience of get () calls involving a DigitalCredential , user agents MUST NOT throw an error if the mediation member is absent or has a value other than " required "."
3. **7.7.** "Similarly, in create () calls involving a DigitalCredential , user agents MUST NOT throw an error if the mediation member is absent or has a value other than " required "."
4. **7.7.3.** "User agents MUST NOT vary the response value based on any information about availability of hardware, presence or configuration of software, credential managers , or digital credentials, or user configuration or preferences."
5. **7.7.3.** "The response value SHOULD vary only by user agent major version and indicate whether the browser supports distributing requests with that protocol to underlying platform or provider."
6. **7.7.3.** "When this method is invoked, the user agent MUST return the result of user agent allows protocol given protocol ."
7. **8.2.** "[[Store]](credential, sameOriginWithAncestors) internal method When invoked, the [[Store]](credential, sameOriginWithAncestors) MUST call the default implementation of Credential 's [[Store]]( credential , sameOriginWithAncestors ) internal method with the same arguments."
8. **11.3.1.** "Presentation Protocol Considerations for User Privacy Issue 255 : Define concrete privacy and security requirements for the supported protocols privacy-tracker security-tracker registry privacy-considerations security-considerations There are two requirements for protocols that I think need further elaboration: MUST have undergone privacy review [...] And MUST have undergone security review [...]…"

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

- `webauthn`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill webauthn`
- `openid4vc`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill openid4vc`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Digital Credentials](https://www.w3.org/TR/digital-credentials/): Working Draft, digital-credentials WD-digital-credentials-20260904 (Working Draft, 2026-09-04), checked 2026-10-06.
