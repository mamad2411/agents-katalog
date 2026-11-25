---
name: dbsc
description: >-
  Device Bound Session Credentials (DBSC): Device Bound Sessions Credentials (DBSC) aims to prevent hijacking via cookie theft by building a protocol and infrastructure that allows a user agent to assert possession of a securely-stored private key. Covers Device Bound Session Credentials Level 1 (track). Use when binding a session to a device key. Triggers: DBSC, Device Bound Session Credentials, Sec-Session-Id.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Device Bound Session Credentials (DBSC)

Device Bound Sessions Credentials (DBSC) aims to prevent hijacking via cookie theft by building a protocol and infrastructure that allows a user agent to assert possession of a securely-stored private key. DBSC is a Web API and a protocol between user agents and servers to achieve this binding.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when binding a session to a device key.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Device Bound Session Credentials Level 1 (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **3. Privacy Considerations.** "As such, we require that browsers MUST clear sessions and keys when clearing other site data (like cookies)."
2. **8.11. Create session key pair.** "User agents SHOULD place an upper limit on the number of registrable origin labels in "relying_origins" to prevent abuse."
3. **9.1. `Secure-Session-Registration` HTTP header field.** "Its ABNF is: SecureSessionRegistration = sf-list Each item in the list must be an inner list, and each item in the inner list MUST be an sf-token representing a supported algorithm (ES256, RS256)."
4. **9.2.1. `Secure-Session-Challenge` structured header serialization.** "Challenges MUST have an sf-parameter named "id" , whose value MUST be a string representing a session identifier ."
5. **9.2.1. `Secure-Session-Challenge` structured header serialization.** "Any other sf-parameter s SHOULD be ignored."
6. **9.3. `Secure-Session-Response` HTTP header field.** "Its ABNF is: SecureSessionResponse = sf-string This string MUST only contain the DBSC proof JWT."
7. **9.4. `Sec-Secure-Session-Id` HTTP header field.** "Its ABNF is: SecSecureSessionId = sf-string This string MUST only contain the session identifier."
8. **9.5. `Secure-Session-Skipped` HTTP header field.** "Its ABNF is: SecureSessionSkipped = sf-list Each item in the list MUST be an sf-token representing a coarse-grained reason for skipping cookie refresh."

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

- [Device Bound Session Credentials](https://www.w3.org/TR/dbsc-1/): First Public Working Draft, dbsc-1 WD-dbsc-1-20250821 (First Public Working Draft, 2025-08-21), checked 2026-10-06.
