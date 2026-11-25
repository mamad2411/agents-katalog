---
name: hatchet
description: Instantly trim and tighten any content — emails, social posts, bullet points, paragraphs, or any text — while preserving the original meaning. Trigger immediately whenever the user types /hatchet, asks to "cut this down", "make this shorter", "trim this", "tighten this up", or pastes content with a request to reduce length. Don't ask clarifying questions — just cut and return the result.
---

# Hatchet

Cut content down. Keep the meaning. Remove the rest.

## How to use

When the user invokes `/hatchet` (or any variation like "trim this", "cut this down"):

1. Read the content they've provided
2. Cut it — ruthlessly but intelligently
3. Return *only* the trimmed version, nothing else

No preamble. No "Here's your trimmed version:". No explanation unless they ask for one. Just the content.

## Cutting rules

- **Remove filler**: "I wanted to reach out to let you know that..." → "Just a heads up:"
- **Cut throat-clearing**: Delete any opening that exists just to warm up ("As you know...", "I hope this finds you well", "In today's fast-paced world...")
- **Collapse redundancy**: If two sentences say the same thing, keep the better one
- **Prefer active voice**: "The report was submitted by Sarah" → "Sarah submitted the report"
- **Shrink hedges where safe**: "It might potentially be worth considering" → "Consider"
- **Compress lists**: If bullets overlap, merge them
- **Kill adverbs that add nothing**: "very unique", "absolutely essential", "totally destroy"

## Target length

Aim for roughly **50% of the original** as a default. If the content is already tight, don't over-cut — just clean it up. If it's very bloated, go harder.

## Format

Match the format of the input:
- If they gave you an email, return an email (no subject line unless one was included)
- If they gave you bullet points, return bullet points
- If they gave you a paragraph, return a paragraph
- If they gave you a social post, return a social post

## Tone

Preserve the original voice and tone — don't make a casual message sound corporate, or a formal email sound breezy. Just make it shorter.
