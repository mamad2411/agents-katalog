---
name: twilio-messaging-channel-advisor
version: 1.0.0
description: Given a use-case — region, volume, media, interactivity, compliance — recommend the right Twilio channel and sender type with the tradeoffs made explicit.
author: matrixx0070
tags: [twilio, channels, decision, whatsapp, rcs]
capabilities: []
---

## When to use

Use this skill when you know the use-case but not the channel: onboarding OTPs, marketing blasts, two-way support, appointment reminders, rich product cards. It maps requirements (region, monthly volume, media needs, interactivity, compliance appetite, budget) onto the correct Twilio channel (SMS, MMS, WhatsApp, RCS) and sender type (10DLC long code, toll-free, short code, WhatsApp sender, RCS agent).

Reach for it whenever someone says "should we use SMS or WhatsApp", "do we need a short code", or "how do we send images to customers".

**Not for:** the concrete configuration of a chosen path — use `twilio-messaging-services` to build the sender pool, `twilio-messaging-webhooks` for two-way/status wiring, and `twilio-messaging-overview` if you have not yet framed the problem at all.

## Method

1. Pin the region. Decision point: US/Canada long-code SMS mandates A2P 10DLC; other countries have their own sender rules (alphanumeric sender IDs, local long codes). MMS is effectively US/Canada only.
2. Pin the volume and throughput. Decision point: low/steady → 10DLC long code; high-throughput one-way (OTP, alerts) → short code or toll-free; bursty marketing → Messaging Service pool.
3. Pin the media need. Text only → SMS. Image/video/PDF in US/CA → MMS or WhatsApp. Rich carousels, buttons, branding → RCS or WhatsApp templates.
4. Pin interactivity. One-way notification → SMS/toll-free/short code. Two-way conversation → WhatsApp, RCS, or a two-way SMS number, and wire `twilio-messaging-webhooks`.
5. Pin compliance tolerance. Decision point: fastest-to-launch US path is toll-free (verification, no per-campaign 10DLC); highest-trust/highest-throughput is a short code (weeks of provisioning); balanced is 10DLC.
6. Emit the recommendation with the runner-up and why it lost.

Channel selection table:

| Use-case | Channel | Sender type | Why |
|---|---|---|---|
| US OTP / 2FA at scale | SMS | Short code or toll-free | Highest throughput, best deliverability |
| US low-volume alerts | SMS | 10DLC long code | Cheap, quick if brand registered |
| US images to customers | MMS | 10DLC / toll-free | Native media, no app needed |
| Global two-way support | WhatsApp | WhatsApp sender | Rich, cheap intl, session window |
| Rich branded cards (Android) | RCS | RCS agent | Verified branding, carousels, read receipts |
| International notifications | SMS | Local long code / alpha sender | Regional deliverability |

Sender-type tradeoffs:

| Sender | Throughput | Setup time | Two-way | Media | Notes |
|---|---|---|---|---|---|
| 10DLC long code | Low–med | Days (registration) | Yes | MMS | Required for US A2P long code |
| Toll-free | Med–high | Days (verification) | Yes | MMS | Fast US launch |
| Short code | High | Weeks | Yes | MMS | Premium, best trust |
| WhatsApp | Med | Days–weeks (approval) | Yes | Yes | 24h window + templates |
| RCS | Med | Weeks (agent verify) | Yes | Yes | Android; falls back to SMS |

## Example

A decision emitted as structured output:

```json
{
  "use_case": "US appointment reminders with a photo of the location",
  "recommended_channel": "MMS",
  "recommended_sender": "toll-free (verified)",
  "compliance": "toll-free verification (no per-campaign 10DLC)",
  "runner_up": "10DLC long code MMS",
  "runner_up_rejected_because": "slower per-campaign registration, lower throughput for bursts",
  "next_skill": "twilio-messaging-services"
}
```

## Pitfalls

- RCS is not universal. iOS/older-Android/unsupported carriers do not receive RCS; always design an SMS fallback.
- WhatsApp is session-bound. Outside the 24-hour window you must use an approved template (63016); it is not a drop-in for one-way SMS blasts without template planning.
- MMS is regional. Sending MMS outside US/Canada silently degrades or fails; prefer WhatsApp for international media.
- Short codes are slow to get. Do not promise a short-code launch on a tight timeline; toll-free or 10DLC is the fast path.
- Alphanumeric sender IDs are one-way and country-specific, and are not supported for US destinations.

## Output format

This skill produces a recommendation object: the chosen channel, the chosen sender type, the compliance path, a named runner-up with the reason it lost, and the next sibling skill to execute. It does not send messages or provision senders.

## Reference

- Channels: SMS/MMS via `https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json`; WhatsApp uses the same `Messages` endpoint with `whatsapp:+E164` on `To`/`From`; RCS via a Messaging Service with an RCS agent and Content templates.
- Content templates (WhatsApp/RCS rich): `https://content.twilio.com/v1/Content`, referenced at send time by `ContentSid` (`HX...`) + `ContentVariables` (JSON string).
- US compliance: A2P 10DLC brand + campaign via TrustHub for long codes; toll-free verification for toll-free; short-code provisioning application for short codes.
- Segment economics: GSM-7 160 (153 concatenated); UCS-2 70 (67 concatenated) — Unicode content multiplies segment count and cost.
- Errors that steer channel choice: 21408 (region not enabled), 30007 (carrier filtered — usually unregistered US long code), 63016 (WhatsApp free-form outside 24h), 21610 (recipient opted out).
- Throughput rough guide: short code ~100+ MPS; toll-free tens of MPS once verified; 10DLC MPS scales with the campaign's carrier trust score.
