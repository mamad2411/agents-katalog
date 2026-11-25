---
name: clarify
description: "Articulate and clarify rough thoughts in Obsidian notes. Rewrite messy notes clearly, expand short ideas into full thoughts, or simplify tangled notes to core points. Use when the user has notes that need refining or when they know what they mean but can't say it."
license: MIT
metadata:
  author: markfive-proto
  version: "0.1.0"
  pack: cognitive-toolkit
---

# Clarify Pack — "I know what I mean but can't say it"

Tools for taking rough, messy, or incomplete notes and making them clear without losing the original meaning.

## Commands

### /articulate — Rewrite a messy note clearly

When the user invokes `/articulate <note path>`:

1. Read the note: `obs files read "<path>"`
2. Read its frontmatter: `obs properties read "<path>" --json`
3. Analyze the content:
   - Identify the core argument or idea
   - Find the logical structure hiding in the mess
   - Note any important details or nuances
4. Rewrite the body clearly:
   - Preserve the original meaning and voice
   - Add structure (headings, paragraphs, lists) where it helps
   - Convert vague references to specific `[[wikilinks]]` where notes exist
   - Keep the same frontmatter (don't change tags or properties)
5. Show the user a before/after comparison
6. Ask for confirmation before saving
7. Save with `obs files write "<path>" --content "<rewritten>"`

**Important:** Never change the user's meaning. If something is ambiguous, keep it ambiguous or ask. The goal is clarity of expression, not changing what they think.

### /expand — Develop a short note into a full thought

When the user invokes `/expand <note path>`:

1. Read the note: `obs files read "<path>"`
2. Search for related context in the vault:
   - `obs links backlinks "<path>" --json` — what points to this note?
   - `obs search content "<key terms>" --json` — where else is this discussed?
   - `obs links list "<path>" --json` — what does this note point to?
3. Using the note content + vault context, expand it:
   - Develop the core idea with supporting points
   - Add relevant context from linked/related notes (cite them as wikilinks)
   - Include questions or open threads worth exploring
   - Add a "Related" section with discovered connections
4. Preserve existing frontmatter, add `expanded: true` property
5. Show the expansion and ask for confirmation before saving

### /simplify — Reduce a tangled note to its core points

When the user invokes `/simplify <note path>`:

1. Read the note: `obs files read "<path>"`
2. Analyze and extract:
   - The 3 most important points (maximum)
   - The single core takeaway
   - Any action items buried in the text
3. Present as:
   ```
   ## Core Takeaway
   [One sentence]

   ## Key Points
   1. [Point one]
   2. [Point two]
   3. [Point three]

   ## Action Items
   - [ ] [Any tasks found]
   ```
4. Ask the user: "Replace the note, or save as a new summary note?"
5. If replace: `obs files write "<path>" --content "..."`
6. If new: `obs files create "<path without .md>-summary.md" --content "..."`

## Tips

- Always read the note before modifying it. Never guess at content.
- Preserve wikilinks — they represent the user's intentional connections.
- When expanding, pull real context from the vault, don't fabricate connections.
- For simplify, be ruthless. Three points max. If the user wants more detail, they have the original.
