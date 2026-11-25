---
name: leaddocket-calls-config
description: >
  Configure the call management system in LeadDocket — setting up call
  tracking numbers, call routing, call recording, AI call scoring, and VoIP
  provider connections. Use when setting up or modifying the phone system
  integration in LeadDocket. For registering VoIP call events via API see
  leaddocket-external-calls.
---

# LeadDocket — Calls Configuration

LeadDocket includes call tracking and management capabilities with native VoIP support and third-party provider integrations.

> Support section: [Calls](https://support.leaddocket.com/hc/en-us/sections/360009496631-Calls)

---

## Call Tracking Numbers

LeadDocket can provision call tracking numbers that route to your firm's main line. Each tracking number captures marketing attribution for calls.

### Setup (Admin, in the LeadDocket UI)

1. Navigate to **Settings → Calls → Tracking Numbers**
2. Click **Add Tracking Number**
3. Select area code and number
4. Configure the forwarding destination (your firm's main line)
5. Assign a name/label for the number (e.g., "Google Ads - PI", "Billboard - DUI")
6. Save

### How attribution works

When a caller dials a tracking number:
1. LeadDocket captures the caller's number
2. Looks up existing leads/opportunities by phone
3. Creates a new opportunity if no match found
4. Records the call with the tracking number's source attribution

---

## Call Routing Configuration

### Business Hours Routing

1. Navigate to **Settings → Calls → Routing**
2. Configure business hours per day/time
3. Set after-hours behavior:
   - Forward to voicemail
   - Forward to answering service
   - Forward to on-call number

### Hunt Groups / Simultaneous Ring

Configure multiple staff numbers to ring simultaneously or in sequence when a tracking number is dialed.

---

## Call Recording

1. Navigate to **Settings → Calls → Recording**
2. Enable call recording (auto-records all inbound calls)
3. Configure the legal disclosure message played before recording begins:
   - "This call may be recorded for quality assurance purposes"
4. Recordings are stored on the call record and visible in the lead

---

## AI Call Scoring (LeadsAI)

LeadDocket uses AI to analyze call recordings:

| Feature | Description |
|---------|-------------|
| **Qualification Score** | Whether the call meets intake criteria |
| **Call Summary** | AI-generated summary of the call |
| **Transcription** | Full text transcript of the call |
| **Sentiment Analysis** | Caller sentiment during the call |

Configure AI processing in **Settings → Calls → AI Settings**.

Access via API:
```http
GET /api/externalcalls/{id}/transcription
GET /api/externalcalls/{id}/recording
```

---

## Third-Party VoIP Integration

For firms using CallRail, Twilio, or other VoIP providers:

1. Navigate to **Settings → Integrations → VoIP Provider**
2. Select your provider or use **Custom (Webhook)**
3. Configure the webhook URL your provider should send events to:
   `https://{instance}.leaddocket.com/api/externalcalls/start`
   `https://{instance}.leaddocket.com/api/externalcalls/end`
4. See `leaddocket-external-calls` for the full payload format

---

## Best Practices

- **Use separate tracking numbers per campaign**: One number per Google Ads campaign, billboard, TV spot, etc. for accurate attribution.
- **Record the compliance disclosure**: Always play a recording disclosure — requirements vary by state (one-party vs. two-party consent).
- **Review AI summaries in the UI**: Use the call review queue in **Calls → All Calls** to audit AI-scored calls regularly.
- **Don't mix tracking and direct lines**: Keep tracking numbers for marketing channels; give staff direct extensions separately.
