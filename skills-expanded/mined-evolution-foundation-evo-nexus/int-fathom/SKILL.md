---
name: int-fathom
description: Search, retrieve, and summarize Fathom meeting recordings — transcripts, summaries, action items, and team info. Use this skill whenever the user mentions meetings, calls, recordings, meeting notes, transcripts, action items, follow-ups from calls, or anything related to Fathom. Also trigger on "o que foi discutido na reuniao", "resumo da call", "quem participou", "proximos passos da reuniao", "meeting recap", or any reference to past conversations/calls that might be recorded.
homepage: https://fathom.video
metadata: {"clawdis":{"emoji":"🎙️","requires":{"config":["skills.entries.fathom.apiKey"]}}}
---

# Fathom

Retrieve meeting recordings, transcripts, summaries, and action items from Fathom.

## Setup

The skill needs a Fathom API key configured in `openclaw.json` under `skills.entries.fathom`:

```json
{
  "skills": {
    "entries": {
      "fathom": {
        "apiKey": "your-fathom-api-key",
        "env": {
          "FATHOM_API_KEY": "your-fathom-api-key"
        }
      }
    }
  }
}
```

The API key is available at https://fathom.video/settings/api (requires Fathom Team or Enterprise plan).

## Quick Commands

```bash
# List recent meetings
{baseDir}/scripts/fathom.sh meetings

# List meetings with summaries included
{baseDir}/scripts/fathom.sh meetings --include-summary

# List meetings with action items
{baseDir}/scripts/fathom.sh meetings --include-actions

# List meetings with full transcript
{baseDir}/scripts/fathom.sh meetings --include-transcript

# Filter by date range
{baseDir}/scripts/fathom.sh meetings --after "2026-03-01" --before "2026-03-11"

# Filter by participant domain (e.g. external meetings only)
{baseDir}/scripts/fathom.sh meetings --domains-type one_or_more_external

# Filter by recorder email
{baseDir}/scripts/fathom.sh meetings --recorded-by "alice@company.com"

# Filter by team
{baseDir}/scripts/fathom.sh meetings --team "Engineering"

# Get summary for a specific recording
{baseDir}/scripts/fathom.sh summary <recording_id>

# Get transcript for a specific recording
{baseDir}/scripts/fathom.sh transcript <recording_id>

# List teams
{baseDir}/scripts/fathom.sh teams

# List team members (optionally filter by team)
{baseDir}/scripts/fathom.sh members [--team "TeamName"]
```

## Common Workflows

### Morning meeting recap
```bash
# Get yesterday's meetings with summaries and action items
{baseDir}/scripts/fathom.sh meetings --after "$(date -d 'yesterday' +%Y-%m-%d)" --include-summary --include-actions
```

### Prepare for a follow-up
```bash
# Find meetings with a specific company/domain
{baseDir}/scripts/fathom.sh meetings --domains "acme.com" --include-summary --include-actions
```

### Review full conversation
```bash
# First find the meeting
{baseDir}/scripts/fathom.sh meetings --after "2026-03-01"
# Then get the full transcript
{baseDir}/scripts/fathom.sh transcript 123456789
```

### Weekly team digest
```bash
# All meetings from the past week with summaries
{baseDir}/scripts/fathom.sh meetings --after "$(date -d '7 days ago' +%Y-%m-%d)" --include-summary --include-actions
```

## Presenting Results

When presenting meeting data to the user, follow these guidelines:

- **Summaries:** Show the markdown-formatted summary directly. It's already well-structured.
- **Action items:** Present as a checklist with assignee, description, and link to the recording timestamp.
- **Transcripts:** Don't dump the full transcript unless asked. Instead, summarize key points or search for specific topics the user asked about.
- **Meeting list:** Show title, date, participants, and recording link. Keep it scannable.
- **Links:** Always include the Fathom recording URL so the user can watch the replay.

## Response Format

The API returns JSON. Key fields per meeting:

- `title` / `meeting_title` — meeting name
- `recording_id` — unique ID (used to fetch summary/transcript)
- `url` — direct link to recording in Fathom
- `share_url` — shareable link
- `created_at`, `scheduled_start_time`, `recording_start_time` — timestamps
- `calendar_invitees` — list of participants with name, email, and whether external
- `recorded_by` — who recorded the meeting
- `default_summary.markdown_formatted` — the AI-generated summary (when `include_summary=true`)
- `action_items` — list with description, assignee, completion status, and recording timestamp link
- `transcript` — array of `{speaker, text, timestamp}` entries

## Pagination

The meetings endpoint uses cursor-based pagination. The script handles this automatically when you pass `--all` to fetch every page. Without `--all`, it returns the first page only (default limit from API).

## Notes

- Base URL: `https://api.fathom.ai/external/v1`
- Auth: `X-Api-Key` header
- Rate limited (429 responses) — the script retries with backoff
- Transcript inclusion in list endpoint may be restricted for OAuth apps; use the dedicated `/recordings/{id}/transcript` endpoint instead
- Dates should be ISO 8601 format (e.g. `2026-03-11T00:00:00Z` or just `2026-03-11`)
