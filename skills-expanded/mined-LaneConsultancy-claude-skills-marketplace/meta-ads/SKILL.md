---
name: meta-ads
description: Use when planning, launching, optimising, or diagnosing Meta/Facebook/Instagram ad campaigns — especially low-budget lead generation (£20-100/day) and info product sales targeting 1+ ROAS. Triggers include 'Facebook ads', 'Meta ads', 'Instagram ads', 'lead gen ads', 'CAPI', 'Conversions API', 'Andromeda', 'Advantage+', 'CPL', 'ROAS', 'Pixel', or any use of the local `meta` CLI.
---

# Meta Ads (2025-2026)

Current best practice for Meta/Facebook/Instagram advertising. Reflects the 2025 Andromeda rollout, the January 2026 attribution change, and the May 2026 ASC/AAC API deprecation.

## When to use

- Planning, launching, optimising, or diagnosing any Meta campaign
- Writing a Meta ad brief or creative plan
- Setting up Conversions API or pixel/dataset
- Using the local `meta` CLI
- Any question about Andromeda, Advantage+, CPL, ROAS, attribution, EMQ

## When NOT to use

- Google/LinkedIn/TikTok ads → this skill is Meta-specific
- Landing page conversion rate → use `page-cro`

## Hard rules (override older guidance)

1. **Creative volume is the lever.** 10-20 *distinct* creative concepts per ad set is the new floor under Andromeda. "Distinct" = different hook, different visual, different angle — not colour swaps. See `andromeda-creative-system.md`.
2. **Attribution defaults are 7-day click + 1-day view only.** 7-day-view and 28-day-view were removed January 2026. Don't compare new data to old reports without converting.
3. **Conversions API is non-optional.** Pixel-only setup loses 40-60% of signal post-iOS 14.5. Set up CAPI before any optimisation work. See `conversions-api-setup.md`.
4. **At <£30/day, ABO beats CBO** for prospecting (94% vs 81% ROAS in 2025 Lebesgue data). At <50 weekly conversions, optimise on a higher-funnel event (Initiate Checkout, Lead Form Open) — Purchase optimisation needs ~50/week to exit learning.
5. **Advantage+ Creative is ON by default since Feb 2026.** Don't disable wholesale; selectively turn off music/text-overlay only when off-brand or non-compliant.
6. **ASC and Advantage+ App Campaigns are dead via API as of 19 May 2026.** Don't write code that creates them.
7. **Default CLI status is PAUSED.** Always preview before activating.

## Decision routing

| Situation | Open this file |
|-----------|----------------|
| What changed recently / what overrides what | `current-state-2026.md` |
| Writing ad copy / hooks / offers / CTAs | `copy-and-offers.md` |
| Creative planning, brief, refresh | `andromeda-creative-system.md` |
| Lead-gen on £20-100/day (PRIMARY use case) | `lead-gen-low-budget.md` |
| Info product launch on £50-100/day for 1+ ROAS | `info-product-1roas.md` |
| CAPI / Pixel / EMQ / domain verification | `conversions-api-setup.md` |
| "CPL is bad" / "no conversions" / diagnostics | `diagnose-performance.md` |
| Using the `meta` CLI / SDK / scripts | `cli-and-api.md` |

## CLI quick check

```bash
meta auth status              # confirm authenticated
meta ads adaccount current    # confirm correct account
```

The CLI auto-loads `.env` from CWD. Default account is `act_88999896`. Override per-command with `--ad-account-id act_XXXX`. **Budgets are in cents** (`--daily-budget 5000` = $50.00 ≈ £40). Full env/multi-account/output-format details in `cli-and-api.md`.

## Cross-references

- `form-cro` — for the page the ad sends to
- `analytics-tracking` — wider GA4 / consent mode setup beyond CAPI
