---
name: ambiguity-detection
description: Detect ambiguous or contradicting wording in requirements and
  specs. Use when reviewing documents before implementation.
metadata:
  tags: ambiguity, detection
---

# Ambiguity Detection

## Use this skill when
- Scanning requirements for vague or contradictory phrasing
- Rewriting ambiguous statements into precise language
- Surfacing unstated assumptions that block implementation

## Do not use this skill when
- Requirements are already precise
- You are implementing code

## Instructions
1. Flag weasel words: quickly, secure, fast, good, etc., large, some.
2. Flag undefined acronyms and domain terms.
3. Check that numbers have units and boundaries.
4. List every unstated assumption explicitly.
5. Rewrite flagged statements with measurable terms.
6. Output an ambiguity list with proposed rewrites.

## Output Format
- Term/Phrase | Location | Why ambiguous | Proposed precise wording

## Common Mistakes
- Leaving vagueness in place
- Introducing new assumptions while rewriting
