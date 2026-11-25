---
name: twilio-compliance-onboarding
version: 1.0.0
description: Run end-to-end Twilio messaging compliance onboarding — Trust Hub profile, EIN business verification, use-case selection, campaign vetting, and rejection remediation.
author: matrixx0070
tags: [twilio, compliance, trust-hub, onboarding, a2p-10dlc, verification]
capabilities: []
---

## When to use

Use this when a business is starting from zero and needs to get fully approved to send US A2P SMS — from creating the Trust Hub profile through an approved 10DLC campaign ready to send. Reach for it to sequence the steps correctly, estimate timelines, and recover from rejections. Use it when someone asks "what do I need to do, in what order, to start texting my customers legally in the US."

**Not for:** the ongoing content/opt-out/throughput rules once you're live — that is `twilio-compliance-traffic`. Not for the vendor model of registering many client businesses — that is `twilio-sms-isv-setup`. Not for choosing a sender type — that is `twilio-numbers-senders`. This skill is the *first-time, single-business* onboarding runbook.

## Method

1. Gather documents before touching the Console: exact **legal business name**, **EIN** (US tax ID) or business registration number, registered address, business website, and an **authorized representative** (name, email, title, phone). Decision point: name and EIN must match IRS records exactly — a DBA won't pass.
2. Create the **Primary Customer Profile** in **Trust Hub** with those details and submit for business verification.
3. Select the **use case** honestly: 2FA/OTP, account notifications, marketing/promotional, delivery notifications, or **mixed**. Decision point: if you send more than one category, pick mixed — mismatched use case is a top rejection reason.
4. Register the **brand** with TCR (identity + EIN vetting). Decision point: opt into **Standard vetting** if you need higher throughput; low-volume/sole-proprietor brands accept strict caps.
5. Create the **campaign**: description, 2-5 realistic **sample messages**, opt-in flow description and screenshot/URL, and flags for embedded links/phone numbers. Include your STOP/HELP language in samples.
6. Provision numbers and a **Messaging Service**, then **associate the approved campaign** with it so numbers inherit the use case and throughput.
7. Track state: profile verification (draft → pending-review → twilio-approved), then brand, then campaign (pending → in-review → approved). Expect carrier vetting to add days.
8. On rejection, read the specific reason, remediate at the right layer (profile/brand/campaign), and resubmit. Decision point: a rejected profile or brand blocks everything downstream — fix upstream first.
9. Send a test through the Messaging Service and confirm delivery before ramping volume.

## Example

```
Onboarding sequence (US A2P 10DLC, single business):

[1] Trust Hub Primary Customer Profile      -> submit  (verification: ~1-3 business days)
[2] TCR Brand Registration (EIN vetting)    -> submit  (brand vetted: minutes-1 day; Standard vetting longer)
[3] A2P Campaign (use case + samples)       -> submit  (carrier review: ~1-3 weeks, use-case dependent)
[4] Messaging Service + numbers             -> associate approved campaign
[5] Test send -> confirm delivery -> ramp within approved throughput

Common rejection -> remediation:
 - "EIN/legal name mismatch"        -> correct to exact IRS registration, resubmit brand
 - "Use case doesn't match samples" -> align use case or rewrite samples, resubmit campaign
 - "Missing opt-in evidence"        -> add consent flow screenshot/URL, resubmit campaign
 - "No opt-out language"            -> add STOP/HELP to sample messages, resubmit
```

## Pitfalls

- **Wrong or fuzzy business identity.** DBA instead of legal name, or a mistyped EIN, fails vetting and stalls the whole chain. Verify against IRS/registration records before submitting.
- **Use case that doesn't match samples.** Registering "notifications" then sending promos is a leading rejection. Declare mixed if you span categories, and make samples representative.
- **No opt-in evidence.** Carriers want to see how consent is collected. Provide a screenshot or URL of the actual opt-in flow.
- **Samples missing STOP/HELP.** Omitting opt-out language from sample messages triggers rejection. Include it in at least one sample.
- **Approved but unassociated campaign.** Approval alone sends nothing — the campaign must be linked to the Messaging Service and its numbers.
- **Under-estimating timelines.** Campaign carrier vetting can take one to several weeks. Start onboarding well before launch; don't promise a go-live that assumes instant approval.

## Output format

```
# Twilio Compliance Onboarding — <business>
IDENTITY: legalName=<> EIN=<> address=<> website=<> rep=<name/email/title>
TRUST HUB PROFILE: status=<draft|pending|approved>
BRAND (TCR): status=<> vetting=<Standard|low-volume>
CAMPAIGN: usecase=<2FA|notifications|marketing|mixed> status=<pending|in-review|approved|rejected>
  samples=<n>  optin_evidence=<yes/no>  stop_help_in_samples=<yes/no>
MESSAGING SERVICE: MG******************************** campaign_associated=<yes/no>
TIMELINE: profile=<eta> brand=<eta> campaign=<eta>
REJECTIONS: <reason -> remediation layer>, ...
GO-LIVE READY: <yes/no + blocking item>
```

## Reference

- **Trust Hub** is Twilio's compliance hub; the **Primary Customer Profile** holds verified business identity (legal name, **EIN**/registration number, address, authorized rep).
- **A2P 10DLC** onboarding chain: Customer Profile verification → **TCR brand** registration (EIN-vetted) → **campaign** registration (use-case + sample messages + opt-in evidence) → associate campaign to a **Messaging Service** (`MG...`).
- **Use cases** include 2FA/OTP, account notifications, marketing, delivery notifications, and **mixed**; the declared use case must match actual message content and samples.
- **Standard brand vetting** (third-party score) unlocks higher **throughput (TPS)** tiers; low-volume/sole-proprietor brands are capped.
- Typical **timelines:** profile verification days; brand vetting minutes-to-day; campaign carrier vetting **~1-3 weeks** depending on use case (marketing is slowest).
- **Rejection remediation** follows the dependency order — fix profile before brand, brand before campaign — because an upstream rejection blocks everything below it.
- Sample messages should include **STOP/HELP** opt-out language and reflect the real opt-in method to pass review.
