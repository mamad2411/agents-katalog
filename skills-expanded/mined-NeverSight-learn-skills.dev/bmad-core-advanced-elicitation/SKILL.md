---
name: bmad-core-advanced-elicitation
description: >-
  Use this skill to iteratively enhance and deepen recently generated content
  through structured elicitation methods drawn from a library of 50 techniques.
  Invoke when the user says "elicit", "advanced elicitation", or "run
  elicitation", or when another skill needs to push output quality higher before
  proceeding. Input is the content or section most recently produced in the
  session. Output is an improved version reached through interactive application
  of multi-perspective analysis, creative reframing, risk assessment, assumption
  challenging, or collaborative reasoning techniques chosen from a menu. The
  user selects methods one at a time, each building on previous enhancements,
  until satisfied and exits with "x". Unlike party-mode brainstorming, this
  skill operates on existing output rather than generating new ideas from
  scratch. Do not invoke when there is no prior content to refine.
argument-hint: "Optionally provide the content or section to enhance. When invoked from another skill, receives current section content automatically."
metadata:
  internal: "true"
  bmad:
    module: "core"
    type: "task"
---

# Advanced Elicitation

Push the LLM to reconsider, refine, and improve its recent output using structured elicitation methods.

## Outcome

Enhanced, refined content produced through iterative application of structured elicitation methods — multi-perspective analysis, creative techniques, risk assessment, and collaborative reasoning.

## Core Rules

- Execute ALL steps in order. Do not skip or reorder.
- HALT immediately when halt-conditions are met.
- Each action within a step is REQUIRED.
- Always speak in your agent communication style using the configured `{communication_language}`.
- Always re-offer the menu after each method execution until the user selects `x`.
- Each method application builds upon previous enhancements — track all changes iteratively.

## Integration

When invoked from another skill or process:

1. Receive or review the current section content that was just generated.
2. Apply elicitation methods iteratively to enhance that specific content.
3. Return the enhanced version back when user selects `x` to proceed.
4. The enhanced content replaces the original section content in the calling skill's output.

## Execution Order

Follow these steps in order.

1. [Initialize](./steps/initialize.md) — Load methods registry, analyze context, select initial methods
2. [Elicit](./steps/elicit.md) — Interactive elicitation loop: present menu, execute methods, refine content

## Halt Conditions

- HALT if no prior content or context exists to elicit from — there is nothing to refine
- HALT if the methods registry (`./data/methods.csv`) is unreadable or empty
- HALT if the user selects a method but provides no feedback after repeated prompting, making iterative refinement impossible

## Data Files

- [./data/methods.csv](./data/methods.csv) — 50 elicitation methods with categories, descriptions, and output patterns

## When to Use

Use this skill when:
- The user says "elicit", "advanced elicitation", or "run elicitation"
- The user wants to push the LLM to reconsider, refine, and improve its recent output
- Another skill needs to enhance generated content using structured elicitation methods
- The user wants multi-perspective analysis, creative techniques, or risk assessment applied to current content
- The user wants to deepen or expand on output already produced in a workflow

