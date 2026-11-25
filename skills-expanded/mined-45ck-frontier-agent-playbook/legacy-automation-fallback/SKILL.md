---
name: legacy-automation-fallback
description: Use when reviewing a prompt, spec, workflow, or architecture for deterministic-first regressions that replace LLM judgment with rules, keyword routing, fixed templates, or brittle scripts. Trigger whenever an LLM-native task is quietly being collapsed into old automation logic.
---
# Legacy Automation Fallback

Goal: detect when a design is using legacy automation patterns where the LLM should be doing the cognition.

## Core rule

If the system is replacing semantic judgment with branch tables, keyword rules, threshold sheets, or canned templates, it is probably falling back to legacy automation.

## Common symptoms

- keyword-based intent routing
- exact-match retrieval for fuzzy knowledge tasks
- regex-only extraction for messy unstructured documents
- brittle selector scripts for changing UIs
- manual tool routers instead of model-selected tools
- fully predetermined chains for tasks that need runtime adaptation
- canned drafting instead of grounded generation
- threshold tables for messy human-style judgment
- command parsers instead of tool-using agent loops

## Review process

1. State what the system is trying to accomplish.
2. Mark where reasoning or judgment is actually required.
3. Identify which parts were turned into keyword, rule, or template logic.
4. Decide whether those deterministic pieces are support infrastructure or misplaced cognition.
5. Name the fallback patterns present.
6. Propose the LLM-native correction.

## Output
### Goal
### Misplaced deterministic cognition
### Fallback patterns found
### What the LLM should own
### What deterministic systems should own
### Recommended correction

