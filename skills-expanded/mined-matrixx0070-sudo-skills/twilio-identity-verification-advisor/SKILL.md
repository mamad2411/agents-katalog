---
name: twilio-identity-verification-advisor
version: 1.0.0
description: Advisory skill that picks the right Twilio identity signal — Verify OTP, Lookup, or Silent Network Auth — for a given risk, friction, and KYC context.
author: matrixx0070
tags: [twilio, identity, verification, kyc, fraud, advisory]
capabilities: []
---

## When to use

Use this when you have not yet decided *how* to verify a user and need to choose the right tool and factor for the risk. Good triggers: designing a signup or login flow, adding step-up auth for a high-value action, cutting SMS fraud costs, or meeting a KYC/AML obligation. This skill reasons about trade-offs — friction, cost, assurance level, coverage — and hands you a concrete plan, not an implementation.

**Not for:** actually sending or checking a code — once you've decided on OTP, use twilio-verify-send-otp. Not for pulling raw number intelligence — use twilio-lookup-phone-intelligence. Not for building the interaction surface — use twilio-studio-flows.

## Method

1. **State the assurance need.** What are you protecting and what's the loss if an attacker gets through? Decision point: low-value (newsletter) → possession-lite is fine; high-value (money movement, PII change) → require step-up and consider a possession + inherence combination.
2. **Map the friction budget.** How much can you make the user do? Silent Network Auth (SNA) verifies the SIM against the carrier with zero user input; OTP costs the user a code entry and a delivery round-trip.
3. **Check coverage.** SNA works only where the carrier and network path support it (mobile data, supported operators). Decision point: if the user is on Wi-Fi only or an unsupported carrier, SNA silently can't run — you must fall back to OTP.
4. **Pre-screen the number with Lookup.** Before spending on delivery, run Lookup line-type and (for risk) sim_swap / reassigned_number to reject VoIP, landlines, or recently-swapped SIMs. Decision point: high sim_swap risk → block or force a stronger factor, don't send OTP to a hijacked line.
5. **Choose the primary factor.** SNA (frictionless, phone-possession), Verify OTP (universal fallback), TOTP/Push (app-based, no telecom cost), or an identity KYC match. Combine when assurance demands it.
6. **Design the step-up.** Reserve heavier verification for risky moments (new device, high amount, changed email) rather than every login, to protect conversion.
7. **Plan the fallback chain** explicitly: e.g. SNA → OTP SMS → OTP call. Every silent method needs a visible fallback.
8. **Note compliance obligations.** If this is KYC/AML, telecom possession alone is not identity proof — flag that a document/identity-match step is required.

## Example

```
Scenario: fintech login + $-transfer step-up, global users.

Decision:
  Login          -> SNA (frictionless) with OTP SMS fallback on unsupported networks
  New device     -> Verify OTP (possession re-check)
  $ transfer     -> step-up: Verify OTP + Lookup sim_swap check (block if swap < 72h)
  Onboarding KYC -> Lookup identity_match + separate document/identity provider
                    (telecom possession != identity)

Rationale: keep 95% of logins zero-friction via SNA; spend OTP + risk
signals only on the money-moving path; never treat SIM possession as KYC.
```

## Pitfalls

- **Treating phone possession as identity.** Verify/SNA prove the user controls a number, not who they are. KYC/AML needs a real identity-match or document step — flag this explicitly.
- **Assuming SNA always works.** SNA needs mobile-data connectivity and a supported carrier; on Wi-Fi or unsupported operators it can't complete. Always pair it with an OTP fallback.
- **Skipping the pre-send Lookup.** Sending OTP blind wastes money on VoIP/landlines and exposes you to SMS-pumping fraud and SIM-swap account takeover. Screen first.
- **Verifying everything, every time.** Uniform high friction kills conversion. Use risk-based step-up so heavy checks fire only on risky events.
- **Ignoring reassigned numbers.** A number recycled to a new owner passes OTP but reaches the wrong person; use the reassigned_number signal for account-recovery flows.
- **One factor, no fallback.** Any single channel has a dead zone (landline, roaming, blocked SMS). Design an explicit fallback chain.

## Output format

```
IDENTITY PLAN
  protects: <asset / action>
  assurance_target: <low | medium | high>
  primary_factor: <SNA | Verify OTP | TOTP/Push | identity-match>
  fallback_chain: <ordered list>
  pre_send_signals: <lookup packages to run>
  step_up_triggers: <events that escalate>
  kyc_required: <yes/no — extra identity step if yes>
  implement_with: <twilio-verify-send-otp | twilio-lookup-phone-intelligence>
```

## Reference

- **Twilio identity products:** Verify (OTP over SMS/call/email/WhatsApp, plus Push and TOTP), Verify Silent Network Auth (SNA — verifies phone possession by matching the SIM against the mobile carrier over the data connection, no user input), Lookup v2 (number intelligence).
- **Assurance ladder:** knowledge (password) < possession-lite (OTP SMS) < possession-strong (SNA / TOTP / Push) < identity (KYC document + identity_match). Combine possession + inherence for high-value actions.
- **SNA coverage caveat:** requires cellular data and a supported carrier/region; not available on Wi-Fi-only sessions — treat OTP as the mandatory fallback.
- **Fraud economics:** OTP SMS is a target for SMS Pumping (artificial traffic inflation); Fraud Guard and pre-send Lookup line-type filtering cut this. SIM-swap and reassigned-number signals defend account takeover and misdelivery.
- **Compliance:** KYC/AML (e.g. US CIP under the Bank Secrecy Act, EU AMLD) requires identity proofing beyond telecom possession. TCPA governs the OTP delivery message (transactional when user-provided for auth). SNA and Lookup consumer-data use may carry regional consent/privacy obligations (GDPR).
- **Auth for any implementation:** Account SID + Auth Token or API Key SID/Secret, server-side only.
