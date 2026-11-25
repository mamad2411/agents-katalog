---
name: visa-trusted-agent-protocol
description: >-
  Visa Trusted Agent Protocol: identify trusted AI agents to merchants with signed HTTP requests. Covers Trusted Agent Protocol. Use when identifying an agent to a merchant. Triggers: Trusted Agent Protocol.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Trusted Agent Protocol

Visa's Trusted Agent Protocol (TAP) lets an AI agent prove to a merchant that it is a trusted agent acting for a consumer, using an RFC 9421 HTTP message signature with an `agent-browser-auth` or `agent-payer-auth` tag, plus signed consumer recognition and payment container objects linked to it by the same nonce. This skill quotes the Merchant Specifications page on Visa Developer and the visa/trusted-agent-protocol repository README pinned at a commit.

**Scope.** The Merchant Specifications page is unversioned and says that accessing or using it means agreeing to the Visa Trusted Agent Protocol Product Terms; read those terms before relying on the page. Where the page labels content as the Visa implementation (Visa ID Token, the Visa-hosted key URL), the rules apply to Visa's deployment of the protocol. The repository's sample agent, proxy and registry code is out of scope.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Merchant, site protection provider (CDN or proxy) verifying agent traffic, or agent developer producing TAP signatures.
- Target version: Trusted Agent Protocol (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Agent Recognition Signature: Required Message Signature Fields (tag).** "Will contain the value of agent-browser-auth or agent-payer-auth based on the type of interaction"
2. **Agent Recognition Signature: Verification Steps.** "If the header does not contain a message signature with a Signature-Input field containing a tag of either agent-browser-auth or agent-payer-auth, the message has not been signed by a trusted agent."
3. **Agent Recognition Signature: Verification Steps (Minimum fields).** "If any of the fields listed in the table above are missing, the message should be blocked."
4. **Agent Recognition Signature: Verification Steps (Timestamps).** "The timestamps (created and expired) should fall within the current GMT time and should not be more than 8 minutes apart."
5. **Agent Recognition Signature: Verification Steps (Nonce).** "If maintaining a record of all nonces received in the last 8 minutes, if the nonce received matches a recorded nonce, the message should be blocked."
6. **Agent Recognition Signature: Verification Steps (Locate the public key).** "If the public key cannot be retrieved or the public key has expired, the message should be blocked."
7. **Agent Recognition Signature: Verification Steps (Validate the signature).** "If signature validation fails, the message should be blocked."
8. **Consumer Recognition.** "That is, the Agentic Consumer Recognition Object contains a signature signed with the same private key used to sign the message signature and one of the fields signed is the same nonce present in the message signature."
9. **Payment: Verification Steps (Nonce).** "If a message signature was present for this interaction and the nonce contained in the object does not match the nonce received in the message signature, the content of the object is inaccurate and should not be used for processing any payment."
10. **Payment: Verification Steps (Validate the signature).** "If signature validation fails, the content of the object is inaccurate and should not be used for processing any payment."
11. **Processing of Payment Data: Browsing IOU.** "Prior to granting access to the resource, the Merchant must verify that the data in the IOU matches the data returned in the 402 response and verify the signature."
12. **Public Keys Retrieval Service.** "Each key must be easily identifiable so it can be selected by the relying party based on the kid or keyid specified in the header of the JWS or Signature-Input respectively."

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
- [ ] Verification rejects a message whose `created` to expiry window exceeds 8 minutes, whose nonce was seen in the last 8 minutes, or whose `keyid` key cannot be retrieved.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `http-message-signatures`, `web-bot-auth`, `jwt`, `mastercard-agent-pay`, `agentic-commerce-protocol`, `ap2`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Trusted Agent Protocol: Merchant Specifications](https://developer.visa.com/capabilities/trusted-agent-protocol/trusted-agent-protocol-specifications): Visa Developer specification, Unversioned page, read 2026-10-06, checked 2026-10-06.
- [Trusted Agent Protocol README](https://raw.githubusercontent.com/visa/trusted-agent-protocol/16d59bdf3f8a542bc538d0962edbb80ea30a02af/README.md): Repository document, commit 16d59bd, 2025-10-28, checked 2026-10-06.
