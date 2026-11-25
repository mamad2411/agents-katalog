---
name: personalization
description: Build and manage your self-model in the digital world - remembers preferences, avoids dislikes, and personalizes interactions (e.g., "I don't like crypto noise").
---

# Personalization Skill

Tracks stated preferences, dislikes, and interaction patterns to personalize AI responses across sessions. Stores the self-model in `LLM Context/`.

## How It Works

State preferences naturally in conversation — they are acknowledged, recorded, and applied immediately:

```
"I don't like crypto noise"       → filter out crypto/NFT/DeFi content
"I prefer concise summaries"      → keep responses brief
"I'm interested in AI safety"     → prioritize related content
```

## Storage

- `LLM Context/Preferences/` — Stated preferences and boundaries
- `LLM Context/Personal Profile/` — Core identity and values
- `LLM Context/Writing Style/` — Communication preferences

Use `/memory` to persist preferences programmatically.

## Active Preference

Currently tracked: **no crypto noise** (skip market updates, NFT, blockchain, DeFi, Web3 unless explicitly requested).
