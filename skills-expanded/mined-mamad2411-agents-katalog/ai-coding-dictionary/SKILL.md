---
name: ai-coding-dictionary
description: Use when the user asks about AI coding jargon, wants to clarify a term like context engineering, harness engineering, prompt engineering, or agent harness, or when the agent needs to agree on a term definition before continuing a technical discussion.
triggers: [user, model]
---
# AI Coding Dictionary

## Overview

AI coding has a growing set of overloaded terms. This skill resolves them by pointing to the canonical definitions in `docs/AI-CODING-DICTIONARY.md`.

## When to use

- User asks "what is X?" about an AI coding term.
- You are about to use a term (e.g., "harness engineering") and want to confirm the user shares the definition.
- A conversation is drifting because a term is being used loosely.

## How to use

1. Read `docs/AI-CODING-DICTIONARY.md`.
2. Find the term. If it is missing, add a tight definition following the existing format (one or two sentences, flag ambiguities, list what to avoid).
3. Quote the definition to the user and ask if they want to add, edit, or remove any nuance.
4. If the term is not in the dictionary and you cannot define it confidently, invoke `research` to find primary sources first.

## Cross-skills

- Use `research` when the dictionary does not yet contain the term and you need authoritative sources.
- Use `teach` when the user wants a full lesson instead of a one-line definition.
