---
name: portfolio-manager
description: Use this skill for a periodic (weekly/monthly) review checklist of a long-term core portfolio — concentration limits, rebalance triggers, and dividend/ETF-specific checks. Trigger on "portfolio review", "rebalance", "concentration check", "core portfolio", "weekly portfolio review". This skill structures a review process; it does not fetch live prices or execute trades.
---

# Portfolio Manager

## Overview

A long-term core portfolio (dividend stocks, ETFs) doesn't need daily attention, but it does drift — position sizes grow unevenly, sector concentration creeps up, a dividend gets cut without anyone noticing. This skill is a structured periodic review checklist, not an execution engine — it turns "check on my portfolio" into a repeatable set of questions instead of an ad hoc glance.

**Not financial advice.** This is a review framework and a set of questions to ask; it does not recommend specific buy/sell/rebalance actions.

## When to use

- ทำ portfolio review รายสัปดาห์/รายเดือน สำหรับพอร์ตระยะยาว (dividend/ETF core)
- ตรวจสอบว่ามีหุ้นตัวไหนมีสัดส่วนเกิน concentration limit ที่ตั้งไว้
- Checking whether a rebalance trigger has been crossed
- Reviewing recent dividend-related news (cuts, suspensions) for holdings

## When NOT to use

- The task is a swing-trade candidate screen or entry timing — that's [dividend-value-screener](../dividend-value-screener/SKILL.md) or a momentum screener, not a periodic core-portfolio review
- The user wants a live, real-time portfolio value — this skill structures periodic review, it doesn't fetch prices

## Core knowledge

**Concentration check**: flag any single position or sector exceeding the user's own stated limit (common starting points discussed in portfolio-construction literature: 5-10% max per single stock position, 20-25% max per sector — these are illustrative anchors, not rules this skill asserts as correct; the user's actual limit should come from their own plan).

**Rebalance triggers**: two common approaches — calendar-based (review every N months regardless of drift) and threshold-based (rebalance when an allocation drifts more than X percentage points from target). Ask which approach the user's plan uses rather than assuming one.

**Dividend-specific checks** (for income-focused holdings):
- Any dividend cut, suspension, or unusually large special dividend since last review?
- Has the payout ratio (dividend / earnings) moved to a level the user would consider unsustainable?
- Has the position's yield changed mainly because the price moved, or because the dividend itself changed? (These have very different implications — a rising yield from a falling price is a different situation than a rising yield from a dividend increase.)

**ETF-specific checks**: expense ratio unchanged, tracking error reasonable, no unexpected structural change (index methodology change, fund closure/merger announcement).

**Review structure**: (1) current allocation vs. target, (2) concentration flags, (3) rebalance-trigger check, (4) dividend/distribution changes since last review, (5) any names that no longer fit the original investment thesis (thesis drift, not just price movement).

## Common mistakes

1. Treating a rebalance check as "sell whatever went up" — rebalancing is about restoring target allocation, not about disliking winners.
2. Confusing a rising yield-on-cost with a rising current yield — a stock that's up a lot can have a low current yield even if the user's own cost-basis yield looks great; both numbers matter for different purposes.
3. Reacting to one quarter's dividend/earnings news without checking whether it's a trend or a one-off.
4. Applying a swing-trading concentration limit (tight) to a long-term core portfolio (typically wider) or vice versa — the two contexts have different appropriate limits.
5. Skipping the "does this still fit the original thesis" question — a stock can be performing fine price-wise while the underlying reason it was bought no longer holds.

## Known limitations

- This skill does not fetch live prices, dividend data, or news — the user (or another data-fetching tool/integration) must supply current holdings and any relevant news for a real review.
- Concentration/rebalance thresholds cited here are illustrative anchors from general portfolio-construction discussion, not personalized recommendations — the user's actual plan should set the real numbers.
