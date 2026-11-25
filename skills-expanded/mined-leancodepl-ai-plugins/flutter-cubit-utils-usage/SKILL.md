---
name: flutter-cubit-utils-usage
description: Explain what the `flutter-cubit-utils` plugin does and how to use it. Use when the user invokes `/flutter-cubit-utils-usage`, asks what this plugin covers, or needs help choosing a cubit-utils base class or recipe.
---

# Cubit Utils Usage

## How to respond

- If the user invoked this skill without a concrete task, start by explaining what this plugin does and when it is the right choice.
- Show how to use it with concrete base-cubit decisions and recipe-style tasks.
- Route to the matching rule for list, details, or action cubits, and point to sibling plugins only when the task is really about CQRS contracts or general BLoC state modeling.
- If the user already gave a concrete cubit-utils task, briefly explain why this plugin fits and then do the work.
- Do not reply with filler like "skill loaded", "ready for the task", or "what would you like to do?" before explaining the plugin.

## What this plugin does

- Covers base classes from `leancode_cubit_utils` and `leancode_cubit_utils_cqrs`.
- Helps choose between `RequestCubit`, `ArgsRequestCubit`, `PaginatedCubit`, `QueryCubit`, and `PaginatedQueryCubit`.
- Provides canonical recipes for paginated list, details, and action cubits.
- Clarifies the boundary between cubit-utils rules here, CQRS contracts in `flutter-cqrs`, and broader state-management guidance in `flutter-bloc`.

## How to use it

- Ask which base cubit fits a new screen or use case.
- Ask to scaffold or refactor a list, details, or action cubit.
- Ask to migrate an ad-hoc cubit to one of the standard base classes.
- Ask whether a problem belongs here, in `flutter-cqrs`, or in `flutter-bloc`.

## Example requests

- "Which cubit base class should I use for a paginated bookings list?"
- "Refactor this details cubit to `ArgsReactiveQueryCubit`."
- "Do I need `flutter-cubit-utils` here, or is this just a plain BLoC task?"

## Reach for these assets

- `references/cubit-utils.md` - base classes and when to use them.
- `references/cubit-list.md` - paginated list cubit recipe.
- `references/cubit-details.md` - details and single-object cubit recipe.
- `references/cubit-action.md` - command and action cubit variants.
- Related plugin: `flutter-cqrs` - CQRS contracts, commands, queries, and data-access boundaries.
- Related plugin: `flutter-bloc` - general BLoC/Cubit state modeling and presentation patterns.
