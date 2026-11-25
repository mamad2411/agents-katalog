---
name: giggle-generation-aimv
description: Use when the user wants to create AI music videos (MV)—including generating music from text prompts or using custom lyrics. Triggers: generate MV, music video, make video for this song, lyrics video, create MV, AI music video, music+video, generate video from lyrics.
version: "0.0.2"
license: MIT
requires:
  bins: [python3]
  env: [GIGGLE_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw":
      {
        "emoji": "📂",
        "requires": {
          "bins": ["python3"],
          "env": ["GIGGLE_API_KEY"],
          "pip": ["requests"]
        },
        "primaryEnv": "GIGGLE_API_KEY"
      },
  }
---

[简体中文](./SKILL.zh-CN.md) | English

# MV Trustee Mode API Skill

Calls the MV trustee mode API to run the full MV generation workflow. **Project creation and task submission are merged into one step in the script**—call `execute_workflow` once only; never call create and submit separately.

## ⚠️ Review Before Installing

**Please review before installing.** This skill will:

1. **Network** – Calls Giggle.pro API for MV generation

**Requirements**: `python3`, `GIGGLE_API_KEY` (system environment variable), pip packages: `requests`

---

## Required Setup Before First Use

**Before performing any operation, confirm the user has configured the API Key.**

**API Key**: Log in to [Giggle.pro](https://giggle.pro/) and obtain the API Key from account settings.

**Configuration**: Set system environment variable `GIGGLE_API_KEY`
- `export GIGGLE_API_KEY=your_api_key`

**Verification steps**:
1. Confirm the user has configured `GIGGLE_API_KEY` in system environment
2. If not configured, **guide the user**:
   > Hello! Before using the MV generation feature, you need to configure the API Key. Please go to [Giggle.pro](https://giggle.pro/) to get your API Key, then run `export GIGGLE_API_KEY=your_api_key` in the terminal.
3. Wait for the user to configure before continuing the workflow

## Three Music Generation Modes

| Mode | music_generate_type | Required params | Description |
|------|---------------------|-----------------|-------------|
| **Prompt** | `prompt` | prompt, vocal_gender | Describe music in text |
| **Custom** | `custom` | lyrics, style, title | Provide lyrics, style, and title |

### Shared Parameters (All Modes, Required)

- **reference_image** or **reference_image_url**: Reference image—provide at least one (asset_id or download URL). Also supports base64 image, e.g. `"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="`. For base64: pass the raw Base64 string directly; do not add the data:image/xxx;base64 prefix.
- **aspect**: Aspect ratio, `16:9` or `9:16`
- **scene_description**: Visual scene description, **default empty**—only set when the user explicitly mentions the scene (max 200 chars)
- **subtitle_enabled**: Enable subtitles, **default false**

### Mode-Specific Parameters

**Prompt mode**:
- `prompt`: Music description (required)
- `vocal_gender`: Vocal gender — `male` / `female` / `auto` (optional, default `auto`)
- `instrumental`: Instrumental only (optional, default false)

**Custom mode**:
- `lyrics`: Lyrics content (required)
- `style`: Music style (required)
- `title`: Song title (required)

## Workflow Function

Use `execute_workflow` to run the full workflow—**call once and wait**. Internally: create project + submit task (merged) → poll progress (every 3 sec) → detect and pay pending items → wait for completion (max 1 hour).

**Important**:
- Never call `create_project` and `submit_mv_task` separately—always use `execute_workflow` or `create_and_submit`
- After calling, just wait for the function to return; all intermediate steps are automatic

### Function Signature

```python
execute_workflow(
    music_generate_type: str,      # Mode: prompt / custom
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
)
```

### Parameter Extraction Rules

1. **reference_image and reference_image_url**: At least one required. Use `reference_image` for asset_id; use `reference_image_url` for image URL or base64.
2. **scene_description**: Default empty—only fill when the user explicitly mentions "scene", "visual description", or "visual style".
3. **subtitle_enabled**: Default False—only set True when the user explicitly requests subtitles.
4. **aspect**: Use `9:16` when the user mentions portrait/vertical/9:16; otherwise default `16:9`.
5. **Mode selection**: "Describe music / use prompt" → prompt; "Here are my lyrics / lyrics are" → custom;

### Examples

**Prompt mode**:
```python
api = MVTrusteeAPI()
result = api.execute_workflow(
    music_generate_type="prompt",
    aspect="16:9",
    project_name="My MV",
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
    project_name="Lyrics MV",
    reference_image="asset_xxx",
    lyrics="Verse 1: Spring breeze on my face...",
    style="pop",
    title="Spring Song"
)
```

**With scene description** (when user explicitly describes the scene):
```python
result = api.execute_workflow(
    music_generate_type="prompt",
    aspect="16:9",
    project_name="Scene MV",
    reference_image_url="https://...",
    prompt="Electronic dance music",
    scene_description="City nightscape, neon lights, flowing traffic"
)
```

### Submit Task API Request Example (Prompt Mode)

Submit endpoint (`/api/v1/trustee_mode/mv/submit`) request body:

```json
{
  "project_id": "c0cb1f32-bb07-4449-add5-e42ccfca1ab6",
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

Note: `reference_image` (asset_id) and `reference_image_url` (URL or base64) are mutually exclusive.

**Custom mode**:

```json
{
  "project_id": "0ea74500-9178-4693-b581-342d5e17994c",
  "music_generate_type": "custom",
  "lyrics": "Verse 1:\nStanding by the sea watching the sunset\nMemories rush in like waves\n\nChorus:\nLet the sea breeze blow away all worries\nIn this golden moment\nWe found each other\n",
  "style": "pop ballad",
  "title": "Seaside Memories",
  "reference_image": "is45gnvumgd",
  "scene_description": "A couple walking on the beach at dusk, long shadows, orange-red sky gradient",
  "aspect": "9:16",
  "subtitle_enabled": false
}
```

### Query Progress API Response Example

Query endpoint (`/api/v1/trustee_mode/mv/query`) response (all steps completed):

```json
{
  "code": 200,
  "msg": "success",
  "uuid": "24052352-f231-495a-9581-3827c4eb0bdf",
  "data": {
    "project_id": "65cf262d-c4b1-4733-abf1-ec6a7bdb944a",
    "video_asset": {
      "asset_id": "ryco1asdmb",
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

Note: When `pay_status` is `pending`, call the pay endpoint. When all `steps` are done, `video_asset.download_url` will have a value—return the full signed URL. Correct format:
```
https://assets.giggle.pro/private/ai_director/348e4956c7bd4f763b/qzjc7gwkpf.mp4?Policy=...&Key-Pair-Id=...&Signature=...&response-content-disposition=attachment
```
Wrong (unsigned URL only):
```
https://assets.giggle.pro/private/ai_director/348e4956c7bd4f763b/qzjc7gwkpf.mp4
```

### Pay API Request and Response

Pay endpoint (`/api/v1/trustee_mode/mv/pay`):

**Request body**:
```json
{
  "project_id": "28b4f4f7-d219-4754-a78b-d9896cd16573"
}
```

**Response**:
```json
{
  "code": 200,
  "msg": "success",
  "uuid": "1440ba5f-ba1c-41f6-a92c-53337a7df1c2",
  "data": {
    "order_id": "2a93f1c1-9e4d-4d29-89d7-15deea4e3732",
    "price": 580
  }
}
```

### Retry API Request Example

When a step fails, guide the user to call the retry endpoint to resume from that step:

```json
{
  "project_id": "28b4f4f7-d219-4754-a78b-d9896cd16573",
  "current_step": "shot"
}
```

Note: `current_step` is the step name to retry (e.g. `music-generate`, `storyboard`, `shot`, `editor`).

### create_and_submit (Optional)

If you only need to create the project and submit the task without waiting for completion, use `create_and_submit`. **Never** call `create_project` and `submit_mv_task` separately:

```python
api = MVTrusteeAPI()
r = api.create_and_submit(
    project_name="My MV",
    music_generate_type="prompt",
    aspect="16:9",
    reference_image_url="https://...",
    prompt="Upbeat pop"
)
# Returns project_id for manual query/pay later
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

Returns error message on failure.
