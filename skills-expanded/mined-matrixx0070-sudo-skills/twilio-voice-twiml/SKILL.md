---
name: twilio-voice-twiml
version: 1.0.0
description: Author TwiML to control live voice calls — speak, play audio, gather DTMF and speech, dial destinations, record, and redirect flow with action callbacks.
author: matrixx0070
tags: [twilio, voice, twiml, ivr, dtmf]
capabilities: []
---

## When to use

Use this to write the XML instructions Twilio executes while a call is connected: greet the
caller with text-to-speech or audio, build IVR menus that gather DTMF or speech, connect the
caller to numbers/clients/SIP endpoints, record audio, enqueue callers, and branch flow with
action/redirect callbacks. TwiML is what the Calls API `Url`/`Twiml` points at, and what an
inbound number's Voice webhook returns.

**Not for:** originating the call itself (see twilio-voice-outbound-calls); real-time media
streaming to an AI voice agent via `<Connect><ConversationRelay>` (see
twilio-voice-conversation-relay); multi-party conferencing beyond a simple `<Dial><Conference>`
(see twilio-conference-calls); recording lifecycle/retrieval (see twilio-call-recordings).

## Method

1. Return a valid TwiML document: `Content-Type: text/xml`, root `<Response>`.
2. Decision point: speak or play? Use `<Say>` (choose `voice`, e.g. `Polly.Joanna`, and
   `language`) for dynamic text; `<Play>` for a hosted audio URL.
3. Collect input with `<Gather>`. Decision point: `input="dtmf"` for keypad, `input="speech"`
   for ASR, or `input="dtmf speech"` for either. Set `numDigits`/`finishOnKey` for DTMF,
   `hints` and `speechTimeout` for speech, and `action` for where results POST (as `Digits`
   or `SpeechResult`). Nest `<Say>`/`<Play>` inside `<Gather>` so prompts are barge-in-able.
4. If `<Gather>` times out with no input, execution continues to verbs after it — put a
   fallback `<Say>`/`<Redirect>` there.
5. Connect calls with `<Dial>`. Decision point on the noun: `<Number>` (PSTN), `<Client>`
   (SDK), `<Sip>` (SIP URI), `<Conference>` (room), or `<Queue>` (bridge to enqueued caller).
   Use `<Dial action=...>` to run TwiML after the dialed leg ends (`DialCallStatus`).
6. Record with `<Record>` (set `maxLength`, `playBeep`, `transcribe`, `recordingStatusCallback`).
7. Route flow with `<Redirect>` (hand off to another TwiML URL), `<Pause length>`,
   `<Hangup>`, `<Reject reason>`, or `<Enqueue>` for call-queue hold.
8. For advanced media: `<Connect>` wraps `<Stream>`, `<ConversationRelay>`, or `<VirtualAgent>`.
9. Validate the XML; malformed markup surfaces as error 11200 to the caller.

## Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Gather input="dtmf speech" numDigits="1" action="/voice/route" method="POST"
          speechTimeout="auto" hints="sales, support, billing">
    <Say voice="Polly.Joanna" language="en-US">
      Thanks for calling. Press 1 or say sales. Press 2 or say support.
    </Say>
  </Gather>
  <!-- Reached only if Gather times out with no input -->
  <Say voice="Polly.Joanna">Sorry, I did not catch that. Goodbye.</Say>
  <Hangup/>
</Response>
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Dial timeout="20" record="record-from-answer" action="/voice/after-dial">
    <Number>+15551234567</Number>
  </Dial>
  <Say voice="Polly.Joanna">The party did not answer.</Say>
</Response>
```

## Pitfalls

- `<Gather action>` receives `Digits` for DTMF and `SpeechResult` (+ `Confidence`) for
  speech; if no `action` is set, Twilio re-requests the same TwiML with results appended —
  usually not what you want. Always set `action` for menus.
- Verbs after a completed `<Gather>` with input are NOT executed; the `action` URL takes over.
  Verbs after a timed-out `<Gather>` ARE executed — that is your no-input path.
- `<Dial>` with a bad destination number raises error 13214; unreachable action URLs raise
  11200; malformed E.164 raises 13223.
- `<Play>` audio must be a reachable URL in a supported format (WAV/MP3); Twilio fetches it
  live, so latency/5xx breaks the call.
- Speech `hints` bias recognition but do not constrain it; keep menus short and confirm.
- `<Record>` blocks until `maxLength`, silence, or `finishOnKey`; without `maxLength` it can
  run long. Recordings are async — poll or use `recordingStatusCallback`.
- Order matters: `<Response>` executes top-to-bottom; a `<Hangup>`/`<Redirect>` ends the doc.

## Output format

An XML `<Response>` document (served as `text/xml`) that Twilio executes verb by verb.
`<Gather>`/`<Dial>`/`<Record>` action callbacks POST result parameters (`Digits`,
`SpeechResult`, `DialCallStatus`, `RecordingUrl`) to the URLs you specify for the next step.

## Reference

- Root: `<Response>`. Verbs: `<Say>` (`voice`, `language`, `loop`), `<Play>` (`loop`,
  `digits`), `<Gather>` (`input`, `numDigits`, `finishOnKey`, `timeout`, `speechTimeout`,
  `hints`, `action`, `method`, `actionOnEmptyResult`), `<Dial>` (`timeout` default 30,
  `record`, `action`, `callerId`, `answerOnBridge`), `<Record>` (`maxLength`, `playBeep`,
  `finishOnKey`, `transcribe`, `recordingStatusCallback`), `<Hangup>`, `<Reject>` (`reason`
  `rejected`|`busy`), `<Redirect>` (`method`), `<Pause>` (`length`), `<Enqueue>`,
  `<Connect>`.
- `<Dial>` nouns: `<Number>`, `<Client>`, `<Sip>`, `<Conference>`, `<Queue>`.
- `<Connect>` nouns: `<Stream>` (Media Streams WebSocket), `<ConversationRelay>` (AI voice),
  `<VirtualAgent>` (Dialogflow).
- `<Gather>` callback params: `Digits` (DTMF), `SpeechResult` + `Confidence` (speech).
- `<Dial>` callback param: `DialCallStatus` (`completed`|`busy`|`no-answer`|`failed`|`canceled`).
- `<Say>` supports Amazon Polly voices (e.g. `Polly.Joanna`, `Polly.Matthew`) and standard
  voices with `language` locale codes; SSML tags are supported inside `<Say>`.
- Error codes: 13214 invalid Dial number, 11200 document retrieval failure, 31003 connection
  timeout, 13223 invalid phone number format.
- TwiML execution itself is free; billed time is call duration, plus recording/transcription
  and any dialed-leg minutes at standard voice rates.
