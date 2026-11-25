---
name: domain-language
description: Fixes the domain language of one feature after the interview, so the spec, code, tests and UI all say the same thing. It records one agreed term per concept, its definition, its name in code and in each UI language, the words not to use, and the states and actions of the main records. It borrows only the ubiquitous-language idea from DDD; it adds no aggregates, bounded contexts or layers. Use it right after on-the-spot in the feature-delivery-pipeline, and whenever the user asks for a glossary, domain language, ubiquitous language, "what do we call this", or notices that two words name the same thing.
---

# Domain language

Scope: only the terms of the current feature, plus the existing terms it touches. Do not model the whole system. Do not introduce DDD structure: no aggregates, entities, value objects, bounded contexts or repositories.

## Inputs

- `.scratchpad/<slug>/interview-decisions.md`
- The code, tests and UI text that the feature touches. Existing names win unless they are wrong.
- The UI languages of the project (for example: the shop in Spanish and English, the back office in English only).

## Steps

1. List every noun and verb in the interview decisions that names a thing, a person, a state or an action of the feature.
2. Group synonyms. For each group, choose one term. Prefer the word a user of the feature would say, then the word the code already uses.
3. For each term, write one table row: term, definition in one sentence, code identifier (table, column, type, route segment), UI text in each UI language, and the words to avoid.
4. For each record with a lifecycle, list its states and the actions that move it between states, with who can do each action. Add a `stateDiagram-v2` (`plain-visual-docs`).
5. Write the open ambiguities: a word that means two things, or a concept without a name. Resolve each one with the recommended option, or ask the user.
6. Check the result against the code. Every identifier that already exists must match its current spelling. Check URL paths, query parameters and form field names too. They are public names that are hard to change later.

## Output

Save `.scratchpad/<slug>/domain-language.md` in the conversation language, with code identifiers as the code spells them. `write-acceptance-spec` copies the table and the state diagram into a `## Domain language` section of the spec, so the language stays in the repository.

From then on, specs, plans, code, tests, commit messages and UI text use only the chosen terms. A review that finds a word from the "avoid" column reports it as a 🟡 finding.

## Template

```markdown
| Term | Definition | Code | UI (es) | UI (en) | Avoid |
| --- | --- | --- | --- | --- | --- |
| order | What a customer bought in one checkout, from payment to delivery or cancellation | `orders`, `Order` | pedido | order | purchase, sale, cart |
```

Use one UI column per UI language of the project.
