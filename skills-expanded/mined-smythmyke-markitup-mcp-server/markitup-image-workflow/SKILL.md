---
name: markitup-image-workflow
description: >-
  Use when the user wants to edit or polish an image in chat with the MarkItUp
  connector — remove a background, upscale/enhance, add labeled callouts to a
  screenshot, outpaint/reframe to a new aspect ratio, or turn a screenshot into
  a marketing visual. Guides correct image input (public URL or the MarkItUp
  upload link for local files), tool choice, and credit-aware usage.
---

# MarkItUp image workflow

MarkItUp edits images on its own servers via the connected MCP tools. This skill
helps you pick the right tool and get the image into it correctly.

## Getting the image in (do this first)
MarkItUp tools accept an image as a **public `image_url`** or an **`upload_id`** —
never inline image bytes (they get corrupted in transit).

- **The user gave a public image URL** → pass it directly as `image_url`.
- **The user has a local / uploaded / pasted image (no URL)** → call
  `markitup_request_upload`, give the user the returned **`browser_url`** to drop
  their file (or PUT the bytes to `put_url` if you can run HTTP from a sandbox),
  poll `markitup_check_upload` until status is `uploaded`, then call the editing
  tool with the returned **`upload_id`**. Do not decline or fall back to a
  non-MarkItUp tool.

## Choosing the tool
- **Remove a background** → `markitup_remove_background` (transparent PNG).
- **Make it bigger / sharper / print-ready** → `markitup_upscale` (2×/3×/4×).
- **Point things out on a screenshot** (tutorials, bug reports, UX feedback) →
  `markitup_annotate` with a `context` describing what to box/arrow/highlight.
- **Change aspect ratio / extend the canvas** (e.g. square → 16:9 banner) →
  `markitup_extend` with the target aspect ratio + pixel dimensions.
- **Turn a screenshot into a polished marketing visual** → `markitup_generate`
  with a `description` and a `template_id` (e.g. `bold_marketing`,
  `clean_minimal`, `glassmorphic`, `dark_professional`, `documentation`). To
  redo one variation consistently, use `markitup_regen` with the prior
  `text_analysis`.

## Presenting results
Each tool returns a hosted full-resolution URL plus a small inline preview.
Show the user the result inline as a markdown image and include the download link.

## Credits (be transparent)
- Check with `markitup_credit_balance`. New accounts get free credits.
- `remove_background`, `upscale`, `annotate`, `regen` = 1 credit each
  (`remove_background` and `upscale` are free for active subscribers).
- `generate` = 2 credits at 1K (default), 3 at 2K, 4 at 4K.
- `extend` = 1 credit (2 at 2K/4K).
- `request_upload`, `check_upload`, `credit_balance` are free.
If the user is low on credits, say so before running a paid tool.
