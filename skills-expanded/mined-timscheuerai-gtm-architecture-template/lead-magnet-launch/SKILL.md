---
name: lead-magnet-launch
description: Prepare and launch a finished lead magnet through a resource page, including email capture, delivery, email-tool segmentation, consent and launch QA. Use for publishing or auditing a resource funnel after the asset exists; lead-magnet-creator makes the asset.
---

Workspace: all context paths below (identity, audience, strategy, voice, brand, raw, output, index, log, workspace preferences and context scripts) resolve from `context/` in the kit root. Read both the root `AGENTS.md` and `context/AGENTS.md`. Skill-local `references/` and flowchart `scripts/` resolve from this skill directory.

# Lead magnet launch

Turn a finished resource into a working, measurable path from discovery to access. The resource delivers its promised value even if the reader never becomes a customer (the generosity rule), and delivery is not outreach.

## Locate the current system

Use `lead-magnet-creator` for the asset. Inspect the live resource page and the code or CMS behind it before choosing routes or data contracts. Check the email tool's current contacts, segments, topics and automations documentation before using an endpoint. Reuse an existing capture endpoint, contact sync and delivery mechanism when sound; never describe a proposed integration as live.

## Define the launch record

For each resource record a stable slug, owner, reader, promised outcome, format, asset version, canonical URL, delivery URL or email, thumbnail, source files, approved proof, publication status and 1 primary conversion event. Public copy states honestly whether access is immediate or emailed.

## Capture and delivery contract

- One submission gives the resource to a new or existing email. Normalise the email and make repeats idempotent per email and resource; a returning reader still gets access. Do not silently create a product account.
- Promotion links carry UTM parameters with your shared convention.
- Record the resource slug, timestamp, UTM values, delivery state and the exact consent choice separately from product signup state. Keep raw emails out of analytics events and logs.
- A resource request authorises resource fulfilment only. Product-update consent is a separate, clear choice, default off; never infer it from an earlier request, contact or account.
- Sync the lead to the email tool with resource origin and interest. On an existing contact, merge the interest without resetting unsubscribe status or earlier consent. A global unsubscribe stays in force.
- The delivery email contains the actual access link and is independent of any marketing sequence. A contact sync alone does not prove delivery.

## Verify before and after release

Preview the page, the form copy, the consent control, the email-tool writes, delivery and recipient scope before external writes. Test with a bounded scope: a new contact without product consent, an existing subscriber, an existing unsubscribed contact and a repeat request. After launch, report the canonical URL, asset and capture versions, test results, the segment or property used, delivery proof and anything unverified. Count page views, submissions, deliveries, explicit opt-ins and product signups separately.
