---
name: flutter-navigation-usage
description: Explain what the `flutter-navigation` plugin does and how to use it. Use when the user invokes `/flutter-navigation-usage`, asks what this plugin covers, or needs help with `auto_route`, `go_router`, route trees, deep links, guards, or navigation flow changes.
---

# Navigation Usage

## How to respond

- If the user invoked this skill without a concrete task, start with a short explanation of what this plugin does and when it should be used.
- Show how to use it through concrete navigation tasks this plugin can handle.
- Point to the router-selection rule first, then the matching router-specific rule. Route to related plugins only when the task expands into DI or broader architecture decisions.
- If the user already gave a concrete navigation task, briefly explain why this plugin fits and then do the work.
- Before applying router-specific conventions, inspect `pubspec.yaml` and existing route files to decide whether the project uses `auto_route` or `go_router`. If both are present during a migration, follow the convention already used by the edited route tree unless the user asks to migrate it.
- Do not reply with filler like "skill loaded", "ready for the task", or "what would you like to do?" before explaining the plugin.

## What this plugin does

- Covers LeanCode navigation conventions for both `auto_route` and `go_router` projects.
- Guides route naming, paths, parameters, data passing, typed route APIs, and deep-link boundaries.
- Covers `auto_route` concepts such as `@RoutePage`, `AppRouter`, generated route classes, guards, and `AutoTabsRouter`.
- Covers `go_router` concepts such as `AppGoRoute`, `route_tree.dart`, package-level `*_routes.dart`, and typed shell routes.

## How to use it

- Ask to add a new page route.
- Ask to refactor route hierarchy, path structure, or shell navigation.
- Ask to debug navigation behavior around `navigateTo`, `pushRoute`, `go`, `push`, guards, or generated routes.
- Ask for help deciding how route boundaries should interact with page structure and DI.

## Example requests

- "Add a typed route for the booking details page."
- "Refactor this feature to use an AutoTabsRouter shell."
- "Why should this value be a path parameter instead of a regular constructor argument?"

## Reach for these references

Read `references/navigation.md` first, then the one that matches the project's router:

- `references/navigation.md` - router selection and shared LeanCode navigation conventions.
- `references/navigation-auto-route.md` - conventions for projects using `auto_route`.
- `references/navigation-go-router.md` - conventions for projects using `go_router`.
- Related plugin: `flutter-di` - page entrypoints and dependency scoping that interact with route boundaries.
- Related plugin: `flutter-leancode-architecture` - feature structure and cross-cutting architecture rules around pages.
