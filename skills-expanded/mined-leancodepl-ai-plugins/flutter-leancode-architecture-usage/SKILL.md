---
name: flutter-leancode-architecture-usage
description: Explain what the `flutter-leancode-architecture` plugin does and how to use it. Use when the user invokes `/flutter-leancode-architecture-usage`, asks what this plugin covers, or needs help with project structure, error handling, logging, or cross-plugin architecture choices.
---

# Architecture Usage

## How to respond

- If the user invoked this skill without a concrete task, start by explaining what this plugin covers.
- Show how to use it through concrete architecture tasks such as scaffolding, reviewing, or choosing the next plugin.
- Point to the most relevant rule or specialized skill, and route to sibling plugins when the task becomes DI, navigation, analytics, localization, or state management specific.
- If the user already gave a concrete architecture task, briefly explain why this plugin fits and then do the work.
- Do not reply with filler like "skill loaded", "ready for the task", or "what would you like to do?" before explaining the plugin.

## What this plugin does

- Covers LeanCode Flutter architecture standards for project structure, error handling, and logging.
- Helps decide when a task belongs here versus a dedicated plugin for DI, navigation, analytics, localization, or state management.

## How to use it

- Ask to scaffold a new feature aligned with LeanCode architecture.
- Ask for an architecture review of an existing feature or folder.
- Ask how to structure files, handle errors, or apply logging safely.
- Ask which related plugin should be used next for a concrete implementation task.

## Example requests

- "Scaffold a new booking feature using LeanCode architecture."
- "Review `lib/features/booking/` for architecture drift."
- "Which plugin should I use next for navigation and DI in this feature?"

## Reach for these assets

- `references/project-structure.md` - feature structure and organization.
- `references/error-handling.md` - failures, retries, and error UX.
- `references/logging.md` - logging conventions and security guardrails.
- `skills/review-leancode-arch/SKILL.md` - systematic architecture review.
- `skills/scaffold-feature/SKILL.md` - feature scaffolding workflow.
- If the task becomes DI, navigation, analytics, localization, or state-management specific, switch to the matching dedicated plugin.
