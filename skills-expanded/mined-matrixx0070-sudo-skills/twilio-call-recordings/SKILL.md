---
name: twilio-call-recordings
version: 1.0.0
description: Record Twilio calls via the <Record> verb, <Dial record>, or the Recordings REST API, with dual-channel capture, transcription, PCI pause/resume, and compliant retrieval.
author: matrixx0070
tags: [twilio, recording, voice, transcription, compliance]
capabilities: []
---

## When to use

Use this when you need to capture call audio — voicemail, agent QA, dual-channel legal records, or compliance archives. Twilio offers three paths: the `<Record>` verb (caller records a message), `<Dial record="...">` (records a bridged two-party call), and the Recordings REST API (start/stop recording on a live call). Pick by what you are recording and when you decide to record.

**Not for:** deciding whether a jurisdiction requires two-party consent (that is your legal call, not a Twilio setting); real-time transcription for an AI agent (use twilio-voice-conversation-relay's transcription); or conference room orchestration (see twilio-conference-calls, which sets `record` on the `<Conference>` and then retrieves media here).

## Method

1. Decision point — which mechanism:
   - Recording a single caller leaving a message → `<Record>` verb.
   - Recording a two-leg bridged conversation → `<Dial record="record-from-answer-dual">`.
   - Starting/stopping recording mid-call from your server → Recordings REST API on the live Call.
2. For `<Record>`: set `action` (where TwiML flow continues), `maxLength`, `playBeep`, `finishOnKey`, and `recordingStatusCallback`. Set `transcribe="true"` for async transcription.
3. Decision point — channels: single-channel mono is the default. Use `RecordingChannels=dual` (or a `*-dual` `record` value) to keep each party on a separate channel — required for reliable speaker separation and diarization.
4. Wire `recordingStatusCallback` with `recordingStatusCallbackEvent` (`in-progress`, `completed`, `absent`) so you learn the RecordingSid and media URL when it is ready.
5. For PCI / sensitive spans, pause recording before capturing card data and resume after: update the recording with `Status=paused` and `PauseBehavior` (`skip` drops the paused audio, `silence` inserts silence), then `Status=in-progress` to resume.
6. Retrieve media from the Recordings resource; append `.mp3` or `.wav` to the recording URL. Store or forward as needed.
7. Apply retention: set account/subaccount retention or delete recordings via the API after your compliance window. Consider encryption-at-rest (Voice Recording Encryption with your public key) for regulated data.

## Example

TwiML voicemail capture with transcription:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say>Please leave a message after the beep.</Say>
  <Record maxLength="120"
          playBeep="true"
          transcribe="true"
          finishOnKey="#"
          recordingStatusCallback="https://example.com/rec-done"
          action="https://example.com/after-record" />
</Response>
```

Dual-channel recording of a bridged call:

```xml
<Response>
  <Dial record="record-from-answer-dual"
        recordingStatusCallback="https://example.com/rec-done">
    +15553334444
  </Dial>
</Response>
```

Start recording a live call and later pause for PCI (Python):

```python
rec = client.calls("CA_live_call_sid").recordings.create(
    recording_channels="dual",
    recording_status_callback="https://example.com/rec-done")

# Pause while collecting card number, dropping that audio entirely
client.calls("CA_live_call_sid").recordings(rec.sid).update(
    status="paused", pause_behavior="skip")

# Resume
client.calls("CA_live_call_sid").recordings(rec.sid).update(status="in-progress")
```

## Pitfalls

- Recordings are single-channel mono unless you explicitly request dual — retrofitting speaker separation on a mono file is unreliable.
- `<Record>` records only one leg (the caller). To capture both sides of a conversation use `<Dial record>` or the Calls Recordings resource.
- Built-in `transcribe="true"` on `<Record>` is async, best-effort, and English-focused; it is not the same as real-time transcription.
- `PauseBehavior=silence` keeps timeline alignment but leaves an audible gap; `skip` shortens the file — choose deliberately for legal timing.
- Recording status callbacks can fire `absent` when nothing was captured (e.g., immediate hangup) — handle that case.
- Media URLs require authenticated access (or a signed/expiring URL); do not treat them as public links.

## Output format

REST returns JSON Recording resources: `sid` (prefix `RE`), `call_sid`, `duration`, `channels`, `status`, `source`, `media_url`. Media is fetched by appending `.mp3` (compressed) or `.wav` (PCM) to the recording URI. Transcriptions arrive as separate Transcription resources (`TR` prefix) via callback.

## Reference

- TwiML `<Record>`: `action`, `method`, `timeout`, `finishOnKey`, `maxLength`, `playBeep`, `trim` (`trim-silence`/`do-not-trim`), `recordingStatusCallback`, `recordingStatusCallbackEvent`, `transcribe`, `transcribeCallback`.
- TwiML `<Dial record>` values: `do-not-record`, `record-from-answer`, `record-from-ringing`, `record-from-answer-dual`, `record-from-ringing-dual`.
- REST base `https://api.twilio.com/2010-04-01/Accounts/{AccountSid}`:
  - Start on live call: `POST /Calls/{CallSid}/Recordings.json` (`RecordingChannels=mono|dual`, `RecordingStatusCallback`, `RecordingStatusCallbackEvent`, `Trim`).
  - Update (pause/resume/stop): `POST /Calls/{CallSid}/Recordings/{RecordingSid}.json` (`Status=paused|in-progress|stopped`, `PauseBehavior=skip|silence`).
  - Fetch/list/delete: `GET|DELETE /Recordings/{RecordingSid}.json`; media at `/Recordings/{RecordingSid}.mp3` or `.wav`.
- Status callback events: `in-progress`, `completed`, `absent`. Recording SIDs start `RE`, transcriptions `TR`.
- Compliance: default storage is Twilio-hosted; enable Voice Recording Encryption (customer public key) for at-rest encryption, configure retention/auto-delete, and remember consent is a legal obligation Twilio does not enforce. For conference recordings, set `record="record-from-start"` on `<Conference>` (see twilio-conference-calls) and retrieve via the same Recordings resource.
