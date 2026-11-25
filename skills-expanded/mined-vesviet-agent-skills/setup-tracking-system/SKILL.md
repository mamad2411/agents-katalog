---
name: setup-tracking-system
description: Configure advanced privacy-first tracking including Server-to-Server (S2S) postbacks, Meta CAPI v20+, TikTok Events API, Google Enhanced Conversions, and affiliate webhooks. Use when launching a new campaign, migrating from pixel-only to server-side tracking, or diagnosing attribution gaps.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
version: "1.0.0"
---

# Setup Tracking System

Use this skill to deploy highly accurate, privacy-first tracking systems necessary for MMO operations in a cookieless landscape.

## When to Use

- launching a new performance marketing or affiliate campaign requiring multi-channel attribution
- migrating from client-side pixels to Server-to-Server (S2S) tracking, Meta CAPI, and TikTok Events API
- implementing Google Enhanced Conversions with gclid, wbraid, and gbraid click parameter handling
- wiring affiliate network webhooks for conversions, rebills, cancellations, and chargebacks
- diagnosing attribution discrepancies, postback drop-offs, or low Event Match Quality (EMQ) scores

## Example (S2S Postback, TikTok Events API & Google Enhanced Conversions)

```bash
# Affiliate network conversion postback with transaction ID, click ID, and payout
https://tracker.example.com/postback?cid={clickid}&payout={payout}&txid={txid}&status={status}
```

```json
// TikTok Events API payload specification (POST https://business-api.tiktok.com/open_api/v1.3/event/track/)
{
  "pixel_code": "C1234567890TIKTOK",
  "event": "CompletePayment",
  "event_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "timestamp": "2027-01-15T10:30:00Z",
  "context": {
    "user": {
      "email": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae",
      "phone_number": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",
      "ttclid": "E.0.123456789.abcdef",
      "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
      "ip": "198.51.100.42"
    },
    "page": { "url": "https://offer.example.com/checkout/success" }
  },
  "properties": { "currency": "USD", "value": 49.99 }
}
```

```json
// Affiliate lifecycle webhook specification (POST https://tracker.example.com/api/v2/affiliate-webhook)
{
  "event_type": "rebill",
  "transaction_id": "aff-tx-8839210",
  "click_id": "clk-us-east-99214",
  "payout": 37.50,
  "currency": "USD",
  "affiliate_network": "MaxBounty",
  "offer_id": "saas-trial-sub-101",
  "status": "approved",
  "signature": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
```

```typescript
// Google Ads Enhanced Conversions API upload snippet
await googleAdsClient.conversionUploads.uploadClickConversions({
  customerId: "1234567890",
  conversions: [{
    conversionAction: "customers/1234567890/conversionActions/987654321",
    conversionDateTime: "2027-01-15 10:30:00+00:00",
    conversionValue: 49.99,
    currencyCode: "USD",
    gbraid: gbraid || undefined,
    wbraid: wbraid || undefined,
    gclid: gclid || undefined,
    userIdentifiers: [
      { hashedEmail: hashSha256(email) },
      { hashedPhoneNumber: hashSha256(phoneE164) }
    ]
  }]
});
```

## Core Rules

- **TRACKING-LOCK**: Never rely solely on client-side JavaScript pixels. Always implement and verify Server-to-Server (S2S) fallbacks. Pixel-only tracking suffers > 35% signal loss from Safari ITP, Brave, ad blockers, and iOS restrictions.
- **META-CAPI-EMQ**: Target Event Match Quality (EMQ) >= 8.0/10 for lower-funnel events (`Purchase`, `Lead`). Transmit server-side `fbp`, `fbc`, `em` (SHA-256 lowercase email), `ph` (E.164 SHA-256 phone), `client_ip_address`, and `client_user_agent`. Persist `fbclid` in HTTP-only first-party cookies for 90 days.
- **TIKTOK-EVENTS-API**: Send server-side events using standardized payload structures containing `pixel_code`, `event`, `event_id`, ISO-8601 `timestamp`, and hashed `context.user` fields (`email`, `phone_number`, `ttclid`). Match `event_id` identically with web pixel events for 48-hour deduplication.
- **GOOGLE-ENHANCED-CONVERSIONS**: Capture and forward Google click identifiers: standard `gclid` on web and modeled privacy click identifiers (`wbraid` for web-to-app / iOS cross-device, `gbraid` for app-to-web conversions). Pass SHA-256 normalized user identifiers (`user_identifiers.hashed_email`, `user_identifiers.hashed_phone_number`) via the Google Ads Conversion API.
- **AFFILIATE-WEBHOOK-SPEC**: Process incoming affiliate network webhooks through a standardized schema supporting events: `conversion`, `rebill`, `refund`, and `chargeback`. Validate signature tokens and enforce idempotency on `(txid, status)` pairs.
- **PII-NORMALIZATION**: Before SHA-256 hashing, lowercase all strings, strip leading/trailing whitespace, and normalize phone numbers to E.164 format (`+14155552671`) without punctuation.
- **EVENT-DEDUPLICATION**: Share identical UUID v4 `event_id` across client-side pixel triggers and server-side CAPI/Events API requests to prevent double-counting conversions within ad network attribution windows.
- **CTIT-FRAUD-FILTER**: Reject S2S postbacks where Click-To-Conversion-Time (CTIT) < 2.5 seconds (automated script injection / IVT). Flag conversions > 7 days on impulse performance offers for manual click hijack review.
- **IDEMPOTENT-POSTBACK-QUEUE**: Ingestion endpoints MUST push postbacks into durable message queues (SQS/Kafka) with unique database constraints on `(transaction_id, event_type)` to eliminate duplicate payouts from retry storms.
- **IOS18-AAK-COMPLIANCE**: Support Apple AdAttributionKit (AAK) schemas alongside SKAN; handle crowd anonymity tiers (0-3) and coarse/fine conversion value mapping.

## Suggested Process

1. **Parameter Capture at Edge**: Configure edge proxy/CDN workers (Cloudflare Workers/Fastly) to parse `fbclid`, `gclid`, `wbraid`, `gbraid`, `ttclid`, and tracker `clickid` from incoming request query parameters. Write them into HTTP-only, Secure, SameSite=Lax first-party cookies on the apex domain.
2. **Affiliate Tracker Integration**: Deploy S2S postback endpoints on tracking servers (Voluum, Binom, Keitaro). Wire affiliate network conversion postback URLs passing `clickid`, `payout`, `txid`, and conversion status flags.
3. **Multi-Platform S2S Dispatch**: Build unified server-side conversion dispatcher that fans out events to Meta CAPI v20+, TikTok Events API v1.3, and Google Ads Enhanced Conversions API with normalized SHA-256 hashed identity vectors.
4. **Affiliate Lifecycle Webhook Handlers**: Implement webhook listeners for post-conversion events (`rebill`, `refund`, `chargeback`). Update tracker revenue balances and push value adjustments to ad networks.
5. **Anti-Fraud & Quality Validation**: Apply CTIT threshold filtering (< 2.5s rejection) and verify Meta EMQ >= 8.0, TikTok Match Quality >= 7.5, and Google upload success in platform event monitoring consoles.
6. **End-to-End Dry Run**: Trigger end-to-end sandbox conversions across all channels; verify zero duplicate attribution and correct payload receipt in ad platform event managers.

## Checklist

- [ ] Edge router captures `fbclid`, `gclid`, `wbraid`, `gbraid`, and `ttclid` into first-party cookies.
- [ ] S2S postback URLs configured with `{clickid}`, `{payout}`, and `{txid}` parameters.
- [ ] Meta CAPI v20+ configured with server-side `fbp`, `fbc`, `em`, `ph`, IP, and user-agent.
- [ ] Meta EMQ verified >= 8.0/10 in Events Manager for core conversion events.
- [ ] TikTok Events API v1.3 integrated with `pixel_code`, `event_id`, `ttclid`, and hashed user data.
- [ ] Google Enhanced Conversions configured with `gclid`, `wbraid`, `gbraid`, and hashed identifiers.
- [ ] Affiliate webhook handlers implemented for `conversion`, `rebill`, `refund`, and `chargeback`.
- [ ] PII normalized (lowercased, whitespace trimmed, E.164 phones) prior to SHA-256 hashing.
- [ ] UUID v4 `event_id` shared across browser pixels and S2S payloads for deduplication.
- [ ] CTIT fraud filter rejects sub-2.5s conversions as programmatic injection.
- [ ] Idempotent queue (Kafka/SQS) with unique `(transaction_id, event_type)` constraint active.
- [ ] Test conversion verified end-to-end across tracker, affiliate network, and ad platforms.

## Output Contracts

When the tracking system is configured or updated for a campaign handoff, emit:

- **`contracts/schemas/mmo-campaign-spec.json`** defining the tracking topology, click parameter mapping (`gclid`, `fbclid`, `ttclid`), postback endpoints, webhook schemas, and platform dataset bindings.
- **`contracts/schemas/deployment-plan.json`** capturing S2S endpoints, postback handlers, event dedup keys, consent capture parameters, and rollback procedures.
- Markdown tracking architecture summary detailing data flow, EMQ targets, and compliance boundaries.

Skip emission for local tracking experiments that do not cross role boundaries.

## Failure Modes

- **Event deduplication failure**: Browser pixel and server-side CAPI/Events API use different `event_id` values, causing 2x conversion inflation in ad algorithms. Mitigation: generate UUID v4 at edge landing and persist across client and server dispatch.
- **Lost iOS click attribution**: Failure to capture `wbraid`/`gbraid` on iOS devices leads to 0% attribution on Google Ads web campaigns. Mitigation: ensure edge gateway preserves and passes `wbraid`/`gbraid` to Google Conversion APIs.
- **Affiliate rebill desynchronization**: Recurring subscription rebills or refunds are not reported back to ad platforms, skewing ROAS. Mitigation: connect affiliate network webhooks to server-side offline conversion adjusters.
- **PII hashing non-compliance**: Sending raw email/phone or improperly formatted hashes triggers platform rejection and privacy violations. Mitigation: enforce strict E.164 normalization and SHA-256 hashing pipeline before payload construction.
- **CTIT fraud injection**: Sub-second conversion bots inflate tracker conversions without generating real revenue. Mitigation: enforce hard 2.5s CTIT minimum gate and quarantine suspicious conversions.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: Customer identifiers and PII used for attribution must be SHA-256 hashed before transmission; never log or persist unhashed PII in tracking databases.
- **ASI04 Supply Chain**: Tracking SDKs, webhook dispatchers, and S2S postback libraries must be schema-validated against approved package manifests; treat unknown packages as untrusted.
- **ASI05 RCE Guard**: Never construct S2S postback payloads, database queries, or webhook handlers directly from unsanitized query string parameters.
- **ASI07 Inter-Agent Communication**: Tracking topology and campaign parameters must be emitted via `contracts/schemas/mmo-campaign-spec.json` so downstream analytics and automation agents can consume structured configs.
- **ASI09 Human-Agent Trust Exploitation**: Never represent tracking coverage as 100% compliant without documenting residual signal loss from ad blockers and private browsing modes.

## Related Skills

- **analyze-campaign-roi**: Ingest and evaluate conversion and attribution data collected by this tracking system.
- **integrate-api-client**: Implement client-side click-capture and event dispatch snippets on custom landing pages.
- Companion reference: `references/server-to-server-postback-and-capi-specs.md`
- Companion example: `examples/meta-capi-s2s-event-dispatcher.ts`
