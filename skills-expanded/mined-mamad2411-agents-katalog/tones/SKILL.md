---
name: tones
description: Public API tone presets (X-API-KEY). List, create, get, update, delete, duplicate, apply to slide deck, save-as-preset. PublicApiToneController (/api/v2/tones).
---

# Skill: Tone Presets

## Description

Manage **tone presets** (voice, audience, detail level) and apply them to a slide deck. This skill documents **PublicApiToneController** at `/api/v2/tones`. Slide decks also expose **per-deck** tone settings under `.../slide-deck/{id}/tone-settings` (see **slide-decks** skill); this skill covers the **shared preset library** endpoints.

Authenticate with `X-API-KEY`.

---

## TypeScript types (request / response)

Mirrors `PublicApiToneController` / client tone DTOs (field names follow API JSON; use snake_case if your client sends snake_case per server config).

```typescript
// --- List (GET) ---
// Query: offset (default 0), limit (default 20), search (optional),
// visibility (optional, repeat or array: PRIVATE, SYSTEM)
type TonePresetListResponse = {
  data: TonePresetResponse[];
  total: number;
  offset: number;
  limit: number;
};

type TonePresetResponse = {
  id: string;
  name: string;
  description?: string | null;
  visibility?: string | null;
  output_language?: string | null;
  text_detail_level?: string | null;
  tone?: string | null;
  voice?: string | null;
  audience?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
};

// --- Create (POST) ---
type CreateTonePresetRequest = {
  name: string;
  description?: string | null;
  output_language?: string | null;
  text_detail_level?: string | null;
  tone?: string | null;
  voice?: string | null;
  audience?: string | null;
};

// --- Update (PUT /{tone_id}) ---
type UpdateTonePresetRequest = {
  name?: string | null;
  description?: string | null;
  output_language?: string | null;
  text_detail_level?: string | null;
  tone?: string | null;
  voice?: string | null;
  audience?: string | null;
};

// --- Apply (POST /{tone_id}/apply) ---
type ApplyTonePresetRequest = {
  project_id: string;
  slide_deck_id: string;
};
type ApplyTonePresetResponse = TonePresetResponse; // applied settings snapshot

// --- Save as preset from deck (POST /save-as-preset) — 201 ---
type SaveAsPresetRequest = {
  slide_deck_id: string;
  name: string;
  description?: string | null;
};

// --- Duplicate (POST /{tone_id}/duplicate) — 201 ---
type DuplicateTonePresetRequest = {
  name: string;
};
```

---

## List Tone Presets

```bash
curl "$LAYERPROOF_BASE_URL/api/v2/tones?offset=0&limit=20" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Get Tone Preset

```bash
curl "$LAYERPROOF_BASE_URL/api/v2/tones/<tone_id>" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Create Tone Preset

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/tones" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"name":"Boardroom","output_language":"en-US","tone":"Professional"}'
```

---

## Update Tone Preset

```bash
curl -X PUT "$LAYERPROOF_BASE_URL/api/v2/tones/<tone_id>" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"description":"Stricter pacing"}'
```

---

## Delete Tone Preset

Response: 204 No Content (cannot delete system presets — 403).

```bash
curl -X DELETE "$LAYERPROOF_BASE_URL/api/v2/tones/<tone_id>" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Apply Preset to Slide Deck

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/tones/<tone_id>/apply" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"project_id":"<project_uuid>","slide_deck_id":"<slide_deck_uuid>"}'
```

---

## Save Current Deck Settings as Preset

Persists the slide deck’s current tone settings as a new preset. Response (201): `TonePresetResponse`.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/tones/save-as-preset" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"slide_deck_id":"<slide_deck_uuid>","name":"From deck settings"}'
```

---

## Duplicate Preset

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/tones/<tone_id>/duplicate" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"name":"Copy of Boardroom"}'
```

---

## Agent behavior

Always check environment variables first before making any API call:

```bash
if [[ -z "${LAYERPROOF_BASE_URL}" ]]; then
  echo "ERROR: LAYERPROOF_BASE_URL is not set."
  return 1
fi
if [[ -z "${LAYERPROOF_API_KEY}" ]]; then
  echo "ERROR: LAYERPROOF_API_KEY is not set."
  return 1
fi

# Load .env.local if present
if [[ -f .env.local ]]; then
  set -a
  source .env.local
  set +a
fi
```

| User intent | Endpoint | Method |
|-------------|----------|--------|
| List presets | `/api/v2/tones` | GET |
| Get preset | `/api/v2/tones/{toneId}` | GET |
| Create preset | `/api/v2/tones` | POST |
| Update preset | `/api/v2/tones/{toneId}` | PUT |
| Delete preset | `/api/v2/tones/{toneId}` | DELETE |
| Apply to slide deck | `/api/v2/tones/{toneId}/apply` | POST |
| Save deck settings as preset | `/api/v2/tones/save-as-preset` | POST |
| Duplicate preset | `/api/v2/tones/{toneId}/duplicate` | POST |

**Note:** Per-deck tone fields without creating a preset are under **GET/PUT** `.../slide-deck/{slideDeckId}/tone-settings` (slide-decks skill).

---

## Response format (required)

- Always show the **raw JSON response** in a JSON code block.
- If the response contains image URLs, show images and the JSON.
