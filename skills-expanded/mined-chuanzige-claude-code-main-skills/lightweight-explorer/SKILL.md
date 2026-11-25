---
name: lightweight-explorer
description: Use when the task is codebase exploration rather than modification, and you need a fast, read-only search pattern that starts broad when location is unknown, narrows when location is known, and parallelizes independent searches
---

# Lightweight Explorer

## Overview

Explore cheaply. This pattern is based on the built-in explore agent in `src/tools/AgentTool/built-in/exploreAgent.ts` and the read-only command rules in the bash tooling.

The explorer's job is to find, read, and report, not to edit.

## Three Properties

A lightweight exploration task should be:

- read-only
- quick
- low-cost

If the task needs edits, stop using this skill and switch to an implementation workflow.

## Search Strategy

### Unknown location

Start broad:

- file globbing
- filename search
- symbol search
- text grep
- test-name search

Search multiple angles in parallel when they are independent.

### Known location

Read narrowly:

- exact file reads
- nearby callers
- adjacent tests
- local imports and exports

Do not keep globbing the whole repo when you already know the file.

### Nothing found

Change search axis instead of repeating the same failed query:

- filename to symbol
- symbol to caller
- implementation to tests
- exact string to regex variant

## Read-Only Rule

Do not:

- edit files
- create temp files
- write shell redirects
- run state-changing commands

Use only read-only tools and commands.

## Reporting Style

Return:

- the files you found
- the most relevant lines or functions
- what each file contributes
- any obvious gaps or next search paths

Keep it concise. Exploration should shorten the path to the next decision.

## Anti-Patterns

- editing while "just exploring"
- running the same failed search repeatedly
- reading large files end to end before narrowing scope
- serializing obviously independent searches

## Done Condition

You have applied this skill correctly when the task stays read-only, the search narrows as evidence improves, and the result gives the next agent enough context without paying modification cost.
