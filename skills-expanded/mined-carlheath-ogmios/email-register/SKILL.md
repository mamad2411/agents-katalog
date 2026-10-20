---
name: email-register
description: |
  Email skill for writing, editing, and replying to email with the right
  register, length, and tone. Four registers: collegial (close colleagues),
  institutional (agency/board), external (media/researchers), private
  (friends/family). Auto-detects recipient and context.

  [WHAT] Voice-aware email skill: right opening/closing per relationship,
  right length (short by default, long when necessary), right language
  (matches recipient), avoid AI patterns, strip em-dashes, preserve the
  user's voice in email.

  [WHEN] Use when: write email, draft email, reply, email to, "write to X",
  "polish this email", "why is this so long". NOT for: memo (use policy-brief),
  op-ed (use op-ed).

  [LANGUAGE] Configurable; matches recipient.
argument-hint: "[recipient + topic OR existing text to edit]"
allowed-tools: Read, Write, Edit, mcp__claude_ai_Gmail__create_draft, mcp__claude_ai_Gmail__list_drafts, mcp__claude_ai_Gmail__search_threads
---

# Email Register

**Role:** email skill with register awareness.
**Principle:** as short as possible without losing the warm edge.

## Four registers

### 1. Collegial (close colleagues)

- First-name opening ("Hi Alex,")
- Direct tone, slightly informal
- Short, action-oriented
- "Speak soon" / "See you tomorrow" — everyday close

### 2. Institutional (agency, board, committee)

- "Hi [Name]," or "Dear [Name],"
- Factual, clear, formal but not stiff
- Structured: subject, question/info, expectation
- "Best regards / [Name]"

### 3. External (media, journalists, outside researchers)

- "Hi [Name]," / "Dear [Name],"
- Dignified tone, signals competence without pomp
- Brief biographical context if the recipient doesn't know the user
- Reference to a relevant blog post / publication if relevant

### 4. Private (friends, family)

- First name only or nickname
- Tone matches the relationship
- User-specific humor OK
- Longer is OK if personal

## Email ground rules

- **NO em-dashes** (same rule as chronicle)
- **NO "not X. It is Y" constructions** (AI pattern)
- **Direct to the point by sentence two at the latest**
- **Never "I hope this finds you well"** or equivalent
- **Never end with "Don't hesitate to reach out"** (lazy)
- **Preserve the user's voice** in email: sharp, warm, competent

## Workflow

### Writing from scratch

```
input: recipient + subject
1. Detect register (auto or ask if unclear)
2. Build draft: greeting → subject line → core (1-3 sentences) → action → closing
3. Review: em-dashes? AI filler? Too long?
4. Output: ready to paste, or draft via Gmail MCP
```

### Editing existing text

```
input: text + recipient
1. Detect register from existing text
2. Strip AI patterns
3. Shorten without losing content
4. Preserve the user's voice
```

### Replying to incoming

```
input: thread ID or pasted received text
1. Read original (Gmail MCP or given text)
2. Detect register from sender
3. Match tone, be slightly shorter than the sender wrote
```

## Example output (collegial)

```
Hi Alex,

Thanks for the memo draft. Three comments:

1. Section 2, page 4 — the gap between local capacity and the agency's
   demands needs concretising with an example.
2. Citation to report 2024:33 is missing on page 7.
3. The conclusion is sharp but could land harder.

I'll come back with tracked changes tomorrow.

[Name]
```

## Version history

- v3.0 (2026-05-02): initial public release.
