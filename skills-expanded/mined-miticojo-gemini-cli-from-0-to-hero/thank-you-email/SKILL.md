---
name: thank-you-email
description: "Composes and drafts a post-workshop thank-you Gmail message with a Nano Banana hero image whose visual mood is driven by the sentiment-insight agent output. Triggers on: send thanks email, post-workshop email, feedback follow-up, attendee thank-you, workshop closing email, mood-aware email, mail with hero image, post-event mail."
---

# Thank-You Email Composer

You orchestrate three steps in order:

1. **Resolve mood** — read the sentiment-insight agent output `{ mood, themes, summary }`.
2. **Generate hero image** via `mcp_nanobanana_generate` using the style cue mapped from `mood` (see table). Save to `functions/email-assets/hero-{workshopId}-{mood}.jpg`.
3. **Draft Gmail message** via Workspace MCP (`gmail_drafts_create`) with HTML body, inline image reference, and recipient batch.

## Mood → style cue

| mood | style cue |
|---|---|
| positive | bright warm palette, celebratory composition, soft confetti, modern editorial style |
| mixed | balanced palette, neutral composition, editorial flat illustration |
| constructive | cool palette, focused composition, clean lines, minimal |
| negative | soft empathetic palette, calm composition, abstract shapes, muted |

## Email template (HTML, inline)

```html
<!doctype html>
<html lang="en">
  <body style="font-family: -apple-system, system-ui, sans-serif; max-width: 640px; margin: 0 auto; padding: 24px;">
    <img src="cid:hero" alt="{{workshopName}} hero" style="width:100%; border-radius:12px;" />
    <h1 style="margin-top:24px;">Thanks for joining {{workshopName}}.</h1>
    <p>{{summary}}</p>
    <p>Top themes: {{themes}}.</p>
    <p>— {{adminName}}</p>
  </body>
</html>
```

## Inputs the skill expects

- `workshopId`, `workshopName`, `workshopDate`, `adminName`.
- Sentiment object from agent: `{ mood, themes[], summary }`.
- Recipient list (array of email strings).

## Rules

- Never send emails directly; always create a Gmail **draft** (`gmail_drafts_create`).
- Cache hero image by `(workshopId, mood)`; reuse if exists.
- Never include attendee PII in the body beyond first name when available.
- If `NANOBANANA_API_KEY` is missing, fall back to `assets/hero-fallback.jpg` and warn.

## See also

- `references/copy-tones.md` — body copy variants per mood.
- `scripts/build_mime.py` — utility to assemble multipart MIME with inline image.
