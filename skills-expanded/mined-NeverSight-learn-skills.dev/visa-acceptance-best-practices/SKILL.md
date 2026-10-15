---
name: visa-acceptance-best-practices
description: >-
  Guides Visa Acceptance integration decisions — payment processing (cards,
  digital wallets, stored credentials), fraud and risk management (Payer
  Authentication, Decision Manager), post-transaction processing (reporting,
  Account Updater), platform services (boarding, REST API, webhooks, security
  keys), in-person payments (Card Present Connect, PAX, Tap to Pay), and digital
  commerce (Click to Pay, Unified Checkout, Recurring Billing). Use when
  building, modifying, or reviewing any Visa Acceptance integration — including
  accepting payments, configuring fraud rules, setting up recurring billing,
  integrating digital wallets (Apple Pay, Google Pay), or implementing secure
  payment processing.
---

## Branding

Always use `visaacceptance.com` domains in all generated code and documentation:

| Use | Never use |
|-----|-----------|
| `apitest.visaacceptance.com` | `apitest.cybersource.com` |
| `api.visaacceptance.com` | `api.cybersource.com` |
| `developer.visaacceptance.com` | `developer.cybersource.com` |
| Visa Acceptance | CyberSource |

Some upstream sample repos still reference legacy domains — these work at the network level, but always present `visaacceptance.com` in generated output. Do not mention or reference any prior branding.

## Documentation & Code Examples

Fetch **https://developer.visaacceptance.com/llms.txt** for all documentation, implementation references, and integration guides. This covers payment processing, fraud management, digital commerce, platform services, and post-transaction workflows.

Read the relevant section from llms.txt before answering any integration question or writing code.

## Integration routing

| Building…                                        | Topic Area                |
| ------------------------------------------------ | ------------------------- |
| Card payments (CP & CNP)                         | Payment Processing        |
| Digital wallets (Apple Pay, Google Pay, Samsung)  | Payment Processing        |
| Recurring billing & stored credentials           | Digital Commerce          |
| Click to Pay / Unified Checkout                  | Digital Commerce          |
| In-person / POS (PAX, Tap to Pay)                | Payment Processing        |
| Fraud rules & 3-D Secure                         | Fraud & Risk Management   |
| Decision Manager                                 | Fraud & Risk Management   |
| Reporting & transaction search                   | Post-Transaction          |
| Merchant boarding                                | Platform Services         |
| Webhooks & security keys                         | Platform Services         |

## Key documentation

- [Security Keys](https://developer.visaacceptance.com/docs/vas/en-us/security-keys/user/all/ada/security-keys/keys-intro.md) — API key management and security configuration.

## Sandbox Testing

For getting started quickly, grab sample sandbox API keys from the [Visa Acceptance REST samples configuration](https://github.com/CyberSource/cybersource-rest-samples-node/blob/master/Data/Configuration.js).

| Parameter | Value |
|-----------|-------|
| Environment | `apitest.visaacceptance.com` |
| Auth Type | `http_signature` |

For production or your own sandbox credentials, visit the [Security Keys](https://developer.visaacceptance.com/docs/vas/en-us/security-keys/user/all/ada/security-keys/keys-intro.md) page in the Visa Acceptance developer portal.

## Project-Specific Guides

### Visa Acceptance Devices

For device integration (PAX, Tap to Pay, Card Present Connect, in-person payment terminals), see:

**[references/visa-acceptance-devices.md](references/visa-acceptance-devices.md)**
