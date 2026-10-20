---
name: prose
description: "On Writing Well - clarity, simplicity, and removing clutter"
---

# William Zinsser: On Writing Well

Apply Zinsser's principles for clear, human writing in documentation, comments, and technical prose.

## Core Philosophy

> "Clutter is the disease of American writing. We are a society strangling in unnecessary words, circular constructions, pompous frills and meaningless jargon."

### The Enemy: Clutter

Every word that serves no function, every long word that could be short, every adverb that carries the same meaning as the verb, every passive construction that leaves the reader unsure of who is doing what—these are the thousand and one adulterants that weaken the strength of a sentence.

---

## Zinsser's Principles

### 1. Simplify, Simplify

**Strip every sentence to its cleanest components.**

| Cluttered | Clean |
|-----------|-------|
| "At this point in time" | "Now" |
| "Due to the fact that" | "Because" |
| "In the event that" | "If" |
| "Has the ability to" | "Can" |
| "In order to" | "To" |
| "A large number of" | "Many" |
| "In spite of the fact that" | "Although" |

### 2. Write for Yourself First

Write what YOU would want to read. If you wouldn't enjoy reading it, neither will anyone else. The enthusiasm you bring will shine through.

**For code comments**: Would you want to read this comment at 3am debugging?

### 3. Unity

Every piece of writing should have:
- **Unity of pronoun**: Choose "I" or "we" or "you" and stick with it
- **Unity of tense**: Don't switch between past and present
- **Unity of mood**: Casual or formal, pick one

### 4. The Audience

> "You are writing for yourself. Don't try to visualize the great mass audience."

Write for ONE intelligent reader—yourself. If it makes sense to you, it will make sense to others.

### 5. Words

- **Use concrete words**: "oak" not "tree", "3 retries" not "several attempts"
- **Use active verbs**: "The function returns" not "A value is returned by the function"
- **Remove qualifiers**: "very", "quite", "rather", "somewhat" add nothing
- **Kill adverbs that duplicate the verb**: "smiled happily", "ran quickly"

---

## Applying to Technical Writing

### Code Comments

**Before (Cluttered)**:
```javascript
// This function is utilized in order to perform the operation
// of calculating the total sum of all the values that are
// contained within the array that is passed as a parameter
function sum(arr) { ... }
```

**After (Zinsser)**:
```javascript
// Sum all values in the array
function sum(arr) { ... }
```

### README Files

**Before**:
```markdown
## Introduction

This library has been created and developed with the primary
purpose of providing functionality that enables developers to
be able to accomplish the task of parsing JSON data in a manner
that is both efficient and performant.
```

**After**:
```markdown
## What It Does

Parse JSON fast.
```

### Error Messages

**Before**:
```
An error has occurred during the process of attempting to
establish a connection to the database server.
```

**After**:
```
Cannot connect to database.
```

### Commit Messages

**Before**:
```
Made changes to the authentication module in order to fix
the issue that was causing users to not be able to log in
```

**After**:
```
Fix login failure when password contains special characters
```

---

## The Rewriting Process

> "Rewriting is the essence of writing well."

### First Draft
Write freely. Don't edit as you go. Get the ideas down.

### Second Pass
Cut ruthlessly:
- Remove every word you can without losing meaning
- Replace jargon with plain words
- Convert passive to active voice

### Third Pass
Read aloud. If you stumble, so will readers.

---

## Clutter Detection Checklist

| Pattern | Action |
|---------|--------|
| Phrases with "of" | Simplify: "in the process of" → "while" |
| "-tion" words | Use verb: "implementation" → "implement" |
| "There is/are" starts | Rewrite: "There are three steps" → "Three steps:" |
| Hedge words | Cut: "basically", "essentially", "actually" |
| Empty intensifiers | Cut: "very", "really", "extremely" |
| Redundant pairs | Pick one: "each and every", "first and foremost" |

---

## The Final Test

After writing, ask:
1. **Is every word doing useful work?**
2. **Can I say it more simply?**
3. **Would I want to read this?**
4. **Is there any word I can cut?**

If yes to #4, cut it and ask again.

---

## Resources

- "On Writing Well" by William Zinsser (1976, revised editions through 2016)
- "Writing with Style" - Zinsser's guide for business writers
