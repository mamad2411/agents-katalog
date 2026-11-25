---
name: ads-router
description: Single entry point that routes paid UA, mobile app ads, ad creatives, TikTok/Meta/ASA campaigns, ROAS, MMP setup, or Spark Ads requests to the correct specialist skill. Use FIRST when the user mentions ads, TikTok ads, Meta ads, Facebook ads, Apple Search Ads, ASA, CPA, CPI, ROAS, ad creative, Spark Ads, MMP, AppsFlyer, paid UA, or "help with my ad campaign" but the right skill is not obvious. Triggers "/ua-skill", "/ads-skill", "/growth-ads", "app ads help". Skip when user explicitly invokes a skill (e.g. /tiktok-campaign-setup). For organic ASO, see aso-skills.
metadata:
  version: 1.0.0
---

# Ads Router

You are the routing layer for UA Skills. Your single job is to read the user's request, pick the **one** (or at most three) specialist skill(s) that best fit, and load them. Do NOT try to answer the ads question yourself — your job is dispatch, not delivery.

## How to Use This Skill

1. Read the user's message.
2. Match it against the routing table below.
3. Announce: `→ Loading: <skill-name>` (and 2nd/3rd if relevant).
4. Read `skills/<skill-name>/SKILL.md` and follow it.
5. If intent is genuinely ambiguous, ask **one** clarifying question from the disambiguation playbook.

Never load more than 3 skills at once. If you would need more, ask the user to narrow down.

## Routing Table

Match by intent first, then by exact phrase. Top match wins.

### Foundation

| User intent / phrase | Route to |
|---------------------|----------|
| "set up context", "ads brief", "growth brief", first paid project | `app-ads-context` |
| "MMP", "AppsFlyer", "Adjust", "Singular", "Branch", "SKAN setup", "purchase events", "TikTok events tracking", "before I spend on ads" | `mmp-setup` |

### Creative Pipeline

| User intent / phrase | Route to |
|---------------------|----------|
| "generate ad creative", "Meta ad image", "ad from App Store listing", "1024 ad" | `meta-ad-creative` |
| "multiple ad variants", "A/B creatives", "3 angles", "5 creatives" | `ad-creative-variants` |
| "edit this ad", "change headline", "navy background", "iterate creative" | `ad-creative-edit` |
| "upload to Meta", "publish Meta ad", "listing to live ad", "draft Facebook ad" | `ad-creative-to-meta` |
| "competitor ads", "what is X advertising", "Meta Ad Library", "spy on ads" | `competitor-ad-teardown` |

### TikTok

| User intent / phrase | Route to |
|---------------------|----------|
| "set up TikTok ads", "TikTok campaign", "app install TikTok", "Smart+", "TikTok app promotion" | `tiktok-campaign-setup` |
| "TikTok ad ideas", "what videos should I make", "6 ads", "UGC format", "before after ad", "glow up ad" | `tiktok-creative-strategy` |
| "Spark Ads", "spark code", "authorization code", "organic post to paid" | `tiktok-spark-ads` |
| "TikTok CPA", "cost per conversion", "ads not working", "scale TikTok", "kill ad", "TikTok audit" | `tiktok-campaign-audit` |

### Meta (Facebook / Instagram)

| User intent / phrase | Route to |
|---------------------|----------|
| "set up Meta ads", "Facebook app install", "Instagram app ads", "Meta app promotion" | `meta-campaign-setup` |
| "audit Meta", "Facebook ad performance", "Meta CPA", "Instagram results" | `meta-campaign-audit` |
| "scale Meta", "pause Facebook ads", "Meta budget", "increase ad spend Meta" | `meta-budget-optimizer` |

### Apple Search Ads

| User intent / phrase | Route to |
|---------------------|----------|
| "ASA ROAS", "Apple Search Ads profit", "ASA revenue", "keyword profitability" | `asa-roas-analysis` |
| "weekly ASA", "optimize ASA", "ASA keywords", "ASA maintenance" | `asa-weekly-optimization` |
| "ASA negatives", "negative keywords", "search terms waste", "block search terms" | `asa-negative-keywords` |
| "ASA admaxxing", "scale ASA", "ASA playbook", "ASA recommendations" | `asa-admaxxing` |

### Measurement & Budget

| User intent / phrase | Route to |
|---------------------|----------|
| "MRR", "RevenueCat", "subscription snapshot", "how is revenue" | `subscription-snapshot` |
| "am I profitable", "LTV vs CPA", "ad margin", "break even CPI" | `campaign-profitability` |
| "all channels", "TikTok vs Meta", "compare ad platforms", "paid dashboard" | `cross-channel-performance` |
| "budget split", "how much per channel", "allocate ad budget" | `cross-channel-budget` |

### Other Channels & Content

| User intent / phrase | Route to |
|---------------------|----------|
| "Google UAC", "Google app campaigns", "Android Google ads" | `google-uac-campaign` |

## Multi-Skill Routing

When a request spans multiple skills, load them in this order:

| Compound request | Skills (in order) |
|------------------|-------------------|
| "TikTok ads from scratch" | `mmp-setup` → `app-ads-context` → `tiktok-campaign-setup` → `tiktok-creative-strategy` → `tiktok-spark-ads` |
| "Meta ad from my listing" | `meta-ad-creative` → `ad-creative-to-meta` |
| "Full paid growth plan" | `app-ads-context` → `cross-channel-budget` → channel setup skills |
| "Are my TikTok ads working?" | `tiktok-campaign-audit` → `campaign-profitability` |
| "Ads get clicks but no subs" | `tiktok-campaign-audit` or `meta-campaign-audit` → aso-skills `onboarding-optimization` → aso-skills `paywall-optimization` |
| "Beat competitor ads" | `competitor-ad-teardown` → `ad-creative-variants` → `ad-creative-to-meta` or `tiktok-creative-strategy` |
| "Scale what's working" | `campaign-profitability` → `cross-channel-performance` → channel audit/optimizer |
| "ASA + TikTok together" | `cross-channel-budget` → `asa-roas-analysis` + `tiktok-campaign-audit` |
| "First time running ads" | `app-ads-context` → `mmp-setup` → `cross-channel-budget` → one channel setup |
| "I spent $500 and nothing worked" | `campaign-profitability` → channel audit → `mmp-setup` (verify tracking) |

## Disambiguation Playbook

When intent is unclear, ask **one** question — never more.

| Signal | Question |
|--------|----------|
| "ads" without platform | "Which channel — **TikTok**, **Meta**, **Apple Search Ads**, or **all three**?" |
| "create ads" | "**Video ads** (TikTok) or **static/image ads** (Meta feed)?" |
| "not converting" | "Low **clicks** (creative problem) or clicks but no **purchases** (onboarding/paywall)?" |
| "ROAS" / "profitable" | "Do you want **per-channel CPA** (audit skill) or **LTV vs spend** (profitability skill)?" |
| "Apple Search Ads" + "TikTok" | "Set up **one channel first** (which?) or **compare existing performance**?" |
| "generate creative" | "**One ad** (meta-ad-creative) or **A/B batch** (ad-creative-variants)?" |
| "competitor" | "**Their paid ads** (competitor-ad-teardown) or **organic ASO** (aso-skills competitor-analysis)?" |
| "subscription app" + "ads" | "Have you completed **MMP setup** so TikTok/Meta can optimize for Purchase/Subscribe?" |

## Routing Anti-Patterns

Do not route to:

| Wrong route | Use instead | Why |
|-------------|-------------|-----|
| `tiktok-campaign-setup` | `tiktok-campaign-audit` | Setup vs performance review |
| `meta-ad-creative` | `tiktok-creative-strategy` | Static Meta API vs TikTok video |
| `campaign-profitability` | `mmp-setup` | Profitability assumes tracking works |
| `google-uac-campaign` | `tiktok-campaign-setup` | User said TikTok but you assumed Google |
| `asa-weekly-optimization` | `asa-roas-analysis` | Ops vs profitability question |
| `meta-campaign-setup` | `mmp-setup` | Never launch without MMP |
| aso-skills `ua-campaign` | Channel-specific skill here | UA overview lives in aso-skills; **execution** lives here |

## Output Template

```
→ Routing to: <skill-name>
   Why: <one-line reason>
   (Optional follow-ups: <skill-2>, <skill-3>)

[Then load and follow skills/<skill-name>/SKILL.md]
```

If you needed to ask a clarifying question first, ask it before the routing block.

## Context Check

Before routing into any skill except `app-ads-context`, check whether `app-ads-context.md` exists. If missing and the skill needs app/budget/CPA context (almost all do), suggest once per session:

> "Quick win: I can set up an app-ads-context doc first (~2 min) so every skill has your budget, target CPA, LTV, and connected accounts. Want me to?"

Also check `app-marketing-context.md` (aso-skills) — merge positioning if present.

## Boundaries — Route OUT to aso-skills

| User need | aso-skills skill |
|-----------|------------------|
| ASO audit, keywords, metadata | `aso-audit`, `keyword-research`, `metadata-optimization` |
| Creator/influencer programs (organic) | `creator-ugc-marketing` |
| Deep SKAN / ATT / MMP debug | `attribution-setup` |
| ASA strategy (not API ops) | `apple-search-ads` |
| UA channel overview (not execution) | `ua-campaign` |
| Paywall, onboarding fixes | `paywall-optimization`, `onboarding-optimization` |

## When NOT to Use This Skill

If the user explicitly invokes a skill (`/tiktok-campaign-setup`, `/meta-ad-creative`, etc.), skip this router and load that skill directly. The router is for ambiguous natural-language requests only.
