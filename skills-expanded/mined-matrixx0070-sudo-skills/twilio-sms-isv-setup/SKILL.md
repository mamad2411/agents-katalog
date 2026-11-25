---
name: twilio-sms-isv-setup
version: 1.0.0
description: Onboard as a Twilio ISV — register brands and A2P 10DLC campaigns on behalf of client businesses using Trust Hub Secondary Customer Profiles.
author: matrixx0070
tags: [twilio, isv, trust-hub, a2p-10dlc, tcr, brand-registration]
capabilities: []
---

## When to use

Use this when your platform sends SMS *on behalf of many client businesses* (a SaaS, agency, or CPaaS reseller) and each client needs its own carrier-registered identity. Reach for it when you must register a brand and A2P 10DLC campaign per customer rather than one for yourself, when you're managing dozens or hundreds of client profiles, and when you want higher, per-brand throughput tiers. Use it whenever the answer to "whose business is this traffic for" is "my customer, not me."

**Not for:** a single business registering its own one brand and campaign — that direct path lives in `twilio-compliance-traffic` / `twilio-compliance-onboarding`. Not for picking sender types or pooling numbers — that is `twilio-numbers-senders`. This skill is specifically the *vendor / multi-tenant* registration model.

## Method

1. Complete your own **Primary Customer Profile** in Trust Hub first — the ISV's own business identity is the umbrella under which client profiles are registered. Decision point: without an approved Primary Profile you cannot create Secondary Profiles.
2. For each client, create a **Secondary Customer Profile** capturing their legal business name, **EIN/business registration number**, address, and an authorized representative. This is the client's identity, distinct from yours.
3. Register the client's **Brand** with **The Campaign Registry (TCR)** through Trust Hub. Decision point: choose **Standard** brand vetting for scale/throughput, or accept low-volume/sole-proprietor limits — vetting score drives throughput tier.
4. Create an **A2P 10DLC Campaign** per client use case (marketing, 2FA, notifications, mixed) referencing the client's brand. Provide sample messages, opt-in flow evidence, and message frequency.
5. Isolate each client's traffic: typically a **subaccount** or at least a dedicated **Messaging Service** per client, with their numbers in its sender pool.
6. Associate the registered campaign with the client's Messaging Service so their numbers inherit the approved use case and throughput.
7. Automate the pipeline via the **Trust Hub** and **Messaging Compliance** APIs (CustomerProfiles, TrustProducts, A2P BrandRegistrations, A2P Campaigns) — clicking per client doesn't scale.
8. Track each client's status through the states (draft → pending → in-review → approved/rejected) and build a remediation loop for rejections. Decision point: a rejected brand blocks all its campaigns — fix the brand before resubmitting campaigns.

## Example

```javascript
const client = require('twilio')(process.env.TWILIO_API_KEY_SID, process.env.TWILIO_API_KEY_SECRET, {
  accountSid: process.env.TWILIO_ACCOUNT_SID,
});

// 1) Create a Secondary Customer Profile for a client business (bundle under your Primary).
const profile = await client.trusthub.v1.customerProfiles.create({
  friendlyName: 'AcmeCorp client profile',
  email: 'compliance@acme.example',
  policySid: 'RN...',              // secondary-profile policy SID
});

// 2) Register the client's brand with TCR (references the customer profile bundle).
const brand = await client.messaging.v1.brandRegistrations.create({
  customerProfileBundleSid: profile.sid, // BU...
  a2PProfileBundleSid: 'BU...',
});

// 3) Create an A2P 10DLC campaign (usAppToPerson) under the client's Messaging Service.
const campaign = await client.messaging.v1
  .services('MG...')                       // client's Messaging Service
  .usAppToPerson.create({
    brandRegistrationSid: brand.sid,       // BN...
    description: 'Appointment reminders and 2FA for Acme customers',
    messageSamples: ['Your Acme code is 123456', 'Reminder: appt tomorrow 3pm. Reply STOP to opt out.'],
    usAppToPersonUsecase: 'MIXED',
    hasEmbeddedLinks: false,
    hasEmbeddedPhone: false,
  });
```

## Pitfalls

- **Skipping the Primary Profile.** Secondary Customer Profiles can only exist under an approved ISV Primary Profile. Get yours approved before onboarding any client.
- **Wrong EIN / legal name.** TCR verifies the client's EIN against official records; a typo or DBA-instead-of-legal-name causes brand rejection and delays every downstream campaign.
- **One shared campaign for all clients.** Bundling many businesses under one campaign violates the ISV model and gets traffic filtered. Register per-client brand + campaign.
- **Under-vetting for the throughput you need.** Throughput tier is tied to the brand vetting score; if you skip Standard vetting, per-day/TPS caps may throttle your clients.
- **Campaign approved but not linked.** A registered campaign does nothing until associated with the client's Messaging Service and numbers.
- **No remediation loop.** Rejections are common; without tracking state per client you lose visibility and clients silently can't send.

## Output format

```
# Twilio ISV Onboarding — <client>
ISV PRIMARY PROFILE: BU******************************** (approved)
SECONDARY PROFILE: BU******************************** | legalName=<> EIN=<>
BRAND: BN******************************** | vetting=<Standard|low-volume> | status=<>
CAMPAIGN: <usecase> | status=<draft|pending|in-review|approved|rejected> | throughput_tier=<>
ISOLATION: subaccount=<AC...|none> messagingService=MG********************************
NUMBERS: <count> in sender pool
REJECTION NOTES: <reason + remediation, if any>
```

## Reference

- **Trust Hub** holds **Primary** (your ISV identity) and **Secondary Customer Profiles** (each client's identity). SIDs: bundles `BU...`, policies `RN...`.
- **A2P 10DLC** = Application-to-Person messaging over 10-digit long codes (US). Brands and campaigns are registered with **The Campaign Registry (TCR)**, the industry registry US carriers use.
- **Brand SID** = `BN...`; campaigns are the `usAppToPerson` resource under a **Messaging Service** (`MG...`).
- **Throughput tiers** are set by carriers from the **brand vetting score** (Standard vetting via a third-party evaluator raises the ceiling); sole-proprietor/low-volume brands have strict caps.
- The ISV registers **one brand + campaign per client**, keeping each business's carrier identity and reputation separate.
- Automation surface: `trusthub.v1.customerProfiles`, `trusthub.v1.trustProducts`, `messaging.v1.brandRegistrations`, `messaging.v1.services(...).usAppToPerson`.
