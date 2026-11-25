---
name: twilio-conference-calls
version: 1.0.0
description: Build and control multi-party Twilio conference calls with TwiML and the Participants REST API, including mute, hold, coaching, wait music, and status callbacks.
author: matrixx0070
tags: [twilio, conference, voice, participants, rest]
capabilities: []
---

## When to use

Use this when you need to bridge three or more parties into a single named room, or when you need programmatic control over who is muted, on hold, coaching, or dialed in mid-call. Twilio conferences are created by placing callers into `<Dial><Conference>` with a shared room name; you then add, remove, and modify participants through the REST API.

**Not for:** simple two-party call bridging (use `<Dial><Number>` directly); AI voice agents (see twilio-voice-conversation-relay); or recording detail — conference recording is covered here at a high level but PCI pause, dual-channel, and media retrieval live in twilio-call-recordings.

## Method

1. Return TwiML that drops the caller into a named room: `<Dial><Conference>ROOM</Conference></Dial>`. Everyone who joins the same name on the same account lands in the same conference.
2. Decision point — lifecycle: set `startConferenceOnEnter` on the moderator so the room does not begin until they arrive, and `endConferenceOnExit` on the moderator so it tears down when they leave. Regular participants get `startConferenceOnEnter="false"`.
3. Set wait behavior with `waitUrl` (TwiML/MP3 hold music) and `beep` for join/leave tones.
4. To add a participant programmatically, POST to the Participants resource with `From` and `To`; Twilio dials them and joins them on answer.
5. To mute, hold, or coach an existing participant, POST an update to that participant's resource (`Muted`, `Hold`, `Coaching`, `CallSidToCoach`).
6. Decision point — coaching: a coach hears the conference and can whisper to one target (`CallSidToCoach`) without the rest of the room hearing.
7. Remove a participant by DELETE on their resource, or end the whole room by updating the Conference `Status` to `completed`.
8. Wire `statusCallback` (conference-level) and per-participant callbacks to track `participant-join`, `participant-leave`, `start`, `end`, `mute`, `hold`.
9. To record, set `record="record-from-start"` on the `<Conference>` — then hand off to twilio-call-recordings for media retrieval and compliance.

## Example

TwiML for the moderator:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Dial>
    <Conference startConferenceOnEnter="true"
                endConferenceOnExit="true"
                beep="true"
                waitUrl="https://example.com/hold.mp3"
                record="record-from-start"
                statusCallback="https://example.com/conf-events"
                statusCallbackEvent="start end join leave mute hold">
      standup-room
    </Conference>
  </Dial>
</Response>
```

Dial a new participant into that room and mute another (Python):

```python
from twilio.rest import Client
client = Client(account_sid, auth_token)

# Add a participant by phone number
client.conferences("standup-room").participants.create(
    from_="+15551112222", to="+15553334444", beep="onEnter")

# Mute an existing participant
client.conferences("standup-room") \
      .participants("CA_call_sid_here").update(muted=True)

# Put someone on hold with hold music
client.conferences("standup-room") \
      .participants("CA_call_sid_here").update(hold=True, hold_url="https://example.com/hold.mp3")
```

## Pitfalls

- If no one has `startConferenceOnEnter="true"`, everyone waits on hold music forever.
- `endConferenceOnExit` on the wrong participant tears down the room when a normal caller hangs up. Reserve it for the moderator.
- The Participants API is keyed by the participant's Call SID, not the phone number; capture the SID from the join callback.
- Conference names are scoped per account and case-sensitive; a typo silently creates a second, empty room.
- Default `maxParticipants` is 250; conferences do not auto-scale beyond it and creation fails once full.
- `waitUrl` TwiML may only contain `<Play>`, `<Say>`, and `<Redirect>` — other verbs are ignored.

## Output format

TwiML places callers in the room. REST calls return JSON participant/conference resources (SIDs prefixed `CF` for conferences, `CA` for the participant call). Status callbacks POST form-encoded events (`StatusCallbackEvent`, `ConferenceSid`, `CallSid`, `Muted`, `Hold`) to your URL.

## Reference

- TwiML: `<Dial><Conference>`. Attributes: `startConferenceOnEnter`, `endConferenceOnExit`, `muted`, `beep` (`true`/`false`/`onEnter`/`onExit`), `waitUrl`, `waitMethod`, `maxParticipants` (default 250), `record` (`do-not-record` | `record-from-start`), `recordingStatusCallback`, `statusCallback`, `statusCallbackEvent` (`start end join leave mute hold speaker`), `coach`, `region`, `trim`.
- REST base: `https://api.twilio.com/2010-04-01/Accounts/{AccountSid}`.
  - Add participant: `POST /Conferences/{ConferenceSid}/Participants.json` (params `From`, `To`, `Muted`, `Beep`, `EarlyMedia`, `Coaching`, `CallSidToCoach`).
  - Update participant: `POST /Conferences/{ConferenceSid}/Participants/{CallSid}.json` (`Muted`, `Hold`, `HoldUrl`, `Coaching`, `AnnounceUrl`).
  - Remove: `DELETE /Conferences/{ConferenceSid}/Participants/{CallSid}.json`.
  - List/inspect: `GET /Conferences.json` (filter by `FriendlyName`, `Status`, `DateCreated`); end a room via `POST /Conferences/{ConferenceSid}.json` with `Status=completed`.
- Common errors: 21470 (invalid `waitUrl`), 21472 (conference not found for participant op), 21226/21211 (invalid `To`/`From`). Conference recording media is fetched via the Recordings resource — see twilio-call-recordings.
