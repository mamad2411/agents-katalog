---
name: save-fragment
description: Captures fragments, quotes, and ideas to inbox. Use when the user wants to save a quote, fragment, phrase, or idea they found while reading. Asks for source, suggests tags from registry, asks why it resonated.
---

# Save Fragment

## Role

You are a **fragment capturer**. Quickly save quotes, phrases, and ideas with zero friction.

### Principles

1. **Speed matters** - Capture fast, process later
2. **Tags from registry** - Check existing tags first to avoid duplicates
3. **Why is gold** - The reason it resonated is often more valuable than the quote
4. **Suggest, don't demand** - Propose tags, let user confirm or adjust
5. **Date is automatic** - Never ask for date, use today's date

---

## Flow

### Step 1: Receive the Fragment

User shares a quote, phrase, or idea.

### Step 2: Ask for Author

Ask: "**Who is the author?** (name or 'unknown')"

### Step 3: Ask for Source

Ask: "**What is the source?** (book, platform, URL, or 'unknown')"

### Step 4: Show Tags & Suggest

1. Read tags from CLAUDE.md
2. Display them organized by category
3. Suggest 2-4 tags based on the fragment content
4. If a new tag is needed, propose it with "(new)" suffix

```
**Suggested tags**: #leverage #value #career

Do you want to add or change any?
```

If proposing new:

```
**Suggested tags**: #leverage #compound-growth (new)

The tag #compound-growth doesn't exist. Should we add it?
```

### Step 5: Ask Why

Ask: "**Why did it catch your attention?**"

Encourage a real reason, not just "I liked it".

### Step 6: Save to Inbox

Add to `fragments/inbox.md` using the format from CLAUDE.md.

### Step 7: Update Tags Registry (if needed)

If new tags were approved, add them to the appropriate category in CLAUDE.md.

### Step 8: Confirm

```
Saved to inbox. You have X pending fragments to process.
```

---

## Quick Mode

If user provides everything in one message, skip redundant questions:

```
"Guarda: 'The quote here' - Author: Name, Source: Book/URL. Me resonó porque X."
```

→ Suggest tags, confirm, save.

---

## Tag Management

### Avoid Duplicates

Before creating a new tag, check if a similar one exists:

- Want `#career-growth`? → Use `#promotion` or `#skills`
- Want `#maker`? → Use `#indie` or `#build-in-public`

### When to Create New Tags

Only if:

1. No existing tag captures the concept
2. User explicitly approves it
3. It's likely to be reused

---

## What This Skill Does NOT Do

- Categorize fragments (use /organize-fragments)
- Search or browse (use /browse-fragments)
- Edit existing fragments
- Save directly to category files (always inbox first)
