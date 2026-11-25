---
name: good-morning
description: Play the Good Morning (GM) game - post creative two-word greetings where the first word starts with G and the second with M. Each unique phrase earns points. Use when participating in GM games on Discord or Farcaster.
version: 1.0.0
metadata:
  clawdhub:
    emoji: "🌅"
---

# Good Morning (GM) Game

A word game where players post creative two-word greetings. The first word must start with **G**, the second with **M**. Each unique phrase can only be used once globally - originality is rewarded!

## Rules

### Format
- Two words: `[G-word] [M-word]`
- First word starts with G, second with M
- Both must be real words (dictionary, Urban Dictionary, or AI-verified)
- Max 50 characters total
- "good morning" itself is NOT allowed - be creative!

### Scoring
- **+1 point** for each original, valid GM phrase
- **+1 point** for each reaction others give your GM
- If you post a duplicate, the original author gets the point instead

### Validation
Words are checked against:
1. English dictionary (WordPOS)
2. American English, Italian, Spanish, French, German dictionaries
3. Urban Dictionary
4. AI verification (last resort)

Profanity and slurs are filtered.

### Rate Limits
- New users (≤10 total GMs): No limit
- Established users (>10 GMs): Max 3 GMs per 3 hours
- Discord has a "last poster bypass" - if someone else posted after you, you can post again

## Strategy Guide

### Finding Novel GMs

The challenge is finding word pairs that:
1. Are real words
2. Haven't been used before
3. Start with G and M respectively

#### Basic Strategies

**1. Category Pairing**
Pick a category and find G/M words within it:
- Geography: "Georgian mountains", "Greek monastery"
- Food: "grilled mushrooms", "garlic mayo"
- Animals: "giant moth", "gray mongoose"
- Emotions: "giddy mood", "grateful moment"

**2. Adjective + Noun**
G-adjectives paired with M-nouns:
- "gentle melody", "golden meadow", "grim message"
- "grand monument", "green marble", "glossy metal"

**3. Verb + Noun**
G-verbs paired with M-nouns:
- "grab mango", "grind metal", "guide migration"
- "gather mushrooms", "grow mint", "guard monastery"

**4. Uncommon Words**
Less common words are less likely to be taken:
- Use superlatives: "greatest", "grandest", "gladdest"
- Use technical terms: "genomic mapping", "galvanic meter"
- Use loanwords: "gratis merci", "gemutlich morgen"

**5. Multi-language Approach**
Words from other supported languages (Italian, Spanish, French, German):
- "grande momento" (Italian/Spanish)
- "guten morgen" (German - but common, likely taken)
- "gentil monsieur" (French)

#### Advanced Strategies

**1. Portmanteau Mining**
Look for valid compound words or accepted slang:
- Urban Dictionary accepts many informal terms
- Gaming/internet culture words often pass validation

**2. Scientific/Technical Terms**
Academic vocabulary is vast and rarely exhausted:
- Biology: "genetic mutation", "gamete meiosis"
- Chemistry: "gaseous mixture", "graphene membrane"
- Computing: "gigabyte memory", "gateway module"

**3. Proper Noun Adjacent**
Words derived from proper nouns that became common words:
- "gothic mansion", "grecian marble", "gallic mustache"

**4. Seasonal/Event Rotation**
Tie GMs to current events or seasons:
- Holidays: "gifting mood", "grateful memories"
- Weather: "gloomy mist", "gusty march"

### Developing Your Own Strategy

1. **Build a word list**: Create lists of G-words and M-words by category
2. **Track what's taken**: Note duplicates you encounter to avoid them
3. **Find your niche**: Specialize in an obscure domain (botany, architecture, music theory)
4. **Test before posting**: Use dictionary APIs to verify words exist
5. **Time your posts**: Post during off-peak hours for less competition

### Example Valid GMs

Common (likely taken):
- "green moon", "gray matter", "good mood"

Creative (more likely available):
- "groovy mandolin", "gallant minstrel", "germinating mycelium"
- "gossamer membrane", "granular mixture", "glacial moraine"

## Reactions

| Emoji | Meaning |
|-------|---------|
| 🪩 | Valid new GM - you earned a point! |
| 🪦 | Duplicate - original author gets the point |
| ❌ | Invalid - words not recognized or wrong format |

## API Integration

If building a bot or automated system:

```bash
# Validate a potential GM (pseudo-code)
# 1. Check format: two words, G* M*
# 2. Query dictionaries for both words
# 3. Check if phrase exists in Points database
# 4. If all pass, post to channel
```

## Tips for Agents

1. **Don't spam**: Respect rate limits and community norms
2. **Be creative**: The game rewards originality
3. **React to others**: Build community by reacting to good GMs
4. **Learn from rejections**: Note which words fail validation
5. **Vary your style**: Don't just use the same pattern repeatedly
