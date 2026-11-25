---
name: privacy-pass
description: >-
  The Privacy Pass Architecture: This document specifies the Privacy Pass architecture and requirements for its constituent protocols used for authorization based on privacy-preserving authentication mechanisms. Covers RFC 9576 The Privacy Pass Architecture, RFC 9577 The Privacy Pass HTTP Authentication Scheme, RFC 9578 Privacy Pass Issuance Protocols. Use when issuing or redeeming a Privacy Pass token. Triggers: Privacy Pass, RFC 9576.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# The Privacy Pass Architecture

This document specifies the Privacy Pass architecture and requirements for its constituent protocols used for authorization based on privacy-preserving authentication mechanisms. It describes the conceptual model of Privacy Pass and its protocols, its security and privacy goals, practical deployment models, and recommendations for each deployment model, to help ensure that the desired security and privacy goals are fulfilled. ¶

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when issuing or redeeming a Privacy Pass token.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 9576 The Privacy Pass Architecture (default); RFC 9577 The Privacy Pass HTTP Authentication Scheme (default); RFC 9578 Privacy Pass Issuance Protocols (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 9576 § 3.5.** "The issuance protocol MUST NOT reveal anything about the Client's private input, including the challenge and nonce, to the Attester or Issuer, regardless of the hardness assumptions of the underlying cryptographic protocol(s)."
2. **RFC 9576 § 3.5.** "The issuance protocol MUST NOT allow malicious Clients or Attesters (acting as Clients) to forge tokens offline or otherwise without interacting with the Issuer directly."
3. **RFC 9577 § 2.1.1.** "All token challenges MUST begin with a 2-octet integer that defines the token type, in network byte order."
4. **RFC 9577 § 2.1.1.** "Clients MUST ignore challenges with token types they do not support."
5. **RFC 9577 § 2.1.3.** "If validation fails, the Client MUST NOT fetch or redeem a token based on the challenge."
6. **RFC 9577 § 2.2.1.** "A token is a structure that begins with a 2-octet field that indicates a token type, which MUST match the token_type in the TokenChallenge structure."
7. **RFC 9577 § 2.2.2.** "Origins SHOULD implement some form of double-spend prevention that prevents a token with the same nonce from being redeemed twice."
8. **RFC 9577 § 5.1.** "All random values in the challenge and token MUST be generated using a cryptographically secure source of randomness [RFC4086]."
9. **RFC 9578 § 4.** "If an Issuer wants to service multiple different Issuer directories, they MUST create unique subdomains for each directory so the TokenChallenge defined in Section 2.1 of [AUTHSCHEME] can be differentiated correctly."
10. **RFC 9578 § 5.5.** "These keys MUST NOT be reused in other protocols."

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

- `web-bot-auth`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill web-bot-auth`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 9576 The Privacy Pass Architecture](https://www.rfc-editor.org/rfc/rfc9576.html): INFORMATIONAL, RFC 9576 (INFORMATIONAL, June 2024), checked 2026-10-06.
- [RFC 9577 The Privacy Pass HTTP Authentication Scheme](https://www.rfc-editor.org/rfc/rfc9577.html): PROPOSED STANDARD, RFC 9577 (PROPOSED STANDARD, June 2024), checked 2026-10-06.
- [RFC 9578 Privacy Pass Issuance Protocols](https://www.rfc-editor.org/rfc/rfc9578.html): PROPOSED STANDARD, RFC 9578 (PROPOSED STANDARD, June 2024), checked 2026-10-06.
