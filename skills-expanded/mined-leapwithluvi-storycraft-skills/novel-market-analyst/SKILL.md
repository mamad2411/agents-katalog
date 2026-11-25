---
name: novel-market-analyst
description: "Use to analyze commercial viability, reader demographics, and genre trends across physical print and digital novel platforms (Royal Road, Webnovel, Wattpad, Amazon KDP, KBM/Fizzo, Substack) — formulates platform positioning, monetization models, and conducts competitive market research."
version: "1.0.0"
category: "ideation"
stage: 1
tags: ["novel", "fiction", "market-analysis", "publishing", "webnovel", "kdp", "royal-road", "wattpad", "monetization", "trends"]
---

# Overview & Purpose

This skill bridges the critical gap between literary craft and publishing reality. A brilliant manuscript published on the wrong platform or miscalibrated for that platform's readership algorithm is doomed to obscurity. Publishing physical books through traditional gatekeepers requires radically different length, pacing, and prose styling than serialized webnovels on Royal Road, paywalled romance on KBM/Fizzo, or algorithmic series on Amazon Kindle Unlimited.

The agent uses this skill to:
- Conduct **Publishing Platform Alignment Audits** across 6 major publishing ecosystems (Traditional Print, Serialized Global Webnovels, Romance/Drama Apps, Southeast Asian Paywall Platforms, Amazon KDP/KU, and Direct Substack/Patreon models).
- Analyze **Platform-Specific Reader Demographics & Top Trending Genres** to calibrate tropes, chapter lengths, and release cadence.
- Execute **Competitive Market & Web Research** (utilizing search or browser subagents when permitted) to inspect current bestseller charts, Royal Road "Rising Stars", Amazon category ranks, and reader review sentiments.
- Synthesize findings into a formal **Market & Distribution Strategy Document** stored in `docs/storycraft/market-analysis.md`.

## When to Use & Trigger Phrases

**Activate this skill when:**
- Choosing where and how to publish a novel (Traditional agent querying vs. Webnovel vs. Amazon KDP vs. Wattpad).
- Adapting an existing manuscript from one format to another (e.g., converting a traditional 90k novel into a serialized Royal Road webnovel or Kindle series).
- Researching current reader trends, top tropes, and tag algorithms for specific platforms.
- Designing a monetization strategy (Advance Patreon chapters, pay-per-chapter coins, Kindle Unlimited page-reads, or print advances).
- Calibrating chapter lengths, cliffhanger frequency, and upload schedules before drafting begins.

**Example trigger phrases:**
- "Where should I publish this novel?"
- "Analyze the market trends for my LitRPG / Dark Romance story"
- "How do I optimize this novel for Royal Road / Webnovel / Wattpad / KDP?"
- "Compare traditional print publishing vs digital serialization for my fantasy book"
- "Research trending tags and comp titles on the web for my genre"
- "/novel-market-analyst"

## Core Literary Methodology & Rules

### 1. The Global Publishing Matrix: 6 Commercial Ecosystems

#### A. Traditional Physical Print & Trade Publishing
- **Target Venues**: Major Publishers (Penguin Random House, HarperCollins, Tor, Gramedia, Mizan) & Reputable Indie Presses.
- **Audience Demographics**: Broad commercial book buyers, library patrons, physical bookstore browsers.
- **Word Count Benchmark**: 70,000–100,000 words (Sci-Fi/Epic Fantasy: 90,000–120,000; Romance/Mystery: 65,000–85,000).
- **Chapter Architecture**: 2,800–4,500 words per chapter. 3-Act or 7-Point structure. Deep interiority and line-level prose polish.
- **Monetization**: Author advances against royalties (typically 6%–15% net). Long production cycles (12–24 months).

#### B. Global Progression & Male-Skewed Webnovels (Royal Road, ScribbleHub)
- **Target Venues**: Royal Road, ScribbleHub, SpaceBattles.
- **Dominant Top Genres**: LitRPG, Progression Fantasy, Cultivation/Xianxia, Isekai, Time Loops, Dungeon Defense, Sci-Fi Strategy.
- **Audience Demographics**: Gamers, anime/manga fans, male-skewed (65%+), tech-literate, analytical readers who love numbers, skill trees, and power scaling.
- **Chapter Architecture**: 1,800–2,500 words per chapter. Release cadence: 3 to 5 chapters per week.
- **Monetization Engine**: Free public release on platform $\rightarrow$ Patreon advance chapters (10–20 chapters ahead, earning $2,000–$20,000+/month) $\rightarrow$ Audiobooks (Audible) + Amazon KDP Boxsets.

#### C. Global Romance & New Adult Serial Platforms (Wattpad, Radish, Yonder)
- **Target Venues**: Wattpad, Radish, Yonder, Inkitt.
- **Dominant Top Genres**: Dark Romance, Enemies-to-Lovers, Mafia Romance, Billionaire/CEO, Werewolf/Alpha, College/Young Adult, LGBTQ+.
- **Audience Demographics**: Female-skewed (75%+), Gen Z & Millennial, highly emotional, community-driven, active in-paragraph commenting.
- **Chapter Architecture**: 1,500–2,500 words. Fast dialogue, visceral emotional stakes, heavy aesthetic visual cues.
- **Monetization Engine**: Wattpad Paid Stories, Webtoon adaptations, print crossover deals, Galatea licensing.

#### D. Southeast Asian & Asian Micro-Transaction Platforms (KBM App, Fizzo, Innovel, GoodNovel, Dreame)
- **Target Venues**: KBM App (Indonesia), Fizzo, Innovel/Dreame, GoodNovel, NovelMe, Mangatoon.
- **Dominant Top Genres**: Domestic Melodrama (Mertua vs Menantu, Pelakor/Perselingkuhan, Istri Teraniaya Balas Dendam, Pernikahan Kontrak), Konglomerat Menyamar, Pendekar Reinkarnasi.
- **Audience Demographics**: Mobile-first, Southeast Asian readers (Indonesia, Philippines, Vietnam), high daily screen time.
- **Chapter Architecture**: 1,000–1,600 words per chapter. Pacing is relentless; Chapters 1–5 must hook readers before the coin paywall.
- **Monetization Engine**: Pay-per-chapter coin unlocking, reader tips, platform author incentive contracts.

#### E. Direct Digital Self-Publishing (Amazon KDP & Kindle Unlimited)
- **Target Venues**: Amazon Kindle Store, Kindle Unlimited (KU).
- **Dominant Top Genres**: Psychological Thriller, Paranormal Romance, Urban Fantasy, LitRPG/Harem, Cozy Mystery, Space Opera.
- **Audience Demographics**: Avid Kindle readers reading 5–15 books per month; KU subscribers.
- **Word Count Benchmark**: 50,000–80,000 words per installment. Series continuity (3 to 10+ books).
- **Monetization Engine**: KDP Select Page-Reads (KENP) paying ~$0.004 per page read + 70% ebook royalties. Rapid release every 45–90 days.

#### F. Direct Newsletter & Patronage Serial (Substack, Ream, Patreon)
- **Target Venues**: Substack, Ream Stories, Patreon.
- **Dominant Top Genres**: Literary Serial, Author-Direct Fantasy, Deep Lore Universes.
- **Monetization Engine**: Direct recurring monthly memberships ($5–$25/month). 100% owned email list.

### 2. The Algorithmic Retention Formula
Regardless of platform, digital fiction lives or dies on early chapter retention curves:
- **Chapter 1 Drop-off**: If more than 30% of readers abandon at Chapter 1, the opening hook lacks immediate sensory friction or stakes.
- **The Paywall / Subscription Chokepoint**: The chapter immediately preceding a paid tier must end on a devastating cliffhanger or massive narrative revelation.
- **The Update Cadence Multiplier**: Algorithms reward consistent release rhythms. 3 chapters per week released on Mon/Wed/Fri outperforms a 10-chapter dump once a month.

### 3. Live Web Research Protocol (When Permitted)
When connected to web search or browser capabilities, the agent executes targeted queries:
1. Search current top rankings in the target genre (e.g., `"Royal Road Rising Stars LitRPG"`, `"Amazon Bestseller Cozy Mystery"`, `"Wattpad hot list enemies to lovers"`).
2. Examine reader reviews on top comps: What are readers praising? What tropes are they complaining are "tired" or "annoying"?
3. Extract successful keyword tags and blurb formulas.

## Required Project State & Inputs

**Before executing this skill, check for:**
- `story-bible.md` (genre, premise, target word count).
- `story-state.md` (active format setting).
- The author's personal goals: Is the primary goal maximum readership volume, passive monthly income, artistic literary prestige, or traditional bookstore distribution?

**If no inputs exist:** Ask the author about their publishing ambitions, target audience, and preferred reading platforms.

## Step-by-Step Execution Protocol

1. **Step 1: Diagnose the Author's Publishing Goal**
   - Identify whether the author targets **Prestige/Traditional Print**, **Serialized Web Subscription (Patreon/RR)**, **KDP/KU Series**, or **Asian Micro-Transaction (KBM/Fizzo)**.

2. **Step 2: Competitive Market Mapping**
   - Cross-examine the premise against the 6 Commercial Ecosystems.
   - Match the novel's core tropes with the platform where that trope commands the highest hungry readership.

3. **Step 3: Web & Trend Intelligence (If Enabled)**
   - Query top comp titles published within the last 12–24 months in that niche.
   - Analyze average chapter length, release frequency, and cover/blurb tropes.

4. **Step 4: Establish Publishing Parameters**
   - **Target Platform(s)**
   - **Calibrated Chapter Length** (e.g., 2,000w for RR vs 3,500w for Traditional)
   - **Cliffhanger Frequency**
   - **Release Schedule** (e.g., 3x/week for 60 chapters)
   - **Monetization Funnel** (Patreon $\rightarrow$ Amazon KU $\rightarrow$ Audio)

5. **Step 5: Write `docs/storycraft/market-analysis.md`**
   - Save the full strategy document into the author's workspace.
   - Update `story-state.md` and `story-bible.md` with the confirmed publishing target.

## Quality Checklist & Verification Criteria

- [ ] Is the recommended platform genuinely aligned with the story's genre tropes and target demographic?
- [ ] Are chapter length and pacing targets calibrated specifically to the chosen platform?
- [ ] Is there a clear, actionable monetization and release cadence blueprint?
- [ ] Does the analysis cite concrete market mechanics (Patreon advance chapters, KDP KENP, pay-per-chapter coin thresholds)?
- [ ] Is the strategy saved cleanly to `docs/storycraft/market-analysis.md`?

## Anti-Patterns & Prohibited AI Tropes

- **The Universal 100k Novel Assumption**: Assuming every book must be an 80k-word physical paperback, ignoring the massive digital webnovel and serialized markets.
- **The Platform Mismatch**: Recommending Royal Road for a slow-burn billionaire domestic romance, or recommending KBM App for hard sci-fi space opera.
- **The Frictionless Success Fantasy**: Telling an author they will become rich instantly without explaining the rigorous release schedule and retention math required on digital platforms.
- **Ignoring Reader Comment Dynamics**: On serial platforms (Royal Road, Wattpad), readers comment on every paragraph; ignoring this social reading dynamic leads to alienating prose styles.

## Concrete Examples (Before vs. After Craft Application)

### Example 1: Market Strategy for a System Apocalypse Fantasy

**Before (Generic Publishing Advice):**
> You should write your system fantasy story and try to submit it to literary agents for print publication. If they reject it, you can put it on Amazon as an ebook for $2.99.

**After (Precision Multiplatform Market Analysis):**
> **Market Assessment for *The Iron Core Apocalypse***:  
> - **Primary Target Platform:** **Royal Road (Serialized)** $\rightarrow$ **Amazon KDP/KU & Audible (Phased Launch)**.  
> - **Demographic Alignment:** High overlap with the LitRPG/Progression Fantasy readership (male 18–35, high gaming literacy). A traditional publisher will reject this due to system stat blocks, but Royal Road readers consume this voraciously.  
> - **Chapter Length Calibration:** Exactly 2,000–2,400 words per chapter. Shorter chapters feel insubstantial; longer chapters hurt release cadence.  
> - **Release Cadence Strategy:**  
>   - *Pre-launch buffer:* Draft 30 chapters before launch.  
>   - *Week 1–2 (Launch Push):* Publish 1 chapter daily for 14 days to trigger the Royal Road "Rising Stars" list algorithm.  
>   - *Sustained Phase:* 3 chapters/week (Mon/Wed/Fri).  
> - **Monetization Funnel:**  
>   - Launch Patreon with 10 advance chapters at $5/mo tier and 20 advance chapters at $10/mo tier. Top comps in this niche convert 1.5%–3% of followers to Patreon.  
>   - After Volume 1 (Chapters 1–60, ~130k words) concludes on Royal Road: Stub earlier chapters and launch Book 1 on Amazon Kindle Unlimited + Audible audiobook.

## Session State Hook

When completing a market analysis:
1. Write the full analysis to `docs/storycraft/market-analysis.md`.
2. Update `story-state.md` under:
   - `**Target Publishing Format:** [Confirmed Platform & Chapter Target]`
3. Update `story-bible.md` under `## 1. Premise & Core Dramatic Question`.
4. Route the author to `novel-chapter-outline` or `novel-chapter-drafter` with calibrated word-count settings.
