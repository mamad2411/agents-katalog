---
name: assemblyai-api
description: "AssemblyAI API skill. Use when working with AssemblyAI for upload, transcript. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# AssemblyAI API
API version: 1.3.4

## Auth
ApiKey Authorization in header

## Base URL
https://api.assemblyai.com

## Setup
1. Set your API key in the appropriate header
2. GET /v2/transcript -- verify access
3. POST /v2/upload -- create first upload

## Endpoints

10 endpoints across 2 groups. See references/api-spec.lap for full details.

### upload
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/upload | Upload a media file |

### transcript
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/transcript | Transcribe audio |
| GET | /v2/transcript | List transcripts |
| GET | /v2/transcript/{transcript_id} | Get transcript |
| DELETE | /v2/transcript/{transcript_id} | Delete transcript |
| GET | /v2/transcript/{transcript_id}/{subtitle_format} | Get subtitles for transcript |
| GET | /v2/transcript/{transcript_id}/sentences | Get sentences in transcript |
| GET | /v2/transcript/{transcript_id}/paragraphs | Get paragraphs in transcript |
| GET | /v2/transcript/{transcript_id}/word-search | Search words in transcript |
| GET | /v2/transcript/{transcript_id}/redacted-audio | Get redacted audio |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a upload?" -> POST /v2/upload
- "Create a transcript?" -> POST /v2/transcript
- "List all transcript?" -> GET /v2/transcript
- "Get transcript details?" -> GET /v2/transcript/{transcript_id}
- "Delete a transcript?" -> DELETE /v2/transcript/{transcript_id}
- "Get transcript details?" -> GET /v2/transcript/{transcript_id}/{subtitle_format}
- "List all sentences?" -> GET /v2/transcript/{transcript_id}/sentences
- "List all paragraphs?" -> GET /v2/transcript/{transcript_id}/paragraphs
- "List all word-search?" -> GET /v2/transcript/{transcript_id}/word-search
- "List all redacted-audio?" -> GET /v2/transcript/{transcript_id}/redacted-audio
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
