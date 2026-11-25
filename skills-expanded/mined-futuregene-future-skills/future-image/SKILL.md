---
version: 1.2.0
name: future-image
description: >
  Generate images from text, edit supplied images, and analyze images or screenshots
  for OCR and visual questions using Future CLI tools. Use for drawing, image editing,
  visual inspection and chart reading within the user's data and resource permissions.
allowed-tools: Bash(future:*)
category: tools
---

# Images

Use the Future CLI for generation, editing and visual analysis. It handles authentication;
never seek, print or embed API keys. Consult `future tools describe <tool>` for actual
size/quality support. Historical provider errors or latency are not permanent capabilities.

## Tools

```bash
future tools call image_gen --prompt "A red fox in an autumn forest" --size "1024x1024" --quality medium --output ./output.png --timeout 600
future tools call image_edit --input /path/to/photo.png --prompt "Convert to watercolor" --output ./edited.png --timeout 600
future tools call image_edit --input /path/to/photo.png --mask /path/to/mask.png --prompt "Replace the masked background" --output ./edited.png --timeout 600
future tools call read_image --input /path/to/photo.png --question "Transcribe the visible text and state uncertain characters"
```

- `image_gen`: prompt, size, quality, n, output_format and output path.
- `image_edit`: source `--input`, optional `--mask`, prompt and output parameters.
- `read_image`: `--input`, `--question`, optional `--mime_type` and `--max_tokens`.

Always use `--input`/`--mask` for files; the CLI encodes them. Avoid putting file bytes
or huge prompts in argv. For long prompts use `--stdin` with JSON; on the detected
platform use suitable stdin syntax or Python `subprocess.run(..., input=json_text)`.
Do not assume POSIX heredocs work in PowerShell.

## Execution contract

Reuse the requested subject, language, style, output format/count and quality. Ask only
about missing decisions that materially affect the result. Do not silently change a
user-pinned quality setting or generate extra paid variants beyond the authorized scope.
`medium` is a reasonable default when unspecified; actual behavior varies by backend.

Source images/masks and visual questions are sent to a remote service. Respect private,
offline and sensitive-image restrictions; ask about an unresolved upload boundary before
sending the file. Preserve supplied originals and distinguish edits from generated substitutes.

For generation/editing, a 600-second CLI HTTP allowance is a useful starting point, not a
runtime guarantee. Set the enclosing shell allowance longer (for example 660 seconds for
one call) to cover CLI startup and saving. Multiple sequential calls need a combined
allowance or separate bounded tool calls. Read-image latency also varies; use an explicit
allowance when necessary rather than assuming it can never time out.

## Verification

Check that the requested output file was actually saved and is a readable image. For
important visible text, charts or scientific material, inspect the final image against
source strings/values and report uncertain characters or visual errors. Generative charts
and illustrations are not measurements. Do not claim perfect OCR or factual correctness
based only on a successful tool exit. Use a distinct revision filename when fixing a result.

For multiple requested outputs, the CLI may suffix filenames; inspect returned paths and
report the actual count. Do not overwrite unrelated images.

## Error handling and retries

Read the actual error before acting:

| Error | Response |
|---|---|
| 401 / unauthorized | Explain missing/expired authorization; ask the user to log in, never launch login unprompted |
| 403 / model access denied | Report access denial; do not assume re-login repairs server-side permissions |
| insufficient credit | Report the balance limitation; do not create a payment or retry blindly |
| invalid size/arguments | Check the current tool schema and correct within the user's contract |
| 429 | Respect retry guidance within the authorized retry/resource allowance |
| transport failure / CLI timeout / aborted | Completion and billing may be uncertain; inspect any receipt/status before retrying |

A local process timeout does **not** prove the remote operation stopped. Do not automatically
resubmit uncertain paid calls or interpret repeated retries as new budget authorization.
If no status lookup is supported, disclose the uncertainty and ask before extending retries.
Quality changes are proposals when they alter the user's requirements, not automatic repairs.
