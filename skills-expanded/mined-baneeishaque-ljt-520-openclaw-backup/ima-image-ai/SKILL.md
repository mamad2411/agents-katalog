---
name: IMA Studio Image Generation
version: 1.0.2
category: file-generation
author: IMA Studio (imastudio.com)
keywords: imastudio, image generation, text to image, midjourney
argument-hint: "[text prompt or image URL]"
description: >
  Use for AI image generation via IMA Open API. Supports text-to-image and image-to-image.
  IMPORTANT — Default model selection rule: always recommend the NEWEST and most POPULAR model,
  NOT the cheapest. Default for text_to_image: SeeDream 4.5 (doubao-seedream-4.5, 5pts) — latest
  doubao flagship, balanced choice. Budget option: Nano Banana2 (gemini-3.1-flash-image, 4pts) —
  fastest and cheapest. Premium: Nano Banana Pro (gemini-3-pro-image, 10-18pts) — premium quality
  with size options (1K/2K/4K). NEW: Midjourney (midjourney, 8-10pts) — artist-level aesthetics.
  Default for image_to_image: SeeDream 4.5 (doubao-seedream-4.5, 5pts, attribute_id 1611).
  Production environment has 4 available models. All text_to_image models (4): SeeDream 4.5 (5pts),
  Nano Banana2 (4pts), Nano Banana Pro (10/10/18pts for 1K/2K/4K), Midjourney (8-10pts for 480p/720p).
  All image_to_image models (4): SeeDream 4.5 (5pts), Nano Banana2 (4pts), Nano Banana Pro (10pts),
  Midjourney (8-10pts). Requires an ima_* API key.
---

# IMA Image AI Creation

## 💬 User Experience Protocol (IM / Feishu / Discord) v1.3 🆕

> **CRITICAL FIX in v1.2:** Added Step 0 to ensure correct message ordering in group chats.
> **NEW in v1.3:** Added original image URL in Step 3 caption for easy copying/sharing.
> 
> **v1.1 Bug:** Confirmation message ("好的!来帮你画...") appeared LAST because it used `NO_REPLY`.
> **v1.2 Fix:** Always reply with confirmation FIRST (Step 0), then push updates via `message` tool.
> **v1.3 Enhancement:** Include `🔗 原始链接：[url]` in success caption so users can copy/share the URL.

This skill runs inside IM platforms (Feishu, Discord via OpenClaw).  
**Never let users wait in silence.** Always follow all 6 steps below, every single time.

### 🚫 Never Say to Users

| ❌ Never say | ✅ What users care about |
|-------------|--------------------------|
| `ima_image_create.py` / 脚本 / script | — |
| 自动化脚本 / automation | — |
| 自动处理产品列表 / 查询接口 | — |
| 自动解析参数 / 智能轮询 | — |
| attribute_id / model_version / form_config | — |
| API 调用 / HTTP 请求 / 任何技术参数名 | — |

Only tell users: **model name · estimated time · credits · result (image/media) · plain-language status**.

---

### Estimated Generation Time per Model

| Model | Estimated Time | Poll Every | Send Progress Every |
|-------|---------------|------------|---------------------|
| **SeeDream 4.5** 🌟 | 30~60s | 5s | 20s |
| **Nano Banana2** 💚 | 20~40s | 5s | 15s |
| **Nano Banana Pro** | 60~120s | 5s | 30s |
| **Midjourney** 🎨 | 40~90s | 8s | 25s |

`estimated_max_seconds` = the upper bound of the range above (e.g. 60 for SeeDream 4.5, 120 for Nano Banana Pro, 90 for Midjourney).

---

### Step 0 — Initial Acknowledgment Reply (Normal Reply) 🆕

**⚠️ CRITICAL:** This step is NEW in v1.2 and fixes the message ordering bug.

**Before doing anything else**, reply to the user with a friendly acknowledgment message using your **normal reply** (not `message` tool). This reply will automatically appear FIRST in the conversation.

**Example acknowledgment messages:**
```
好的!来帮你画一只萌萌的猫咪 🐱
```
```
收到！马上为你生成一张 16:9 的风景照 🏔️
```
```
OK! Starting image generation with SeeDream 4.5 🎨
```

**Rules:**
- Keep it short and warm (< 15 words)
- Match the user's language (Chinese/English)
- Include relevant emoji (🐱/🎨/✨)
- This is your ONLY normal reply — all subsequent updates use `message` tool

**Why this matters:**
- Normal replies automatically appear FIRST in the conversation thread
- `message` tool pushes appear in chronological order AFTER your initial reply
- This ensures users see: "好的!" → "🎨 开始生成..." → "✅ 成功!" (correct order)

---

### Step 1 — Pre-Generation Notification (Push via message tool)

**After Step 0 reply**, use the `message` tool to push a notification immediately to the group/channel:

```python
# Agent implementation
message(
    action="send",
    target=group_id,  # or channel_id for Discord
    message="""🎨 开始生成图片，请稍候…
• 模型：[Model Name]
• 预计耗时：[X ~ Y 秒]
• 消耗积分：[N pts]"""
)
```

**User-facing message template:**
```
🎨 开始生成图片，请稍候…
• 模型：[Model Name]
• 预计耗时：[X ~ Y 秒]
• 消耗积分：[N pts]
```

**Cost transparency examples:**
- Balanced/default (5-6 pts): "使用 SeeDream 4.5（5 积分，性价比最佳）"
- Premium (>10 pts): "使用 Nano Banana Pro（10-18 积分，最高质量，支持 1K/2K/4K）"
- Budget (user explicit): "使用 Nano Banana2（4 积分，最便宜最快）"

> Adapt language to match the user. Chinese → `🎨 开始生成图片，请稍候…` / English → `🎨 Starting image generation, please wait…`

---

### Step 2 — Progress Updates (Push via message tool)

**Implementation:**

1. Start the generation script in background or use polling loop
2. Track elapsed time since start
3. Every `[Send Progress Every]` seconds (from table above), push a progress update via `message` tool
4. Stop when task completes (success/failure)

**Progress message template:**
```
⏳ 正在生成中… [P]%
已等待 [elapsed]s，预计最长 [max]s
```

**Progress formula:**
```python
P = min(95, floor(elapsed_seconds / estimated_max_seconds * 100))
```

**Rules:**
- **Cap at 95%** — never show 100% until the API returns `success`
- If `elapsed > estimated_max`: keep P at 95% and append `「稍等，即将完成…」`
- Example: elapsed=40s, max=60s → P = min(95, floor(40/60*100)) = min(95, 66) = **66%**

**When to send progress:**
- **Short tasks (<20s)**: No progress needed, skip Step 2
- **Medium tasks (20-60s)**: Send 1-2 updates
- **Long tasks (>60s)**: Send updates every 20-30s

---

### Step 3 — Success Notification (Push image via message tool)

When task status = `success`, use the `message` tool to **send the generated image directly** (not as a text URL):

**Agent implementation:**
```python
# Get result URL from script output or task detail API
result = get_task_result(task_id)
image_url = result["medias"][0]["url"]

# Push image + caption to group/channel
message(
    action="send",
    target=group_id,
    media=image_url,  # Feishu/Discord will render the image
    caption="""✅ 图片生成成功！
• 模型：[Model Name]
• 耗时：预计 [X~Y]s，实际 [actual]s
• 消耗积分：[N pts]

🔗 原始链接：[image_url]"""
)
```

**User-facing message:**
```
✅ 图片生成成功！
• 模型：[Model Name]
• 耗时：预计 [X~Y]s，实际 [actual]s
• 消耗积分：[N pts]

🔗 原始链接：https://...

[图片直接显示在上方]
```

**Platform-specific notes:**
- **Feishu**: `message(action=send, media=url, caption="...")` — caption appears below image
- **Discord**: Image embeds automatically from URL; caption can be in message text
- **Telegram**: Use `message(action=send, media=url, caption="...")`

**⚠️ Important**: Do NOT send plain text URL like `https://cdn.../image.jpg`. Users expect to see the actual image rendered.

---

### Step 4 — Failure Notification (Push via message tool)

When task status = `failed` or any API/network error, push a failure message with alternative suggestions:

**Agent implementation:**
```python
message(
    action="send",
    target=group_id,
    message="""❌ 图片生成失败
• 原因：[natural_language_error_message]
• 建议改用：
  - [Alt Model 1]（[特点]，[N pts]）
  - [Alt Model 2]（[特点]，[N pts]）

需要我帮你用其他模型重试吗？"""
)
```

**⚠️ CRITICAL: Error Message Translation**

**NEVER show technical error messages to users.** Always translate API errors into natural language:

| Technical Error | ❌ Never Say | ✅ Say Instead (Chinese) | ✅ Say Instead (English) |
|----------------|-------------|------------------------|------------------------|
| `"Invalid product attribute"` / `"Insufficient points"` | Invalid product attribute | 生成参数配置异常，请稍后重试 | Configuration error, please try again later |
| `Error 6006` (credit mismatch) | Error 6006 | 积分计算异常，系统正在修复 | Points calculation error, system is fixing |
| `Error 6010` (attribute_id mismatch) | Attribute ID does not match | 模型参数不匹配，请尝试其他模型 | Model parameters incompatible, try another model |
| `error 400` (bad request, e.g. invalid size) | error 400 / Bad request | 图片参数设置有误，请调整尺寸或比例 | Image parameter error, adjust size or aspect ratio |
| `resource_status == 2` | Resource status 2 / Failed | 图片生成遇到问题，建议换个模型试试 | Image generation failed, try another model |
| `status == "failed"` (no details) | Task failed | 这次生成没成功，要不换个模型试试？ | Generation unsuccessful, try a different model? |
| `timeout` | Task timed out / Timeout error | 生成时间过长已超时，建议用更快的模型 | Generation took too long, try a faster model |
| Network error / Connection refused | Connection refused / Network error | 网络连接不稳定，请检查网络后重试 | Network connection unstable, check network and retry |
| API key invalid | Invalid API key / 401 Unauthorized | API 密钥无效，请联系管理员 | API key invalid, contact administrator |
| Rate limit exceeded | 429 Too Many Requests / Rate limit | 请求过于频繁，请稍等片刻再试 | Too many requests, please wait a moment |
| Model unavailable | Model not available / 503 Service Unavailable | 当前模型暂时不可用，建议换个模型 | Model temporarily unavailable, try another model |
| Unsupported aspect ratio (Nano Banana Pro) | Parameter not supported | 该模型不支持自定义比例，推荐使用 SeeDream 4.5 | This model doesn't support custom aspect ratios, try SeeDream 4.5 |

**Generic fallback (when error is unknown):**
- Chinese: `图片生成遇到问题，请稍后重试或换个模型试试`
- English: `Image generation encountered an issue, please try again or use another model`

**Best Practices:**
1. **Focus on user action**: Tell users what to do next, not what went wrong technically
2. **Be reassuring**: Use phrases like "建议换个模型试试" instead of "生成失败了"
3. **Avoid blame**: Never say "你的参数有问题" → say "参数需要调整一下"
4. **Provide alternatives**: Always suggest 1-2 alternative models in the failure message
5. **Image-specific**: For aspect ratio errors, recommend SeeDream 4.5 (supports custom ratios)

**Failure fallback table:**

| Failed Model | First Alt | Second Alt |
|-------------|-----------|------------|
| **SeeDream 4.5** | **Nano Banana2**（4pts，快速便宜） | **Nano Banana Pro**（10-18pts，高质量） |
| **Nano Banana2** | **SeeDream 4.5**（5pts，更高质量） | **Nano Banana Pro**（10-18pts） |
| **Nano Banana Pro** | **SeeDream 4.5**（5pts，性价比高） | **Nano Banana2**（4pts，最便宜） |
| Any / Unknown | **SeeDream 4.5**（5pts，默认首选） | **Nano Banana2**（4pts，预算紧张） |

---

### Step 5 — Done (No Further Action Needed) 🆕

**v1.2 Change:** Step 5 is now simplified.

After completing Steps 0-4:
- ✅ **Step 0** already sent your normal reply (appears FIRST in chat)
- ✅ **Steps 1-4** pushed all updates via `message` tool (appear in order)
- ✅ **No further action needed** — conversation is complete

**Do NOT:**
- ❌ Reply again with `NO_REPLY` (you already replied in Step 0)
- ❌ Send duplicate confirmation messages
- ❌ Use `message` tool to send the same content twice

**Why this works:**
```
User: "帮我画一只猫"
  ↓
[Step 0] Your normal reply:  "好的!来帮你画一只萌萌的猫咪 🐱"  ← Appears FIRST
  ↓
[Step 1] message tool push:  "🎨 开始生成图片..."  ← Appears SECOND
  ↓
[Step 2] message tool push:  "⏳ 正在生成中… 45%"  ← (if task takes >20s)
  ↓
[Step 3] message tool push:  "✅ 图片生成成功! [图片]"  ← Appears LAST
  ↓
[Step 5] Done. No further replies.
```

---

### 🎯 Summary: What Changed in v1.2 & v1.3

| Version | Step | Change |
|---------|------|--------|
| **v1.2** | Step 0 | ✅ **NEW:** Normal reply with acknowledgment (appears FIRST) |
| **v1.2** | Step 1 | Use `message` tool for **notification only** (not all messages) |
| **v1.2** | Step 5 | ✅ **FIXED:** No further action (already replied in Step 0), no `NO_REPLY` |
| **v1.3** | Step 3 | ✅ **NEW:** Added `🔗 原始链接：[url]` in caption for easy copying |

**Root cause of v1.1 bug:**
- v1.1 used `message` tool for ALL messages (including acknowledgment)
- Then replied `NO_REPLY` to suppress normal reply
- Result: Acknowledgment appeared LAST (because `message` tool pushes are chronological)

**v1.2 fix:**
- Step 0 uses normal reply (automatically appears FIRST)
- Steps 1-4 use `message` tool (appear in chronological order)
- No `NO_REPLY` needed (already replied in Step 0)

**v1.3 enhancement:**
- Step 3 caption now includes original image URL
- Users can easily copy/share the link without asking

---

## Complete Example: Correct v1.2 Flow

```python
# User: "帮我画一只可爱的猫咪"

# Step 0: Normal reply (appears FIRST in chat)
# Agent's normal response mechanism automatically handles this
reply_text = "好的!来帮你画一只萌萌的猫咪 🐱"
# (This is your normal LLM response, not a tool call)

# Step 1: Push start notification
message(
    action="send",
    target="oc_b30b266d43b69674e3ad160de9d13cf2",
    message="🎨 开始生成图片，请稍候…\n• 模型：SeeDream 4.5\n• 预计耗时：30~60秒\n• 消耗积分：5 pts"
)

# Background: Start generation
exec(command="python3 ima_image_create.py ...", background=True, sessionId=sid)

# Step 2: Progress updates (if task takes >20s)
# (Poll in background and push updates via message tool)
start_time = time.time()
while not done:
    elapsed = int(time.time() - start_time)
    if elapsed >= 20 and elapsed % 20 == 0:  # Every 20s
        progress = min(95, int(elapsed / 60 * 100))
        message(
            action="send",
            target="oc_b30b266d43b69674e3ad160de9d13cf2",
            message=f"⏳ 正在生成中… {progress}%\n已等待 {elapsed}s，预计最长 60s"
        )
    time.sleep(5)  # Poll every 5s

# Step 3: Success (push image)
result = get_result(task_id)
message(
    action="send",
    target="oc_b30b266d43b69674e3ad160de9d13cf2",
    media="https://ws.esxscloud.com/.../image.jpeg",
    caption=f"✅ 图片生成成功！\n• 模型：SeeDream 4.5\n• 耗时：实际 35s\n• 消耗积分：5 pts\n\n🔗 原始链接：{result['url']}"
)

# Step 5: Done — no further action
# (Do NOT reply again, do NOT use NO_REPLY)
```

**Result in chat (correct order):**
```
[User] 帮我画一只可爱的猫咪

[Agent] 好的!来帮你画一只萌萌的猫咪 🐱  ← Step 0 (normal reply)

[Agent] 🎨 开始生成图片，请稍候…         ← Step 1 (message tool)
        • 模型：SeeDream 4.5
        • 预计耗时：30~60秒
        • 消耗积分：5 pts

[Agent] ⏳ 正在生成中… 66%                ← Step 2 (message tool, if >20s)
        已等待 40s，预计最长 60s

[Agent] ✅ 图片生成成功！                 ← Step 3 (message tool)
        • 模型：SeeDream 4.5
        • 耗时：实际 35s
        • 消耗积分：5 pts
        
        🔗 原始链接：https://...
        [图片]
```

---

## ⚙️ How This Skill Works

**For transparency:** This skill uses a bundled Python script (`scripts/ima_image_create.py`) to call the IMA Open API. The script:
- Sends your prompt to IMA's servers (two domains, see below)
- Uses `--user-id` **only locally** as a key for storing your model preferences
- Returns an image URL when generation is complete

### 🌐 Network Endpoints Used

This skill connects to **two domains** owned by IMA Studio for complete functionality:

| Domain | Purpose | What's Sent | Authentication |
|--------|---------|-------------|----------------|
| `api.imastudio.com` | Main API (task creation, status polling) | Prompts, model params, task IDs | Bearer token (IMA API key) |
| `imapi.liveme.com` | Image upload service (OSS token generation) | Image files (for i2i tasks), IMA API key | IMA API key + APP_KEY signature |

**Why two domains?**
- `api.imastudio.com`: IMA's image generation API (handles task orchestration)
- `imapi.liveme.com`: IMA's media storage infrastructure (handles large file uploads)
- Both services are **owned and operated by IMA Studio**

**Privacy implications:**
- Your IMA API key is sent to **both domains** for authentication
- Image files are uploaded to `imapi.liveme.com` to obtain CDN URLs (for image_to_image tasks)
- Image generation happens on `api.imastudio.com` using the CDN URLs
- For text_to_image tasks (no image input), only `api.imastudio.com` is contacted

**Security verification:**
```bash
# List all network endpoints in the code:
grep -n "https://" scripts/ima_image_create.py

# Expected output:
# 60: DEFAULT_BASE_URL = "https://api.imastudio.com"
# 61: DEFAULT_IM_BASE_URL = "https://imapi.liveme.com"
```

**If you're concerned about the two-domain architecture:**
1. Review IMA Studio's privacy policy at https://imastudio.com/privacy
2. Contact IMA technical support to confirm domain ownership: support@imastudio.com
3. Use a test/scoped API key first (see security notice below)
4. Monitor network traffic during first run (instructions in SECURITY.md)

### ⚠️ Credential Security Notice

**Your IMA API key is sent to TWO domains:**
1. `api.imastudio.com` — Main image generation API
2. `imapi.liveme.com` — Image upload service (only when using image_to_image tasks)

**Both domains are owned by IMA Studio**, but if you're concerned about credential exposure:

✅ **Best practices:**
- Use a **test/scoped API key** for initial testing (create at https://imastudio.com/api-keys)
- Set a low quota (e.g., 100 credits) for the test key
- Rotate your key after testing if needed
- Monitor network traffic during first run (see SECURITY.md § "Network Traffic Verification")
- Contact IMA support to confirm domain ownership: support@imastudio.com

❌ **Do NOT:**
- Use a production key if you're uncomfortable with the two-domain architecture
- Share your API key with others
- Commit your API key to version control

**What gets sent to IMA servers:**
- ✅ Your image prompt/description
- ✅ Model selection (SeeDream/Nano Banana/Midjourney)
- ✅ Image parameters (size, quality, aspect ratio, etc.)
- ✅ Image files (for image_to_image tasks, uploaded to `imapi.liveme.com`)
- ✅ IMA API key (for authentication to both domains)
- ❌ NO user_id (it's only used locally)

**What's stored locally:**
- `~/.openclaw/memory/ima_prefs.json` - Your model preferences (< 1 KB)
- `~/.openclaw/logs/ima_skills/` - Generation logs (auto-deleted after 7 days)
- See [SECURITY.md](SECURITY.md) for complete privacy policy

### Agent Execution (Internal Reference)

> **Note for users:** You can review the script source at `scripts/ima_image_create.py` anytime.  
> The agent uses this script to simplify API calls. Network requests go to two IMA Studio domains: `api.imastudio.com` (API) and `imapi.liveme.com` (image uploads for i2i tasks).

Use the bundled script internally to ensure correct parameter construction:

```bash
# List available models
python3 {baseDir}/scripts/ima_image_create.py \
  --api-key  $IMA_API_KEY \
  --task-type text_to_image \
  --list-models

# Generate image
python3 {baseDir}/scripts/ima_image_create.py \
  --api-key  $IMA_API_KEY \
  --task-type text_to_image \
  --model-id  doubao-seedream-4.5 \
  --prompt   "a cute puppy running on grass" \
  --user-id  {user_id} \
  --output-json

# Image to image
python3 {baseDir}/scripts/ima_image_create.py \
  --api-key      $IMA_API_KEY \
  --task-type    image_to_image \
  --model-id     doubao-seedream-4.5 \
  --prompt       "turn into oil painting style" \
  --input-images https://example.com/photo.jpg \
  --user-id      {user_id} \
  --output-json
```

The script outputs JSON — parse it to get the result URL and pass it to the user via the UX protocol messages above.

---

## Overview

Call IMA Open API to create AI-generated images. All endpoints require an `ima_*` API key. The core flow is: **query products → create task → poll until done**.

---

## 🔒 Security & Transparency Policy

> **This skill is community-maintained and open for inspection.**

### ✅ What Users CAN Do

**Full transparency:**
- ✅ **Review all source code**: Check `scripts/ima_image_create.py` and `ima_logger.py` anytime
- ✅ **Verify network calls**: Network requests go to two IMA Studio domains: `api.imastudio.com` (API) and `imapi.liveme.com` (image uploads for i2i tasks). See "🌐 Network Endpoints Used" section above for full details.
- ✅ **Inspect local data**: View `~/.openclaw/memory/ima_prefs.json` and log files
- ✅ **Control privacy**: Delete preferences/logs anytime, or disable file writes (see below)

**Configuration allowed:**
- ✅ **Set API key** in environment or agent config:
  - Environment variable: `export IMA_API_KEY=ima_your_key_here`
  - OpenClaw/MCP config: Add `IMA_API_KEY` to agent's environment configuration
  - Get your key at: https://imastudio.com
- ✅ **Use scoped/test keys**: Test with limited API keys, rotate after testing
- ✅ **Disable file writes**: Make prefs/logs read-only or symlink to `/dev/null`

**Data control:**
- ✅ **View stored data**: `cat ~/.openclaw/memory/ima_prefs.json`
- ✅ **Delete preferences**: `rm ~/.openclaw/memory/ima_prefs.json` (resets to defaults)
- ✅ **Delete logs**: `rm -rf ~/.openclaw/logs/ima_skills/` (auto-cleanup after 7 days anyway)
- ✅ **Review security**: See [SECURITY.md](SECURITY.md) for complete privacy policy

### ⚠️ Advanced Users: Fork & Modify

If you need to modify this skill for your use case:
1. **Fork the repository** (don't modify the original)
2. **Update your fork** with your changes
3. **Test thoroughly** with limited API keys
4. **Document your changes** for troubleshooting

**Note:** Modified skills may break API compatibility or introduce security issues. Official support only covers the unmodified version.

### ❌ What to AVOID (Security Risks)

**Actions that could compromise security:**
- ❌ Sharing API keys publicly or in skill files
- ❌ Modifying API endpoints to unknown servers
- ❌ Disabling SSL/TLS certificate verification
- ❌ Logging sensitive user data (prompts, IDs, etc.)
- ❌ Bypassing authentication or billing mechanisms

**Why this matters:**
1. **API Compatibility**: Skill logic aligns with IMA Open API schema
2. **Security**: Malicious modifications could leak credentials or bypass billing
3. **Support**: Modified skills may not be supported
4. **Community**: Breaking changes affect all users

### 📋 Privacy & Data Handling Summary

**What this skill does with your data:**

| Data Type | Sent to IMA? | Stored Locally? | User Control |
|-----------|-------------|-----------------|--------------|
| Image prompts | ✅ Yes (required for generation) | ❌ No | None (required) |
| API key | ✅ Yes (authentication header) | ❌ No | Set via env var |
| user_id (optional CLI arg) | ❌ **Never** (local preference key only) | ✅ Yes (as prefs file key) | Change `--user-id` value |
| Model preferences | ❌ No | ✅ Yes (~/.openclaw) | Delete anytime |
| Generation logs | ❌ No | ✅ Yes (~/.openclaw) | Auto-cleanup 7 days |

**Privacy recommendations:**
1. **Use test/scoped API keys** for initial testing
2. **Note**: `--user-id` is **never sent to IMA servers** - it's only used locally as a key for storing preferences in `~/.openclaw/memory/ima_prefs.json`
3. **Review source code** at `scripts/ima_image_create.py` to verify network calls (search for `create_task` function)
4. **Rotate API keys** after testing or if compromised

**Get your IMA API key:** Visit https://imastudio.com to register and get started.

### 🔧 For Skill Maintainers Only

**Version control:**
- All changes must go through Git with proper version bumps (semver)
- CHANGELOG.md must document all changes
- Production deployments require code review

**File checksums (optional):**
```bash
# Verify skill integrity
sha256sum SKILL.md scripts/ima_image_create.py
```

If users report issues, verify file integrity first.

---

## 🧠 User Preference Memory

> User preferences **override** recommended defaults. If a user has generated before, use their preferred model — not the system default.

### Storage

Preferences are stored in `~/.openclaw/memory/ima_prefs.json`:

```json
{
  "user_{user_id}": {
    "text_to_image": {
      "model_id":   "doubao-seedream-4.5",
      "model_name": "SeeDream 4.5",
      "credit":     5,
      "last_used":  "2026-02-26T03:07:27Z"
    },
    "image_to_image": {
      "model_id":   "doubao-seedream-4.5",
      "model_name": "SeeDream 4.5",
      "credit":     5,
      "last_used":  "2026-02-25T10:00:00Z"
    }
  }
}
```

If the file or key doesn't exist, fall back to the ⭐ Recommended Defaults below.

---

### When to Read (Before Every Generation)

1. Load `~/.openclaw/memory/ima_prefs.json` (silently, no error if missing)
2. Look up `user_{user_id}.{task_type}` (e.g. `user_12345.text_to_image`)
3. **If found** → use that model; mention it in the pre-generation notification:
   ```
   🎨 根据你的使用习惯，将用 [Model Name] 帮你生成图片…
   • 模型：[Model Name]（你的常用模型）
   • 预计耗时：[X ~ Y 秒]
   • 消耗积分：[N pts]
   ```
4. **If not found** → use the ⭐ Recommended Default and skip any mention of "习惯"

---

### When to Write (After Every Successful Generation)

After task status = `success`, save the used model back to the preference file:

```python
import json, os
from datetime import datetime, timezone

prefs_path = os.path.expanduser("~/.openclaw/memory/ima_prefs.json")
os.makedirs(os.path.dirname(prefs_path), exist_ok=True)

try:
    with open(prefs_path) as f:
        prefs = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    prefs = {}

user_key = f"user_{user_id}"
prefs.setdefault(user_key, {})[task_type] = {
    "model_id":   model_id,
    "model_name": model_name,
    "credit":     credit,
    "last_used":  datetime.now(timezone.utc).isoformat(),
}

with open(prefs_path, "w") as f:
    json.dump(prefs, f, ensure_ascii=False, indent=2)
```

---

### When to Update (User Explicitly Changes Model)

Detect intent in user messages. Trigger phrases (Chinese + English):

| Trigger | Action |
|---------|--------|
| `用XXX` / `换成XXX` / `改用XXX` | Switch to named model for this request AND save as new preference |
| `以后都用XXX` / `默认用XXX` / `always use XXX` | Save as preference, confirm: `✅ 已记住！以后图片生成默认用 [XXX]` |
| `换个模型` / `try another model` | Ask user to choose; save chosen model as new preference |
| `用最好的` / `best quality` / `最强的` | Use highest-quality model (Nano Banana Pro); save preference |
| `用便宜的` / `cheapest` | Use lowest-cost model; do NOT save as preference unless user says "以后都用" |

---

### Preference Confirmation Message

When switching to a different model than their preference, confirm:

```
💡 你之前喜欢用 [Old Model]。这次你选了 [New Model]，要把它设为默认吗？
回复「是」保存 / 回复「否」仅本次使用
```

---

## ⭐ Recommended Defaults

> **These are fallback defaults — only used when no user preference exists.**  
> **Always default to the newest and most popular model. Do NOT default to the cheapest.**

| Task | Default Model | model_id | version_id | Cost | Why |
|------|--------------|----------|------------|------|-----|
| text_to_image | **SeeDream 4.5** | `doubao-seedream-4.5` | `doubao-seedream-4-5-251128` | 5 pts | Latest doubao flagship, photorealistic 4K |
| text_to_image (budget) | **Nano Banana2** | `gemini-3.1-flash-image` | `gemini-3.1-flash-image` | 4 pts | Fastest and cheapest option |
| text_to_image (premium) | **Nano Banana Pro** | `gemini-3-pro-image` | `gemini-3-pro-image-preview` | 10/10/18 pts | Premium quality, 1K/2K/4K options |
| text_to_image (artistic) | **Midjourney** 🎨 | `midjourney` | `v6` | 8/10 pts | Artist-level aesthetics, creative styles |
| image_to_image | **SeeDream 4.5** | `doubao-seedream-4.5` | `doubao-seedream-4-5-251128` | 5 pts | Latest, best i2i quality |
| image_to_image (budget) | **Nano Banana2** | `gemini-3.1-flash-image` | `gemini-3.1-flash-image` | 4 pts | Cheapest option |
| image_to_image (premium) | **Nano Banana Pro** | `gemini-3-pro-image` | `gemini-3-pro-image-preview` | 10 pts | Premium quality |
| image_to_image (artistic) | **Midjourney** 🎨 | `midjourney` | `v6` | 8/10 pts | Artist-level aesthetics, style transfer |

**Selection guide by use case:**
- General image generation → **SeeDream 4.5** (5pts)
- **Custom aspect ratio (16:9, 9:16, 4:3, etc.)** → **SeeDream 4.5** 🌟 or **Nano Banana Pro/2/MAX** 🆕 (native support)
- Budget-conscious / fast generation → **Nano Banana2** (4pts)
- Highest quality with size control (1K/2K/4K) → **Nano Banana Pro** (text_to_image: 10-18pts, image_to_image: 10pts)
- **Artistic/creative styles, illustrations, paintings** → **Midjourney** 🎨 (8-10pts)
- Style transfer / image editing → **SeeDream 4.5** (5pts) or **Midjourney** 🎨 (artistic)

**🆕 MAJOR UPDATE: Nano Banana series now has NATIVE aspect_ratio support!**
- **Nano Banana Pro**: ✅ Supports `aspect_ratio` (1:1, 16:9, 9:16, 4:3, 3:4) NATIVELY
- **Nano Banana2**: ✅ Supports `aspect_ratio` (1:1, 16:9, 9:16, 4:3, 3:4) NATIVELY
- **Nano Banana MAX**: ✅ Supports `aspect_ratio` (1:1, 16:9, 9:16, 4:3, 3:4) NATIVELY

**When user requests unsupported combinations:**
- **Midjourney + aspect_ratio (16:9, etc.)**: Recommend **SeeDream 4.5** or **Nano Banana series** instead
  ```
  ❌ Midjourney 暂不支持自定义 aspect_ratio（仅支持 1024x1024 方形）
  
  ✅ 推荐方案：
    1. SeeDream 4.5（支持虚拟参数 aspect_ratio）
    2. Nano Banana Pro/2/MAX（原生支持 aspect_ratio）
       • 支持比例：1:1, 16:9, 9:16, 4:3, 3:4
  ```
    • 成本：5 积分（性价比最佳）
    • 质量：4K photorealistic
  
  需要我帮你用 SeeDream 4.5 生成吗？
  ```
- **Any model + 8K**: Inform user no model supports 8K, max is 4K (Nano Banana Pro or SeeDream 4.5)
- **Any model + 7:3 ratio**: Non-standard ratio, not supported. Suggest closest supported ratio (e.g., 21:9 for ultra-wide, 2:3 for portrait)

---

## Supported Models

⚠️ **Production Environment**: **4 image models** are currently available in production (as of 2026-02-28).

### text_to_image (4 models)

| Name | model_id | version_id | Cost | attribute_id | Size Options |
|------|----------|------------|------|--------------|--------------|
| **SeeDream 4.5** 🌟 | `doubao-seedream-4.5` | `doubao-seedream-4-5-251128` | 5 pts | 2341 | Default (adaptive 4k) |
| **Nano Banana2** 💚 | `gemini-3.1-flash-image` | `gemini-3.1-flash-image-preview` | 4/6/10/13 pts | 4400/4401/4402/4403 | 512px (4pts) / 1K (6pts) / 2K (10pts) / 4K (13pts) |
| **Nano Banana Pro** | `gemini-3-pro-image` | `gemini-3-pro-image-preview` | 10/10/18 pts | 2399/2400/2401 | 1K (10pts) / 2K (10pts) / 4K (18pts) |
| **Midjourney** 🎨 | `midjourney` | `v6` | 8/10 pts | 5451/5452 | 480p (8pts) / 720p (10pts) |

### image_to_image (4 models)

| Name | model_id | version_id | Cost | attribute_id | Size Options |
|------|----------|------------|------|--------------|--------------|
| **SeeDream 4.5** 🌟 | `doubao-seedream-4.5` | `doubao-seedream-4-5-251128` | 5 pts | 1611 | Default (adaptive 4k) |
| **Nano Banana2** 💚 | `gemini-3.1-flash-image` | `gemini-3.1-flash-image-preview` | 4/6/10/13 pts | 4404/4405/4406/4407 | 512px (4pts) / 1K (6pts) / 2K (10pts) / 4K (13pts) |
| **Nano Banana Pro** | `gemini-3-pro-image` | `gemini-3-pro-image-preview` | 10 pts | 2402/2403/2404 | 1K (10pts) / 2K (10pts) / 4K (18pts) |
| **Midjourney** 🎨 | `midjourney` | `v6` | 8/10 pts | 5453/5454 | 480p (8pts) / 720p (10pts) |

### Recommended Defaults (Based on Production Data)

| Task Type | Default Model | Reason | Cost |
|-----------|---------------|--------|------|
| **text_to_image** | SeeDream 4.5 | Latest DouBao flagship, balanced quality/cost | 5 pts |
| **text_to_image (budget)** | Nano Banana2 | Fastest and cheapest option | 4 pts |
| **text_to_image (artistic)** | Midjourney 🎨 | Artist-level aesthetics, creative styles | 8-10 pts |
| **image_to_image** | SeeDream 4.5 | Newest, most stable, cost-effective | 5 pts (attribute_id: 1611) |
| **image_to_image (budget)** | Nano Banana2 | Cheapest option | 4 pts |
| **image_to_image (artistic)** | Midjourney 🎨 | Artist-level aesthetics, style transfer | 8-10 pts |

**Premium option**: Nano Banana Pro — Highest quality with size control (1K/2K/4K), higher cost (10-18 pts for text_to_image, 10 pts for image_to_image).

### Model Capabilities (Parameter Support)

⚠️ **Critical**: Models have **varying parameter support**. Custom aspect ratios are now **supported by multiple models**.

| Model | Custom Aspect Ratio | Max Resolution | Size Options | Notes |
|-------|---------------------|----------------|--------------|-------|
| **SeeDream 4.5** | ✅ (via virtual params) | 4K (adaptive) | 8 aspect ratios | Supports 1:1, 16:9, 9:16, 4:3, 3:4, 2:3, 3:2, 21:9 (5 pts) |
| **Nano Banana2** | ✅ **Native support** 🆕 | 4K (4096×4096) | 512px/1K/2K/4K + aspect ratios | Supports 1:1, 16:9, 9:16, 4:3, 3:4; size via `attribute_id` |
| **Nano Banana Pro** | ✅ **Native support** 🆕 | 4K (4096×4096) | 1K/2K/4K + aspect ratios | Supports 1:1, 16:9, 9:16, 4:3, 3:4; size via `attribute_id` |
| **Midjourney** 🎨 | ❌ (1:1 only) | 1024px (square) | 480p/720p via `attribute_id` | Fixed 1024x1024, artistic style focus |

**Key Capabilities**:
- ✅ **Aspect ratio control**: **SeeDream 4.5** (virtual params), **Nano Banana Pro/2/MAX** (native support)
- ❌ **8K**: Not supported by any model (max is 4K)
- ✅ **Size control**: **Nano Banana2**, **Nano Banana Pro**, and **Midjourney** support multiple size options via different `attribute_id`s
- ✅ **Budget option**: **Nano Banana2** is the cheapest at 4 pts for 512px, but 4K costs 13pts
- 🎨 **Artistic styles**: **Midjourney** excels at creative, artistic, and illustration styles
- 💡 **Best value**: **SeeDream 4.5** at 5pts offers aspect ratio flexibility; **Nano Banana2** 512px at 4pts for fastest/cheapest

---

## Environment

Base URL: `https://api.imastudio.com`

Required/recommended headers for all `/open/v1/` endpoints:

| Header | Required | Value | Notes |
|--------|----------|-------|-------|
| `Authorization` | ✅ | `Bearer ima_your_api_key_here` | API key authentication |
| `x-app-source` | ✅ | `ima_skills` | Fixed value — identifies skill-originated requests |
| `x_app_language` | recommended | `en` / `zh` | Product label language; defaults to `en` if omitted |

```
Authorization: Bearer ima_your_api_key_here
x-app-source: ima_skills
x_app_language: en
```

---

## ⚠️ MANDATORY: Always Query Product List First

> **CRITICAL**: You MUST call `/open/v1/product/list` BEFORE creating any task.  
> The `attribute_id` field is REQUIRED in the create request. If it is `0` or missing, you get:  
> `"Invalid product attribute"` → `"Insufficient points"` → task fails completely.  
> **NEVER construct a create request from the model table alone. Always fetch the product first.**

### Why attribute_id is required

The `attribute_id` uniquely identifies the exact product variant (model + quality tier). The billing and routing system uses it to:
1. Validate the product is purchasable
2. Deduct the correct credits via `credit_rules`
3. Route the request to the right backend model

### How to get attribute_id

```python
# Step 1: Query product list for the target category
GET /open/v1/product/list?app=ima&platform=web&category=text_to_image

# Step 2: Walk the V2 tree to find your model (type=3 leaf nodes only)
for group in response["data"]:
    for version in group.get("children", []):
        if version["type"] == "3" and version["model_id"] == target_model_id:
            attribute_id = version["credit_rules"][0]["attribute_id"]
            credit       = version["credit_rules"][0]["points"]
            model_version = version["id"]    # = version_id
            model_name    = version["name"]
            form_defaults = {f["field"]: f["value"] for f in version["form_config"]}
```

### Quick Reference: Known attribute_ids

⚠️ **Production warning**: `attribute_id` and `credit` values change frequently. Always call `/open/v1/product/list` at runtime; table below is pre-queried reference (2026-02-27).

**text_to_image**:

| Model | model_id | attribute_id | credit | Size |
|-------|----------|-------------|--------|------|
| **SeeDream 4.5** 🌟 | `doubao-seedream-4.5` | **2341** | 5 pts | Default (adaptive 4k) |
| **Nano Banana2** (512px) | `gemini-3.1-flash-image` | **4400** | 4 pts | 512px (512×512) |
| **Nano Banana2** (1K) | `gemini-3.1-flash-image` | **4401** | 6 pts | 1K (1024×1024) |
| **Nano Banana2** (2K) | `gemini-3.1-flash-image` | **4402** | 10 pts | 2K (2048×2048) |
| **Nano Banana2** (4K) | `gemini-3.1-flash-image` | **4403** | 13 pts | 4K (4096×4096) |
| Nano Banana Pro (1K) | `gemini-3-pro-image` | **2399** | 10 pts | 1K (1024×1024) |
| Nano Banana Pro (2K) | `gemini-3-pro-image` | **2400** | 10 pts | 2K (2048×2048) |
| Nano Banana Pro (4K) | `gemini-3-pro-image` | **2401** | 18 pts | 4K (4096×4096) |

**image_to_image**:

| Model | model_id | attribute_id | credit | Size |
|-------|----------|-------------|--------|------|
| **SeeDream 4.5** 🌟 | `doubao-seedream-4.5` | **1611** | 5 pts | Default (adaptive 4k) |
| **Nano Banana2** (512px) | `gemini-3.1-flash-image` | **4404** | 4 pts | 512px (512×512) |
| **Nano Banana2** (1K) | `gemini-3.1-flash-image` | **4405** | 6 pts | 1K (1024×1024) |
| **Nano Banana2** (2K) | `gemini-3.1-flash-image` | **4406** | 10 pts | 2K (2048×2048) |
| **Nano Banana2** (4K) | `gemini-3.1-flash-image` | **4407** | 13 pts | 4K (4096×4096) |
| Nano Banana Pro (1K) | `gemini-3-pro-image` | **2402** | 10 pts | 1K (1024×1024) |
| Nano Banana Pro (2K) | `gemini-3-pro-image` | **2403** | 10 pts | 2K (2048×2048) |
| Nano Banana Pro (4K) | `gemini-3-pro-image` | **2404** | 10 pts | 4K (4096×4096) |

⚠️ **Note**: Production has 3 models (SeeDream 4.5 + Nano Banana2 + Nano Banana Pro). All other models mentioned in older documentation are no longer available.

---

## Core Flow

```
1. GET /open/v1/product/list?app=ima&platform=web&category=<type>
   → REQUIRED: Get attribute_id, credit, model_version, form_config defaults

[image_to_image only]
2. Upload input image → get public HTTPS URL
   → See "Image Upload" section below

3. POST /open/v1/tasks/create
   → Must include: attribute_id, model_name, model_version, credit, cast, prompt (nested!)

4. POST /open/v1/tasks/detail  {task_id: "..."}
   → Poll every 2–5s until medias[].resource_status == 1
   → Extract url from completed media
```

### Common Mistakes (and resulting errors)

| Mistake | Error |
|---------|-------|
| `attribute_id` is 0 or missing | `"Invalid product attribute"` → Insufficient points |
| `attribute_id` outdated (production changed) | Same errors; always query product list first |
| `prompt` at outer level instead of `parameters.parameters.prompt` | Prompt ignored or error |
| `cast` missing from inner `parameters` | Billing validation failure |
| `credit` wrong / missing | Error 6006 |
| `model_name` or `model_version` missing | Wrong model routing |
| Skip product list, use hardcoded values | All of the above |

---

## Image Upload (Required for image_to_image)

**The IMA Open API does NOT accept raw bytes or base64 images. All input images must be public HTTPS URLs.**

When a user provides an image (local file, bytes, base64), upload it first using the IMA presigned URL flow — the same flow the IMA frontend uses.

### Two-Step Upload Flow

```
Step 1: GET /api/rest/oss/getuploadtoken  → { ful, fdl }
Step 2: PUT {ful}  with raw image bytes
         → use fdl (CDN URL) as input_images value
```

See `ima-all-ai/SKILL.md` → "Image Upload" section for the complete implementation.

### Quick Reference

```python
# If user provides a URL already → use directly
if source.startswith("https://"):
    input_url = source

# If user provides a local file → upload first
else:
    token = get_upload_token(uid, ima_token, suffix="jpeg",
                             content_type="image/jpeg", ...)
    upload_image_to_oss(image_bytes, "image/jpeg", token["ful"])
    input_url = token["fdl"]   # CDN URL → use as input_images

# Then create task
task_id = create_task("image_to_image", prompt, product,
                      input_images=[input_url], size="4k")
```

> **CDN**: `https://ima-ga.esxscloud.com/`  |  **OSS**: `zhubite-imagent-bot.oss-us-east-1.aliyuncs.com`

---

## Supported Task Types

| category | Capability | Input |
|----------|------------|-------|
| `text_to_image` | Text → Image | prompt |
| `image_to_image` | Image → Image | prompt + input image URL |

---

## Detail API status values

| Field | Type | Values |
|-------|------|--------|
| **`resource_status`** | int or `null` | `0`=处理中, `1`=可用, `2`=失败, `3`=已删除；`null` 当作 0 |
| **`status`** | string | `"pending"`, `"processing"`, `"success"`, `"failed"` |

| `resource_status` | `status` | Action |
|-------------------|----------|--------|
| `0` or `null` | `pending` / `processing` | Keep polling |
| `1` | `success` (or `completed`) | Stop when **all** medias are 1; read `url` |
| `1` | `failed` | Stop, handle error |
| `2` / `3` | any | Stop, handle error |

> **Important**: Treat `resource_status: null` as 0. Stop only when **all** medias have `resource_status == 1`. Check `status != "failed"` when rs=1.

---

## API 1: Product List

```
GET /open/v1/product/list?app=ima&platform=web&category=text_to_image
```

Returns a **V2 tree structure**: `type=2` nodes are model groups, `type=3` nodes are versions (leaves). Only `type=3` nodes contain `credit_rules` and `form_config`.

```json
[
  {
    "id": "SeeDream",
    "type": "2",
    "name": "SeeDream",
    "model_id": "",
    "children": [
      {
        "id": "doubao-seedream-4-5-251128",
        "type": "3",
        "name": "SeeDream 4.5",
        "model_id": "doubao-seedream-4.5",
        "credit_rules": [
          { "attribute_id": 2341, "points": 5, "attributes": { "default": "enabled" } }
        ],
        "form_config": [
          { "field": "size", "type": "tags", "value": "4k",
            "options": [{"label":"2K","value":"2k"}, {"label":"4K","value":"4k"}] }
        ]
      }
    ]
  }
]
```

**How to pick a version for task creation:**
1. Traverse nodes to find `type=3` leaves (versions)
2. Use `model_id` and `id` (= `model_version`) from the leaf
3. Pick `credit_rules[].attribute_id` matching your desired quality/size
4. Use `form_config[].value` as default `parameters` values

---

## API 2: Create Task

```
POST /open/v1/tasks/create
```

### text_to_image — Verified ✅

No image input. `src_img_url: []`, `input_images: []`.

```json
{
  "task_type": "text_to_image",
  "enable_multi_model": false,
  "src_img_url": [],
  "parameters": [{
    "attribute_id":  2341,
    "model_id":      "doubao-seedream-4.5",
    "model_name":    "SeeDream 4.5",
    "model_version": "doubao-seedream-4-5-251128",
    "app":           "ima",
    "platform":      "web",
    "category":      "text_to_image",
    "credit":        5,
    "parameters": {
      "prompt":       "a beautiful mountain sunset, photorealistic",
      "size":         "4k",
      "n":            1,
      "input_images": [],
      "cast":         {"points": 5, "attribute_id": 2341}
    }
  }]
}
```

### image_to_image — Verified ✅

```json
{
  "task_type": "image_to_image",
  "enable_multi_model": false,
  "src_img_url": ["https://example.com/input.jpg"],
  "parameters": [{
    "attribute_id":  1611,
    "model_id":      "doubao-seedream-4.5",
    "model_name":    "SeeDream 4.5",
    "model_version": "doubao-seedream-4-5-251128",
    "app":           "ima",
    "platform":      "web",
    "category":      "image_to_image",
    "credit":        5,
    "parameters": {
      "prompt":       "turn into oil painting style",
      "size":         "4k",
      "n":            1,
      "input_images": ["https://example.com/input.jpg"],
      "cast":         {"points": 5, "attribute_id": 1611}
    }
  }]
}
```

> ⚠️ `size` must be from `form_config` options (e.g. `"2k"`, `"4k"`, `"2048x2048"`). `"adaptive"` is NOT valid for SeeDream 4.5 — causes error 400.
> Top-level `src_img_url` **and** `parameters.input_images` must both contain the input image URL.

**Key fields**:

| Field | Required | Description |
|-------|----------|-------------|
| `parameters[].credit` | ✅ | Must equal `credit_rules[].points`. Error 6006 if wrong. |
| `parameters[].parameters.prompt` | ✅ | Prompt must be nested here, NOT at top level. |
| `parameters[].parameters.cast` | ✅ | `{"points": N, "attribute_id": N}` — mirror of credit. |
| `parameters[].parameters.n` | ✅ | Number of outputs (usually `1`). |
| `parameters[].parameters.input_images` | image_to_image | Array of input image URLs. |
| top-level `src_img_url` | image_to_image | Must also contain the input image URL. |

Response: `data.id` = task ID for polling.

---

## API 3: Task Detail (Poll)

```
POST /open/v1/tasks/detail
{"task_id": "<id from create response>"}
```

Poll every 2–5s. Completed response:

```json
{
  "id": "task_abc",
  "medias": [{
    "resource_status": 1,
    "url": "https://cdn.../output.jpg",
    "format": "jpg",
    "width": 1024,
    "height": 1024
  }]
}
```

Output fields: `url`, `width`, `height`, `format` (jpg/png).

---

## FAQ: Parameter Support & Limitations

### Q1: Can I generate 16:9 or 7:3 aspect ratio images?

**A:** ✅ **YES! Multiple models now support custom aspect ratios.**

**✅ Supported aspect ratios:**
- **SeeDream 4.5**: 1:1, 16:9, 9:16, 4:3, 3:4, 2:3, 3:2, 21:9 (via virtual params)
- **Nano Banana Pro/2/MAX**: 1:1, 16:9, 9:16, 4:3, 3:4 (native support) 🆕

**❌ Not supported:**
- **Midjourney**: Fixed 1024×1024 (1:1 only)
- **Custom ratios**: 7:3, 8:3, or other non-standard ratios are NOT supported by any model

**Workarounds for unsupported ratios:**
1. **Use video models** (recommended): Generate with video models (e.g., Wan 2.6 text_to_video) that support 16:9, 9:16, 1:1, then extract the first frame as an image.
2. **Post-processing**: Generate a 1:1 image, then crop/extend to desired aspect ratio.

**Model recommendation by aspect ratio need:**
- **Standard ratios (16:9, 9:16, 4:3, 3:4)**: Nano Banana Pro/2 (native support, no virtual params)
- **Extended ratios (2:3, 3:2, 21:9)**: SeeDream 4.5 only
- **Square (1:1)**: Any model (SeeDream, Nano Banana, or Midjourney)

### Q2: How do I generate 4K images with Nano Banana Pro?

**A:** ✅ **Use the `size` parameter** with the correct `attribute_id`.

Nano Banana Pro supports 3 size options via different `credit_rules`:
- **1K** (1024×1024): 10 pts, attribute_id `2399` (default)
- **2K** (2048×2048): 10 pts, attribute_id `2400`
- **4K** (4096×4096): **18 pts**, attribute_id `2401`

**Script usage:**
```bash
python3 ima_image_create.py \
  --task-type text_to_image \
  --model-id gemini-3-pro-image \
  --prompt "your prompt" \
  --extra-params '{"size": "4K"}'
```

The script automatically selects the correct `attribute_id` (2401) when you specify `size: "4K"`.

### Q3: Can I generate 8K images?

**A:** ❌ **No**. No model currently supports 8K resolution. The maximum available is:
- **Nano Banana Pro**: 4K (4096×4096)
- **SeeDream 4.5 / 4.0 / 3.0**: 4K (adaptive)
- **All others**: ≤ 1280×1280

**Workaround**: Generate at maximum resolution (4K), then use external AI upscaling tools (e.g., Real-ESRGAN, Topaz Gigapixel) to upscale to 8K.

### Q4: Which models support custom aspect ratios?

**A:** 🌟 **Multiple models now support aspect ratios!**

**✅ NATIVE support (no virtual params needed):**
- **Nano Banana Pro**: 1:1, 16:9, 9:16, 4:3, 3:4 🆕
- **Nano Banana2**: 1:1, 16:9, 9:16, 4:3, 3:4 🆕
- **Nano Banana MAX**: 1:1, 16:9, 9:16, 4:3, 3:4 🆕

**✅ Virtual parameter mapping (SeeDream):**
- **SeeDream 4.5**: 1:1, 16:9, 9:16, 4:3, 3:4, 2:3, 3:2, 21:9, 2k, 4k

**❌ NOT supported:**
- **Midjourney**: Fixed 1024×1024 (1:1) only

**SeeDream 4.5 aspect_ratio support (8 ratios):**
- `1:1` → 2048×2048 (square, 5 pts)
- `16:9` → 2560×1440 (widescreen, 5 pts)
- `9:16` → 1440×2560 (vertical/portrait, 5 pts)
- `4:3` → 2304×1728 (classic, 5 pts)
- `3:4` → 1728×2304 (vertical, 5 pts)
- `2:3` → 1664×2496 (portrait, 5 pts)
- `3:2` → 2496×1664 (landscape, 5 pts)
- `21:9` → 3024×1296 (ultra-wide, 5 pts)
- `2k` / `4k` → Adaptive resolution (5 pts)

**Nano Banana series native support (5 ratios):**
- `1:1`, `16:9`, `9:16`, `4:3`, `3:4`
- No virtual params needed, passed directly to API

**Usage:**
```bash
# SeeDream 4.5 (virtual params)
python3 ima_image_create.py \
  --task-type text_to_image \
  --model-id doubao-seedream-4.5 \
  --prompt "beautiful landscape" \
  --extra-params '{"aspect_ratio": "16:9"}'

# Nano Banana Pro (native support)
python3 ima_image_create.py \
  --task-type text_to_image \
  --model-id gemini-3-pro-image \
  --prompt "beautiful landscape" \
  --extra-params '{"aspect_ratio": "16:9"}'
```

**How it works (virtual param mapping for SeeDream):**
1. User provides `aspect_ratio: "16:9"` as input
2. Script queries product list and finds `is_ui_virtual=true` field
3. Applies `value_mapping`: `aspect_ratio: "16:9"` → `size: "2560x1440"`
4. API receives actual parameter: `size: "2560x1440"`

**Nano Banana series**: Aspect ratio passed directly, no mapping needed.

### Q5: Why does my `aspect_ratio` parameter get ignored?

**A:** Two possibilities:

1. **Model doesn't support it**: Only SeeDream 4.5 and Nano Banana series support custom aspect ratios. Midjourney only supports 1:1 (square).

2. **Virtual param not available in production**: For SeeDream 4.5, the `is_ui_virtual=true` feature may not be deployed yet. If you get 1:1 square output despite requesting 16:9, the API doesn't have the virtual parameter mapping active.

**Solution:**
- Use **SeeDream 4.5** or **Nano Banana Pro/2/MAX** for aspect ratio needs
- Use **video models** with custom aspect ratio, extract first frame
- Post-process: Crop or extend the image manually

### Q6: What's the difference between `size` and `resolution`?

**A:**
- **`size`**: For Nano Banana Pro only. Options: "1K", "2K", "4K". Controls output resolution via different `attribute_id`s.
- **`resolution`**: Used in **video models** (e.g., "1080P", "720P", "4K"). Not applicable to text_to_image models.

### Q7: Can I control the aspect ratio after generation?

**A:** Not directly in this skill. Options:
1. **Crop**: Take the center/top/bottom portion of the square image to get desired ratio.
2. **Extend (inpainting)**: Use image editing APIs to extend the image to fill the target aspect ratio.
3. **Video workaround**: Use video models with desired aspect ratio, extract first frame.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `attribute_id` not from `credit_rules` | Always fetch product list first |
| Placing `prompt` at param top-level | `prompt` must be inside `parameters[].parameters` |
| Missing `app` / `platform` in parameters | Required — use `ima` / `web` |
| Wrong `credit` value | Must exactly match `credit_rules[].points` (error 6006) |
| `size: "adaptive"` for SeeDream 4.5 i2i | Use values from `form_config` options only |
| Missing image in both `src_img_url` and `input_images` | Both fields required for image_to_image |

---

## Python Example

```python
import time
import requests

BASE_URL = "https://api.imastudio.com"
API_KEY  = "ima_your_key_here"
HEADERS  = {
    "Authorization":  f"Bearer {API_KEY}",
    "Content-Type":   "application/json",
    "x-app-source":   "ima_skills",
    "x_app_language": "en",
}


def get_products(category: str) -> list:
    """Returns flat list of type=3 version nodes from V2 tree."""
    r = requests.get(
        f"{BASE_URL}/open/v1/product/list",
        headers=HEADERS,
        params={"app": "ima", "platform": "web", "category": category},
    )
    r.raise_for_status()
    nodes = r.json()["data"]
    versions = []
    for node in nodes:
        for child in node.get("children") or []:
            if child.get("type") == "3":
                versions.append(child)
            for gc in child.get("children") or []:
                if gc.get("type") == "3":
                    versions.append(gc)
    return versions


def create_image_task(task_type: str, prompt: str, product: dict, input_images: list = None, **extra) -> str:
    """Returns task_id. task_type: 'text_to_image' or 'image_to_image'."""
    input_images = input_images or []
    rule = product["credit_rules"][0]
    form_defaults = {f["field"]: f["value"] for f in product.get("form_config", []) if f.get("value") is not None}

    nested_params = {
        "prompt": prompt,
        "n":      1,
        "input_images": input_images,
        "cast":   {"points": rule["points"], "attribute_id": rule["attribute_id"]},
        **form_defaults,
    }
    nested_params.update({k: v for k, v in extra.items() if k in ("size",)})

    body = {
        "task_type":          task_type,
        "enable_multi_model": False,
        "src_img_url":        input_images,
        "parameters": [{
            "attribute_id":  rule["attribute_id"],
            "model_id":      product["model_id"],
            "model_name":    product["name"],
            "model_version": product["id"],
            "app":           "ima",
            "platform":      "web",
            "category":      task_type,
            "credit":        rule["points"],
            "parameters":    nested_params,
        }],
    }
    r = requests.post(f"{BASE_URL}/open/v1/tasks/create", headers=HEADERS, json=body)
    r.raise_for_status()
    return r.json()["data"]["id"]


def poll(task_id: str, interval: int = 3, timeout: int = 300) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = requests.post(f"{BASE_URL}/open/v1/tasks/detail", headers=HEADERS, json={"task_id": task_id})
        r.raise_for_status()
        task   = r.json()["data"]
        medias = task.get("medias", [])
        if medias:
            if any(m.get("status") == "failed" for m in medias):
                raise RuntimeError(f"Task failed: {task_id}")
            rs = lambda m: m.get("resource_status") if m.get("resource_status") is not None else 0
            if any(rs(m) == 2 for m in medias):
                raise RuntimeError(f"Task failed: {task_id}")
            if all(rs(m) == 1 for m in medias):
                return task
        time.sleep(interval)
    raise TimeoutError(f"Task timed out: {task_id}")


# text_to_image (SeeDream 4.5)
products = get_products("text_to_image")
task_id  = create_image_task("text_to_image", "mountain sunset, photorealistic", products[0])
result   = poll(task_id)
print(result["medias"][0]["url"])

# text_to_image with Midjourney (artistic style)
products    = get_products("text_to_image")
midjourney  = next(p for p in products if p["model_id"] == "midjourney")
task_id     = create_image_task("text_to_image", "fantasy castle, impressionist painting style", midjourney)
result      = poll(task_id, interval=8)  # Midjourney: poll every 8s
print(result["medias"][0]["url"])

# text_to_image with aspect ratio (Nano Banana Pro - native support)
products = get_products("text_to_image")
nano_pro = next(p for p in products if p["model_id"] == "gemini-3-pro-image")
task_id  = create_image_task("text_to_image", "beautiful landscape", nano_pro, aspect_ratio="16:9")
result   = poll(task_id)
print(result["medias"][0]["url"])

# image_to_image (size must match form_config options, NOT "adaptive")
products     = get_products("image_to_image")
seedream_i2i = next(p for p in products if p["model_id"] == "doubao-seedream-4.5")
task_id      = create_image_task(
    "image_to_image", "turn into oil painting style", seedream_i2i,
    input_images=["https://example.com/input.jpg"],
    size="4k",
)
result = poll(task_id)
print(result["medias"][0]["url"])

# image_to_image with Midjourney (artistic style transfer)
products     = get_products("image_to_image")
midjourney   = next(p for p in products if p["model_id"] == "midjourney")
task_id      = create_image_task(
    "image_to_image", "anime style, vibrant colors", midjourney,
    input_images=["https://example.com/portrait.jpg"],
)
result = poll(task_id, interval=8)  # Midjourney: poll every 8s
print(result["medias"][0]["url"])
```
