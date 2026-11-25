---
name: extract-knowledge
description: Deep content analysis and insight extraction from articles, transcripts, documents, videos, PDFs. Prioritizes novelty and surprise over summaries. USE WHEN extract knowledge, extract insights, analyze this content, extract alpha, key ideas, what's important in this.
---

# Extract Knowledge

**Mode:** Deep content analysis and insight extraction
**Input:** User-provided content (articles, transcripts, documents, videos, PDFs)
**This is NOT web research.** It analyzes content the user provides or points to.

## When to Use

- User says "extract knowledge", "extract insights", "analyze this content", "extract alpha"
- User provides an article, transcript, video URL, PDF, or paste of text and wants the key ideas pulled out
- Deep analysis of a specific piece of content (not broad web research)
- User wants to capture the most important and surprising insights from something they consumed

## Philosophy

Based on Claude Shannon's information theory: **real information is what is different, not what is the same.** This skill prioritizes novelty, surprise, and non-obvious insights over comprehensive summaries. Standard extraction catches the obvious points. This skill catches what standard extraction misses -- the subtle, the counterintuitive, the profound.

## Available Tools

| Tool | Use For |
|------|---------|
| **WebFetch** | Retrieve article/page content from a URL the user provides |
| **claude-browser MCP** | Retrieve content from auth-required or JS-heavy pages |
| **Read** | Read local files (PDFs, text files, documents) the user points to |

---

## Workflow

### Step 1: Acquire Content

Determine the content source and retrieve it:

**Web URL provided:**
```
WebFetch(url: "[user's URL]", prompt: "Extract the full article/transcript content")
```

**Local file provided:**
```
Read(file_path: "[user's file path]")
```

**Text pasted directly:**
Use the pasted content as-is.

**YouTube URL provided:**
```
WebFetch(url: "[youtube URL]", prompt: "Extract the video transcript or description")
```
If WebFetch cannot get the transcript, use the claude-browser MCP to access the page and extract available content.

**Auth-required or JS-heavy page:**
Use the claude-browser MCP server to navigate and extract content.

### Step 2: Deep Thinking Analysis

Before extracting anything, engage in extended thinking across these dimensions:

1. **SURFACE SCAN** -- What are the obvious main points?
2. **DEPTH PROBE** -- What implications are not explicitly stated?
3. **CONNECTION MAP** -- What unusual connections exist between ideas?
   - What makes you stop and think "wait, how does THAT work?"
   - What cross-domain patterns appear (same principle across biology/ML, physics/economics, human/AI)?
   - What would feel personally relevant in a surprising way?
4. **ASSUMPTION CHALLENGE** -- What conventional wisdom is being questioned?
5. **NOVELTY DETECTION** -- What is genuinely new or surprising here?
6. **FRAMEWORK EXTRACTION** -- What mental models or frameworks emerge?
7. **SUBTLE INSIGHTS** -- What quiet observations carry profound weight?
8. **CONTRARIAN ANGLES** -- What goes against common thinking?
9. **FUTURE IMPLICATIONS** -- What does this suggest about what is coming?
10. **SYNTHESIS** -- What are the highest-value ideas across all dimensions?

Allow thinking to wander and make unexpected connections. Question every assumption about what is "important." Prioritize novelty and surprise over comprehensiveness.

### Step 3: Extract and Structure

Produce a structured extraction with these sections:

```markdown
## Knowledge Extraction: [Content Title]

**Source:** [URL, file path, or "provided text"]
**Content Type:** [Article / Transcript / Video / PDF / Essay / Interview]
**Date Analyzed:** [YYYY-MM-DD]

### One-Paragraph Summary
[Dense paragraph capturing the essence -- what is this about, why does it matter, what is the core argument or contribution.]

### Key Ideas (5-10)
[The main substantive points, written clearly. These are the ideas someone would want if they only had 30 seconds.]
- [Key idea 1]
- [Key idea 2]
- ...

### Surprising Insights (5-15)
[The high-alpha extractions. Ideas that are counterintuitive, novel, or make you reconsider something. Written in approachable 8-15 word bullets.]
- [Surprising insight 1]
- [Surprising insight 2]
- ...

### Mental Models and Frameworks
[Any reusable thinking tools, frameworks, or mental models found in the content.]
- **[Framework name]:** [Brief description of the model and when to apply it]
- ...

### Actionable Recommendations
[What should someone DO based on this content? Specific, concrete actions.]
- [Action 1]
- [Action 2]
- ...

### Quotes Worth Saving
[Direct quotes that are exceptionally well-phrased, memorable, or capture a key idea perfectly. Include attribution.]
> "[Quote]" -- [Speaker/Author]

### Connections and Implications
[What does this connect to? What are the second-order effects? What domains does this apply to beyond the obvious?]
- [Connection 1]
- [Connection 2]
```

### Step 4: Quality Check

Before delivering, verify:
- **Surprising Insights are actually surprising** -- if an insight is obvious or commonly known, remove it
- **Key Ideas cover the substance** -- someone reading only this section should understand the content
- **Mental Models are reusable** -- not just restated points, but genuine thinking tools
- **Quotes are exact** -- do not paraphrase in the quotes section
- **Actionable Recommendations are specific** -- "think more carefully" is not actionable; "spend 10 minutes writing down assumptions before starting" is

---

## What Makes a Good Extraction

### HIGH-VALUE signals (include these):
- Makes you stop and reconsider something you thought you knew
- Connects ideas from different domains unexpectedly
- Challenges industry consensus or common wisdom
- Reframes a familiar concept in a surprising way
- Has second-order implications not explicitly stated
- Represents a novel mental model or framework
- Captures a subtle observation with profound weight

### LOW-VALUE signals (avoid these):
- Restates common knowledge everyone already knows
- Generic advice that could apply to anything ("work hard", "be curious")
- Surface-level observations without depth
- Purely factual information without insight
- Ideas that have been said many times before in the same way

---

## Output Persistence

Extraction results are delivered inline. To persist, write to:

```
~/.augment/MEMORY/RESEARCH/{YYYY-MM-DD}_{content-slug}/
  extraction.md      # The full structured extraction
  metadata.md        # Source info, content type, date analyzed
```

Create and save automatically if the extraction exceeds 500 words or the user requests it.

---

## Comparison to Standard Summarization

| Aspect | Standard Summary | Extract Knowledge |
|--------|-----------------|-------------------|
| Focus | Comprehensiveness | Novelty and surprise |
| Thinking depth | Surface | Deep multi-dimensional analysis |
| Mental models | Rarely extracted | Explicitly identified |
| Surprising insights | Mixed with obvious | Separated and prioritized |
| Actionable items | Sometimes included | Always included and specific |
| Quotes | Rarely preserved | Best quotes captured |
| Quality bar | "Did I cover everything?" | "Did I find what others would miss?" |
