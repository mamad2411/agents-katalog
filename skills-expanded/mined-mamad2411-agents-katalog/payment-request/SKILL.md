---
name: payment-request
description: >-
  Payment Request API: build browser checkouts with PaymentRequest, payment method identifiers and web-based payment handlers. Covers Payment Request API (build), Payment Method Identifiers, Web-based Payment Handler API (track). Use when building a checkout that uses Payment Request, a payment method identifier, or a web-based payment handler. Triggers: Payment Request, PaymentRequest, payment method identifier.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Payment Request API

This specification standardizes an API to allow merchants (i.e. web sites selling physical or digital goods) to utilize one or more payment methods with minimal integration. User agents (e.g., browsers) facilitate the payment flow between merchant and user.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when building a checkout that uses Payment Request, a payment method identifier, or a web-based payment handler.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Payment Request API (default, posture build); Payment Method Identifiers (default); Web-based Payment Handler API (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **3.1.** "The PaymentRequest( methodData , details , options ) constructor MUST act as follows: If this 's relevant global object 's associated Document is not allowed to use the "payment" permission, then throw a " SecurityError " DOMException ."
2. **3.3.** "The show(optional detailsPromise ) method MUST act as follows: Let request be this ."
3. **3.3.** "The user agent SHOULD prioritize the user's preference when presenting payment methods."
4. **3.3.** "The user interface SHOULD be presented using the language and locale-based formatting that matches the document 's document element's language , if any, or an appropriate fallback if that is not available."
5. **3.3.** "Optionally, the user agent SHOULD send the appropriate data from request to the"
6. **3.4.** "The abort () method MUST act as follows: Let request be this ."
7. **3.5.** "The canMakePayment () method MUST run the can make payment algorithm ."
8. **9..** "requestBillingAddress member A boolean that indicates whether the user agent SHOULD collect and return the billing address associated with a payment method (e.g., the billing address associated with a credit card)."

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

- [Payment Request API](https://www.w3.org/TR/payment-request/): Candidate Recommendation Draft, payment-request CRD-payment-request-20260622 (Candidate Recommendation Draft, 2026-06-22), checked 2026-10-06.
- [Payment Method Identifiers](https://www.w3.org/TR/payment-method-id/): Recommendation, payment-method-id REC-payment-method-id-20220908 (Recommendation, 2022-09-08), checked 2026-10-06.
- [Web-based Payment Handler API](https://www.w3.org/TR/web-based-payment-handler/): Working Draft, web-based-payment-handler WD-web-based-payment-handler-20260930 (Working Draft, 2026-09-30), checked 2026-10-06.
