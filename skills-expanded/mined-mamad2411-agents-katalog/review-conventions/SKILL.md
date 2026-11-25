---
name: review-conventions
description: This skill should be used whenever reviewing or commenting on a pull request or merge request, leaving review feedback, or phrasing a code-review comment, even when conventions are not explicitly mentioned, applying the Conventional Comments standard to code review comments.
---

# Review conventions

A reusable standard for code review comments, based on
[Conventional Comments](https://conventionalcomments.org/). Apply it by
default when commenting on pull or merge requests. This skill is the
baseline standard, not an opinionated ruleset: compose it with your own
context (see "Adapt to your context" below).

## Format

`<label> [decorations]: <subject>`

Followed by an optional discussion paragraph.

- The label states the kind of comment, so the reader immediately knows
  intent (a `praise` reads very differently from an `issue`).
- A decoration qualifies it, mainly to signal whether it must be resolved.
- The subject is the actionable message; keep the discussion below it.

## Labels

- `praise`: highlight something positive.
- `nitpick`: trivial, preference-based; usually non-blocking.
- `suggestion`: propose a specific improvement.
- `issue`: point out a problem; pair with a suggestion when you can.
- `question`: ask for clarification.
- `thought`: a non-blocking idea sparked by the change.
- `chore`: a small required task (changelog, tests, formatting).
- `note`: a non-blocking observation, for awareness.

## Decorations

- `(blocking)`: must be resolved before approval.
- `(non-blocking)`: should not prevent approval.
- `(if-minor)`: resolve only if the change is minor.

## Examples

```
praise: clean separation of concerns here, easy to follow.
suggestion (non-blocking): extract this into a helper to avoid the repetition.
issue (blocking): this nil case is not handled and will panic.
question: is this timeout intentional, or should it match the client?
nitpick (if-minor): rename `tmp` to something descriptive.
```

## Adapt to your context

This skill stays generic on purpose. Layer your own conventions on top:
your team's required labels, approval rules, or tone guidelines belong in
your own `CLAUDE.md` or a higher-priority skill. This skill does not impose
them.
