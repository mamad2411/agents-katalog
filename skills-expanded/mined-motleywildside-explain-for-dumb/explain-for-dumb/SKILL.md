---
name: explain-for-dumb
description: Explains code changes (branch diff vs master, or uncommitted changes) in plain human language, no scary jargon — so the user understands what an agent (or they) actually changed. Two modes - a "for dummies" story (what was, what happened, how it was done) or a per-file walkthrough. Use when the user says "explain-for-dumb", "explain my changes", "what did the agent do", "walk me through the diff", or wants a plain-language recap of a PR/diff.
---

# Explain For Dumb

Explain code changes so a person who delegated the implementation (and may not know the codebase deeply) can stay aligned with what now lives in the codebase. The reader is smart but tired — no jargon walls, no line-by-line diff recitals.

The goal is to restore context and understanding, not to replace tests or code review.

**Answer in the language the user is speaking in this session.**

## Step 1 — Decide WHAT to explain (scope)

Run:
- `git branch --show-current`
- `git status --porcelain` (uncommitted = staged + unstaged + untracked)

Then:

1. **On master/main:**
   - Uncommitted changes exist → explain only those.
   - Working tree clean → say there is nothing to explain and stop. Do not invent work.
2. **On a feature branch:**
   - Uncommitted changes exist → **ask the user** (AskUserQuestion): explain the whole branch diff vs master, or only the uncommitted changes.
   - Clean tree → explain the whole branch diff vs master, no question needed.

Getting the branch diff: `git diff $(git merge-base master HEAD)...HEAD` (use `origin/master` if there is no local `master`). For uncommitted: `git diff HEAD` plus untracked files' contents.

## Step 2 — Ask which mode (always ask, AskUserQuestion)

1. **For dummies** — one coherent story, not a file list:
   - **Before:** how things worked / what was broken before.
   - **After:** what works now / what the user-visible outcome is.
   - **How it was done:** the approach in everyday analogies, almost no code, every term explained the moment it appears.
2. **Per-file walkthrough** — go file by file:
   - What this file is responsible for (one sentence).
   - What changed in it and why.
   - Each new/changed function in human words: "here is function X — it exists to …". No jargon; if a technical word is unavoidable, explain it inline in parentheses.
   - Link files as clickable markdown links **with line anchors to the changed code**: `[file.tsx:42](relative/path/file.tsx#L42)`, or a range `[file.tsx:42-51](relative/path/file.tsx#L42-L51)` for a function/block. Point at the actual changed hunk, not just the file.

## Step 3 — Actually understand before explaining

- Read the surrounding code of changed hunks, not just the diff — explanations must be true, not guessed. Read callers/usages of new functions when their purpose isn't obvious from the diff.
- Explain intent and meaning, never paraphrase the diff line by line.
- Huge diffs (~30+ files): group changes into logical chunks (feature area / concern) and walk the chunks; don't grind through every file.

## Step 4 — Wrap up (both modes)

End with:
- **Summary:** 3–5 bullet points of what changed overall.

Do NOT add a code-review section (risks, suspicious spots, "things to watch out for") — this skill explains changes, it doesn't review them.
