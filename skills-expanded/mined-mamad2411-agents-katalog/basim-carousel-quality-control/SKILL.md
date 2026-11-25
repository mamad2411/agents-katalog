---
name: basim-carousel-quality-control
description: Use when Basim asks for carousel/social content quality to stay consistent across Repliz cron jobs; preserves the 15 Juni 2026 audit bar for trend research, angle scoring, carousel structure, media verification, and scheduling reports.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [basim, carousel, repliz, social-media, quality-control]
    category: social-media
    related_skills: [senang-carousel-generator, threads-content-and-scheduling]
created_by: agent
---

# Basim Carousel Quality Control

## Overview

This skill preserves the production quality bar Basim approved for carousel + Repliz workflows, especially the strong run pattern from **15 Juni 2026**. Use it to keep automated carousel content from degrading into short generic output after model/provider changes, cron edits, or fallback generation.

Core standard: every carousel run must feel like a complete editorial/audit workflow, not just “generate slides and schedule.” The output should explain why the angle was chosen, why it is safe, why it fits Basim, how media was verified, and where it was scheduled.

## When to Use

Use this skill when:

- Basim asks to keep carousel/content quality consistent.
- Editing or running `Basim general viral/tips carousel to Repliz multi-platform`.
- A cron/model/provider change risks losing long prompt instructions.
- Carousel output becomes too short, generic, or lacks audit/scoring.
- Scheduling carousel content through Repliz to Threads, Instagram, TikTok, and YouTube.
- Comparing today’s carousel output against “kemarin” / “seperti hari kemarin”.

Related skills to load as needed:

- `senang-carousel-generator` for slide generation/export and Basim visual defaults.
- `threads-content-and-scheduling` for Repliz scheduling, analytics, and Threads/Instagram/TikTok/YouTube payload rules.

## Quality Bar From 15 Juni 2026

A production carousel report should include all of these sections:

```text
Laporan carousel otomatis — <tanggal WIB>

Tren/sinyal yang dicek:
- ...

Performa Repliz 48 jam terakhir:
- ...

Skor kandidat:
1. ... Skor ...
2. ... Skor ...
3. ... Skor ...

Angle terpilih:
- ...

Audit konten:
- Kenapa aman/low-risk
- Kenapa cocok untuk carousel/saveable
- Kenapa tidak mengulang angle 48 jam terakhir

Status:
- Auto-scheduled / butuh approval jika sensitif
- Collision check: ...

Validasi media:
- jumlah slide dan dimensi
- ZIP valid
- public URLs
- MP4

Schedule Repliz:
- Threads — <WIB> scheduleId: ...
- Instagram — <WIB> scheduleId: ...
- TikTok — <WIB> scheduleId: ...
- YouTube — <WIB> scheduleId: ...

Local artifact:
MEDIA:<zip path>
```

If any section cannot be completed, explicitly say why. Do not silently omit it.

## Content Research Requirements

Before choosing an angle:

1. Check current Indonesian/social/digital signals for the run date.
2. Prefer useful, low-risk trends:
   - AI tools for creators/business owners
   - UMKM/bisnis workflow
   - manual customer follow-up
   - Meta Ads leads leaking
   - app ideas stuck in the head
   - teams working from scattered chats
   - AI output becoming stiff because context is missing
   - SOP/decisions waiting for the owner
   - security/digital behavior when not fearmongering
3. Treat sensitive news carefully:
   - demos/protests
   - public policy outrage
   - disasters/public safety
   - crime, death, identity-based conflict
   - allegations without strong sourcing

Sensitive/current-event topics should usually become **draft + audit for approval**, not auto-scheduled carousel content.

## Candidate Scoring

Score at least 3 candidate angles before choosing one. Use this scale:

| Dimension | Meaning |
|---|---|
| Momentum | Is it connected to current/recent conversation? |
| Relatability | Will an owner/creator say “ini gue”? |
| Saveability | Does it become a checklist, reminder, or practical pattern? |
| Twist | Is there a reversal like “dikira A, ternyata B”? |
| Safety | Is it low-risk, non-sensitive, non-clickbait? |
| Fit | Does it support Basim’s direction: AI, systems, owner fatigue, execution? |

Default scoring: each dimension 1–5, total /30.

Choose the highest score only if it is safe. A lower score but safer angle can win over a risky current event.

## Carousel Structure

Prefer **7–10 slides**. Six slides is acceptable only if the idea is very small and still complete.

Recommended structure:

1. Hook parable/analogy: concrete, relatable, not jargon.
2. Twist/conflict: what looks fast/large/clever is not always what wins.
3. Bridge to owner/business/AI daily reality.
4. Hidden system: manual process, decision bottleneck, missing context.
5. More hidden system or consequence: lead leaks, follow-up missed, SOP absent.
6. Micro-example: one realistic operational moment.
7. Second micro-example or mini-framework.
8. Saveable checklist.
9. Payoff reflection.
10. Optional soft CTA or closing line.

Avoid:

- corporate pitch deck feel
- generic motivation quotes
- crowded bullet slides
- AI futurism/glow/neon/dashboard visual language
- too many claims per slide
- hard-sell service copy

## Visual Standard

Default to Basim's current approved carousel look unless Basim explicitly approves a visual experiment. The reference Basim showed has this visual DNA:

- Square/portrait clean canvas with **plain white background** and very large negative space.
- Text-first composition: short Indonesian phrase centered in the upper/middle area.
- Modern sans-serif typography, black text, no serif look, no border/frame.
- Bold emphasis only on the key words inside each line, e.g. `dikira **alat** / yang paling **penting** / ternyata **arah**`.
- Each slide should usually contain one punchy idea, not paragraphs.
- Character/avatar accent sits **small at bottom-right**, not dominating the slide.
- Futuristic blue hologram/dashboard elements may sit behind/around the character as an accent, not as full background.
- A small subtle chevron/arrow near bottom center is acceptable.
- Palette: white + black text + small blue/cyan tech accent + character colors.
- Overall feel: premium, clean, calm, strategic, not a busy infographic.
- Approved examples and the exact avatar+hologram template are documented in `references/approved-avatar-hologram-template.md`.

Operational defaults:

- When Basim provides a visual reference and says the draft is not matching, treat the reference image as the source of truth and regenerate against it instead of defending the earlier draft.
- For this approved template, keep slides to one short punchy idea in 3 lines; do not use paragraph-style educational copy on the visual itself.
- If the style is being re-established or changed, send a contact-sheet test first and wait for Basim's confirmation before applying it broadly in cron outputs.
Operational defaults:

- Indonesian language.
- **Default approved reference format is square 1:1** (`1080x1080`) for this Basim avatar/hologram carousel style. Use 4:5 only if a specific platform constraint or Basim request requires it; when adapting to 4:5, preserve the same white space and bottom-right avatar composition.
- handle: `@cerita.basim.id` only if it belongs in the visual template; do not force it if the approved reference omits it.
- whitespace generous.
- one idea per slide.
- no border/frame unless Basim asks.
- no dense bullets except one saveable checklist slide.
- When Basim asks for a “draft contoh carousel”, send an actual **visual preview asset** (contact sheet and/or slide PNG ZIP) in the approved reference style — not just text copy or a generic mockup description.
- Before generating preview slides, sanity-check that the draft still matches the approved style DNA: 3 centered lines, one bold keyword per line, lowercase sans-serif, white background, avatar/hologram accent bottom-right, subtle chevron, and premium negative space.
- If the first preview misses the style, correct the visual system immediately rather than defending the old mockup. Basim treats the approved reference image as the source of truth.
- For Basim’s current approved style set, see `references/avatar-hologram-square-style.md`.

Reference accounts like `@ceritaberkelas` may inform **content mechanics only**:

- parable/analogy
- one idea per slide
- reflective short copy
- soft curiosity
- saveable lesson

Do **not** copy their wording, logo, illustration style, identity, or replace Basim’s current approved visual template unless Basim explicitly asks.

## Caption Standard

Public caption should be short:

- 1–2 lines.
- Soft curiosity.
- Natural Indonesian.
- No hashtag.
- Not a full summary of the carousel.
- No internal labels such as `topic`, `draft`, `judul`, `skor`, `sumber`, or audit notes.

Good pattern:

```text
yang cepat belum tentu rapi. kadang bisnis cuma butuh alur yang lebih tenang.
```

## Scheduling & Collision Rules

Before POSTing to Repliz:

1. Check existing pending schedules/recent content when possible.
2. Avoid stacking carousel batch within **±45 minutes** of Threads evergreen/radar posts.
3. If collision exists, move the carousel batch to the next safe slot.
4. Schedule only one carousel batch per run.
5. Threads + Instagram use album.
6. TikTok + YouTube use MP4 slideshow/video.
7. YouTube must have a real title; never `unknown`.
8. If one platform fails, report that platform only. Do not claim all succeeded.

## Media Verification

Before reporting success:

- Verify slide count.
- Verify every slide dimension is `1080x1350`.
- Verify ZIP opens and `testzip()` is `None`.
- Verify public image URLs return HTTP 200.
- Verify MP4 URL returns HTTP 200 and is video content.
- Verify Repliz returns HTTP 200/201 with `scheduleId`.
- If `GET /public/schedule/{scheduleId}` works, verify `status: pending` or equivalent.

If SenangCarousels API fails:

- Retry only if the error suggests a short transient retry.
- If quota/approval guard blocks generation, use fallback only if it preserves Basim’s normal 1080x1350 style.
- Label fallback honestly in the report.
- Do not auto-schedule an off-template fallback.

## Hard Rules

- Never expose Repliz/Gemini/API credentials.
- Never add hashtags unless Basim explicitly reverses the no-hashtag preference.
- Never put internal metadata into public caption/body.
- Never auto-post sensitive current-event/newsjacking content without approval.
- Never reduce report quality to a short summary when the job is meant to be an audited production run.
- Never say a schedule succeeded unless schedule IDs/statuses were actually returned.

## Common Pitfalls

1. **Prompt got shortened during cron update.** Restore this quality skill and full report format; do not rely on “existing configuration” wording.
2. **Model/provider changed and output became generic.** Force candidate scoring + current trend check + audit before generation.
3. **Fallback local carousel used silently.** State fallback, verify dimensions, and ensure it stays visually consistent.
4. **Local draft preview misses Basim's approved reference.** Do not defend the mockup. Regenerate in the reference style: square 1:1, white background, 3 centered lowercase lines, one bold keyword per line, avatar+hologram accent bottom-right, subtle chevron. Avoid text-heavy 4:5 paragraph slides unless Basim explicitly asks for that format.
5. **Approval mapping drifted to an older queue item.** If Basim replies with phrases like `approve #1`, `approve #2`, etc., do not assume the numbering refers to an older radar run or previously mentioned candidate. First verify the **latest relevant approval queue output** and map the approval to that exact run before scheduling anything. If multiple radar outputs exist, use the newest one unless Basim explicitly points to an older batch.
6. **Caption accidentally includes labels or hashtags.** Strip all internal labels and hashtags before scheduling.
7. **Too close to other Threads jobs.** Run collision check and shift publish time.
8. **YouTube title becomes `unknown`.** Generate a real title from the selected angle.

## Approval Queue Discipline

When Basim gives short approval replies such as `approve #1`, `approve #2`, or `GAS POST` after a radar/approval queue message:

1. Identify the most recent relevant approval queue artifact first.
2. Re-read the exact candidate title, slot recommendation, and safety status from that latest queue.
3. Confirm the scheduled body/thread matches that candidate, not a stale earlier queue item with the same numbering.
4. After scheduling, report the candidate title in the confirmation message so Basim can spot mismatch immediately.

This rule matters especially when multiple viral-radar runs happened on the same day and each produced its own `#1/#2/#3` set.

## Verification Checklist

- [ ] Current signals checked.
- [ ] 48-hour performance or recent content reviewed when API access allows.
- [ ] 3 candidate angles scored.
- [ ] Selected angle is low-risk or flagged for approval.
- [ ] Carousel has 7–10 slides unless justified.
- [ ] Caption is short and hashtag-free.
- [ ] Visual style matches Basim/Senang defaults.
- [ ] Media dimensions and ZIP verified.
- [ ] Public media URLs verified.
- [ ] Repliz schedule IDs verified per platform.
- [ ] Final report includes the full quality bar sections.
