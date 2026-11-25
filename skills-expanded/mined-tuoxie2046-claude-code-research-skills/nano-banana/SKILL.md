---
name: nano-banana
description: Generate images from the terminal with Google's nano-banana (Gemini image model) via the Antigravity CLI (`agy`), billed to the signed-in Google account. Use whenever the user asks to create / draw / generate an image, picture, icon, logo, illustration, poster, infographic, or diagram specifically with nano-banana / Gemini / Antigravity — or wants rich, text-heavy infographics. For the OpenAI gpt-image-2 path use the separate `gpt-image` skill instead.
allowed-tools: Bash, Read
---

# nano-banana — image generation via Antigravity (`agy`)

Wraps the `agy` (Google Antigravity) **agent** so Claude Code can generate images with
nano-banana. Unlike a plain CLI, image generation here is an agent tool
(`generate_image`) invoked through natural language — the wrapper builds a strict
instruction, runs `agy -p`, then **verifies the output file actually landed** (with
recovery from agy's `brain/` working dir). Auth is the Google account signed into `agy`.

All commands go through the helper:

```
~/.claude/skills/nano-banana/scripts/nano-banana.sh <check|generate|batch> [args]
```

## Workflow

1. **Preflight once per session:** `nano-banana.sh check`. If it reports no creds /
   auth, the user must run `agy` once interactively to log in (browser OAuth) — you
   cannot do this for them. Token expiry surfaces at generate time as an auth error.
2. **Generate** with an explicit `--output` PNG path. The helper prints
   `IMAGE\t<path>\t<WxH>` on success.
3. **Always `Read` the produced PNG** to view it and verify, then report the path.
4. Iterate by re-running with a refined prompt.

## Commands

Generate (text → PNG):
```bash
~/.claude/skills/nano-banana/scripts/nano-banana.sh generate \
  --prompt "PROMPT TEXT" --output ./out.png
```

Batch (many prompts → many images; one per prompt, continue-on-error, manifest):
```bash
# from a file (one prompt per line; blank lines and # comments skipped)
~/.claude/skills/nano-banana/scripts/nano-banana.sh batch \
  --prompts-file ./prompts.txt --outdir ./renders
# inline / stdin
~/.claude/skills/nano-banana/scripts/nano-banana.sh batch --prompt "a" --prompt "b" --outdir ./out
printf 'one\ntwo\n' | ~/.claude/skills/nano-banana/scripts/nano-banana.sh batch --prompts-file -
```
Name an output by prefixing a line with `stem<TAB>prompt` (else `001.png`, …).
Default `--outdir` is `./nb-batch-<timestamp>/`; read `<outdir>/manifest.tsv` for the
stem→status→path→prompt map. Per-image failures are recorded and skipped, but an
**auth failure aborts the whole batch** (no point retrying every prompt against dead
auth) — re-login with `agy` and re-run.

## How it works / behaviors

- Underlying tool is `generate_image` (nano-banana is the model). There is **no
  `agy image` subcommand** — the agent calls the tool from the prompt.
- The agent generates a **JPEG into `~/.gemini/antigravity-cli/brain/<conv-id>/`**, then
  converts to PNG at your `--output`. The wrapper forces an absolute path and, if the
  agent doesn't save there, recovers the newest brain image and converts it via `sips`.
- Output paths are absolutized (agy resets cwd). Parent dirs are created.
- One retry on a no-file result; auth/eligibility errors fail fast with guidance.
- **Non-destructive:** success requires the output file to actually change this run
  (checked via its inode:mtime:size), so a pre-existing/stale file is never reported as a
  fresh result and is **not deleted** if generation fails.

## ⚠️ Safety

This path drives an **autonomous agent** (`agy -p … --dangerously-skip-permissions`):
tool calls and file writes are auto-approved. A prompt is therefore not just image text —
a malicious or careless prompt could instruct the agent to run other tools or touch other
files. **Only pass trusted prompt text** (and trusted `--prompts-file` contents). For the
non-agent, capability-scoped path, prefer the `gpt-image` skill.

## Strengths & limitations (vs gpt-image-2)

- **Strengths:** excellent in-image **text rendering**; tends to produce rich, fully
  fleshed-out infographics (adds detail, gradients, sub-labels). Great for posters and
  content-heavy diagrams; strong at consistent image **editing** (via prompt + a file path).
- **Limitations:**
  - **No precise size control** through the agent — it returns its own dimensions
    (often ~16:9). If you need an exact size, post-process with `sips -z H W`.
  - **Slower** than gpt-image-2 (it's an agent turn: tool call + format convert).
  - **Tends to elaborate** — if you want strictly minimal output, say "minimal, no
    extra text, exactly three boxes" etc.
  - Needs a live `agy` login; tokens expire and require interactive re-auth.

## Troubleshooting

- `agy ... not found` → install Antigravity (https://antigravity.google) or ensure
  `~/.local/bin` is on PATH.
- auth / `IneligibleTier` / "Authentication required" → run `agy` once interactively to
  log in; the standalone `gemini` CLI is not usable on free-tier accounts.
- No file produced → check stderr for the agy transcript; re-run (one retry is automatic).
