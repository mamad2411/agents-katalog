---
name: wave
description: Quick web research (~60 sec) - fast lookups, Opus synthesis. Use for "quick lookup", "fast research", or any topic needing quick context.
user-invocable: true
---

# Searchwave

Quick web research synthesis in ~60 seconds.

## Overview

Single orchestrator, 3 parallel searches, 3 parallel fetches. Produces a
300-400 word summary with sources. No questions asked — receives topic and
runs immediately.

## When to Use

**Use /wave when:**
- User asks for "quick lookup" or "fast research"
- Need context before a meeting or decision
- Simple factual questions
- Time-sensitive requests

**Use /deepwave instead when:**
- User wants depth selection or priority focus
- Complex topics requiring multiple angles
- Need confidence assessment and source evaluation
- "Deep research" or "comprehensive" requests

**Use /firewave instead when:**
- JS-heavy sources (docs sites, SPAs, React apps)
- WebFetch has failed or returned incomplete content
- Need content from dynamic/rendered pages

## Variants

| Skill | Synthesis | Speed | Cost |
|-------|-----------|-------|------|
| `/wave` | Opus (model default) | ~60s | Higher |
| `/searchwave-sonnet:wave` | **Sonnet** | ~60s | Lower |
| `/deepwave` | Opus | 70s-10min | Higher |
| `/searchwave-sonnet:deepwave` | **Sonnet** | 70s-10min | Lower |

**Token-efficient alternative:** Install `searchwave-sonnet` from the marketplace for Sonnet synthesis variants.

## Execution

**Complete in 60 seconds. Dense facts, not fluff.**

### Step 0: Print banner

Print this banner immediately:
```
╔═════════════════════════════════════════╗
║           S E A R C H W A V E           ║
║                · · · · ·                ║
║      Searching: 3 parallel queries      ║
╚═════════════════════════════════════════╝
```

### Step 1: Search (3 parallel)

Fire 3 WebSearches in ONE message:
```
"[topic]"              → baseline
"[topic] interesting"  → non-obvious angles
"[topic] guide"        → actionable content
```

All searches use `blocked_domains: ["medium.com"]` — Medium never fetches usefully.

### Step 2: Curate (10 sec)

Pick 3 URLs. Prefer: gov/institutional, domain authorities, quality blogs.

Skip for fetching:
- Wikipedia (403s — use snippet from search results instead)
- Medium (blocked at search level — never useful)
- Paywalled sites
- SEO farms, outdated content

### Step 3: Fetch (3 parallel)

Fire 3 WebFetches in ONE message. If any fetch fails, proceed with available results — do not retry the full batch.

### Step 4: Write

**Adapt structure to topic. No rigid template.**

Always include:
- **Overview** — 2-3 sentences, plain language
- **Key Findings** — Specific numbers, names, thresholds. This is the meat.
- **Sources** — With one-line descriptions

Include ONLY if warranted:
- **Practical Takeaways** — If topic has actionable advice
- **Of Interest** — ONLY if genuinely surprising. Skip if straightforward.
- **Go Deeper?** — ONLY if topic clearly warrants more research

**Style:**
- Concrete > abstract
- Numbers > vague claims
- Useful > clever
- Skip sections that don't add value
- ASCII tables/diagrams when helpful for comparisons
- No --- dividers between sections
- Tight, scannable organization
- Inline citations for statistics: "According to X...", "One study found..."

**Avoid AI writing patterns:**
- No dramatic reframes or hyperbole
- Let facts speak; don't editorialize
- Be concise, lead with numbers

**Line width formatting (critical for terminal readability):**
- Prose paragraphs: hard-wrap at 80 columns
- Bullet lists: hard-wrap at 80 columns
- Tables: NO width limit (columns break if wrapped)
- Code blocks: NO width limit
- ASCII diagrams: NO width limit

End with: `*Searchwave · [N] sources*` (where N is the number of sources fetched)
