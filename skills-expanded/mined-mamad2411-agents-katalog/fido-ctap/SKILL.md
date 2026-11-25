---
name: fido-ctap
description: >-
  FIDO CTAP: This specification describes an application layer protocol for communication between a roaming authenticator and another client/platform, as well as bindings of this application protocol to a variety of transport protocols using different physical media. Covers CTAP 2.3, CTAP 2.2 (supported), CTAP 2.1 (supported), CTAP 2.3.1 (track preview). Use when implementing a FIDO authenticator or client. Triggers: CTAP, CTAP2, authenticatorMakeCredential.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# FIDO CTAP

This specification describes an application layer protocol for communication between a roaming authenticator and another client/platform, as well as bindings of this application protocol to a variety of transport protocols using different physical media. The application layer protocol defines requirements for such transport protocols. Each transport binding defines the details of how such transport layer connections should be set up, in a manner that meets the requirements of the application layer protocol.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when implementing a FIDO authenticator or client.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: CTAP 2.3 (default); CTAP 2.2 (supported); CTAP 2.1 (supported); U2F 1.2 (legacy: read and upgrade, never author); CTAP 2.3.1 (preview, posture track: emit only when the user opts in and the posture is build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.1. Relationship to Other Specifications.** "Thus a superseded document or feature SHOULD NOT be used unless the replacement is not implemented by the counterparty."
2. **1.1. Relationship to Other Specifications.** "a CTAP 2.1 authenticator MUST still support authenticatorClientPIN ’s getPinToken subcommand if it supports clientPIN and CTAP 2.0.) The [U2FUsbHid] , [U2FNfc] , [U2FBle] , and [U2FRawMsgs] specifications, specifically, are superseded by this specification."
3. **1.1. Relationship to Other Specifications.** "CTAP2 authenticators SHOULD also implement CTAP1/U2F."
4. **2. Conformance.** "The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this specification are to be interpreted as described in [RFC2119] ."
5. **5. Terminology.** "Note: Authenticators with a method to collect a user gesture inside the authenticator boundary via other methods MUST not use this method."
6. **5. Terminology.** "not a command from the platform.) The duration of this timeout is chosen by the authenticator but MUST be at least 10 seconds."
7. **6. Authenticator API.** "In order to accommodate authenticators with limited capacity, the following accommodations are made: The state SHOULD NOT be maintained across power cycles."
8. **6. Authenticator API.** "An authenticator MUST discard the state for a stateful command command if the pinUvAuthToken that authenticated the state initializing command expires since the stateful commands do not themselves always verify a pinUvAuthToken ."

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

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [CTAP 2.3](https://fidoalliance.org/specs/fido-v2.3-ps-20260226/fido-client-to-authenticator-protocol-v2.3-ps-20260226.html): Proposed Standard, CTAP 2.3 Proposed Standard 2026-02-26 (Proposed Standard, 2026-02-26), checked 2026-10-06.
- [CTAP 2.2](https://fidoalliance.org/specs/fido-v2.2-ps-20250714/fido-client-to-authenticator-protocol-v2.2-ps-20250714.html): Proposed Standard, CTAP 2.2 Proposed Standard 2025-07-14 (Proposed Standard, 2025-07-14), checked 2026-10-06.
- [CTAP 2.1](https://fidoalliance.org/specs/fido-v2.1-ps-20210615/fido-client-to-authenticator-protocol-v2.1-ps-20210615.html): Proposed Standard, CTAP 2.1 Proposed Standard 2021-06-15 (Proposed Standard, 2021-06-15), checked 2026-10-06.
- [U2F 1.2](https://fidoalliance.org/specs/fido-u2f-v1.2-ps-20170411/fido-u2f-raw-message-formats-v1.2-ps-20170411.html): Proposed Standard, U2F 1.2 raw message formats (Proposed Standard, 2017-04-11), checked 2026-10-06.
- [CTAP 2.3.1](https://fidoalliance.org/specs/fido-v2.3.1-wd-20260529/fido-client-to-authenticator-protocol-v2.3.1-wd-20260529.html): Working Draft, CTAP 2.3.1 Working Draft 2026-05-29 (Working Draft, 2026-05-29), checked 2026-10-06.
