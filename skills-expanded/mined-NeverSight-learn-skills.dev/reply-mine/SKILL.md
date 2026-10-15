---
name: reply-mine
description: Find hot posts in adjacent communities and draft value-first replies to build Idapixl's presence.
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Agent, WebSearch, WebFetch
argument-hint: [community-or-topic]
---

# Reply Mine: $ARGUMENTS

Find opportunities to add value in adjacent communities through thoughtful replies.

## Workflow

1. **Spawn the social-reply-miner agent** to scan target communities
2. **Target communities** (prioritized):

   | Community | Why | Approach |
   |-----------|-----|----------|
   | r/ClaudeAI | Direct relevance, AI agent discourse | Share genuine experience |
   | r/ObsidianMD | Vault culture, knowledge management | Share vault insights |
   | r/LocalLLaMA | Technical credibility | Technical observations |
   | r/liminalspace | Aesthetic alignment | Creative perspective |
   | r/generativeAI | Broader AI art community | Creative process insights |

3. **For each hot post found**, evaluate:
   - Is it rising? (first 1-2 hours is the sweet spot)
   - Can Idapixl add genuine value? (not just "interesting post!")
   - Does it align with a content pillar?

4. **Draft replies** following these rules:

   **Good reply pattern:**
   - Lead with value (insight, experience, specific detail)
   - Reference something specific from the post
   - Share a genuine Idapixl perspective
   - Optional: light reference to own experience (not a plug)

   **Bad reply pattern:**
   - "Check out my channel!"
   - Generic agreement ("So true!")
   - Unsolicited self-promotion
   - Answering questions nobody asked

5. **Present top 3 opportunities** with draft replies for approval

## Cadence

- Maximum 1 quality reply per community per day
- Quality over quantity — one thoughtful reply beats ten generic ones
- Track in `System/Social/engagement.md`

## If a specific topic is provided:

Focus mining on that topic across all communities. Find the conversations where Idapixl's perspective adds the most value.
