---
name: mls
description: >-
  The Messaging Layer Security (MLS) Protocol: Messaging applications are increasingly making use of end-to-end security mechanisms to ensure that messages are only accessible to the communicating endpoints, and not to any servers involved in delivering messages. Covers RFC 9420 The Messaging Layer Security (MLS) Protocol. Use when implementing Messaging Layer Security. Triggers: MLS, RFC 9420.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# The Messaging Layer Security (MLS) Protocol

Messaging applications are increasingly making use of end-to-end security mechanisms to ensure that messages are only accessible to the communicating endpoints, and not to any servers involved in delivering messages. Establishing keys to provide such protections is challenging for group chat settings, in which more than two clients need to agree on a key but may not be online at the same time. In this document, we specify a key establishment protocol that provides efficient asynchronous group key establishment with forward secrecy (FS) and post-compromise security (PCS) for groups in size ranging from two to thousands. ¶

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when implementing Messaging Layer Security.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 9420 The Messaging Layer Security (MLS) Protocol (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 9420 § 6.** "Applications MUST use PrivateMessage to encrypt application messages and SHOULD use PrivateMessage to encode handshake messages, but they MAY transmit handshake messages encoded as PublicMessage objects in cases where it is necessary for the Delivery Service to examine such messages."
2. **RFC 9420 § 6.2.** "When decoding a PublicMessage into an AuthenticatedContent, the application MUST check membership_tag and MUST check that the FramedContentAuthData is valid."
3. **RFC 9420 § 6.3.1.** "To avoid this situation, the sender of a message MUST generate a fresh random four-byte "reuse guard" value and XOR it with the first four bytes of the nonce from the key schedule before using the nonce for encryption."
4. **RFC 9420 § 9.1.** "Each key/nonce pair MUST NOT be used to encrypt more than one message."
5. **RFC 9420 § 9.2.** "As soon as a group member consumes a value, they MUST immediately delete (all representations of) that value."
6. **RFC 9420 § 11.** "To protect against downgrade attacks, the creator MUST use the capabilities information in these KeyPackages to verify that the chosen version and cipher suite is the best option supported by all members."
7. **RFC 9420 § 12.1.** "On receiving a FramedContent containing a Proposal, a client MUST verify the signature inside FramedContentAuthData and that the epoch field of the enclosing FramedContent is equal to the epoch field of the current GroupContext object."
8. **RFC 9420 § 12.4.3.3.** "Regardless of how the client obtains the tree, the client MUST verify that the root hash of the ratchet tree matches the tree_hash of the GroupContext before using the tree for MLS operations."
9. **RFC 9420 § 14.** "The generation of Commit messages MUST NOT modify a client's state, since the client doesn't know at that time whether the changes implied by the Commit message will conflict with another Commit or not."
10. **RFC 9420 § 15.2.** "During each epoch, senders MUST NOT encrypt more data than permitted by the security bounds of the AEAD scheme used [CFRG-AEAD-LIMITS]."
11. **RFC 9420 § 17.1.** "The mandatory-to-implement cipher suite for MLS 1.0 is MLS_128_DHKEMX25519_AES128GCM_SHA256_Ed25519, which uses Curve25519 for key exchange, AES-128-GCM for HPKE, HKDF over SHA2-256, and Ed25519 for signatures. MLS clients MUST implement this cipher suite."

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

- [RFC 9420 The Messaging Layer Security (MLS) Protocol](https://www.rfc-editor.org/rfc/rfc9420.html): PROPOSED STANDARD, RFC 9420 (PROPOSED STANDARD, July 2023), checked 2026-10-06.
