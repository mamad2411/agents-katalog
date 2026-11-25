---
name: smallest-change-first
description: Use before writing any new code, function, file, or dependency — walks a decision ladder that prefers reuse over new code, and requires asking before adding anything beyond the literal request.
---

# Smallest Change First

## Overview

New code is a liability the moment it's written: it has to be read, tested, and maintained forever
after. Most requests don't need new code at all — they need something that already exists, used
correctly.

**Core principle:** the best code is the code you don't write.

## The Ladder

Before writing anything, walk this ladder in order. Stop at the first step that resolves the need.

1. **Does this need to exist at all?** Is the request actually solved by deleting something, or by
   not doing the thing? Some "fixes" are actually removals.
2. **Is it already in this codebase?** Grep/graphify for an existing function, class, or pattern
   that does this or something close enough to extend.
3. **Is it in the language's standard library?** Don't hand-roll what `stdlib` already provides
   correctly and tested.
4. **Is it a native platform/framework feature?** Check the framework's own docs (see the
   researcher agent) before writing custom logic — many "custom" needs are a one-line config flag.
5. **Is it an already-adopted dependency in this project?** Check `package.json`/`pyproject.toml`/
   `build.gradle`/etc. for a library already in use that does this, before adding a new one.
6. **Can it be one line?** If steps 1–5 don't resolve it, can the need be met in a single
   expression rather than a new abstraction?
7. **Only now, write the minimum code that solves the stated problem.** No more.

## The "ask before extra" rule

If step 5 concludes a *new* dependency is genuinely warranted, or if satisfying the request would
require touching files, adding abstractions, or writing code beyond the literal scope of what was
asked — **stop and ask the user first.** Do not silently expand scope because a better version
occurred to you mid-task. Surface it, explain why, let them decide.

## Deliberate shortcuts

Sometimes the right call under the ladder is still an intentional simplification — e.g. step 6/7
lands on something that works for the current case but has a known ceiling. When that happens,
don't leave a silent TODO. Log it via the `logging-tradeoffs` skill instead: a documented,
findable tradeoff beats an undocumented one every time.

## Red flags

| Thought | Reality |
|---|---|
| "I'll just add a small helper for this" | Check steps 2–4 first — it may already exist. |
| "This library is heavy, I'll write my own version" | A hand-rolled subset is usually worse than the dependency, and now it's yours to maintain forever. |
| "While I'm in here, I'll also clean up X" | That's scope creep. Surface it, ask, don't just do it. |
| "This edge case probably won't happen" | If it's in scope, handle it; if it's not, don't add speculative handling either. |
