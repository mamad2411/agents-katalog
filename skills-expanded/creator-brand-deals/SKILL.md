---
name: creator-brand-deals
description: Help creators land and run brand deals - media kit, rate card from their own numbers, pitch emails to brands, contract red flags (usage rights, exclusivity, payment terms), and sponsorship disclosure rules for India (ASCI), Canada and the US (FTC). Use when the user asks "how much should I charge", "make my media kit", "pitch this brand", "is this contract ok", or "how do I disclose a sponsored post".
---

# Brand deals

## Media kit (1 page)
Name/handle, niche in one line, audience (top countries/cities, age, gender split from platform insights), followers per platform, median views, engagement rate, 2 to 3 best posts with numbers, past brands, contact. Use real numbers only.

## Pricing: run the script on their recent posts
```
python scripts/rates.py posts.csv --followers 25000 --cpm-low 15 --cpm-high 30
```
- Price from median views (not followers): views/1000 × CPM.
- CPM comes from their past deals, the brand's stated budget, or an agency rate card the user provides. Don't make up market rates; if they have none, give a range and tell them to test it.
- Add-ons (state them separately): usage rights for ads (priced per month of use), exclusivity (no competitor posts for X days), raw footage, extra stories/links, rush delivery.
- Bundle discounts for 3+ deliverables. Gifted-only deals are fine for growth, but the product still counts as income for tax.

## Pitch email
Under 120 words: who they are + one audience stat, why this brand fits (a real detail about the brand), one concrete content idea, a link to the media kit, a simple ask ("Open to a call next week?"). Follow up once after 5 to 7 days.

## Contract red flags (explain each one found)
- Perpetual or worldwide usage rights, or rights to use their face in ads without extra pay.
- Long exclusivity for a small fee.
- Payment terms over 30 to 45 days, or "on brand approval" with no deadline.
- Unlimited revisions; no cap on reshoots.
- Brand can edit their content or captions without approval.
- Kill fee missing (what they're paid if the brand cancels).
- Morality or claw-back clauses that are vague.
Suggest exact replacement wording. Not legal advice; for big contracts suggest a lawyer.

## Disclosure (always required for paid, gifted or affiliate posts)
- India: ASCI influencer guidelines: a clear label like #ad, #collab, #sponsored or "Paid partnership", visible upfront (not buried in hashtags); in video, say it and show it. Health/finance creators have extra qualification rules.
- US: FTC Endorsement Guides: "#ad" or "Sponsored" at the start, plus the platform's paid-partnership tool; say it in the video too.
- Canada: Ad Standards Influencer Marketing Disclosure Guidelines and the Competition Act: same idea, clear and upfront, including for gifted products and affiliate links.

For tax on brand income and gifted products, use the country skill: india-creator-tax, canada-creator-tax or us-creator-tax.

## Calculator code
If `scripts/rates.py` isn't in this skill's folder (some apps keep only SKILL.md), save this code as `rates.py` and run it the same way. Don't do the arithmetic by hand.

<!-- embed: scripts/rates.py -->
```python
"""Engagement rate and a CPM-based price range for a sponsored post.
Usage: python rates.py posts.csv --followers 25000 --cpm-low 15 --cpm-high 30
posts.csv columns: views,likes,comments,saves,shares   (one row per recent post, 10 to 20 posts)
CPM = price per 1,000 views. Use rates from the creator's own past deals or the brand's budget; this script doesn't invent them.
"""
import argparse
import csv
from statistics import median


def stats(rows, followers):
    eng = [sum(float(r.get(k) or 0) for k in ("likes", "comments", "saves", "shares")) for r in rows]
    views = [float(r["views"]) for r in rows]
    return {
        "median_views": median(views),
        "engagement_rate_followers": median(eng) / followers,
        "engagement_rate_views": median(e / v for e, v in zip(eng, views) if v),
    }


def price_range(median_views, cpm_low, cpm_high):
    return round(median_views / 1000 * cpm_low), round(median_views / 1000 * cpm_high)


if __name__ == "__main__":
    s = stats([{"views": "10000", "likes": "800", "comments": "50", "saves": "100", "shares": "50"},
               {"views": "20000", "likes": "900", "comments": "60", "saves": "20", "shares": "20"}], 20000)
    assert s["median_views"] == 15000 and s["engagement_rate_followers"] == 0.05
    assert price_range(15000, 20, 40) == (300, 600)

    p = argparse.ArgumentParser()
    p.add_argument("csv")
    p.add_argument("--followers", type=float, required=True)
    p.add_argument("--cpm-low", type=float, required=True)
    p.add_argument("--cpm-high", type=float, required=True)
    a = p.parse_args()
    with open(a.csv, newline="") as f:
        s = stats(list(csv.DictReader(f)), a.followers)
    lo, hi = price_range(s["median_views"], a.cpm_low, a.cpm_high)
    print(f"Median views per post: {s['median_views']:,.0f}")
    print(f"Engagement rate: {s['engagement_rate_followers']:.2%} of followers, {s['engagement_rate_views']:.2%} of views")
    print(f"One post at CPM {a.cpm_low:g} to {a.cpm_high:g}: {lo:,} to {hi:,} (same currency as the CPM)")
    print("Add for: usage rights, exclusivity, extra deliverables, rush timelines.")
```
