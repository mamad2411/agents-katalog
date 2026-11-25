---
name: web-cryptography
description: >-
  Web Cryptography API: This specification describes a JavaScript API for performing basic cryptographic operations in web applications, such as hashing, signature generation and verification, and encryption and decryption. Covers Web Cryptography API Level 1, Web Cryptography Level 2 (track preview). Use when using SubtleCrypto or CryptoKey in a browser. Triggers: WebCrypto, SubtleCrypto, CryptoKey.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Web Cryptography API

This specification describes a JavaScript API for performing basic cryptographic operations in web applications, such as hashing, signature generation and verification, and encryption and decryption. Additionally, it describes an API for applications to generate and/or manage the keying material necessary to perform these operations. Uses for this API range from user or service authentication, document or code signing, and the confidentiality and integrity of communications.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when using SubtleCrypto or CryptoKey in a browser.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Web Cryptography API Level 1 (default); Web Cryptography Level 2 (preview, posture track: emit only when the user opts in and the posture is build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **3. Conformance.** "The key words MUST , REQUIRED , and SHALL in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
2. **3. Conformance.** "The following conformance classes are defined by this specification: conforming user agent A user agent is considered to be a conforming user agent if it satisfies all of the MUST -, REQUIRED - and SHALL -level criteria in this specification that apply to implementations."
3. **3. Conformance.** "(In particular, the algorithms defined in this specification are intended to be easy to follow, and not intended to be performant.) User agents that use ECMAScript to implement the APIs defined in this specification MUST implement them in a manner consistent with the ECMAScript Bindings defined in the Web IDL specification [ WebIDL ] as this specification uses that specification and terminology."
4. **4.2 Cryptographic algorithms.** "Because the underlying cryptographic implementations will vary between conforming user agents, and may be subject to local policy, including but not limited to concerns such as government or industry regulation, security best practices, intellectual property concerns, and constrained operational environments, this specification does not dictate a mandatory set of algorithms that MUST be implemented."
5. **8. Dependencies.** "DOM A conforming user agent MUST support at least the subset of the functionality defined in DOM that this specification relies upon; in particular, it MUST support Promise s and DOMException ."
6. **8. Dependencies.** "[ DOM ] HTML A conforming user agent MUST support at least the subset of the functionality defined in HTML that this specification relies upon; in particular, it MUST support the ArrayBufferView typedef and serializable objects ."
7. **8. Dependencies.** "[ HTML ] Web IDL A conforming user agent MUST be a conforming implementation of the IDL fragments in this specification, as described in the Web IDL specification."
8. **14.3.6 The generateKey method.** "When invoked, generateKey MUST perform the following steps: Let algorithm , extractable and usages be the algorithm , extractable and keyUsages parameters passed to the generateKey () method, respectively."

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

- `jwt`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill jwt`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Web Cryptography API](https://www.w3.org/TR/WebCryptoAPI/): Recommendation, webcrypto-1 WD-webcrypto-2-20250422 (Recommendation, 2017-01-26), checked 2026-10-06.
- [Web Cryptography Level 2](https://www.w3.org/TR/webcrypto-2/): First Public Working Draft, webcrypto-2 WD-webcrypto-2-20250422 (First Public Working Draft, 2025-04-22), checked 2026-10-06.
