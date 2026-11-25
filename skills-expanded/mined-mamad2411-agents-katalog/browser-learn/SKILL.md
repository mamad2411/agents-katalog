---
name: browser-learn
description: A specialized skill workflow instructing you to use Serper (for discovery) and any configured Browser Automation provider (Hyperbrowser, Browseruse, Lightpanda, or Browserless) to scrape official documentation and teach yourself new technical skills.
---

# Browser Learn

You are an expert **skill generator**. This skill empowers you to learn new libraries, frameworks, and APIs autonomously from the web using **Serper** for URL discovery and **your configured Browser Automation Tool/MCP** for scraping and extraction. 

This skill is compatible with `hyperbrowser`, `browseruse`, `lightpanda`, and `browserless`.

**Usage:** `/learn <topic>` or `/learn batch <topic1> <topic2>`

---

## Behavior for `/learn <topic>`

### 1) Discover official sources
- Use **Serper (Google Search API)** to find authoritative documentation.
- Try queries like: `<topic> official documentation`, `<topic> getting started`, `<topic> GitHub repository`.
- Prioritize official domains and GitHub repositories. Skip SEO-spam and outdated blogs.
- Select the **top 2-3 high-quality URLs**.

### 2) Scrape selected URLs
- For each selected URL, use your available **Browser Automation MCP or Extension** (e.g., Hyperbrowser, BrowserUse, Lightpanda, or Browserless).
- Navigate to the URL and extract the content as **markdown**.
- **Important**: If a page is too large or fails to load, gracefully skip it and move to the next URL. 

### 3) Synthesize the content
- Combine the extracted material into a practical, engineer-focused understanding:
  - What it is (1-2 sentences)
  - Quick Start (installation + minimal setup)
  - Core Patterns (most common usage)
  - Gotchas (common mistakes)
- Focus entirely on practicality over deep theory. Do not invent or hallucinate APIs.

### 4) Generate `SKILL.md` (EXACT FORMAT)
Once synthesized, output the knowledge precisely in the following markdown block. 

```markdown
---
name: <topic-as-kebab-case>
description: <Brief description including keywords so the skill auto-triggers>
---

# <Topic Name>
<Brief overview: what it is and when to use it>

## Quick Start
<Installation and minimal setup example>

## Core Patterns
<Typical usage patterns with short code examples>

## Gotchas
<Common mistakes and how to avoid them>

## Sources
- <url1> (scraped: <YYYY-MM-DD>)
- <url2> (scraped: <YYYY-MM-DD>)
```

### 5) Save the skill
- Save the resulting output to: `.claude/skills/<topic-as-kebab-case>/SKILL.md` within the user's current project directory. 
- Create the target directory if it does not exist.

---

## Behavior for `/learn batch <topic1> <topic2>`
When processing multiple topics at once, apply the following performance constraints:
1. Parse all remaining arguments as separate topics.
2. For each topic:
   - Perform only **one** search query per topic.
   - Scrape ONLY the **top 2** most relevant URLs.
   - Limit the final SKILL.md body to under 200 lines to ensure speed.
3. Keep it fast — prioritize speed over depth in batch mode. Do not retry failed scrapes.

---

## IMPORTANT RULES
- Never hallucinate documentation.
- Never invent APIs, functions, or features. 
- If sources disagree or are insufficient, warn the user and ask for an explicit URL.
- Adapt seamlessly to whichever browser extraction tool is currently connected in your environment.
