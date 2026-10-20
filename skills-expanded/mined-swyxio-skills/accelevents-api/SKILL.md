---
name: accelevents-api
description: Use when reading or updating AI Engineer Europe speaker records through the Accelevents REST API, especially for full-record PUT updates, auth header quirks, and preserving existing speaker fields.
---

# Accelevents API — Speaker Management

## API Endpoints

- **Base URL:** `https://api.accelevents.com/rest/host/event/{eventUrl}/speaker`
- **Event URL for Europe:** `ai-engineer-europe-2026`
- **API Key:** stored as `ACCELEVENTS_API_KEY` secret

### Authentication

- **Read (GET):** Use `Authorization: Bearer {key}` header
- **Write (PUT):** Use `Key: {key}` header — the `Authorization: Bearer` header returns 401 on write operations. This is an undocumented quirk.

### GET speakers list

```
GET /rest/host/event/{eventUrl}/speaker?page=0&size=500
Headers: Authorization: Bearer {api_key}
```

Returns `{"data": [...], "recordsTotal": N}`. Each speaker has fields: `speakerId`, `firstName`, `lastName`, `email`, `company`, `linkedIn`, `twitter`, `instagram`, `bio`, `title`, `imageUrl`, `allowEditSessions`, `allowOverrideDetails`, etc.

### PUT (update) speaker

```
PUT /rest/host/event/{eventUrl}/speaker/{speakerId}
Headers: Key: {api_key}, Content-Type: application/json
Body: { full speaker DTO }
```

**CRITICAL: The PUT endpoint replaces the entire speaker record.** Any fields omitted from the request body will be reset to `null`/`false`. You MUST:
1. Fetch the current speaker data first (via GET)
2. Merge your updates into the complete existing data
3. Send the full merged payload in the PUT request

Required fields: `speakerId`, `firstName`, `lastName`, `email`

Fields to always preserve if they exist: `company`, `linkedIn`, `twitter`, `instagram`, `bio`, `title`, `pronouns`, `imageUrl`, `allowEditSessions`, `allowOverrideDetails`, `allowAttendeeAccess`, `moderator`, `showModerator`, `position`

Successful response: `{"type": "Success", "message": "Speaker updated"}`

## Bidirectional Sync Workflow

The sync script (`src/pages/europe/source/_scripts/sync_accelevents.py`) pulls data FROM Accelevents. But schedule.json may have richer data (from prior scraping) that Accelevents lacks. The correct workflow is:

1. **Pull** latest data from Accelevents API
2. **Compare** schedule.json vs API data to find gaps in both directions
3. **Push UP** any data that schedule.json has but Accelevents doesn't (LinkedIn, Twitter, company)
4. **Pull DOWN** any data that Accelevents has but schedule.json doesn't
5. **Save snapshot** after all updates

This ensures both systems have the superset of all known data.

## Known Issues

### Corrupted Company Names
The Accelevents portal has a UI bug where company fields get overwritten with single characters (e.g., "i", "d", "N"). This appears to be a keystroke capture issue in the portal UI. The sync script has a safeguard that rejects single-character company values and logs a `[WARN]`.

### Data Source of Truth
- **schedule.json** is the website's source of truth (at `src/pages/europe/source/schedule.json`)
- **accelevents_speakers_latest.json** is a raw API snapshot for reference/debugging only — not consumed by the website build
- After schedule.json changes, run: `python3 _scripts/export_csv.py`
- After photo changes, run: `pnpm europe:source:sync-public`
