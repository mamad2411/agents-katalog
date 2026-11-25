---
name: persona-mapping
description: "Build user models that actually inform decisions. Maps motivations, friction points, and decision triggers beyond demographic templates. Use when building for multiple user types or when the agent needs to reason about different users."
---

# Persona Mapping

Build user models that actually inform decisions.

## How to use

- `/persona-mapping` Apply persona constraints to this conversation.

## Constraints

### What a Persona Must Include
- Motivation: what drives them to seek this product
- Context: when and where they encounter the problem
- Current solution: what they do today (including doing nothing)
- Decision trigger: what would make them switch
- Success metric: how they'd know this product is working for them
- NEVER include demographics unless they directly affect product behavior

### What a Persona Must NOT Be
- A demographic profile with a stock photo
- An aspirational user you wish you had
- A composite of all users (that's nobody)
- Static. Personas should update as you learn more.

### Usage Rules
- MUST have no more than 3 primary personas for any product
- MUST prioritize: which persona do you serve first?
- SHOULD include an "anti-persona" (who this product is NOT for)
- Every feature decision should reference which persona benefits
- Conflicting persona needs MUST be resolved by priority, not by compromise

### Anti-Patterns
- Personas without behavioral differences (if they'd use the product the same way, they're one persona)
- Creating personas before talking to real users
- Personas that live in a document nobody reads
- Designing for the edge case persona instead of the primary one
