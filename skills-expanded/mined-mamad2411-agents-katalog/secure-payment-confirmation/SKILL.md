---
name: secure-payment-confirmation
description: >-
  Secure Payment Confirmation (SPC): Secure Payment Confirmation (SPC) is a Web API to support streamlined authentication during a payment transaction. Covers Secure Payment Confirmation (build). Use when confirming a payment with a passkey in the browser. Triggers: SPC, Secure Payment Confirmation, secure-payment-confirmation.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Secure Payment Confirmation (SPC)

Secure Payment Confirmation (SPC) is a Web API to support streamlined authentication during a payment transaction. It is designed to scale authentication across merchants, to be used within a wide range of authentication protocols, and to produce cryptographic evidence that the user has confirmed transaction details.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when confirming a payment with a passkey in the browser.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Secure Payment Confirmation (default, posture build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **4.7. Availability of Secure Payment Confirmation capabilities.** "partial interface PaymentRequest { static Promise < SecurePaymentConfirmationCapabilities > getSecurePaymentConfirmationCapabilities (); }; typedef record < DOMString , boolean > SecurePaymentConfirmationCapabilities ; Keys in SecurePaymentConfirmationCapabilities MUST be sorted in ascending lexicographical order."
2. **4.7. Availability of Secure Payment Confirmation capabilities.** "The set of keys SHOULD contain the set of enumeration values of SecurePaymentConfirmationCapability , but the user agent MAY omit keys as it deems necessary; see § 12.6 Fingerprinting via getSecurePaymentConfirmationCapabilities ."
3. **4.10. Displaying a transaction confirmation UX.** "When PaymentRequest.show() is called and the Secure Payment Confirmation payment handler is selected (steps 19-24 of that algorithm), the User Agent MUST present the user with a user interface that allows them to select if and how they wish to proceed."
4. **4.10.1. Information presented to the user.** "However, so that a Relying Party can trust the information included in CollectedClientPaymentData , the User Agent MUST ensure that the following is communicated to the user and that the user’s consent is collected for the authentication: The payeeName if it is present."
5. **4.10.1. Information presented to the user.** "The user agent is not required to display the label for each PaymentEntityLogo , but SHOULD use them for accessibility purposes."
6. **4.10.1. Information presented to the user.** "If showOptOut is true , the user agent MUST give the user the opportunity to indicate that they want to opt out of the process for the given relying party ."
7. **4.10.2. Outcome of the transaction confirmation UX.** "A User Agent MUST allow the user to indicate one of the following options as to if and how to proceed: The user wishes to proceed with the payment, using an SPC Credential to authenticate, Run the user accepts the payment request algorithm on the PaymentRequest the user is interacting with."
8. **9.1. Verifying an Authentication Assertion.** "In order to perform an authentication ceremony for Secure Payment Confirmation, the Relying Party MUST proceed as follows: Let credential be a PublicKeyCredential returned from a successful invocation of the Secure Payment Confirmation payment handler by the SPC caller ."

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

- [Secure Payment Confirmation](https://www.w3.org/TR/secure-payment-confirmation/): Candidate Recommendation Draft, secure-payment-confirmation CRD-secure-payment-confirmation-20260702 (Candidate Recommendation Draft, 2026-07-02), checked 2026-10-06.
