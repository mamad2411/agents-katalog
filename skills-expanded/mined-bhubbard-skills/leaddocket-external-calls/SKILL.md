---
name: leaddocket-external-calls
description: >
  Integrate third-party VoIP and call tracking providers with LeadDocket using
  the External Calls API. Covers registering call start and end events (with
  provider-agnostic JSON payloads including UTM/marketing attribution),
  fetching call details by ID, retrieving call recordings, and retrieving
  transcriptions. Use for CallRail, Twilio, or any custom VoIP webhook
  integration. The /start endpoint requires no authentication; /end and GET
  endpoints require an API key. For built-in LeadDocket call configuration
  see leaddocket-calls-config.
---

# LeadDocket — External Calls (VoIP Integration)

Base URL: `https://{instance}.leaddocket.com`.

The External Calls API accepts call events from any VoIP provider. When calls
are received, LeadDocket will automatically associate them with existing leads
and opportunities based on caller phone number and capture marketing attribution.

## Reference
Support article: [External Call Provider Integration: Developer Quick Start](https://support.leaddocket.com/hc/en-us/articles/46274439786523)

---

## Register call start

No API key required — designed for webhook delivery from VoIP providers.

```http
POST /api/externalcalls/start
Content-Type: application/json
```

### Structured format (recommended)

```json
{
  "ProviderName": "MyVoIPProvider",
  "Common": {
    "ProviderId": "call-uuid-12345",
    "CallerNumber": "+15551234567",
    "CalleeNumber": "+15559876543",
    "Direction": "Inbound",
    "CallStatus": "ringing",
    "StartCallDTM": "2026-07-01T14:30:00Z",
    "CallerName": "Jane Smith",
    "CallerCity": "Austin",
    "CallerState": "TX",
    "CallerCountry": "US",
    "ReferrerUrl": "https://lawfirm.com/contact"
  },
  "Metadata": {
    "utm_source": "google",
    "utm_medium": "cpc",
    "utm_campaign": "injury-2026"
  }
}
```

### Flat format (simpler integrations)

```json
{
  "ProviderId": "call-uuid-12345",
  "CallerNumber": "+15551234567",
  "CalleeNumber": "+15559876543",
  "Direction": "Inbound",
  "utm_source": "google"
}
```

Returns `CallEventResponse`:
```json
{ "success": true, "timestamp": "2026-07-01T14:30:00Z", "id": 9876 }
```

---

## Register call end

```http
POST /api/externalcalls/end
Content-Type: application/json

{
  "ProviderName": "MyVoIPProvider",
  "Common": {
    "ProviderId": "call-uuid-12345",
    "CallStatus": "completed",
    "EndCallDTM": "2026-07-01T14:35:00Z",
    "DurationSeconds": 312,
    "RecordingUrl": "https://provider.com/recordings/12345.mp3"
  },
  "Metadata": {
    "transcription_text": "Agent: Thank you for calling...",
    "qualified": "true"
  }
}
```

The `ProviderId` links this to the start event. Returns `CallEventResponse`.

---

## Common payload fields

| Field | Required | Notes |
|-------|----------|-------|
| `ProviderId` | **Yes** | Unique call ID from VoIP provider. Used for deduplication. Alias: `CallSID` |
| `CallerNumber` | Yes (start) | Auto-normalized. Alias: `CallFrom` |
| `CalleeNumber` | No | Tracking number called. Alias: `CallTo` |
| `Direction` | No | `Inbound`, `Outbound`, `Unknown` (or `0`, `1`, `-1`) |
| `CallStatus` | No | `completed`, `busy`, `no-answer`, `failed` |
| `StartCallDTM` | No | ISO 8601. Alias: `CreatedDate` |
| `EndCallDTM` | No | ISO 8601 |
| `DurationSeconds` | No | Integer. Alias: `Duration` |
| `RecordingUrl` | No | Must be publicly accessible |
| `ReferrerUrl` | No | Landing page URL. Alias: `ReferringUrl` |

### Marketing metadata fields (in `Metadata` or root for flat format)

| Field | Description |
|-------|-------------|
| `utm_source` | Traffic source (google, facebook) |
| `utm_medium` | Medium (cpc, organic, email) |
| `utm_campaign` | Campaign name |
| `utm_term` | Keyword |
| `utm_content` | Ad content ID |
| `gclid` | Google Click ID |
| `fbclid` | Facebook Click ID |
| `msclkid` | Microsoft Click ID |
| `transcription_text` | Full call transcription |
| `summary` | Call summary |

Any unknown fields are stored as custom fields on the call record.

---

## Get call details by ID

Requires API key.

```http
GET /api/externalcalls/{id}
```

Returns `ExternalPhoneCall` object (use the `id` returned from start/end event response).

---

## Get call recording

```http
GET /api/externalcalls/{id}/recording
```

Returns `audio/mp3` binary stream.

---

## Get call transcription

```http
GET /api/externalcalls/{id}/transcription
```

Returns `text/plain` transcription file.

---

## Best Practices

- **Always use consistent ProviderId**: Use the VoIP provider's own call UUID. Never generate a new ID per request — the same ID is used to update/upsert the record across start and end.
- **Send start immediately, end when complete**: Real-time association happens at start. Marketing data in start events is captured even if the end event fails.
- **Include UTM data at start**: Attribution data propagates to the associated lead — capture it early.
- **Recording URLs must be public**: LeadDocket fetches the recording from the URL to import it into blob storage.
- **Handle 429**: Retry with exponential backoff. Start calls during high-volume campaigns can burst.
- **Node.js transform example**:

```js
function toLeadDocketPayload(providerWebhook) {
  return {
    ProviderName: "MyProvider",
    Common: {
      ProviderId: providerWebhook.call_id,
      CallerNumber: providerWebhook.from,
      CalleeNumber: providerWebhook.to,
      Direction: "Inbound",
      StartCallDTM: new Date(providerWebhook.started_at).toISOString(),
      RecordingUrl: providerWebhook.recording_url
    },
    Metadata: {
      utm_source: providerWebhook.tracking?.source,
      utm_campaign: providerWebhook.tracking?.campaign
    }
  };
}
```
