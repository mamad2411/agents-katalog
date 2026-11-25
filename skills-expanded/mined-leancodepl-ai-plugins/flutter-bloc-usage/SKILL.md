---
name: flutter-bloc-usage
description: Explain what the `flutter-bloc` plugin does and how to use it. Use when the user invokes `/flutter-bloc-usage`, asks what this plugin covers, or needs help with Cubit/BLoC state modeling, presentation effects, or the boundary with `flutter-cubit-utils`.
---

# BLoC Usage

## How to respond

- If the user invoked this skill without a concrete task, start by explaining what this plugin covers and where its boundaries are.
- Show how to use it with concrete state-management tasks this plugin can handle.
- Point to the main rule here, or route the user to `flutter-cubit-utils` when the task is really about base cubits and canonical recipes.
- If the user already gave a concrete BLoC/Cubit task, briefly explain why this plugin fits and then do the work.
- Do not reply with filler like "skill loaded", "ready for the task", or "what would you like to do?" before explaining the plugin.

## What this plugin does

- Covers LeanCode conventions for `bloc` and `flutter_bloc`.
- Covers presentation side effects with `bloc_presentation`.
- Covers widget state-read simplifications like replacing a top-level `BlocBuilder` with `context.watch` when that refactor is safe.
- Clarifies the boundary between general BLoC guidance here and base-cubit recipes in `flutter-cubit-utils`.

## How to use it

- Ask to design or refactor cubit state for a feature.
- Ask how to model presentation events for snackbars, dialogs, or navigation side effects.
- Ask to simplify a widget tree that uses a root `BlocBuilder` only to pass through cubit state.
- Ask whether a task belongs here or in `flutter-cubit-utils`.
- Ask for a review of a cubit/widget pair against LeanCode state-management rules.

## Example requests

- "Refactor this cubit state to follow LeanCode BLoC conventions."
- "How should I model a snackbar or navigation side effect from this cubit?"
- "Does this belong in `flutter-bloc` or `flutter-cubit-utils`?"

## Reach for these assets

- `references/state-management.md` - main BLoC/Cubit fundamentals.
- `skills/flutter-context-watch-instead-of-top-builder/SKILL.md` - focused workflow for replacing a top-level `BlocBuilder` with `context.watch`.
- Related plugin: `flutter-cubit-utils` - base classes and canonical recipes for `QueryCubit`, `PaginatedQueryCubit`, `RequestCubit`, and related cubits.
- If the task is mainly about choosing or implementing a base cubit, switch to `flutter-cubit-utils`.
