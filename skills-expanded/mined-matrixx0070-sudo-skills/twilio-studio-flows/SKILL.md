---
name: twilio-studio-flows
version: 1.0.0
description: Design and operate Twilio Studio drag-and-drop IVR and messaging flows — widgets, triggers, and the Execution REST API — without writing full call/message routing code.
author: matrixx0070
tags: [twilio, studio, ivr, flow, messaging, automation]
capabilities: []
---

## When to use

Use this when you want to build a phone (IVR) or SMS/WhatsApp conversation as a visual flow instead of hand-coding TwiML and webhooks: a call menu, an appointment reminder that gathers a reply, a lead-capture bot, an after-hours router. Reach for it when the logic is branchy but expressible as widgets and you want product/ops people to edit it. Also use it to trigger, inspect, or debug a running flow via the Executions REST API.

**Not for:** skills-based routing of tasks to human agents/workers — use twilio-taskrouter-routing. Not for sending/checking OTP codes — use twilio-verify-send-otp (though a Studio flow can call Verify). Not for phone number intelligence — use twilio-lookup-phone-intelligence.

## Method

1. **Pick the trigger.** A Flow has three trigger entry points: Incoming Message, Incoming Call, and REST API. Decision point: reminders/outbound campaigns start from REST API (`POST .../Executions`); customer-initiated support starts from Incoming Call/Message.
2. **Sketch the states as widgets.** Map the conversation to widgets before dragging: Send & Wait For Reply, Send Message, Gather Input on Call (DTMF/speech), Say/Play, Run Function, HTTP Request, Split Based On, Set Variables, Connect Call To, Enqueue (to TaskRouter).
3. **Wire the branches.** Each widget has transition events (e.g. Gather → `keypress`, `speech`, `timeout`, `no_match`). Decision point: always wire `timeout` and `no_match` — unwired transitions dead-end the caller.
4. **Reference variables with Liquid.** Read prior widget output and flow variables via Liquid, e.g. `{{widgets.gather_1.Digits}}`, `{{flow.data}}`, `{{trigger.message.Body}}`.
5. **Call out for data/logic.** Use HTTP Request or Run Function widgets for lookups, DB writes, or calling other Twilio APIs (Verify, Lookup). Keep heavy logic in a Function, not spread across many Splits.
6. **Publish the flow.** Studio requires an explicit Publish to make edits live; a Flow has revisions. Decision point: test on the current draft/test number before publishing to production.
7. **Trigger programmatically when outbound.** `POST /v2/Flows/{FlowSid}/Executions` with `To`, `From` (a Studio-connected Twilio number), and `Parameters` (JSON injected as `{{flow.data}}`).
8. **Inspect and debug via REST.** List/fetch Executions and read the ExecutionContext to see the variable state at each step; use it to diagnose where a flow branched wrong.

## Example

```bash
# Trigger a flow (e.g. appointment reminder) via REST
curl -X POST "https://studio.twilio.com/v2/Flows/$FLOW_SID/Executions" \
  --data-urlencode "To=+14155551234" \
  --data-urlencode "From=+16505557890" \
  --data-urlencode 'Parameters={"name":"Jane","appt":"Tue 3pm"}' \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"
# -> { "sid": "FN...", "status": "active", "context": {...} }

# Inspect the execution's variable context (debug where it branched)
curl "https://studio.twilio.com/v2/Flows/$FLOW_SID/Executions/$EXECUTION_SID/ExecutionContext" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"
```

```
# Inside a Send Message widget body, referencing injected + captured data:
Hi {{flow.data.name}}, reply YES to confirm your {{flow.data.appt}} appointment.

# A Split Based On widget testing the reply:
Variable to test: {{widgets.reply_1.inbound.Body}}
  matches "YES" (case-insensitive) -> confirm branch
  no match                         -> reprompt branch
```

## Pitfalls

- **Unwired transitions dead-end users.** Every Gather/Send & Wait widget has `timeout` and `no_match`/`no_input` events — wire them all or the flow silently strands the caller.
- **Forgetting to Publish.** Edits stay in draft until you Publish; "my change didn't take" is almost always an unpublished revision.
- **Widget variable scope confusion.** Widget outputs are namespaced (`{{widgets.<name>.<field>}}`); a value captured in one widget isn't a bare global. Use Set Variables or `{{flow.data}}` for cross-step state.
- **Synchronous HTTP Request timeouts.** The HTTP Request widget blocks the flow; slow endpoints stall the caller. Keep called services fast or offload to an async Run Function pattern.
- **Outbound trigger needs a connected From number.** `POST Executions` requires `From` to be a Twilio number attached to that Studio flow, and messaging still obeys A2P/opt-in rules.
- **Executions accumulate.** Long-lived or stuck executions stay `active`; monitor and end/expire them, and use ExecutionContext (not guesswork) to debug branch logic.

## Output format

```
STUDIO FLOW PLAN
  flow_name: <name>
  trigger: <Incoming Call | Incoming Message | REST API>
  widgets:
    - <widget type> : <purpose> -> transitions [event -> target]
  variables_used: <{{flow.data.*}}, {{widgets.*}}, {{trigger.*}}>
  external_calls: <HTTP Request / Run Function targets>
  publish_status: <draft | published rev N>
  rest_trigger: POST /v2/Flows/{FlowSid}/Executions (if outbound)
```

## Reference

- **Product:** Twilio Studio — visual, revision-based flow builder for voice and messaging. Host `studio.twilio.com`, API version v2.
- **Triggers:** three entry widgets — Incoming Message, Incoming Call, REST API.
- **Common widgets:** Send Message, Send & Wait For Reply, Gather Input on Call (DTMF + speech recognition), Say/Play, Split Based On (branching), Set Variables, Run Function (invoke a Twilio Function), HTTP Request (call external APIs), Connect Call To, Enqueue Call (hand to a TaskRouter TaskQueue), Make Outgoing Call.
- **Variables (Liquid templating):** `{{trigger.message.Body}}`, `{{trigger.call.From}}`, `{{widgets.<widgetName>.<output>}}` (e.g. `.Digits`, `.inbound.Body`), `{{flow.data}}` (Parameters injected at trigger), `{{flow.channel.address}}`.
- **Execution REST:** `POST /v2/Flows/{FlowSid}/Executions` (start; body `To`, `From`, `Parameters`), `GET .../Executions/{ExecutionSid}`, `GET .../Executions/{ExecutionSid}/ExecutionContext` (full variable state — the debug view), `GET .../Executions/{ExecutionSid}/Steps` (per-widget step log).
- **Publishing:** flows are draft until explicitly Published; each publish creates a revision you can roll back to.
- **Auth:** Account SID + Auth Token or API Key SID/Secret. **Webhook security:** validate the `X-Twilio-Signature` header (HMAC-SHA1 of the URL + sorted params, keyed by your Auth Token) on any Function/HTTP endpoint Studio calls, to confirm requests genuinely came from Twilio.
- **Compliance:** outbound messaging via Studio is subject to TCPA consent/opt-out (STOP/HELP), A2P 10DLC registration for US long codes, and WhatsApp template rules where applicable.
