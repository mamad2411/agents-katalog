---
name: flutter-di-usage
description: Explain what the `flutter-di` plugin does and how to use it. Use when the user invokes `/flutter-di-usage`, asks what this plugin covers, or needs help wiring providers, choosing dependency scope, or planning async initialization.
---

# DI Usage

## How to respond

- If the user invoked this skill without a concrete task, start by explaining what this plugin does and when it should be used.
- Show how to use it through concrete DI tasks, especially provider wiring and scope decisions.
- Point to the main rule here, or route to `flutter-bloc` when the task is really about cubit logic after dependencies are provided.
- If the user already gave a concrete DI task, briefly explain why this plugin fits and then do the work.
- Do not reply with filler like "skill loaded", "ready for the task", or "what would you like to do?" before explaining the plugin.

## What this plugin does

- Covers LeanCode `provider`-based dependency injection in Flutter features.
- Covers provider scope, page-scoped dependencies, and `GlobalProviders`.
- Covers creating dependency values directly in the provider's `create` function.
- Covers simple asynchronous global dependency initialization in `main()`.

## How to use it

- Ask to wire dependencies for a new page or feature.
- Ask whether a dependency should live at page scope or global scope.
- Ask to refactor a provider so values are created directly in `create:`.
- Ask whether async setup belongs in `main()`.

## Example requests

- "Wire the dependencies for this booking page with `provider`."
- "Should this service live in `GlobalProviders` or stay local to the route?"
- "Should this dependency be initialized in `main()` or provided later?"

## Reach for these assets

- `references/dependency-injection.md` - LeanCode DI rules and guardrails.
- Related plugin: `flutter-bloc` - cubit/bloc state-management patterns after dependencies are provided.
