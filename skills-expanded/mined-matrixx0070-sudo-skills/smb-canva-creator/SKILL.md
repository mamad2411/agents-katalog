---
name: smb-canva-creator
version: 1.0.0
description: Turn an approved content brief into a posting calendar plus Canva social designs and captions, pausing for owner sign-off at each stage.
author: matrixx0070
tags: [marketing, canva, social-media, content, design, captions]
capabilities: []
---

# Canva Creator

## When to use
Use this after a content brief is approved and you want it turned into finished, ready-to-post assets. This is the execution arm — it builds the calendar, the Canva designs, and the captions, pausing for sign-off at each stage.

**Not for:** deciding what to promote or building the strategy (use smb-content-strategy first). This executes an existing brief; it does not plan one. It also never publishes.

## Method
1. Read the approved brief. Confirm platforms, post count, and brand kit with the owner before creating anything. Decision point: if the brief is missing a platform or count, ask before proceeding.
2. Draft a posting calendar — date, platform, topic, format per post — and get owner approval on the schedule.
3. For each approved post, generate a Canva design using the brand kit. Present a thumbnail or link and wait for approval before finalizing or exporting.
4. Write a caption per post with hashtags and a clear call to action. Present captions for edits. Decision point: match caption length and tone to the platform (short and punchy for IG, more context for LinkedIn).
5. Export approved designs. Never publish or schedule to a live channel — hand finished assets back to the owner.

## Example
Brief: 4 posts, IG + LinkedIn, spring-promo brand kit. Calendar approved. Post 1 (IG, Mon, carousel): design link presented → owner approves → caption drafted: "Spring bookings are open. Three slots left this month — link in bio. #SpringClean #LocalBusiness" → approved → exported to /assets/spring/post1.png. Repeat for posts 2-4.

## Pitfalls
- **Skipping the brand kit check.** Off-brand colors or logos mean rework; confirm the kit up front.
- **Batch-exporting before approval.** Export only what the owner signed off on, one stage at a time.
- **Generic captions.** "Check out our latest!" converts nothing — tie each caption to the post's specific offer.
- **Publishing.** This skill hands back assets; scheduling or posting to a live channel is always the owner's action.

## Output format
```
Posting calendar:
| Date | Platform | Topic | Format |
|------|----------|-------|--------|

Per approved post:
  Design: <preview link>
  Caption: <text>
  Hashtags: <#...>
  "Approve to continue."

Exported assets:
  - <file/location>
```

## Reference

### Platform dimension cheat-sheet (px)
Design at these sizes so nothing gets cropped. Canva has templates for each — start from the right canvas rather than resizing after.

| Platform / format | Dimensions | Aspect | Notes |
|---|---|---|---|
| Instagram feed (portrait) | 1080 × 1350 | 4:5 | Portrait wins the most feed real estate |
| Instagram square | 1080 × 1080 | 1:1 | Safe default, works cross-posted |
| Instagram / TikTok Story & Reel | 1080 × 1920 | 9:16 | Keep text/CTA out of top 250px and bottom 320px (UI overlap) |
| Instagram carousel | 1080 × 1350 | 4:5 | 2-10 slides; slide 1 is the hook |
| Facebook feed | 1080 × 1350 | 4:5 | Same asset as IG usually fine |
| LinkedIn feed image | 1200 × 1200 or 1200 × 627 | 1:1 / 1.91:1 | Square gets more feed height |
| LinkedIn document/PDF | 1080 × 1350 | 4:5 | Carousel-as-PDF performs well |
| X / Twitter | 1600 × 900 | 16:9 | |
| YouTube thumbnail | 1280 × 720 | 16:9 | Large readable text, high contrast face |

Keep critical content inside a center "safe zone" (~10% margin all sides), since platforms crop previews differently.

### Caption length and structure by platform
- **Instagram:** front-load the hook in the first 125 characters (that's what shows before "…more"). Sweet spot 138-150 chars for reach, though longer story-style captions can drive saves. 3-5 hashtags in the caption or first comment.
- **LinkedIn:** first 2-3 lines before "see more" must earn the click. 900-1,300 characters performs well; add line breaks for scannability; 3-5 hashtags max.
- **Facebook:** shorter is better — 40-80 characters often gets the most engagement.
- **X/Twitter:** under 100 characters leaves room for replies/quotes; 1-2 hashtags.
- **TikTok:** short caption, 1-3 hashtags mixing broad + niche.

### The caption formula
Every caption should have four parts: **Hook** (stop the scroll) → **Value/context** (why they care) → **CTA** (one clear action) → **Hashtags**. One CTA per post — "link in bio," "DM us," "comment below," or "book now" — never a menu of three.

### Hashtag strategy
Mix tiers so you're not only competing in the biggest pools: 1-2 broad (1M+ posts), 2-3 mid-niche (50k-500k), 1-2 tightly targeted or branded (your own tag + local geo tag like #AustinCleaners). Rotate sets; recycling one identical block can suppress reach.

### Rough best-time-to-post guide
Defaults to test against your own analytics (audience data always wins): weekday mornings 9-11am and evenings 7-9pm; Instagram mid-week (Tue-Thu) trends best; LinkedIn Tue-Thu 8-10am; avoid late Friday and weekend mornings for B2B.

### Pre-export design checklist
- Logo present and correct version; brand colors/fonts from the kit (no default Canva fonts left in).
- Text legible at thumbnail size; contrast passes (dark text on light or vice versa).
- No lorem ipsum, no placeholder image, no stray guide lines.
- Correct dimensions for the target platform; critical content inside the safe zone.
- Spelling and the offer/price checked; export as PNG (static) or MP4 (motion) at the platform size.

### Owner-approval gate
Three gates, in order: (1) the calendar, (2) each design before finalize/export, (3) each caption before it's paired. The skill exports approved assets to a folder and hands them back. It never connects to or publishes on a live channel — scheduling and posting are always the owner's action.
