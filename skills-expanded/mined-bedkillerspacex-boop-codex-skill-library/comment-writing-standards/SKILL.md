---
name: comment-writing-standards
description: >
  Standards for when and why to write comments, what not to narrate, and how to
  document decisions, invariants, and non-obvious constraints in code. Use when
  writing comments, reviewing comment quality, documenting intent, 写注释, 注释规范,
  or deciding whether code needs a comment. Complements code-quality-standards;
  does not replace naming or structure work.
---

# Comment Writing Standards

## Scope And Authorization

- **In scope:** source you are allowed to edit; respect license and confidentiality of internal design notes.
- **Out of scope:** embedding secrets, credentials, or customer data in comments.
- Prefer fixing unclear code over papering with comments when rename/extract works.
- Pair with `code-quality-standards`, `naming-conventions-general`, and `docstring-and-typedoc` for APIs.

## When To Use

- Adding or reviewing comments / TODOs / invariants.
- Onboarding docs inside code (“why this exists”).
- Tokens: comments, invariants, intent, 写注释, non-obvious constraints.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Overall code quality | `code-quality-standards` |
| API docs / docstrings | `docstring-and-typedoc` |
| Naming only | `naming-conventions-general` |
| PR review tone | `code-review-comments-style` |
| Commit messages | `commit-message-conventions` |

## When To Comment

| Comment for | Examples |
| --- | --- |
| Why, not what | Business rule, legal constraint, historical bug |
| Invariants | “len(buf) always power of two here” |
| External contracts | Wire format quirks, vendor bugs, RFC deviations |
| Trade-offs | “O(n^2) OK: n ≤ 32 by protocol” |
| Security non-obvious | “Padding intentional against timing oracle X” |
| Workarounds | Link issue ID; expiry if temporary |

## When Not To Comment

| Avoid | Prefer |
| --- | --- |
| Narrating `i++ // increment i` | Delete comment |
| Restating the function name | Better name |
| Large commented-out code | VCS history |
| Stale lies | Update or delete |
| Secrets / prod URLs with tokens | Secret manager + config |

## Comment Styles

```go
// Good: why + constraint
// Retry only on 503: payment vendor returns 500 for business declines.
// Retrying those double-charges (INC-1842).

// Bad
// Loop over users
for _, u := range users {
```

```python
# GOOD: invariant for maintainers
# prices are minor units (cents); never float.
```

**TODO format:**

```text
// TODO(username or team): actionable next step — ticket ABC-123
```

Avoid bare `// TODO: fix later`.

## Workflow

### 1. Read surrounding style

1. Match project comment language (English vs team standard).
2. Respect linter rules (`eslint`, `godoc`, etc.).

### 2. Prefer clarity in code first

1. Rename, extract function, introduce type.
2. If still non-obvious → comment.

### 3. Write high-signal comments

1. State **motivation**, **constraint**, **risk if changed**.
2. Link ticket/RFC when durable.
3. Keep short; put long design in docs/ ADR.

### 4. Review comments in PR like code

1. Delete outdated comments in same PR as behavior change.
2. Flag comments that restate the code as nits (`code-review-comments-style`).

### 5. Special cases

| Case | Guidance |
| --- | --- |
| Public API | Use doc comments per language (`///`, `/**`, godoc) — see docstring skill |
| Security | Never include key material; describe property not secret |
| Generated code | “DO NOT EDIT” + generator pointer only |
| Protocol | Reference version and compatibility window |

### 6. Verify

1. New reader test: does comment answer a question the code doesn’t?
2. Grep for `TODO` without tickets; clean or ticket.
3. No secrets in comment grep.

### 7. Hand off

1. Team style snippet in CONTRIBUTING if missing.
2. Optional lint for banned patterns (commented-out blocks).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Content | Why / invariant | What the next line does |
| Freshness | Updated with code | Lie from 2019 |
| TODO | Owner + ticket | `TODO` forever |
| Secrets | None | AWS key “for debug” |
| Length | 1–5 lines | Essay in hot path |

## Output Checklist

- [ ] Code clarified before commenting where possible
- [ ] Comments explain why/invariants/constraints
- [ ] No narration or dead commented-out blocks
- [ ] TODOs have owner/ticket
- [ ] No secrets in comments
- [ ] Public APIs use proper doc comments if required
- [ ] Stale comments removed with behavior change

## Rules

- Comments are for humans; keep them true and minimal.
- Prefer structure and names over commentary when equal effort.
- Complements, does not replace, `code-quality-standards`.
- Never store credentials in comments.
