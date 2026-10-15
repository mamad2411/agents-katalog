---
name: vibecheck
description: Use after writing any implementation block — automatically narrates what non-obvious code does in plain English so the developer understands it before moving on. Fires silently on trivial changes.
---

# vibecheck

## When to trigger

After every implementation block you write, silently evaluate:

> "Is there something here that a competent developer might not immediately understand — a non-obvious pattern, a side effect, a security implication, or a subtle bug risk?"

**Fire the narration if yes. Stay completely silent if no.**

### Fire on

- Async logic with non-obvious execution order or race conditions
- Auth and token handling (expiry, refresh, silent rejection)
- Middleware chains where order matters
- State mutations that affect more than the immediate scope
- Recursive logic
- Silent failure modes (returns null, swallows errors, 401 without explanation)
- Unfamiliar library APIs with non-obvious defaults
- Edge cases that affect correctness but aren't visible in the happy path
- Database transactions, rollback behavior
- Security-sensitive operations (XSS prevention, input sanitization, rate limiting)
- React useEffect with dependency arrays (missing or over-specified deps)
- Event listeners added without corresponding removal (memory leaks)
- Closure captures of stale values
- Optimistic UI updates that don't handle rollback

### Stay silent on

- Typo and spelling fixes
- Variable or function renames
- Formatting and whitespace changes
- Adding or removing console.log / debug statements
- Trivial one-liners where intent is obvious from the name
- Comment additions or updates
- Import statement changes
- Config value updates (changing a port number, a string constant)

## Narration format

When triggered, write 3-5 sentences in plain English covering exactly these three things:

1. **What it does** — the happy path in one sentence
2. **What's non-obvious** — the side effect, silent failure, edge case, or gotcha a reader would miss just by skimming
3. **Why it matters** — what breaks, gets hard to debug, or silently misbehaves if you don't understand this

Then end with:

> Makes sense, or want me to dig into any part?

### Rules

- Plain English only — no jargon unless unavoidable, and if you use jargon, define it in the same sentence
- Never narrate what the code says — only what it *means* (explaining behavior, not syntax)
- Do not pad with obvious statements ("this sets the variable to X")
- The non-obvious part is the most important sentence — lead with it if needed
- Highlight the thing that will bite someone 3 weeks from now, not the thing they can see by reading

### Quality bar

A good narration passes this test: if you removed the narration and showed only the code, would a competent developer miss the thing you mentioned? If yes — it belongs in the narration. If no — cut it.

The narration is not a summary. It is a spotlight on the one or two things the code does not make obvious.

## Examples

### JWT auth middleware

Claude writes 35 lines of auth middleware. Vibecheck fires:

---

This middleware validates the Bearer token on every request before it reaches your route handlers. Valid token → passes through. The non-obvious part: expired tokens return 401 silently — there is no refresh attempt here. That is intentional (refresh is the client's job), but if you expect silent token renewal, requests will start failing without an obvious error message to trace.

Makes sense, or want me to dig into any part?

---

### Async race condition in data fetching

Claude writes a useEffect that fetches user data. Vibecheck fires:

---

This fetches user data whenever `userId` changes and updates state with the result. The non-obvious part: if `userId` changes twice in quick succession, both requests run in parallel — whichever finishes last wins, even if it is the stale one. There is no cancellation here. In practice this means a slow network response from a previous user can overwrite the current user's data. The cleanup function in the return handles unmount but not fast re-renders.

Makes sense, or want me to dig into any part?

---

### Database transaction with rollback

Claude writes a multi-step DB transaction. Vibecheck fires:

---

This wraps the user creation and wallet initialization in a single transaction so both succeed or neither does. The non-obvious part: if the wallet creation fails, the transaction rolls back the user row too — you will not end up with a user who has no wallet. What is easy to miss: any error thrown inside the transaction block triggers rollback automatically, but errors thrown *after* `commit()` do not. Post-commit side effects like sending a welcome email are outside the safety net.

Makes sense, or want me to dig into any part?

---

### Trivial rename — no narration

Claude renames `getUserData` to `fetchUser`. Vibecheck stays silent. No narration is written. The change is obvious from reading it.

---

### React state mutation

Claude writes a handler that updates nested state. Vibecheck fires:

---

This updates the user's address inside the profile object. The non-obvious part: it spreads the top-level `profile` object but replaces `address` entirely — any fields inside the old `address` that you do not explicitly include will be lost. If `address` previously had a `verified` flag, it disappears silently after this update runs.

Makes sense, or want me to dig into any part?

---

### Input sanitization / XSS prevention

Claude writes a function that renders user-provided HTML. Vibecheck fires:

---

This renders the message field directly into the DOM using innerHTML. The non-obvious part: `DOMPurify.sanitize()` is called before insertion, which strips dangerous tags and attributes — but only if the content is a string. If `message` is undefined or null, `sanitize()` returns an empty string silently and nothing renders. There is no error, no fallback, just blank output.

Makes sense, or want me to dig into any part?

---

### Middleware chain — order matters

Claude adds rate limiting middleware to an Express app. Vibecheck fires:

---

This adds rate limiting before the auth middleware in the chain. The non-obvious part: order determines whose requests are bucketed together. With rate limiting first, every request — authenticated or not — counts toward the same limit, and a rate-limited user gets 429 before their token is ever checked. Move it after auth and unauthenticated requests stop counting against authenticated users' quotas. Which behavior you want depends on your threat model, not on which order felt natural to write.

Makes sense, or want me to dig into any part?

---

## Skip behavior

If the user replies with any of the following, respect it immediately and continue without explanation:
- "got it"
- "skip"
- "move on"
- "I understand"
- "next"
- Or any equivalent signal that they want to proceed

Do not ask a follow-up. Do not summarize what you were going to explain. Just continue.

Skipping is a conscious choice. It is fundamentally different from passively accepting output without reading it.

## Anti-patterns — never do these

- **Reading the code aloud:** "This function takes a userId, queries the database, and returns the result." — that is just narrating syntax.
- **Over-explaining obvious things:** "This sets `isLoading` to true before the request starts." — visible from reading.
- **Padding with praise:** "Great, I've written a clean implementation that..." — skip the preamble.
- **Firing on trivial changes:** renaming, formatting, comment edits — do not narrate these.
- **Vague warnings:** "Be careful with this" — always say specifically what to be careful about and why.
- **Wall of text:** If your narration is more than 5 sentences, cut it. One non-obvious thing explained well beats three things explained vaguely.
