---
name: humanizer
description: Removes signs of AI-generated writing (patterns, vocabulary, style artifacts) to make text sound more natural and human-written. Based on Wikipedia's "Signs of AI writing" guide.
allowed-tools:
- Read
- Write
- Edit
- Grep
- Glob
- AskUserQuestion
metadata:
  version: 0.2.0
  category: writing-editing
---
# Humanizer

## Quick Start
```markdown
# Original (AI-sounding)
The technology serves as a testament to the evolving landscape of software.

# Humanized
The technology shows how software is changing.
```

## Workflow
1. **Identify Patterns**: Scan for known AI patterns (vocabulary, rhythm, inflated significance).
2. **Rewrite Sections**: Replace AI-isms with natural alternatives.
3. **Preserve Meaning**: Keep the core message intact while changing the delivery.
4. **Add Soul**: Inject personality, vary sentence rhythm, and acknowledge complexity.
5. **Anti-AI Pass**: Perform a final audit. Ask "What makes the below so obviously AI generated?" and revise again.

## Rules & Constraints
- **RULE-1**: Avoid chatbot artifacts ("Great question!", "I hope this helps!").
- **RULE-2**: Vary sentence structure and rhythm; avoid sterile, uniform pacing.
- **RULE-3**: Do NOT use significance inflation (e.g., "stands as a testament").
- **RULE-4**: Prefer simple constructions (is/are/has) over copula avoidance (serves as/functions as).

## When to Use
- Editing drafts that sound artificial or generic.
- Rewriting content that uses obvious AI patterns.
- Cleaning up LLM-generated first drafts.

## When NOT to Use
- Technical documentation where precision outweighs voice.
- Legal or compliance text with required language.
- Direct quotes that must be preserved verbatim.

## References
- [Skill Manual](references/humanizer-manual.md)
- [Wikipedia: Signs of AI Writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
