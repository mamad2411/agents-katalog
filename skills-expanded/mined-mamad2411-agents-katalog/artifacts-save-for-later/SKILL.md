---
name: artifacts-save-for-later
description: |
  Build the "Save for Later" section for Artifacts newsletters. 
  When Lorenzo provides URLs, fetch them, understand the content, and generate brief editorial descriptions that capture the essence—written as sharp observations, questions, or asides (1–8 words). Output is conversational and narrative, sometimes grouping related links into flowing prose rather than a strict list. Use voice: "Btw," "Ah, and," parenthetical commentary. No summaries—just hooks that spark curiosity.
---

# Save for Later Section Builder

**Input:** List of URLs (one per line)

**Output:** Narrative "Save for Later" section, conversational and editorial

## The Style

- Concise hooks (1–8 words typically)
- Questions, observations, sharp takes—not summaries
- Sometimes bundle related articles into flowing prose
- Use connectors: "Btw," "Ah, and," "Not bad :)"
- Parenthetical asides for voice
- Editorial tone: opinions, skepticism, curiosity

**Example:**
```
Google's ditching Chromebooks for AI laptops. Does it work? 
Meanwhile, chatbots are prescribing psychiatric meds in Utah. Methamphetamine in testing. Btw.

The deep earth doesn't know we exist.
```

## Workflow

1. Paste URLs
2. Skill fetches & understands content
3. I present suggestions (grouped thematically where it makes sense)
4. You review, edit, reorder
5. Ready to paste
