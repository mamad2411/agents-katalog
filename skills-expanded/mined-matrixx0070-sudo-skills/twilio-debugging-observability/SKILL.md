---
name: twilio-debugging-observability
version: 1.0.0
description: Diagnose Twilio issues using Debugger error logs, Monitor/Alerts API, Event Streams, resource SIDs, and Voice Insights.
author: matrixx0070
tags: [twilio, debugging, observability, monitor, event-streams, error-codes]
capabilities: []
---

## When to use

Use this when a message or call misbehaved and you need to find out why — a webhook failed, delivery stalled, or an error code appeared. Use it to pull error logs from the Debugger, query the Monitor API for Alerts/Events, stream events to your own sink, and correlate everything by resource SID. Use it when you need delivery-status ground truth or per-call voice quality metrics.

**Not for:** designing webhooks in the first place — use twilio-webhook-architecture. Building retry/backoff/idempotency — use twilio-reliability-patterns. Email event/bounce diagnostics — use twilio-email-deliverability-advisor.

## Method

1. Start with the Debugger. Console → Monitor → Logs → Errors, or `twilio debugger:logs:list`. Each entry has an error code, the request/response payloads, and the affected resource SID. This is the first stop for webhook and delivery failures.
2. Look up the error code. Map the numeric code (e.g. 11200 HTTP retrieval failure, 30007 carrier filtered) via twilio.com/docs/api/errors before theorizing — the code plus its request/response usually names the root cause directly.
3. Correlate by SID. Every resource has a typed SID prefix: `SM`/`MM` message, `CA` call, `AC` account, `MG` messaging service, `NO` notification/alert. Fetch the resource (`client.messages(sid).fetch()`) to see current status and `errorCode`/`errorMessage`.
4. Query the Monitor API for programmatic access. `Alerts` (`/v1/Alerts`) are debugger errors; `Events` (`/v1/Events`) are the audit trail of configuration/API changes. Filter by date, resource SID, or product. Decision point: recurring same-code alerts → fix root cause; one-off → likely transient carrier issue.
5. For inbound-request failures, inspect the request the way Twilio saw it: the alert payload includes the URL called, method, and the response body/status your server returned — use it to reproduce.
6. Stand up Event Streams for continuous observability. Create a Sink (webhook or Amazon Kinesis) and a Subscription to event types; Twilio pushes events (message status, voice, etc.) to your pipeline in near real time — better than polling logs at scale.
7. For voice quality, open Voice Insights: per-call metrics (jitter, packet loss, MOS), SIP/PSTN details, and call-summary events. Use it when calls connect but sound bad or drop.
8. Set proactive alerting. Subscribe to Debugger webhook notifications (Console → Monitor → Debugger → webhook) so new errors POST to you immediately.
9. Emit your own correlation ID. Store the SID alongside your request ID in your logs so a support ticket or a customer complaint maps to a single Twilio resource.

## Example

```bash
# CLI: recent errors + one resource
twilio debugger:logs:list --log-level error -o json
twilio api:core:messages:fetch --sid SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx -o json
```

```javascript
import twilio from 'twilio';
const client = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);

// Monitor API: alerts (debugger errors) in a window
const alerts = await client.monitor.v1.alerts.list({
  startDate: new Date(Date.now() - 24*3600*1000),
  limit: 50,
});
alerts.forEach(a => console.log(a.errorCode, a.alertText, a.resourceSid));

// Delivery ground truth for a specific message
const m = await client.messages('SMxxxx...').fetch();
console.log(m.status, m.errorCode, m.errorMessage); // e.g. undelivered 30007

// Event Streams: create a webhook sink + subscription
const sink = await client.events.v1.sinks.create({
  description: 'prod-observability',
  sinkConfiguration: { destination: 'https://app.example.com/events', method: 'POST', batch_events: true },
  sinkType: 'webhook',
});
await client.events.v1.subscriptions.create({
  description: 'message + voice status',
  sinkSid: sink.sid,
  types: [{ type: 'com.twilio.messaging.message.delivered' }, { type: 'com.twilio.voice.insights.call-summary.complete' }],
});
```

## Pitfalls

- **Theorizing before reading the error body.** The Debugger alert contains the actual request URL, response status, and body from your server. Read it first; the code + payload usually name the cause.
- **Confusing Alerts with Events.** Monitor `Alerts` = errors/warnings; `Events` = audit log of who changed what. Querying the wrong one wastes time.
- **Polling logs at scale.** The Debugger UI/list is fine for spot checks but rate-limited and lossy for volume. Use Event Streams (webhook or Kinesis) for real-time, durable delivery of events.
- **Ignoring SID prefixes.** `SM` vs `MM` vs `CA` tells you the resource type instantly; passing a call SID to a message fetch just 404s.
- **Missing errorCode on the resource.** A message can be `undelivered` with a 30xxx `errorCode` that never appears in create logs — always fetch the resource or consume status callbacks.
- **Alert retention.** Debugger logs retain ~30 days (13 months for some accounts/products). Export via Event Streams if you need long-term history.

## Output format

```
INCIDENT: <symptom>  window=<from..to>
RESOURCE: sid=<SM../CA..> status=<..> errorCode=<code> errorMessage=<..>
SOURCE: <Debugger alert | Monitor API | Event Streams | Voice Insights>
ROOT CAUSE: <error-code meaning + request/response evidence>
SCOPE: <one-off | recurring count=<n>>
FIX: <config/code change>  MONITORING: <alert/subscription added>
```

## Reference

- **Debugger / Error Logs:** Console → Monitor → Logs → Errors; CLI `twilio debugger:logs:list`. Captures error code, request, and response for each event.
- **Monitor API:** `GET /v1/Alerts` and `GET /v1/Alerts/{Sid}` (debugger errors, filter by `LogLevel`, `StartDate`, `EndDate`); `GET /v1/Events` (audit trail of API/config changes, filter by `ResourceSid`, `Actor`, `EventType`).
- **Event Streams:** `Sinks` (webhook or `kinesis`) + `Subscriptions` to typed events (`com.twilio.messaging.message.*`, `com.twilio.voice.insights.*`). Near-real-time, durable fan-out.
- **SID prefixes:** `AC` account, `SM`/`MM` message, `CA` call, `MG` messaging service, `NO` notification/alert, `SK` API key, `EV` event.
- **Common error codes:** 11200 HTTP retrieval failure, 11205 HTTPS connection failed, 12100/12200 TwiML/document parse, 30003–30008 message delivery failures, 30007 carrier filtered (spam), 21211 invalid number.
- **Voice Insights:** per-call quality (MOS, jitter, packet loss, latency), SIP details, call-summary and call-quality events; call-summary available via API and Event Streams.
- **Delivery status:** authoritative via status callbacks and `messages(sid).fetch()` — status + `errorCode` + `errorMessage`.
