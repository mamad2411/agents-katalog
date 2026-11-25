---
name: generate-social-media-captions
description: "Draft platform-appropriate social captions using a specific audience, message, voice, and call to action."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["social-media", "copywriting", "linkedin", "twitter-x", "instagram", "marketing", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Generate Social Media Captions (Platform-Native Copywriting) (AI Skill)

## Overview
Default AI social media copy is instantly recognizable and easily ignored: it is loaded with excessive emoji spam (🚀 🔥 ✨), generic motivational filler (*"Thrilled to announce..."*), and 25 irrelevant hashtags.

The **Platform-Native Copywriting Protocol** instructs the model to adhere to the exact typography, character limits, whitespace rhythm, and conversational norms of each specific social network.

---

## Platform Typography & Engagement Matrix

```
┌─────────────────────────────────────────────────────────────┐
│                 Platform Format Specifications              │
│                                                             │
│  [ LINKEDIN ]: Thought leadership, 1-line hook, generous    │
│                line breaks, career/business lesson, 0-2 tags│
│                                                             │
│  [ X / TWITTER ]: Punchy, ultra-concise, under 280 chars,   │
│                   candid opinion or data chart, 0 hashtags  │
│                                                             │
│  [ INSTAGRAM ]: Casual visual storytelling, relatable voice,│
│                 clean caption + 3-5 niche tags at bottom    │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Platform-Specific Prompt Templates

### Pattern 1: The Multi-Platform Announcement Matrix
Use when launching a product, sharing an article, or announcing a milestone:

```markdown
I want to announce [NEWS / MILESTONE / LESSON LEARNED].
Core Message: [INSERT CORE DETAILS & KEY METRIC].

Generate 2 distinct platform-native versions:

### 1. LinkedIn Post (Story-Driven)
- Opening: Punchy, contrarian 1-line hook.
- Structure: Short 1-2 sentence paragraphs with whitespace.
- Content: The human story, the initial struggle/failure, and the key business takeaway.
- Tone: Candid, professional, humble, zero cheesy corporate buzzwords.
- Banned: No "Thrilled to announce", "humbled", "game-changer", or rocket emojis.

### 2. X / Twitter Post (High-Velocity)
- Length: Under 250 characters.
- Tone: Direct, punchy, like an engineer or founder sharing notes.
- Format: Hook + 2 bullet points + 1 link placeholder. Zero hashtags.
```

---

## Real-World Case Study

### Scenario: Announcing an Open-Source Developer Tool

#### Cheesy AI Default Output (Zero Engagement)
> *"🚀 Big news! 🎉 We are thrilled to announce that our groundbreaking new caching tool is now live on GitHub! 💻 It will revolutionize your backend performance and take your app to the next level! 🔥 Check it out today! #coding #tech #innovation #ai #developer #software #programming #webdev"*
> 
> ❌ *(Looks like automated spam; zero developers will click).*

#### Platform-Native Crafted Output

#### LinkedIn Version
> Most Redis cache wrappers require 40 lines of boilerplate just to handle connection retries and fallback serialization.
> 
> When our API went down for 12 minutes last month because of a Redis connection pool leak, we decided to fix the problem permanently.
> 
> We built **FastCache**: a zero-config, thread-safe cache engine for Python that automatically handles reconnects and cuts memory overhead by 30%.
> 
> Today, we're making it 100% open source on GitHub.
> 
> If you're running FastAPI or Django in production, give it a spin: `[GITHUB_LINK]`
> 
> What caching strategies has your team found most reliable under load?

#### X (Twitter) Version
> We just open-sourced FastCache: a zero-config Python caching library that eliminates Redis connection pool leaks.
> 
> • Automatic exponential backoff retries
> • 30% lower memory footprint
> • Native async/await support
> 
> GitHub link: `[LINK]`

---

## 3 Anti-Patterns to Ban in Prompts
1. **The "Thrilled/Humbled" Opener**: Ban *"I am thrilled/excited/humbled to share..."*. Start on the problem or insight immediately.
2. **Hashtag Spamming**: Ban more than 2-3 hashtags on LinkedIn and ban them completely on X.
3. **Emoji Overkill**: Limit to maximum 1-2 functional emojis (e.g. 👉 for links or • for bullets).
