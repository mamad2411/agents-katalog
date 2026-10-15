---
name: maliang-image
version: "1.3.0"
description: "Generate images from text prompts or edit existing images with AI. Powered by Google Gemini via Maliang API. Free credit on first use. Supports text-to-image and multi-image inpainting editing."
user-invocable: true
metadata:
  openclaw:
    emoji: "🎨"
    homepage: "https://nano.djdog.ai"
    requires:
      bins:
        - curl
---

# Maliang Image — AI Image Generation & Editing

**Provider**: Maliang API ([nano.djdog.ai](https://nano.djdog.ai))
**Model**: Google Gemini (image generation & editing)
**Pricing**: Returned dynamically by the API. Free credit on first use.

## What it does

Generate images from text descriptions or edit existing images using AI.

- **No images provided** → text-to-image generation
- **Images provided** → AI image editing / inpainting (1–10 reference images, user-provided only)

## Security & Data Handling

- **API Key**: Auto-provisioned on first use and stored locally at `~/.config/maliang/`. One account per machine (identified by hostname), persisted across all sessions. You can revoke it at any time.
- **Images**: Only images explicitly provided by the user are sent to the API. The skill never reads files unless the user specifies the file path. All uploads go over HTTPS.
- **No data collection**: The API processes your request and returns results. Images are not stored permanently on the server.

## Inputs needed

| Input | Source | Required |
|-------|--------|----------|
| Text prompt | User message | YES |
| Reference images | User provides file paths or URLs | NO (if omitted, generates from text) |
| Aspect ratio | User preference | NO (default: `1:1`) |

## API Key Management (Persistent, One Account Per Machine)

The API key and short code are stored in persistent files so they survive across sessions. **NEVER provision a new key if one already exists and is valid.**

### Step 0 — Load or provision API key

```bash
# 1. Check persistent key file first
CONFIG_DIR="$HOME/.config/maliang"
KEY_FILE="$CONFIG_DIR/api_key"
CODE_FILE="$CONFIG_DIR/short_code"

MALIANG_API_KEY=""
MALIANG_SHORT_CODE=""

if [ -f "$KEY_FILE" ]; then
  MALIANG_API_KEY=$(cat "$KEY_FILE")
fi
if [ -f "$CODE_FILE" ]; then
  MALIANG_SHORT_CODE=$(cat "$CODE_FILE")
fi

# 2. If no key exists, provision with machine_id for idempotency
if [ -z "$MALIANG_API_KEY" ]; then
  mkdir -p "$CONFIG_DIR"
  MACHINE_ID=$(hostname)
  PROVISION_RESULT=$(curl -s -X POST "https://nano.djdog.ai/api/v1/provision" \
    -H "Content-Type: application/json" \
    -d "{\"machine_id\": \"$MACHINE_ID\"}")
  MALIANG_API_KEY=$(echo "$PROVISION_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['api_key'])")
  MALIANG_SHORT_CODE=$(echo "$PROVISION_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['short_code'])")
  echo "$MALIANG_API_KEY" > "$KEY_FILE"
  echo "$MALIANG_SHORT_CODE" > "$CODE_FILE"
  chmod 600 "$KEY_FILE"
  # Show the user their short code and balance from PROVISION_RESULT
fi
```

**IMPORTANT**: Always read from `~/.config/maliang/api_key` first. Only call `/api/v1/provision` if the file does not exist. The `machine_id` (hostname) ensures that even if the key file is lost, the same machine reconnects to the same account without getting extra credit.

### Verify existing key (401 recovery)

If the key file exists but API returns 401, the key may be invalid. Re-provision with `machine_id` — this will reconnect to the existing account (no new credit):

```bash
# If 401 error, re-provision with machine_id
rm -f "$KEY_FILE" "$CODE_FILE"
MACHINE_ID=$(hostname)
PROVISION_RESULT=$(curl -s -X POST "https://nano.djdog.ai/api/v1/provision" \
  -H "Content-Type: application/json" \
  -d "{\"machine_id\": \"$MACHINE_ID\"}")
MALIANG_API_KEY=$(echo "$PROVISION_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['api_key'])")
MALIANG_SHORT_CODE=$(echo "$PROVISION_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['short_code'])")
echo "$MALIANG_API_KEY" > "$KEY_FILE"
echo "$MALIANG_SHORT_CODE" > "$CODE_FILE"
chmod 600 "$KEY_FILE"
```

## Balance Check

After each task, check remaining balance:

```bash
curl -s "https://nano.djdog.ai/api/v1/balance" \
  -H "Authorization: Bearer ${MALIANG_API_KEY}"
```

Response includes `short_code` for recharge reference. If balance is low, remind the user:
> Your balance is $X.XX. To recharge, visit: https://nano.djdog.ai/recharge/{short_code}

### View status

To show the user their account status at any time:

```bash
echo "Key prefix: ${MALIANG_API_KEY:0:11}..."
echo "Short code: $MALIANG_SHORT_CODE"
# Then call the balance endpoint above to show current balance
```

## Workflow

### Step 1 — Determine mode

- If the user provides one or more images (file paths, URLs, or pasted base64): **edit mode**
- Otherwise: **generate mode**

### Step 2 — Prepare images (edit mode only)

For each image the user provides:
1. If it is a local file path, read and base64-encode it.
2. If it is a URL, download it first, then base64-encode.
3. Strip any `data:image/...;base64,` prefix — the API accepts raw base64.
4. Verify each image is under 10 MB after decoding.
5. Maximum 10 images total.

### Step 3 — Submit task

**Generate mode** — call:

```bash
curl -s -X POST "https://nano.djdog.ai/api/v1/generate" \
  -H "Authorization: Bearer ${MALIANG_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "<user prompt>",
    "aspect_ratio": "<ratio, default 1:1>"
  }'
```

**Edit mode** — call:

```bash
curl -s -X POST "https://nano.djdog.ai/api/v1/edit" \
  -H "Authorization: Bearer ${MALIANG_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "<user editing instruction>",
    "image": "<base64 string or array of base64 strings>",
    "aspect_ratio": "<ratio, optional>"
  }'
```

Both return:

```json
{
  "success": true,
  "data": {
    "task_id": "...",
    "status": "pending",
    "created_at": "..."
  }
}
```

Extract `task_id` from the response.

### Step 4 — Poll for result

Poll every 3 seconds, up to 120 seconds max:

```bash
curl -s "https://nano.djdog.ai/api/v1/tasks/${TASK_ID}" \
  -H "Authorization: Bearer ${MALIANG_API_KEY}"
```

Response `data.status` values:

| Status | Meaning | Action |
|--------|---------|--------|
| `pending` | Queued | Keep polling |
| `processing` | Generating | Keep polling |
| `completed` | Done | Get image from `image_url` or `image_base64` |
| `failed` | Error | Show `error.message` to user |
| `dead` | Max retries exceeded | Show error, suggest retry |

### Step 5 — Deliver result

When `status` is `completed`:
- If `image_url` is present: show the URL to the user (preferred).
- If only `image_base64` is present: save to a local file and show the path.

## Output format

```
Image generated successfully!
URL: https://...
Aspect ratio: 1:1
Prompt: "<original prompt>"
```

## Guardrails

- **NEVER provision a new key if `~/.config/maliang/api_key` already exists and is valid.** One machine = one account.
- Never fabricate task IDs or image URLs. Only use values from API responses.
- Never poll more than 40 times (120 seconds). If not completed, tell the user it is still processing and provide the task ID for manual checking.
- Do not send images larger than 10 MB to the edit endpoint.
- Do not send more than 10 images to the edit endpoint.
- If the API returns 402 (INSUFFICIENT_BALANCE), tell the user their balance is low and they need to recharge.
- Prompt max length is 4000 characters. If the user's prompt is longer, ask them to shorten it.

## Failure handling

| Error | Action |
|-------|--------|
| 401 Unauthorized | Key may be invalid. Re-provision with `machine_id` (see "Verify existing key" above). This reconnects to the same account — no extra credit. |
| 402 Insufficient Balance | Tell user to recharge via `https://nano.djdog.ai/recharge/{short_code}` (get short_code from balance endpoint or `~/.config/maliang/short_code`) |
| 400 IMAGE_TOO_LARGE | Tell user the image exceeds 10 MB limit |
| 400 TOO_MANY_IMAGES | Tell user max 10 images allowed |
| Network error | Retry once, then report failure |
| Timeout (120s) | Report task ID, suggest checking later |

## Examples

**Text-to-image:**
```
User: Generate a cute orange cat sitting on a windowsill at sunset, anime style
→ Load key from ~/.config/maliang/api_key (or provision if first use)
→ POST /api/v1/generate with prompt → poll for result → return image URL
```

**Image editing:**
```
User: Change the background of this photo to a beach scene [attaches photo]
→ Base64-encode the photo
→ POST /api/v1/edit with prompt + image, poll for result, return image URL
```

**Multi-image editing:**
```
User: Combine these character designs into one group portrait [attaches 3 images]
→ Base64-encode all 3 images
→ POST /api/v1/edit with prompt + image array, poll for result, return image URL
```
