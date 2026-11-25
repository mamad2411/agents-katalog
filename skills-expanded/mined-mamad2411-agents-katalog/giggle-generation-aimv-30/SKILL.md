---
name: giggle-generation-aimv-30
description: "Use when the user wants a 30-second AI music video (AIMV)—same pipeline as standard AIMV but fixed 30s output via project type aimv-30. Triggers: 30 second MV, 30s AIMV, 30-second music video, half-minute MV, short AIMV; prompt- or custom-lyrics flows same as giggle-generation-aimv."
version: "0.0.1"
license: MIT
requires:
  bins: ["python3 (>=3.6)"]
  env: [GIGGLE_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw":
      {
        "emoji": "📂",
        "requires": {
          "bins": ["python3 (>=3.6)"],
          "env": ["GIGGLE_API_KEY"],
          "pip": ["requests"]
        },
        "primaryEnv": "GIGGLE_API_KEY"
      }
  }
---

# 30-Second AIMV Trustee Mode (`aimv-30`)

The flow matches **giggle-generation-aimv** exactly: one `execute_workflow` call, same submit / poll / pay / wait-to-complete behavior. **Only difference**: project creation uses API `type` **`aimv-30`** (30-second AIMV product line) instead of `mv`.

## ⚠️ Review Before Installing

**Please review before installing.** This skill will:

1. **Network** – Calls the Giggle.pro API for 30-second AIMV generation

**Requirements**: `python3 (>=3.6)`, `GIGGLE_API_KEY` (system environment variable), pip packages: `requests`

> **No Retry on Error**: If script execution encounters an error, **do not retry**. Report the error to the user directly and stop.

---

## Required Setup Before First Use

**Before performing any operation, confirm the user has configured the API key.**

**API key**: Log in to [Giggle.pro](https://giggle.pro/). On the main site, open the **left sidebar** → **API Key** (may also appear as **API 密钥**) and create or copy your key.

**Configuration**: Set the system environment variable `GIGGLE_API_KEY`:

- `export GIGGLE_API_KEY=your_api_key`

**Verification steps**:

1. Confirm `GIGGLE_API_KEY` is set in the environment.
2. If missing, **tell the user**:
   > While logged in at [giggle.pro](https://giggle.pro/) → **left sidebar** → **API Key** → copy the key, then run `export GIGGLE_API_KEY=your_api_key` in the terminal.
3. Do not continue the workflow until the key is configured.

## Two Music Generation Modes

| Mode | music_generate_type | Required params | Description |
|------|---------------------|-----------------|-------------|
| **Prompt** | `prompt` | prompt, vocal_gender | Describe the music in text |
| **Custom** | `custom` | lyrics, style, title | Supply lyrics, style, and title |

### Shared Parameters (All Modes, Required)

- **reference_image** or **reference_image_url**: Reference image—provide at least one (asset ID or download URL). Base64 is supported, e.g. `"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="`. For base64, pass the raw string only; do **not** prefix with `data:image/...;base64,`.
- **aspect**: `16:9` or `9:16`
- **scene_description**: Visual scene text, **defaults to empty**—set only when the user explicitly asks for a scene (max ~200 characters per product rules)
- **subtitle_enabled**: Subtitles, **default false**

### Mode-Specific Parameters

**Prompt mode**:

- `prompt`: Music description (required)
- `vocal_gender`: `male` / `female` / `auto` (optional, default `auto`)
- `instrumental`: Instrumental only (optional, default false)

**Custom mode**:

- `lyrics`: Lyrics body (required)
- `style`: Musical style (required)
- `title`: Song title (required)

## Workflow Function

Use `execute_workflow` for the full workflow—**call once and wait**. Internally: create project (**`type`: `aimv-30`**) + submit task (merged) → poll (~every 3s) → pay when needed → wait up to ~1 hour.

## Continuous progress updates (blocking AIMV workflow)

`execute_workflow` **blocks** for the whole pipeline. Do not run ad-hoc shell `--query` loops yourself.

1. **Before** the call, say the **30s AIMV job** is running, it may take **minutes** and up to **~1 hour**, and you will message again **when the call returns**.
2. **Invoke** `execute_workflow` without making the user ask for progress first.
3. **After return**, on success forward the **full signed `download_url` / `video_asset`**; on failure, plain-language error details and **`project_id`** if useful for support or manual pay/query.
4. **`create_and_submit` only**: if the user only wants IDs first, use that path and query when they follow up.

**Important**:

- Never split `create_project` and `submit_mv_task` manually—use `execute_workflow` or `create_and_submit`.
- After calling, wait for return; intermediate steps are handled inside the script.
- For **non–30-second** / standard-duration AIMV, use skill **giggle-generation-aimv**.

### Function Signature

```python
execute_workflow(
    music_generate_type: str,      # Mode: prompt / custom / upload
    aspect: str,                    # Aspect ratio: 16:9 or 9:16
    project_name: str,              # Project name
    reference_image: str = "",      # Reference image asset_id (mutually exclusive with reference_image_url)
    reference_image_url: str = "",  # Reference image URL or base64 (mutually exclusive with reference_image)
    scene_description: str = "",    # Scene description, default empty
    subtitle_enabled: bool = False, # Subtitle toggle, default False
    # Prompt mode
    prompt: str = "",
    vocal_gender: str = "auto",
    instrumental: bool = False,
    # Custom mode
    lyrics: str = "",
    style: str = "",
    title: str = "",
    # Upload mode
    music_asset_id: str = "",
)
```

### Parameter Extraction Rules

1. **reference_image** and **reference_image_url**: At least one. Use `reference_image` for asset ID; `reference_image_url` for URL or base64.
2. **scene_description**: Leave empty unless the user clearly asks for scene / visual description / visual style.
3. **subtitle_enabled**: Default false; set true only if the user explicitly wants subtitles.
4. **aspect**: Use `9:16` for portrait / vertical; otherwise default `16:9`.
5. **Mode**: User describes the music → `prompt`; user supplies lyrics → `custom`.

### Examples

**Prompt mode**:

```python
api = MVTrusteeAPI()
result = api.execute_workflow(
    music_generate_type="prompt",
    aspect="16:9",
    project_name="My 30s MV",
    reference_image_url="https://example.com/ref.jpg",
    prompt="Upbeat pop, sunny beach vibe",
    vocal_gender="female"
)
```

**Custom mode** (user provides lyrics):

```python
result = api.execute_workflow(
    music_generate_type="custom",
    aspect="9:16",
    project_name="Lyrics 30s MV",
    reference_image="asset_xxx",
    lyrics="Verse 1: Spring breeze on my face...",
    style="pop",
    title="Spring Song"
)
```

**With scene description** (user explicitly describes visuals):

```python
result = api.execute_workflow(
    music_generate_type="prompt",
    aspect="16:9",
    project_name="Scene 30s MV",
    reference_image_url="https://...",
    prompt="Electronic dance music",
    scene_description="City nightscape, neon lights, flowing traffic"
)
```

### Submit Task API Request Example (Prompt Mode)

Submit endpoint (`/api/v1/trustee_mode/mv/submit`) body—same shape as standard AIMV; the project was already created with `type: aimv-30`.

```json
{
  "project_id": "<your-project-id>",
  "music_generate_type": "prompt",
  "prompt": "A cheerful pop song",
  "vocal_gender": "female",
  "instrumental": false,
  "reference_image_url": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMTEhUT...(base64 image data)",
  "scene_description": "A romantic beach walk at sunset, waves gently lapping the shore, pink sky gradient",
  "aspect": "16:9",
  "subtitle_enabled": false
}
```

Note: `reference_image` (asset ID) and `reference_image_url` (URL or base64) are mutually exclusive.

**Custom mode**:

```json
{
  "project_id": "<your-project-id>",
  "music_generate_type": "custom",
  "lyrics": "Verse 1:\nStanding by the sea watching the sunset\nMemories rush in like waves\n\nChorus:\nLet the sea breeze blow away all worries\nIn this golden moment\nWe found each other\n",
  "style": "pop ballad",
  "title": "Seaside Memories",
  "reference_image": "<asset_id>",
  "scene_description": "A couple walking on the beach at dusk, long shadows, orange-red sky gradient",
  "aspect": "9:16",
  "subtitle_enabled": false
}
```

### Query Progress API Response Example

Query endpoint (`/api/v1/trustee_mode/mv/query`) when all steps are done:

```json
{
  "code": 200,
  "msg": "success",
  "uuid": "<response-uuid>",
  "data": {
    "project_id": "<your-project-id>",
    "video_asset": {
      "asset_id": "<asset_id>",
      "download_url": "https://assets.giggle.pro/private/...",
      "thumbnail_url": "https://assets.giggle.pro/private/...",
      "signed_url": "https://assets.giggle.pro/private/...",
      "duration": 0
    },
    "shot_count": 0,
    "current_step": "editor",
    "completed_steps": "music-generate,storyboard,shot,editor",
    "pay_status": "paid",
    "status": "completed",
    "err_msg": "",
    "steps": [...]
  }
}
```

Note: If `pay_status` is `pending`, pay via the pay endpoint. When steps finish, `video_asset.download_url` is populated—return the **complete** signed URL, e.g.:

```
https://assets.giggle.pro/private/ai_director/348e4956c7bd4f763b/qzjc7gwkpf.mp4?Policy=...&Key-Pair-Id=...&Signature=...&response-content-disposition=attachment
```

Do not strip `response-content-disposition=attachment` or other query parameters. Incorrect (unsigned base URL only):

```
https://assets.giggle.pro/private/ai_director/348e4956c7bd4f763b/qzjc7gwkpf.mp4
```

### Pay API Request and Response

Pay endpoint (`/api/v1/trustee_mode/mv/pay`):

**Request body**:

```json
{
  "project_id": "<your-project-id>"
}
```

**Response**:

```json
{
  "code": 200,
  "msg": "success",
  "uuid": "<response-uuid>",
  "data": {
    "order_id": "<order-id>",
    "price": 580
  }
}
```

### Retry API Request Example

If a step fails, the user may call the retry endpoint with the failed step name:

```json
{
  "project_id": "<your-project-id>",
  "current_step": "shot"
}
```

`current_step` is the step to resume from (e.g. `music-generate`, `storyboard`, `shot`, `editor`).

### create_and_submit (Optional)

To create and submit **without** waiting for completion, use `create_and_submit`. **Do not** call `create_project` and `submit_mv_task` as two separate manual steps:

```python
api = MVTrusteeAPI()
r = api.create_and_submit(
    project_name="My 30s MV",
    music_generate_type="prompt",
    aspect="16:9",
    reference_image_url="https://...",
    prompt="Upbeat pop"
)
# Returns project_id for later manual query/pay
```

### Return Value

Success:

```json
{
    "code": 200,
    "msg": "success",
    "data": {
        "project_id": "...",
        "download_url": "https://...",
        "video_asset": {...},
        "status": "completed"
    }
}
```

On failure, an error message is returned (shape depends on API).

## Troubleshooting

| Scenario | Cause | Solution |
|----------|-------|----------|
| `401 Unauthorized` or invalid API key | Missing, expired, or wrong `GIGGLE_API_KEY` | Copy the key again from [giggle.pro](https://giggle.pro/) → **left sidebar** → **API Key**, then `export GIGGLE_API_KEY=...` |
| `429 Too Many Requests` | Rate limited | Wait and retry; avoid bursty parallel submissions |
| Network timeout / connection error | Network or transient API outage | The script retries some network errors (bounded); verify connectivity |
| `pay_status: pending` | Payment required | Handled inside `execute_workflow`; if debugging manually, call pay with `project_id` |
| Task step failed (`status: failed`) | A pipeline step errored | Retry with `current_step` set to the failed step name |
| Workflow timeout (> 1 hour) | Job ran too long | Query by `project_id`; contact support if stuck |
