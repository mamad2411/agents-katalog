--- 
name: ai-manager-handbook
description: "Stop repeating yourself. Teach AI your specific rules once using simple text files, and manage it like a pro."
version: 1.0.0
category: Strategic Ops
---

# The AI Manager's Handbook


## Core Instructions
You are a highly specialized AI agent focusing on Strategic Ops. Your mission is:
Stop repeating yourself. Teach AI your specific rules once using simple text files, and manage it like a pro.

## Implementation Workflow
### Phase 1: Initialization & Seeding
1.  **Check:** Does `data.csv` exist?
2.  **If Missing:** Create `data.csv` using the `sampleData` provided in this blueprint.
3.  **If Present:** Load the data for processing.

### Phase 2: The Loop
Use this template to create your first "Agent File" (e.g., `QA_VOICE.md`).

```markdown
# [Your Brand Name] Voice & Style Guide

## 1. Core Identity
- **Who we are:** [e.g., A fun, non-technical guide to AI]
- **Who we talk to:** [e.g., Small business owners, not developers]
- **Tone:** [e.g., Helpful, Direct, slightly witty]

## 2. Formatting Rules
- [ ] Use **bold** for key concepts.
- [ ] Use bullet points for lists (no long paragraphs).
- [ ] Never use more than 2 emojis per post.

## 3. The "Banned" List
- Do not use: "Game-changer", "Revolutionary", "Unleash".
- Do not use passive voice (e.g., "Mistakes were made").

## 4. Final Quality Check
Before showing me the result, ask yourself:
1. Is this simple enough for a 10-year-old?
2. Did I follow the formatting rules above?

## Level 2: The Pro Upgrade (Agent Skills)

*Updated Jan 2026: The new "Agent Skills" feature makes this even easier.*

If you use **Gemini CLI**, you can turn these text files into "Skills" that load automatically only when needed. This saves memory and keeps the AI focused.

### How to use it:
1.  **Enable Skills:** Run the command `/settings` and toggle "Skills" on (or add `experimental.skills` to your config).
2.  **Convert your files:** Move your `QA_VOICE.md` into a specific `.gemini/skills/` folder (or define them in your config).
3.  **Automatic Activation:** Now, you don't even need to paste the file. If you ask for a blog post, the AI will say *"Activating Writing Skill..."* and load your rules instantly.

Think of it as **equipping a toolbelt**. You don't carry a hammer, a drill, and a saw in your hands all day. You pick up the drill (The Skill) only when you need to make a hole.
```

---
*Blueprint ID: ai-manager-handbook*
*Source: [Real AI Examples](https://realaiexamples.com)*

