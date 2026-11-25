---
name: 'ai-ugc-test-loop'
description: 'Research public AI UGC patterns, score references against the account baseline, test one variable at a time, render one agent-media test take, then finish with real app footage, captions and a UTM publish packet.'
allowed-tools: ['mcp__agent-media__make_ugc', 'mcp__agent-media__quote_ugc', 'mcp__agent-media__generate_video', 'mcp__agent-media__generate_image', 'mcp__agent-media__generate_audio', 'mcp__agent-media__quote', 'mcp__agent-media__list_models', 'mcp__agent-media__get_account', 'mcp__agent-media__list_characters', 'mcp__agent-media__get_run_status', 'mcp__agent-media__upload_image', 'mcp__agent-media__rate_run', 'mcp__agent-media__open_upload_panel', 'mcp__agent-media__get_uploads']
x-skill-slug: 'ai-ugc-test-loop'
x-skill-version: '1.0.1'
---
# AI UGC Test Loop

Run a research-first AI UGC testing loop. Agent Media makes the video take; you handle reference intake, outlier scoring, prompt writing, review, finishing, and the publish packet. This workflow is inspired by public AI UGC workflows in general terms. Do not copy exact scripts, protected likenesses, trademarks, or shots from references.

Use only Agent Media MCP tools that are listed in the user's client. This skill may use `get_account`, `list_models`, `list_characters`, `open_upload_panel`, `get_uploads`, `upload_image`, `quote_ugc`, `make_ugc`, `quote`, `generate_image`, `generate_video`, `generate_audio`, `get_run_status`, and `rate_run`. Missing steps are handled with normal files, local editing, the user's pasted references, and your own analysis. There is no Agent Media scraper, reference analyzer, campaign tool, batch tool, tool that cuts an app screen recording into a take, caption exporter, or publish packet exporter.

## Operating rules

- Research first. Ask for product context, account baseline, and 3 to 10 references before rendering.
- Score references against the account's own baseline. Use `outlier_score = reference_views / account_baseline_views` when both numbers exist.
- Change one variable per test. Good variables are hook, creator type, starting frame, objection, proof moment, offer, and CTA.
- Render one test take first through Agent Media, after quoting it.
- Batch only after the user approves the first take and says to render more variants.
- Finish final variants with a real app screen recording and captions. Do not fake app screens when the user can supply a recording.
- Build a publish packet with final URLs or files, variant IDs, post copy, CTA, thumbnail notes, baseline metric, and UTM links that include `utm_source=skill`.

## 1. Product context

Ask for only what you need:

- Product URL or product name.
- Audience and buyer pain.
- One-sentence promise.
- Main objection.
- Offer and CTA.
- Priority platform or placement.
- Existing account baseline: median views, top 10 percent views, recent post count.
- Assets: logo, product photo, app screen recording, creator photo, saved character, or none.

If browsing is unavailable or the product page is not readable, ask the user to paste page copy or screenshots.

## 2. Reference intake

Ask for 3 to 10 references. Accept links, screenshots, transcripts, captions, rough descriptions, or exported research notes. For each reference, capture label, URL if available, handle if provided, views, account baseline if known, hook, open question, beat sequence, payoff, proof moment, CTA, and risk notes.

Prefer patterns over copying. Keep the inspired-by creative brief general: structure, pacing, proof type, objection, or hook category.

## 3. Outlier scoring

Create a compact table:

`label | URL | views | baseline | outlier score | hook | open question | sequence | payoff | risk | keep?`

When enough data exists, calculate `views / baseline`. If no baseline exists, use a rough tier:

- `5` clear outlier.
- `3` likely above normal.
- `1` unproven.

Pick 3 to 5 winners and explain the pattern each one suggests.

## 4. Test matrix

Create 6 to 10 variants, changing one variable per row.

Use these columns:

`variant_id | reference | variable changed | hook | creator | starting frame | proof | CTA | agent-media input notes`

Label rows with stable IDs such as `A1-hook`, `A2-start-frame`, and `B1-proof`. Pick one row for the first test take and explain why it is the safest first render.

## 5. Starting frame

The first frame should look real: phone framing, normal skin detail, natural hands, believable room or outdoor setting, and no text covering the face. Keep the product or app context visible only when it matters. Name the sound plainly: phone mic, quiet room, street noise, car interior, gym room, or soft room tone.

If the opening needs a still frame, create it with `generate_image` or ask the user for one. Pass it as `first_frame` to `generate_video`. If identity or product consistency matters more than exact first-frame control, use `refs` instead when the selected model requires that mode.

## 6. One Agent Media test take

Before generation, call `get_account`. If `free_first_ad_available` is true, use `quote_ugc` or `quote` to confirm whether the selected first take is free, then ask the user to approve the free watermarked ad. If it is not free, show the quote and ask before spending credits.

Prefer `make_ugc` when the request fits one finished vertical UGC video. Use only needed fields: `script`, one identity source, optional `scene`, optional `product_image`, optional `duration`, optional `captions`, optional `caption_style`, `look`, and `aspect_ratio`.

Use `generate_video` when you need exact first-frame, reference, or model control. Include `prompt`, `seconds`, `aspect`, `audio`, only needed references, optional `quality`, and a fresh `request_id`.

After submission, call `get_run_status` with `wait:true`. Repeat until completed or failed. Give the user the final URL, not only the job id.

## 7. Quality review

Check lips, hands, face drift, product clarity, sound believability, starting frame, hook clarity, payoff, and CTA. Use `rate_run` when available. Give a short verdict:

- `ship`
- `fix then batch`
- `remake first`

Do not auto-remake. Ask what to fix.

## 8. Batch only after approval

Ask: `Do you want me to render the next variants from the matrix now?`

Only batch after the user says yes. Keep variant IDs tied to the matrix. Change one variable per variant. Quote before spending. Poll every run with `get_run_status`.

## 9. Finish with real app screen and captions

Use the user's real app screen recording for the final proof moment. Agent Media does not cut a screen recording into a take. `make_ugc` with `broll_url` (an https video) can overlay one on the lower half while the person narrates, as a paid run; for anything else, finish with local editing when files are available: trim the take, append or overlay the screen recording, add captions from the final transcript, keep title-safe framing, and export 9:16 MP4 files named by variant ID.

If the screen recording path is missing, ask for it or skip that finish step. Do not fake app screens.

## 10. Publish packet

Create a packet with:

- Final file or URL.
- Variant ID.
- Platform or placement.
- Post copy.
- CTA.
- UTM link with `utm_source=skill`.
- Thumbnail note.
- Baseline metric to compare against.
- What changed from the previous test.

Judge each placement against its own account baseline. When a variant wins, recommend remaking it with real creators or production footage.
