---
name: flutter-cqrs-usage
description: Explain what the `flutter-cqrs` plugin does and how to use it. Use when the user invokes `/flutter-cqrs-usage`, asks what this plugin covers, or needs help with queries, commands, repositories, or CQRS boundaries.
---

# CQRS Usage

## How to respond

- If the user invoked this skill without a concrete task, start with a short explanation of what this plugin does and when it should be used.
- Show how to use it through concrete CQRS tasks this plugin can handle.
- Point to the main rule or the `data-access` skill, and route to `flutter-cubit-utils` when the task is really about base cubit selection.
- If the user already gave a concrete CQRS task, briefly explain why this plugin fits and then do the work.
- Do not reply with filler like "skill loaded", "ready for the task", or "what would you like to do?" before explaining the plugin.

## What this plugin does

- Covers CQRS contracts, commands, queries, operations, and `Cqrs` client usage.
- Covers contract generation and repository boundaries.
- Clarifies when work should move to `flutter-cubit-utils` for base cubits and cubit recipes.

## How to use it

- Ask to implement a new query or command.
- Ask whether to call `Cqrs` directly or introduce a repository boundary.
- Ask to refactor ad-hoc API code toward generated contracts.
- Ask whether a task belongs here or in `flutter-cubit-utils`.

## Example requests

- "Implement the CQRS query for booking details."
- "Should this mutation go through a repository or direct `cqrs.run`?"
- "Refactor this feature from manual API calls to generated contracts."

## Reach for these assets

- `references/cqrs-data-access.md` - CQRS conventions and boundaries.
- `skills/data-access/SKILL.md` - data-access workflow.
- `skills/data-access/reference.md` - quick reference for commands, queries, contracts, and repositories.
- Related plugin: `flutter-cubit-utils` - base classes and canonical recipes for `QueryCubit`, `PaginatedQueryCubit`, and request flows.
- If the task is mainly about choosing or shaping a base cubit, switch to `flutter-cubit-utils`.
