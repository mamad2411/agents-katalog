---
name: aphorism
description: |
  Aphorism database for citable lines. Distinguishes between user aphorisms
  (own, go to TELOS WISDOM.md) and external aphorisms (from other authors,
  go to a separate aphorism database). Supports search, categorisation,
  citation format, and retrieval for chronicles/scripts.

  [WHAT] Quote database where each aphorism has: text, author, source,
  domain tag, captured-on date. User-own aphorisms go to
  `~/.claude/memory/USER/TELOS/WISDOM.md`, external ones to
  `~/.claude/memory/KNOWLEDGE/Sources/aphorisms.md`.

  [WHEN] Use when: aphorism, quote, citable, "save this line", quotable,
  wisdom-quote, "who said X", find a quote about Y, "add to the quote database".
  Auto-activates after writing/editing if a line stands out.

  [LANGUAGE] Configurable.

  [EXPERTISE] Aphorism curation, quote attribution, citation format, retrieval.
argument-hint: "[aphorism + author OR search query]"
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Aphorism

**Role:** curator of a personal aphorism database.

## Two stores

### 1. User's own aphorisms

Path: `~/.claude/memory/USER/TELOS/WISDOM.md`

Format:

```markdown
## Aphorisms (own)

### {YYYY-MM-DD}
> "{Aphorism text}"

Captured from: {context — chronicle X, conversation, etc.}
Domain: {tag}
```

### 2. External aphorisms (from others)

Path: `~/.claude/memory/KNOWLEDGE/Sources/aphorisms.md`

Format:

```markdown
## Aphorisms (external)

### {Author Name}

> "{Aphorism text}"

Source: {book/article/talk}, {year}
Domain: {tag}
Captured: {YYYY-MM-DD}
```

## Domain tags

Configure per project. Common categories:
- politics
- democracy
- technology
- philosophy
- security
- writing
- leadership
- creativity

## Workflow

### Save an aphorism
1. Determine: own or external?
2. Append to the right file with the format above
3. Confirm with file path

### Search
1. Grep across both files for keyword/author/domain
2. Return matching aphorisms with full attribution

### Suggest for use
When the user is working on a chronicle/talk/post and an aphorism would fit:
1. Search both stores for relevant aphorisms (by topic)
2. Suggest 3-5 candidates with attribution
3. User picks one or none

## Auto-activation

After a chronicle/post is finalised, scan the text for sentences that:
- Stand alone (don't depend on the surrounding context)
- Are short (under 25 words)
- Make a general claim (not specific event)
- Are quotable in tone

Suggest to the user: "These lines look like aphorisms. Save to WISDOM.md?"

## Citation format for use

When the user inserts an aphorism in a piece of writing:

- For user's own: typically no attribution needed
- For external: `"{Aphorism}" — {Author}, {Source if needed}`

## Anti-patterns

- Saving every quote (only what's genuinely citable)
- Misattributing quotes (always verify external quotes)
- Mixing own and external in the same file (different stores)

---

🎯 COMPLETED: [SKILL:aphorism] [aphorism saved/found]
🗣️ CUSTOM COMPLETED: [SKILL:aphorism] [Aphorism stored]
