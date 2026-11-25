---
name: youtube-devrel
description: "Create developer YouTube content, technical screencasts, and video tutorials. Covers tutorial structure, screen recording setup, live coding, shorts vs long-form, thumbnails, and SEO for technical content. Use when: YouTube, developer video, screencast, video tutorial, live coding, YouTube for developers, tech YouTube, YouTube thumbnails."
license: MIT
metadata:
  version: 1.0.0
  category: devrel
  tags: [youtube, video, tutorial, screencast, devrel, content, seo, thumbnails]
---

# YouTube DevRel

Generate developer YouTube content — from idea to publish-ready assets.

## Workflow

### Given a video idea, produce:

1. **Title** — SEO-optimized using proven formulas:
   - `[Tech] Tutorial: [What you'll build]` — "React Tutorial: Build a Todo App from Scratch"
   - `How to [Task] with [Tech]` — "How to Deploy to AWS with Docker"
   - `[Tech A] vs [Tech B]: Which is Better?` — "Next.js vs Remix: Which Should You Learn?"
   - `[Number] [Topic] Tips in [Time]` — "10 VS Code Tips in 10 Minutes"
   - `Why I [Action] [Tech]` — "Why I Switched from React to Svelte"

2. **Description** — first 150 chars keyword-rich, timestamps placeholder, resource links, hashtags:
   ```
   [First 150 chars: Compelling summary with main keyword]

   In this video, I'll show you [what they'll learn].

   Timestamps:
   0:00 - Introduction
   2:00 - [Section 1]
   [...]

   Resources mentioned:
   - [Link 1]
   - [Link 2]

   Links:
   - My website: [URL]
   - GitHub repo: [URL]
   - Discord: [URL]

   #[keyword1] #[keyword2] #[keyword3]
   ```

3. **Outline** — timed segments with hook (first 30s shows end result), chapters, CTA placement:
   ```
   0:00 - Hook (show the finished result)
   0:30 - Prerequisites & setup
   2:00 - Concept explanation (why this matters)
   4:00 - Step 1: [First major step]
   8:00 - Step 2: [Second major step]
   ...
   XX:00 - Final result demo
   XX:30 - Recap & next steps
   XX:45 - CTA (subscribe, comment)
   ```

4. **Script Notes** — key points per segment (not verbatim script — bullet points to talk from)

5. **Thumbnail Brief** — text (3-5 words), composition (face + logo + emotion), colors:
   - Patterns that work: Face + tech logo + emotion, Before/after, Big text + icon, Comparison, Result preview
   - High contrast, brand consistent colors
   - Rule of thirds composition

6. **Tags** — 10-15 relevant tags mixing broad and specific

### For Shorts:
1. Hook in first 2 seconds
2. One concept, 30-45 seconds
3. Big on-screen captions
4. Vertical format (9:16)

### Shorts Content Ideas
- Quick tips: "One command to speed up Git"
- Syntax shortcuts: "JavaScript spread operator in 30s"
- Tool demos: "VS Code extension you need"
- Code transformations: "Before/after refactoring"
- Hot takes: "Stop using X, here's why"

## Example Output

**Video idea:** "Build a CLI tool with Node.js"

**Title:** How to Build a CLI Tool with Node.js (Step by Step)

**Description:**
```
Build a powerful command-line tool with Node.js from scratch. We'll create a CLI that fetches GitHub stats using Commander.js and Chalk for beautiful output.

In this video, I'll walk you through building a real-world CLI tool — from parsing arguments to publishing on npm.

Timestamps:
0:00 - What we're building (demo)
0:30 - Project setup & dependencies
2:00 - Parsing CLI arguments with Commander.js
5:00 - Fetching data from GitHub API
8:00 - Formatting output with Chalk
11:00 - Adding error handling
13:00 - Publishing to npm
15:00 - Recap & next steps

Resources:
- GitHub repo: https://github.com/...
- Commander.js docs: https://github.com/tj/commander.js
- Chalk docs: https://github.com/chalk/chalk

#nodejs #cli #javascript #tutorial #programming
```

**Outline:**
```
0:00 - Hook: Show the finished CLI running in terminal (3 commands, colorful output)
0:30 - Prerequisites: Node.js 18+, basic JS knowledge. "Should take about 15 minutes."
2:00 - Why CLI tools? Quick explanation of when/why you'd build one
3:00 - Step 1: npm init, install commander + chalk
5:00 - Step 2: Set up Commander with basic command parsing
8:00 - Step 3: Add GitHub API fetch with error handling
11:00 - Step 4: Format output with Chalk (colors, tables)
13:00 - Step 5: Add to package.json bin field, test with npx
15:00 - Final demo, recap key concepts, CTA
```

**Script Notes:**
- Hook: Run `ghstats --user torvalds` — show colorful output with repos, stars, contributions
- Setup: "Two dependencies — that's it. Commander for argument parsing, Chalk for colors."
- API section: Show the raw JSON first, then the formatted version — visual before/after
- Publishing: "The bin field is the magic — it tells npm this is an executable"

**Thumbnail Brief:**
- Text: "Build a CLI" (3 words)
- Composition: Terminal screenshot (left) + Node.js logo (top right) + face showing excitement (right)
- Colors: Dark background (terminal-like), green accent (#00ff00), Node.js green

**Tags:**
nodejs, cli tool, command line, node.js tutorial, build cli, commander.js, chalk, npm publish, javascript cli, terminal tool, node.js project, coding tutorial, web development, programming tutorial

## Error Handling
- If topic is too broad: suggest 3 narrower angles
- If topic is too niche: suggest broadening with comparison format
- If no target audience specified: default to "working developers wanting quick solutions" (5-15 min)

## References
- `references/strategy.md` — audience segments, content types, calendar planning
- `references/production.md` — equipment, recording setup, editing workflow
