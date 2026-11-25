---
name: commit-message
version: 1.0.0
description: Turn a diff or plain description into a conventional-commit message - honest type and scope, a why-focused body, breaking changes flagged, nothing invented.
triggers:
  - commit message
  - write a commit message
  - conventional commit
  - describe this change for git
capabilities: []
inputs:
  - name: change
    required: true
    description: What changed - a diff, a diff summary, or a plain description.
  - name: convention
    required: false
    description: House style if not conventional-commits (e.g. plain imperative, ticket-prefixed).
---

# Commit Message

## When to use
Use this when you have a change - a diff, a summary, or a spoken description - and need the commit message a maintainer will thank you for two years later: what changed, why, and what to watch for.

**Not for:** PR descriptions or changelogs (those summarize many commits and address users, not future maintainers); release notes; or squashing unrelated changes into one message. If the change does several unrelated things, that is a signal to split the commit, not to write one vague message.

## Method
1. **Find the single dominant intent.** One change, one reason. If you cannot name it in a phrase, the commit is probably two commits.
2. **Pick the type honestly.** `fix` = behavior correction; `feat` = new capability; `refactor` = no behavior change; `docs`, `test`, `chore` as they say. *Decision point:* if the change mixes types, choose the dominant one and mention the rest in the body - never label a refactor `fix` to look productive.
3. **Set the scope from the actual area touched** (`parser`, `auth`). Omit it rather than invent one when the change is broad.
4. **Write the subject:** `type(scope): imperative summary`, 72 chars max, no trailing period.
5. **Write the body (wrap ~72 cols).** Explain WHY: the bug's cause, the constraint, the reasoning. The diff already shows what. *Decision point:* if the description is too thin to know why, say so plainly rather than inventing a rationale.
6. **Add footers.** `BREAKING CHANGE:` for incompatible changes; ticket refs only if given.

## Example
**Input:** "we stopped caching user avatars because stale images showed after profile updates, now they get a cache-busting hash in the url"

**Output:**
```
fix(avatars): cache-bust avatar URLs with a content hash

Profile updates left stale avatars on screen because the CDN kept
serving the cached image at the unchanged URL. Appending a content
hash makes every new upload a new URL, so caches stay hot for
unchanged avatars while updates appear immediately.

Old cached URLs remain valid until CDN TTL expiry; no purge needed.
```

## Pitfalls
- **Restating the diff.** "Changed line 42 in parser.js" is noise; the diff shows that. Record the reason instead.
- **Dishonest type.** Tagging a behavior change `refactor`, or a cleanup `fix`, so history lies about what happened.
- **Inventing metadata.** Ticket numbers, benchmarks, or reviewer names that were never provided.
- **Silent breaking changes.** Shipping an incompatible change with no `BREAKING CHANGE:` footer, so downstream discovers it in production.

## Output format
```
type(scope): imperative subject, <=72 chars, no period

Why this change exists: the problem, its cause or the constraint
that forced this design. Wrapped at ~72 columns. Omit if the
subject is genuinely self-explanatory.

BREAKING CHANGE: <what breaks and the migration> (only if true)
Refs: <ticket> (only if provided)
```
