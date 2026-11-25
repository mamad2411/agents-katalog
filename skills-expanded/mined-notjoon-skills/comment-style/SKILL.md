---
name: comment-style
description: Rules for writing and revising code comments. Use whenever you write a new comment, review or rewrite existing comments, or a task asks you to clean up, tidy, or refine comments. Follows the Linux kernel commenting guidance for prose and intent, while leaving comment delimiters and layout to the host language or project.
---

# Comment style

Rules for any code comment you write or revise.

Follow the Linux kernel commenting guidance for the content and prose of
comments. Do not copy its `/* ... */` delimiter or block layout rules unless
the surrounding project already uses them.

## 1. Describe WHAT, not HOW

Comments should explain what the code does, guarantees, represents, or exists
to accomplish. Do not narrate the implementation step by step when the code
itself can make those steps clear.

- Rewrite procedural comments such as "first check X, then increment Y, then
  store Z" into a statement of the behavior, invariant, or result that matters.
- Do not use comments to compensate for code that is unnecessarily difficult
  to follow. Prefer clearer code when that is within the scope of the task.
- Remove or shorten comments that merely repeat information already obvious
  from the code, type, name, or signature.

## 2. Explain WHY when it adds useful context

A useful comment may explain why a choice exists when that reason is not
recoverable from the code alone. Preserve context that helps a future reader
understand constraints or avoid breaking an invariant.

Useful context includes:

- where a value comes from and what invariant ties it to another value
- non-obvious constraints or ordering requirements
- compatibility, correctness, or safety reasons for otherwise surprising code
- the reason a workaround exists, preferably with a link when appropriate

When condensing a comment, remove procedural narration before removing this
kind of context.

## 3. Keep comments focused and close to their purpose

Avoid excessive commentary inside function bodies. If a function needs many
comments to explain each part of its implementation, the code may need a
clearer structure instead.

Small local comments are appropriate when they call out a non-obvious detail,
constraint, workaround, or surprising behavior. For broader behavior, prefer a
comment near the function or declaration that says what it does and, when
useful, why it does it.

Do not add boilerplate documentation that only restates a function signature,
field name, type, or other information already visible in the declaration.

## 4. Prefer plain sentence structure

Write comments as direct, natural prose. Prefer short sentences with a clear
subject and purpose over compressed punctuation or dense modifier chains.

- Avoid em dashes when a comma, period, parentheses, or a separate sentence
  reads more naturally. They are not forbidden, but should be uncommon.
- Avoid semicolons when two ordinary sentences are clearer. Use one only when
  it materially improves the sentence.
- Avoid inventing or overusing dash-joined compounds for concepts that can be
  expressed plainly. Prefer phrases such as "at parse time" over "parse-time"
  when the compound adds no precision.
- Keep established terms, proper names, protocol names, and code identifiers
  unchanged when their spelling includes a hyphen or dash.

Do not force a rewrite solely to remove punctuation or a legitimate compound
when the existing wording is already the clearest option.

## 5. Preserve useful comments during cleanup

WHAT over HOW is not a reason to delete information that cannot be recovered
from the code. When revising an existing comment, preserve important context
unless it is wrong, obsolete, or clearly redundant.

If unsure whether a piece of context is important, prefer keeping it and
making the wording clearer.

## Scope of a cleanup task

When asked to tidy comments after a change, only touch comments on or directly
related to the changed lines. Leave unrelated existing comments alone unless
told otherwise. Never alter code lines while editing comments. Run the
formatter and tests afterward when the task and environment make that
appropriate.
