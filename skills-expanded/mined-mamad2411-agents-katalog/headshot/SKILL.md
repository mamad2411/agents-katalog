---
name: headshot
description: |
  Generate a studio-quality professional headshot from any selfie or portrait
  photo. One command, ~10 seconds, ~$0.12. Uses GPT Image 2 image-to-image
  edit via the BlockRun MCP plugin (x402 USDC on Base). Five styles: corporate,
  creative, startup, actor, linkedin-2025 (--all renders the four core styles).
triggers:
  - "professional headshot"
  - "linkedin photo"
  - "profile picture"
  - "headshot"
  - "portrait photo"
  - "make me look professional"
  - "corporate photo"
  - "founder photo"
  - "actor headshot"
  - "business photo"
  - "startup headshot"
user-invocable: true
allowed-tools: mcp__blockrun__blockrun_image, mcp__blockrun__blockrun_wallet, Bash(curl:*), Bash(mkdir:*), Bash(date:*), Bash(file:*), Bash(base64:*), Read, Write
---

# `/headshot` — Studio-quality professional photo in ~10 seconds

Turns any selfie or candid photo into a polished headshot suitable for
LinkedIn, a company website, a casting submission, or a press kit. The
person's identity is preserved — only wardrobe, lighting, and background
are restyled.

## What this skill does

Reads the user's input photo, picks a style from the **Style variants**
section below, calls `mcp__blockrun__blockrun_image` with `action="edit"`
and `model="openai/gpt-image-2"`, then downloads the result to
`./blockrun-out/{ts}-headshot/headshot.png`.

## Inputs

| Input | Required | Default | Notes |
|---|---|---|---|
| `image` (path or URL) | yes | — | A photo containing the person. JPG / PNG / HEIC / WebP. |
| `style` | no | `corporate` | One of `corporate`, `creative`, `startup`, `actor`, `linkedin-2025`, or `all` for a 4-pack. |
| `output_dir` | no | `./blockrun-out/{ts}-headshot/` | Override with `BLOCKRUN_OUT_DIR` env var if set. |

If the user only says "make me a headshot" without attaching a photo, ask
for the photo path before proceeding.

## Workflow (Claude executes this strictly in order)

### Step 0 — Verify the BlockRun MCP server is registered

Before any tool call, confirm `mcp__blockrun__blockrun_wallet` is
available. If it is not (the user has not registered the MCP server
yet), the entire skill cannot run — surface a clear install message
and stop:

> "The BlockRun MCP server isn't registered with Claude Code yet, so
> `/headshot` can't run. Please run **once**:
>
> ```
> claude mcp add blockrun -s user -- npx -y @blockrun/mcp@latest
> ```
>
> Then restart Claude Code and try `/headshot` again. (Full install
> guide: `INSTALL.md` in the Claude Code-GPT-IMAGE2-SeeDance-BlockRun bundle.)"

Do not attempt the wallet preflight or the image call if the MCP tools
are missing.

### Step 1 — Wallet preflight

Call `mcp__blockrun__blockrun_wallet` with `{"action": "status"}`.

- If the response shows a balance below **$0.20 USDC** (single style) or
  **$0.60 USDC** (`--all` 4-pack), pause and tell the user:
  > "Your BlockRun wallet balance is too low. Run `blockrun_wallet action: setup`
  > to top up Base USDC. /headshot needs ~$0.12 per style."
  Do not proceed.

- If balance is fine, continue.

- If the response indicates `No wallet found`, run
  `mcp__blockrun__blockrun_wallet` with `{"action": "setup"}` and walk the
  user through the QR-code top-up flow before retrying.

### Step 2 — Prepare prompt

Use the master template from the **Style variants** section at the
bottom of this file. Pick the block matching `{style}` (default
`corporate`) and substitute its `{background}`, `{lighting}`, `{wardrobe}`
slots into the master template.

### Step 3 — Prepare the input image

The MCP `image` parameter accepts either a URL or a base64 data URI.

- If the user gave a URL: pass it through.
- If the user gave a local path:
  1. Verify the file exists with `Read`.
  2. `file --mime-type` to confirm it's `image/*`.
  3. Encode: `base64 -i <path>` (macOS) or `base64 -w0 <path>` (Linux).
  4. Build the data URI: `data:<mime>;base64,<b64>`.

If the file is over ~5 MB, warn the user that uploads may be slow and
recommend resizing first.

### Step 4 — Call BlockRun MCP

```
Tool: mcp__blockrun__blockrun_image
Arguments:
{
  "prompt": "<filled template from Step 2>",
  "action": "edit",
  "model": "openai/gpt-image-2",
  "image": "<URL or data-URI from Step 3>",
  "size": "1024x1024",
  "quality": "hd"
}
```

The tool returns synchronously (no polling). Expect ~5–15 seconds.

If `--all` was passed, run Step 4 four times in series with each style,
saving each result with a `-{style}` suffix.

### Step 5 — Download and save

1. Compute timestamp: `date -u +"%Y-%m-%dT%H%M%SZ"`.
2. Determine output dir: `${BLOCKRUN_OUT_DIR:-./blockrun-out}/{ts}-headshot/`.
3. `mkdir -p` the dir.
4. Read `response.structuredContent.url` from the tool result.
5. `curl -sSL "<url>" -o <out_dir>/headshot.png` (or `headshot-<style>.png` per variant).
6. Confirm the file is non-empty (`ls -la`).

### Step 6 — Report to user

Output exactly:

```
✅ Headshot ready

  File:   {relative path}
  Style:  {style}
  Model:  openai/gpt-image-2 (HD)
  Cost:   ~$0.12 (settled on Base via x402)

Open it: open {relative path}
```

For `--all`, list all four files and note total cost ~$0.48.

## Failure handling

| Error pattern | Action |
|---|---|
| Tool `isError: true` with text containing `payment` or `balance` | Show: "Wallet balance too low. Run `blockrun_wallet action: setup` to top up." Do NOT retry. |
| Text contains `content filter` or `safety` or `invalid request` | Apply the "Looks like a different person" retry addendum from the **Common pitfalls + auto-retry templates** section below and retry once. If it fails again, tell the user the source photo may have triggered a filter. |
| Network timeout / `fetch failed` | Retry once after 5s. If still failing, surface the error verbatim. |
| `No wallet found` | Walk through `blockrun_wallet action: setup`, then retry. |

## Cost

- Single style: ~$0.12 (gpt-image-2 HD 1024×1024)
- `--all` 4-pack: ~$0.48
- Settled on Base USDC via x402; no charge if the call fails before completion.

## Examples (paste these into Claude Code)

```
/headshot ./me.jpg
/headshot ./me.jpg --style startup
/headshot ./me.jpg --style actor
/headshot ./me.jpg --all
/headshot https://example.com/photo.jpg --style linkedin-2025
```

---

## Master template

> Used by Step 2 above. Default `{style}` is `corporate` if the user
> doesn't say. Default `{wardrobe}` is derived from style.

```
Transform the person in this image into a professional headshot.

Maintain facial features, skin tone, hair color, and identity exactly as in
the source image — only restyle environment, lighting, and wardrobe.

Background: {background}
Lighting: {lighting}
Wardrobe: {wardrobe}
Composition: head-and-shoulders crop, eyes at upper third, slight three-quarter
turn, looking just past camera, gentle natural smile.

Render at high resolution with sharp focus on the eyes, soft skin retouching
that preserves pores and natural texture (do NOT smooth into plastic),
neutral white balance, suitable for LinkedIn or a corporate website.

Do not add text, watermarks, logos, or borders. Do not change the person's
ethnicity, age, gender, or facial structure.
```

## Style variants

Pick one of these by `--style` (or ask the user if unset).

### `corporate` (default — investment-bank / consulting / law-firm vibe)

```
{background}: smooth charcoal-to-graphite gradient, soft vignette
{lighting}: butterfly key with subtle fill, hint of rim light from camera-left
{wardrobe}: tailored navy suit jacket, crisp white shirt, no tie OR a single
            understated dark tie; minimalist accessories only
```

### `creative` (designer / writer / agency creative director)

```
{background}: warm neutral wall (oat / clay / sage), shallow depth of field
{lighting}: soft window light from camera-left, golden-hour warmth
{wardrobe}: well-fitted casual blazer over a fine-knit crewneck OR a
            high-quality oversized denim shirt; one tasteful watch or ring
```

### `startup` (founder / engineer / PM — modern tech aesthetic)

```
{background}: out-of-focus modern workspace (concrete + warm wood tones) OR
              clean off-white seamless paper
{lighting}: bright diffused daylight, slight cool tone, no harsh shadows
{wardrobe}: high-quality plain crew tee in navy / charcoal / cream, OR a
            zip-up technical sweater; no logos
```

### `actor` (headshot for casting / talent agencies)

```
{background}: solid neutral grey or muted teal seamless paper
{lighting}: clamshell lighting (large soft key + reflector fill), eyes catch
            two clear specular highlights
{wardrobe}: solid-color simple top in a hue that complements skin tone, no
            patterns, no jewelry, no collar that distracts from face
```

### `linkedin-2025` (the "I just got promoted" vibe — slightly aspirational)

```
{background}: slightly out-of-focus modern office or warm-tone neutral wall
{lighting}: warm Rembrandt-style key with soft fill, faint rim from behind
{wardrobe}: structured blazer over a knit tee OR a polished button-down with
            top button open; sleeves clean, posture confident-but-relaxed
```

## Common pitfalls + auto-retry templates

If the first response shows any of these, retry with the matching addendum
appended to the prompt.

### "Looks like a different person"

Append:
```
CRITICAL: this is an image-to-image edit, NOT a re-imagining. Preserve the
exact facial geometry of the source: eye spacing, nose bridge, jawline,
hairline, and skin tone must match the source 1:1. Treat this as a
"clothing + lighting + background" swap only.
```

### "Too plastic / over-retouched"

Append:
```
Skin must show natural texture: pores, faint stubble or peach fuzz where
applicable, soft tonal variation. Avoid the "AI plastic" smoothness — aim
for the polish of a Hasselblad medium-format portrait, not a beauty filter.
```

### "Wrong wardrobe / colors clashing"

Append:
```
Wardrobe color must complement the source's skin undertone. If the source
appears to be {warm/cool/neutral}-toned, choose {complementary palette}.
Avoid pure black and pure white if they fight the skin tone.
```
