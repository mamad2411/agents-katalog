---
name: name-it

description: Suggest clear, natural, and appropriate names for skills, variables, features, and other technical concepts. Use when something needs a better name, the current name feels awkward, or you are unsure what to call something.

metadata:

  disable-model-invocation: true

---

# Name It

What should this be called?

This skill helps choose names for technical concepts such as skills, variables, features, commands, functions, files, modules, and similar artifacts.

The goal is not to produce the most clever name. The goal is to find a name that accurately communicates what the thing is and fits its context.

## Understand the thing first

Before suggesting names, determine:

- What the thing does
- What problem it solves
- What it is responsible for
- What it is not responsible for
- Where the name will be used
- The surrounding naming convention
- Any length, style, or compatibility constraints

Use the surrounding code, skills, or project terminology when available.

Do not name something from its implementation details alone when its purpose is more important.

## Naming criteria

Prefer names that are:

- **Clear** — the purpose is understandable from the name.
- **Specific** — avoids being so broad that it could mean many things.
- **Natural** — sounds like something a developer would actually name it.
- **Consistent** — matches nearby naming conventions.
- **Concise** — avoids unnecessary words.
- **Stable** — describes the underlying responsibility rather than a temporary implementation detail.

Avoid names that are:

- Needlessly clever
- Buzzword-heavy
- Overly generic
- Redundant
- Misleading
- Longer than necessary
- Based on assumptions about implementation that may change

Do not prefer a "cool" name over an accurate one unless the user explicitly wants branding or a memorable name.

## Generate candidates

Provide a small set of strong candidates rather than a large list of weak variations.

Normally suggest **3–7 names**.

For each candidate, include a brief reason.

When useful, group candidates by style:

- **Literal** — directly describes the purpose
- **Concise** — shorter but still clear
- **Conceptual** — names the underlying concept
- **Distinctive** — more memorable while remaining understandable

Do not generate multiple variants that differ only by punctuation or trivial wording.

## Choose a recommendation

After presenting candidates, identify the **best default**.

The recommendation should be based on the actual context, not personal preference alone.

Briefly explain why it is the strongest fit and mention the main trade-off when one exists.

For example:

> **Best: `what-next`** — directly describes the action the skill performs and fits the existing imperative-style skill names.

## Naming by context

Consider the conventions appropriate to the thing being named.

Examples:

- **Skill** → usually describe the user-facing purpose.
- **Variable** → describe the value it represents.
- **Function / command** → describe the action it performs.
- **Feature** → describe the capability or user-visible behavior.
- **File / module** → describe the responsibility or contents.
- **Internal implementation** → implementation-oriented names may be appropriate when the implementation itself is the important distinction.

Follow the project's existing convention whenever one is already established.

## When the current name is good

If the existing name is already clear and appropriate, say so.

Do not rename something merely to produce a different name.

## When context is insufficient

If the correct name depends on an important distinction that is not available, ask for the smallest piece of information needed.

Do not invent context just to produce a confident-sounding name.

## Avoid unnecessary renaming

A name should change only when the new name provides a meaningful improvement.

Prefer:

> `skill-gap`

over a more elaborate alternative when the existing name already communicates the concept clearly.

## How to answer

Format every reply as:

1. **Best name** — the strongest recommendation.
2. **Alternatives** — 2–6 other good candidates.
3. **Why** — a concise explanation of the recommendation and important trade-offs.

When the user asks for a specific naming style, optimize for that style.

When the user provides an existing name, evaluate it before suggesting replacements.

Stop after that.

## Maintenance

This skill should remain focused on naming and naming decisions.

Only update this file when its naming criteria, context rules, or output format need to change.