---
name: one-liner

description: Turn a long explanation, discussion, or context into one or two concise sentences that preserve the essential meaning and can be reused as a description, summary, prompt, or context note.

metadata:

  disable-model-invocation: true

---

# One Liner

Make it reusable in one or two sentences.

This skill compresses a long explanation, discussion, or piece of context into **one or two concise sentences** that preserve the essential meaning and remain useful when reused elsewhere.

The result should stand on its own without requiring the original explanation.

It is a **compression tool**, not a general summarizer.

## Preserve the core meaning

Before rewriting, identify:

- The main subject
- The essential point
- The purpose or behavior being described
- Important constraints or distinctions
- Any terminology that must remain precise
- The intended context of reuse, when available

Keep information that is necessary to correctly understand or use the result.

Remove:

- Repetition
- Examples that are not essential
- Background that does not affect the meaning
- Conversational filler
- Explanations of obvious details
- Secondary points that do not survive the compression

Do not remove a detail if doing so would materially change the meaning.

## Make it reusable

The result should work when copied into another context such as:

- A skill description
- A prompt
- A commit or task note
- A handoff summary
- Documentation
- A feature description
- Context for another agent
- A short explanation to another person

Prefer concrete wording over vague phrases like:

> "This thing helps with stuff..."

The output should communicate **what it is, what it does, and why it matters** when those details are relevant.

## One or two sentences

Prefer **one sentence** when the idea can be expressed cleanly.

Use **two sentences** when combining the purpose and an important boundary or condition would otherwise make the sentence unclear.

Do not force two sentences when one is sufficient.

Do not exceed two sentences unless explicitly requested.

## Preserve terminology

Keep important technical terms, names, identifiers, and domain-specific terminology when replacing them would reduce precision.

Do not introduce new terminology just to make the sentence sound sophisticated.

## Adapt to the target context

When the user specifies where the one-liner will be used, optimize for that context.

Examples:

- **Skill description** → describe the skill's purpose and trigger.
- **Prompt context** → emphasize intent and relevant constraints.
- **Handoff note** → emphasize current state and what matters next.
- **Feature description** → emphasize user-visible behavior.
- **Documentation** → favor clarity and precise terminology.

When no target is specified, produce a neutral reusable statement.

## Avoid losing important distinctions

Do not collapse concepts that are meaningfully different.

For example:

- "recommend" is not the same as "execute"
- "available" is not the same as "installed"
- "narrow" is not the same as "split"
- "summarize" is not the same as "rewrite"

Preserve distinctions that affect how the text should be used.

## When the source is already concise

If the provided explanation is already one or two clear sentences, keep it or make only a minimal refinement.

Do not rewrite for the sake of changing wording.

## When the source is ambiguous

If the source does not provide enough information to produce a reliable one-liner, do not invent missing meaning.

Ask for the smallest clarification needed.

## How to answer

Return:

### One-liner

```text
<one or two sentence reusable version>
````

Do not include additional explanation unless the user asks for it.

## Maintenance

This skill should remain focused on compressing existing explanations or context into reusable one- or two-sentence statements.

Only update this file when its compression rules, reuse criteria, or output format need to change.