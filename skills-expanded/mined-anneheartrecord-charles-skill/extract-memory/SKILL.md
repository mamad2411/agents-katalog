---
name: extract-memory
description: |
  Extract writing style, personality traits, and key insights from a collection of documents
  (Markdown, PDF, TXT, DOCX) and save them as a Claude Code memory file. Use when the user
  wants to capture their writing DNA, build a personal style guide, or create a reusable
  memory profile from their existing content.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
---

# extract-memory

Analyze a collection of documents and extract a personal writing style profile into a Claude Code memory file.

## What This Skill Does

1. Reads all documents from a given directory or file
2. Analyzes writing patterns, style, tone, vocabulary, themes
3. Generates a structured writing style profile
4. Saves the profile to a memory file (default: `~/.claude/writing-style.md`)

## Supported Input Formats

- `.md` — Markdown files
- `.txt` — Plain text files
- `.pdf` — PDF documents (read via the Read tool)
- `.lakebook` — Yuque exports (auto-detected, will run `/convert-lakebook` first)

## Workflow

### Step 1: Identify Input

Determine what the user provided:

- **Directory path**: Read all supported files in the directory
- **Single file path**: Read that one file
- **`.lakebook` file**: First convert to Markdown using `python3 ~/Desktop/lakebook-converter/convert.py`, then process the output directory

### Step 2: Sample Documents

For large collections (20+ files):
- Read all files but sample strategically — pick diverse documents by length and topic
- Aim to read at least 15-20 substantial documents (>500 chars each)
- Prioritize longer, more expressive documents over short notes

For small collections (<20 files):
- Read all files completely

### Step 3: Analyze Writing Style

Examine the documents and extract the following dimensions:

#### Structure Patterns
- How do they open articles? (Hook style, question, statement, story)
- What's the typical article structure? (Sections, numbering, flow)
- How do they close? (Summary, call-to-action, question, open-ended)

#### Language Characteristics
- Vocabulary level and preferences
- Use of metaphors and analogies (what domains do they draw from?)
- Sentence length patterns (short and punchy? Long and flowing?)
- Use of rhetorical devices (repetition, contrast, parallelism)
- Multilingual patterns (code-switching, foreign terms)

#### Tone & Voice
- Formality level
- Emotional range (analytical, passionate, humorous, serious)
- Relationship with reader (teacher, peer, friend, mentor)
- Confidence level and how they handle uncertainty

#### Thinking Patterns
- How do they approach problems? (First principles, analogy, data-driven)
- Common frameworks and mental models they use
- How do they handle disagreement or controversial topics?

#### Content Themes
- Recurring topics and interests
- Core beliefs and values that surface across multiple pieces
- What they reference frequently (books, people, concepts)

#### Formatting Habits
- Use of bold, italic, headers
- List styles (numbered, bullet, emoji)
- Use of tables, code blocks, quotes
- Paragraph length preferences

### Step 4: Generate Profile

Create a structured Markdown file with the analysis results. Use this template:

```markdown
# Writing Style DNA — [Name/Alias]

## Structure Patterns
[findings]

## Language Characteristics
[findings]

## Tone & Voice
[findings]

## Thinking Patterns
[findings]

## Content Themes
[findings]

## Formatting Habits
[findings]

## Core Identity
[one paragraph summary of the writer's essence]

## One-Line Summary
> [single sentence that captures their writing DNA]
```

### Step 5: Save & Report

1. Write the profile to the target memory file
2. Report to the user:
   - How many documents were analyzed
   - Key findings summary (3-5 bullet points)
   - Where the file was saved
   - How to use it: "You can now tell Claude to read `~/.claude/writing-style.md` before writing tasks"

## Usage Examples

```
/extract-memory ~/Desktop/lakebook-converter/output/
/extract-memory ~/Documents/blog-posts/
/extract-memory ~/Desktop/export.lakebook
/extract-memory ~/Desktop/my-article.md
```

### With Custom Output Path

If the user specifies where to save:
```
/extract-memory ~/Documents/posts/ --save-to ~/.claude/my-style.md
```

Default save location: `~/.claude/writing-style.md`

## Important Notes

- **Do NOT store the full document content** in the memory file — only the distilled style analysis
- **Keep the output under 3KB** to avoid excessive token consumption when loaded as context
- If a memory file already exists at the target path, ask the user if they want to overwrite or merge
- The analysis should be specific and actionable, not generic — include actual examples from the user's writing
