---
name: glossary
description: Create and maintain GLOSSARY.md when defining domain terms, resolving ambiguous language, or establishing shared project vocabulary.
---

# Glossary

Maintain a shared vocabulary in a single GLOSSARY.md at the repository root.

- Read the existing glossary before proposing changes.
- Identify vague terms, conflicting definitions, and synonyms. Propose one canonical term per concept.
- Use concrete scenarios to clarify boundaries between concepts. Check relevant code and docs for conflicting usage.
- Ask the user when the intended meaning is unclear. Do not record guesses as agreed definitions.
- Capture resolved terms immediately. Create GLOSSARY.md when the first term is resolved.
- Include only project-specific domain terms. Keep definitions to one or two sentences, excluding implementation details, specifications, and decisions.
- List discouraged synonyms only when they mean the same concept.

Use the existing format, or start with:

```markdown
# Glossary

## {Canonical term}

{One or two sentences defining the concept in this project's context.}

_Avoid_: {Discouraged synonyms, if any}.
```
