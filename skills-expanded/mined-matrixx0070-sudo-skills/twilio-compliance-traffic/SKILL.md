---
name: twilio-compliance-traffic
version: 1.0.0
description: Make SMS traffic compliant and deliverable — A2P 10DLC/TCR registration, toll-free verification, STOP/HELP opt-out, SHAFT content rules, and throughput.
author: matrixx0070
tags: [twilio, compliance, a2p-10dlc, tcpa, opt-out, ctia]
capabilities: []
---

## When to use

Use this when messages are getting filtered, blocked, or you're about to launch traffic and need it to actually reach handsets and stay on the right side of carrier and legal rules. Reach for it to register A2P 10DLC brands/campaigns for US long codes, verify toll-free numbers, implement STOP/HELP keyword handling, and audit message content against SHAFT and CTIA guidelines. Use it whenever "why are our texts undelivered" or "are we allowed to send this" comes up.

**Not for:** the multi-tenant vendor registration model (registering on behalf of client businesses) — that is `twilio-sms-isv-setup`. Not for the step-by-step Trust Hub business-verification walkthrough — that is `twilio-compliance-onboarding`. Not for picking a sender type — that is `twilio-numbers-senders`. This skill is about keeping live traffic compliant.

## Method

1. Identify the sender type in play and its compliance gate: US long code → **A2P 10DLC** (TCR brand + campaign); toll-free → **toll-free verification**; short code → CTIA short-code application. Decision point: no US A2P traffic should run on an unregistered/unverified sender.
2. Register (or confirm) the **brand** and a **campaign** matched to the real use case (marketing, 2FA, notifications, mixed) with accurate sample messages and opt-in evidence.
3. Implement **opt-in**: capture and be able to prove consent (checkbox, keyword join, web form). TCPA requires prior express consent — and prior express *written* consent for marketing/autodialed messages.
4. Implement **opt-out**: honor **STOP** (also STOPALL, UNSUBSCRIBE, CANCEL, END, QUIT) by ceasing messages, and support **HELP/INFO**. Decision point: use Twilio's **Advanced Opt-Out** on the Messaging Service to auto-handle keywords, or handle them yourself — but one of the two must exist.
5. Audit content against **SHAFT** (no Sex, Hate, Alcohol, Firearms, Tobacco — cannabis included) and CTIA guidelines; flag public URL shorteners, which carriers penalize.
6. Match sending rate to your approved **throughput (TPS)** tier; pool numbers to spread load rather than exceeding a single number's cap.
7. Monitor delivery: watch **error codes** (30007 carrier filtered, 30034 unregistered 10DLC, 30032 toll-free not verified) and delivery-receipt status callbacks.
8. Remediate: registration errors → fix brand/campaign; filtering → fix content/consent/opt-out; throughput → raise tier or add numbers.

## Example

```javascript
// Advanced Opt-Out managed by the Messaging Service handles STOP/HELP automatically.
// If handling yourself, respond to inbound STOP and suppress future sends:
app.post('/inbound', (req, res) => {
  const body = (req.body.Body || '').trim().toUpperCase();
  const from = req.body.From;
  const stopWords = ['STOP', 'STOPALL', 'UNSUBSCRIBE', 'CANCEL', 'END', 'QUIT'];
  const helpWords = ['HELP', 'INFO'];
  const twiml = new (require('twilio')).twiml.MessagingResponse();

  if (stopWords.includes(body)) {
    suppress(from);                              // add to do-not-message list
    twiml.message('You are unsubscribed. No more messages will be sent. Reply START to resubscribe.');
  } else if (helpWords.includes(body)) {
    twiml.message('Acme Alerts: support@acme.example. Msg&data rates may apply. Reply STOP to cancel.');
  }
  res.type('text/xml').send(twiml.toString());
});
```

## Pitfalls

- **Sending on unregistered 10DLC.** Error 30034 / heavy filtering. Register brand+campaign with TCR before any US long-code A2P traffic.
- **Ignoring STOP.** Failing to honor opt-out is a TCPA violation and gets you carrier-blocked. Honor STOP immediately and permanently until an explicit re-opt-in.
- **SHAFT / prohibited content.** Alcohol, cannabis, firearms, and hate content are filtered regardless of registration. Audit templates before launch.
- **Public URL shorteners.** Shared shorteners (bit.ly, tinyurl) are widely blocked because bad actors abuse them. Use a branded/dedicated link domain.
- **Exceeding throughput.** Blasting above your TPS tier queues and delays messages and can look like an attack. Match rate to tier and pool numbers.
- **No consent record.** If challenged, you must produce proof of opt-in. Log timestamp, source, and the exact consent language.

## Output format

```
# Twilio Traffic Compliance
SENDER TYPE: <10DLC|toll-free|short code>   MARKET: US
REGISTRATION: brand=<BN...|n/a> campaign=<status> | TF verification=<status> 
OPT-IN: method=<checkbox|keyword|web> consent_logged=<yes/no>
OPT-OUT: STOP=<handled: advanced/custom> HELP=<handled>
CONTENT AUDIT: SHAFT=<pass/fail> shortener=<branded/public> 
THROUGHPUT: tier=<TPS> numbers_pooled=<n>
DELIVERY: error_codes_seen=<30007|30034|30032|none> action=<remediation>
```

## Reference

- **A2P 10DLC** (US 10-digit long code, Application-to-Person) requires a **brand + campaign** registered with **The Campaign Registry (TCR)**; carriers filter unregistered traffic. Toll-free requires **toll-free verification**; short codes require a CTIA short-code application.
- **TCPA** requires prior express consent for non-marketing and prior express **written** consent for marketing/autodialed texts; violations carry per-message statutory damages.
- **Opt-out keywords:** STOP, STOPALL, UNSUBSCRIBE, CANCEL, END, QUIT; **help:** HELP, INFO; resubscribe: START/YES. Twilio's **Advanced Opt-Out** (Messaging Service) automates these.
- **SHAFT** = Sex, Hate, Alcohol, Firearms, Tobacco (cannabis grouped in) — prohibited/restricted content per CTIA Messaging Principles.
- Common errors: **30007** (message filtered by carrier), **30034** (US A2P 10DLC number not registered), **30032** (toll-free not verified).
- **Throughput (TPS)** is set by carrier per registered campaign/brand vetting tier; pool numbers in a Messaging Service to scale within limits.
