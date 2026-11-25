---
name: human-commit-messages
description: >-
  Write commit messages and PR descriptions the way an engineer does: a plain
  summary of what changed and why. Use this WHENEVER you write a git commit
  message, a PR or MR title and body, or a changelog entry. Emoji prefixes
  ("✨ feat:", "🐛 fix:"), gushing language ("amazing new feature"), restating
  the diff line by line, and padded multi-paragraph bodies for a one-line change
  are the tell that a model wrote it. Keep a short imperative subject, an
  optional body that explains the why and any non-obvious tradeoff, and nothing
  the diff already shows.
---

# Human commit messages

A commit message is a note to the next person reading `git log`, often you in six
months. It should say what changed and, when it is not obvious, why. AI-written
commits give themselves away with emoji prefixes, marketing adjectives, and bodies
that narrate the diff the reader can already see.

The rule: the subject says what changed in the imperative; the body, if any, says
why. Never decorate, never restate the code.

## Subject line

- Imperative mood: "Add retry to the upload client", not "Added" or "Adds" or
  "This commit adds".
- Short, roughly under 70 characters. Specific over cute.
- No emoji. No "✨", no "🚀". If the repo uses Conventional Commits, plain
  `fix:` / `feat:` prefixes are fine, but without an emoji glued on.
- No hype: not "Add amazing new caching layer", just "Cache parsed config".

## Body, only when it adds something

Most small commits need no body. Add one when there is a why the diff cannot show:

- the reason behind the change (the bug it fixes, the constraint it satisfies)
- a tradeoff or a path not taken ("kept the sync API for back-compat")
- a follow-up or a known limitation

Do not write a body that just lists the files you touched or paraphrases the code
line by line. The reader has the diff.

## Before and after

Before:
```
✨ feat: Implement an amazing new robust retry mechanism!!! 🚀

- Added retry function to client.js
- Imported the sleep helper
- Updated the call site in upload.js
- Bumped the version
```

After:
```
Retry failed uploads up to 3 times

The upload endpoint returns sporadic 503s under load. Retry with backoff on
5xx only; 4xx still fails fast so we do not mask bad requests.
```

## PR descriptions

Same spirit at a larger scale: a plain summary of what the PR does and why, a
short list of notable changes if it is large, and how to test it if that is not
obvious. Cut the "This PR introduces a powerful new..." opener and the emoji
section headers.

## Before you deliver

Read the subject: is it an imperative summary a teammate would understand at a
glance, with no emoji and no hype? Read the body: does every line tell the reader
something the diff does not? If a line just restates the code, delete it.

For the prose inside bodies and PR descriptions, pair with `no-filler-phrases`,
`no-em-dashes`, and `no-fancy-ascii`.
