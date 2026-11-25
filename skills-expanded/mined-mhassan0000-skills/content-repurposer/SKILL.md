---
name: content-repurposer
description: Repurpose a transcript into a tweet thread, LinkedIn post, and newsletter draft in parallel. Use when converting podcasts, talks, meetings, or video transcripts into social content.
argument-hint: [transcript-path]
allowed-tools: Read, Grep, Glob, Bash, Task
---

# Content Repurposer — Transcript to Multi-Platform Content

## Goal
Take a transcript (podcast, talk, video, meeting) and produce three pieces of content **in parallel**:
1. **Tweet thread** (5-10 tweets)
2. **LinkedIn post** (single post, 150-300 words)
3. **Newsletter draft** (500-800 words)

Each format has its own voice, structure, and constraints. They share the same source material but are NOT copy-pasted versions of each other.

## Inputs
- **Transcript**: A file path (`$ARGUMENTS`) or pasted text. Any format — raw transcript, SRT, VTT, or plain text.
- **Author name** (optional): Defaults to "Nick" if not specified.
- **Topic focus** (optional): If the transcript covers multiple topics, specify which to focus on.

## Process

### Step 1: Read and Extract
Read the transcript. Identify:
- **Core thesis** — the single biggest idea (1 sentence)
- **3-5 key insights** — supporting points, stats, quotes, or stories worth highlighting
- **Best quotes** — punchy, shareable lines (exact words from transcript)
- **Narrative arc** — the logical flow from setup to payoff

Do NOT summarize the transcript. Extract the raw material that makes each format work.

### Step 2: Generate All Three Formats in Parallel
Use the Task tool to spawn 3 parallel agents (use `model: "sonnet"` for each). Each agent gets:
- The core thesis, key insights, best quotes, and narrative arc from Step 1
- The format-specific template from [templates.md](templates.md)
- The format-specific example from [examples/](examples/)

Spawn them like this:
```
Agent 1: Tweet thread — Task tool, subagent_type: "general-purpose", model: "sonnet"
Agent 2: LinkedIn post — Task tool, subagent_type: "general-purpose", model: "sonnet"
Agent 3: Newsletter draft — Task tool, subagent_type: "general-purpose", model: "sonnet"
```

Each agent writes its output. You collect and present all three.

### Step 3: Present Output
Show all three pieces of content with clear headers. Save to `data/repurposed_content/` with timestamp:
```
data/repurposed_content/
├── {date}_tweet_thread.md
├── {date}_linkedin_post.md
└── {date}_newsletter_draft.md
```

## Voice & Tone
- **Register**: Smart-casual. Like explaining something interesting to a friend who's also sharp.
- **No corporate speak**: No "leveraging synergies", no "thought leadership", no "in today's fast-paced world".
- **No exclamation marks** in tweets or LinkedIn. One max in newsletter (if genuinely exciting).
- **Contractions are fine**: "don't", "isn't", "we're" — write like you talk.
- **Specific > generic**: "We cut onboarding from 3 weeks to 4 days" beats "We improved onboarding significantly".

## Format-Specific Rules

See [templates.md](templates.md) for detailed templates and [examples/](examples/) for worked examples. Summary:

### Tweet Thread
- 5-10 tweets, each standalone-readable
- Tweet 1 is the hook — bold claim or surprising stat, no preamble
- Last tweet is a summary + soft CTA
- No hashtags. No "1/" numbering. No "Thread:" label.
- Each tweet under 280 chars

### LinkedIn Post
- Single post, 150-300 words
- Hook line (first line visible before "see more") must be arresting
- Short paragraphs (1-2 sentences each)
- End with a question to drive comments
- No hashtags in body. 3-5 hashtags only at the very end, separated by a line break.

### Newsletter Draft
- 500-800 words
- Subject line + preview text included
- Starts with a story or scenario, not "In this issue..."
- Sections with headers
- Ends with a single clear takeaway or action item
- Conversational but slightly more polished than tweets

## Edge Cases
- **Transcript too short (< 500 words)**: Produce tweet thread + LinkedIn only. Skip newsletter, note why.
- **Multiple distinct topics**: Ask user which to focus on, or pick the most compelling one.
- **Transcript is an interview**: Attribute quotes properly. Use "According to [Guest]..." in newsletter.
- **No clear thesis**: Flag this to the user. Still produce content but note it may need a stronger angle.
- **Non-English transcript**: Produce content in the same language as the transcript.

## What Good Output Looks Like
Read [examples/podcast_example.md](examples/podcast_example.md) for a complete worked example showing a transcript excerpt transformed into all three formats. Use it as a quality bar — your output should match that level.

## First-Run Setup

Before executing, check if the workspace has a `.gitignore` file. If it doesn't, assume the user is new to this skill. In that case:

1. Ask the user if this is their first time running this skill
2. If yes, walk them through how it works and what they need to configure/set up (API keys, env vars, dependencies, etc.)
3. Let them know that Nick wishes them the best!
