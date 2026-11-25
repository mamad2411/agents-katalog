---
name: mastercard-agent-pay
description: >-
  Mastercard Agent Pay: verify and accept purchases from certified AI agents as a merchant, using Web Bot Auth signatures with the Agent-pay-auth tag, agentic tokens and the Agent Pay payment object. Covers the Mastercard Developers agentic commerce playbook (Levels 1 to 3) as published in 2026; the Agent Pay Acceptance Framework itself is not public and is not pinned. Use when a merchant site, CDN rule or checkout API must recognise Mastercard Agent Pay traffic, check Signature-Input and Signature headers against the Mastercard key directory, block replays, or validate an agentic payment token and intent. Triggers: Mastercard Agent Pay, Agent-pay-auth, agentic token, agentic commerce Mastercard, Signature-Agent, agentpay-key-directory, Verifiable Intent.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Mastercard Agent Pay (merchant acceptance)

Mastercard Agent Pay is Mastercard's framework for certified AI agents that buy on behalf of consumers. Mastercard Developers publishes a merchant playbook, "Developer Playbook on Preparing for Agentic Commerce", in Markdown; this skill quotes its Agent Pay guidance on agent identification, replay protection, agentic tokens and the Level 3 payment object.

**Scope.** The pinned texts are Mastercard's developer guides, not a specification. They point to the Mastercard Agent Pay Acceptance Framework "for the complete Intent API specification and implementation details"; that framework is not publicly downloadable and is out of scope. The guides describe the playbook as reflecting "currently available public information" that "may evolve", so re-read them before relying on a rule.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Merchant, merchant platform or payment service provider receiving agent traffic; CDN or edge rule author.
- Target version: Mastercard Agent Pay (2026 playbook) (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Example request.** "Signature-Agent: "https://agentpay-key-directory.mastercard.com/""
2. **Understanding the Signature Headers.** "Identifies the interaction type: `Agent-pay-auth`, `agent-browser-auth` or `agent-payer-auth`"
3. **Verification Steps Reference.** "Verify all required fields are present (`@authority`, `@path`, `created`, `keyid`, `expires`, `tag`, `alg`, `nonce`) | Block request"
4. **Verification Steps Reference.** "Confirm `expires - created` ≤ 8 minutes"
5. **Replay Attack Protection.** "Maintain a cache of seen nonces for the past 8 minutes. Reject any request with a previously seen nonce."
6. **Step 2: Validate the intent.** "Reject the checkout if intent validation fails. Do not process payments against invalid, expired, or missing intents."
7. **Step 3: Validate the payment token.** "If a message signature was present, confirm the nonce in the payment object matches the nonce from the message signature headers"
8. **Step 3: Validate the payment token.** "If signature validation fails, the payment object may have been tampered with. Do not process the payment."
9. **Cards on File and Agentic Tokens.** "AI Agents cannot use consumers' existing cards on file with merchants, even when logging a consumer into their merchant account."

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
- [ ] The tag comparison accepts the Mastercard tag as both pages spell it (`Agent-pay-auth` on the Level 1 page, `agent-pay-auth` in the glossary) until Mastercard settles the case.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `web-bot-auth`, `http-message-signatures`, `sd-jwt`, `visa-trusted-agent-protocol`, `agentic-commerce-protocol`, `ucp`, `ap2`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Developer Playbook on Preparing for Agentic Commerce](https://developer.mastercard.com/merchant-cloud/documentation/tutorials-and-guides/agentic-commerce-guide/index.md): Mastercard Developers guide, Overview page, read 2026-10-06, checked 2026-10-06.
- [Level 1 Agentic Commerce - Enable Agent Support with Minimal Changes](https://developer.mastercard.com/merchant-cloud/documentation/tutorials-and-guides/agentic-commerce-guide/21/index.md): Mastercard Developers guide, Level 1 page, read 2026-10-06, checked 2026-10-06.
- [Level 3 Agentic Commerce - Advanced Programmatic Checkout](https://developer.mastercard.com/merchant-cloud/documentation/tutorials-and-guides/agentic-commerce-guide/23/index.md): Mastercard Developers guide, Level 3 page, read 2026-10-06, checked 2026-10-06.
- [Preparing for Agentic Commerce: Testing, Validation, and Reference Guide](https://developer.mastercard.com/merchant-cloud/documentation/tutorials-and-guides/agentic-commerce-guide/24/index.md): Mastercard Developers guide, Reference page, read 2026-10-06, checked 2026-10-06.
