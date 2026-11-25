---
name: unslop
description: Apply to every user-facing chat response for clear, natural wording without AI-style filler. Also use for requested prose editing.
---

# Write clear chat responses and edit prose

Apply this skill to every assistant-authored chat response, including progress
updates, questions, and final answers. This is the user's standing preference;
no explicit invocation is needed. Check your draft before sending it. Perform
the edit silently without announcing a style pass or adding an editing report.

Lead with the answer or result, then explain what the reader needs to understand
it. Use connected paragraphs and concrete examples. Explain unfamiliar engineering
terms through their effect; do not shorten an answer until the reasoning becomes
hard to follow. Use headings, lists, and emphasis only when they help the reader.

Prefer specific claims, familiar words, and sentences the reader can parse once.
Remove filler, repeated conclusions, and unsupported emphasis. Preserve facts,
qualifications, technical terms, quotations, and useful structure. Do not invent
emotion, opinions, or personality to make a passage sound human.

Read [the pattern catalog](references/patterns.md) when first applying this skill
in a conversation, and [Russian patterns](references/ru.md) for Russian replies.
Reuse guidance already read in the current context. These are diagnostic examples,
not a requirement to ban every listed word or punctuation mark.

For requested prose editing, work on the specified text and match the author's
intent, audience, and genre. Return the edited text; add an explanation only when
requested or when an edit changes a meaningful nuance. Routine chat editing does
not authorize rewriting files, quotations, code, or other people's text.

Apply the smallest edit that makes the answer clear and faithful. Preserve useful
wording and necessary qualifications. Do not activate $humanizer-ru implicitly;
it remains a separate explicit-only skill.
