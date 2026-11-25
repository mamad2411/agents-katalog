---
name: ad-creative-edit
description: When the user wants to edit an existing Appeeky-generated ad creative with natural language instructions. Use when the user mentions "edit ad creative", "change background", "bigger headline", "iterate on ad image", "tweak the ad", or mode edit for app ad creatives. For fresh angles see meta-ad-creative. For publishing see ad-creative-to-meta.
metadata:
  version: 1.0.0
---

# Ad Creative Edit (Iterate)

Iterate on a previous Appeeky-generated ad using `mode: edit`. Use edits for **incremental improvements** on a winning or near-winning concept. Use fresh `mode: generate` for new angles, presets, or formats.

Editing is cheaper than guessing. Winners get A′/B′ variations; losers get retired, not endlessly patched.

## When to Edit vs Re-Generate

| Situation | Use edit | Use generate |
|-----------|----------|--------------|
| Bigger headline / font size | ✅ | |
| Background color / contrast | ✅ | |
| Minor layout tweak | ✅ | |
| Localize on-image text | ✅ | |
| New hook / new angle | | ✅ |
| Different preset (UGC → split) | | ✅ |
| Structural format change | | ✅ |
| Failed concept (low CTR + low CPA) | | ✅ new variant |

## Prerequisites

| Input | Source |
|-------|--------|
| `previous_ad` object | `get_app_ad_creative_job` → `result.ad` |
| Same `app_url` | Original generation |
| Specific `edit_instruction` | User request — must be concrete |
| Optional `key_points` | Preserved from analyze step |

### previous_ad Fields (API result object, camelCase)

```json
{
  "style": "ugc",
  "imagePreset": "person_holding_phone",
  "creativeHeadline": "Plan your week in 5 min",
  "creativeSubhead": "The focus app that sticks",
  "imageUrl": "https://..."
}
```

If user has no job ID, reconstruct from Ads Manager export or screenshot description — quality drops without `imageUrl`.

## Edit Instruction Framework

Good instructions are **specific, visual, and bounded**.

### Instruction Template

```
Change [element] to [target state].
Keep [what must not change].
```

### Examples

| Quality | Instruction |
|---------|-------------|
| ✅ Good | "Make the on-image headline 30% larger, bold white text on navy background. Keep phone mockup position unchanged." |
| ✅ Good | "Switch background from gradient to solid charcoal. Increase contrast on subhead." |
| ✅ Good | "Translate on-image text to German. Keep layout identical." |
| ❌ Bad | "Make it better" |
| ❌ Bad | "More professional" (too vague) |
| ❌ Bad | "Copy competitor X" (use teardown + generate) |

## Workflow

### Step 1 — Load Previous Creative

```
get_app_ad_creative_job
  job_id: "<original-job-id>"
```

Extract `result.ad` for `previous_ad`. Show user current image + copy before editing.

### Step 2 — Clarify Instruction

If user request is vague, offer 2–3 concrete options:

```
Option A: Dark background + larger headline
Option B: Minimal white background, smaller subhead
Option C: Re-generate with professional preset (new job)
```

### Step 3 — Call Edit API

**MCP:**
```
generate_app_ad_creative
  app_url: "https://apps.apple.com/us/app/id123456789"
  mode: "edit"
  edit_instruction: "Make headline bigger, navy background, more contrast on CTA text"
  previous_ad: {
    "style": "ugc",
    "imagePreset": "person_holding_phone",
    "creativeHeadline": "Plan your week in 5 min",
    "creativeSubhead": "The focus app that sticks",
    "imageUrl": "https://..."
  }
  quality: "medium"
```

**REST:**
```bash
POST /v1/app-ad-creatives/generate

{
  "appUrl": "https://apps.apple.com/us/app/id123456789",
  "mode": "edit",
  "editInstruction": "Make headline bigger, navy background, more contrast",
  "previousAd": { ... },
  "quality": "medium"
}
```

### Step 4 — Poll Job

```
get_app_ad_creative_job
  job_id: "<new-job-id>"
```

Poll every 3–5 seconds until `completed` or `failed`.

### Step 5 — Present Before / After

Use output template. Ask user to pick version for Meta upload.

## Edit Patterns That Work

| Request | Typical result | Notes |
|---------|----------------|-------|
| Bigger headline | Larger type, same layout | Specify % or "dominant" |
| Navy / dark background | Higher contrast | Good for feed thumb-stopping |
| More minimal | Reduced clutter | May remove decorative elements |
| Brighter / warmer | Lifestyle feel | Pairs with `lifestyle` style |
| Localize text | Translated on-image copy | Specify language code |
| Show different screenshot | Partial change | May need MCP `extra_screenshot_urls` (REST `extraScreenshotUrls`) + generate |
| Add rating stars | Social proof overlay | Only if accurate per listing |

## Edit Patterns That Fail

| Request | Why | Alternative |
|---------|-----|-------------|
| "Make it viral" | Not a visual parameter | New angle via generate |
| Change aspect ratio | API outputs 1024×1024 | Crop in design tool |
| Add video motion | Static API | `tiktok-creative-strategy` |
| Copy exact competitor layout | IP/policy risk | Teardown-inspired generate |
| Fix fundamentally weak hook | Copy problem | New `angle` in generate |

## Winner Iteration Playbook (A′ / B′)

After `meta-campaign-audit` identifies a winner:

| Iteration | edit_instruction focus | Goal |
|-----------|----------------------|------|
| A′ hook | Change on-image headline text only | Isolate hook |
| A′ visual | Background / contrast tweak | CTR lift |
| A′ proof | Add rating or user count | CVR lift |
| A′ localize | Translate for EU geo test | Geo expansion |

**Rule:** One change per edit job. Multi-variable edits obscure what worked.

```
# Winner A′ — hook tweak only
generate_app_ad_creative
  app_url: "https://apps.apple.com/us/app/id123456789"
  mode: "edit"
  edit_instruction: "Change headline to 'Stop juggling 4 apps.' Keep all visual styling identical."
  previous_ad: { ...winner A... }
```

## Copy-Only Refresh

If image is fine but Meta copy underperforms:

```
generate_app_ad_creative
  app_url: "https://apps.apple.com/us/app/id123456789"
  mode: "analyze"
  generate_image: false
  angle: "new hook: outcome-first for busy parents"
```

Then manually update Ads Manager text — or re-generate image if on-image text must match.

## Credit Costs

| Quality | Creative credits |
|---------|------------------|
| `low` | 1 |
| `medium` | 2 |
| `high` | 5 |

Same as generate. Inform user before each edit round.

**Typical iteration session:** 2–3 edits × medium = 4–6 creative credits.

## Output Template

```markdown
# Ad Creative Edit — [App Name]

## Edit Request
"[user instruction]"

## Before
- **Image:** [previous imageUrl]
- **Headline:** [previous creativeHeadline]
- **Subhead:** [previous creativeSubhead]
- **Primary text:** [previous copy.primaryText]

## After
- **Image:** [new imageUrl]
- **Headline:** [new creativeHeadline]
- **Subhead:** [new creativeSubhead]
- **Primary text:** [new copy.primaryText]

## Copy Changes (if any)
| Field | Before | After |
|-------|--------|-------|
| Primary text | | |
| Headline | | |

## Recommendation
- [ ] Ship to Meta (replace ad or new ad in same set)
- [ ] Edit again (specify next change)
- [ ] Re-generate fresh angle

## Meta Action
- Replace creative: upload new image → new ad OR swap in ad-creative-to-meta pipeline
- Keep loser paused — do not delete (learning history)
```

## Meta Upload After Edit

Edited image must be re-uploaded to Meta:

```
meta_ads_upload_ad_image_from_url
  ad_account_id: "act_xxx"
  image_url: "<new imageUrl from edit result>"
```

Then create new ad with new `imageHash` — see `ad-creative-to-meta`. Pausing old ad preserves audit trail.

## Benchmarks (edit impact)

| Metric | Expectation |
|--------|-------------|
| CTR lift from contrast edit | +10–25% if original was low contrast |
| CTR lift from hook-only edit | +15–40% if new hook stronger |
| CPA change | Follows CTR × CVR — measure 48h |
| Diminishing returns | After 3 edits, re-generate new angle |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Editing losers instead of killing | Pause at 2× CPA; edit winners only |
| Stacking 5 edits on one ad | One variable per edit |
| No `imageUrl` in previous_ad | Always save job results |
| Editing without audit data | Let data pick the winner first |
| Same primary text, new image only | Align on-image and feed copy |

## Pre-Edit Checklist

```
- [ ] Original job_id and previous_ad saved
- [ ] User instruction is specific and bounded
- [ ] Credit cost communicated
- [ ] Confirmed edit vs re-generate decision
- [ ] Poll completed before presenting
- [ ] Meta re-upload planned if going live
```

## Related Skills

- `meta-ad-creative` — fresh generation from listing
- `ad-creative-variants` — initial batch before edits
- `ad-creative-to-meta` — publish edited creative
- `meta-campaign-audit` — identify which ad deserves A′
- `competitor-ad-teardown` — inspiration for new angles (not edits)
- `screenshot-optimization` (aso-skills) — if edit needs new screenshot source
