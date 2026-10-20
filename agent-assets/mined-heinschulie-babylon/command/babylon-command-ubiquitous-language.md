---
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
description: Extract DDD-style ubiquitous language glossary from conversation context, flag ambiguities, propose canonical terms, save to UBIQUITOUS_LANGUAGE.md
model: opus
---

# Purpose

Extract and formalize domain terminology from the current conversation into a consistent, opinionated glossary. Follow the Instructions and Workflow below to produce a `UBIQUITOUS_LANGUAGE.md` file in the working directory.

## Instructions

- Scan the full conversation for domain-relevant nouns, verbs, and concepts
- Be opinionated: when multiple words exist for the same concept, pick the best one and list the rest as "aliases to avoid"
- Flag conflicts explicitly: if a term is used ambiguously, call it out with a clear recommendation
- Keep definitions to one sentence max — define what it IS, not what it does
- Show relationships between terms using bold names and express cardinality where obvious
- Only include domain terms — skip generic programming concepts (array, function, endpoint) unless they carry domain-specific meaning
- Group terms into multiple tables when natural clusters emerge (by subdomain, lifecycle, or actor); use one table if all terms belong to a single cohesive domain — don't force groupings
- Write an example dialogue (3-5 exchanges) between a dev and domain expert demonstrating precise term usage and clarifying boundaries between related concepts
- When re-running against an existing file: read it first, incorporate new terms, update evolved definitions, mark changed entries "(updated)" and new entries "(new)", re-flag ambiguities, and rewrite the example dialogue

## Workflow

1. Check if `UBIQUITOUS_LANGUAGE.md` already exists in the working directory; if so, read it as baseline
2. Scan the conversation for all domain-relevant terms, identifying:
   - Same word used for different concepts (ambiguity)
   - Different words used for the same concept (synonyms)
   - Vague or overloaded terms
3. Propose a canonical glossary with opinionated term choices
4. Organize terms into grouped tables with columns: Term (bold), Definition, Aliases to avoid
5. Write a Relationships section expressing how terms connect with cardinality
6. Write an example dialogue section showing terms used precisely in context
7. Write a Flagged ambiguities section listing every ambiguous usage with recommendations
8. Save the result to `UBIQUITOUS_LANGUAGE.md` in the working directory using the table/section format described above

## Report

State: "Written/updated `UBIQUITOUS_LANGUAGE.md`. From this point forward I will use these terms consistently. If I drift from this language or you notice a term that should be added, let me know." Then provide a concise summary listing: number of terms defined, number of ambiguities flagged, and any key decisions made about canonical term choices.