---
name: twilio-marketing-promotions-advisor
version: 1.0.0
description: Advise on compliant marketing and promotional SMS over Twilio — TCPA express written consent, A2P 10DLC marketing use-case registration, opt-in capture, quiet hours, frequency, and STOP handling.
author: matrixx0070
tags: [twilio, sms, marketing, tcpa, a2p-10dlc, consent, opt-in]
capabilities: []
---

## When to use

Use this when you are planning promotional, offer, or campaign SMS to consumers in the US and need to know what makes it legal and deliverable rather than filtered or fined. Use it before you launch a marketing campaign, when you are capturing opt-ins on a web form, or when carrier filtering is blocking your promotional traffic. This is advisory — it decides consent, registration, and content rules; it does not push the messages itself.

**Not for:** provisioning the sending number or long code (see `twilio-numbers-senders`), the general A2P/traffic registration mechanics (see `twilio-compliance-traffic`), or transactional alerts and receipts, which have a lower consent bar (see `twilio-notifications-alerts-advisor`).

## Method

1. Classify the message as marketing/promotional. If it advertises, offers, or upsells, it is marketing under TCPA — this is the highest consent tier, regardless of how "informational" it feels.
2. Require express written consent before the first marketing text. The consent record must show the consumer affirmatively agreed to receive marketing texts at that number, with clear disclosure of the program, message frequency, "msg & data rates may apply," and links to Terms and Privacy Policy. Decision point: no logged express written consent → do not send; capture it first.
3. Register the A2P 10DLC Brand and a Campaign with the correct marketing/promotional use-case. Carriers filter unregistered marketing traffic hard; the use-case, sample messages, and opt-in flow you register must match what you actually send.
4. Capture and store the opt-in: timestamp, the exact consent language shown, IP/source, and the number. This record is your defense in a TCPA claim and is often requested during campaign vetting.
5. Enforce quiet hours. Send only within the recipient's local time window (the common safe standard is 8am–9pm local); many state mini-TCPA laws are stricter. Schedule against the recipient time zone, not the server's.
6. Cap frequency to what you disclosed at opt-in and keep it reasonable — over-messaging drives opt-outs, spam reports, and carrier throttling.
7. Handle STOP/UNSUBSCRIBE and HELP. Honor STOP, UNSUBSCRIBE, CANCEL, END, QUIT immediately and permanently; respond to HELP. Twilio's Advanced Opt-Out can automate this, but you must never re-message a stopped number.
8. Monitor deliverability and error codes. Watch for 30007 (carrier filtered), 30034 (unregistered/violation), and opt-out rates; if filtering climbs, fix content and registration rather than rotating numbers.

## Example

Compliant marketing opt-in confirmation and a well-formed first message:

```
Opt-in web form (logged): "By checking this box you agree to receive
recurring marketing texts from Acme at the number provided. Up to 4
msgs/mo. Msg & data rates may apply. Reply STOP to cancel, HELP for help.
Terms: acme.com/terms  Privacy: acme.com/privacy"

First SMS (from a registered 10DLC number):
"Acme: You're in! 15% off your first order: ACME15.
Up to 4 msgs/mo. Reply STOP to opt out, HELP for help."
```

```bash
# Send only after consent + registration; from your registered 10DLC number
curl -sX POST "https://api.twilio.com/2010-04-01/Accounts/$ACCOUNT_SID/Messages.json" \
  -u "$TWILIO_API_KEY:$TWILIO_API_SECRET" \
  --data-urlencode "To=+15551234567" \
  --data-urlencode "From=+15559876543" \
  --data-urlencode "Body=Acme: 15% off first order: ACME15. Reply STOP to opt out."
```

## Pitfalls

- **Treating opt-in for one thing as consent for marketing.** A phone number given for a receipt or account alert is not marketing consent. Marketing needs its own express written opt-in.
- **Missing disclosures at opt-in.** Omitting frequency, "msg & data rates may apply," or Terms/Privacy links weakens consent and fails campaign vetting. Include all of them in the checkbox/keyword flow.
- **Sending unregistered marketing over a 10DLC number.** Unregistered or use-case-mismatched marketing gets filtered (30007) or blocked (30034). Register the marketing campaign and match your samples.
- **Ignoring quiet hours and time zones.** Sending at the wrong local hour is a TCPA violation even with consent. Schedule by recipient local time; assume 8am–9pm and check state rules.
- **Not honoring STOP permanently.** Re-messaging after opt-out is a direct TCPA liability. Suppress stopped numbers forever, across all campaigns.
- **Purchased or scraped lists.** Consent is not transferable; texting a bought list is a violation regardless of how the number was obtained.

## Output format

```
# Marketing SMS Review: <campaign>
CLASSIFICATION: marketing/promotional (TCPA highest tier)
CONSENT: express-written=<yes|no> record=<source+timestamp+language>
REGISTRATION: 10DLC brand=<...> campaign-use-case=marketing status=<...>
CONTENT: disclosures=[freq, rates, STOP/HELP, terms/privacy] pass=<y/n>
TIMING: quiet-hours=<local window> tz-source=recipient freq-cap=<n/period>
OPT-OUT: STOP handling=<auto|manual> suppression=permanent
DELIVERABILITY: watch=[30007,30034] opt-out-rate=<%>
VERDICT: <send | fix-before-send> BLOCKERS: [...]
```

## Reference

- Legal basis: US TCPA requires prior express written consent for marketing/promotional texts and autodialed marketing; transactional/informational messages have a lower bar. State mini-TCPA laws (e.g. Florida, Oklahoma) can be stricter on timing and consent.
- Carrier requirement: US application-to-person messaging over standard 10-digit long codes must be registered under A2P 10DLC (Brand + Campaign) via The Campaign Registry; the campaign's use-case (marketing, mixed, etc.), sample messages, and opt-in flow are vetted.
- Twilio specifics: Messaging API `POST /2010-04-01/Accounts/{AccountSid}/Messages.json`; Advanced Opt-Out and Messaging Services manage STOP/HELP keywords. Standard opt-out keywords: STOP, STOPALL, UNSUBSCRIBE, CANCEL, END, QUIT; help: HELP, INFO.
- Common error codes: 30007 (message filtered by carrier), 30034 (A2P registration/use-case violation), 21610 (attempt to message a number that sent STOP).
- CTIA Messaging Principles and Best Practices define the industry norms carriers enforce for consent, content, and opt-out on promotional traffic.
