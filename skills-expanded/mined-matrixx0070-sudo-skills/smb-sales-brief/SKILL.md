---
name: smb-sales-brief
version: 1.0.0
description: Surface top and bottom sellers plus seasonality, then produce a two-week content brief mapped to channels.
author: matrixx0070
tags: [sales, analysis, content, seasonality, marketing, calendar]
capabilities: []
---

# Sales Brief

## When to use
Run this when the owner wants to know what's selling and what to post about next. It connects the numbers to a concrete two-week content plan without committing to any spend.

**Not for:** executing or sending anything (use smb-run-campaign); pricing decisions (use smb-price-check); this skill plans content and publishes nothing.

## Method
1. **Pull the data.** Recent sales from connected systems, or ask the owner for a period to analyze.
2. **Rank products.** Top sellers by revenue and by units; bottom sellers that are dragging or stale.
3. **Detect seasonality and trend.** Compare against prior periods; flag items rising or fading and any recurring seasonal pattern. Decision point: separate a genuine trend from a one-off spike (a single big order isn't a pattern).
4. **Turn findings into angles.** Which winners to amplify, which slow movers to promote or clear, which stories the data suggests.
5. **Build a two-week content brief.** A dated calendar of post ideas mapped to channels, each with a hook and the product or angle it supports.
6. **Present for editing.** The owner edits; hand off to smb-run-campaign when ready to execute.

## Example
Last 30 days: top by revenue = leather wallets ($4,200), top by units = keychains (210); bottom = phone cases (stale 3 months). Trend: wallets up 18% MoM, cases fading — not a one-off. Angles: amplify wallets (gift angle), clear cases with a bundle. Two-week calendar: Mon IG "wallet gifting" hook, Wed email "case + wallet bundle," Fri IG keychain UGC. Handoff: smb-run-campaign to launch the bundle.

## Pitfalls
- Reading a single large order as a "trend" and building a campaign on noise.
- Ranking only by revenue and missing a high-unit item worth featuring for reach.
- A content calendar with hooks but no product/angle tied to each post — pretty but empty.
- Drifting into sending or spending; this brief stops at a plan the owner edits.

## Output format
- **Top/bottom seller tables:** product | revenue | units | trend arrow.
- **Seasonality note** (2-4 sentences).
- **Two-week calendar:** date | channel | hook | supporting product.
- **Handoff line** pointing to smb-run-campaign when the owner is ready to execute.

## Reference

### Ranking framework (rank on more than one axis)
- **By revenue** — what pays the bills; your headline sellers.
- **By units** — reach and popularity; a low-price high-unit item is a great content and acquisition hook even if it's not top revenue.
- **By margin contribution** — margin$ × units; the item that actually funds growth (pull from smb-price-check if available).
- **By trend** — % change vs. prior period; where momentum is, up or down.
Feature the intersection: a product that's high-units *and* rising is your best content bet this fortnight.

### Trend vs. noise: separation rules
- A single large order is **not** a trend — strip outliers before ranking.
- Require a pattern across **at least 2-3 periods** (or same period last year) before calling something "rising" or "fading."
- Watch **week-of-month and day-of-week** effects; compare like-to-like (last 4 Mondays, not Monday vs. Saturday).
- Distinguish **seasonal** (repeats yearly), **trend** (sustained direction), and **spike** (one-off promotion or event).

### Seasonality quick-reference (common SMB patterns)
| Window | Pattern | Content angle |
|--------|---------|---------------|
| Jan | Post-holiday slump; "new year/reset" intent | Restock, resolutions, clearance |
| Feb | Valentine's | Gifting, bundles |
| Mar-Apr | Spring pickup; tax refunds hit | New arrivals, treat-yourself |
| May-Jun | Mother's/Father's Day, grads, weddings | Occasion gifting |
| Jul-Aug | Summer slowdown (many retail) | Re-engagement, cold-brew/seasonal SKUs |
| Sep | Back-to-school; fall reset | Routine, replenishment |
| Nov-Dec | BFCM + holiday peak — bulk of many SMBs' year | Gift guides, urgency, VIP early access |
Note: service and B2B businesses often invert this (busy summer, slow December).

### From findings to content angles
- **Amplify winners** — feature the top rising seller with a fresh hook (gifting, use-case, UGC).
- **Clear slow movers** — bundle a stale item with a winner, or a limited clearance (check margin before discounting).
- **Tell the data's story** — "customers who buy X also buy Y" → cross-sell post.
- **Reach play** — feature the high-unit low-price item to pull new eyeballs.

### Two-week content calendar template
| Date | Channel | Hook | Supporting product/angle | Goal |
|------|---------|------|--------------------------|------|
| Mon | IG | benefit-led | top rising seller | awareness |
| Wed | Email | offer/bundle | winner + slow-mover | conversion |
| Fri | IG | UGC / social proof | high-unit item | reach |
| (repeat wk 2 with fresh hooks) | | | | |
Cadence rule of thumb: 3-4 touches/week is sustainable for a solo owner; every post ties to a product or angle or it's cut.

### Channel fit
- **Email** — best for conversion and existing customers; offers, bundles.
- **Instagram/TikTok** — awareness, visual products, UGC and behind-the-scenes.
- **Google Business / local** — discovery for brick-and-mortar; hours, new arrivals.
Match the product to where its buyers already are, not to every channel at once.

### Boundary
This skill plans content and publishes nothing. It commits no spend and sends nothing to customers. When the owner is ready to execute, hand off to smb-run-campaign, which gates every customer-facing and money step.
