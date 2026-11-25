---
name: twilio-voice-outbound-calls
version: 1.0.0
description: Place outbound programmable voice calls with the Twilio Calls API, controlling TwiML, answering-machine detection, status callbacks, recording, and timeouts.
author: matrixx0070
tags: [twilio, voice, calls, amd, callbacks]
capabilities: []
---

## When to use

Use this to originate outbound phone calls programmatically: notifications, reminders,
click-to-call, IVR outreach, and voice OTP delivery. You control what the callee hears via
TwiML (fetched from a URL or passed inline), detect humans vs answering machines, receive
lifecycle status callbacks, optionally record, and tune ring timeout and DTMF injection.

**Not for:** authoring the TwiML that runs once the call connects (see twilio-voice-twiml);
recording retrieval/storage/transcription detail (see twilio-call-recordings); inbound call
handling (configure the number's Voice webhook instead); SMS/RCS (see twilio-rcs-messaging).

## Method

1. Choose a call-control source. Decision point: dynamic per-call logic → set `Url` to a
   TwiML endpoint (Twilio GETs/POSTs it on answer); fixed static markup → pass `Twiml`
   inline; reusable app config → pass `ApplicationSid`.
2. Set `To` (E.164) and `From` (a Twilio number or verified caller ID on the account).
3. Decision point: is the callee likely a machine? Enable `MachineDetection=Enable` (fast,
   returns a hint) or `DetectMessageEnd` (waits for the greeting to finish before your TwiML
   runs — best for leaving voicemail). AMD result arrives as `AnsweredBy` on the answer
   callback (`human`, `machine_start`, `machine_end_beep`, `fax`, `unknown`).
4. Set `Timeout` (ring seconds, default 60) to cap how long Twilio waits for an answer.
5. Wire `StatusCallback` + `StatusCallbackEvent` to observe lifecycle:
   `initiated`, `ringing`, `answered`, `completed`.
6. Decision point: record the call? Set `Record=true` (or use `<Record>`/dual-channel via
   `RecordingChannels`); handle the RecordingStatusCallback — see twilio-call-recordings.
7. Send digits into an IVR after connect with `SendDigits` (e.g. `"wwww1928#"`; `w` = 0.5s).
8. Create the call: POST to the Calls resource; capture the Call SID (`CA...`).
9. Mid-call, modify or hang up by POSTing to the Call instance (`Status=completed` ends it;
   `Url` redirects live TwiML execution).

## Example

```python
from twilio.rest import Client

client = Client(account_sid, auth_token)

call = client.calls.create(
    to="+15551234567",
    from_="+15557654321",
    url="https://example.com/twiml/reminder",   # TwiML served on answer
    machine_detection="DetectMessageEnd",       # wait for greeting to end
    timeout=30,
    record=True,
    status_callback="https://example.com/voice/status",
    status_callback_event=["initiated", "ringing", "answered", "completed"],
    status_callback_method="POST",
)
print(call.sid, call.status)  # CAxxxx, queued
```

## Pitfalls

- `From` must be a Twilio number or a verified outbound caller ID, else the call is rejected.
- AMD adds latency before your TwiML executes (Twilio listens to classify); `DetectMessageEnd`
  can add several seconds. Do not enable it for time-sensitive human interactions.
- `AnsweredBy` can be `unknown`; design TwiML to be safe for both human and machine.
- `Timeout` is ring time, not call duration; there is no built-in max-duration param — guard
  long calls in your TwiML or with a status-callback teardown.
- Error 11200 means Twilio could not retrieve your TwiML URL (5xx/timeout/bad markup);
  13223/13214 indicate malformed/invalid numbers; 31003 is a downstream connection timeout.
- Inline `Twiml` and `Url`/`ApplicationSid` are mutually exclusive — pass exactly one source.
- StatusCallback fires per event only if listed in `StatusCallbackEvent`; `ringing` and
  `initiated` are not sent by default.

## Output format

A Call resource with `sid` (`CA...`) and initial `status` (`queued`/`initiated`). Status
callbacks POST call progress (`CallStatus`, `AnsweredBy`, `CallDuration`, `Timestamp`) to
your URL through completion. Recordings, if enabled, arrive via RecordingStatusCallback.

## Reference

- Create: `POST https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Calls.json`.
- Key params: `To`, `From`, `Url` (TwiML URL) or `Twiml` (inline) or `ApplicationSid`,
  `StatusCallback`, `StatusCallbackEvent` (`initiated`|`ringing`|`answered`|`completed`),
  `StatusCallbackMethod`, `Record`, `RecordingChannels` (`mono`|`dual`),
  `RecordingStatusCallback`, `Timeout` (default 60s), `MachineDetection`
  (`Enable`|`DetectMessageEnd`), `MachineDetectionTimeout`, `SendDigits`.
- Modify/end: `POST .../Calls/{CallSid}.json` with `Status=completed` or `Url` to redirect.
- Call status values: `queued`, `initiated`, `ringing`, `in-progress`, `completed`, `busy`,
  `no-answer`, `canceled`, `failed`.
- `AnsweredBy`: `human`, `machine_start`, `machine_end_beep`, `machine_end_silence`,
  `machine_end_other`, `fax`, `unknown`.
- Error codes: 13214 invalid Dial number, 11200 HTTP retrieval failure, 31003 connection
  timeout, 13223 invalid phone number format.
- Pricing: per-minute outbound billed in 1-minute increments by destination; AMD carries a
  small per-call add-on; recording and storage bill separately. Confirm rates in Console.
