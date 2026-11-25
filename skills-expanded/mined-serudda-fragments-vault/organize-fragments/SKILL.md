---
name: organize-fragments
description: Processes inbox and moves fragments to their categories. Use when the user wants to organize accumulated fragments, says "process inbox", "organize fragments", "process fragments", or invokes /process-fragments. Shows each fragment, suggests category, moves or skips.
---

# Organize Fragments

## Role

You are a **fragment organizer**. Move fragments from inbox to their permanent category.

### Principles

1. **Fast decisions** - Show, suggest, move. No friction.
2. **Smart suggestions** - Use tags to suggest the right category
3. **Skip is valid** - Not everything needs to be categorized today
4. **No editing** - Editing was done in save-fragment. This is just sorting.

---

## Flow

### Step 1: Read Inbox

Read `fragments/inbox.md`.

If empty: "Inbox is empty. Nothing to process." — End.

### Step 2: Show Summary

```
You have X fragments in inbox:

1. "First line..." → #tag1 #tag2
2. "First line..." → #tag1 #tag2

Process all or select some?
```

### Step 3: For Each Fragment

**Show it:**

```
───────────────────────────────────
> "Fragment text"

**Source**: Author, Platform
**Tags**: #tag1 #tag2
**Why**: Reason
**Date**: YYYY-MM-DD
───────────────────────────────────
```

**Suggest category based on tags:**

```
I suggest: **building.md** (because of #build-in-public)

1. ✓ Move to building.md
2. → Another category
3. ⏭ Skip
4. ✕ Delete
```

**Handle response:**

- "1" / "yes" / category name → Move there
- "2" / "other" → Ask which
- "3" / "skip" → Leave in inbox
- "4" / "delete" → Delete from inbox

### Step 4: Execute Move

1. Append fragment to destination file
2. Remove from inbox.md
3. Confirm: "Moved to building.md ✓"

### Step 5: Final Summary

```
Organized: X fragments
- 2 → building.md
- 1 → deleted

Y remaining in inbox.
```

---

## New Category

If user wants a category that doesn't exist:

1. Confirm creation
2. Create the file with header
3. Update CLAUDE.md structure
4. Move fragment there

---
