---
name: picgen
description: Use when the user wants to generate images from the current agent context through configured PicGen providers. Trigger directly only on explicit image-generation requests or when the user names PicGen; ask for confirmation for strong visual-output intent; only suggest PicGen for weak visual exploration intent.
---

# PicGen Skill

PicGen connects agent workflows to user-configured image generation providers. It is designed for non-technical users who want to generate images inside an agent conversation without copying prompts into external image platforms.

## Invocation Policy

Use PicGen when the user explicitly asks to generate, create, make, render, or produce an image, or explicitly names PicGen.

Ask before entering the PicGen workflow when the user expresses strong visual-output intent but has not clearly asked to generate now.

Only suggest PicGen when the user discusses visual direction, mood, brand style, or abstract visual ideas without asking for an output.

Never silently spend user quota. Do not send full conversation context to providers by default; summarize only the visual details needed for the final prompt.

## Installation

If `picgen` is not available, install the CLI first:

```bash
npm install -g @ai-agent-tools/picgen@latest
```

To install or update this skill for supported agents, prefer the standard Skills installer:

```bash
npx -y skills add ai-agent-tools/picgen --skill picgen -g -y --copy
```

For Codex only, the CLI also provides a direct fallback:

```bash
picgen skill install codex --force
```

After installing or updating a skill, the user may need to restart the agent or open a new session before the skill is visible.

## Upgrade

When the user asks to upgrade PicGen, update both the CLI and this skill. Do not ask non-technical users to understand npm, skill caches, or version details.

First check that Node.js and npm are available:

```bash
node -v
npm -v
```

If Node.js or npm is missing, guide the user to install Node.js LTS first.

Upgrade the CLI:

```bash
npm install -g @ai-agent-tools/picgen@latest
picgen --version
picgen doctor --json
```

Then update the skill:

```bash
npx -y skills add ai-agent-tools/picgen --skill picgen -g -y --copy
```

If the Skills installer is unavailable and the current agent is Codex, use:

```bash
picgen skill install codex --force
```

After updating the skill, tell the user to open a new conversation so the agent can reload the latest PicGen instructions. If the new conversation still does not recognize the updated skill, ask the user to restart the agent app.

Keep existing provider and API key configuration. Upgrades should not require users to reconfigure keys unless `picgen doctor --json` reports a real configuration problem.

## Update Awareness

PicGen includes an update checker:

```bash
picgen update check --json
```

Check for updates in these moments:

- The user asks to install, upgrade, configure, diagnose, or open PicGen.
- The user asks about a newer capability, such as reference images, masks, local web UI, provider management, or history.
- A PicGen command fails because an option, command, protocol feature, or skill instruction appears unavailable.
- `picgen doctor --json` or `picgen quickstart` already reports an update hint.

Do not check before every generation request. Avoid interrupting a successful image-generation flow just to suggest an update.

When an update is available, explain the benefit in user terms before giving commands. Prefer capability-led wording:

```text
PicGen 有新版可用。升级后通常可以直接保留现有渠道和 API key，同时获得新版能力，例如参考图、遮罩编辑、本地网页配置/历史查看，以及更好的 Agent 使用说明。要我帮你现在升级吗？
```

If the user is in the middle of an urgent generation task, keep the suggestion lightweight:

```text
当前版本也可以继续用。我看到 PicGen 有新版，完成这次生成后可以升级，能获得更多生图和配置能力。
```

After the user agrees, follow the Upgrade workflow above. If they decline, continue the current task without repeating the reminder in the same conversation unless a missing capability blocks progress.

When update information is unavailable because the npm registry cannot be reached, do not treat it as an error. Continue the requested task and mention only if the user explicitly asked to check updates.

## Environment Check

Before installing the CLI, installing skills, or saving API keys, check whether the current terminal is the user's persistent local environment or a sandbox/temporary environment.

Use lightweight checks such as:

```bash
pwd
echo "$HOME"
node -v
npm -v
npm root -g
which picgen || true
```

If the environment appears persistent and user-level, continue setup there.

If the environment appears sandboxed, remote, temporary, reset between sessions, or unable to write to the user's real home directory, do not install PicGen, install skills, or save API keys there. First request permission to use the user's host/persistent terminal or a persistent user-level environment. Example user-facing wording:

```text
我检测到当前可能是临时沙箱。PicGen 需要安装到你的本机持久环境，否则新会话可能会丢失 CLI、skill 或 API key。请允许我在本机持久环境中继续安装和配置；如果无法授权，我再给你最少的本机终端命令。
```

If permission is granted, continue installation and provider setup in that persistent environment. If permission is unavailable or denied, give the user a minimal copy-paste command sequence for their local terminal. Keep manual instructions short and explain only what the user must do.

## Local Web Interface

If the user says "open PicGen", "打开 PicGen", "打开生图工具", asks for a visual settings page, wants to generate without learning CLI commands, or wants to find previously generated images, start the local web interface:

```bash
picgen open
```

Return the printed local URL to the user. PicGen binds to `127.0.0.1`, defaults to port `8188`, and automatically tries the next ports if needed. The server runs in the foreground; the user or agent should keep the terminal running while the page is in use and close it with Ctrl+C when finished.

If the current environment appears sandboxed, remote, or temporary, first request access to the user's persistent local environment before running `picgen open`. If that is impossible, give the user one short instruction to run `picgen open` in their local terminal and open the printed URL.

The local page may show full API keys only inside the user's browser after an explicit reveal action. In chat, inspect keys only with masked commands such as:

```bash
picgen key list --json
picgen key show PICGEN_GEMINI_PROXY_KEY --json
```

Use the web interface for user-facing setup, provider management, generation, and history browsing. Use CLI commands for agent-driven dry-runs, automation, diagnostics, and precise reproducible steps.

For first-time agent-assisted setup, prefer the clipboard-based CLI flow because it keeps the user in conversation and avoids extra UI switching. Prefer the web interface when the user wants to manage multiple providers, inspect masked key sources, reveal a full key locally, generate images without CLI commands, or find saved image history.

## Workflow

1. Run `picgen doctor --json` to check configuration.
2. If no usable provider is configured, configure one before generation.
3. Choose a preset from the user's intent, such as `poster`, `product-shot`, or `social-cover`.
4. Run `picgen create --dry-run --preset <preset> "<prompt>"`.
5. Present the dry-run as a user-facing generation preview. Do not expose `dry-run` as a technical term unless useful.
6. After the user confirms, run `picgen create --preset <preset> "<prompt>"`.
7. Show local image previews or saved file paths.

If the user explicitly says to generate directly or not ask for confirmation, you may skip the user-facing confirmation step. Still form a generation plan internally.

Default to one generated image. Do not generate multiple images merely to offer options. Generate multiple images only when the user explicitly asks for multiple options, variations, comparisons, or a specific count.

## Provider Setup

When terminal prompts are visible to the user, `picgen setup` is acceptable.

When running inside an agent environment where interactive terminal prompts are not visible, do not run `picgen setup` as a blocking wizard. Ask the user for:

- Provider type: Gemini or OpenAI-compatible.
- Provider host: host only, such as `https://www.pandai.vip`; do not include `/v1` or `/v1beta`.
- API key. Prefer asking the user to copy the key to their clipboard and reply "copied"; avoid asking them to paste secrets into chat.

Then use non-interactive commands.

Gemini-compatible third-party channel:

```bash
picgen provider quick-add gemini-proxy --host https://www.pandai.vip --prefer
picgen key set PICGEN_GEMINI_PROXY_KEY --clipboard
picgen provider test gemini_proxy --json
```

OpenAI-compatible third-party channel:

```bash
picgen provider quick-add openai-proxy --host https://www.pandai.vip --prefer
picgen key set PICGEN_OPENAI_PROXY_KEY --clipboard
picgen provider test openai_proxy --json
```

If clipboard access is unavailable, pass the API key through stdin for `picgen key set`; do not put secrets directly in shell history unless the user explicitly accepts that tradeoff. If the agent runtime cannot pass stdin safely, ask the user to run `picgen key set <ENV_NAME>` in their terminal and paste the key into the hidden prompt.

To inspect configured keys without revealing secret values:

```bash
picgen key list --json
picgen key show PICGEN_GEMINI_PROXY_KEY --json
```

These commands show source, length, masked preview, and fingerprint only. Never ask the user to paste a key into chat just to verify it.

When explaining key inspection to users, say: "In this conversation I only read masked key status, not the full secret. If you need to inspect or edit the complete saved key yourself, PicGen's managed key file is `~/.picgen/.env`; a project-level `.env` in the current directory may override it; shell environment variables take highest priority."

For reference-image generation, pass local images with repeated `--reference <path>` flags:

```bash
picgen create --dry-run --reference ./reference.png --preset poster "<prompt>"
picgen create --reference ./reference.png --preset poster "<prompt>"
```

For local edits or inpainting, pass a mask image together with at least one reference image:

```bash
picgen create --dry-run --reference ./source.png --mask ./mask.png --preset poster "<prompt>"
picgen create --reference ./source.png --mask ./mask.png --preset poster "<prompt>"
```

OpenAI-compatible providers use `/v1/images/edits` with multipart `image[]` uploads when reference images are provided, and multipart `mask` uploads when masks are provided. Gemini providers use `generateContent`; masks are treated as mask-guidance images with explicit edit instructions rather than native inpainting.

PicGen routes by provider capabilities. When reference images are provided, agents may omit `--provider` and let PicGen select a provider that supports `reference-image`, unless the user explicitly requested a provider.

## First Smoke Test

After configuring a provider, run the first test generation with a low-cost, fast, one-image plan. Do not use `poster`, `product-shot`, `social-cover`, premium modes, large sizes, or high-quality presets for initial verification.

For Gemini providers, prefer the flash image model for the first test:

```bash
picgen create --dry-run --provider gemini_proxy --preset fast-draft --model gemini-3.1-flash-image-preview "一张简洁的 PicGen 测试图，白色背景，少量蓝绿色科技感点缀"
picgen create --yes --provider gemini_proxy --preset fast-draft --model gemini-3.1-flash-image-preview "一张简洁的 PicGen 测试图，白色背景，少量蓝绿色科技感点缀"
```

For OpenAI-compatible providers:

```bash
picgen create --dry-run --provider openai_proxy --preset fast-draft "一张简洁的 PicGen 测试图，白色背景，少量蓝绿色科技感点缀"
picgen create --yes --provider openai_proxy --preset fast-draft "一张简洁的 PicGen 测试图，白色背景，少量蓝绿色科技感点缀"
```

Present the dry-run preview and ask for confirmation before the real generation unless the user explicitly asked to generate immediately. The first smoke test should generate one image.

## After Provider Success

After one provider is configured and the first smoke test succeeds, tell the user the provider is ready and ask whether they want to add another channel as a fallback. Example:

```text
Gemini 渠道已经配置并测试成功。你还可以继续添加另一个渠道作为备用，例如 OpenAI-compatible。要继续添加吗？
```

If the user says yes, repeat provider setup and smoke testing for the next channel. If the user says no, stop setup and tell them PicGen is ready to use.

## Preferences and Overrides

Treat `picgen create` flags as one-off overrides. They must not change user preferences:

```bash
picgen create --provider gemini_official "<prompt>"
picgen create --model gemini-3-pro-image-preview "<prompt>"
picgen create --preset poster "<prompt>"
picgen create --mode premium "<prompt>"
picgen create --reference ./reference.png "<prompt>"
picgen create --mask ./mask.png --reference ./source.png "<prompt>"
```

Only change defaults when the user explicitly asks to remember a preference, such as "use Gemini by default from now on".

## Output Handling

PicGen normalizes provider responses into local image files. Providers may return URLs, base64, inline bytes, or file references, but the agent should only use PicGen's local paths and metadata.

After generation:

- Show image previews or local paths.
- Do not paste base64, binary image data, or full provider responses into the conversation.
- Do not read or display provider response payloads from metadata unless debugging is explicitly requested.
- Do not automatically read, attach, analyze, or resend generated images.
- Load generated images only when the user asks to inspect, edit, continue from, or compare them.
- When loading is needed, load only the specific referenced image or images.

Do not explain token or context management to ordinary users unless they ask.

PicGen redacts generated image payloads and Gemini thought signatures from metadata, but agents should still treat metadata as diagnostics rather than user-facing content.

## Error Handling

If `doctor` reports no usable provider, configure a provider. Prefer non-interactive setup in agent environments.

If an API key is missing, save it with `picgen key set <ENV_NAME> --clipboard`, `--stdin`, or guide the user to run `picgen setup` when interactive prompts are visible. Name the required environment variable only when useful for debugging.

If a provider is disabled, suggest enabling it or using a one-off provider override.

If the user provides a mask without a reference image, ask for or locate the source/reference image before generating. Masks only make sense together with a source image.

If a provider call fails, show a short error and point to the metadata or error path if available. Do not silently retry with another paid provider unless the user has approved fallback behavior.

## Examples

Explicit:

```text
用 PicGen 生成一张产品发布海报
```

Confirmation:

```text
我可以先用 PicGen 做一次轻量测试生成，默认只出 1 张，确认工具和渠道都可用。要我现在开始吗？
```

Generation preview:

```text
生成预览：
我将使用当前渠道生成 1 张轻量测试图，保存到本地。

确认后开始生成。
```
