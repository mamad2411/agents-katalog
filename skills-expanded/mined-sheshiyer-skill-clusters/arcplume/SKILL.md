---
name: arcplume
description: "Arcplume runs Grok through the Grok Build CLI's own OAuth-authenticated session (grok login) for image generation, with strict preflight validation, secret-safe handling, and headless CLI-driven execution -- no separate XAI_API_KEY billing. Video falls back to the billed xAI API. USE WHEN a user wants to generate an image via a locally logged-in Grok Build CLI session, e.g. 'generate an image with grok', 'use grok build', or 'use my logged-in grok session'."
cluster: media-gen
version: 1.1.0
origin: "craft-agent workspace"
displayName: "🪽 Arcplume — Grok Build CLI Session"
emoji: "🪽"
homepage: https://skills.sh
license: MIT
---

# 🪽 Arcplume — Grok Build CLI Session

Use this skill when the user explicitly wants **Grok via the locally authenticated Grok Build CLI session** and CLI-driven execution.

## When to trigger

Trigger on prompts like:
- "use grok build to generate an image"
- "generate an image with grok"
- "run the grok CLI"
- "use my logged-in grok session"

Do **not** auto-trigger for generic “use Grok API” requests unless the user asks for the CLI/logged-in-session mode.

## Default behavior

1. Validate local prerequisites (`grok` available)
2. Verify the session is logged in (`scripts/preflight.sh`)
3. Execute via **CLI-driven headless image generation** path
4. Keep outputs concise and never expose secrets

## Auth resolution order (strict)

1. Check the `grok` binary is present on `PATH`
2. Check that a logged-in session exists (Grok Build CLI manages its own OAuth tokens; this skill does not resolve or read any env vars or cookie files)

If either check fails, stop and return a precise remediation message.

## Mandatory preflight (must pass)

```bash
command -v grok && grok --version
```

```bash
bash scripts/preflight.sh
```

If preflight fails, do not attempt Grok execution. Explain exactly which layer failed:
- binary missing
- session not logged in
- session invalid/expired

## Execution path

### Primary: CLI-driven headless image generation (recommended)

Drive the already-authenticated `grok` binary directly:
1. Run `scripts/generate-image.sh --prompt "<text>" --out "<path>"` (optional `--max-turns`)
2. This invokes `grok` headlessly (single-turn, JSON output) with a system-prompt override that forces use of Grok's real built-in image-generation tool, not a hand-drawn approximation
3. The script locates the resulting image file and copies it to the requested `--out` path
4. Return the resolved output path + a brief summary

This path is default because it relies on the CLI's own maintained OAuth session rather than any credential this skill would otherwise have to manage.

### Optional: API mode (explicit opt-in only)

If and only if user asks for API mode, or asks for **video** (Grok Build's own OAuth
session does not expose a native video-generation tool — confirmed by live testing:
asking it to generate video with no workarounds allowed returns an explicit "no
built-in video-generation tool available here" answer):
- Use `XAI_API_KEY`
- Call `api.x.ai`
- For video: run `scripts/generate-video.sh --prompt "<text>" --out "<path.mp4>"`
  (optional `--duration`, `--model`, `--timeout`); it wraps the same
  `api.x.ai/v1/videos/generations` endpoint `scripts/doctor.sh` and
  `scripts/test-video.sh` already exercise, in this skill's standard
  `--prompt`/`--out` interface
- Clearly mark output as **API mode**, not CLI-session mode

## Hard constraints

- Never print or log the contents of `~/.grok/auth.json`, or any API keys
- Never dump the raw JSON response from a headless `grok` call — only the resolved output path should ever be printed
- Never persist secrets to files
- Never silently switch from CLI-session mode to API mode
- Never rewrite user prompt without user permission
- For state-changing actions, show draft and request confirmation first

## Fast diagnostics snippets

```bash
# presence check only (safe)
command -v grok >/dev/null 2>&1 && echo "grok: found ($(grok --version))" || echo "grok: missing"

# full diagnostic (binary + session + one real end-to-end test generation)
bash scripts/doctor-cli.sh
```

## Failure messaging template

Use this style:
- **Failed at:** session validation
- **Reason:** `scripts/preflight.sh` reported the Grok Build CLI session is not logged in
- **Fix:** run `grok login --oauth` (interactive) or `grok login --device-auth` (headless/remote), then retry

## Security posture

- Principle of least exposure: only test what is required
- Output redaction by default
- Deterministic preflight before runtime actions
- No destructive action without explicit confirmation
