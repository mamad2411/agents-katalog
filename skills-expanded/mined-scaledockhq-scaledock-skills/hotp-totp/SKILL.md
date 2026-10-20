---
name: hotp-totp
description: >-
  HOTP and TOTP (RFC 4226, RFC 6238): generate and verify HMAC-based and time-based one-time passwords. Covers RFC 4226 HOTP: An HMAC-Based One-Time Password Algorithm, RFC 6238 TOTP: Time-Based One-Time Password Algorithm. Use when verifying a one-time password. Triggers: HOTP, TOTP, RFC 4226, RFC 6238.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# HOTP: An HMAC-Based One-Time Password Algorithm

HOTP: An HMAC-Based One-Time Password Algorithm

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when verifying a one-time password.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 4226 HOTP: An HMAC-Based One-Time Password Algorithm (default); RFC 6238 TOTP: Time-Based One-Time Password Algorithm (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 4226 § 4.** "R6 - The algorithm MUST use a strong shared secret. The length of the shared secret MUST be at least 128 bits. This document RECOMMENDs a shared secret length of 160 bits."
2. **RFC 4226 § 5.3.** "Implementations MUST extract a 6-digit code at a minimum and possibly 7 and 8-digit code."
3. **RFC 4226 § 7.1.** "This implies that a throttling/lockout scheme is RECOMMENDED on the validation server side."
4. **RFC 4226 § 7.3.** "The delay or lockout schemes MUST be across login sessions to prevent attacks based on multiple parallel guessing techniques."
5. **RFC 4226 § 7.5.** "The data store holding the shared secrets MUST be in a secure area, to avoid as much as possible direct attack on the validation system and secrets database."
6. **RFC 6238 § 3.** "The algorithm MUST use HOTP [RFC4226] as a key building block."
7. **RFC 6238 § 3.** "The prover and verifier MUST use the same time-step value X."
8. **RFC 6238 § 4.2.** "The implementation of this algorithm MUST support a time value T larger than a 32-bit integer when it is beyond the year 2038."
9. **RFC 6238 § 5.2.** "We RECOMMEND that at most one time step is allowed as the network delay."
10. **RFC 6238 § 5.2.** "We RECOMMEND a default time-step size of 30 seconds."
11. **RFC 6238 § 5.2.** "The verifier MUST NOT accept the second attempt of the OTP after the successful validation has been issued for the first OTP, which ensures one-time only use of an OTP."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
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

- [RFC 4226 HOTP: An HMAC-Based One-Time Password Algorithm](https://www.rfc-editor.org/rfc/rfc4226.html): INFORMATIONAL, RFC 4226 (INFORMATIONAL, December 2), checked 2026-10-06.
- [RFC 6238 TOTP: Time-Based One-Time Password Algorithm](https://www.rfc-editor.org/rfc/rfc6238.html): INFORMATIONAL, RFC 6238 (INFORMATIONAL, May 2011), checked 2026-10-06.
