---
name: opencode-reilabs-provider
description: Install the Rei Labs (reilabs) custom provider into the user's OpenCode config so that rei-qwen3-coder, rei-coder-lite, rei-coder-pro, and rei-coder-max become available. Use when the user asks to add, enable, or install Rei Labs models, the reilabs provider, or coder.reilabs.org in OpenCode.
---

# Install the Rei Labs provider for OpenCode

Add a `reilabs` entry under `provider` in the user's OpenCode config so the four Rei Labs coder models are selectable. The provider uses the OpenAI-compatible adapter pointed at `https://coder.reilabs.org/v1`.

This skill supports Linux, macOS, and Windows (including WSL).

## Canonical provider block

This is the exact block to merge under `provider` in `opencode.json`:

```json
"reilabs": {
  "npm": "@ai-sdk/openai-compatible",
  "name": "Rei Labs",
  "options": {
    "baseURL": "https://coder.reilabs.org/v1"
  },
  "models": {
    "rei-qwen3-coder": { "name": "Rei Qwen3 Coder" },
    "rei-coder-lite":  { "name": "Rei Coder Lite" },
    "rei-coder-pro":   { "name": "Rei Coder Pro" },
    "rei-coder-max":   { "name": "Rei Coder Max" }
  }
}
```

## Procedure

1. **Pick the target config file.**
   - Default global path by platform:
     - Linux/macOS: `~/.config/opencode/opencode.json`
     - Windows (native): `%USERPROFILE%\.config\opencode\opencode.json`
     - Windows (WSL, recommended by OpenCode docs): `~/.config/opencode/opencode.json` inside the WSL distro
   - If a project-local `./opencode.json` exists in the cwd, ask the user which one to edit.
   - If neither exists, create the global file with minimal scaffold: `{ "$schema": "https://opencode.ai/config.json", "provider": {} }`.

2. **Read and parse the file as JSON.** Keep an in-memory copy of the original text so you can restore it if the write fails validation.

3. **Merge, do not replace.** Insert the canonical block as `provider.reilabs`. Preserve every other top-level key and every other provider already under `provider` (for example, an existing `openrouter` entry must remain untouched).

4. **Idempotency.**
   - If `provider.reilabs` is absent, add it.
   - If present and deep-equal to the canonical block, report "already installed, no changes" and stop.
   - If present but different, show the user a diff between current and canonical, and ask before overwriting.

5. **Write the file** with 2-space indentation and a trailing newline, matching typical `opencode.json` style.

6. **Validate.** Re-parse the written file. If parsing fails, restore the pre-write text and report the error; do not leave a broken config.

7. **Report.** Print the final list of provider keys and call out the four newly available models:
   - `reilabs/rei-qwen3-coder` — Rei Qwen3 Coder
   - `reilabs/rei-coder-lite` — Rei Coder Lite
   - `reilabs/rei-coder-pro` — Rei Coder Pro
   - `reilabs/rei-coder-max` — Rei Coder Max

## API key

Do not handle API keys. After the provider is installed, the user runs `/connect` inside OpenCode, selects "Rei Labs", and OpenCode prompts for the key directly. Tell the user this as the final step.

## Out of scope

- Do not modify `model` defaults, agent bindings, or any unrelated provider.
- Do not install npm packages; OpenCode resolves `@ai-sdk/openai-compatible` on demand.
- Do not create a backup file unless the user asks — the pre-write in-memory copy is sufficient for rollback within this run.
