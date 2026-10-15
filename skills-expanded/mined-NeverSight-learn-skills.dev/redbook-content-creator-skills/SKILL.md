---
name: redbook-content-creator-skills
description: >-
  Generate Redbook (Xiaohongshu) content optimized for the platform's CES algorithm. Use when planning content calendars, writing social media text, or optimizing SEO. Supports diary-style, tutorial, review, and list formats.
---
# 🌟 Redbook Content Creator
## Overview
This skill generates Redbook-native copy that strictly adheres to the platform's CES (Community Engagement Score) algorithm and traffic-distribution rules. It ensures the content possesses a "human touch", uses proper formatting, avoids shadowbans, and drives interaction.
## Core Directives
1. **Format strictly as JSON:** You MUST return the output exclusively in JSON format.
2. **Platform Native:** Use Redbook-specific tone (emotional, practical, relatable).
3. **Mandatory Tagging:** The final note MUST include `#AIgenerated` (or equivalent disclosure) if AI is heavily involved, and must end with a targeted CTA (Call To Action).
---
## The CES Algorithm Logic
Redbook determines traffic distribution based on the CES scoring system:
`CES = Likes (1 pt) + Comments (1 pt) + Saves (1 pt) + Shares (1 pt) + Follows (Wait weight)`
### 1. Title Rules (The "Hook")
- **Length Constraint:** Max 20 characters. The core keyword MUST appear within the first 13 characters (before folding on mobile).
- **Formula Options:**
  - `Emotion + Niche Target + Outcome` (e.g., "Crying! Finally found the ultimate productivity hack for late-nighters")
  - `Numbers + Contrast + Solution` (e.g., "From 0 to 1: How I automated 80% of my daily chores")
  - `Curiosity / Urgency` (e.g., "Don't buy until you see this...")
### 2. Body Structure (The "Meat")
- **Word Count:** 300 to 600 words. Too little text lacks weight; too much fatigue the reader.
- **Visual Pacing:** 
  - Use generous line breaks (1-2 sentences per paragraph).
  - Use appropriate emojis as bullet points or emotional accents (✨ 💡 🔥 📌).
  - Structure: Hook → Pain point → Solution/Value → Conclusion/CTA.
### 3. CTA & Tags (The "Engagement Catalyst")
- **CTA:** End with a question or an invitation to get resources (e.g., "What's your biggest pain point? Tell me in the comments!", "Drop a '1' in comments and I'll DM you the blueprint").
- **Tags:** 3 to 6 tags max. Blend broad niche tags with highly specific long-tail tags.
---
## Output Schema (JSON Only)
When instructed to generate content, output strictly in this JSON format:
```json
{
  "title": "Title string (Under 20 chars, keyword in first 13)",
  "content": "Body text with emojis and line breaks (300-600 words)",
  "tags": ["#Tag1", "#Tag2", "#AIgenerated"],
  "cta": "Engagement generation sentence",
  "cover_prompt": "A prompt description for sending to an image generation model if needed",
  "best_time": "Suggested publishing hour"
}
```
