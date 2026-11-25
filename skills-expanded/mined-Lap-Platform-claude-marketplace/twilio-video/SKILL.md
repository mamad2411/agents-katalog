---
name: twilio-video
description: "Twilio - Video API skill. Use when working with Twilio - Video for Compositions, CompositionHooks, CompositionSettings. Covers 39 endpoints."
version: 1.0.0
generator: lapsh
---

# Twilio - Video
API version: 1.0.0

## Auth
Bearer basic

## Base URL
https://video.twilio.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v1/Compositions -- verify access
3. POST /v1/Compositions -- create first Compositions

## Endpoints

39 endpoints across 6 groups. See references/api-spec.lap for full details.

### Compositions
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/Compositions/{Sid} | Returns a single Composition resource identified by a Composition SID. |
| DELETE | /v1/Compositions/{Sid} | Delete a Recording Composition resource identified by a Composition SID. |
| GET | /v1/Compositions | List of all Recording compositions. |
| POST | /v1/Compositions |  |

### CompositionHooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/CompositionHooks/{Sid} | Returns a single CompositionHook resource identified by a CompositionHook SID. |
| DELETE | /v1/CompositionHooks/{Sid} | Delete a Recording CompositionHook resource identified by a `CompositionHook SID`. |
| POST | /v1/CompositionHooks/{Sid} |  |
| GET | /v1/CompositionHooks | List of all Recording CompositionHook resources. |
| POST | /v1/CompositionHooks |  |

### CompositionSettings
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/CompositionSettings/Default |  |
| POST | /v1/CompositionSettings/Default |  |

### Recordings
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/Recordings/{Sid} | Returns a single Recording resource identified by a Recording SID. |
| DELETE | /v1/Recordings/{Sid} | Delete a Recording resource identified by a Recording SID. |
| GET | /v1/Recordings | List of all Track recordings. |

### RecordingSettings
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/RecordingSettings/Default |  |
| POST | /v1/RecordingSettings/Default |  |

### Rooms
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/Rooms/{Sid} |  |
| POST | /v1/Rooms/{Sid} |  |
| POST | /v1/Rooms |  |
| GET | /v1/Rooms |  |
| GET | /v1/Rooms/{RoomSid}/Participants/{Sid} |  |
| POST | /v1/Rooms/{RoomSid}/Participants/{Sid} |  |
| GET | /v1/Rooms/{RoomSid}/Participants |  |
| POST | /v1/Rooms/{RoomSid}/Participants/{Sid}/Anonymize |  |
| GET | /v1/Rooms/{RoomSid}/Participants/{ParticipantSid}/PublishedTracks/{Sid} | Returns a single Track resource represented by TrackName or SID. |
| GET | /v1/Rooms/{RoomSid}/Participants/{ParticipantSid}/PublishedTracks | Returns a list of tracks associated with a given Participant. Only `currently` Published Tracks are in the list resource. |
| GET | /v1/Rooms/{RoomSid}/Participants/{ParticipantSid}/SubscribeRules | Returns a list of Subscribe Rules for the Participant. |
| POST | /v1/Rooms/{RoomSid}/Participants/{ParticipantSid}/SubscribeRules | Update the Subscribe Rules for the Participant |
| GET | /v1/Rooms/{RoomSid}/Participants/{ParticipantSid}/SubscribedTracks/{Sid} | Returns a single Track resource represented by `track_sid`.  Note: This is one resource with the Video API that requires a SID, be Track Name on the subscriber side is not guaranteed to be unique. |
| GET | /v1/Rooms/{RoomSid}/Participants/{ParticipantSid}/SubscribedTracks | Returns a list of tracks that are subscribed for the participant. |
| GET | /v1/Rooms/{RoomSid}/Recordings/{Sid} |  |
| DELETE | /v1/Rooms/{RoomSid}/Recordings/{Sid} |  |
| GET | /v1/Rooms/{RoomSid}/Recordings |  |
| GET | /v1/Rooms/{RoomSid}/RecordingRules | Returns a list of Recording Rules for the Room. |
| POST | /v1/Rooms/{RoomSid}/RecordingRules | Update the Recording Rules for the Room |
| GET | /v1/Rooms/{RoomSid}/Transcriptions/{Ttid} |  |
| POST | /v1/Rooms/{RoomSid}/Transcriptions/{Ttid} |  |
| GET | /v1/Rooms/{RoomSid}/Transcriptions |  |
| POST | /v1/Rooms/{RoomSid}/Transcriptions |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get Composition details?" -> GET /v1/Compositions/{Sid}
- "Delete a Composition?" -> DELETE /v1/Compositions/{Sid}
- "List all Compositions?" -> GET /v1/Compositions
- "Create a Composition?" -> POST /v1/Compositions
- "Get CompositionHook details?" -> GET /v1/CompositionHooks/{Sid}
- "Delete a CompositionHook?" -> DELETE /v1/CompositionHooks/{Sid}
- "List all CompositionHooks?" -> GET /v1/CompositionHooks
- "Create a CompositionHook?" -> POST /v1/CompositionHooks
- "List all Default?" -> GET /v1/CompositionSettings/Default
- "Create a Default?" -> POST /v1/CompositionSettings/Default
- "Get Recording details?" -> GET /v1/Recordings/{Sid}
- "Delete a Recording?" -> DELETE /v1/Recordings/{Sid}
- "List all Recordings?" -> GET /v1/Recordings
- "List all Default?" -> GET /v1/RecordingSettings/Default
- "Create a Default?" -> POST /v1/RecordingSettings/Default
- "Get Room details?" -> GET /v1/Rooms/{Sid}
- "Create a Room?" -> POST /v1/Rooms
- "List all Rooms?" -> GET /v1/Rooms
- "Get Participant details?" -> GET /v1/Rooms/{RoomSid}/Participants/{Sid}
- "List all Participants?" -> GET /v1/Rooms/{RoomSid}/Participants
- "Create a Anonymize?" -> POST /v1/Rooms/{RoomSid}/Participants/{Sid}/Anonymize
- "Get PublishedTrack details?" -> GET /v1/Rooms/{RoomSid}/Participants/{ParticipantSid}/PublishedTracks/{Sid}
- "List all PublishedTracks?" -> GET /v1/Rooms/{RoomSid}/Participants/{ParticipantSid}/PublishedTracks
- "List all SubscribeRules?" -> GET /v1/Rooms/{RoomSid}/Participants/{ParticipantSid}/SubscribeRules
- "Create a SubscribeRule?" -> POST /v1/Rooms/{RoomSid}/Participants/{ParticipantSid}/SubscribeRules
- "Get SubscribedTrack details?" -> GET /v1/Rooms/{RoomSid}/Participants/{ParticipantSid}/SubscribedTracks/{Sid}
- "List all SubscribedTracks?" -> GET /v1/Rooms/{RoomSid}/Participants/{ParticipantSid}/SubscribedTracks
- "Get Recording details?" -> GET /v1/Rooms/{RoomSid}/Recordings/{Sid}
- "Delete a Recording?" -> DELETE /v1/Rooms/{RoomSid}/Recordings/{Sid}
- "List all Recordings?" -> GET /v1/Rooms/{RoomSid}/Recordings
- "List all RecordingRules?" -> GET /v1/Rooms/{RoomSid}/RecordingRules
- "Create a RecordingRule?" -> POST /v1/Rooms/{RoomSid}/RecordingRules
- "Get Transcription details?" -> GET /v1/Rooms/{RoomSid}/Transcriptions/{Ttid}
- "List all Transcriptions?" -> GET /v1/Rooms/{RoomSid}/Transcriptions
- "Create a Transcription?" -> POST /v1/Rooms/{RoomSid}/Transcriptions
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
