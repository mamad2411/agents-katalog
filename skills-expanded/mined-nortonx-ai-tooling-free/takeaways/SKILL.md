---
name: takeaways
description: "Extract conclusions and key takeaways from YouTube videos, Instagram Reels/posts, or long-form content, providing a fast comparison and a clear final verdict that directly answers the question or premise in the video's title. Args: <url | text>"
argument-hint: "<url | text>"
---

<!-- Note: $ARGUMENTS is substituted by Claude commands only. In Copilot,
     the user must include their argument inline in the prompt; the skill
     body sees the literal text "$ARGUMENTS" unsubstituted. -->

## Arguments

`<url | text>`

- Required. A URL to a video, social post, or article, OR raw text/transcript content.
- **Examples**: `/takeaways https://www.youtube.com/watch?v=example`, `/takeaways <pasted transcript>`

> Copilot CLI note: `$ARGUMENTS` does not substitute in skills; include the argument inline in your prompt.

# Extract Takeaways: $ARGUMENTS

Extract the core conclusions, pros, cons, and answers from long-form content, video transcripts, or social posts. Always resolve clickbait titles up front by delivering a direct, unambiguous verdict.

## Step 1: Input Resolution

Check the content provided in `$ARGUMENTS`:

1. **Raw text or pasted transcript**: proceed directly to Step 2.
2. **URL (YouTube, Instagram, article, podcast)**:
   - If runtime browsing or fetching tools are available, attempt to retrieve page content or transcript.
   - If external tools are unavailable, if scraping is blocked by captchas/auth, or if no captions are extractable, **stop and ask the user**:
     > "Could not extract transcript automatically from `<url>`. Please paste the transcript, subtitles, or article text to continue."
3. **Empty or missing argument**: stop and prompt:
   > "Usage: `/takeaways <url | text>`. Please provide a URL or paste the content to analyze."

## Step 2: Identify Core Premise and Title Question

Identify the central question, debate, or promise in the title or opening framing (for example: "Is framework X worth learning?", "Tool A vs Tool B", "Does technique Y really work?").

## Step 3: Group Findings and Key Points

Synthesize the content into clear categories:
- Primary claims and evidence presented
- Concrete pros and cons
- Product, tool, or methodology comparisons
- Benchmark numbers, pricing, or measurable results

## Step 4: Output Template

Render the analysis in this structured format:

```markdown
# Takeaways: <Title or Subject>

**Core Premise**: <The central question or debate investigated in the content>

**Direct Verdict**: <Direct, definitive answer resolving any clickbait or open question up front>

## Key Takeaways

- **<Point 1>**: <Summary of finding with evidence or rationale>
- **<Point 2>**: <Summary of finding with evidence or rationale>
- **<Point 3>**: <Summary of finding with evidence or rationale>

## Comparison / Breakdown

| Subject / Option | Advantages | Disadvantages | Verdict |
|---|---|---|---|
| <Item A> | <Key strength> | <Key weakness> | <Assessment> |
| <Item B> | <Key strength> | <Key weakness> | <Assessment> |

## Actionable Recommendation

<1-2 concise paragraphs summarizing practical advice, trade-offs, and when to choose what>
```

## Rules

- State the final verdict directly up front; do not preserve clickbait suspense.
- Do not invent facts, benchmarks, or opinions absent from the source content.
- Be concise: prioritize bullet points and tables over dense prose.
