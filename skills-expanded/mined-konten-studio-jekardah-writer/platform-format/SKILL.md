---
name: platform-format
description: Use when a finished or near-finished draft needs to be shaped for a specific channel — Instagram caption, X/Twitter thread, LinkedIn post, TikTok/Reels script, newsletter/email, or generic long-form — including length limits, line breaks, thread splitting, or script beats.
---

# Platform Format

Shape an already-written draft to fit one channel's conventions. This is a structural/layout pass, not a rewrite: it never changes facts, hook wording, voice diction, or claims.

## Load only what you need

- Read [references/platform-specs.md](references/platform-specs.md) for per-platform length limits, structural conventions, and split/beat rules.

## Scope contract

This skill owns segmentation, ordering into platform units (tweets/slides/beats), length trimming that removes only redundancy (never claims), hashtag/CTA placement, and line-break rhythm for the target channel. It cannot own or invent facts, change the hook's wording or angle, change voice diction/register, or add claims to fit a length limit. If the draft cannot fit the platform limit without cutting a defensible proposition, stop and report the conflict instead of cutting silently.

## Core workflow

1. **Identify the target.** Confirm platform (Instagram feed/carousel, X/Twitter, LinkedIn, TikTok/Reels script, newsletter/email, or generic long-form) and any explicit constraints (thread length cap, carousel slide count, video duration).
2. **Load the spec.** Use [references/platform-specs.md](references/platform-specs.md) for that platform's limits and conventions.
3. **Segment.** Split the draft into the platform's native units (tweets, slides, beats, paragraphs) at natural sense-breaks — never mid-proposition.
4. **Trim only redundancy.** If over length, cut repeated phrasing, filler transitions, or restated points first. Never cut a name, number, date, attribution, or the hook/payoff pair.
5. **Place CTA and hashtags/tags** per the target platform's convention from the spec, using the CTA intent already locked upstream — do not invent a new CTA.
6. **Verify fit.** Confirm every unit is within the platform's limit and the split reads naturally stand-alone (each tweet/slide should not require the next to make sense on its own, where the platform expects that).

## Composition contract

- **Input owned by orchestrator:** source draft, fact/story lock, selected hook, CTA intent, platform target.
- **This skill owns:** platform segmentation, unit ordering, length trims of redundancy only, hashtag/CTA placement, line-break rhythm.
- **This skill returns:** `platform_target`, the formatted output, and `platform_format_check` (`pass` or a named conflict if a limit forced a cut the skill refused to make).
- **This skill must not change:** facts, numbers, names, dates, attribution, hook wording/angle, voice diction, CTA intent.
- **Conflict order:** factual integrity > hook/payoff integrity > platform limit compliance > cosmetic tightening.
- **Final gate:** diff the formatted output against the pre-format draft; any change beyond segmentation/trimming/placement is a violation — revert and report.

## Output

Return the platform-formatted draft in the platform's native unit structure (numbered tweets, labeled slides, beat list with visual cue + line, etc.), followed by:

```text
Platform: [target]
platform_format_check: [pass / conflict — reason]
```

If a length limit cannot be met without cutting a defensible proposition, do not cut it. Report the conflict and offer the smallest safe trim instead.
