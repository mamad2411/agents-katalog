---
name: twilio-conversation-intelligence
version: 1.0.0
description: Run Twilio Conversational Intelligence — create a Service, attach Language Operators, transcribe recordings, and retrieve summary, sentiment, entity, and PII-redaction results.
author: matrixx0070
tags: [twilio, intelligence, transcripts, operators, analytics]
capabilities: []
---

You extract structured insight from conversations after (or near) the fact: transcribe a recording, run Language Operators over it, and read back summaries, sentiment, entities, and redacted PII. This is the analytics layer, distinct from live conversation control.

## When to use

Use this when you have call recordings or transcripts and need machine analysis: a call summary, sentiment score, entities/slots extracted, PII redacted for storage/compliance, or a custom operator (e.g. did the agent read the disclosure). Powers QA, ACW automation, compliance, and reporting.

Decision gate: prebuilt operator covers the need (summary/sentiment/entity/PII)? Attach it. Domain-specific extraction/classification? Author a custom operator on the Service. Need results live mid-turn? This is asynchronous — use a real-time path instead (see the augmentation architect for the split).

**Not for:** live turn routing or replying (see twilio-conversation-orchestrator); attaching an assistant to a channel (see twilio-agent-connect); designing the overall assist system (see twilio-agent-augmentation-architect).

## Method

1. Create an Intelligence Service. `POST https://intelligence.twilio.com/v2/Services` with a `UniqueName`. This container holds your operator configuration and default settings (language, redaction defaults). You get a Service SID (`GA...`).
2. Attach Language Operators to the Service. Choose from prebuilt operators — Conversation Summary, Sentiment, Entity Recognition, PII Redaction — and/or create custom operators (Generative, Extract, or Classify types) via `/Operators`. Operators run automatically on every Transcript created under the Service.
3. Create a Transcript. `POST https://intelligence.twilio.com/v2/Transcripts` referencing the Service SID (`ServiceSid`) and the audio source — either a Twilio `RecordingSid` (via the `Channel`/media source parameters) or an external media URL. Specify the two-channel/participant mapping so operators attribute sentences to speakers.
4. Wait for completion. Transcription and operator execution are asynchronous. Poll `GET /Transcripts/{Sid}` for `status` = `completed`, or subscribe to the completion webhook. Do not read results before `completed`.
5. Retrieve results:
   - Sentences: `GET /Transcripts/{Sid}/Sentences` (raw or redacted).
   - Operator results: `GET /Transcripts/{Sid}/OperatorResults` — one entry per operator with its extracted value/label/summary.
6. Apply redaction policy. If storing, request the redacted sentence view and persist only that where PII must not be retained. Redaction is driven by the PII operator and Service redaction settings.
7. Feed downstream. Map operator results into CRM/ticket fields for ACW, dashboards, or QA scorecards.

## Example

Create a Transcript over a recording and read operator results (Python, requests):

```python
import requests
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth(ACCOUNT_SID, AUTH_TOKEN)
base = "https://intelligence.twilio.com/v2"

# 1. Kick off a transcript for a two-party recording
resp = requests.post(f"{base}/Transcripts", auth=auth, data={
    "ServiceSid": "GAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "Channel": '{"media_properties":{"source_sid":"RExxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"},'
               '"participants":[{"channel_participant":1,"role":"Agent"},'
               '{"channel_participant":2,"role":"Customer"}]}',
})
transcript_sid = resp.json()["sid"]

# 2. Poll until completed
import time
while True:
    t = requests.get(f"{base}/Transcripts/{transcript_sid}", auth=auth).json()
    if t["status"] in ("completed", "failed"):
        break
    time.sleep(3)

# 3. Read operator results (summary, sentiment, entities, ...)
results = requests.get(f"{base}/Transcripts/{transcript_sid}/OperatorResults", auth=auth).json()
for op in results["operator_results"]:
    print(op["name"], op.get("operator_type"), op.get("text_generation_results") or op.get("labels"))
```

## Pitfalls

- Reading results before `status == completed` — you get empty or partial data. Always gate on completion.
- Wrong speaker mapping. If `participants`/channel roles are wrong, sentiment and summaries attribute to the wrong party. Map Agent/Customer correctly, ideally from a dual-channel recording.
- Mono recordings blur speakers. Two-channel recordings give far better per-speaker attribution.
- Persisting un-redacted PII. If compliance requires redaction, store the redacted sentences, not the raw ones.
- Expecting real-time. Operator results are async (seconds to minutes). Not a live-assist path.
- Adding an operator after transcripts exist. New operators apply to newly created Transcripts, not retroactively — re-run to backfill.
- Language mismatch. The Service/transcript language must match the audio or accuracy collapses.

## Output format

Return: (1) the Service SID and its attached operator list (prebuilt + custom, each with purpose), (2) the Transcript creation call with source and speaker mapping, (3) the completion-wait mechanism (poll or webhook), (4) the retrieval calls and the shape of `OperatorResults` you consume, (5) redaction/storage policy, (6) downstream field mapping. Keep operator authoring reusable across Transcripts.

## Reference

- Base: `https://intelligence.twilio.com/v2`. Resources: `/Services` (SID `GA...`), `/Transcripts` (SID `GT...`), `/Operators` (SID `LY...`), plus `/Transcripts/{Sid}/Sentences`, `/Transcripts/{Sid}/OperatorResults`, `/Transcripts/{Sid}/Media`.
- Auth: HTTP Basic `AccountSid`:`AuthToken` (or API key).
- Prebuilt operators: Conversation Summary, Sentiment Analysis, Entity Recognition, PII Redaction (plus language-specific availability). Custom operator types: Generative, Extract, Classify.
- Operators attach at the Service level and execute automatically on each new Transcript created under that Service; they are not retroactive.
- Transcript source: a Twilio `RecordingSid` (`RE...`) or external media URL, with a channel/participant map assigning roles (Agent/Customer). Dual-channel recommended for attribution.
- Status lifecycle: `queued` → `in-progress` → `completed` / `failed`. Completion webhooks are configurable on the Service.
- Redaction: PII redaction produces redacted `Sentences`; request the redacted view for storage under data-retention policy.
- Errors: 404 on unknown Transcript/Service SID; 429 rate limiting; transcript `failed` status carries a failure reason for bad media/language.
